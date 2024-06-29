# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    uom_category_name = fields.Char("UOM Type Name")

    @api.onchange('price_total', 'quantity', 'discount', 'price_unit', 'tax_ids', 'currency_id')
    def recompute_values(self):
        # add this line to help us control the price_total field edit
        self.uom_category_name = self.product_uom_id.category_id.name
        if (self.uom_category_name and
                self.quantity < 1 and self.uom_category_name.lower() == 'weight'):
            raise UserError(_('Sorry, Please first supply a value for Quantity'))

    @api.depends('quantity', 'discount', 'price_unit', 'tax_ids', 'currency_id')
    def _compute_totals(self):
        for line in self:
            line.uom_category_name = line.product_uom_id.category_id.name
            if line.display_type != 'product':
                line.price_total = line.price_subtotal = False
                # Compute 'price_subtotal'
            line_discount_price_unit = line.price_unit * (1 - (line.discount / 100.0))
            subtotal = line.quantity * line_discount_price_unit

            if line.uom_category_name and line.uom_category_name.lower() != 'weight':
                # Compute 'price_total'.
                if line.tax_ids:
                    taxes_res = line.tax_ids.compute_all(
                        line_discount_price_unit,
                        quantity=line.quantity,
                        currency=line.currency_id,
                        product=line.product_id,
                        partner=line.partner_id,
                        is_refund=line.is_refund,
                    )
                    line.price_subtotal = taxes_res['total_excluded']
                    line.price_total = taxes_res['total_included']
                else:
                    line.price_total = line.price_subtotal = subtotal
            else:
                if line.price_total and line.tax_ids:
                    taxes = []
                    for tax in line.tax_ids:
                        taxes.append(tax.amount / 100)
                    line.price_unit = line.price_total / (1 + sum(taxes))/line.quantity
                    line_discount_price_unit = line.price_unit * (1 - (line.discount / 100.0))
                    # subtotal = line.quantity * line_discount_price_unit
                    taxes_res = line.tax_ids.compute_all(
                        line_discount_price_unit,
                        quantity=line.quantity,
                        currency=line.currency_id,
                        product=line.product_id,
                        partner=line.partner_id,
                        is_refund=line.is_refund,
                        )
                    line.price_subtotal = taxes_res['total_excluded']
                    line.move_id.amount_residual = line.price_subtotal

            if line.price_total and not line.tax_ids:
                line.price_unit = line.price_total / line.quantity
                subtotal = line.price_subtotal = line.price_unit * line.quantity


    @api.depends('product_id', 'product_uom_id')
    def _compute_price_unit(self):
        for line in self:
            line.uom_category_name = line.product_uom_id.category_id.name
            if not line.product_id or line.display_type in ('line_section', 'line_note'):
                continue
            if line.move_id.is_sale_document(include_receipts=True):
                document_type = 'sale'
            elif line.move_id.is_purchase_document(include_receipts=True):
                document_type = 'purchase'
            else:
                document_type = 'other'
            if line.uom_category_name and line.uom_category_name.lower() != 'weight':
                line.price_unit = line.product_id._get_tax_included_unit_price(
                    line.move_id.company_id,
                    line.move_id.currency_id,
                    line.move_id.date,
                    document_type,
                    fiscal_position=line.move_id.fiscal_position_id,
                    product_uom=line.product_uom_id,
                )


