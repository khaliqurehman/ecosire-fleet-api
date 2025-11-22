#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Installation script for ECOSIRE Fleet API module
This script helps install and configure the module in Odoo
"""

import os
import sys
import subprocess

def install_module():
    """Install the ECOSIRE Fleet API module"""
    print("🚀 Installing ECOSIRE Fleet API Module...")
    
    # Check if we're in the right directory
    if not os.path.exists('__manifest__.py'):
        print("❌ Error: Please run this script from the module directory")
        return False
    
    print("✓ Module directory found")
    
    # Check module structure
    required_files = [
        '__manifest__.py',
        '__init__.py',
        'models/__init__.py',
        'models/res_partner.py',
        'views/res_partner_views.xml',
        'security/ir.model.access.csv'
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"❌ Missing: {file_path}")
            return False
    
    print("\n📋 Module Structure:")
    print("├── __manifest__.py (Module manifest)")
    print("├── __init__.py (Main module initialization)")
    print("├── models/")
    print("│   ├── __init__.py")
    print("│   └── res_partner.py (Contact model extension)")
    print("├── views/")
    print("│   └── res_partner_views.xml (Contact form enhancements)")
    print("├── security/")
    print("│   └── ir.model.access.csv (Access control)")
    print("└── static/")
    print("    └── description/")
    print("        └── index.html (Module description)")
    
    print("\n🎯 New Fields Added to Contact Form:")
    print("1. Commercial Registration - Text field for company registration")
    print("2. Latitude - Float field for geographical latitude")
    print("3. Longitude - Float field for geographical longitude")
    print("4. Location Display - Computed field showing formatted coordinates")
    
    print("\n📝 Installation Instructions:")
    print("1. Copy this module to your Odoo addons directory")
    print("2. Restart your Odoo server")
    print("3. Update the module list in Odoo")
    print("4. Install the 'ECOSIRE Fleet API' module")
    print("5. The new fields will appear in contact forms")
    
    print("\n✨ Installation script completed successfully!")
    return True

if __name__ == '__main__':
    install_module()
