# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Contact Type Selection - Extended to include Driver
    contact_type = fields.Selection([
        ('individual', 'Individual'),
        ('company', 'Company'),
        ('driver', 'Driver')
    ], string='Contact Type', default='individual', required=True,
        help='Type of contact: Individual, Company, or Driver')

    # Commercial Registration Field
    commercial_registration = fields.Char(
        string='Commercial Registration',
        help='Commercial registration number or identifier for the company/contact'
    )

    # Driver-specific fields
    driver_license_number = fields.Char(
        string='Driver License Number',
        help='Driver license number for driver contacts'
    )
    
    driver_license_expiry = fields.Date(
        string='License Expiry Date',
        help='Expiry date of the driver license'
    )
    
    driver_license_class = fields.Selection([
        ('class_a', 'Class A'),
        ('class_b', 'Class B'),
        ('class_c', 'Class C'),
        ('class_d', 'Class D'),
        ('commercial', 'Commercial'),
        ('motorcycle', 'Motorcycle'),
        ('other', 'Other')
    ], string='License Class', help='Driver license class')
    
    # Iqama/ID Number field - from Studio customization
    x_studio_iqama_number = fields.Char(
        string='ID Number',
        help='Iqama number or ID number for individual/driver identification'
    )
    
    # Additional driver information
    iqama_number = fields.Char(
        string='Iqama Number',
        help='Iqama number for driver identification (legacy field - use x_studio_iqama_number)'
    )
    
    issue_number = fields.Char(
        string='Issue Number',
        help='Issue number for document tracking'
    )
    
    vehicle_assigned_id = fields.Many2one(
        'fleet.vehicle',
        string='Assigned Vehicle',
        help='Vehicle assigned to this driver from the fleet'
    )

    # Location fields (these already exist in base model but we'll make them more visible)
    # partner_latitude and partner_longitude already exist in base model
    # We'll add computed fields for better display
    location_display = fields.Char(
        string='Location Coordinates',
        compute='_compute_location_display',
        help='Display format of latitude and longitude coordinates'
    )

    @api.depends('partner_latitude', 'partner_longitude')
    def _compute_location_display(self):
        """Compute a user-friendly display of location coordinates."""
        for partner in self:
            if partner.partner_latitude and partner.partner_longitude:
                partner.location_display = f"{partner.partner_latitude:.6f}, {partner.partner_longitude:.6f}"
            else:
                partner.location_display = "Not set"

    @api.depends('contact_type')
    def _compute_is_company(self):
        """Override the is_company field to work with our contact_type field."""
        for partner in self:
            if partner.contact_type == 'company':
                partner.is_company = True
            else:
                partner.is_company = False

    @api.depends('is_company')
    def _compute_contact_type(self):
        """Sync contact_type with is_company field for backward compatibility."""
        for partner in self:
            if partner.is_company:
                if partner.contact_type != 'company':
                    partner.contact_type = 'company'
            else:
                if partner.contact_type == 'company':
                    partner.contact_type = 'individual'

    @api.onchange('contact_type')
    def _onchange_contact_type(self):
        """Handle contact type changes."""
        if self.contact_type == 'company':
            self.is_company = True
        else:
            self.is_company = False

    @api.onchange('is_company')
    def _onchange_is_company(self):
        """Handle is_company changes for backward compatibility."""
        if self.is_company:
            self.contact_type = 'company'
        else:
            if self.contact_type == 'company':
                self.contact_type = 'individual'

    def _get_contact_type_display(self):
        """Get display name for contact type."""
        type_mapping = {
            'individual': _('Individual'),
            'company': _('Company'),
            'driver': _('Driver')
        }
        return type_mapping.get(self.contact_type, _('Individual'))

    def action_set_location_from_address(self):
        """Action to set location coordinates from address using geocoding."""
        self.ensure_one()
        if not self.street or not self.city:
            raise UserError(_("Please provide at least street and city to geocode the address."))
        
        # This would typically use a geocoding service
        # For now, we'll just show a message
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Geocoding'),
                'message': _('Geocoding functionality would be implemented here to get coordinates from address.'),
                'type': 'info',
            }
        }