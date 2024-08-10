---
date: 2023-10-16
title: Local LLMs on a Windows Laptop without a GPU
author: mitja
category: Local LLMs
tags:
 - Phi
 - Ollama
 - Windows
 - AI Laptop
---

Generative AI ist am einfachsten über eine API oder Dienste wie ChatGPT nutzbar. Da sind die besten Modelle verfügbar. Hin und wieder kann man diese aber nicht nutzen, etwa, weil Unternehmensdaten nicht rausgehen dürfen, oder für langlaufende Experimente mit potenziell hohen Kosten. In diesen Fällen kann man sich mit lokalen LLMs behelfen. Dank Quantisierung, Tools wie llama.cpp und Ollama und mittlerweile recht starken kleinen Modellen ist das sogar auf Windows Laptops ohne GPU möglich.

Ich hab einiges ausprobiert und finde, dass Phi und Ollama eine sehr gute Kombination sind. Hier zeige ich Dir, wie Du das auf einem Windows Laptop ohne GPU und mit restriktivem Internet Zugang zum Laufen bekommst und welche Performance Du damit erhälst.

## Voraussetzungen

- Windows Laptop mit relativ aktueller CPU und möglichst mindestens 16 GB RAM. Es kann auch auf 8 GB laufen, aber dann wird es schon sehr langsam.

## Schritte zu Installation

- Installiere Ollama
- Lade Phi über den Browser herunter
- erstelle ein Modelfile und lade damit das Modell in Ollama
- starte Ollama

Jetzt kannst Du es von der Kommandozeile nutzen. Über `--verbose` kannst Du sehen, wie schnell es ist. Ich nutze es gerne mit Excel, dafür hab ich das beigefügte Excel Spreadsheet mit VBA Makro erstellt. Auch gut: LLM von Simon Wilison.

## Performance

Hier sind einige Vergleichswerte zwischen Phi, Gemma, Mistral7B mit den Default Tags von Ollama auf verschiedenen Systemen:

| Modell | System | Geschwindigkeit |
|--------|--------|-----------------|
| Phi-2  | Surfacebook 8, Windows 11 , 16 GB RAM | 1 ms / Token    |
| Phi-2  | Mac Mini M1 16 GB RAM | 1 ms / Token    |
| Phi-2  | MacBook Pro | 1 ms / Token    |
| Phi-2  | Windows 11 Pro, AMD, 16 GB RAM, GPU | 1 ms / Token    |

Phi-2 ist wie ich finde ein guter Kompromiss - Mistral 7b ist schon sehr langsam auf dem Windows Laptop, Gemma fand ich von der Qualität her nicht so gut, ist aber einen Versuch wert, weil es schon noch etwas schneller ist.

Bei der Hardware ist ein MacBook aktuell eindeutig der beste Einstieg in lokale Modelle auf Laptops. Selbst ein MacBook Air ist schnell genug für Echtzeit-Interaktionen, auch mit Mistral 7b (ab 50 Token/s fühlt sich das komplett flüssig an). Mind. 16 GB (Air M2 derzeit für unter 1500 EUR) besser das 24 GB Modell (Macbook Air M2 um 1900 EUR, was auch Modelle in der 13B Klasse laufen lassen kann). MBA 8 GB kann Phi-2 schnell laufen lassen um 1000 EUR. PCs ohne GPU, also in der Preisklasse um 1000 EUR bis 2000 EUR sind dagegen nur für sehr kleine lokale Modelle bei langsamer Performance geeignet.

Der PC zeigt, dass selbst mit einer alten GPU sehr gute Performance möglich ist. Ich habe Ollama angewiesen alle Layer auf der GPU zu berechnen. Ich denke, dass Laptops mit GPU und mindestens 8 GB vRAM sehr gut für sehr schnelle Inferenz mit 7B Modellen geeignet sind. Die vRAM nutzung war, damit könnten eventuell auch GPUs mit 6 GB vRAM ausreichen, Beispiel [Dell XPS-16](https://www.dell.com/de-de/shop/cty/pdp/spd/xps-16-9640-laptop/cn96007cc?tfcid=84651726&&gacd=9639087-5496-5761040-271209370-0&dgc=ST&SA360CID=71700000111180735&&gad_source=1&gclid=CjwKCAjww_iwBhApEiwAuG6ccONpO5gRVQAi91I3eaR-R8ZAGGGn9TBzyo_B--l1E6TjWYo9SkzGhhoCWdwQAvD_BwE&gclsrc=aw.ds), 16 Zoll Bildschirm, Intel Core Ultra 7 155H (16 Cores), NVIDIA GeForce RTX 4070 mit 8 GB vRAM, 32 GB RAM, 1 TB NVMe kostet rd. 3000 EUR. Der selbe Laptop mit NVIDIA GeForce RTX 4060 mit 6 GB vRAM ist nur 100 EUR günstiger. ich würde da eindeutig die 8GB Variante nehmen. NVIDIA GPUs sind flexibel und am besten unterstützt. Die Intel ARC GPU würde ich aktuell noch nicht nehmen, auch weil dann max. 16 GB RAM insgesamt unterstützt werden. Die kommenden AI PCs von Microsoft und Intel angekündigt werden die Situation für Windows Anwender sicher nochmals verbessern.

## Zusammenfassung

- Phi-2 ist auf Windows Laptops ohne GPU mit geringer Performance verwendbar
- MacBooks oder Laptops mit GPU bieten flüssige Nutzung auch mit 7B Modellen wie Mistral, kosten aber rd. 2500 EUR (MacBook) bzw. 3000 EUR (Dell XPS-16 mit NVIDIA GeForce RTX 4070 GPU)
- AI Laptops bringen lokale Inferenz hoffentlich auch in die 1000 EUR Laptop Klasse

Mehr Details zu Ollama findest Du hier: [Ollama]().
Mehr Details zu Phi findest Du hier: [Phi]().