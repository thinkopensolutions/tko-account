# -*- coding: utf-8 -*-
# © 2017 TKO <http://tko.tko-br.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Analytic Account Type',
    'summary': '',
    'description': 'This module adds type in analytic accounts',
    'author': 'TKO',
    'category': 'Accounting',
    'license': 'AGPL-3',
    'website': 'http://tko.tko-br.com',
    'version': '10.0.0.0.0',
    'application': False,
    'installable': True,
    'auto_install': False,
    'depends': ['analytic',
                'account_analytic_default',
                'account_analytic_plans',
                'br_account',
                'tko_br_account_account_analytic_plans',
                ],
    'external_dependencies': {
        'python': [],
        'bin': [],
    },
    'init_xml': [],
    'update_xml': [],
    'css': [],
    'demo_xml': [],
    'test': [],
    'data': [
        'views/analytic_account_view.xml',
        'views/account_invoice_view.xml',
             ],

}
