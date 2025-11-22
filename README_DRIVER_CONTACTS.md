# ECOSIRE Fleet API - Driver Contacts Feature

## Overview

The ECOSIRE Fleet API module now includes a third contact category called "Driver" alongside the existing Individual and Company categories. This feature extends Odoo's contact management system to better support fleet management operations.

## Features

### Contact Types

- **Individual**: Standard person contacts (existing functionality)
- **Company**: Business entity contacts (existing functionality)  
- **Driver**: Fleet drivers with license information (new feature)

### Driver-Specific Fields

- **Driver License Number**: Unique identifier for the driver's license
- **License Class**: Classification of the driver's license (Class A, B, C, D, Commercial, Motorcycle, Other)
- **License Expiry Date**: Expiration date of the driver's license

### Enhanced Contact Management

- **Contact Type Selection**: Radio button interface for easy type selection
- **Backward Compatibility**: Maintains compatibility with existing `is_company` field
- **Location Tracking**: Enhanced location fields for fleet management
- **Commercial Registration**: Business registration information for companies

## Technical Implementation

### Model Extensions

The `res.partner` model has been extended with:

- `contact_type`: Selection field with Individual/Company/Driver options
- `driver_license_number`: Char field for license number
- `driver_license_class`: Selection field for license classification
- `driver_license_expiry`: Date field for license expiration
- `commercial_registration`: Char field for business registration

### View Enhancements

- **Form Views**: Driver-specific fields appear in dedicated tabs/sections
- **Tree Views**: Contact type column for easy identification
- **Search Views**: Filters for drivers, companies, and individuals
- **Menu Structure**: Dedicated menu items for drivers and fleet companies

### Data Management

- **Demo Data**: Sample driver and company contacts included
- **Default Values**: Proper defaulting for new contacts
- **Validation**: License expiry date validation and formatting

## Usage

### Creating Driver Contacts

1. Navigate to **Contacts > Fleet API > Drivers**
2. Click **Create** to add a new driver
3. Fill in the required fields:

   - Name
   - Contact Type (set to Driver)
   - Email and Phone
   - Driver License Information
   - Location coordinates (optional)

### Managing Driver Information

- **License Tracking**: Monitor license expiry dates
- **Location Services**: Track driver locations for fleet management
- **Contact Integration**: Full integration with Odoo's contact system

### Search and Filtering

- **Driver Filter**: Quick access to all driver contacts
- **License Expiry Filter**: Find drivers with expiring licenses
- **Location Filter**: Filter contacts with/without location data

## API Integration

The driver contact system is fully compatible with the ECOSIRE Fleet API:

```json
{
  "name": "John Driver",
  "contact_type": "driver",
  "email": "john.driver@example.com",
  "phone": "+1-555-0100",
  "driver_license_number": "DL123456789",
  "driver_license_class": "class_b",
  "driver_license_expiry": "2025-12-31",
  "partner_latitude": 40.7128,
  "partner_longitude": -74.0060
}
```

## Security and Access Control

- **Role-Based Access**: Standard Odoo security model applies
- **Field-Level Security**: Driver license information protected
- **Data Privacy**: GDPR-compliant data handling

## Testing

Comprehensive test suite included:

- **Unit Tests**: Model field validation and computation
- **Integration Tests**: View rendering and user interaction
- **API Tests**: External system integration validation

## Installation

1. Ensure the module is properly installed in Odoo
2. Update the module list
3. Install/Upgrade the ECOSIRE Fleet API module
4. Access the new driver contact functionality through the menu

## Migration from Existing Contacts

Existing contacts will automatically be categorized as:

- **Companies**: Contacts with `is_company = True`
- **Individuals**: Contacts with `is_company = False`

New contacts can be created with any of the three contact types.

## Best Practices

1. **License Management**: Regularly update driver license information
2. **Location Tracking**: Use GPS coordinates for accurate fleet tracking
3. **Data Consistency**: Maintain consistent contact information across systems
4. **Security**: Protect sensitive driver information with proper access controls

## Support

For technical support and feature requests, contact the ECOSIRE development team.

---

*This feature is part of the ECOSIRE Agent OS ecosystem, designed for 100X development efficiency in Odoo applications.*
