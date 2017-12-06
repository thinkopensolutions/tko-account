# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
import datetime
import logging
import time

from odoo import models, fields, api, _
import odoo.tools
from odoo.tools.translate import _
from odoo.exceptions import UserError, ValidationError

import odoo.addons.decimal_precision as dp


class account_analytic_account(models.Model):
    _name = "account.analytic.account"
    _inherit = "account.analytic.account"

    parent_id = fields.Many2one('account.analytic.account', 'Parent Account', ondelete="set null")
    child_ids = fields.One2many('account.analytic.account', 'parent_id', 'Child Accounts')
    child_complete_ids = fields.Many2many('account.analytic.account','analytic_account_rel', 'analytic_id','analytic_id_col',compute='_child_compute',
                                          string="Account Hierarchy")

    balance = fields.Monetary(compute='_compute_debit_credit_balance', string='Balance')
    debit = fields.Monetary(compute='_compute_debit_credit_balance', string='Debit')
    credit = fields.Monetary(compute='_compute_debit_credit_balance', string='Credit')
    parent_left = fields.Integer('Left Parent', index=1)
    parent_right = fields.Integer('Right Parent', index=1)

    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = 'code, name'
    _order = 'parent_left'

    @api.model
    def _move_domain_get(self, domain=None):
        domain = domain and safe_eval(str(domain)) or []
        if self._context.get('from_date', False):
            domain.append(('date', '>=', self._context['from_date']))
        if self._context.get('to_date', False):
            domain.append(('date', '<=', self._context['to_date']))
        return domain


    @api.multi
    def _compute_debit_credit_balance(self):
        analytic_line_obj = self.env['account.analytic.line']
        default_domain = self._move_domain_get()
        for account in self:
            sub_accounts = self.with_context({'show_parent_account': True}).search([('id', 'child_of', [account.id])])
            credit = 0.0
            debit = 0.0
            search_domain = default_domain[:]
            search_domain.insert(0, ('account_id', 'in', sub_accounts.ids))
            for aal in analytic_line_obj.search(search_domain):
                if aal.amount < 0.0:
                    debit += aal.amount
                else:
                    credit += aal.amount
            account.balance = credit - debit
            account.credit = credit
            account.debit = abs(debit)

    @api.one
    def _child_compute(self):
        self.child_complete_ids = [(6, 0, [child.id for child in self.child_ids])]
