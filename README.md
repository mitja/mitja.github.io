# My Blog

This is my blog. I write mostly about AI Engineering. 

I'm using Hugo with the [Blowfish](https://github.com/nunocoracao/blowfish) theme. Here is how to serve it, locally:

```sh
hugo serve
```

I've experiemented with the terminal theme and added missing shortcuts (alert, carousel, youtubeLite). You can see how it would look like with the terminal theme:

```sh
hugo serve -t my-terminal,terminal
```
## Embedding Apps with iframed

The `iframed` shortcode allows embedding external apps (like Python Air demos) in blog posts. Use it in markdown like this:

```markdown
{{</* iframed url="chatty.mitjamartini.com" title="Chat Demo" height="600px" */>}}
```

Parameters: `url` (required), `title` (optional), `height` (optional, default "600px"), `responsive` (optional, set to "true" for 16:9 aspect ratio).

## Creating New Posts

The `new-post.py` script creates new blog posts with automatic year/month folder organization.

### Usage

**Create a new English post:**
```sh
./new-post.py "My Awesome Post Title"
```

**Create a new German post:**
```sh
./new-post.py "Mein toller Artikel" --lang de
```

**Create as draft:**
```sh
./new-post.py "Draft Post" --draft
```

### What it does

- Creates post in `content/posts/YYYY/MM/slug/` structure
- Generates URL-friendly slug from title
- **For German posts**: Automatically translates title to English for folder name (requires `OPENAI_API_KEY`)
- Adds localized slug to front matter for language-specific URLs
- Sets up proper front matter with date and title
- Optionally marks as draft

### Examples

**English post:**
```sh
./new-post.py "AI Engineering Tips"
```

Creates:
```
content/posts/2025/10/ai-engineering-tips/
└── index.md
```

**German post** (with automatic English folder naming):
```sh
./new-post.py "Kleine Python Scripte entwickeln" --lang de
```

Creates:
```
content/posts/2025/10/developing-small-python-scripts/
└── index.de.md  (with German slug in front matter)
```

This keeps folder names in English for easy navigation while URLs are localized:
- Folder: `developing-small-python-scripts/`
- German URL: `/de/posts/kleine-python-scripte-entwickeln/`
- English URL (after translation): `/posts/developing-small-python-scripts/`

## Translating Posts

The `translate.py` script uses Pydantic AI and OpenAI to translate blog posts between English and German. It automatically generates translated slugs for clean, language-specific URLs.

### Requirements

Set your OpenAI API key:
```sh
export OPENAI_API_KEY="your-key-here"
```

### Usage

**Translate from English to German (default):**
```sh
./translate.py content/posts/my-post/index.md
```

**Translate from German to English:**
```sh
./translate.py --to-lang en content/posts/my-post/index.de.md
```

**Translate all posts:**
```sh
# For flat structure
./translate.py "content/posts/*/index.md"

# For year/month structure
./translate.py "content/posts/*/*/*/index.md"
```

**Use a different model:**
```sh
./translate.py --model gpt-4o content/posts/my-post/index.md
```

### How it works

- Translates title, content, categories, and tags
- Generates URL-friendly slugs for both languages (e.g., `der-schnelle-solopreneur`)
- Preserves markdown formatting, code blocks, and links
- Never overwrites existing translations
- Keeps files organized in the same directory (`index.md` + `index.de.md`)

### URL Structure

With translated slugs, your URLs stay clean regardless of folder structure:

- English: `/posts/the-fast-solopreneur/`
- German: `/de/posts/der-schnelle-solopreneur/`

This lets you reorganize content into date-based folders (e.g., `2025/05/`) without breaking URLs.