# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class AccountAnalyticAccontType(models.Model):
    _name = 'account.analytic.account.type'
    _rec_name = "analytic_account_type"

    analytic_account_type = fields.Char("Analytic Type")
    parent_analytic_account_type_id = fields.Many2one('account.analytic.account',string="Parent Type", domain="[('is_parent', '=', True)]")


class AccountAnalyticAccont(models.Model):
    _inherit = 'account.analytic.account'

    type = fields.Selection([('n', 'Normal'), ('v', u'View')], default='n', required=True, string=u'Type')
    analytic_account_type_id = fields.Many2one('account.analytic.account.type',string="Type of Analytic Account")
    is_parent = fields.Boolean('Is Parent?')
    # analytic_account_type_parent = fields.Many2one('account.analytic.account',string="Parent Account", domain="[('is_parent', '=', True)]")
    analytic_account_type_parent = fields.Many2one('account.analytic.account',related="analytic_account_type_id.parent_analytic_account_type_id",string="Parent Account")

    @api.multi
    @api.onchange('analytic_account_type_id')
    def _onchange_analytic_account_type_id(self):
        for account in self:
            account.analytic_account_type_parent = account.analytic_account_type_id.parent_analytic_account_type_id