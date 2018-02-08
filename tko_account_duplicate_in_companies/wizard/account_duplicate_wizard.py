# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class DuplicateAccounts(models.TransientModel):
    _name = 'duplicate.accounts'

    company_ids = fields.Many2many('res.company','Company')

    @api.model
    def default_get(self, field_list):
        res = super(DuplicateAccounts, self).default_get(field_list)
        res.update({
            'company_id': [(6, 0, self.env['res.company'].sudo().search([]).ids )],
        })
        return res

    @api.one
    def duplicate_accounts(self):
        self = self.sudo()
        active_ids = self._context.get('active_ids',[])
        accounts = self.env['account.account'].sudo().browse('active_ids')
        for company in self.company_ids:
            accounts.copy(default={'company_id' : company.id})
        return True
