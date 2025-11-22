# ECOSIRE Fleet API - Contact Form Enhancement

## Overview

This module enhances the Odoo contact form by adding essential fields for fleet management and customer information tracking. It extends the `res.partner` model with commercial registration and location fields.

## Features

### 1. Commercial Registration Field
- **Field Name**: `commercial_registration`
- **Type**: Char (Text)
- **Purpose**: Store commercial registration numbers or identifiers for companies/contacts
- **Location**: Added to main contact form after VAT field
- **Visibility**: Shown for companies in simplified form

### 2. Location Fields
- **Latitude**: `partner_latitude` (Float, 10,7 precision)
- **Longitude**: `partner_longitude` (Float, 10,7 precision)
- **Location Display**: `location_display` (Computed field showing formatted coordinates)
- **Purpose**: Store geographical coordinates for fleet tracking and location-based services

### 3. Enhanced User Interface
- **Form Views**: Fields integrated into main contact form and simplified form
- **List Views**: Commercial registration column added to partner tree view
- **Search Views**: Enhanced search capabilities with location filters
- **Geocoding Button**: Placeholder for future geocoding functionality

## Installation

1. Copy the module to your Odoo addons directory
2. Update the module list in Odoo
3. Install the "ECOSIRE Fleet API" module
4. The new fields will automatically appear in contact forms

## Usage

### Adding Commercial Registration
1. Open any contact/company form
2. Find the "Commercial Registration" field (after VAT field)
3. Enter the registration number (e.g., "CR123456789")

### Adding Location Data
1. In the contact form, scroll to the "Location Information" section
2. Enter latitude and longitude values manually
3. The "Location Coordinates" field will automatically display formatted coordinates
4. Use the "Get Location from Address" button for future geocoding functionality

### Searching and Filtering
- Use the search bar to find contacts by commercial registration
- Apply "Has Location Data" or "No Location Data" filters
- View commercial registration in list views

## Technical Details

### Model Extensions
- **Base Model**: `res.partner`
- **New Fields**: 4 fields added
- **Computed Fields**: 1 computed field for location display
- **Methods**: 1 action method for geocoding (placeholder)

### View Modifications
- **Form Views**: Enhanced main and simplified forms
- **Tree Views**: Added commercial registration column
- **Search Views**: Enhanced search and filter capabilities

### Security
- Inherits existing `res.partner` security rules
- No additional security configuration required
- Fields follow standard Odoo access control

## Dependencies

- `base` - Core Odoo functionality
- `fleet` - Fleet management module

## Compatibility

- **Odoo Version**: 18.0+
- **Python Version**: 3.8+
- **Database**: PostgreSQL

## Future Enhancements

1. **Geocoding Integration**: Implement actual geocoding service integration
2. **Map Widget**: Add interactive map widget for location selection
3. **API Integration**: Connect with external fleet management APIs
4. **Reporting**: Add location-based reporting capabilities
5. **Validation**: Add field validation for commercial registration formats

## Support

For support and questions regarding this module, please contact the ECOSIRE development team.

## License

This module is licensed under LGPL-3.

---

**ECOSIRE Agent OS** - World-class AI-powered development intelligence system for Odoo applications.
