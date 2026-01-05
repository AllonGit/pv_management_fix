from __future__ import annotations

from datetime import date
from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo, EntityCategory

from .const import DOMAIN, DATA_CTRL, CONF_NAME


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
):
    """Setup der Sensoren."""
    ctrl = hass.data[DOMAIN][entry.entry_id][DATA_CTRL]
    name = entry.data.get(CONF_NAME, "PV Amortisation")

    entities = [
        # === Haupt-Sensoren (Übersicht) ===
        AmortisationPercentSensor(ctrl, name),
        TotalSavingsSensor(ctrl, name),
        RemainingCostSensor(ctrl, name),
        StatusSensor(ctrl, name),

        # === Energie-Sensoren ===
        SelfConsumptionSensor(ctrl, name),
        FeedInSensor(ctrl, name),
        PVProductionSensor(ctrl, name),

        # === Finanz-Sensoren ===
        SavingsSelfConsumptionSensor(ctrl, name),
        EarningsFeedInSensor(ctrl, name),

        # === Effizienz-Sensoren ===
        SelfConsumptionRatioSensor(ctrl, name),
        AutarkyRateSensor(ctrl, name),

        # === Statistik-Sensoren ===
        AverageDailySavingsSensor(ctrl, name),
        AverageMonthlySavingsSensor(ctrl, name),
        AverageYearlySavingsSensor(ctrl, name),
        DaysSinceInstallationSensor(ctrl, name),

        # === Prognose-Sensoren ===
        EstimatedRemainingDaysSensor(ctrl, name),
        EstimatedPaybackDateSensor(ctrl, name),

        # === Umwelt-Sensoren ===
        CO2SavedSensor(ctrl, name),

        # === Konfigurations-Sensoren (Diagnose) ===
        CurrentElectricityPriceSensor(ctrl, name),
        CurrentFeedInTariffSensor(ctrl, name),
        InstallationCostSensor(ctrl, name),
    ]

    async_add_entities(entities)


class BaseEntity(SensorEntity):
    """Basis-Klasse für alle Sensoren."""

    _attr_should_poll = False

    def __init__(
        self,
        ctrl,
        name: str,
        key: str,
        unit=None,
        icon=None,
        state_class=None,
        device_class=None,
        entity_category=None,
    ):
        self.ctrl = ctrl
        self._attr_name = f"{name} {key}"
        uid_name = "".join(c if c.isalnum() else "_" for c in name).lower()
        self._attr_unique_id = f"{DOMAIN}_{uid_name}_{key.lower().replace(' ', '_')}"
        self._attr_native_unit_of_measurement = unit
        self._attr_icon = icon
        self._attr_state_class = state_class
        self._attr_device_class = device_class
        self._attr_entity_category = entity_category
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, name)},
            name=name,
            manufacturer="Custom",
            model="PV Amortisation Tracker",
        )

    async def async_added_to_hass(self):
        self.ctrl.register_entity_listener(self._on_ctrl_update)

    @callback
    def _on_ctrl_update(self):
        self.async_write_ha_state()


# =============================================================================
# HAUPT-SENSOREN
# =============================================================================


class AmortisationPercentSensor(BaseEntity):
    """Amortisation in Prozent - Hauptindikator."""

    def __init__(self, ctrl, name: str):
        super().__init__(
            ctrl,
            name,
            "Amortisation",
            unit="%",
            icon="mdi:percent-circle",
            state_class=SensorStateClass.MEASUREMENT,
        )

    @property
    def native_value(self) -> float:
        return round(self.ctrl.amortisation_percent, 2)

    @property
    def extra_state_attributes(self):
        return {
            "total_savings": f"{self.ctrl.total_savings:.2f}€",
            "installation_cost": f"{self.ctrl.installation_cost:.2f}€",
            "remaining": f"{self.ctrl.remaining_cost:.2f}€",
            "is_amortised": self.ctrl.is_amortised,
        }


class TotalSavingsSensor(BaseEntity):
    """Gesamtersparnis in Euro."""

    def __init__(self, ctrl, name: str):
        super().__init__(
            ctrl,
            name,
            "Gesamtersparnis",
            unit="€",
            icon="mdi:cash-plus",
            state_class=SensorStateClass.TOTAL,
            device_class=SensorDeviceClass.MONETARY,
        )

    @property
    def native_value(self) -> float:
        return round(self.ctrl.total_savings, 2)

    @property
    def extra_state_attributes(self):
        return {
            "savings_self_consumption": f"{self.ctrl.savings_self_consumption:.2f}€",
            "earnings_feed_in": f"{self.ctrl.earnings_feed_in:.2f}€",
            "offset": f"{self.ctrl.savings_offset:.2f}€",
        }


