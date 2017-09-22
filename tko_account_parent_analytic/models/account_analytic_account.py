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

class AccountAnalyticAccont(models.Model):
    _inherit = 'account.analytic.account'

    account_type = fields.Selection([('n', 'Normal'), ('v', u'View')], default='n', required=True, string=u'Type')


class account_analytic_account(models.Model):
    _name = "account.analytic.account"
    _inherit = "account.analytic.account"

    parent_id = fields.Many2one('account.analytic.account', 'Parent Account', ondelete="set null")
    parent_hierarchy = fields.Many2one('account.analytic.account', 'Parent Hierarchy', ondelete="set null")
    child_ids = fields.One2many('account.analytic.account', 'parent_hierarchy', 'Child Accounts')
    child_complete_ids = fields.Many2many('account.analytic.account','analytic_account_rel', 'analytic_id','analytic_id_col',compute='_child_compute',
                                          string="Account Hierarchy")
    parent_left = fields.Integer('Left Parent', index=1)
    parent_right = fields.Integer('Right Parent', index=1)

    _parent_name = "parent_hierarchy"
    _parent_store = True
    _parent_order = 'code, name'
    _order = 'parent_left'


    @api.one
    def _child_compute(self):
        self.child_complete_ids = [(6, 0, [child.id for child in self.child_ids])]

    @api.multi
    def name_get(self):
        def get_names(cat):
            """ Return the list [parent.name, parent.parent_id.name, ...] """
            res = []
            while cat:
                res.append(cat.name)
                cat = cat.parent_hierarchy
            return res
        return [(cat.id, " / ".join(reversed(get_names(cat)))) for cat in self]


    @api.multi
    def read(self, fields=None, load='_classic_read'):
        result = super(account_analytic_account, self).read(fields, load='_classic_read')
        for rec in result:
            if rec.get('parent_hierarchy'):
                rec_res = self.browse(rec.get('parent_hierarchy')[0])
                result[0].update({'parent_hierarchy': (rec.get('parent_hierarchy')[0], rec_res.name)})
        return result
