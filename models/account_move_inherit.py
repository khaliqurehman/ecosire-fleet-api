# -*- coding: utf-8 -*-

import logging

import requests

from odoo import fields, models


_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    external_order_id = fields.Char(
        string="External ID",
        index=True,
        help="External order identifier coming from the Fleet Management or Sales system.",
    )

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------
    def _ecosire_get_upload_endpoint(self):
        """Return the full upload endpoint URL, configurable via system parameter.

        System parameter: ``ecosire_fleet_api.upload_base_url``, default ``http://app:8001``.
        """
        self.ensure_one()
        base_url = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("ecosire_fleet_api.upload_base_url", default="http://app:8001")
        )
        base_url = (base_url or "").rstrip("/")
        return f"{base_url}/api/v1/orders/upload-file"

    def _ecosire_render_invoice_pdf(self):
        """Render and return the PDF bytes for this invoice.

        Uses the standard account invoice report.
        """
        self.ensure_one()
        # Use the generic report service with the new signature that expects the
        # report reference (xmlid or report_name) separately from the record ids.
        # For customer invoices we use the standard account invoice report.
        report_service = self.env["ir.actions.report"]
        pdf_content, _ = report_service._render_qweb_pdf(
            "account.account_invoices", self.ids
        )
        return pdf_content

    def _ecosire_upload_invoice_pdf(self):
        """Upload this invoice's PDF to the external API.

        Sends multipart/form-data with:
        - order_id: invoice.external_order_id
        - file: invoice PDF
        """
        self.ensure_one()

        if not self.external_order_id:
            _logger.info(
                "Skip upload of invoice %s: no external_order_id set.", self.name
            )
            return

        # Only handle customer invoices
        if self.move_type != "out_invoice":
            _logger.debug(
                "Skip upload of move %s: move_type %s is not 'out_invoice'.",
                self.name,
                self.move_type,
            )
            return

        try:
            pdf_content = self._ecosire_render_invoice_pdf()
        except Exception:
            _logger.exception(
                "Failed to render PDF for invoice %s; skipping external upload.",
                self.name,
            )
            return

        url = self._ecosire_get_upload_endpoint()

        data = {
            "order_id": self.external_order_id,
        }
        files = {
            "file": (
                f"invoice_{self.name or self.id}.pdf",
                pdf_content,
                "application/pdf",
            )
        }

        try:
            response = requests.post(url, data=data, files=files, timeout=20)
            if response.ok:
                _logger.info(
                    "Successfully uploaded invoice PDF for %s to %s (status %s).",
                    self.name,
                    url,
                    response.status_code,
                )
            else:
                _logger.warning(
                    "Upload of invoice PDF for %s to %s failed with status %s: %s",
                    self.name,
                    url,
                    response.status_code,
                    response.text,
                )
        except Exception:
            # Do not block posting; just log the error.
            _logger.exception(
                "Error while uploading invoice PDF for %s to external service at %s.",
                self.name,
                url,
            )

    # -------------------------------------------------------------------------
    # Overrides
    # -------------------------------------------------------------------------
    def action_post(self):
        """After posting, upload PDFs for relevant invoices to the external API."""
        res = super().action_post()

        for move in self:
            # Only attempt upload for customer invoices with external_order_id set.
            if move.move_type == "out_invoice" and move.external_order_id:
                move._ecosire_upload_invoice_pdf()

        return res