class RemainingCostSensor(BaseEntity):
    """Verbleibender Betrag bis Amortisation."""

    def __init__(self, ctrl, name: str):
        super().__init__(
            ctrl,
            name,
            "Restbetrag",
            unit="€",
            icon="mdi:cash-minus",
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.MONETARY,
        )

    @property
    def native_value(self) -> float:
        return round(self.ctrl.remaining_cost, 2)

    @property
    def icon(self) -> str:
        if self.ctrl.is_amortised:
            return "mdi:cash-check"
        return "mdi:cash-minus"


class StatusSensor(BaseEntity):
    """Status-Text (z.B. '45.2% amortisiert' oder 'Amortisiert!')."""

    def __init__(self, ctrl, name: str):
        super().__init__(
            ctrl,
            name,
            "Status",
            icon="mdi:solar-power-variant",
        )

    @property
    def native_value(self) -> str:
        return self.ctrl.status_text

    @property
    def icon(self) -> str:
        if self.ctrl.is_amortised:
            return "mdi:party-popper"
        elif self.ctrl.amortisation_percent >= 75:
            return "mdi:trending-up"
        elif self.ctrl.amortisation_percent >= 50:
            return "mdi:solar-power-variant"
        else:
            return "mdi:solar-panel"

    @property
    def extra_state_attributes(self):
        attrs = {
            "percent": f"{self.ctrl.amortisation_percent:.1f}%",
            "total_savings": f"{self.ctrl.total_savings:.2f}€",
            "remaining": f"{self.ctrl.remaining_cost:.2f}€",
        }
        if self.ctrl.is_amortised:
            profit = self.ctrl.total_savings - self.ctrl.installation_cost
            attrs["profit"] = f"{profit:.2f}€"
        return attrs


# =============================================================================
# ENERGIE-SENSOREN
# =============================================================================


class SelfConsumptionSensor(BaseEntity):
    """Eigenverbrauch in kWh."""

    def __init__(self, ctrl, name: str):
        super().__init__(
            ctrl,
            name,
            "Eigenverbrauch",
            unit="kWh",
            icon="mdi:home-lightning-bolt",
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
        )

    @property
    def native_value(self) -> float:
        return round(self.ctrl.self_consumption_kwh, 2)


class FeedInSensor(BaseEntity):
    """Netzeinspeisung in kWh."""

    def __init__(self, ctrl, name: str):
        super().__init__(
            ctrl,
            name,
            "Einspeisung",
            unit="kWh",
            icon="mdi:transmission-tower-export",
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
        )

    @property
    def native_value(self) -> float:
        return round(self.ctrl.feed_in_kwh, 2)


class PVProductionSensor(BaseEntity):
    """PV-Produktion in kWh (gespiegelt vom Input-Sensor)."""

    def __init__(self, ctrl, name: str):
        super().__init__(
            ctrl,
            name,
            "PV Produktion",
            unit="kWh",
            icon="mdi:solar-power",
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.ENERGY,
            entity_category=EntityCategory.DIAGNOSTIC,
        )

    @property
    def native_value(self) -> float:
        return round(self.ctrl.pv_production_kwh, 2)


# =============================================================================
# FINANZ-SENSOREN
# =============================================================================


class SavingsSelfConsumptionSensor(BaseEntity):
    """Ersparnis durch Eigenverbrauch."""

    def __init__(self, ctrl, name: str):
        super().__init__(
            ctrl,
            name,
            "Ersparnis Eigenverbrauch",
            unit="€",
            icon="mdi:piggy-bank",
            state_class=SensorStateClass.TOTAL,
            device_class=SensorDeviceClass.MONETARY,
        )

    @property
    def native_value(self) -> float:
        return round(self.ctrl.savings_self_consumption, 2)

    @property
    def extra_state_attributes(self):
        return {
            "self_consumption_kwh": f"{self.ctrl.self_consumption_kwh:.2f} kWh",
            "electricity_price": f"{self.ctrl.current_electricity_price:.4f} €/kWh",
        }


