from __future__ import annotations

from typing import Final
from homeassistant.const import Platform

# --- Domain / Platforms -------------------------------------------------------
DOMAIN: Final[str] = "pv_management_fix"
DATA_CTRL: Final[str] = "ctrl"

# Nur Sensor und Button - keine Switches (kein Batterie-Management bei Fixpreis)
PLATFORMS: Final[tuple[Platform, ...]] = (
    Platform.SENSOR,
    Platform.BUTTON,
)

# --- Config keys (Setup) ------------------------------------------------------
CONF_NAME: Final[str] = "name"
CONF_PV_PRODUCTION_ENTITY: Final[str] = "pv_production_entity"
CONF_GRID_EXPORT_ENTITY: Final[str] = "grid_export_entity"
CONF_GRID_IMPORT_ENTITY: Final[str] = "grid_import_entity"
CONF_CONSUMPTION_ENTITY: Final[str] = "consumption_entity"

# --- Option keys (können später geändert werden) ------------------------------
CONF_ELECTRICITY_PRICE: Final[str] = "electricity_price"
CONF_ELECTRICITY_PRICE_ENTITY: Final[str] = "electricity_price_entity"
CONF_ELECTRICITY_PRICE_UNIT: Final[str] = "electricity_price_unit"
CONF_FEED_IN_TARIFF: Final[str] = "feed_in_tariff"
CONF_FEED_IN_TARIFF_ENTITY: Final[str] = "feed_in_tariff_entity"
CONF_FEED_IN_TARIFF_UNIT: Final[str] = "feed_in_tariff_unit"

# --- Preis-Einheiten ----------------------------------------------------------
PRICE_UNIT_EUR: Final[str] = "eur"
PRICE_UNIT_CENT: Final[str] = "cent"
CONF_INSTALLATION_COST: Final[str] = "installation_cost"
CONF_SAVINGS_OFFSET: Final[str] = "savings_offset"
CONF_ENERGY_OFFSET_SELF: Final[str] = "energy_offset_self_consumption"
CONF_ENERGY_OFFSET_EXPORT: Final[str] = "energy_offset_export"
CONF_INSTALLATION_DATE: Final[str] = "installation_date"

# --- Fixpreis (Haupt-Feature dieser Integration) ------------------------------
CONF_FIXED_PRICE: Final[str] = "fixed_price"  # Der Fixpreis in ct/kWh (netto Arbeitspreis)
CONF_MARKUP_FACTOR: Final[str] = "markup_factor"  # Aufschlagfaktor für Netz+Steuern+MwSt

# --- Amortisation Helper Sync -------------------------------------------------
CONF_AMORTISATION_HELPER: Final[str] = "amortisation_helper"
CONF_RESTORE_FROM_HELPER: Final[str] = "restore_from_helper"

# --- Stromkontingent (Jahres-kWh-Budget) --------------------------------------
CONF_QUOTA_ENABLED: Final[str] = "quota_enabled"
CONF_QUOTA_YEARLY_KWH: Final[str] = "quota_yearly_kwh"
CONF_QUOTA_START_DATE: Final[str] = "quota_start_date"
CONF_QUOTA_START_METER: Final[str] = "quota_start_meter"
CONF_QUOTA_MONTHLY_RATE: Final[str] = "quota_monthly_rate"
CONF_QUOTA_SEASONAL: Final[str] = "quota_seasonal"

# --- Batterie -----------------------------------------------------------------
CONF_BATTERY_SOC_ENTITY: Final[str] = "battery_soc_entity"
CONF_BATTERY_CHARGE_ENTITY: Final[str] = "battery_charge_entity"
CONF_BATTERY_DISCHARGE_ENTITY: Final[str] = "battery_discharge_entity"
CONF_BATTERY_CAPACITY: Final[str] = "battery_capacity"
DEFAULT_BATTERY_CAPACITY: Final[float] = 10.0  # kWh

