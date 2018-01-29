# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO, Open Source Management Solution
#    Copyright (C) 2016 Steigend IT Solutions
#    For more details, check COPYRIGHT and LICENSE files
#
##############################################################################

from odoo import models, fields, api,_


class OpenAnalyticTypeAccount(models.TransientModel):
    """
    For Chart of Accounts
    """
    _name = "open.analytic.type.account"
    _description = "Open Analytic Type Accounts"

    date_from = fields.Date(string='Start Date')
    date_to = fields.Date(string='End Date')
    
    def _build_contexts(self, data):
        result = {}
        result['date_from'] = data['date_from'] or False
        result['date_to'] = data['date_to'] or False
        result['show_parent_account'] = True
        return result

    @api.multi
    def account_chart_open_type_window(self):
        """
        Opens chart of Accounts
        @return: dictionary of Open account chart window on given date(s) and all Entries or posted entries
        """
        self.ensure_one()
        data = self.read([])[0]
        used_context = self._build_contexts(data)
        self  = self.with_context(used_context)
        # if self.env['account.analytic.account.type'].search([('parent_analytic_account_type_id','!=',False)],limit=1):
        if self.env['account.analytic.account'].search([('is_parent','=',False)],limit=1):
            result = self.env.ref('tko_account_analytic_type.open_view_analytic_type_account_tree').read([])[0]
        else:
            result = self.env.ref('tko_account_analytic_type.open_view_analytic_type_account_noparent_tree').read([])[0]
        result_context = eval(result.get('context','{}')) or {}
        used_context.update(result_context)
        result['context'] = str(used_context)
        return result

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: