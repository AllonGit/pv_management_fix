from __future__ import annotations

import logging
import time
from datetime import datetime, date
from collections import deque

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback, Event
from homeassistant.const import EVENT_STATE_CHANGED, STATE_UNAVAILABLE, STATE_UNKNOWN

from .const import (
    DOMAIN, DATA_CTRL, PLATFORMS,
    CONF_PV_PRODUCTION_ENTITY, CONF_GRID_EXPORT_ENTITY,
    CONF_GRID_IMPORT_ENTITY, CONF_CONSUMPTION_ENTITY,
    CONF_ELECTRICITY_PRICE, CONF_ELECTRICITY_PRICE_ENTITY, CONF_ELECTRICITY_PRICE_UNIT,
    CONF_FEED_IN_TARIFF, CONF_FEED_IN_TARIFF_ENTITY, CONF_FEED_IN_TARIFF_UNIT,
    CONF_INSTALLATION_COST, CONF_SAVINGS_OFFSET,
    CONF_ENERGY_OFFSET_SELF, CONF_ENERGY_OFFSET_EXPORT,
    CONF_INSTALLATION_DATE,
    DEFAULT_ELECTRICITY_PRICE, DEFAULT_FEED_IN_TARIFF,
    DEFAULT_INSTALLATION_COST, DEFAULT_SAVINGS_OFFSET,
    DEFAULT_ENERGY_OFFSET_SELF, DEFAULT_ENERGY_OFFSET_EXPORT,
    DEFAULT_ELECTRICITY_PRICE_UNIT, DEFAULT_FEED_IN_TARIFF_UNIT,
    PRICE_UNIT_CENT,
)

_LOGGER = logging.getLogger(__name__)

# CO2 Faktor für deutschen Strommix (kg CO2 pro kWh)
CO2_FACTOR_GRID = 0.4


