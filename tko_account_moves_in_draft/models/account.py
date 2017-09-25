# -*- coding: utf-8 -*-

from odoo import models, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'


    @api.model
    def create(self,vals):
        ctx = dict(self._context)
        ctx.update({'create' : True})
        self = self.with_context(ctx)
        res = super(AccountInvoice, self).create(vals)
        res.action_move_create()
        res.move_id.write({'state' : 'draft'})
        return res

    @api.multi
    def write(self, vals):
        context = self.env.context
        for record in self:
            super(AccountInvoice, record).write(vals)
            if record.state == 'draft' and 'move_id' not in vals.keys() and 'create' not in context.keys() and 'validate' not in context.keys():
                self.env.cr.execute("update account_invoice set move_id = null where id='%s'" %(record.id))
                move = record.move_id
                move.line_ids.unlink()
                move.unlink()
                record.action_move_create()
                record.move_id.write({'state': 'draft', 'date':record.date_invoice})
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
        return to_open_invoices.invoice_validate()