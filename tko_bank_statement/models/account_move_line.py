# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.tools.misc import formatLang
    
class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.multi
    def prepare_move_lines_for_reconciliation_widget(self, target_currency=False, target_date=False):
        """ Returns move lines formatted for the manual/bank reconciliation widget

            :param target_currency: currency (browse_record or ID) you want the move line debit/credit converted into
            :param target_date: date to use for the monetary conversion
        """
        context = dict(self._context or {})
        rets = super(AccountMoveLine, self).prepare_move_lines_for_reconciliation_widget(target_currency, target_date)
        ret_data = []
        for ret in rets:
            line = self.env['account.move.line'].browse(ret['id'])
            # inv_id = self.env['account.invoice'].search([('number','=',ret['ref'])])
            inv_id = self.env['account.invoice'].search([('move_id','=',line.move_id.id)])
            if inv_id:
                if inv_id.state == 'open':
                    ret_data.append(ret)
            # elif line.move_id.state != 'draft' and ret['already_paid'] == 'False':
            #     ret_data.append(ret)
        return ret_data
