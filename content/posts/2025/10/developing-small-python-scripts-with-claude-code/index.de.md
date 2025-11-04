---
title: "Kleine Scripte mit Claude Code entwickeln"
slug: kleine-scripte-mit-claude-code-entwickeln
date: 2025-10-24
draft: false
---

Claude Code ist sehr gut darin, kleine Python Skripte zu entwickeln. Das ist nicht nur praktisch (die Skripte sparen Arbeit), es ist auch ein guter Weg um Claude Code besser kennenzulernen und seine Programmierkenntnisse mit Claude Code zu verbessern.

In diesem Artikel beschreibe ich am Beispiel von zwei Python Scripten, wie ich kleine Tool geplant und ad-hoc mit Claude Code entwickele.

<!-- more -->

## Wie gehe ich vor? 

Kurz:

1) Erstes Prompt, möglichst gut durchdacht.
2) Testen und verbessern.
3) Den Code lesen und wenn nötig manuell verbessern.

Als erstes ist es super wichtig, genau zu beschreiben, was man will und welche Rahmenbedingungen dabei zu beachten sind. Ich versuche, das erste Prompt so gut wie möglich zu machen und dabei auf relevante Dokumentationen zu verweisen und vorhandene Erfahrungen zu nutzen. Je genauer, desto besser ist der erste Versuch. Bei Scripten bin ich aber nicht allzu penibel. So erstelle ich z. B. keinen Plan oder gar eine Spezifikation.

Das Script teste ich sofort, wobei ich Claude Code anweise, die Tests selbst durchzuführen. Damit sieht Claude eventuelle Fehler und die Ergebnisse und kann nötige Korrekturen erkennen und selbstständig umsetzen.

Ich schaue mir das Ergebnis auch an und bleibe "im Loop". Bei Bedarf korrigiere ich Claude oder frage weitere Tests an. Damit kann ich sofort sehen, ob mir das Ergebnis gefällt und Claude Code instruieren, das Script nach meinen Wünschen zu verbessern.

Ich finde es leichter, schnell erste Ergebnisse zu erzeugen, die ich dann in mehreren Iterationen verbessere. Oft erkenne ich erst beim Ausprobieren was ich will (und nicht will). Deswegen bin ich für kleine Scripte meist auch nicht übertrieben penibel mit meinem ersten Prompt.

Am Ende lese ich das Script durch und ändere es bei Bedarf manuell. Der Code Review ist aus meiner Sicht sehr wichtig. Nicht nur, um Sicherheitsprobleme oder gravierende Fehler zu erkennen. Ich lerne dabei meist auch neue Lösungsansätze kennen, die ich dann später vertiefen kann. Erkannte Fehler oder Fehlermuster helfen mir, künftige Prompts besser zu gestalten und sensibilisien mich für diese Fehler. ist es aus meiner Sicht wichtig, eine Programmiersprache zu verwenden, die man selbst beherrscht. Das muss nicht Python sein. TypeScript, JavaScript oder Bash kann Claude Code sicher genauso gut verwenden. Wichtig ist: Dass man sich seine Werkzeuge bewusst aussucht.

## Ein geplantes Script

