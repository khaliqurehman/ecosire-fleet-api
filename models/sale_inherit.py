# -*- coding: utf-8 -*-

from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    fleet_order_id = fields.Many2one(
        "ecosire.fleet.order", string="Fleet Order", index=True
    )

    external_order_id = fields.Char(
        string="External ID",
        index=True,
        help="External order identifier coming from the Fleet Management system.",
    )

    fleet_cost_line_ids = fields.Many2many(
        "ecosire.fleet.order.cost.line",
        string="Fleet Cost Lines",
        compute="_compute_fleet_cost_line_ids",
        readonly=True,
    )

    @api.depends("fleet_order_id")
    def _compute_fleet_cost_line_ids(self):
        for order in self:
            if order.fleet_order_id:
                order.fleet_cost_line_ids = order.fleet_order_id.cost_line_ids
            else:
                order.fleet_cost_line_ids = False

    def _prepare_invoice(self):
        """Propagate the external order ID to the invoice when created from the sale order."""
        self.ensure_one()
        invoice_vals = super()._prepare_invoice()

        external_id = self.external_order_id or (
            self.fleet_order_id and self.fleet_order_id.external_order_id
        )
        if external_id:
            invoice_vals["external_order_id"] = external_id

        return invoice_vals
