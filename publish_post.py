#!/usr/bin/env python3
"""
Jekyll Blog Post Publisher
Converts a simple markdown file to Jekyll format and publishes it.
Automatically handles image attachments.
"""

import os
import sys
import re
import shutil
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
    # Get timezone offset
    import time
    offset = -time.timezone if (time.localtime().tm_isdst == 0) else -time.altzone
    offset_hours = offset // 3600
    offset_minutes = (offset % 3600) // 60
    tz_str = f"{offset_hours:+03d}{offset_minutes:02d}"
    
    # Replace colon with hyphen in title to prevent Jekyll build errors
    safe_title = title.replace(':', ' -')
    
    front_matter = f"""---
title: "{safe_title}"
date: {date.strftime('%Y-%m-%d %H:%M:%S')} {tz_str}
categories:
  - blog
tags:
  - post
layout: single
author_profile: true
read_time: true
comments: false
share: false
related: true
---

"""
    # Remove the title from content if it's the first heading
    lines = content.strip().split('\n')
    if lines and lines[0].strip().startswith('# '):
        content = '\n'.join(lines[1:]).strip()
    
    return front_matter + content


def process_images(content, draft_dir):
    """
    Find images in markdown content, move them to images/ folder,
    rename them to be web-safe, and update markdown links.
    Returns: (updated_content, list_of_moved_images)
    """
    moved_images = []
    
    # Regex to find markdown images: ![alt](path) or <img src="path">
    # We focus on standard markdown syntax for now: ![alt](path)
    # and also capture optional title: ![alt](path "title")
    img_pattern = re.compile(r'!\[(.*?)\]\((.*?)(?:\s+"(.*?)")?\)')
    
    def replace_image(match):
        alt_text = match.group(1)
        img_path = match.group(2)
        title_text = match.group(3)
        
        # Ignore absolute URLs (http://, https://)
        if img_path.startswith(('http://', 'https://', '//')):
            return match.group(0)
        
        # Resolve local image path
        # If path starts with /, it's absolute to project root (not supported for draft moving usually)
        # We assume relative path from draft file
        local_img_path = os.path.join(draft_dir, img_path)
        
        if not os.path.exists(local_img_path):
            print(f"⚠️  Warning: Image not found at {local_img_path}")
            return match.group(0)
            
        # Prepare new filename
        original_filename = os.path.basename(img_path)
        name, ext = os.path.splitext(original_filename)
        safe_name = slugify(name) + ext.lower()
        
        # Target directory
        target_dir = 'images'
        os.makedirs(target_dir, exist_ok=True)
        target_path = os.path.join(target_dir, safe_name)
        
        # Handle duplicate filenames (append counter)
        counter = 1
        while os.path.exists(target_path):
            # If content is same, reuse it? For now just rename
            target_path = os.path.join(target_dir, f"{slugify(name)}-{counter}{ext.lower()}")
            counter += 1
            
        # Copy file
        shutil.copy2(local_img_path, target_path)
        moved_images.append(target_path)
        print(f"✓ Moved image: {original_filename} -> {target_path}")
        
        # Return new markdown link
        new_url = f"/images/{os.path.basename(target_path)}"
        if title_text:
            return f"![{alt_text}]({new_url} \"{title_text}\")"
        else:
            return f"![{alt_text}]({new_url})"

    new_content = img_pattern.sub(replace_image, content)
    return new_content, moved_images


def publish_post(draft_path, auto_commit=True):
    """Publish a draft post to the blog."""
    if not os.path.exists(draft_path):
        print(f"❌ Error: File '{draft_path}' not found!")
        return False
    
    draft_dir = os.path.dirname(draft_path)
    
    # Read the draft content
    with open(draft_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Process images FIRST (before adding front matter)
    print("🔍 Scanning for images...")
    content, moved_images = process_images(content, draft_dir)
    
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
            files_to_add = [target_path] + moved_images
            subprocess.run(['git', 'add'] + files_to_add, check=True)
            
            commit_message = f'Add new post: {title}'
            if moved_images:
                commit_message += f' (with {len(moved_images)} images)'
                
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
