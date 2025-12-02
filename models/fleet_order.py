# -*- coding: utf-8 -*-

from odoo import api, fields, models


class EcosireFleetOrder(models.Model):
    _name = "ecosire.fleet.order"
    _description = "ECOSIRE Fleet Order"
    _order = "create_date desc"
    _rec_name = "order_no"

    company_id = fields.Many2one(
        "res.company", required=True, default=lambda self: self.env.company
    )

    order_no = fields.Char(
        string="Order No", required=True, copy=False, index=True, readonly=True, default="/"
    )
    external_order_id = fields.Char(string="External ID", index=True)

    order_type = fields.Selection(
        selection=[("transport", "Transport")], required=True
    )
    cargo_type = fields.Selection(
        selection=[("bulk", "Bulk"), ("container", "Container")], required=True
    )
    customer_id = fields.Many2one(
        "res.partner", string="Customer", required=True
    )
    driver_id = fields.Many2one("hr.employee", string="Driver")
    vehicle_id = fields.Many2one("fleet.vehicle", string="Vehicle")

    delivery_type = fields.Selection(
        selection=[("yard", "Yard"), ("client", "Client")], required=True
    )
    status = fields.Selection(
        selection=[
            ("created", "Created"),
            ("dispatched", "Dispatched"),
            ("started", "Started"),
            ("enroute", "Enroute"),
            ("drop_off_complete", "Drop Off Complete"),
            ("completed", "Completed"),
            ("empty_container_return", "Empty Container Return"),
            ("yard_drop_off", "Yard Drop Off"),
            ("yard_drop_off_complete", "Yard Drop Off Complete"),
            ("yard_pick_up", "Yard Pick Up"),
            ("canceled", "Canceled"),
        ],
        default="created",
        required=True,
        index=True,
    )

    cargo_size = fields.Char()
    container_number = fields.Char()
    container_weight = fields.Float()
    bulk_weight = fields.Float()

    # ---- Pickup Location ----
    pickup_location_lat = fields.Float("Pickup Latitude")
    pickup_location_lng = fields.Float("Pickup Longitude")
    pickup_location_address = fields.Char("Pickup Address")
    pickup_location_city_new = fields.Char("Pickup City")

    # ---- Drop-off Location ----
    drop_off_location_lat = fields.Float("Drop-off Latitude")
    drop_off_location_lng = fields.Float("Drop-off Longitude")
    drop_off_location_address = fields.Char("Drop-off Address")
    drop_off_location_city_new = fields.Char("Drop-off City")

    # ---- Empty Dropoff Location ----
    empty_dropoff_location_lat = fields.Float("Empty Dropoff Latitude")
    empty_dropoff_location_lng = fields.Float("Empty Dropoff Longitude")
    empty_dropoff_location_address = fields.Char("Empty Dropoff Address")
    empty_dropoff_location_city_new = fields.Char("Empty Dropoff City")
    empty_dropoff_location_name = fields.Char("Empty Dropoff Name")
    empty_dropoff_location_phone = fields.Char("Empty Dropoff Phone")

    # ---- Yard Dropoff (if applicable) ----
    yard_dropoff_location_lat = fields.Float("Yard Dropoff Latitude")
    yard_dropoff_location_lng = fields.Float("Yard Dropoff Longitude")
    yard_dropoff_location_address = fields.Char("Yard Dropoff Address")
    yard_dropoff_location_city_new = fields.Char("Yard Dropoff City")

    notes = fields.Text()
    proof_of_delivery = fields.Char()
    proof_of_delivery_sign = fields.Json()
    proof_empty_container_return = fields.Char()

    last_date_container_return = fields.Date()
    items = fields.Json()
    payment = fields.Json()
    expected_delivery_date = fields.Date()
    waybill_id = fields.Integer()
    bayan_trip_id = fields.Integer()
    bill_of_lading_number = fields.Char()
    bayan_number = fields.Char()

    # Payment Terms
    payment_method = fields.Selection(
        selection=[
            ('Cash', 'Cash'),
            ('ATM Card', 'ATM Card'),
            ('Credit Card', 'Credit Card'),
            ('SDAD', 'SDAD'),
            ('Cheque', 'Cheque'),
            ('Bank Transfer', 'Bank Transfer'),
        ],
        string="Payment Method",
    )
    is_tradable = fields.Boolean(string="Tradable")
    fare = fields.Float(string="Fare")
    paid_by_sender = fields.Boolean(string="Paid By Sender")

    # Item lines
    line_ids = fields.One2many("ecosire.fleet.order.line", "order_id", string="Items")

    # Cost lines to be billed
    cost_line_ids = fields.One2many(
        "ecosire.fleet.order.cost.line", "order_id", string="Cost Lines"
    )

    # Related Sales Orders created from this fleet order
    sale_order_ids = fields.One2many(
        "sale.order", "fleet_order_id", string="Sales Orders"
    )

    _sql_constraints = [
        ("ecosire_fleet_order_order_no_uniq", "unique(order_no)", "Order number must be unique."),
    ]

    @api.model
    def create(self, vals):
        if vals.get("order_no", "/") in (False, "/", ""):
            vals["order_no"] = (self.env["ir.sequence"].next_by_code("ecosire.fleet.order.seq") or "/")
        return super().create(vals)

    def action_open_form(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "ecosire.fleet.order",
            "res_id": self.id,
            "view_mode": "form",
            "target": "current",
        }

    def write(self, vals):
        creating_sale_after = False
        if vals.get("status") == "completed":
            creating_sale_after = True
        result = super().write(vals)
        if creating_sale_after:
            for order in self:
                order._create_sale_order_from_cost_lines()
        return result

    def _create_sale_order_from_cost_lines(self):
        self.ensure_one()
        SaleOrder = self.env["sale.order"]
        
        # Create the Sale Order Header ONLY (no order lines here)
        sale = SaleOrder.create(
            {
                "partner_id": self.customer_id.id,
                "company_id": self.company_id.id,
                "origin": self.order_no,
                "fleet_order_id": self.id,
                "external_order_id": self.external_order_id,
            }
        )
        
        # Confirm order (this will result in a confirmed order with $0.00 amount initially)
        # Order lines will be added via API when invoice expenses are added
        sale.action_confirm()
        return sale

    def action_view_sale_orders(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Sales Orders",
            "res_model": "sale.order",
            "view_mode": "list,form",
            "domain": [("fleet_order_id", "=", self.id)],
            "context": {"default_fleet_order_id": self.id, "default_partner_id": self.customer_id.id},
            "target": "current",
        }


