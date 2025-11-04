#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "pydantic-ai",
#     "openai",
#     "pydantic>=2.0",
#     "python-frontmatter",
# ]
# ///

"""
Translate Hugo markdown posts between languages using Pydantic AI and OpenAI.

Usage:
    # Translate from English to German (default)
    ./translate.py content/posts/my-post/index.md

    # Translate all posts from English to German
    ./translate.py "content/posts/*/index.md"

    # Translate from German to English
    ./translate.py --from-lang de --to-lang en content/posts/my-post/index.de.md

    # Translate all German posts to English
    ./translate.py --to-lang en "content/posts/*/index.de.md"
"""

import argparse
import sys
from pathlib import Path
from typing import Optional
import frontmatter
from pydantic import BaseModel, Field
from pydantic_ai import Agent


class TranslatedContent(BaseModel):
    """Structured translation result."""

    title: str = Field(description="Translated title")
    slug: str = Field(description="URL-friendly slug for the translated content (lowercase, hyphenated)")
    content: str = Field(description="Translated markdown content")
    categories: Optional[list[str]] = Field(default=None, description="Translated categories if applicable")
    tags: Optional[list[str]] = Field(default=None, description="Translated tags if applicable")


class MarkdownTranslator:
    """Translates markdown files between languages using Pydantic AI."""

    LANGUAGE_NAMES = {
        'en': 'English',
        'de': 'German',
    }

    def __init__(self, model_name: str = "gpt-5", source_lang: str = "en", target_lang: str = "de"):
        """Initialize translator with OpenAI model.

        Args:
            model_name: OpenAI model to use (e.g., 'gpt-5', 'gpt-5-mini')
            source_lang: Source language code (e.g., 'en', 'de')
            target_lang: Target language code (e.g., 'en', 'de')
        """
        self.source_lang = source_lang
        self.target_lang = target_lang
        source_name = self.LANGUAGE_NAMES.get(source_lang, source_lang)
        target_name = self.LANGUAGE_NAMES.get(target_lang, target_lang)

        self.agent = Agent(
            f'openai:{model_name}',
            output_type=TranslatedContent,
            system_prompt=(
                f"You are a professional translator specializing in technical content. "
                f"Translate the provided {source_name} content to {target_name}, maintaining the "
                f"markdown formatting, technical terms, and tone. Keep code blocks, "
                f"URLs, and proper nouns unchanged. Translate categories and tags "
                f"where it makes sense, but keep technical terms in English."
            ),
        )

    async def translate_post(self, source_path: Path) -> bool:
        """Translate a single markdown post.

        Args:
            source_path: Path to the source markdown file

        Returns:
            True if translation was successful, False otherwise
        """
        # Detect source language from filename and determine target path
        stem = source_path.stem
        suffix = source_path.suffix

        # Remove language code from stem if present (e.g., index.de -> index)
        detected_lang = None
        if '.' in stem:
            parts = stem.split('.')
            if len(parts) > 1 and parts[-1] in self.LANGUAGE_NAMES:
                detected_lang = parts[-1]
                stem = '.'.join(parts[:-1])

        # Generate target filename
        if self.target_lang == 'en':
            # For English, use plain stem (index.md)
            target_stem = stem
        else:
            # For other languages, add language code (index.de.md)
            target_stem = f"{stem}.{self.target_lang}"

        target_path = source_path.parent / f"{target_stem}{suffix}"

        # Check if target already exists
        if target_path.exists():
            print(f"⏭️  Skipping {source_path} - translation already exists at {target_path}")
            return False

        # Read and parse source file
        try:
            post = frontmatter.load(source_path)
        except Exception as e:
            print(f"❌ Error reading {source_path}: {e}")
            return False

        # Prepare translation prompt
        categories = post.get('categories', [])
        tags = post.get('tags', [])
        target_name = self.LANGUAGE_NAMES.get(self.target_lang, self.target_lang)

        # Get the directory name as context for slug
        directory_name = source_path.parent.name

        prompt = f"""You are translating a blog post to {target_name}.

Original title: {post.get('title', 'Untitled')}
Original categories: {', '.join(categories) if categories else 'None'}
Original tags: {', '.join(tags) if tags else 'None'}

Blog post content to translate:
---
{post.content}
---

Instructions:
1. Translate ONLY the blog post content above to {target_name}
2. Maintain all markdown formatting exactly
3. Keep code blocks, URLs, and HTML comments unchanged
4. Provide a translated title
5. Provide a URL-friendly slug (lowercase, hyphenated) based on the translated title
   Example: "Der schnelle Solopreneur" → slug: "der-schnelle-solopreneur"
6. Translate categories and tags where appropriate

DO NOT include any labels like "Title:", "Content:", etc. in your translation."""

        # Translate using Pydantic AI
        print(f"🔄 Translating {source_path}...")
        try:
            result = await self.agent.run(prompt)
            translated = result.output
        except Exception as e:
            print(f"❌ Translation failed for {source_path}: {e}")
            return False

        # Create new post with translated content
        new_post = frontmatter.Post(translated.content)

        # Copy over metadata, translating where appropriate
        new_post['title'] = translated.title
        new_post['date'] = post.get('date')
        new_post['author'] = post.get('author')
        new_post['draft'] = post.get('draft', False)

        # Always add slug to make URLs independent of folder structure
        new_post['slug'] = translated.slug

        # Use translated categories/tags if provided, otherwise keep original
        if translated.categories:
            new_post['categories'] = translated.categories
        elif categories:
            new_post['categories'] = categories

        if translated.tags:
            new_post['tags'] = translated.tags
        elif tags:
            new_post['tags'] = tags

        # Copy any other metadata (but skip slug for source content)
        for key, value in post.metadata.items():
            if key not in ['title', 'date', 'author', 'draft', 'categories', 'tags', 'slug']:
                new_post[key] = value

        # Write translated file
        try:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(frontmatter.dumps(new_post))
            print(f"✅ Translated to {target_path}")
            return True
        except Exception as e:
            print(f"❌ Error writing {target_path}: {e}")
            return False


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Translate Hugo markdown posts between languages using Pydantic AI"
    )
    parser.add_argument(
        'paths',
        nargs='+',
        help='Path(s) to markdown file(s), supports glob patterns'
    )
    parser.add_argument(
        '--model',
        default='gpt-5',
        help='OpenAI model to use (default: gpt-5)'
    )
    parser.add_argument(
        '--from-lang',
        '--source-lang',
        dest='source_lang',
        default='en',
        help='Source language code (default: en)'
    )
    parser.add_argument(
        '--to-lang',
        '--target-lang',
        dest='target_lang',
        default='de',
        help='Target language code (default: de)'
    )

    args = parser.parse_args()

    # Expand glob patterns
    files_to_translate = []
    for path_pattern in args.paths:
        path = Path(path_pattern)
        if '*' in path_pattern or '?' in path_pattern:
            # Glob pattern
            base_path = Path('.')
            matches = list(base_path.glob(path_pattern))
            files_to_translate.extend([m for m in matches if m.is_file()])
        elif path.is_file():
            files_to_translate.append(path)
        else:
            print(f"⚠️  Warning: {path_pattern} is not a file or valid pattern", file=sys.stderr)

    if not files_to_translate:
        print("❌ No files found to translate", file=sys.stderr)
        sys.exit(1)

    print(f"📝 Found {len(files_to_translate)} file(s) to translate")
    print(f"🔄 Translating from {args.source_lang} to {args.target_lang}\n")

    # Initialize translator
    translator = MarkdownTranslator(
        model_name=args.model,
        source_lang=args.source_lang,
        target_lang=args.target_lang
    )

    # Translate each file
    successful = 0
    skipped = 0
    failed = 0

    for file_path in files_to_translate:
        result = await translator.translate_post(file_path)
        if result:
            successful += 1
        elif file_path.parent / f"{file_path.stem}.de{file_path.suffix}".exists():
            skipped += 1
        else:
            failed += 1

    # Summary
    print(f"\n📊 Summary:")
    print(f"   ✅ Translated: {successful}")
    print(f"   ⏭️  Skipped: {skipped}")
    print(f"   ❌ Failed: {failed}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
