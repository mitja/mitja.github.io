---
title: "Was beim Vibe Coding Zeit kostet"
slug: was-beim-vibe-coding-zeit-kostet
date: 2026-01-13
categories: ["AI Engineering", "Blog"]
tags: ["Vibe Coding", "Flet"]
stream: false
---

Vibe Scripting ist für mich, wenn ich kleine Tools für mich selbst mit Hilfe von Coding Agents entwickle. Das funktioniert wirklich extrem gut und, vor allem, wenn es sich um Kommandozeilen-Tools handelt.

Ich hab es neulich einem Steuerberater davon erzählt, er war interessiert und wollte sehen, wie es funktioniert. Ich hab dann vor Ort ein kleines Beispiel, einen Umsatzssteuer-Rechner, entwickelt. Sicher kein sehr gutes Beispiel, aber mir fiel auf die Schnelle nichts Besseres ein.

Das hat gut funktioniert und nach fünf Minuten war der Umsatzssteuer-Rechner mit Flet/Flutter GUI am Start. 

Ich konnte aber auch sehen: Da kann noch einiges verbessert werden. Beispielsweise war das Layout nicht toll und die Funktionalität zu eingeschränkt.

Weil ich wissen wollte, wie lange es dauert, daraus eine etwas vollständigere Lösung zu machen, habe ich dann später daraus einen USt Rechner für alle EU Länder gemacht, der mit einer kleinen KI Pipeline die Raten und Beschreibungen, welche Produktkategorien mit welcher Umsatzssteuer bezuschlagt werden, von offiziellen EU Seiten lädt und in einem verbesserten GUI anzeigt.

{{< figure
    src="ust-rechner.png"
    alt="EU USt Rechner"
    caption="Der EU USt Rechner nach 2h Entwicklungszeit"
    >}}

Aus 5 Minuten für die einfache Version wurden dann rund zwei Stunden. Natürlich ist es jetzt auch viel besser. Aber es ist schon interessant, wie groß der Aufwandsunterschied ist zwischen einer Lösung, die einem spezifischen, eng begrenztem Zweck dient und einer App, die allgemeiner verwendbar ist. Da steckt viel Arbeit drin und Finesse ist nötig. Ich brauche dafür Iterationen mit "Human in the loop". Vielleicht gibt es auch Entwickler, die alles perfekt vorab spezifizieren können. Mir hilft, etwas vor Augen zu haben, um es dann bewerten und verbessern zu können. 

KI beschleunigt Iterationen enorm, und man kann sich entscheiden, ob man es früher als "gut genug" betrachtet, oder eben noch ein paar weitere Iterationen dreht. Ich glaube das ist ein wichtiger Grund warum ich mit KI nicht schneller entwickle. Ich stecke die Zeit in mehr Iterationen, anstatt früher aufzuhören. Und vielleicht auch in "weniger Nachdenken vorab", was dann wieder zu mehr Iterationen führt.
