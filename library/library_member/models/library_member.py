from odoo import fields, models

class LibraryMember(models.Model):
    _name = "library.member"
    _description = "Library Member"
    _inherits = {"res.partner": "partner_id"}
    _inherit = ["mail.thread", "mail.activity.mixin"]

    card_number = fields.Char("Card Number")
    partner_id = fields.Many2one("res.partner", required=True, ondelete="cascade")
