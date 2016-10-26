# -*- coding: utf-8 -*-
# © 2015 Alex Comba - Agile Business Group
# © 2016 Andrea Cometa - Apulia Software
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    'name': "Invoice Report Origin Group",
    'version': '9.0.1.0.0',
    'description': """
This module adds a custom qweb report for account.invoice which gets invoice
lines grouped by their origin.
It inherits sale_layout.report_invoice_layouted template.
""",
    'author': 'Agile Business Group, Apulia Software',
    'website': 'http://www.agilebg.com',
    'license': 'GPL-3',
    'depends': [
        'account',
        'sale_layout',
        'stock_picking_invoice_link',
    ],
    "data": [
        'views/report_invoice.xml',
    ],
    "installable": True
}
