#!/usr/bin/env python3
"""
Tesla Robotaxi Monitor - Cleanup Script
Removes temporary files, caches, and old data
"""

import os
import shutil
from datetime import datetime

# Get script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def cleanup():
    """Clean up temporary files and caches"""
    print("\n" + "="*80)
    print("TESLA MONITOR CLEANUP SCRIPT")
    print("="*80 + "\n")
    
    cleaned_items = []
    errors = []
    
    # 1. Remove Python cache
    print("🧹 Cleaning Python cache files...")
    pycache_dirs = [
        os.path.join(SCRIPT_DIR, '__pycache__'),
        os.path.join(SCRIPT_DIR, 'output', '__pycache__'),
    ]
    
    for cache_dir in pycache_dirs:
        if os.path.exists(cache_dir):
            try:
                shutil.rmtree(cache_dir)
                cleaned_items.append(f"✅ Removed: {cache_dir}")
            except Exception as e:
                errors.append(f"❌ Error removing {cache_dir}: {e}")
    
    # 2. Remove .pyc files
    print("🧹 Cleaning .pyc files...")
    for root, dirs, files in os.walk(SCRIPT_DIR):
        for file in files:
            if file.endswith('.pyc'):
                pyc_path = os.path.join(root, file)
                try:
                    os.remove(pyc_path)
                    cleaned_items.append(f"✅ Removed: {pyc_path}")
                except Exception as e:
                    errors.append(f"❌ Error removing {pyc_path}: {e}")
    
    # 3. Remove .DS_Store files (macOS)
    print("🧹 Cleaning .DS_Store files...")
    for root, dirs, files in os.walk(SCRIPT_DIR):
        for file in files:
            if file == '.DS_Store':
                ds_path = os.path.join(root, file)
                try:
                    os.remove(ds_path)
                    cleaned_items.append(f"✅ Removed: {ds_path}")
                except Exception as e:
                    errors.append(f"❌ Error removing {ds_path}: {e}")
    
    # 4. Clean up old temporary files
    print("🧹 Cleaning temporary files...")
    temp_patterns = ['.tmp', '.temp', '~']
    for root, dirs, files in os.walk(SCRIPT_DIR):
        for file in files:
            if any(file.endswith(pattern) for pattern in temp_patterns):
                temp_path = os.path.join(root, file)
                try:
                    os.remove(temp_path)
                    cleaned_items.append(f"✅ Removed: {temp_path}")
                except Exception as e:
                    errors.append(f"❌ Error removing {temp_path}: {e}")
    
    # 5. Clean up Jupyter checkpoints
    print("🧹 Cleaning Jupyter checkpoints...")
    checkpoint_dir = os.path.join(SCRIPT_DIR, '.ipynb_checkpoints')
    if os.path.exists(checkpoint_dir):
        try:
            shutil.rmtree(checkpoint_dir)
            cleaned_items.append(f"✅ Removed: {checkpoint_dir}")
        except Exception as e:
            errors.append(f"❌ Error removing {checkpoint_dir}: {e}")
    
    # Summary
    print("\n" + "="*80)
    print("CLEANUP SUMMARY")
    print("="*80 + "\n")
    
    if cleaned_items:
        print(f"✅ Cleaned {len(cleaned_items)} items:")
        for item in cleaned_items[:10]:  # Show first 10
            print(f"   {item}")
        if len(cleaned_items) > 10:
            print(f"   ... and {len(cleaned_items) - 10} more")
    else:
        print("✅ System already clean - no items to remove")
    
    if errors:
        print(f"\n⚠️  {len(errors)} errors encountered:")
        for error in errors[:5]:  # Show first 5
            print(f"   {error}")
        if len(errors) > 5:
            print(f"   ... and {len(errors) - 5} more")
    
    print("\n" + "="*80)
    print(f"✅ CLEANUP COMPLETE - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80 + "\n")

if __name__ == "__main__":
    cleanup()

