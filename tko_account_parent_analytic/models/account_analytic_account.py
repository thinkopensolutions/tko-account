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
    parent_left = fields.Integer('Left Parent', index=1)
    parent_right = fields.Integer('Right Parent', index=1)

    _parent_name = "parent_id"
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
                cat = cat.parent_id
            return res
        return [(cat.id, " / ".join(reversed(get_names(cat)))) for cat in self]

