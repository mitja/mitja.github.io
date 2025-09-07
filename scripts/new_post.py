#!/usr/bin/env python3
"""
Script to create new Jekyll blog posts with proper front matter and filename.
"""
import os
import re
import sys
from datetime import datetime
from pathlib import Path


def slugify(text):
    """Convert text to URL-friendly slug."""
    # Convert to lowercase and replace spaces with hyphens
    slug = re.sub(r'[^\w\s-]', '', text.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')


def create_new_post(title, category=None, tags=None, author="mitja"):
    """Create a new blog post with proper Jekyll front matter."""
    
    # Get current date
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    
    # Create slug from title
    slug = slugify(title)
    
    # Create filename
    filename = f"{date_str}-{slug}.md"
    
    # Determine the correct directory (_posts or _drafts)
    base_dir = Path(__file__).parent.parent
    posts_dir = base_dir / "_posts"
    drafts_dir = base_dir / "_drafts"
    
    # Default to drafts directory
    target_dir = drafts_dir
    file_path = target_dir / filename
    
    # Create tags list
    if tags:
        if isinstance(tags, str):
            tags = [tag.strip() for tag in tags.split(',')]
        tags_str = '[' + ', '.join(f'"{tag}"' for tag in tags) + ']'
    else:
        tags_str = '[]'
    
    # Create front matter
    front_matter = f"""---
title: "{title}"
date: {date_str}
author: {author}"""
    
    if category:
        front_matter += f"\ncategory: {category}"
    
    front_matter += f"""
tags: {tags_str}
permalink: /blog/{slug}/
---

"""
    
    # Check if file already exists
    if file_path.exists():
        print(f"Error: File {filename} already exists in {target_dir}")
        return False
    
    # Create the file
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(front_matter)
        
        print(f"Created new blog post: {file_path}")
        print(f"Title: {title}")
        print(f"Date: {date_str}")
        print(f"Slug: {slug}")
        if category:
            print(f"Category: {category}")
        print(f"Tags: {tags_str}")
        print(f"\nTo publish, move from _drafts to _posts:")
        print(f"mv {file_path} {posts_dir / filename}")
        
        return True
        
    except Exception as e:
        print(f"Error creating file: {e}")
        return False


def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) < 2:
        print("Usage: python new_post.py 'Post Title' [category] [tags]")
        print("Example: python new_post.py 'My New Post' 'Tech' 'python,ai,tutorial'")
        sys.exit(1)
    
    title = sys.argv[1]
    category = sys.argv[2] if len(sys.argv) > 2 else None
    tags = sys.argv[3] if len(sys.argv) > 3 else None
    
    if create_new_post(title, category, tags):
        print("\nPost created successfully!")
    else:
        print("\nFailed to create post.")
        sys.exit(1)


if __name__ == "__main__":
    main()