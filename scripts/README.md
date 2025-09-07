# Blog Scripts

This directory contains scripts to help with blog management and content creation.

## new_post.py

A Python script to quickly create new blog posts with proper Jekyll front matter.

### Usage

```bash
python scripts/new_post.py 'Post Title' [category] [tags]
```

### Examples

```bash
# Basic post
python scripts/new_post.py 'My New Blog Post'

# With category
python scripts/new_post.py 'AI Tutorial' 'Tech'

# With category and tags
python scripts/new_post.py 'Getting Started with Python' 'Programming' 'python,tutorial,beginners'
```

### Features

- Automatically generates filename with current date and URL-friendly slug
- Creates proper Jekyll front matter matching your existing posts
- Creates posts in `_drafts` folder by default
- Provides instructions to move to `_posts` when ready to publish
- Handles title, category, tags, author, and permalink fields
- Prevents overwriting existing files

The script creates posts in your `_drafts` folder, so you can work on them before publishing by moving them to `_posts`.