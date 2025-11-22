# -*- coding: utf-8 -*-

from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    fleet_order_id = fields.Many2one(
        "ecosire.fleet.order", string="Fleet Order", index=True
    )
    
    fleet_cost_line_ids = fields.Many2many(
        'ecosire.fleet.order.cost.line',
        string="Fleet Cost Lines",
        compute='_compute_fleet_cost_line_ids',
        readonly=True
    )
    
    @api.depends('fleet_order_id')
    def _compute_fleet_cost_line_ids(self):
        for order in self:
            if order.fleet_order_id:
                order.fleet_cost_line_ids = order.fleet_order_id.cost_line_ids
            else:
                order.fleet_cost_line_ids = False