# --- Defaults -----------------------------------------------------------------
DEFAULT_NAME: Final[str] = "PV Fixpreis"
DEFAULT_ELECTRICITY_PRICE: Final[float] = 0.1092  # €/kWh (Grünwelt classic)
DEFAULT_ELECTRICITY_PRICE_UNIT: Final[str] = PRICE_UNIT_EUR
DEFAULT_FEED_IN_TARIFF: Final[float] = 0.08  # €/kWh
DEFAULT_FEED_IN_TARIFF_UNIT: Final[str] = PRICE_UNIT_EUR
DEFAULT_INSTALLATION_COST: Final[float] = 10000.0  # €
DEFAULT_SAVINGS_OFFSET: Final[float] = 0.0  # € bereits amortisiert
DEFAULT_ENERGY_OFFSET_SELF: Final[float] = 0.0  # kWh Eigenverbrauch vor Tracking
DEFAULT_ENERGY_OFFSET_EXPORT: Final[float] = 0.0  # kWh Export vor Tracking

# Fixpreis Default (Grünwelt classic netto Arbeitspreis)
DEFAULT_FIXED_PRICE: Final[float] = 10.92  # ct/kWh netto
DEFAULT_MARKUP_FACTOR: Final[float] = 2.0  # Faktor für Netz+Steuern+MwSt (10ct → 20ct brutto)

# Stromkontingent Defaults
DEFAULT_QUOTA_ENABLED: Final[bool] = False
DEFAULT_QUOTA_YEARLY_KWH: Final[float] = 4000.0  # kWh pro Jahr
DEFAULT_QUOTA_START_METER: Final[float] = 0.0  # Zählerstand bei Start
DEFAULT_QUOTA_MONTHLY_RATE: Final[float] = 0.0  # €/Monat Abschlag
DEFAULT_QUOTA_SEASONAL: Final[bool] = True

# Saisonale Gewichtungsfaktoren (deutscher Wohnstrom-Durchschnitt)
# Normalisiert auf Summe = 12 (Faktor 1.0 = Durchschnitt)
SEASONAL_FACTORS: Final[dict[int, float]] = {
    1: 1.20,   # Januar
    2: 1.15,   # Februar
    3: 1.05,   # März
    4: 0.95,   # April
    5: 0.85,   # Mai
    6: 0.75,   # Juni
    7: 0.75,   # Juli
    8: 0.80,   # August
    9: 0.90,   # September
    10: 1.00,  # Oktober
    11: 1.15,  # November
    12: 1.45,  # Dezember
}

# --- Ranges für Config Flow / Options -----------------------------------------
RANGE_PRICE_EUR: Final[dict] = {"min": 0.01, "max": 1.0, "step": 0.001}
RANGE_PRICE_CENT: Final[dict] = {"min": 1.0, "max": 100.0, "step": 0.01}
RANGE_TARIFF_EUR: Final[dict] = {"min": 0.0, "max": 0.5, "step": 0.001}
RANGE_TARIFF_CENT: Final[dict] = {"min": 0.0, "max": 50.0, "step": 0.01}
RANGE_COST: Final[dict] = {"min": 0.0, "max": 200000.0, "step": 1.0}
RANGE_OFFSET: Final[dict] = {"min": 0.0, "max": 100000.0, "step": 0.01}
RANGE_ENERGY_OFFSET: Final[dict] = {"min": 0.0, "max": 500000.0, "step": 0.01}
RANGE_MARKUP_FACTOR: Final[dict] = {"min": 1.0, "max": 5.0, "step": 0.1}

# Stromkontingent Ranges
RANGE_QUOTA_KWH: Final[dict] = {"min": 100.0, "max": 100000.0, "step": 1.0}
RANGE_QUOTA_METER: Final[dict] = {"min": 0.0, "max": 9999999.0, "step": 0.01}
RANGE_QUOTA_RATE: Final[dict] = {"min": 0.0, "max": 10000.0, "step": 0.01}
RANGE_BATTERY_CAPACITY: Final[dict] = {"min": 0.1, "max": 200.0, "step": 0.1}

# --- Benchmark ----------------------------------------------------------------
CONF_BENCHMARK_ENABLED: Final[str] = "benchmark_enabled"
CONF_BENCHMARK_HOUSEHOLD_SIZE: Final[str] = "benchmark_household_size"
CONF_BENCHMARK_COUNTRY: Final[str] = "benchmark_country"

