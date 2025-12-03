#!/usr/bin/env python3
"""
Jekyll Blog Post Publisher
Converts a simple markdown file to Jekyll format and publishes it.
"""

import os
import sys
import re
from datetime import datetime
import subprocess


def slugify(text):
    """Convert text to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text


def extract_title_from_content(content):
    """Extract title from markdown content (first # heading or first line)."""
    lines = content.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('# '):
            return line[2:].strip()
        elif line and not line.startswith('---'):
            return line.strip()
    return "Untitled Post"


def has_front_matter(content):
    """Check if content already has YAML front matter."""
    return content.strip().startswith('---')


def add_front_matter(content, title, date):
    """Add YAML front matter to markdown content."""
    front_matter = f"""---
title: "{title}"
date: {date.strftime('%Y-%m-%d %H:%M:%S %z')}
categories:
  - blog
tags:
  - post
layout: single
author_profile: true
read_time: true
comments: true
share: true
related: true
---

"""
    # Remove the title from content if it's the first heading
    lines = content.strip().split('\n')
    if lines and lines[0].strip().startswith('# '):
        content = '\n'.join(lines[1:]).strip()
    
    return front_matter + content


def publish_post(draft_path, auto_commit=True):
    """Publish a draft post to the blog."""
    if not os.path.exists(draft_path):
        print(f"❌ Error: File '{draft_path}' not found!")
        return False
    
    # Read the draft content
    with open(draft_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if it already has front matter
    if has_front_matter(content):
        print("✓ Post already has YAML front matter")
        final_content = content
        # Try to extract title from front matter
        title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
        if title_match:
            title = title_match.group(1)
        else:
            title = extract_title_from_content(content)
    else:
        # Extract title and add front matter
        title = extract_title_from_content(content)
        print(f"✓ Extracted title: {title}")
        
        date = datetime.now()
        final_content = add_front_matter(content, title, date)
        print(f"✓ Added YAML front matter")
    
    # Generate filename
    date = datetime.now()
    slug = slugify(title)
    filename = f"{date.strftime('%Y-%m-%d')}-{slug}.md"
    target_path = os.path.join('docs', '_posts', filename)
    
    # Ensure target directory exists
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    
    # Write the post
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"✓ Created post: {target_path}")
    
    if auto_commit:
        # Git operations
        try:
            subprocess.run(['git', 'add', target_path], check=True)
            commit_message = f'Add new post: {title}'
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            print(f"✓ Committed to git")
            
            # Ask for push confirmation
            response = input("Push to GitHub? (y/n): ").strip().lower()
            if response == 'y':
                subprocess.run(['git', 'push', 'origin', 'master'], check=True)
                print(f"✓ Pushed to GitHub")
                print(f"\n🎉 Post published successfully!")
            else:
                print(f"\n✓ Post committed locally. Push manually when ready.")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Git error: {e}")
            print(f"Post created at {target_path} but not committed.")
    
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python publish_post.py <draft_file.md>")
        print("\nExample:")
        print("  python publish_post.py drafts/my-new-post.md")
        sys.exit(1)
    
    draft_path = sys.argv[1]
    auto_commit = '--no-commit' not in sys.argv
    
    publish_post(draft_path, auto_commit)


if __name__ == '__main__':
    main()