class EcosireFleetOrderLine(models.Model):
    _name = "ecosire.fleet.order.line"
    _description = "ECOSIRE Fleet Order Line"

    order_id = fields.Many2one(
        "ecosire.fleet.order", string="Order", required=True, ondelete="cascade"
    )
    unit = fields.Char(string="Unit")
    quantity = fields.Float(string="Quantity")
    price = fields.Float(string="Price")
    good_type = fields.Char(string="Good Type")
    weight = fields.Float(string="Weight")


class EcosireFleetOrderCostLine(models.Model):
    _name = "ecosire.fleet.order.cost.line"
    _description = "ECOSIRE Fleet Order Cost Line"

    order_id = fields.Many2one(
        "ecosire.fleet.order", string="Order", required=True, ondelete="cascade"
    )
    company_id = fields.Many2one(
        related="order_id.company_id", comodel_name="res.company", string="Company", store=True, readonly=True
    )
    currency_id = fields.Many2one(
        related="company_id.currency_id", comodel_name="res.currency", string="Currency", store=True, readonly=True
    )

    product_id = fields.Many2one(
        "product.product",
        string="Product",
        domain="[('sale_ok','=',True)]",
    )
    name = fields.Text(string="Description")
    quantity = fields.Float(string="Quantity", default=1.0)
    price_unit = fields.Float(string="Unit Price")
    tax_ids = fields.Many2many(
        "account.tax",
        string="Taxes",
        domain="[('type_tax_use','=','sale'), ('company_id','=',company_id)]",
    )
    price_subtotal = fields.Monetary(string="Subtotal", compute="_compute_amount", store=False)
    price_total = fields.Monetary(string="Total", compute="_compute_amount", store=False)

    @api.depends("price_unit", "quantity", "tax_ids")
    def _compute_amount(self):
        for line in self:
            taxes_res = line.tax_ids.compute_all(
                line.price_unit,
                currency=line.currency_id,
                quantity=line.quantity,
                product=line.product_id,
                partner=line.order_id.customer_id,
            ) if line.tax_ids else {
                'total_excluded': line.price_unit * line.quantity,
                'total_included': line.price_unit * line.quantity,
            }
            line.price_subtotal = taxes_res.get("total_excluded", 0.0)
            line.price_total = taxes_res.get("total_included", 0.0)

    @api.onchange("product_id")
    def _onchange_product_id_set_defaults(self):
        for line in self:
            product = line.product_id
            if not product:
                continue
            line.name = product.get_product_multiline_description_sale()
            # Quantity default to 1.0 only when not already set
            if not line.quantity:
                line.quantity = 1.0
            # Price from list_price, user may edit later
            line.price_unit = product.list_price
            # Default taxes for sales, filtered by company
            taxes = product.taxes_id.filtered(lambda t: t.company_id == line.company_id and t.type_tax_use == 'sale')
            line.tax_ids = [(6, 0, taxes.ids)]
