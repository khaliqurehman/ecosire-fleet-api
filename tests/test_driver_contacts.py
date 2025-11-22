# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestDriverContacts(TransactionCase):
    """Test cases for driver contact functionality in ECOSIRE Fleet API module."""

    def setUp(self):
        super().setUp()
        self.partner_model = self.env['res.partner']
        self.country_us = self.env.ref('base.us')

    def test_create_driver_contact(self):
        """Test creating a driver contact with all required fields."""
        driver_data = {
            'name': 'John Driver',
            'contact_type': 'driver',
            'email': 'john.driver@example.com',
            'phone': '+1-555-0100',
            'driver_license_number': 'DL123456789',
            'driver_license_class': 'class_b',
            'driver_license_expiry': '2025-12-31',
            'iqama_number': '1234567890',
            'issue_number': 'ISS123456',
            'partner_latitude': 40.7128,
            'partner_longitude': -74.0060,
        }
        
        driver = self.partner_model.create(driver_data)
        
        # Verify driver contact was created
        self.assertEqual(driver.contact_type, 'driver')
        self.assertEqual(driver.is_company, False)
        self.assertEqual(driver.driver_license_number, 'DL123456789')
        self.assertEqual(driver.driver_license_class, 'class_b')
        self.assertEqual(driver.driver_license_expiry.strftime('%Y-%m-%d'), '2025-12-31')
        self.assertEqual(driver.iqama_number, '1234567890')
        self.assertEqual(driver.issue_number, 'ISS123456')

    def test_create_company_contact(self):
        """Test creating a company contact."""
        company_data = {
            'name': 'Fleet Management Corp',
            'contact_type': 'company',
            'email': 'info@fleetmanagement.com',
            'phone': '+1-555-1000',
            'commercial_registration': 'CR123456789',
        }
        
        company = self.partner_model.create(company_data)
        
        # Verify company contact was created
        self.assertEqual(company.contact_type, 'company')
        self.assertEqual(company.is_company, True)
        self.assertEqual(company.commercial_registration, 'CR123456789')

    def test_create_individual_contact(self):
        """Test creating an individual contact."""
        individual_data = {
            'name': 'Jane Individual',
            'contact_type': 'individual',
            'email': 'jane.individual@example.com',
            'phone': '+1-555-2000',
        }
        
        individual = self.partner_model.create(individual_data)
        
        # Verify individual contact was created
        self.assertEqual(individual.contact_type, 'individual')
        self.assertEqual(individual.is_company, False)

    def test_contact_type_sync_with_is_company(self):
        """Test that contact_type syncs properly with is_company field."""
        # Test setting is_company to True
        partner = self.partner_model.create({
            'name': 'Test Company',
            'is_company': True,
        })
        self.assertEqual(partner.contact_type, 'company')
        
        # Test setting is_company to False
        partner.is_company = False
        self.assertEqual(partner.contact_type, 'individual')

    def test_driver_license_fields_visibility(self):
        """Test that driver license fields are only visible for driver contacts."""
        driver = self.partner_model.create({
            'name': 'Test Driver',
            'contact_type': 'driver',
            'driver_license_number': 'DL123456789',
            'driver_license_class': 'class_b',
        })
        
        # Driver should have license fields
        self.assertTrue(driver.driver_license_number)
        self.assertTrue(driver.driver_license_class)
        
        # Change to individual - license fields should still exist but not be relevant
        driver.contact_type = 'individual'
        self.assertEqual(driver.contact_type, 'individual')

    def test_location_display_computation(self):
        """Test the location display computation."""
        partner = self.partner_model.create({
            'name': 'Test Partner',
            'contact_type': 'driver',
            'partner_latitude': 40.7128,
            'partner_longitude': -74.0060,
        })
        
        # Test location display format
        expected_display = "40.712800, -74.006000"
        self.assertEqual(partner.location_display, expected_display)
        
        # Test with no coordinates
        partner.partner_latitude = False
        partner.partner_longitude = False
        self.assertEqual(partner.location_display, "Not set")

    def test_search_filters(self):
        """Test that search filters work correctly for different contact types."""
        # Create test data
        self.partner_model.create({
            'name': 'Driver 1',
            'contact_type': 'driver',
            'email': 'driver1@example.com',
        })
        
        self.partner_model.create({
            'name': 'Company 1',
            'contact_type': 'company',
            'email': 'company1@example.com',
        })
        
        self.partner_model.create({
            'name': 'Individual 1',
            'contact_type': 'individual',
            'email': 'individual1@example.com',
        })
        
        # Test driver filter
        drivers = self.partner_model.search([('contact_type', '=', 'driver')])
        self.assertEqual(len(drivers), 1)
        self.assertEqual(drivers[0].name, 'Driver 1')
        
        # Test company filter
        companies = self.partner_model.search([('contact_type', '=', 'company')])
        self.assertEqual(len(companies), 1)
        self.assertEqual(companies[0].name, 'Company 1')
        
        # Test individual filter
        individuals = self.partner_model.search([('contact_type', '=', 'individual')])
        self.assertEqual(len(individuals), 1)
        self.assertEqual(individuals[0].name, 'Individual 1')

    def test_contact_type_display(self):
        """Test the contact type display method."""
        driver = self.partner_model.create({
            'name': 'Test Driver',
            'contact_type': 'driver',
        })
        
        display_name = driver._get_contact_type_display()
        self.assertIn('Driver', display_name)

    def test_backward_compatibility(self):
        """Test backward compatibility with existing is_company field."""
        # Create partner using old method
        partner = self.partner_model.create({
            'name': 'Test Partner',
            'is_company': True,
        })
        
        # Should automatically set contact_type to company
        self.assertEqual(partner.contact_type, 'company')
        
        # Change is_company to False
        partner.is_company = False
        self.assertEqual(partner.contact_type, 'individual')

    def test_driver_license_expiry_validation(self):
        """Test driver license expiry date validation."""
        from datetime import date, timedelta
        
        # Test with future expiry date
        future_date = date.today() + timedelta(days=365)
        driver = self.partner_model.create({
            'name': 'Test Driver',
            'contact_type': 'driver',
            'driver_license_expiry': future_date,
        })
        
        self.assertEqual(driver.driver_license_expiry, future_date)
        
        # Test with past expiry date (should still be allowed for data integrity)
        past_date = date.today() - timedelta(days=30)
        driver.driver_license_expiry = past_date
        self.assertEqual(driver.driver_license_expiry, past_date)
