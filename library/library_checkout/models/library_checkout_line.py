from odoo import api, fields, models, exceptions

class CheckoutLine(models.Model):
    _name = 'library.checkout.line'
    _description = 'Borrow Request Line'

    checkout_id = fields.Many2one('library.checkout', required=True)
    book_id = fields.Many2one('library.book', required=True)
    note = fields.Char("Notes")
    book_cover = fields.Binary(related="book_id.image")