class EarningsFeedInSensor(BaseEntity):
    """Einnahmen durch Einspeisung."""

    def __init__(self, ctrl, name: str):
        super().__init__(
            ctrl,
            name,
            "Einnahmen Einspeisung",
            unit="€",
            icon="mdi:cash-plus",
            state_class=SensorStateClass.TOTAL,
            device_class=SensorDeviceClass.MONETARY,
        )

    @property
    def native_value(self) -> float:
        return round(self.ctrl.earnings_feed_in, 2)

    @property
    def extra_state_attributes(self):
        return {
            "feed_in_kwh": f"{self.ctrl.feed_in_kwh:.2f} kWh",
            "feed_in_tariff": f"{self.ctrl.current_feed_in_tariff:.4f} €/kWh",
        }


# =============================================================================
# EFFIZIENZ-SENSOREN
# =============================================================================


class SelfConsumptionRatioSensor(BaseEntity):
    """Eigenverbrauchsquote in Prozent."""

    def __init__(self, ctrl, name: str):
        super().__init__(
            ctrl,
            name,
            "Eigenverbrauchsquote",
            unit="%",
            icon="mdi:home-percent",
            state_class=SensorStateClass.MEASUREMENT,
        )

    @property
    def native_value(self) -> float:
        return round(self.ctrl.self_consumption_ratio, 1)

    @property
    def extra_state_attributes(self):
        return {
            "description": "Anteil der PV-Produktion der selbst verbraucht wird",
            "self_consumption_kwh": f"{self.ctrl.self_consumption_kwh:.2f} kWh",
            "pv_production_kwh": f"{self.ctrl.pv_production_kwh:.2f} kWh",
        }


class AutarkyRateSensor(BaseEntity):
    """Autarkiegrad in Prozent."""

    def __init__(self, ctrl, name: str):
        super().__init__(
            ctrl,
            name,
            "Autarkiegrad",
            unit="%",
            icon="mdi:home-battery",
            state_class=SensorStateClass.MEASUREMENT,
        )

    @property
    def native_value(self) -> float:
        return round(self.ctrl.autarky_rate, 1)

    @property
    def extra_state_attributes(self):
        return {
            "description": "Anteil des Verbrauchs der durch PV gedeckt wird",
            "self_consumption_kwh": f"{self.ctrl.self_consumption_kwh:.2f} kWh",
            "total_consumption_kwh": f"{self.ctrl.consumption_kwh:.2f} kWh",
        }


# =============================================================================
# STATISTIK-SENSOREN
# =============================================================================


class AverageDailySavingsSensor(BaseEntity):
    """Durchschnittliche tägliche Ersparnis."""

    def __init__(self, ctrl, name: str):
        super().__init__(
            ctrl,
            name,
            "Ersparnis pro Tag",
            unit="€/Tag",
            icon="mdi:calendar-today",
            state_class=SensorStateClass.MEASUREMENT,
        )

    @property
    def native_value(self) -> float:
        return round(self.ctrl.average_daily_savings, 2)


class AverageMonthlySavingsSensor(BaseEntity):
    """Durchschnittliche monatliche Ersparnis."""

    def __init__(self, ctrl, name: str):
        super().__init__(
            ctrl,
            name,
            "Ersparnis pro Monat",
            unit="€/Monat",
            icon="mdi:calendar-month",
            state_class=SensorStateClass.MEASUREMENT,
        )

    @property
    def native_value(self) -> float:
        return round(self.ctrl.average_monthly_savings, 2)


class AverageYearlySavingsSensor(BaseEntity):
    """Durchschnittliche jährliche Ersparnis."""

    def __init__(self, ctrl, name: str):
        super().__init__(
            ctrl,
            name,
            "Ersparnis pro Jahr",
            unit="€/Jahr",
            icon="mdi:calendar",
            state_class=SensorStateClass.MEASUREMENT,
        )

    @property
    def native_value(self) -> float:
        return round(self.ctrl.average_yearly_savings, 2)


class DaysSinceInstallationSensor(BaseEntity):
    """Tage seit Installation."""

    def __init__(self, ctrl, name: str):
        super().__init__(
            ctrl,
            name,
            "Tage seit Installation",
            unit="Tage",
            icon="mdi:calendar-clock",
            state_class=SensorStateClass.TOTAL_INCREASING,
        )

    @property
    def native_value(self) -> int:
        return self.ctrl.days_since_installation


# =============================================================================
# PROGNOSE-SENSOREN
# =============================================================================