class PVAmortisationController:
    """Controller für PV-Amortisationsberechnung."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        self.hass = hass
        self.entry = entry

        # Input-Entitäten
        self.pv_production_entity = entry.data.get(CONF_PV_PRODUCTION_ENTITY)
        self.grid_export_entity = entry.data.get(CONF_GRID_EXPORT_ENTITY)
        self.grid_import_entity = entry.data.get(CONF_GRID_IMPORT_ENTITY)
        self.consumption_entity = entry.data.get(CONF_CONSUMPTION_ENTITY)

        # Konfigurierbare Werte (aus Options, fallback zu data)
        self._load_options()

        # Aktuelle Sensor-Werte
        self._pv_production_kwh = 0.0
        self._grid_export_kwh = 0.0
        self._grid_import_kwh = 0.0
        self._consumption_kwh = 0.0

        # Berechnete Werte
        self._self_consumption_kwh = 0.0
        self._savings_self_consumption = 0.0
        self._earnings_feed_in = 0.0
        self._total_savings = 0.0

        # Historische Daten für Durchschnittsberechnungen
        self._daily_savings_history = deque(maxlen=365)  # 1 Jahr
        self._last_day_savings = 0.0
        self._last_calculation_day = None
        self._first_seen_date = None

        # Listener
        self._remove_listeners = []
        self._entity_listeners = []

    def _load_options(self):
        """Lädt Optionen aus Entry (Options überschreiben Data)."""
        opts = {**self.entry.data, **self.entry.options}

        self.electricity_price = opts.get(CONF_ELECTRICITY_PRICE, DEFAULT_ELECTRICITY_PRICE)
        self.electricity_price_entity = opts.get(CONF_ELECTRICITY_PRICE_ENTITY)
        self.electricity_price_unit = opts.get(CONF_ELECTRICITY_PRICE_UNIT, DEFAULT_ELECTRICITY_PRICE_UNIT)
        self.feed_in_tariff = opts.get(CONF_FEED_IN_TARIFF, DEFAULT_FEED_IN_TARIFF)
        self.feed_in_tariff_entity = opts.get(CONF_FEED_IN_TARIFF_ENTITY)
        self.feed_in_tariff_unit = opts.get(CONF_FEED_IN_TARIFF_UNIT, DEFAULT_FEED_IN_TARIFF_UNIT)
        self.installation_cost = opts.get(CONF_INSTALLATION_COST, DEFAULT_INSTALLATION_COST)
        self.savings_offset = opts.get(CONF_SAVINGS_OFFSET, DEFAULT_SAVINGS_OFFSET)
        self.energy_offset_self = opts.get(CONF_ENERGY_OFFSET_SELF, DEFAULT_ENERGY_OFFSET_SELF)
        self.energy_offset_export = opts.get(CONF_ENERGY_OFFSET_EXPORT, DEFAULT_ENERGY_OFFSET_EXPORT)
        self.installation_date = opts.get(CONF_INSTALLATION_DATE)

    def _convert_price_to_eur(self, price: float, unit: str) -> float:
        """Konvertiert Preis zu Euro/kWh (von Cent falls nötig)."""
        if unit == PRICE_UNIT_CENT:
            return price / 100.0
        return price

    def _get_dynamic_price(self, entity_id: str | None, fallback: float) -> float:
        """Holt dynamischen Preis von Sensor oder verwendet Fallback."""
        if not entity_id:
            return fallback

        state = self.hass.states.get(entity_id)
        if state and state.state not in (STATE_UNAVAILABLE, STATE_UNKNOWN):
            try:
                return float(state.state)
            except (ValueError, TypeError):
                pass
        return fallback

    @property
    def current_electricity_price(self) -> float:
        """Aktueller Strompreis in €/kWh (dynamisch oder statisch, konvertiert von Cent falls nötig)."""
        raw_price = self._get_dynamic_price(self.electricity_price_entity, self.electricity_price)
        return self._convert_price_to_eur(raw_price, self.electricity_price_unit)

    @property
    def current_feed_in_tariff(self) -> float:
        """Aktuelle Einspeisevergütung in €/kWh (dynamisch oder statisch, konvertiert von Cent falls nötig)."""
        raw_tariff = self._get_dynamic_price(self.feed_in_tariff_entity, self.feed_in_tariff)
        return self._convert_price_to_eur(raw_tariff, self.feed_in_tariff_unit)

    @property
    def pv_production_kwh(self) -> float:
        return self._pv_production_kwh

    @property
    def grid_export_kwh(self) -> float:
        return self._grid_export_kwh

    @property
    def grid_import_kwh(self) -> float:
        return self._grid_import_kwh

    @property
    def consumption_kwh(self) -> float:
        return self._consumption_kwh

    @property
    def self_consumption_kwh(self) -> float:
        """Eigenverbrauch inkl. Offset."""
        return self._self_consumption_kwh + self.energy_offset_self

    @property
    def feed_in_kwh(self) -> float:
        """Einspeisung inkl. Offset."""
        return self._grid_export_kwh + self.energy_offset_export

    @property
    def savings_self_consumption(self) -> float:
        """Ersparnis durch Eigenverbrauch."""
        return self.self_consumption_kwh * self.current_electricity_price

    @property
    def earnings_feed_in(self) -> float:
        """Einnahmen durch Einspeisung."""
        return self.feed_in_kwh * self.current_feed_in_tariff

    @property
    def total_savings(self) -> float:
        """Gesamtersparnis inkl. Offset."""
        return self.savings_self_consumption + self.earnings_feed_in + self.savings_offset

    @property
    def amortisation_percent(self) -> float:
        """Amortisation in Prozent."""
        if self.installation_cost <= 0:
            return 100.0
        return min(100.0, (self.total_savings / self.installation_cost) * 100)

    @property
    def remaining_cost(self) -> float:
        """Restbetrag bis zur Amortisation."""
        return max(0.0, self.installation_cost - self.total_savings)

    @property
    def is_amortised(self) -> bool:
        """True wenn vollständig amortisiert."""
        return self.total_savings >= self.installation_cost

    @property
    def self_consumption_ratio(self) -> float:
        """Eigenverbrauchsquote (%)."""
        if self._pv_production_kwh <= 0:
            return 0.0
        return min(100.0, (self._self_consumption_kwh / self._pv_production_kwh) * 100)

    @property
    def autarky_rate(self) -> float:
        """Autarkiegrad (%)."""
        if self._consumption_kwh <= 0:
            return 0.0
        return min(100.0, (self._self_consumption_kwh / self._consumption_kwh) * 100)

    @property
    def co2_saved_kg(self) -> float:
        """Eingesparte CO2-Emissionen in kg."""
        return self.self_consumption_kwh * CO2_FACTOR_GRID

    @property
    def days_since_installation(self) -> int:
        """Tage seit Installation."""
        if self.installation_date:
            try:
                if isinstance(self.installation_date, str):
                    install_date = datetime.fromisoformat(self.installation_date).date()
                else:
                    install_date = self.installation_date
                return (date.today() - install_date).days
            except (ValueError, TypeError):
                pass

        if self._first_seen_date:
            return (date.today() - self._first_seen_date).days
        return 0

    @property
    def average_daily_savings(self) -> float:
        """Durchschnittliche tägliche Ersparnis."""
        days = self.days_since_installation
        if days <= 0:
            return 0.0
        return self.total_savings / days

    @property
    def average_monthly_savings(self) -> float:
        """Durchschnittliche monatliche Ersparnis."""
        return self.average_daily_savings * 30.44  # Durchschnittliche Tage pro Monat

    @property
    def average_yearly_savings(self) -> float:
        """Durchschnittliche jährliche Ersparnis."""
        return self.average_daily_savings * 365

    @property
    def estimated_remaining_days(self) -> int | None:
        """Geschätzte verbleibende Tage bis Amortisation."""
        if self.is_amortised:
            return 0
        daily_avg = self.average_daily_savings
        if daily_avg <= 0:
            return None
        return int(self.remaining_cost / daily_avg)

    @property
    def estimated_payback_date(self) -> date | None:
        """Geschätztes Amortisationsdatum."""
        remaining = self.estimated_remaining_days
        if remaining is None:
            return None
        if remaining == 0:
            return date.today()
        from datetime import timedelta
        return date.today() + timedelta(days=remaining)

    @property
    def status_text(self) -> str:
        """Status-Text für Anzeige."""
        if self.is_amortised:
            # Berechne Gewinn seit Amortisation
            profit = self.total_savings - self.installation_cost
            return f"Amortisiert! +{profit:.2f}€ Gewinn"
        else:
            return f"{self.amortisation_percent:.1f}% amortisiert"

    def register_entity_listener(self, cb) -> None:
        """Sensoren registrieren sich hier für Updates."""
        self._entity_listeners.append(cb)

    def _notify_entities(self) -> None:
        """Informiert alle Entities über Zustandsänderungen."""
        for cb in self._entity_listeners:
            try:
                cb()
            except Exception as e:
                _LOGGER.exception("Entity-Listener Fehler: %s", e)

    def _recalculate(self) -> None:
        """Berechnet alle abgeleiteten Werte neu."""
        # Eigenverbrauch berechnen
        if self.grid_export_entity:
            # Eigenverbrauch = PV Produktion - Grid Export
            self._self_consumption_kwh = max(0.0, self._pv_production_kwh - self._grid_export_kwh)
        elif self.consumption_entity and self.grid_import_entity:
            # Eigenverbrauch = Verbrauch - Netzbezug
            self._self_consumption_kwh = max(0.0, self._consumption_kwh - self._grid_import_kwh)
        else:
            # Fallback: min(PV, Verbrauch)
            self._self_consumption_kwh = min(self._pv_production_kwh, self._consumption_kwh)

        self._notify_entities()

    @callback
    def _on_state_changed(self, event: Event) -> None:
        """Handler für Zustandsänderungen der überwachten Entities."""
        entity_id = event.data.get("entity_id")
        new_state = event.data.get("new_state")

        if not new_state or new_state.state in (STATE_UNAVAILABLE, STATE_UNKNOWN):
            return

        try:
            value = float(new_state.state)
        except (ValueError, TypeError):
            return

        # Initialisiere first_seen_date
        if self._first_seen_date is None:
            self._first_seen_date = date.today()

        # Update entsprechenden Wert
        if entity_id == self.pv_production_entity:
            self._pv_production_kwh = value
        elif entity_id == self.grid_export_entity:
            self._grid_export_kwh = value
        elif entity_id == self.grid_import_entity:
            self._grid_import_kwh = value
        elif entity_id == self.consumption_entity:
            self._consumption_kwh = value
        else:
            return  # Nicht für uns

        self._recalculate()

    async def async_start(self) -> None:
        """Startet das Tracking."""
        # Initiale Werte laden
        for entity_id, attr in [
            (self.pv_production_entity, "_pv_production_kwh"),
            (self.grid_export_entity, "_grid_export_kwh"),
            (self.grid_import_entity, "_grid_import_kwh"),
            (self.consumption_entity, "_consumption_kwh"),
        ]:
            if entity_id:
                state = self.hass.states.get(entity_id)
                if state and state.state not in (STATE_UNAVAILABLE, STATE_UNKNOWN):
                    try:
                        setattr(self, attr, float(state.state))
                    except (ValueError, TypeError):
                        pass

        self._recalculate()

        # Event-Listener registrieren
        @callback
        def state_listener(event: Event):
            self._on_state_changed(event)

        self._remove_listeners.append(
            self.hass.bus.async_listen(EVENT_STATE_CHANGED, state_listener)
        )

    async def async_stop(self) -> None:
        """Stoppt das Tracking."""
        for remove in self._remove_listeners:
            remove()
        self._remove_listeners.clear()

    def set_options(self, **kwargs) -> None:
        """Setzt Optionen zur Laufzeit."""
        for key, value in kwargs.items():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)
        self._recalculate()


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Setup der Integration."""
    ctrl = PVAmortisationController(hass, entry)
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {DATA_CTRL: ctrl}

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    await ctrl.async_start()

    entry.add_update_listener(_async_update_listener)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Entlädt die Integration."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        ctrl = hass.data[DOMAIN][entry.entry_id][DATA_CTRL]
        await ctrl.async_stop()
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handler für Options-Updates."""
    await hass.config_entries.async_reload(entry.entry_id)
