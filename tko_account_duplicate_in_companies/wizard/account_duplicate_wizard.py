# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class DuplicateAccounts(models.TransientModel):
    _name = 'duplicate.accounts'

    company_ids = fields.Many2many('res.company', 'company_duplicate_accounts_rel','duplicate_account_id','company_id','Company')

    @api.model
    def default_get(self, field_list):
        res = super(DuplicateAccounts, self).default_get(field_list)
        res.update({
            'company_ids': [(6, 0, self.env['res.company'].sudo().search([]).ids )],
        })
        return res

    @api.multi
    def duplicate_accounts(self):
        self = self.sudo()
        active_ids = self._context.get('active_ids',[])
        accounts = self.env['account.account'].sudo().browse(active_ids)
        new_accounts = []
        for company in self.company_ids:
            for account in accounts:
                new_account = account.copy(default={'name': account.name, 'company_id': company.id})
                new_accounts.append(new_account.id)
        return {
            'name': _('Chart of Accounts'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.account',
            'domain': [('id', 'in', new_accounts)],
        }

