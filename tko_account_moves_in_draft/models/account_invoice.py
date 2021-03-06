# -*- coding: utf-8 -*-

from odoo import models, api, _, fields
from odoo.exceptions import UserError, RedirectWarning, ValidationError
from odoo import tools
from odoo import SUPERUSER_ID
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT as DTF
import pytz


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def create(self, vals):
        ctx = dict(self._context)
        ctx.update({'create': True})
        self = self.with_context(ctx)
        res = super(AccountInvoice, self).create(vals)
        if len(res.invoice_line_ids):
            res.action_move_create()
            res.move_id.write({'state': 'draft', 'date': res.date_invoice})
        return res

    @api.multi
    def write(self, vals):
        context = self.env.context
        for record in self:
            old_move_id = record.move_id and record.move_id.id or False
            old_move = record.move_id
            super(AccountInvoice, record).write(vals)
            if record.state == 'draft' and 'move_id' not in vals.keys() and 'create' not in context.keys() and 'validate' not in context.keys():
                # constraint won't allow move deletion, so before deleting set move_id null
                self.env.cr.execute("update account_invoice set move_id = null where id='%s'" % (record.id))
                move = record.move_id
                move.line_ids.unlink()
                move.unlink()
                record.action_move_create()
                record.set_move_and_analytic_date()
            elif record.state == 'draft' and not record.move_id and len(record.invoice_line_ids):
                record.action_move_create()
                record.set_move_and_analytic_date()
            # Delete old move in some cases it is left as orphan move in DB
            elif old_move_id and 'move_id' in vals.keys() and vals['move_id'] and vals['move_id'] != old_move_id:
                old_move.line_ids.unlink()
                old_move.unlink()

        return True

    # set accout move to unposted
    # set move date and analytic entries date from invoice
    @api.multi
    def set_move_and_analytic_date(self):
        for record in self:
            record.move_id.write({'state': 'draft', 'date': record.date_invoice})
            for mline in record.move_id.line_ids:
                for line in mline.analytic_line_ids:
                    line.date = record.date_invoice
        return True

    # can't call super if move is already created
    # otherwise will create a posted move but we want only to post the non-posted entry
    # This method is not inherited anywhere so it can be maintained here
    # no other solution I can see to create non-posted entry and use same
    # on confirmation of invoice
    @api.multi
    def action_invoice_open(self):
        # lots of duplicate calls to action_invoice_open, so we remove those already open
        to_open_invoices = self.filtered(lambda inv: inv.state != 'open')
        if to_open_invoices.filtered(lambda inv: inv.state not in ['proforma2', 'draft']):
            raise UserError(_("Invoice must be in draft or Pro-forma state in order to validate it."))
        to_open_invoices.action_date_assign()
        to_open_invoices.action_move_create()
        # if move is already created just post it, otherwise create move on confirmation
        for inv in to_open_invoices:
            if not inv.move_id:
                inv.action_move_create()
            if inv.move_id and inv.type in ('in_invoice', 'in_refund'):
                inv.move_id.post()
            # if inv.move_id and inv.type in ('out_invoice', 'out_refund') and inv.partner_id.post_moves == 'o':
            #     inv.move_id.post()
        return to_open_invoices.invoice_validate()
