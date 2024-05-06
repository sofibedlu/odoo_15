from odoo import fields, models, api

class BookCategory(models.Model):
    _name = "library.book.category"
    _description = "Book Category"

    name = fields.Char(translate=True, required=True)
    # Hierarchy fields
    parent_id = fields.Many2one("library.book.category", string="Parent Category", ondelete="restrict")

    parent_path = fields.Char(index=True)
    # Optional, but nice to have:
    child_ids = fields.One2many(
        "library.book.category",
        "parent_id",
        "Subcategories"
    )

    Highlighted = fields.Reference(
        [("library.book", "Book"), ("res.partner", "Author")],
        "Category Highlight"
    )