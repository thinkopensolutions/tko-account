# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountAnalyticAccont(models.Model):
    _inherit = 'account.analytic.account'

    type = fields.Selection([('n', 'Normal'), ('v', u'View')], default='n', required=True, string=u'Type')
