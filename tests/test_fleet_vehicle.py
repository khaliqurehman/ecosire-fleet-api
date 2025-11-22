# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase


class TestFleetVehicle(TransactionCase):
    """Test cases for fleet vehicle functionality in ECOSIRE Fleet API module."""

    def setUp(self):
        super().setUp()
        self.vehicle_model = self.env['fleet.vehicle']
        self.brand_model = self.env['fleet.vehicle.model.brand']
        self.model_model = self.env['fleet.vehicle.model']

    def test_create_vehicle_with_saudi_plate(self):
        """Test creating a vehicle with Saudi plate structure."""
        # Create brand and model first
        brand = self.brand_model.create({'name': 'Toyota'})
        model = self.model_model.create({
            'name': 'Corolla',
            'brand_id': brand.id,
            'model_year': 2022
        })
        
        vehicle_data = {
            'name': 'Toyota Corolla - أصد1280',
            'license_plate': 'أصد1280',
            'plate_type_id': 2,
            'plate_right_letter': 'أ',
            'plate_middle_letter': 'ص',
            'plate_left_letter': 'د',
            'plate_number': '1280',
            'vehicle_type': 'sedan',
            'vin_sn': '1HGCM82633A123456',
            'model_id': model.id,
            'model_year': '2022'
        }
        
        vehicle = self.vehicle_model.create(vehicle_data)
        
        # Verify vehicle was created with Saudi plate structure
        self.assertEqual(vehicle.plate_type_id, 2)
        self.assertEqual(vehicle.plate_right_letter, 'أ')
        self.assertEqual(vehicle.plate_middle_letter, 'ص')
        self.assertEqual(vehicle.plate_left_letter, 'د')
        self.assertEqual(vehicle.plate_number, '1280')
        self.assertEqual(vehicle.vehicle_type, 'sedan')
        self.assertEqual(vehicle.vin_sn, '1HGCM82633A123456')

    def test_formatted_plate_computation(self):
        """Test the formatted plate computation."""
        vehicle = self.vehicle_model.create({
            'name': 'Test Vehicle',
            'plate_right_letter': 'أ',
            'plate_middle_letter': 'ص',
            'plate_left_letter': 'د',
            'plate_number': '1280'
        })
        
        # Test formatted plate computation
        expected_formatted = "أصد 1280"
        self.assertEqual(vehicle.formatted_plate, expected_formatted)

    def test_to_fleet_api_format(self):
        """Test conversion to fleet API format."""
        # Create brand and model
        brand = self.brand_model.create({'name': 'Toyota'})
        model = self.model_model.create({
            'name': 'Corolla',
            'brand_id': brand.id,
            'model_year': 2022
        })
        
        vehicle = self.vehicle_model.create({
            'name': 'Toyota Corolla',
            'plate_type_id': 2,
            'plate_right_letter': 'أ',
            'plate_middle_letter': 'ص',
            'plate_left_letter': 'د',
            'plate_number': '1280',
            'vehicle_type': 'sedan',
            'vin_sn': '1HGCM82633A123456',
            'model_id': model.id,
            'model_year': '2022'
        })
        
        api_data = vehicle.to_fleet_api_format()
        
        # Verify API format
        expected_data = {
            "plateTypeId": 2,
            "vehiclePlate": {
                "rightLetter": "أ",
                "middleLetter": "ص",
                "leftLetter": "د",
                "number": "1280"
            },
            "chassis_number": "1HGCM82633A123456",
            "vehicle_manufacturer": "Toyota",
            "vehicle_model": "Corolla",
            "vehicle_year": "2022",
            "vehicle_type": "sedan"
        }
        
        self.assertEqual(api_data, expected_data)

    def test_update_from_fleet_api(self):
        """Test updating vehicle from fleet API data."""
        vehicle = self.vehicle_model.create({
            'name': 'Test Vehicle'
        })
        
        api_data = {
            "plateTypeId": 2,
            "vehiclePlate": {
                "rightLetter": "ب",
                "middleLetter": "ط",
                "leftLetter": "ن",
                "number": "5678"
            },
            "chassis_number": "1HGCM82633B789012",
            "vehicle_type": "dyna"
        }
        
        vehicle.update_from_fleet_api(api_data)
        
        # Verify updates
        self.assertEqual(vehicle.plate_type_id, 2)
        self.assertEqual(vehicle.plate_right_letter, 'ب')
        self.assertEqual(vehicle.plate_middle_letter, 'ط')
        self.assertEqual(vehicle.plate_left_letter, 'ن')
        self.assertEqual(vehicle.plate_number, '5678')
        self.assertEqual(vehicle.vin_sn, '1HGCM82633B789012')
        self.assertEqual(vehicle.vehicle_type, 'dyna')

    def test_vehicle_type_selection(self):
        """Test vehicle type selection options."""
        vehicle_types = [
            'sedan', 'suv', 'truck', 'van', 'pickup', 
            'dyna', 'bus', 'motorcycle', 'other'
        ]
        
        for vehicle_type in vehicle_types:
            vehicle = self.vehicle_model.create({
                'name': f'Test {vehicle_type}',
                'vehicle_type': vehicle_type
            })
            self.assertEqual(vehicle.vehicle_type, vehicle_type)

    def test_plate_components_validation(self):
        """Test plate component field sizes and validation."""
        vehicle = self.vehicle_model.create({
            'name': 'Test Vehicle',
            'plate_right_letter': 'أ',
            'plate_middle_letter': 'ص', 
            'plate_left_letter': 'د',
            'plate_number': '1234567890'  # Max size test
        })
        
        # Verify all components are stored correctly
        self.assertEqual(vehicle.plate_right_letter, 'أ')
        self.assertEqual(vehicle.plate_middle_letter, 'ص')
        self.assertEqual(vehicle.plate_left_letter, 'د')
        self.assertEqual(vehicle.plate_number, '1234567890')
