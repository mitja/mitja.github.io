---
date: 2024-05-28
title: "A Script to Export Models from Ollama"
author: mitja
category: Local AI
tags:
 - Ollama
 - LLMs
 - Python
---
I wanted to load Ollama models onto a system with restricted internet access. 

Unfortunately, Ollama doesn't yet support private registries or has a command for exporting models.

As a workaround, I have created a Python script that can export a model from Ollama with a single command:

```bash
python export_ollama_model.py <modelname> <tagname> –repository reponame –output filename.zip
```

Here is an example for `phi3:mini`:

```bash
python export_ollama_model.py phi3 mini --output phi3_mini.zip
```

The result is a ZIP file that contains all files related to the model in Ollama: The manifest and the blobs. 

Then I moved the ZIP file to the airgapped computer and imported it to it's local `.ollama` folder by running this command in the folder where `.ollama` is located:

```bash
tar -xf phi3_mini.zip
```

Here is the script (`export_ollama_model.py`):

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

