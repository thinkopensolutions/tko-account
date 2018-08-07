# -*- coding: utf-8 -*-

from odoo import models, api, _, fields
import pytz
from odoo import api, SUPERUSER_ID, tools

class AccountMove(models.Model):
    _inherit = 'account.move'

    # set current date on Account Move and Analytic lines
    @api.depends('state')
    def post(self):
        res = super(AccountMove, self).post()
        tz = pytz.timezone(self.env['res.users'].browse(SUPERUSER_ID).partner_id.tz) or pytz.utc
        current_date = pytz.utc.localize(fields.datetime.now()).astimezone(tz)
        current_date = current_date.strftime(tools.DEFAULT_SERVER_DATE_FORMAT)

        for move in self:
            invoice = self.env['account.invoice'].search([('move_id','=',move.id)])
            if len(invoice) and invoice.type == 'out_invoice':
                move.date = current_date
                for mline in move.line_ids:
                    for line in mline.analytic_line_ids:
                        line.date = current_date
        return res
