#!/usr/bin/env python
"""
Simple script to compile Django translations without gettext
Creates a minimal .mo file that Django can read
"""

import os
import struct

def create_mo_file(po_file, mo_file):
    """Create a minimal .mo file from .po file"""
    
    # Read .po file
    with open(po_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse translations
    translations = {}
    lines = content.split('\n')
    msgid = None
    msgstr = None
    
    for line in lines:
        line = line.strip()
        if line.startswith('msgid "'):
            msgid = line[7:-1]  # Remove 'msgid "' and '"'
        elif line.startswith('msgstr "'):
            msgstr = line[8:-1]  # Remove 'msgstr "' and '"'
            if msgid and msgstr and msgid != '""':
                translations[msgid] = msgstr
    
    # Create .mo file structure
    # MO file format: https://www.gnu.org/software/gettext/manual/html_node/MO-Files.html
    
    # Header
    magic = 0x950412de  # Magic number for .mo files
    revision = 0  # Format revision
    count = len(translations)  # Number of strings
    
    # Calculate offsets
    header_size = 28  # 7 * 4 bytes
    hash_offset = header_size
    hash_size = 0  # No hash table for simplicity
    strings_offset = hash_offset + hash_size
    
    # Create string entries
    string_entries = []
    string_data = b''
    
    # Sort translations by key for consistent ordering
    sorted_translations = sorted(translations.items())
    
    for msgid, msgstr in sorted_translations:
        # Original string (msgid)
        msgid_bytes = msgid.encode('utf-8')
        msgid_len = len(msgid_bytes)
        
        # Translated string (msgstr)
        msgstr_bytes = msgstr.encode('utf-8')
        msgstr_len = len(msgstr_bytes)
        
        # String entry: (length, offset)
        string_entries.append((msgid_len, len(string_data)))
        string_data += msgid_bytes + b'\x00'
        
        string_entries.append((msgstr_len, len(string_data)))
        string_data += msgstr_bytes + b'\x00'
    
    # Calculate final offsets
    orig_offset = strings_offset + len(string_entries) * 8
    trans_offset = orig_offset + len(string_entries) * 8
    
    # Write .mo file
    with open(mo_file, 'wb') as f:
        # Header
        f.write(struct.pack('<I', magic))  # Magic number
        f.write(struct.pack('<I', revision))  # Revision
        f.write(struct.pack('<I', count))  # Number of strings
        f.write(struct.pack('<I', orig_offset))  # Offset of original strings
        f.write(struct.pack('<I', trans_offset))  # Offset of translated strings
        f.write(struct.pack('<I', hash_offset))  # Offset of hash table
        f.write(struct.pack('<I', hash_size))  # Size of hash table
        
        # String entries (original)
        for length, offset in string_entries[::2]:  # Every other entry (msgid)
            f.write(struct.pack('<I', length))
            f.write(struct.pack('<I', offset))
        
        # String entries (translated)
        for length, offset in string_entries[1::2]:  # Every other entry (msgstr)
            f.write(struct.pack('<I', length))
            f.write(struct.pack('<I', offset))
        
        # String data
        f.write(string_data)

if __name__ == '__main__':
    po_file = 'locale/en/LC_MESSAGES/django.po'
    mo_file = 'locale/en/LC_MESSAGES/django.mo'
    
    if os.path.exists(po_file):
        create_mo_file(po_file, mo_file)
        print(f"Created {mo_file}")
    else:
        print(f"PO file not found: {po_file}") 