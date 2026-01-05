# PV Amortisation

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/release/hoizi89/pv_amortisation.svg)](https://github.com/hoizi89/pv_amortisation/releases)

Eine Home Assistant Integration zur Berechnung der PV-Anlagen Amortisation.

## Features

- **Amortisationsberechnung** - Berechnet wie viel % der Anlage bereits abbezahlt ist
- **Eigenverbrauch & Einspeisung** - Automatische Berechnung basierend auf deinen Sensoren
- **Dynamische Preise** - Unterstützt feste Preise oder dynamische Strompreis-Sensoren
- **Euro oder Cent** - Preise können in €/kWh oder ct/kWh angegeben werden
- **Statistiken** - Ersparnis pro Tag/Monat/Jahr, Restlaufzeit, Prognose
- **Offset-Unterstützung** - Für Anlagen die schon vor dem Tracking liefen
- **CO2-Ersparnis** - Zeigt eingesparte CO2-Emissionen

## Sensoren

| Sensor | Beschreibung |
|--------|--------------|
| **Amortisation** | Amortisation in % |
| **Gesamtersparnis** | Gesamte Ersparnis in € |
| **Restbetrag** | Verbleibender Betrag bis Amortisation |
| **Status** | Text-Status (z.B. "45.2% amortisiert") |
| **Eigenverbrauch** | Selbst verbrauchter PV-Strom in kWh |
| **Einspeisung** | Ins Netz eingespeister Strom in kWh |
| **Ersparnis Eigenverbrauch** | Ersparnis durch Eigenverbrauch in € |
| **Einnahmen Einspeisung** | Einnahmen durch Einspeisung in € |
| **Eigenverbrauchsquote** | Anteil der PV-Produktion der selbst verbraucht wird |
| **Autarkiegrad** | Anteil des Verbrauchs der durch PV gedeckt wird |
| **Ersparnis pro Tag/Monat/Jahr** | Durchschnittliche Ersparnis |
| **Restlaufzeit** | Geschätzte Tage bis Amortisation |
| **Amortisationsdatum** | Geschätztes Datum der vollständigen Amortisation |
| **CO2 Ersparnis** | Eingesparte CO2-Emissionen in kg |

## Installation

### HACS (empfohlen)

1. Öffne HACS in Home Assistant
2. Klicke auf "Integrationen"
3. Klicke auf die drei Punkte oben rechts → "Benutzerdefinierte Repositories"
4. Füge `https://github.com/hoizi89/pv_amortisation` als Repository hinzu (Kategorie: Integration)
5. Suche nach "PV Amortisation" und installiere es
6. Starte Home Assistant neu

### Manuell

1. Kopiere den `custom_components/pv_amortisation` Ordner in dein `config/custom_components/` Verzeichnis
2. Starte Home Assistant neu

## Konfiguration

1. Gehe zu Einstellungen → Geräte & Dienste
2. Klicke auf "Integration hinzufügen"
3. Suche nach "PV Amortisation"
4. Folge dem Setup-Assistenten

### Erforderliche Sensoren

- **PV Produktion** - Ein Sensor der die gesamte PV-Produktion in kWh misst (total_increasing)

### Optionale Sensoren (für genauere Berechnung)

- **Netzeinspeisung** - Sensor für Grid-Export in kWh
- **Netzbezug** - Sensor für Grid-Import in kWh
- **Hausverbrauch** - Sensor für Gesamtverbrauch in kWh

### Einstellungen

| Einstellung | Beschreibung |
|-------------|--------------|
| **Strompreis-Einheit** | Euro oder Cent pro kWh |
| **Strompreis** | Aktueller Strompreis |
| **Dynamischer Strompreis** | Optional: Sensor für dynamischen Preis |
| **Einspeisevergütung-Einheit** | Euro oder Cent pro kWh |
| **Einspeisevergütung** | Vergütung für eingespeisten Strom |
| **Anschaffungskosten** | Gesamtkosten der PV-Anlage |
| **Installationsdatum** | Datum der Installation |
| **Ersparnis-Offset** | Bereits amortisierter Betrag (vor Tracking) |
| **Energie-Offset** | Eigenverbrauch/Einspeisung vor Tracking |

## Beispiel Dashboard

```yaml
type: entities
title: PV Amortisation
entities:
  - entity: sensor.pv_amortisation_status
  - entity: sensor.pv_amortisation_amortisation
  - entity: sensor.pv_amortisation_gesamtersparnis
  - entity: sensor.pv_amortisation_restbetrag
  - entity: sensor.pv_amortisation_restlaufzeit
  - entity: sensor.pv_amortisation_amortisationsdatum
  - type: divider
  - entity: sensor.pv_amortisation_eigenverbrauch
  - entity: sensor.pv_amortisation_einspeisung
  - entity: sensor.pv_amortisation_eigenverbrauchsquote
  - entity: sensor.pv_amortisation_autarkiegrad
  - type: divider
  - entity: sensor.pv_amortisation_ersparnis_pro_tag
  - entity: sensor.pv_amortisation_ersparnis_pro_monat
  - entity: sensor.pv_amortisation_co2_ersparnis
```

## Changelog

### v1.0.0
- Initiales Release
- Amortisationsberechnung
- Euro/Cent Unterstützung
- Dynamische Strompreise
- Offset für bestehende Anlagen
- 21 verschiedene Sensoren

## Lizenz

MIT License - siehe [LICENSE](LICENSE)
