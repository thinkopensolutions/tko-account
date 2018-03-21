# -*- coding: utf-8 -*-

from odoo import models, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError
from odoo.osv import expression

class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"
    _description = "Bank Statement Line"

    ####################################################
    # Show only Posted Account Move Lines
    # in Reconciliation Widget
    ####################################################

    def get_move_lines_for_reconciliation(self, excluded_ids=None, str=False, offset=0, limit=None,
                                          additional_domain=None, overlook_partner=False):
        """ Return account.move.line records which can be used for bank statement reconciliation.

            :param excluded_ids:
            :param str:
            :param offset:
            :param limit:
            :param additional_domain:
            :param overlook_partner:
        """
        if additional_domain is None:
            additional_domain = []
        else:
            additional_domain = expression.normalize_domain(additional_domain)
        additional_domain = expression.AND([additional_domain, [('move_id.state', '=', 'posted')]])

        lines = super(AccountBankStatementLine, self).get_move_lines_for_reconciliation(excluded_ids=excluded_ids, str=str,
                                                                                offset=offset, limit=limit,
                                                                                additional_domain=additional_domain,
                                                                                overlook_partner=overlook_partner)

        # return only lines with invoice in open stage because we have moves in draft stage now
        return lines.filtered(lambda line: line.move_id.invoice_id.state == 'open')

