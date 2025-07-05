#!/usr/bin/env python
"""
Create a minimal .mo file that Django can read
"""

import struct

def create_minimal_mo():
    """Create a minimal .mo file with empty translations"""
    
    # MO file header structure
    magic = 0x950412de  # Magic number
    revision = 0  # Format revision
    count = 0  # No translations
    orig_offset = 28  # Offset of original strings
    trans_offset = 28  # Offset of translated strings
    hash_offset = 28  # Offset of hash table
    hash_size = 0  # No hash table
    
    with open('locale/en/LC_MESSAGES/django.mo', 'wb') as f:
        # Write header
        f.write(struct.pack('<I', magic))
        f.write(struct.pack('<I', revision))
        f.write(struct.pack('<I', count))
        f.write(struct.pack('<I', orig_offset))
        f.write(struct.pack('<I', trans_offset))
        f.write(struct.pack('<I', hash_offset))
        f.write(struct.pack('<I', hash_size))

if __name__ == '__main__':
    create_minimal_mo()
    print("Created minimal django.mo file") 