# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.tools.misc import formatLang

class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"


    @api.multi
    def get_move_lines_for_reconciliation_widget(self, excluded_ids=None, str=False, offset=0, limit=None):
        """ Returns move lines for the bank statement reconciliation widget, formatted as a list of dicts
        """
        aml_recs = self.get_move_lines_for_reconciliation(excluded_ids=excluded_ids, str=str, offset=offset, limit=None)
        target_currency = self.currency_id or self.journal_id.currency_id or self.journal_id.company_id.currency_id
        return aml_recs.prepare_move_lines_for_reconciliation_widget(target_currency=target_currency, target_date=self.date)
