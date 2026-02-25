# PV Energy Management+

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/v/release/hoizi89/pv_management_fix)](https://github.com/hoizi89/pv_management_fix/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> The all-in-one Home Assistant integration for your PV system with **fixed-price tariffs**.

> **For spot/variable tariffs** (aWATTar, smartENERGY, Tibber) with battery management:
> [pv_management](https://github.com/hoizi89/pv_management)

---

## What Can This Integration Do?

| Feature | Description |
|---------|-------------|
| **Amortization** | See in real-time how much of your PV system is paid off |
| **Energy Benchmark** | Compare your consumption with AT/DE/CH averages |
| **Battery Tracking** | SOC, efficiency, cycles — all at a glance |
| **Electricity Quota** | Yearly kWh budget with seasonal weighting |
| **ROI Calculation** | Return on Investment — before and after amortization |
| **Daily Costs** | Grid import, feed-in, and net electricity cost per day |
| **Notifications** | Milestones, quota warnings, monthly reports |

---

## New in v1.9.0: Energy Benchmark

Compare your electricity consumption with the average for your country — **completely offline**, no cloud needed.

- **Countries:** Austria, Germany, Switzerland
- **Household size:** 1-6 persons
- **6 sensors:** Average, own consumption, comparison (%), CO2 avoided, efficiency score (0-100), rating
- **Heat pump optional:** HP consumption is benchmarked separately for fair comparison

| Sensor | What it shows | Example |
|--------|--------------|---------|
| Benchmark Average | Reference consumption for your country/household | 4000 kWh/year |
| Benchmark Own Consumption | Your consumption extrapolated to 1 year | 3200 kWh/year |
| Benchmark Comparison | Deviation from average | -20% |
| Benchmark CO2 Avoided | CO2 savings from PV per year | 180 kg/year |
| Benchmark Efficiency Score | Overall rating 0-100 | 72 points |
| Benchmark Rating | Text classification | "Sehr gut" |

---

## Installation

### HACS (recommended)

1. Open HACS > Integrations > 3-dot menu > **Custom repositories**
2. URL: `https://github.com/hoizi89/pv_management_fix`
3. Category: **Integration**
4. Install and **restart** Home Assistant

### Manual

Copy `custom_components/pv_management_fix` to `config/custom_components/`, then restart.

---

## Quick Start

1. **Settings** > Devices & Services > **Add Integration**
2. Search for "PV Energy Management+"
3. Select your sensors:
   - **PV Production** (required) — kWh counter
   - **Grid Export** (optional) — for earnings calculation
   - **Grid Import** (optional) — for quota & cost tracking
   - **Consumption** (optional) — for autarky rate
4. Enter **fixed price** (e.g. 10.92 ct/kWh net)
5. Set **markup factor** (default: 2.0 — turns 10ct net into 20ct gross)
6. Configure **installation cost** and **Amortization Helper** (input_number)

> All settings can be changed later under **Options**.

---

## Sensors Overview

### Main Device: PV Fixpreis

| Sensor | Unit | Description |
|--------|------|-------------|
| Amortization | % | How much of the system is paid off |
| Total Savings | EUR | Savings from self-consumption + feed-in |
| Remaining Cost | EUR | Remaining until amortization |
| Status | — | e.g. "45.2% amortized" or "Amortized! +500 EUR profit" |
| Remaining Days | Days | Estimated days until amortization |
| Amortization Date | Date | When the system will be paid off |
| Self Consumption | kWh | PV electricity consumed directly |
| Feed-in | kWh | PV electricity exported to grid |
| Self Consumption Ratio | % | Share of PV production used directly |
| Autarky Rate | % | Share of consumption covered by PV |
| Savings per Day/Month/Year | EUR | Average savings |
| CO2 Savings | kg | Avoided CO2 emissions |
| ROI | % | Return on Investment |
| ROI per Year | %/year | Annual ROI |
| Electricity Price Gross | EUR/kWh | For Energy Dashboard |

### Device: Electricity Prices

| Sensor | Unit | Description |
|--------|------|-------------|
| Feed-in Today | EUR | Today's feed-in earnings |
| Grid Import Today | EUR | Today's grid import cost |
| Net Electricity Cost Today | EUR | Grid import minus feed-in |

### Device: Energy Benchmark (optional)

Appears when enabled under Options > Energy Benchmark.

| Sensor | Unit | Description |
|--------|------|-------------|
| Benchmark Average | kWh/year | Reference consumption (E-Control/BDEW/BFE) |
| Benchmark Own Consumption | kWh/year | Your household consumption extrapolated |
| Benchmark Comparison | % | Deviation (negative = better than average) |
| Benchmark CO2 Avoided | kg/year | CO2 savings from PV |
| Benchmark Efficiency Score | Points | 0-100 (consumption + autarky + self-consumption) |
| Benchmark Rating | — | Hervorragend / Sehr gut / Gut / Durchschnittlich |
| Benchmark HP Average | kWh/year | Reference HP consumption (only with HP) |
| Benchmark HP Consumption | kWh/year | Your HP consumption (only with HP) |

### Device: Battery (optional)

Appears when at least one battery sensor is configured.

| Sensor | Unit | Description |
|--------|------|-------------|
| Battery SOC | % | State of charge with dynamic icon |
| Battery Charge Total | kWh | Total energy charged into battery |
| Battery Discharge Total | kWh | Total energy discharged from battery |
| Battery Efficiency | % | Discharge / Charge x 100 |
| Battery Cycles | Cycles | Estimated: Charge / Capacity |

### Device: Electricity Quota (optional)

Appears when the quota is enabled.

| Sensor | Unit | Description |
|--------|------|-------------|
| Quota Remaining | kWh | Remaining kWh in yearly budget |
| Quota Usage | % | Percent of quota used |
| Quota Reserve | kWh | Over/under budget (positive = good) |
| Quota Daily Budget | kWh/day | Allowed daily consumption |
| Quota Today Remaining | kWh | Daily budget minus today's consumption |
| Quota Forecast | kWh | Yearly consumption projection |
| Quota Remaining Days | Days | Remaining days in period |
| Quota Status | — | Text summary |

---

## Options (configurable after setup)

Under **Settings > Devices & Services > PV Energy Management+ > Configure**:

| Category | What you can configure |
|----------|----------------------|
| **Sensors** | PV Production, Grid Export, Grid Import, Consumption |
| **Electricity Prices** | Fixed price, markup factor, dynamic sensor, feed-in tariff |
| **Amortization Helper** | input_number for persistent storage |
| **Historical Data** | Already amortized amount, energy offsets |
| **Electricity Quota** | Yearly kWh, start date, meter reading, seasonal calculation |
| **Battery** | SOC, charge/discharge sensors, capacity |
| **Energy Benchmark** | Country, household size, heat pump |

---

## Energy Dashboard

Use `sensor.pv_fixpreis_strompreis_brutto` as the electricity price entity in the Home Assistant Energy Dashboard. The sensor outputs the gross price in `EUR/kWh`.

---

## Dashboard Examples

### Amortization

```yaml
type: entities
title: PV Amortization
entities:
  - entity: sensor.pv_fixpreis_status
  - entity: sensor.pv_fixpreis_amortisation
  - entity: sensor.pv_fixpreis_gesamtersparnis
  - entity: sensor.pv_fixpreis_restbetrag
  - entity: sensor.pv_fixpreis_restlaufzeit
  - entity: sensor.pv_fixpreis_roi
  - type: divider
  - entity: sensor.pv_fixpreis_eigenverbrauch
  - entity: sensor.pv_fixpreis_einspeisung
  - entity: sensor.pv_fixpreis_eigenverbrauchsquote
  - type: divider
  - entity: sensor.pv_fixpreis_ersparnis_pro_monat
  - entity: sensor.pv_fixpreis_co2_ersparnis
```

### Energy Benchmark

```yaml
type: entities
title: Energy Benchmark
entities:
  - entity: sensor.pv_fixpreis_benchmark_effizienz_score
  - entity: sensor.pv_fixpreis_benchmark_bewertung
  - type: divider
  - entity: sensor.pv_fixpreis_benchmark_eigener_verbrauch
  - entity: sensor.pv_fixpreis_benchmark_durchschnitt
  - entity: sensor.pv_fixpreis_benchmark_vergleich
  - type: divider
  - entity: sensor.pv_fixpreis_benchmark_co2_vermieden
```

### Battery

```yaml
type: entities
title: Battery
entities:
  - entity: sensor.pv_fixpreis_batterie_ladestand
  - entity: sensor.pv_fixpreis_batterie_effizienz
  - entity: sensor.pv_fixpreis_batterie_zyklen
  - entity: sensor.pv_fixpreis_batterie_ladung_gesamt
  - entity: sensor.pv_fixpreis_batterie_entladung_gesamt
```

### Electricity Quota

```yaml
type: entities
title: Electricity Quota
entities:
  - entity: sensor.pv_fixpreis_kontingent_status
  - entity: sensor.pv_fixpreis_kontingent_verbleibend
  - entity: sensor.pv_fixpreis_kontingent_verbrauch
  - entity: sensor.pv_fixpreis_kontingent_reserve
  - entity: sensor.pv_fixpreis_kontingent_tagesbudget
  - entity: sensor.pv_fixpreis_kontingent_heute_verbleibend
  - entity: sensor.pv_fixpreis_kontingent_prognose
```

### Daily Costs

```yaml
type: entities
title: Electricity Costs Today
entities:
  - entity: sensor.pv_fixpreis_netzbezug_heute
  - entity: sensor.pv_fixpreis_einspeisung_heute
  - entity: sensor.pv_fixpreis_stromkosten_netto_heute
```

---

## Events (Notifications)

The integration fires `pv_management_event` events for custom automations:

### Milestone Events (25%, 50%, 75%, 100%)

```yaml
trigger:
  - platform: event
    event_type: pv_management_event
    event_data:
      type: amortisation_milestone
action:
  - service: notify.mobile_app
    data:
      title: "PV Milestone!"
      message: "{{ trigger.event.data.message }}"
```

### Quota Warnings

```yaml
trigger:
  - platform: event
    event_type: pv_management_event
    event_data:
      type: quota_warning_80
action:
  - service: notify.mobile_app
    data:
      title: "Electricity Quota"
      message: "{{ trigger.event.data.message }}"
```

---

## Comparison: pv_management vs pv_management_fix

| Feature | pv_management (Spot) | pv_management_fix (Fixed) |
|---------|:--------------------:|:-------------------------:|
| Amortization | Yes | Yes |
| Energy Tracking | Yes | Yes |
| **Energy Benchmark** | **Yes** | **Yes** |
| Battery Tracking | No | **Yes** |
| ROI Calculation | No | **Yes** |
| Electricity Quota | No | **Yes** |
| Daily Costs | Yes | **Yes** |
| Recommendation Signal | **Yes** | No |
| Auto-Charge | **Yes** | No |
| Discharge Control | **Yes** | No |
| EPEX Quantile | **Yes** | No |
| Solcast | **Yes** | No |

For **spot tariffs** (aWATTar, smartENERGY) with battery management:
[pv_management](https://github.com/hoizi89/pv_management)

---

## Changelog

### v1.9.0
- **NEW: Energy Benchmark** — Compare with DACH averages (AT/DE/CH), CO2 savings, efficiency score 0-100
- **NEW: Heat Pump** — Optional HP sensor for fair benchmark comparison
- **Rename:** "PV Management Fixpreis" -> "PV Energy Management+"
- Domain and entity IDs remain unchanged (no breaking change)

### v1.8.1
- Fix: `remaining_amount` -> `remaining_cost` (crash on milestones)
- Fix: Missing "Helper" menu translation

### v1.8.0
- NEW: Battery tracking (SOC, charge, discharge, efficiency, cycles)
- NEW: ROI sensors (Return on Investment + annual ROI)
- Fix: Quota sensors appear without HA restart

### v1.7.1
- Battery-compatible self-consumption and autarky rate calculation

### v1.5.0
- NEW: Markup factor for automatic gross price calculation
- NEW: Energy Dashboard sensor (EUR/kWh)

### v1.4.0
- NEW: Helper sync, milestone events, quota warnings, monthly summary

### v1.1.0
- NEW: Electricity quota (yearly kWh budget)

### v1.0.0
- Initial release

---

## Support

[Report issues](https://github.com/hoizi89/pv_management_fix/issues) | [Discussions](https://github.com/hoizi89/pv_management_fix/discussions)

## License

MIT License — see [LICENSE](LICENSE)