class EstimatedRemainingDaysSensor(BaseEntity):
    """Geschätzte verbleibende Tage bis Amortisation."""

    def __init__(self, ctrl, name: str):
        super().__init__(
            ctrl,
            name,
            "Restlaufzeit",
            unit="Tage",
            icon="mdi:timer-sand",
            state_class=SensorStateClass.MEASUREMENT,
        )

    @property
    def native_value(self) -> int | None:
        return self.ctrl.estimated_remaining_days

    @property
    def extra_state_attributes(self):
        remaining = self.ctrl.estimated_remaining_days
        if remaining is None:
            return {"status": "Berechnung nicht möglich"}

        years = remaining // 365
        months = (remaining % 365) // 30
        days = remaining % 30

        parts = []
        if years > 0:
            parts.append(f"{years} Jahr{'e' if years > 1 else ''}")
        if months > 0:
            parts.append(f"{months} Monat{'e' if months > 1 else ''}")
        if days > 0 or not parts:
            parts.append(f"{days} Tag{'e' if days != 1 else ''}")

        return {
            "formatted": ", ".join(parts),
            "years": years,
            "months": months,
            "days": days,
        }


class EstimatedPaybackDateSensor(BaseEntity):
    """Geschätztes Amortisationsdatum."""

    def __init__(self, ctrl, name: str):
        super().__init__(
            ctrl,
            name,
            "Amortisationsdatum",
            icon="mdi:calendar-check",
            device_class=SensorDeviceClass.DATE,
        )

    @property
    def native_value(self) -> date | None:
        return self.ctrl.estimated_payback_date

    @property
    def icon(self) -> str:
        if self.ctrl.is_amortised:
            return "mdi:calendar-check"
        return "mdi:calendar-question"


# =============================================================================
# UMWELT-SENSOREN
# =============================================================================


class CO2SavedSensor(BaseEntity):
    """Eingesparte CO2-Emissionen."""

    def __init__(self, ctrl, name: str):
        super().__init__(
            ctrl,
            name,
            "CO2 Ersparnis",
            unit="kg",
            icon="mdi:molecule-co2",
            state_class=SensorStateClass.TOTAL_INCREASING,
        )

    @property
    def native_value(self) -> float:
        return round(self.ctrl.co2_saved_kg, 1)

    @property
    def extra_state_attributes(self):
        kg = self.ctrl.co2_saved_kg
        return {
            "tonnes": f"{kg / 1000:.2f} t",
            "trees_equivalent": int(kg / 21),  # ~21kg CO2 pro Baum/Jahr
            "car_km_equivalent": int(kg / 0.12),  # ~120g CO2 pro km
        }


# =============================================================================
# KONFIGURATIONS-SENSOREN (DIAGNOSE)
# =============================================================================


class CurrentElectricityPriceSensor(BaseEntity):
    """Aktueller Strompreis."""

    def __init__(self, ctrl, name: str):
        super().__init__(
            ctrl,
            name,
            "Strompreis",
            unit="€/kWh",
            icon="mdi:currency-eur",
            state_class=SensorStateClass.MEASUREMENT,
            entity_category=EntityCategory.DIAGNOSTIC,
        )

    @property
    def native_value(self) -> float:
        return round(self.ctrl.current_electricity_price, 4)

    @property
    def extra_state_attributes(self):
        return {
            "source": "sensor" if self.ctrl.electricity_price_entity else "config",
            "config_value": f"{self.ctrl.electricity_price:.4f} €/kWh",
        }


class CurrentFeedInTariffSensor(BaseEntity):
    """Aktuelle Einspeisevergütung."""

    def __init__(self, ctrl, name: str):
        super().__init__(
            ctrl,
            name,
            "Einspeisevergütung",
            unit="€/kWh",
            icon="mdi:currency-eur",
            state_class=SensorStateClass.MEASUREMENT,
            entity_category=EntityCategory.DIAGNOSTIC,
        )

    @property
    def native_value(self) -> float:
        return round(self.ctrl.current_feed_in_tariff, 4)

    @property
    def extra_state_attributes(self):
        return {
            "source": "sensor" if self.ctrl.feed_in_tariff_entity else "config",
            "config_value": f"{self.ctrl.feed_in_tariff:.4f} €/kWh",
        }


class InstallationCostSensor(BaseEntity):
    """Anschaffungskosten der PV-Anlage."""

    def __init__(self, ctrl, name: str):
        super().__init__(
            ctrl,
            name,
            "Anschaffungskosten",
            unit="€",
            icon="mdi:cash",
            device_class=SensorDeviceClass.MONETARY,
            entity_category=EntityCategory.DIAGNOSTIC,
        )

    @property
    def native_value(self) -> float:
        return round(self.ctrl.installation_cost, 2)
