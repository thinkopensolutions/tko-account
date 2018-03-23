# -*- encoding: utf-8 -*-


from openerp import models, fields, api, _
import datetime
from odoo.exceptions import Warning as UserError
from odoo.exceptions import ValidationError
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as OE_DFORMAT


class ResPartner(models.Model):
    _inherit = 'res.partner'

    post_moves = fields.Selection([('o',u'Fatura Aberta'),('p',u'Fatura Paga')], string=u'Lançar movimento em')