# PV Energy Management+

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/v/release/hoizi89/pv_management_fix)](https://github.com/hoizi89/pv_management_fix/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Die All-in-One Home Assistant Integration fuer deine PV-Anlage mit Fixpreis-Tarif.

---

## Was kann diese Integration?

| Feature | Beschreibung |
|---------|-------------|
| **Amortisation** | Sieh in Echtzeit, wie viel deiner PV-Anlage schon abbezahlt ist |
| **Energie-Benchmark** | Vergleiche deinen Verbrauch mit dem DACH-Durchschnitt (AT/DE/CH) |
| **Batterie-Tracking** | Ladestand, Effizienz, Zyklen — alles auf einen Blick |
| **Stromkontingent** | Jahres-kWh-Budget mit saisonaler Gewichtung |
| **ROI-Berechnung** | Return on Investment — vor und nach Amortisation |
| **Tageskosten** | Netzbezug, Einspeisung und Netto-Stromkosten pro Tag |
| **Benachrichtigungen** | Meilensteine, Kontingent-Warnungen, Monatsberichte |

---

## Neu in v1.9.0: Energie-Benchmark

Vergleiche deinen Stromverbrauch mit dem Durchschnitt deines Landes — **komplett offline**, keine Cloud noetig.

- **Laender:** Oesterreich, Deutschland, Schweiz
- **Haushaltsgroesse:** 1-6 Personen
- **6 Sensoren:** Durchschnitt, eigener Verbrauch, Vergleich (%), CO2-Einsparung, Effizienz-Score (0-100), Bewertung
- **Waermepumpe optional:** WP-Verbrauch wird separat benchmarkt fuer fairen Vergleich

| Sensor | Was er zeigt | Beispiel |
|--------|-------------|---------|
| Benchmark Durchschnitt | Referenzverbrauch fuer dein Land/Haushaltsgroesse | 4000 kWh/Jahr |
| Benchmark Eigener Verbrauch | Dein Verbrauch hochgerechnet auf 1 Jahr | 3200 kWh/Jahr |
| Benchmark Vergleich | Abweichung vom Durchschnitt | -20% |
| Benchmark CO2 Vermieden | CO2-Einsparung durch PV pro Jahr | 180 kg/Jahr |
| Benchmark Effizienz Score | Gesamtbewertung 0-100 | 72 Punkte |
| Benchmark Bewertung | Textuelle Einstufung | "Sehr gut" |

---

## Installation

### HACS (empfohlen)

1. HACS oeffnen > Integrationen > 3-Punkt-Menue > **Benutzerdefinierte Repositories**
2. URL: `https://github.com/hoizi89/pv_management_fix`
3. Kategorie: **Integration**
4. Installieren und Home Assistant **neustarten**

### Manuell

`custom_components/pv_management_fix` nach `config/custom_components/` kopieren, dann neustarten.

---

## Schnellstart

1. **Einstellungen** > Geraete & Dienste > **Integration hinzufuegen**
2. "PV Energy Management+" suchen
3. Sensoren auswaehlen:
   - **PV Produktion** (Pflicht) — kWh-Zaehler
   - **Netzeinspeisung** (optional) — fuer Einnahmenberechnung
   - **Netzbezug** (optional) — fuer Kontingent & Kostentracking
   - **Hausverbrauch** (optional) — fuer Autarkiegrad
4. **Fixpreis** eingeben (z.B. 10.92 ct/kWh netto)
5. **Aufschlagfaktor** setzen (Standard: 2.0 — macht 10ct zu 20ct brutto)
6. **Anschaffungskosten** und **Amortisation Helper** (input_number) konfigurieren

> Alle Einstellungen koennen nachtraeglich unter **Optionen** geaendert werden.

---

## Sensoren-Uebersicht

### Haupt-Device: PV Fixpreis

| Sensor | Einheit | Beschreibung |
|--------|---------|-------------|
| Amortisation | % | Wie viel der Anlage ist abbezahlt |
| Gesamtersparnis | EUR | Ersparnis durch Eigenverbrauch + Einspeisung |
| Restbetrag | EUR | Noch offen bis zur Amortisation |
| Status | — | z.B. "45.2% amortisiert" oder "Amortisiert! +500EUR Gewinn" |
| Restlaufzeit | Tage | Geschaetzte Tage bis Amortisation |
| Amortisationsdatum | Datum | Wann ist die Anlage voraussichtlich abbezahlt |
| Eigenverbrauch | kWh | PV-Strom der selbst verbraucht wurde |
| Einspeisung | kWh | PV-Strom der ins Netz ging |
| Eigenverbrauchsquote | % | Anteil der PV-Produktion die selbst genutzt wird |
| Autarkiegrad | % | Anteil des Verbrauchs der durch PV gedeckt wird |
| Ersparnis pro Tag/Monat/Jahr | EUR | Durchschnittliche Ersparnis |
| CO2 Ersparnis | kg | Eingesparte CO2-Emissionen |
| ROI | % | Return on Investment |
| ROI pro Jahr | %/Jahr | Jaehrlicher ROI |
| Strompreis Brutto | EUR/kWh | Fuer Energy Dashboard |

### Device: Strompreise

| Sensor | Einheit | Beschreibung |
|--------|---------|-------------|
| Einspeisung Heute | EUR | Heutige Einspeiseverguetung |
| Netzbezug Heute | EUR | Heutige Netzbezugskosten |
| Stromkosten Netto Heute | EUR | Netzbezug minus Einspeisung |

### Device: Energie-Benchmark (optional)

Erscheint wenn unter Optionen > Energie-Benchmark aktiviert.

| Sensor | Einheit | Beschreibung |
|--------|---------|-------------|
| Benchmark Durchschnitt | kWh/Jahr | Referenzverbrauch (E-Control/BDEW/BFE) |
| Benchmark Eigener Verbrauch | kWh/Jahr | Dein Haushaltsstrom hochgerechnet |
| Benchmark Vergleich | % | Abweichung (negativ = besser als Durchschnitt) |
| Benchmark CO2 Vermieden | kg/Jahr | CO2-Einsparung durch PV |
| Benchmark Effizienz Score | Punkte | 0-100 (Verbrauch + Autarkie + Eigenverbrauch) |
| Benchmark Bewertung | — | Hervorragend / Sehr gut / Gut / Durchschnittlich |
| Benchmark WP Durchschnitt | kWh/Jahr | Referenz WP-Verbrauch (nur mit WP) |
| Benchmark WP Verbrauch | kWh/Jahr | Eigener WP-Verbrauch (nur mit WP) |

### Device: Batterie (optional)

Erscheint wenn mindestens ein Batterie-Sensor konfiguriert ist.

| Sensor | Einheit | Beschreibung |
|--------|---------|-------------|
| Batterie Ladestand | % | SOC mit dynamischem Icon |
| Batterie Ladung Gesamt | kWh | Gesamt ins Batterie geladen |
| Batterie Entladung Gesamt | kWh | Gesamt aus Batterie entladen |
| Batterie Effizienz | % | Entladung / Ladung x 100 |
| Batterie Zyklen | Zyklen | Geschaetzt: Ladung / Kapazitaet |

### Device: Stromkontingent (optional)

Erscheint wenn das Kontingent aktiviert ist.

| Sensor | Einheit | Beschreibung |
|--------|---------|-------------|
| Kontingent Verbleibend | kWh | Verbleibende kWh im Jahresbudget |
| Kontingent Verbrauch | % | Prozent des Kontingents verbraucht |
| Kontingent Reserve | kWh | Ueber/unter Budget (positiv = gut) |
| Kontingent Tagesbudget | kWh/Tag | Erlaubter Tagesverbrauch |
| Kontingent Heute Verbleibend | kWh | Tagesbudget minus heutiger Verbrauch |
| Kontingent Prognose | kWh | Hochrechnung Jahresverbrauch |
| Kontingent Restlaufzeit | Tage | Verbleibende Tage in der Periode |
| Kontingent Status | — | Text-Zusammenfassung |

---

## Options (nach Setup aenderbar)

Unter **Einstellungen > Geraete & Dienste > PV Energy Management+ > Konfigurieren** findest du:

| Kategorie | Was du einstellen kannst |
|-----------|------------------------|
| **Sensoren** | PV Produktion, Netzeinspeisung, Netzbezug, Hausverbrauch |
| **Strompreise** | Fixpreis, Aufschlagfaktor, dynamischer Sensor, Einspeiseverguetung |
| **Amortisation Helper** | input_number fuer persistente Speicherung |
| **Historische Daten** | Bereits amortisierter Betrag, Energie-Offsets |
| **Stromkontingent** | Jahres-kWh, Startdatum, Zaehlerstand, saisonale Berechnung |
| **Batterie** | SOC, Ladung/Entladung Sensoren, Kapazitaet |
| **Energie-Benchmark** | Land, Haushaltsgroesse, Waermepumpe |

---

## Energy Dashboard

Verwende `sensor.pv_fixpreis_strompreis_brutto` als Strompreis-Entity im Home Assistant Energy Dashboard. Der Sensor gibt den Brutto-Preis in `EUR/kWh` aus.

---

## Dashboard Beispiele

### Amortisation

```yaml
type: entities
title: PV Amortisation
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

### Energie-Benchmark

```yaml
type: entities
title: Energie-Benchmark
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

### Batterie

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

### Stromkontingent

```yaml
type: entities
title: Stromkontingent
entities:
  - entity: sensor.pv_fixpreis_kontingent_status
  - entity: sensor.pv_fixpreis_kontingent_verbleibend
  - entity: sensor.pv_fixpreis_kontingent_verbrauch
  - entity: sensor.pv_fixpreis_kontingent_reserve
  - entity: sensor.pv_fixpreis_kontingent_tagesbudget
  - entity: sensor.pv_fixpreis_kontingent_heute_verbleibend
  - entity: sensor.pv_fixpreis_kontingent_prognose
```

### Tageskosten

```yaml
type: entities
title: Stromkosten Heute
entities:
  - entity: sensor.pv_fixpreis_netzbezug_heute
  - entity: sensor.pv_fixpreis_einspeisung_heute
  - entity: sensor.pv_fixpreis_stromkosten_netto_heute
```

---

## Events (Benachrichtigungen)

Die Integration feuert `pv_management_event` Events fuer eigene Automationen:

### Meilenstein-Events (25%, 50%, 75%, 100%)
```yaml
trigger:
  - platform: event
    event_type: pv_management_event
    event_data:
      type: amortisation_milestone
action:
  - service: notify.mobile_app
    data:
      title: "PV Meilenstein!"
      message: "{{ trigger.event.data.message }}"
```

### Kontingent-Warnungen
```yaml
trigger:
  - platform: event
    event_type: pv_management_event
    event_data:
      type: quota_warning_80
action:
  - service: notify.mobile_app
    data:
      title: "Stromkontingent"
      message: "{{ trigger.event.data.message }}"
```

---

## Unterschied zu pv_management

| Feature | pv_management (Spot) | pv_management_fix (Fixpreis) |
|---------|---------------------|------------------------------|
| Amortisation | Ja | Ja |
| Energie-Tracking | Ja | Ja |
| **Energie-Benchmark** | Nein | **Ja** |
| Batterie-Tracking | Nein | Ja |
| ROI-Berechnung | Nein | Ja |
| Stromkontingent | Nein | Ja |
| Tageskosten | Nein | Ja |
| Empfehlungssignal | Ja | Nein |
| Auto-Charge | Ja | Nein |
| Entlade-Steuerung | Ja | Nein |
| EPEX Quantil | Ja | Nein |
| Solcast | Ja | Nein |

Fuer **Spot-Tarife** (aWATTar, smartENERGY) mit Batterie-Management:
[pv_management](https://github.com/hoizi89/pv_management)

---

## Changelog

### v1.9.0
- **NEU: Energie-Benchmark** — Vergleich mit DACH-Durchschnitt (AT/DE/CH), CO2-Einsparung, Effizienz-Score 0-100
- **NEU: Waermepumpe** — Optionaler WP-Sensor fuer fairen Benchmark-Vergleich
- **Rename:** "PV Management Fixpreis" -> "PV Energy Management+"
- Domain und Entity-IDs bleiben unveraendert (kein Breaking Change)

### v1.8.1
- Fix: `remaining_amount` -> `remaining_cost` (Crash bei Meilensteinen)
- Fix: Fehlende "Helper" Menu-Translation

### v1.8.0
- NEU: Batterie-Tracking (SOC, Ladung, Entladung, Effizienz, Zyklen)
- NEU: ROI-Sensoren (Return on Investment + jaehrlicher ROI)
- Fix: Quota-Sensoren erscheinen ohne HA-Neustart

### v1.7.1
- Batterie-kompatible Eigenverbrauch- und Autarkiegrad-Berechnung

### v1.5.0
- NEU: Aufschlagfaktor fuer automatische Brutto-Berechnung
- NEU: Energy Dashboard Sensor (EUR/kWh)

### v1.4.0
- NEU: Helper-Sync, Meilenstein-Events, Kontingent-Warnungen, Monatszusammenfassung

### v1.1.0
- NEU: Stromkontingent (Jahres-kWh-Budget)

### v1.0.0
- Erstveroeffentlichung

---

## Support

[Fehler melden](https://github.com/hoizi89/pv_management_fix/issues) | [Diskussionen](https://github.com/hoizi89/pv_management_fix/discussions)

## Lizenz

MIT License — siehe [LICENSE](LICENSE)
