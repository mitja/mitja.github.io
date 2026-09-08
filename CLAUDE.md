# Claude Code Project Guide

This is a Hugo-based blog website about AI Engineering. The site is bilingual (English/German) using Hugo's multilingual features.

## Project Structure

```
.
├── content/posts/          # Blog posts
│   ├── YYYY/MM/slug/      # Date-organized posts (future structure)
│   │   ├── index.md       # English version
│   │   └── index.de.md    # German version
│   └── slug/              # Current structure (flat)
│       ├── index.md
│       └── index.de.md
├── config/_default/        # Hugo configuration
│   ├── hugo.toml          # Main config
│   ├── languages.en.toml  # English language config
│   └── languages.de.toml  # German language config
├── themes/blowfish/        # Main theme
├── new-post.py            # Helper script to create new posts
└── translate.py           # Helper script to translate posts
```

## Main Workflows

### 1. Creating a New Blog Post

Use the `new-post.py` helper script:

```bash
# Create new English post
./new-post.py "My Awesome Post Title"

# Create new German post
./new-post.py "Mein toller Artikel" --lang de

# Create as draft
./new-post.py "Draft Post" --draft
```

**What it does:**
- Creates post in `content/posts/YYYY/MM/slug/` structure
- Generates URL-friendly slug from title
- **For German posts**: Automatically translates title to English for folder name using Pydantic AI
- Adds German slug to front matter for localized URLs
- Uses `hugo new content` under the hood
- Sets up proper front matter

**Requirements for German posts:**
- `OPENAI_API_KEY` environment variable must be set

**Folder structure created:**

English post:
```
content/posts/2025/10/my-awesome-post-title/
└── index.md
```

German post (English folder, German slug):
```
content/posts/2025/10/developing-python-scripts/  ← English folder name
└── index.de.md                                     ← German file with German slug
```

This keeps folder names in English (easier to navigate) while URLs remain localized:
- Folder: `developing-python-scripts/`
- German URL: `/de/posts/python-scripte-entwickeln/`

### 2. Translating Posts

Use the `translate.py` script with Pydantic AI and OpenAI:

```bash
# Translate English to German
./translate.py content/posts/2025/10/my-post/index.md

# Translate German to English
./translate.py --to-lang en content/posts/2025/10/my-post/index.de.md

# Translate all posts
./translate.py "content/posts/*/index.md"
./translate.py "content/posts/*/*/index.md"  # For dated structure

# Use different model
./translate.py --model gpt-4o content/posts/2025/10/my-post/index.md
```

**Requirements:**
- Set `OPENAI_API_KEY` environment variable
- Uses GPT-5 by default (configurable with `--model`)

**What it translates:**
- Title → Generates translated slug
- Content → Preserves markdown formatting
- Categories → Where applicable
- Tags → Where applicable

### 3. Rendering a Post to PDF

```bash
pandoc -d pandoc-pdf content/posts/2026/01/my-post/index.md -o my-post.pdf
```

**Files:**
- `pandoc-pdf.yaml` — XeLaTeX on A4, Charter/Seravek/Menlo, footer with author and date
- `pandoc-pdf.lua` — puts the output file name into the footer
- `pandoc-table-autowidth.lua` — sizes table columns by their content
- `pandoc-table-rules.lua` — draws a hairline between table rows

**Table widths:** pandoc otherwise derives column widths from the dashes in the
markdown separator row, so `|--|--|--|` gives equally wide columns regardless of
what is in them. `pandoc-table-autowidth.lua` measures the cells instead, leaves
narrow tables at their natural width, and splits the page between wide columns in
proportion to how much text they hold, never letting a column of prose fall below a
readable width while the page can spare it. Crowded tables step down to `\small`
and a tighter `\tabcolsep`, and long paths get break points, so nothing runs off
the page.

**Table rows** are separated by a light hairline. Pandoc styles tables with
booktabs, which rules only the head and the foot — fine for a few rows, hard to
read across twenty. `pandoc-table-rules.lua` writes a `\rowrule` at the start of
each row, which lands between rows because TeX accepts `\noalign` there; the
macro itself is defined in `header-includes`. Turn it off with
`table-row-rules: false` in the front matter.

**Code blocks** are set at 9pt, which fits 89 columns against 73 at the body
size. Every monospace font on macOS has the same 0.6em advance, so a different
font gains nothing — only the size does. Change `\footnotesize` in the
`header-includes` of `pandoc-pdf.yaml` to `\scriptsize` (8pt, 100 columns) or
`\small` (10pt, 80 columns). Lines longer than that still run off the page:
fancyvrb cannot wrap them without the `fvextra` package, which BasicTeX omits.

Opt out for a single table with a `fixed-widths` class, or set
`table-autowidth: false` in the front matter. If you change `geometry` or
`fontsize` in `pandoc-pdf.yaml`, update `table-line-width` / `table-font-size` in
the same file to match.

### 4. Local Development

```bash
# Start Hugo development server
hugo server

# Build for production
hugo

# Preview with draft posts
hugo server --buildDrafts
```

## URL Structure

The site uses **slugs** to decouple URLs from folder structure:

**Front matter:**
```yaml
---
title: "My Awesome Post"
slug: "my-awesome-post"  # Controls URL
date: 2025-10-24
---
```

**URLs:**
- English: `/posts/my-awesome-post/`
- German: `/de/posts/mein-toller-artikel/`

**Benefits:**
- Can reorganize folders without breaking URLs
- Clean, short URLs
- Language-specific slugs for SEO

## Front Matter Schema

```yaml
---
title: "Post Title"
slug: "url-friendly-slug"           # Optional for en, auto-generated by translate.py
date: 2025-10-24
author: mitja
categories: ["AI Engineering", "Blog"]
tags: ["Python", "AI"]
draft: false                         # Set to true for drafts
---
```

## Language Configuration

The site supports English (default) and German:

- **English**: Default language, served at `/posts/...`
- **German**: Served at `/de/posts/...`
- Language switcher available in theme

Files:
- `config/_default/languages.en.toml`
- `config/_default/languages.de.toml`

## Theme

Using [Blowfish](https://github.com/nunocoracao/blowfish) theme.

## Custom Shortcodes

### iframed

Embed external apps in posts:

```markdown
{{</* iframed url="chatty.mitjamartini.com" title="Chat Demo" height="600px" */>}}
```

## Common Tasks for AI Assistants

### Creating a new blog post

1. Run `./new-post.py "Post Title" [--lang de] [--draft]`
2. Edit the created file
3. Optionally translate: `./translate.py path/to/post/index.md`

### Translating existing content

1. Ensure `OPENAI_API_KEY` is set
2. Run `./translate.py` with appropriate flags
3. Review translation in created `.de.md` or `.md` file

### Modifying site configuration

- Edit files in `config/_default/`
- Language-specific config in `languages.*.toml`
- Main config in `hugo.toml`

### Working with drafts

- Set `draft: true` in front matter
- Preview: `hugo server --buildDrafts`
- Publish: Change to `draft: false`

## Important Files

- `new-post.py` - Create new posts with date structure
- `translate.py` - Translate posts between languages
- `pandoc-pdf.yaml` - Pandoc defaults for rendering a post to PDF
- `pandoc-table-autowidth.lua` - Sizes PDF table columns by their content
- `pandoc-table-rules.lua` - Draws a hairline between PDF table rows
- `config/_default/hugo.toml` - Main Hugo configuration
- `config/_default/languages.*.toml` - Language configurations
- `README.md` - User-facing documentation

## Git Workflow

The repository is tracked in git. Main branch is `main`.

## Deployment

Details TBD (check `hugo.toml` for `baseURL`)
