---
author: null
date: 2026-01-17
draft: false
slug: hardware-fuer-lokale-coding-modelle-noch-bezahlbar
title: Hardware für lokale Coding-Modelle ist noch bezahlbar. Wie lange noch?
stream: false
---
Die jüngsten Preisanstiege bei RAM haben auch die GPU-Preise nach oben getrieben. Die einzigen Systeme, die bislang nicht im gleichen Maße betroffen sind, sind Macs und High-End GPUs (RTX 6000 Pro und aufwärts). GPUs würde ich allerdings bereits als "nicht bezahlbar" einstufen: Um Coding-Modelle mit ausreichend großen Kontextfenstern zu betreiben, wären eine bis zwei RTX 6000 Pro oder drei bis sechs RTX 5090 erforderlich.

Schauen wir uns stattdessen Macs an.

|Preis|Bandbr.|CPU|RAM|NVMe|CPU|GPU|Modell|Preis/Bandbreite|Preis/Speicher|
|--|--|--|--|--|--|--|--|--|--|
|2.500 EUR|273 GB/s|M4 Pro|64 GB|1 TB|12C|16C|Mac Mini|9,15 EUR/GB/s|39,06 EUR/GB|
|4.027 EUR|546 GB/s|M4 Max|128 GB|1 TB|16C|40C|Mac Studio|7,14 EUR/GB/s|31,43 EUR/GB|
|4.200 EUR|800 GB/s|M3 Ultra|96 GB|1 TB|28C|60C|Mac Studio|**5,52 EUR/GB/s**|43,75 EUR/GB|
|6.720 EUR|800 GB/s|M3 Ultra|256 GB|2 TB|28C|60C|Mac Studio|8,40 EUR/GB/s|26,25 EUR/GB|
|11.900 EUR|800 GB/s|M3 Ultra|512 GB|4 TB|32C|80C|Mac Studio|14,87 EUR/GB/s|**23,24 EUR/GB**|

Mac Studios mit dem M3 Ultra bieten derzeit das beste Gesamtpaket. Die 96-GB-Variante ist schnell, und die RAM-Ausstattung reicht aus, um viele Allzweckmodelle mithilfe von Quantisierung auszuführen. Die 256-GB-Version ist in der Lage, Coding-Modelle mit akzeptablen Quantisierungsgraden und 64k-Kontext zu nutzen – gerade ausreichend für den Einsatz mit Coding-Agenten [^1]. Das 512-GB-Modell überschreitet leider die Marke von 10.000 €, was ich als "nicht mehr bezahlbar" betrachten würde.

Der Preisunterschied zwischen den 96-GB- und 256-GB-Varianten des Mac Studio liegt überraschend nahe an den aktuellen Marktpreisen für Arbeitsspeicher. Zum Vergleich: 256 GB DDR5-6000 kosten derzeit rund 3.430 €, also etwa 13,39 € pro GB. Die Preisdifferenz zwischen den 96-GB- und 256-GB-Versionen des Mac Studio sowie zwischen den 256-GB- und 512-GB-Modellen beträgt jeweils etwa 12,88 € pro GB bzw. 18,50 € pro GB. Würde Apple zu den üblichen Speicheraufschlägen zurückkehren, läge die 256-GB-Konfiguration sehr wahrscheinlich deutlich näher an 10.000 €.

Gehostete Inferenz ist günstiger und leistungsfähiger, kann aber nicht immer verwendet werden. Besonders Freelancer und kleinere Unternehmen dürfen bei Aufträgen für große Unternehmen allenfalls lokale Modelle verwenden, falls sie überhaupt eigene KI einsetzen dürfen. Der M3 Ultra, der im März 2025 vorgestellt wurde, hat zusammen mit verbesserten Modellen, Quantisierung und REAP eine Ära bezahlbarer lokaler Coding-Modelle eingeläutet. Diese Ära könnte nun ins Stocken geraten: Für 2026 werden weiter steigende RAM-Preise erwartet, und ein hohes Preisniveau dürfte bis 2027 oder sogar 2028 anhalten [^2].

[^1]: Basierend auf Benchmark-Ergebnissen in [r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/comments/1pw8h6w/glm476bit_mlx_vs_minimaxm216bit_mlx_benchmark/) 

[^2]: Basierend auf einer Analyse vom Dezember 2025 von [wccftech](https://wccftech.com/memory-ddr5-ddr4-shortages-last-till-q4-2027-higher-prices-throughout-2026/)
