# -*- encoding: utf-8 -*-


from openerp import models, fields, api, _
import datetime
from odoo.exceptions import Warning as UserError
from odoo.exceptions import ValidationError
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as OE_DFORMAT


class ResPartner(models.Model):
    _inherit = 'res.partner'

    unposted_move = fields.Selection([('p',u'padrão'),('c',u'Customizada')], string=u'Rotina Movimento Contábil Customizada Clientes')