DEFAULT_BENCHMARK_ENABLED: Final[bool] = False
DEFAULT_BENCHMARK_HOUSEHOLD_SIZE: Final[int] = 3
DEFAULT_BENCHMARK_COUNTRY: Final[str] = "AT"

# Wärmepumpe (optional, für fairen Benchmark)
CONF_BENCHMARK_HEATPUMP: Final[str] = "benchmark_heatpump"
CONF_BENCHMARK_HEATPUMP_ENTITY: Final[str] = "benchmark_heatpump_entity"
DEFAULT_BENCHMARK_HEATPUMP: Final[bool] = False

# Durchschnittlicher Jahres-Stromverbrauch OHNE WP pro Haushaltsgröße (kWh/Jahr)
# Quellen: E-Control (AT), BDEW (DE), BFE (CH) — 2023/2024 Daten
BENCHMARK_CONSUMPTION: Final[dict[str, dict[int, int]]] = {
    "AT": {1: 2200, 2: 3500, 3: 4000, 4: 4500, 5: 5500, 6: 6500},
    "DE": {1: 2000, 2: 3200, 3: 3900, 4: 4400, 5: 5400, 6: 6300},
    "CH": {1: 2500, 2: 3800, 3: 4400, 4: 5000, 5: 6000, 6: 7000},
}

# Durchschnittlicher WP-Stromverbrauch (kWh/Jahr) — Einfamilienhaus
# Quellen: Austrian Energy Agency, BDEW Wärmepumpen-Studie 2023
BENCHMARK_HEATPUMP_CONSUMPTION: Final[dict[str, int]] = {
    "AT": 4000,  # ~160m² EFH, SCOP ~3.5
    "DE": 4500,  # kälteres Klima im Schnitt
    "CH": 3500,  # gut gedämmte Häuser
}

# CO2-Faktor Strommix (kg CO2/kWh) — Umweltbundesamt AT/DE, BFE CH
BENCHMARK_CO2_FACTORS: Final[dict[str, float]] = {
    "AT": 0.150,  # viel Wasserkraft
    "DE": 0.380,  # noch Kohle/Gas
    "CH": 0.030,  # Nuklear + Wasserkraft
}

RANGE_HOUSEHOLD_SIZE: Final[dict] = {"min": 1, "max": 6, "step": 1}

# --- PV-Strings (Vergleich mehrerer Strings) --------------------------------
CONF_PV_STRING_1_NAME: Final[str] = "pv_string_1_name"
CONF_PV_STRING_1_ENTITY: Final[str] = "pv_string_1_entity"
CONF_PV_STRING_2_NAME: Final[str] = "pv_string_2_name"
CONF_PV_STRING_2_ENTITY: Final[str] = "pv_string_2_entity"
CONF_PV_STRING_3_NAME: Final[str] = "pv_string_3_name"
CONF_PV_STRING_3_ENTITY: Final[str] = "pv_string_3_entity"
CONF_PV_STRING_4_NAME: Final[str] = "pv_string_4_name"
CONF_PV_STRING_4_ENTITY: Final[str] = "pv_string_4_entity"
CONF_PV_STRING_1_POWER: Final[str] = "pv_string_1_power"
CONF_PV_STRING_2_POWER: Final[str] = "pv_string_2_power"
CONF_PV_STRING_3_POWER: Final[str] = "pv_string_3_power"
CONF_PV_STRING_4_POWER: Final[str] = "pv_string_4_power"

PV_STRING_CONFIGS = [
    (CONF_PV_STRING_1_NAME, CONF_PV_STRING_1_ENTITY, CONF_PV_STRING_1_POWER),
    (CONF_PV_STRING_2_NAME, CONF_PV_STRING_2_ENTITY, CONF_PV_STRING_2_POWER),
    (CONF_PV_STRING_3_NAME, CONF_PV_STRING_3_ENTITY, CONF_PV_STRING_3_POWER),
    (CONF_PV_STRING_4_NAME, CONF_PV_STRING_4_ENTITY, CONF_PV_STRING_4_POWER),
]
