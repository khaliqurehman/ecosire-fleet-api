#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for ECOSIRE Fleet API Contact Fields Extension
This script tests the new fields added to the res.partner model
"""

import sys
import os

# Add the Odoo server path to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

def test_contact_fields():
    """Test the new contact fields functionality"""
    print("Testing ECOSIRE Fleet API Contact Fields Extension...")
    
    try:
        # Import Odoo modules
        import odoo
        from odoo import api, SUPERUSER_ID
        
        # Initialize Odoo
        odoo.cli.server.main()
        
        # Get the database cursor
        db_name = 'odoo18'  # Adjust database name as needed
        registry = odoo.registry(db_name)
        
        with registry.cursor() as cr:
            env = api.Environment(cr, SUPERUSER_ID, {})
            
            # Test creating a partner with new fields
            partner_vals = {
                'name': 'Test Company',
                'is_company': True,
                'commercial_registration': 'CR123456789',
                'partner_latitude': 25.2048,
                'partner_longitude': 55.2708,
                'email': 'test@example.com',
                'phone': '+971501234567',
                'street': 'Sheikh Zayed Road',
                'city': 'Dubai',
                'country_id': env.ref('base.ae').id,  # UAE
            }
            
            # Create the partner
            partner = env['res.partner'].create(partner_vals)
            print(f"✓ Created partner: {partner.name}")
            print(f"✓ Commercial Registration: {partner.commercial_registration}")
            print(f"✓ Location: {partner.location_display}")
            
            # Test the computed field
            assert partner.location_display == "25.204800, 55.270800", "Location display not computed correctly"
            print("✓ Location display computed correctly")
            
            # Test updating fields
            partner.write({
                'commercial_registration': 'CR987654321',
                'partner_latitude': 25.2049,
                'partner_longitude': 55.2709,
            })
            print("✓ Updated partner fields successfully")
            
            # Test search functionality
            partners_with_cr = env['res.partner'].search([('commercial_registration', '!=', False)])
            print(f"✓ Found {len(partners_with_cr)} partners with commercial registration")
            
            partners_with_location = env['res.partner'].search([
                ('partner_latitude', '!=', False),
                ('partner_longitude', '!=', False)
            ])
            print(f"✓ Found {len(partners_with_location)} partners with location data")
            
            print("\n🎉 All tests passed successfully!")
            print("\nNew fields added to contact form:")
            print("1. Commercial Registration - Text field for company registration number")
            print("2. Latitude - Float field for geographical latitude")
            print("3. Longitude - Float field for geographical longitude")
            print("4. Location Display - Computed field showing formatted coordinates")
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False
    
    return True

if __name__ == '__main__':
    test_contact_fields()
