#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pydantic-ai",
#     "openai",
#     "pydantic>=2.0",
# ]
# ///

"""
Create a new Hugo blog post with year/month folder structure.

Usage:
    ./new-post.py "My Awesome Post Title"
    ./new-post.py "Mein toller Artikel" --lang de
    ./new-post.py "Draft Post" --draft
"""

import argparse
import subprocess
import sys
import asyncio
from datetime import datetime, timezone
from pathlib import Path
import re
from pydantic import BaseModel, Field
from pydantic_ai import Agent


class TranslatedTitle(BaseModel):
    """Translated title result."""

    title: str = Field(description="Translated title in English")
    slug: str = Field(description="URL-friendly slug (lowercase, hyphenated)")


async def translate_title_to_english(german_title: str, model: str = "gpt-4o") -> TranslatedTitle:
    """Translate a German title to English for folder naming.

    Args:
        german_title: German title to translate
        model: OpenAI model to use

    Returns:
        TranslatedTitle with English title and slug
    """
    agent = Agent(
        f'openai:{model}',
        output_type=TranslatedTitle,
        system_prompt=(
            "You are a professional translator. Translate the provided German blog post title "
            "to English, maintaining the meaning and tone. Also provide a URL-friendly slug "
            "(lowercase, hyphenated) based on the English translation."
        ),
    )

    result = await agent.run(f"Translate this blog post title to English: {german_title}")
    return result.output


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug.

    Args:
        text: Text to convert to slug

    Returns:
        Lowercase, hyphenated slug
    """
    # Convert to lowercase
    text = text.lower()
    # Replace spaces and underscores with hyphens
    text = re.sub(r'[\s_]+', '-', text)
    # Remove special characters
    text = re.sub(r'[^\w\-]', '', text)
    # Remove multiple consecutive hyphens
    text = re.sub(r'-+', '-', text)
    # Strip leading/trailing hyphens
    text = text.strip('-')
    return text


async def create_post(title: str, lang: str = "en", draft: bool = False, model: str = "gpt-4o") -> int:
    """Create a new Hugo blog post.

    Args:
        title: Post title
        lang: Language code ('en' or 'de')
        draft: Whether to create as draft
        model: OpenAI model to use for translation

    Returns:
        Exit code (0 for success)
    """
    # For German posts, translate title to English for folder name
    german_slug = None
    if lang == "de":
        print("🔄 Translating title to English for folder name...")
        try:
            translated = await translate_title_to_english(title, model)
            slug = translated.slug
            german_slug = slugify(title)  # Also keep German slug for front matter
            print(f"✅ English folder: {slug}")
            print(f"✅ German slug: {german_slug}\n")
        except Exception as e:
            print(f"⚠️  Translation failed: {e}")
            print(f"⚠️  Falling back to German slug for folder name\n")
            slug = slugify(title)
    else:
        # For English posts, use title directly
        slug = slugify(title)

    # Get current date for folder structure
    now = datetime.now(tz=timezone.utc)
    year = now.strftime("%Y")
    month = now.strftime("%m")

    # Determine filename based on language
    if lang == "en":
        filename = "index.md"
    else:
        filename = f"index.{lang}.md"

    # Build path: content/posts/YYYY/MM/slug/index.md
    post_path = f"content/posts/{year}/{month}/{slug}/{filename}"

    # Check if post already exists
    full_path = Path(post_path)
    if full_path.exists():
        print(f"❌ Error: Post already exists at {post_path}", file=sys.stderr)
        return 1

    # Build hugo new content command
    cmd = ["hugo", "new", "content", post_path]

    print(f"📝 Creating new post:")
    print(f"   Title: {title}")
    print(f"   Language: {lang}")
    print(f"   Path: {post_path}")
    print(f"   Draft: {draft}")
    print()

    # Run hugo new content
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)

        # If draft flag is set, update the front matter
        if draft:
            if full_path.exists():
                content = full_path.read_text()
                # Replace draft: false with draft: true
                content = content.replace("draft: false", "draft: true")
                full_path.write_text(content)
                print(f"✅ Set draft: true")

        # Update the title and slug in the front matter
        if full_path.exists():
            content = full_path.read_text()
            lines = content.split('\n')

            # Find the end of front matter (second ---)
            front_matter_end = -1
            dash_count = 0
            for i, line in enumerate(lines):
                if line.strip() == '---':
                    dash_count += 1
                    if dash_count == 2:
                        front_matter_end = i
                        break

            # Update title and add slug if German
            for i, line in enumerate(lines):
                if line.startswith('title:'):
                    lines[i] = f'title: "{title}"'
                    # Add slug for German posts after title
                    if german_slug and i < front_matter_end:
                        lines.insert(i + 1, f'slug: {german_slug}')
                    break

            full_path.write_text('\n'.join(lines))
            print(f"✅ Updated title to: {title}")
            if german_slug:
                print(f"✅ Added German slug to front matter: {german_slug}")

        print(f"\n✅ Post created successfully!")
        print(f"\nNext steps:")
        print(f"1. Edit the post: {post_path}")
        print(f"2. Preview: hugo server")
        if lang == "en":
            print(f"3. Translate to German: ./translate.py {post_path}")
        else:
            print(f"3. Translate to English: ./translate.py --to-lang en {post_path}")

        return 0

    except subprocess.CalledProcessError as e:
        print(f"❌ Error running hugo new content:", file=sys.stderr)
        print(e.stderr, file=sys.stderr)
        return 1
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


async def main_async():
    """Async main entry point."""
    parser = argparse.ArgumentParser(
        description="Create a new Hugo blog post with year/month folder structure"
    )
    parser.add_argument(
        'title',
        help='Post title (will be converted to slug for folder name)'
    )
    parser.add_argument(
        '--lang',
        '--language',
        dest='lang',
        default='en',
        choices=['en', 'de'],
        help='Post language (default: en)'
    )
    parser.add_argument(
        '--draft',
        action='store_true',
        help='Create as draft'
    )
    parser.add_argument(
        '--model',
        default='gpt-4o',
        help='OpenAI model to use for title translation (default: gpt-4o)'
    )

    args = parser.parse_args()

    return await create_post(args.title, args.lang, args.draft, args.model)


def main():
    """Main entry point."""
    sys.exit(asyncio.run(main_async()))


if __name__ == "__main__":
    main()
