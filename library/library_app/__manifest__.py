# -*- coding: utf-8 -*-
{
    'name': "Library Management",
    'summary': "Manage library book catalogue and lending",
    'author': "sofi",
    'license': "AGPL-3",
    'website': "https://www.odoo.com",
    'version': '15.0.1.0.0',
    'depends': ['base'],
    'application': True,
    'category': 'Services/Library',
    'data': [
        'security/library_security.xml',
        'security/ir.model.access.csv',
        'views/book_view.xml',
        'views/library_menu.xml',
        'views/book_list_template.xml',
        'reports/library_book_report.xml',
        'reports/library_publisher_report.xml',
    ],
    'demo': [
        'data/res.partner.csv',
        'data/library.book.csv',
        'data/book_demo.xml',
    ],
}