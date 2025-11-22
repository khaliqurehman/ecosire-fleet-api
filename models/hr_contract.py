# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HrContract(models.Model):
    _inherit = 'hr.contract'

    # Other Allowances field from Studio customization
    x_studio_other_allowances = fields.Char(
        string='Other Allowances',
        help='Additional allowances or benefits provided in the contract'
    )