---
author: null
categories:
- Lokale KI
date: 2024-05-28
draft: false
showTableOfContents: false
showZenMode: true
slug: ein-skript-zum-exportieren-von-modellen-aus-ollama
summary: A workaround for transferring models to air-gapped Ollama instances.
tags:
- Ollama
- LLMs
- Python
title: Ein Skript zum Exportieren von Modellen aus Ollama
---

Ich wollte Ollama-Modelle auf ein System mit eingeschränktem Internetzugang laden. Leider unterstützt Ollama noch keine privaten Registries und bietet keinen Befehl zum Exportieren von Modellen. 

Als Workaround habe ich ein Python-Skript erstellt, das ein Modell aus Ollama in ein ZIP-Archiv exportieren kann, das dann in eine andere Ollama-Instanz importierbar ist.

<!-- more -->

{{< alert "lightbulb" >}}
Da Ollama inzwischen das Laden von Modellen aus benutzerdefinierten OCI Registries unterstützt, ist es mittlerweile besser, im privaten Netzwerk eine Registry zu betreiben, die Images für private Ollama Instanzen bereitstellt.
{{< /alert >}}

## Modelle aus Ollama exportieren

```bash
python export_ollama_model.py \ 
  $MODELNAME $TAGNAME \
  –repository $REPONAME \
  –output filename.zip
```

Die Angabe des Repository ist optional. Das Default Repository ist das von Ollama selbst betriebene. Hier ist ein Beispiel für `phi3:mini`:

```bash
python export_ollama_model.py phi3 mini --output phi3_mini.zip
```

Das Ergebnis ist eine ZIP-Datei, die alle zum Modell in Ollama gehörenden Dateien enthält: das Manifest und die Blobs der Image-Layer. 

## Modelle in Ollama importieren

Transferiere die ZIP-Datei auf den air-gapped Rechner und entpacke sie im lokalen `.ollama` Ordner, indem Du diesen Befehl in dem Ordner ausführen, in dem sich `.ollama` befindet (also meistens der `$HOME`):

```bash
tar -xf phi3_mini.zip
```

## Und wo ist das Skript?

Hier ist das Skript (`export_ollama_model.py`):

```python
import os
import json
import zipfile
import argparse
from pathlib import Path

def get_model_manifest_path(registry, repository, model_name, model_tag):
    return Path(f".ollama/models/manifests/{registry}/{repository}/{model_name}/{model_tag}")

def get_blob_file_path(digest):
    return Path(f".ollama/models/blobs/sha256-{digest.split(':')[1]}")

def read_manifest(ollamamodels, manifest_path):
    with open(Path.joinpath(ollamamodels, manifest_path), 'r') as file:
        return json.load(file)

def create_zip(ollamamodels, registry, repository, model_name, model_tag, output_zip):
    manifest_path = get_model_manifest_path(registry, repository, model_name, model_tag)
    manifest = read_manifest(ollamamodels, manifest_path)

    with zipfile.ZipFile(output_zip, 'w') as zipf:
        # Add manifest file
        zipf.write(Path.joinpath(ollamamodels, manifest_path), arcname=manifest_path.relative_to('.'))
        
        # Add blobs
        for layer in manifest['layers']:
            blob_path = get_blob_file_path(layer['digest'])
            zipf.write(Path.joinpath(ollamamodels, blob_path), arcname=blob_path.relative_to('.'))

        # Add config blob
        config_blob_path = get_blob_file_path(manifest['config']['digest'])
        zipf.write(Path.joinpath(ollamamodels, config_blob_path), arcname=config_blob_path.relative_to('.'))

    print(f"Model '{repository}{model_name}:{model_tag}' exported successfully to '{output_zip}'")
    print(f"You can import it to another Ollama instance with 'tar -xf <modelname>_<tag>_export.zip'")

def main():
    homedir = Path.home()
    parser = argparse.ArgumentParser(description='Export Ollama model to a zip file.')
    parser.add_argument('model_name', type=str, help='Name of the model (e.g., gemma)')
    parser.add_argument('model_tag', type=str, help='Tag of the model (e.g., 2b)')
    parser.add_argument('--ollamamodels', type=str, default=homedir, help='The folder for OLLAMA_MODELS (default: homedir)')
    parser.add_argument('--registry', type=str, default="registry.ollama.ai", help="The Ollama model registry.")
    parser.add_argument('--repository', type=str, default="library", help="name of the repository, (eg. jina)")
    parser.add_argument('--output', type=str, default='model_export.zip', help='Output zip file name')
    args = parser.parse_args()

    create_zip(args.ollamamodels, args.registry, args.repository, args.model_name, args.model_tag, args.output)

if __name__ == "__main__":
    main()
```