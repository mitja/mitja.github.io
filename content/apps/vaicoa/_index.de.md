---
title: "Vaicoa"
weight: 30
subtitle: "Freigaben für KI-Agenten im IT-Betrieb"
kicker: "Projekt"
status: "Experiment"
status_note: "Experiment: Vaicoa ist ein persönliches Projekt von mir, Alpha-Software, kein Produkt und kein kommerzielles Angebot. Es gibt keinen Support, und der Code ist noch nicht öffentlich."
teaser: "Agenten schlagen vor. Du unterschreibst. Der Server prüft. Jede Änderung siehst Du als konkreten Plan, gibst sie am Handy frei, und das Zielsystem prüft Deine Signatur selbst, bevor es etwas ausführt."
summary: "Vaicoa ist eine Freigabeschicht für KI-Agenten im IT-Betrieb: Jede Änderung zeigt Dir der Kern als konkreten Plan, Du gibst ihn am Handy frei, und das Zielsystem prüft Deine Signatur selbst, bevor es etwas ausführt."
primary:
  text: "Kontakt bei Interesse"
  url: "mailto:hi@mitjamartini.com?subject=Vaicoa"
secondary:
  text: "Mehr auf vaicoa.com"
  url: "https://vaicoa.com/"
layout: product
showDate: false
showReadingTime: false
showWordCount: false
showTableOfContents: false
showPagination: false
sharingLinks: false
---

**Agenten schlagen vor. Du unterschreibst. Der Server prüft.**

## Worum es geht

Coding-Agenten können heute Betriebsarbeit erledigen: ein Deployment ausrollen, einen Server anlegen, einen Alarm stummschalten. Dafür brauchen sie Schreibrechte in Produktion. Gibst Du ihnen die Schlüssel, entscheidet am Ende das Modell, was passiert. Gibst Du sie ihnen nicht, bleibt die Arbeit bei Dir. Vaicoa ist mein Versuch, dazwischen einen Weg zu finden: Der Agent bekommt keine Schlüssel, sondern darf nur vorschlagen.

## So funktioniert es

1. **Vorschlag.** Der Agent wählt eine Aktion aus einem signierten Katalog, etwa einen Deploy oder einen Pull Request. Was nicht im Katalog steht, kann er nicht vorschlagen.
2. **Plan.** Der Kern prüft die Parameter, berechnet aus dem aktuellen Zustand einen Plan (vorher → nachher) und lässt die Policy entscheiden: ablehnen, ausführen oder eine Freigabe verlangen.
3. **Freigabe.** Braucht es eine Freigabe, landet sie auf Deinem Handy. Die App zeigt Dir den Plan, Du gibst ihn mit Face ID frei, und das Gerät signiert mit einem Schlüssel, der es nicht verlässt.
4. **Prüfung und Ausführung.** Der Node auf dem Zielsystem holt die Änderung ab, prüft Signatur, Team-Roster und Plan selbst und führt genau diesen Plan aus.
5. **Protokoll.** Jeder Schritt landet in einem hash-verketteten Audit: wer vorgeschlagen hat, wer freigegeben hat, was gelaufen ist.

Freigeben kannst Du mit Apps für iPhone, Android und Mac oder mit der Kommandozeile.

## Was der Server selbst prüft

Der Kern ist nicht die letzte Instanz. Der Node auf jedem Host verlässt sich nicht auf ihn, sondern prüft vor jeder Änderung:

- **Die Signatur.** Du signierst einen Digest über Aktion, Parameter, Plan und Nachweise. Ändert der Kern einen Teil davon, ist Deine Signatur ungültig.
- **Den Roster.** Ob Du freigeben darfst, prüft der Node gegen den signierten Team-Roster, den er selbst gepinnt hat.
- **Den Plan.** Hat sich der Zustand seit Deiner Freigabe geändert, ist sie ungültig, und es braucht eine neue.

Dazu kommen Regeln, die für alle gelten: Riskante Aktionen brauchen immer einen Menschen, und wer vorschlägt, gibt nicht selbst frei. Die zwei Ausnahmen, der Allein-Modus und der Notfall-Change, sind sichtbar markiert und stehen im Audit.

## Grenzen

- **Alpha.** Formate und Schnittstellen ändern sich ohne Ankündigung. Es gab kein unabhängiges Audit, nur interne und automatisierte Reviews.
- **Aktionen gegen fremde APIs** wie Hetzner Cloud oder Forgejo prüft der Kern, nicht ein Node. Für sie ist der Kern der Kontrollpunkt.
- **Freigaben durch Reviewer-Agenten** kann ein Node noch nicht prüfen, nur Freigaben von Menschen.
- **Die Apps** sind aus dem Quellcode gebaut, nicht in den Stores, und bisher nur in Simulatoren und Emulatoren gelaufen, nicht auf echten Geräten.

Die vollständige Liste steht auf [vaicoa.com](https://vaicoa.com/docs/limitations/).

## Stand und wie es weitergeht

Vaicoa ist ein persönliches Experiment. Ich erprobe es zuerst in meinem eigenen Betrieb und arbeite dafür das Handbuch Schritt für Schritt durch. Danach entscheide ich, wie es weitergeht. Die Idee ist im Moment, es als Open Source zu veröffentlichen.

## Kontakt

Wenn Dich das Thema interessiert oder Du Fragen hast, schreib mir an [hi@mitjamartini.com](mailto:hi@mitjamartini.com?subject=Vaicoa).
