# -*- coding: utf-8 -*-
# © 2015 Alex Comba - Agile Business Group
# © 2016 Andrea Cometa - Apulia Software
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from itertools import groupby
from openerp import models, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def grouped_lines_by_origin(self, invoice_id):
        """
        Returns invoice lines from a specified invoice grouped by origin

        :Parameters:
            -'invoice_id' (int): specify the concerned invoice.
        """
        all_lines = self.browse(invoice_id).invoice_line_ids
        lines_no_origin = all_lines.filtered(lambda r: not r.origin)
        lines = all_lines - lines_no_origin
        sortkey = lambda x: x.origin if x.origin else ''

        grouped_lines = []
        lines = sorted(lines, key=sortkey)
        for key, valuesiter in groupby(lines, sortkey):
            group = {}
            group['origin'] = key
            group['lines'] = list(v for v in valuesiter)
            grouped_lines.append(group)

        # put lines with no origin at the end
        if lines_no_origin:
            group_no_origin = {
                'origin': '',
                'lines': [line for line in lines_no_origin]}
            grouped_lines.append(group_no_origin)
        return grouped_lines

