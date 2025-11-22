# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    # Saudi Plate Structure Fields
    plate_type_id = fields.Integer(
        string='Plate Type ID',
        help='Plate type identifier for Saudi license plates'
    )
    
    plate_right_letter = fields.Char(
        string='Right Letter',
        size=1,
        help='Right letter of the Saudi license plate'
    )
    
    plate_middle_letter = fields.Char(
        string='Middle Letter', 
        size=1,
        help='Middle letter of the Saudi license plate'
    )
    
    plate_left_letter = fields.Char(
        string='Left Letter',
        size=1, 
        help='Left letter of the Saudi license plate'
    )
    
    plate_number = fields.Char(
        string='Plate Number',
        size=10,
        help='Numeric part of the Saudi license plate'
    )
    
    # Vehicle Category Field (different from model's vehicle_type)
    vehicle_category = fields.Selection([
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('truck', 'Truck'),
        ('van', 'Van'),
        ('pickup', 'Pickup'),
        ('dyna', 'Dyna'),
        ('bus', 'Bus'),
        ('motorcycle', 'Motorcycle'),
        ('other', 'Other')
    ], string='Vehicle Category', help='Category/type of the vehicle for fleet management')
    
    # Computed field for formatted plate display
    formatted_plate = fields.Char(
        string='Formatted Plate',
        compute='_compute_formatted_plate',
        help='Formatted display of the complete license plate'
    )

    # Istimara (Vehicle Registration) Fields
    x_studio_istimara_serial_number = fields.Char(
        string='Istimara Serial Number',
        help='Vehicle registration serial number'
    )
    
    x_studio_istimara_start_date_1 = fields.Date(
        string='Istimara Start Date',
        help='Vehicle registration start date'
    )
    
    x_studio_istimara_expiry_date = fields.Date(
        string='Istimara Expiry Date',
        help='Vehicle registration expiry date',
        tracking=True
    )

    # Insurance Fields
    x_studio_insurance_type = fields.Char(
        string='Insurance Type',
        help='Type of vehicle insurance (e.g., Comprehensive, Third Party)'
    )
    
    x_studio_insurance_number = fields.Char(
        string='Insurance Number',
        help='Vehicle insurance policy number'
    )
    
    x_studio_insurance_start_date_1 = fields.Date(
        string='Insurance Start Date',
        help='Insurance policy start date'
    )
    
    x_studio_insurance_expiry_date = fields.Date(
        string='Insurance Expiry Date',
        help='Insurance policy expiry date',
        tracking=True
    )

    @api.depends('plate_right_letter', 'plate_middle_letter', 'plate_left_letter', 'plate_number')
    def _compute_formatted_plate(self):
        """Compute formatted plate display from individual components."""
        for vehicle in self:
            if all([vehicle.plate_right_letter, vehicle.plate_middle_letter, 
                   vehicle.plate_left_letter, vehicle.plate_number]):
                vehicle.formatted_plate = f"{vehicle.plate_right_letter} {vehicle.plate_middle_letter} {vehicle.plate_left_letter} {vehicle.plate_number}"
            else:
                vehicle.formatted_plate = vehicle.license_plate or ""

    def to_fleet_api_format(self):
        """Convert Odoo vehicle data to fleet API JSON format."""
        return {
            "plateTypeId": self.plate_type_id or 2,  # Default Saudi plate type
            "vehiclePlate": {
                "rightLetter": self.plate_right_letter or "",
                "middleLetter": self.plate_middle_letter or "",
                "leftLetter": self.plate_left_letter or "",
                "number": self.plate_number or ""
            },
            "chassis_number": self.vin_sn or "",
            "vehicle_manufacturer": self.brand_id.name if self.brand_id else "",
            "vehicle_model": self.model_id.name if self.model_id else "",
            "vehicle_year": self.model_year or 2024,
            "vehicle_type": self.vehicle_category or "sedan",
            # Additional document information
            "istimara": {
                "serial_number": self.x_studio_istimara_serial_number or "",
                "start_date": self.x_studio_istimara_start_date_1.isoformat() if self.x_studio_istimara_start_date_1 else "",
                "expiry_date": self.x_studio_istimara_expiry_date.isoformat() if self.x_studio_istimara_expiry_date else ""
            },
            "insurance": {
                "type": self.x_studio_insurance_type or "",
                "number": self.x_studio_insurance_number or "",
                "start_date": self.x_studio_insurance_start_date_1.isoformat() if self.x_studio_insurance_start_date_1 else "",
                "expiry_date": self.x_studio_insurance_expiry_date.isoformat() if self.x_studio_insurance_expiry_date else ""
            }
        }

    def update_from_fleet_api(self, api_data):
        """Update vehicle fields from fleet API JSON data."""
        if 'plateTypeId' in api_data:
            self.plate_type_id = api_data['plateTypeId']
        
        if 'vehiclePlate' in api_data:
            plate_data = api_data['vehiclePlate']
            self.plate_right_letter = plate_data.get('rightLetter', '')
            self.plate_middle_letter = plate_data.get('middleLetter', '')
            self.plate_left_letter = plate_data.get('leftLetter', '')
            self.plate_number = plate_data.get('number', '')
        
        if 'vehicle_type' in api_data:
            self.vehicle_category = api_data['vehicle_type']
        
        if 'chassis_number' in api_data:
            self.vin_sn = api_data['chassis_number']
        
        # Update Istimara information
        if 'istimara' in api_data:
            istimara_data = api_data['istimara']
            self.x_studio_istimara_serial_number = istimara_data.get('serial_number', '')
            if istimara_data.get('start_date'):
                self.x_studio_istimara_start_date_1 = istimara_data['start_date']
            if istimara_data.get('expiry_date'):
                self.x_studio_istimara_expiry_date = istimara_data['expiry_date']
        
        # Update Insurance information
        if 'insurance' in api_data:
            insurance_data = api_data['insurance']
            self.x_studio_insurance_type = insurance_data.get('type', '')
            self.x_studio_insurance_number = insurance_data.get('number', '')
            if insurance_data.get('start_date'):
                self.x_studio_insurance_start_date_1 = insurance_data['start_date']
            if insurance_data.get('expiry_date'):
                self.x_studio_insurance_expiry_date = insurance_data['expiry_date']