`translate.py` ist ein typisches Beispiel für ein geplantes Script. Ich stelle fest, dass ich ein Script brauche und starte eine neue Claude Code Session mit dem Plan, das Script zu entwickeln. Die Motivation hinter `translate.py` ist, dass mein Blog bislang nur Englische Inhalte hat und ich künftig alle Inhalte auch in Deutsch veröffentlichen will. Das Script soll mir beim Start der Übersetzung helfen. Ich habe die Session mit folgendem Prompt gestartet (ich hab das diktiert und dann korrigiert und die Verweise ergänzt, Zeilenumbrüche habe ich nicht verwendet, aber für diesen Blog Post ergänzt: 

```
please create a python uv script that uses the Pydantic AI
and the OpenAI API with gpt-5 models to translate content 
into German. 

The script shall translate one post or generally content 
item at a time, based on the command line input argument. 

multiple tranlations in one go (iterate) shall be possible 
with glob matching. The translation shall be done for 
markdown files in folders like

@content/posts/the-speedy-solopreneur/index.md 

shall be translated and saved to a file named 

@content/posts/the-speedy-solopreneur/index.de.md 

in the same directory as the original file. 
Don't overwrite existing files. translate also 
front matter where applicable. define the dependencies 

in the script itself as described in
https://docs.astral.sh/uv/guides/scripts/#declaring-script-dependencies
```

Das Prompt enthält:

- Infos zur Programmierumgebung (Python, uv, PydanticAI, OpenAI)
- Infos zur Aufgabe (EN-DE, für einzelne oder mehrere Inhalte iterativ)
- Ein konkretes Beispiel (Quelle, wohin es übersetzt werden soll)
- Weitere Rahmenbedingungen (im gleichen Ordner, nicht überschreiben)
- Eine Referenz zu einer Dokumentation (Script-Abhängigkeiten im Script selbst deklarieren)

Das Script funktionierte nicht auf Anhieb, was daran lag, dass Claude den Code für eine veraltete Version von Pydantic AI geschrieben hat. Claude Code hat selbst festgestellt, woran der Fehler liegt. Ich habe dann trotzdem unterbrochen, um einen Hinweis zur PydanticAI Dokumentation zu geben:

```
please check the getting started with pydandic model 
to see how the new pydantic ai version is used:
https://ai.pydantic.dev/examples/pydantic-model/ 
```

Das Script hat dann auf Anhieb funktioniert. Da es so gut klappte, habe ich Claude gebeten, auch Übersetzungen von Deutsch nach Englisch zu implementieren, obwohl ich es an sich nicht brauchte:

```
please update the script so that it can also 
translate from German to English. 
```

Das hat auch funktioniert. Ich mir den von Claude übersetzten Inhalt angesehen und dabei festgestellt, dass die URL immer in Englisch ist. Ich wollte nun gerne auch die URLs übersetzen, wusste aber nicht ob das mit Hugo unter Beibehaltung der Ordnerstruktur geht. Also hab ich Claude Code gefragt:

```
is it possible with Hugo to translate the canonical path 
of an article but still keep the translation files in the
same directory?
```

Claude hat mir erklärt, dass es mit `slugs` geht und gefragt, ob das Script angepasst werden soll, was ich mit `yes please` bestätigte.

Das Script funktionierte wieder auf Anhieb. Aktuell habe ich alle Posts direkt im Ordner `posts` angelegt. Künftig will ich aber vielleicht auf Unterordner mit Jahr und Monat wechseln. Ich hab das Claude Code gesagt und gefragt, wie ich dann die "slugs" schreiben soll:

```
Great! I want to later rearrange the folder structure
to add a year and maybe a month to the path (eg. 2025/10/)
to get a better overview of my content. How should I write 
the slugs, then? I would prefer to leave the slug as short
as possible (leave the year and month out of the URL)
```

Claude Code hat es mir erklärt, dass das möglich ist, wenn in beiden Sprachen "slugs" verwendet werden und angeboten, es zu implementieren, was ich mit `yes` bestätigte. 

Claude Code hat auch diese Änderung erfolgreich umgesetzt und dann versucht zu testen, ist dabei aber auf einen Namenskonflikt gestoßen. Nach einigen vergeblichen Runden habe ich Claude unterbrochen und "aus der Patsche" geholfen:

```
I believe the copied article cannot be found under 
2025/10/the-speedy-solopreneur since the slug is 
still without the year and month. Maybe change the 
slug for the test to include year and month. 
```

Das hat geklappt. Ich hab das Script für mich erstmal als "fertig" deklariert und Claude Code gebeten die README.md um eine Beschreibung des Scripts zu ergänzen:

```
great! Please add a section to @README.md that 
describes how to use the @translate.py script.
```

Da das Blog Repository noch keine CLAUDE.md Datei hatte, hab ich Claude gebeten, auch diese anzulegen, damit Claude das Script später auch selbst verwenden kann. Bei der Gelegenheit habe ich dann Claude Code gebeten, mir ein `new-post.py` Script zu schreiben:

```
create a CLAUDE.md file for working with this project - 
mainly: a Hugo based website, main tasks: 

Create new post (in German or English first, then translate), 
create a draft. 

Please also create another small helper script in Python 
and uv that uses `hugo new content` to create a new post 
with folders like year/month/english-post-slug.

Here is a documentation on the hugo new content command: 
https://gohugo.io/commands/hugo_new_content/
```

## Ein Ad-Hoc Script

Oft stelle ich in Claude Code Sessions "nebenbei" fest, dass jetzt ein kleines Script hilfreich wäre. `new-post.py` ist ein Beispiel dafür. Hugo hat selbst ein Tool zum Erstellen neuer Inhalte, das aber nicht meine spezielle Ordnerstruktur, etc. berücksichtigt. Also bat ich Claude Code am Ende der `translate.py` Session, mir das `new-post.py` Script zu erstellen.

Obwohl die Aufforderung nur als Teil eines anderen Prompt war, hat auch dieses Script Anhieb funktioniert. Beim Testen fiel mir aber auf, dass dass eine automatische Übersetzung des Titels auch hier nett wäre. Also hab ich Claude Code gebeten, das Script anzupassen:

```
i think the new-post.py script also needs a little
translation helper (eg. with Pydantic AI) to generate
English folder names based on German titles. 
can you implement this? 
```

Claude Code hat das Script geändert, getestet und selbstständig die README.md und CLAUDE.md aktualisiert. Für einen etwas vollständigeren Test habe ich Claude Code gebeten, nochmal einen neuen Post anzulegen:

```
create a new post in German, tited "Das ist ein Test". 
```

Claude hat daraufhin automatisch das `new-post.py` Script verwendet und damit

- den Titel nach Englisch übersetzt,
- einen Ordner auf Basis des englischen Titels angelegt (`content/posts/2025/10/this-is-a-test/`) und
- in dem Ordner eine `index.de.md` Datei mit folgendem Inhalt angelegt:

```yaml
---
title: "Das ist ein Test"
slug: das-ist-ein-test
date: 2025-10-24T18:51:35+02:00
draft: true
---
```

Ich habe dann mit `/clear` den Kontext gelöscht (sozusagen eine neue Session gestartet) und Claude Code mit folgendem Prompt erfolgreich gebeten, den Blog Post anzulegen, den Du gerade liest:

```
create a new article (first in german) titled: "Kleine Python Scripte mit Claude Code entwickeln"
```

## Code Review

Der Code Review der beiden Scripte war eher oberflächlich, weil auch Fehlfunktionen keine gravierenden Auswirkungen hat. Mir ist trotzdem einiges aufgefallen, ich habe aber nur wenig geändert:

- einige nicht verwendete Variablen
- überschreibt nicht
- eigenwillige Ableitung der Sprache anhand des Dateinamens
- Glob / iterieren ist implementiert, aber nicht getestet
- namen könnte besser sein (MarkdownTranslator -> Hugo Translator?)
- neue gpt version (habe ich angepasst: gpt-5 statt gpt-4o)
- `now = datetime.now(timezone=datetime.timezon.utc)`

## Bis zur Unendlichkeit und noch viel weiter

- funktioniert super
- schnelle Ergebnisse
- oft besser als ursprünglich geplant
- so wenig Aufwand, dass man auch "nebenbei" kleine Tools entwickeln kann
- Man sollte die Programmiersprache beherrschen
- Man muss in aller Kürze recht genau beschreiben können, was man will.
- darf es nicht mit allgemein verwendbaren "produktiven" Lösungen verwechseln. Sehr spezifisch, wenig bis keine Sonderfälle. Wenige Tests (z. B. weitere Sprachen? Anderes Content Layout?) Der Sprung von solchen kleinen Tools zu wiederverwendbarer/verkaufbarer Software ist groß.
- trotzdem gerade kleine Tools die Möglichkeit zu iterieren und eine funktionierende Lösung zu erstellen, die man im Besten Fall auch noch regelmäßig verwedet. Das ist ein sehr gutes Feedback zum Lernen und Verbessern.
