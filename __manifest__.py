# -*- coding: utf-8 -*-
{
    'name': 'ECOSIRE Fleet API',
    'version': '18.0.2.0.0',
    'category': 'Fleet',
    'summary': 'ECOSIRE Fleet Management API Integration',
    'description': """
        ECOSIRE Fleet API Module
        ========================
        
        This module provides API integration capabilities for fleet management
        within the ECOSIRE Agent OS ecosystem.
        
        Features:
        - Fleet API integration
        - Data synchronization
        - External system connectivity
    """,
    'author': 'ECOSIRE',
    'website': 'https://ecosire.com',
    'depends': [
        'base',
        'fleet',
        'contacts',
        'hr',
        'hr_contract',
        'hr_skills',
        'sale',
        'account',     
    ],
    'data': [
        # Security files
        'security/ir.model.access.csv',
        # Optional rules
        # 'security/ir_rule.xml',
        
        # Views
        'views/res_partner_views.xml',
        'views/fleet_order_views.xml',
        'views/fleet_vehicle_views.xml',
        'views/sale_order_views.xml', 
        'views/menu_views.xml',
        'views/hr_contract_views.xml',
        'views/hr_employee_views.xml',
        
        # Data files
        'data/partner_data.xml',
        'data/ir_sequence.xml',
    ],
    'demo': [
        # Demo data will be added here
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}

