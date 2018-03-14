# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)

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
                if company.id != account.company_id.id:
                    # ORM search is not returning result
                    # new_account = self.env['account.account'].search([('code','=',account.code),('company_id','=',company.id)])
                    self.env.cr.execute("select id from account_account where code = '%s' and company_id=%s" % (account.code, company.id))
                    new_account = self.env.cr.fetchall()
                    if not len(new_account):
                        new_account = account.copy(default={'name': account.name, 'code': account.code, 'company_id': company.id})
                        new_accounts.append(new_account.id)
                    else:
                        _logger.info("Not Duplicated: Account %s alredy exists in company %s" %(account.name, account.company_id.name))
        return {
            'name': _('Chart of Accounts'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.account',
            'domain': [('id', 'in', new_accounts)],
        }

