# PV Management Fixpreis

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/v/release/hoizi89/pv_management_fix)](https://github.com/hoizi89/pv_management_fix/releases)

Home Assistant Integration für **Fixpreis-Stromtarife** (z.B. Grünwelt classic, Energie AG).

Berechnet die Amortisation deiner PV-Anlage, trackt Batterie-Effizienz und überwacht dein Stromkontingent.

## Features

- **Amortisationsberechnung** — Wie viel deiner PV-Anlage ist abbezahlt?
- **Energie-Tracking** — Eigenverbrauch und Einspeisung (inkrementell, persistent)
- **Batterie-Tracking** — Ladestand, Effizienz, Zyklen, Ladung/Entladung
- **ROI-Berechnung** — Return on Investment nach Amortisation
- **Stromkontingent** — Jahres-kWh-Budget mit saisonaler Gewichtung
- **Tägliche Stromkosten** — Netzbezug, Einspeisung, Netto-Kosten pro Tag
- **Helper-Sync** — Speichert Werte in input_number für maximale Persistenz
- **Event-Benachrichtigungen** — Meilensteine, Kontingent-Warnungen, Monatszusammenfassungen

## Installation

### HACS (empfohlen)

1. HACS öffnen > Integrationen > 3-Punkt-Menü > **Benutzerdefinierte Repositories**
2. URL eingeben: `https://github.com/hoizi89/pv_management_fix`
3. Kategorie: **Integration**
4. Integration suchen und installieren
5. Home Assistant **neustarten**

### Manuell

1. `custom_components/pv_management_fix` Ordner nach `config/custom_components/` kopieren
2. Home Assistant neustarten

## Konfiguration

1. Einstellungen > Geräte & Dienste > **Integration hinzufügen**
2. "PV Management Fixpreis" suchen
3. Sensoren auswählen:
   - **PV Produktion** (Pflicht) — kWh-Zähler
   - **Netzeinspeisung** (optional) — für Einnahmenberechnung
   - **Netzbezug** (optional) — für Stromkontingent & Kostentracking
   - **Hausverbrauch** (optional) — für Autarkiegrad
4. **Fixpreis** eingeben (Standard: 10.92 ct/kWh netto)
5. **Aufschlagfaktor** (Standard: 2.0 → 10ct netto wird 20ct brutto)
6. **Anschaffungskosten** eingeben
7. **Amortisation Helper** auswählen (input_number Entity)

## Sensoren

### Haupt-Device: PV Fixpreis

| Sensor | Beschreibung | Einheit |
|--------|-------------|---------|
| Amortisation | Prozent der Anlage abbezahlt | % |
| Gesamtersparnis | Gesamte Ersparnis | € |
| Restbetrag | Verbleibend bis Amortisation | € |
| Status | Text-Zusammenfassung | — |
| Restlaufzeit | Geschätzte Tage bis Amortisation | Tage |
| Amortisationsdatum | Geschätztes Datum | Datum |
| Eigenverbrauch | Selbst verbrauchte kWh | kWh |
| Einspeisung | Ins Netz eingespeiste kWh | kWh |
| Eigenverbrauchsquote | Anteil PV der selbst verbraucht wird | % |
| Autarkiegrad | Anteil Verbrauch durch PV gedeckt | % |
| Ersparnis pro Tag/Monat/Jahr | Durchschnittliche Ersparnis | €/Zeitraum |
| CO2 Ersparnis | Eingesparte Emissionen | kg |
| **ROI** | Return on Investment (nach Amortisation) | % |
| **ROI pro Jahr** | Jährlicher ROI | %/Jahr |
| Strompreis Brutto | Für Energy Dashboard | EUR/kWh |

### Device: Strompreise

| Sensor | Beschreibung | Einheit |
|--------|-------------|---------|
| Einspeisung Heute | Tägliche Einspeisevergütung | € |
| Netzbezug Heute | Tägliche Netzbezugskosten | € |
| Stromkosten Netto Heute | Netzbezug minus Einspeisung | € |

### Device: Batterie (optional)

Erscheint nur wenn mindestens ein Batterie-Sensor konfiguriert ist.

| Sensor | Beschreibung | Einheit |
|--------|-------------|---------|
| Batterie Ladestand | SOC mit dynamischem Icon | % |
| Batterie Ladung Gesamt | Gesamt ins Batterie geladen | kWh |
| Batterie Entladung Gesamt | Gesamt aus Batterie entladen | kWh |
| Batterie Effizienz | Entladung / Ladung × 100 | % |
| Batterie Zyklen | Geschätzt: Ladung / Kapazität | Zyklen |

> **Beispiel:** 4868 kWh geladen, 3820 kWh entladen → **78.5% Effizienz**, **371 Zyklen** (bei 13.1 kWh Kapazität)

### Device: Stromkontingent (optional)

Erscheint nur wenn das Kontingent aktiviert ist.

| Sensor | Beschreibung | Einheit |
|--------|-------------|---------|
| Kontingent Verbleibend | Verbleibende kWh im Jahresbudget | kWh |
| Kontingent Verbrauch | Prozent des Kontingents verbraucht | % |
| Kontingent Reserve | Über/unter Budget (positiv = gut) | kWh |
| Kontingent Tagesbudget | Erlaubter Tagesverbrauch für Restperiode | kWh/Tag |
| Kontingent Prognose | Hochrechnung Jahresverbrauch | kWh |
| Kontingent Restlaufzeit | Verbleibende Tage in der Periode | Tage |
| Kontingent Status | Text-Zusammenfassung | — |

## Options (nach Setup änderbar)

### Sensoren
- PV Produktion, Netzeinspeisung, Netzbezug, Hausverbrauch

### Strompreise & Amortisation
- **Fixpreis netto** (ct/kWh) — Arbeitspreis vom Anbieter
- **Aufschlagfaktor** (Standard: 2.0) — Netto × Faktor = Brutto
- **Strompreis per Sensor** (optional) — überschreibt den statischen Fixpreis
- **Einspeisevergütung** (€/kWh oder ct/kWh, statisch oder per Sensor)
- **Anschaffungskosten** und **Installationsdatum**

> **Beispiel:** Netto 10.92 ct × Faktor 2.0 = **21.84 ct brutto** (wird für Ersparnisberechnung verwendet)

### Batterie
- **Ladestand Sensor** (SOC) — z.B. `sensor.battery_state_of_charge`
- **Ladung Gesamt Sensor** — z.B. `sensor.total_battery_charge`
- **Entladung Gesamt Sensor** — z.B. `sensor.total_battery_discharge`
- **Kapazität** in kWh (z.B. 13.1)

### Amortisation Helper
- **input_number Entity** — Speichert die Gesamtersparnis persistent
- **Von Helper wiederherstellen** — Startwert beim nächsten Start laden

### Historische Daten
- Bereits amortisierter Betrag (€)
- Eigenverbrauch / Einspeisung vor Tracking (kWh)

### Stromkontingent
- **Aktivieren/Deaktivieren** — Sensoren erscheinen automatisch (kein Neustart nötig)
- **Jahres-Kontingent** in kWh (z.B. 4000)
- **Startdatum** der Tarifperiode
- **Zählerstand** am Startdatum (Netzbezug)
- **Monatlicher Abschlag** (optional, nur Anzeige)
- **Saisonale Berechnung** — Berücksichtigt Winter-/Sommer-Verbrauchsmuster

## Energy Dashboard

Verwende `sensor.pv_fixpreis_strompreis_brutto` als Strompreis-Entity im Home Assistant Energy Dashboard. Der Sensor gibt den Brutto-Preis in `EUR/kWh` aus.

## Dashboard Beispiel

```yaml
type: entities
title: PV Fixpreis
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

### Batterie Dashboard

```yaml
type: entities
title: Batterie
entities:
  - entity: sensor.pv_fixpreis_batterie_ladestand
  - entity: sensor.pv_fixpreis_batterie_effizienz
  - entity: sensor.pv_fixpreis_batterie_zyklen
  - entity: sensor.pv_fixpreis_batterie_ladung_gesamt
  - entity: sensor.pv_fixpreis_batterie_entladung_gesamt
```

### Stromkontingent Dashboard

```yaml
type: entities
title: Stromkontingent
entities:
  - entity: sensor.pv_fixpreis_kontingent_status
  - entity: sensor.pv_fixpreis_kontingent_verbleibend
  - entity: sensor.pv_fixpreis_kontingent_verbrauch
  - entity: sensor.pv_fixpreis_kontingent_reserve
  - entity: sensor.pv_fixpreis_kontingent_tagesbudget
  - entity: sensor.pv_fixpreis_kontingent_prognose
  - entity: sensor.pv_fixpreis_kontingent_restlaufzeit
```

### Tägliche Stromkosten

```yaml
type: entities
title: Stromkosten Heute
entities:
  - entity: sensor.pv_fixpreis_netzbezug_heute
  - entity: sensor.pv_fixpreis_einspeisung_heute
  - entity: sensor.pv_fixpreis_stromkosten_netto_heute
```

## Events (Benachrichtigungen)

Die Integration feuert `pv_management_event` Events für eigene Automationen:

### Meilenstein-Events (25%, 50%, 75%, 100%)
```yaml
event_type: pv_management_event
event_data:
  type: "amortisation_milestone"
  milestone: 50
  total_savings: 3500.00
  remaining: 3500.00
  message: "50% der PV-Anlage amortisiert!"
```

### Kontingent-Warnungen (80%, 100%, über Budget)
```yaml
event_type: pv_management_event
event_data:
  type: "quota_warning_80"
  consumed_percent: 80.5
  remaining_kwh: 780
  message: "80% des Stromkontingents verbraucht!"
```

### Monatliche Zusammenfassung
```yaml
event_type: pv_management_event
event_data:
  type: "monthly_summary"
  month: "Januar 2025"
  grid_import_kwh: 180.5
  grid_import_cost: 32.50
  amortisation_percent: 52.3
  message: "PV-Bericht Januar 2025: 180 kWh Netzbezug, 52.3% amortisiert"
```

### Beispiel-Automation

```yaml
alias: "PV Meilenstein Benachrichtigung"
trigger:
  - platform: event
    event_type: pv_management_event
    event_data:
      type: amortisation_milestone
action:
  - service: notify.mobile_app
    data:
      title: "PV Meilenstein erreicht!"
      message: "{{ trigger.event.data.message }}"
```

## Unterschied zu pv_management

Diese Integration ist optimiert für **Fixpreis-Tarife**.

Für **Spot-Tarife** (aWATTar, smartENERGY) mit Batterie-Management:
[pv_management](https://github.com/hoizi89/pv_management)

| Feature | pv_management | pv_management_fix |
|---------|--------------|-------------------|
| Amortisation | Ja | Ja |
| Energie-Tracking | Ja | Ja |
| Batterie-Tracking | Nein | Ja |
| ROI-Berechnung | Nein | Ja |
| Stromkontingent | Nein | Ja |
| Tägliche Stromkosten | Nein | Ja |
| Empfehlungssignal | Ja | Nein |
| Auto-Charge | Ja | Nein |
| Entlade-Steuerung | Ja | Nein |
| EPEX Quantil | Ja | Nein |
| Solcast | Ja | Nein |

## Changelog

### v1.8.1
- **Fix:** `remaining_amount` → `remaining_cost` (Crash bei Meilensteinen)
- **Fix:** Fehlende "Helper" Menu-Translation

### v1.8.0
- **NEU: Batterie-Tracking** — Eigenes Device mit 5 Sensoren (SOC, Ladung, Entladung, Effizienz, Zyklen)
- **NEU: ROI-Sensoren** — Return on Investment und jährlicher ROI
- **Fix: Quota-Sensoren** erscheinen ohne HA-Neustart wenn nachträglich aktiviert
- Options-Menü: neuer "Batterie" Bereich

### v1.7.1
- Batterie-kompatible Eigenverbrauch- und Autarkiegrad-Berechnung
- Verbesserte Preis-Config Labels

### v1.5.0
- **NEU: Aufschlagfaktor** — Netto-Preis + Faktor für automatische Brutto-Berechnung
- **NEU: Energy Dashboard Sensor** — `EUR/kWh` Sensor für HA Energy Dashboard

### v1.4.0
- **NEU: Helper-Sync** — input_number für persistente Ersparnisspeicherung
- **NEU: Meilenstein-Events** — Automatische Events bei 25%, 50%, 75%, 100%
- **NEU: Kontingent-Warnungen** — Events bei 80%, 100% und über Budget
- **NEU: Monatliche Zusammenfassung**

### v1.1.0
- **NEU: Stromkontingent** — Jahres-kWh-Budget Tracking
- 7 neue Sensoren für Kontingent-Überwachung

### v1.0.0
- Erstveröffentlichung
- Amortisationsberechnung mit Fixpreis
- Energie-Tracking (Eigenverbrauch, Einspeisung)
- Ersparnisstatistiken (Tag/Monat/Jahr)

## Support

[Fehler melden](https://github.com/hoizi89/pv_management_fix/issues)

## Lizenz

MIT License — siehe [LICENSE](LICENSE)
