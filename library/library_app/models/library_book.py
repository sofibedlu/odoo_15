from odoo import models, fields, api
from odoo.exceptions import ValidationError

"""
library book module
"""

class Book(models.Model):
    _name = "library.book"
    _description = "Book"
    # String fields:
    name = fields.Char("Title")
    isbn = fields.Char("ISBN")
    book_type = fields.Selection(
        [("paper","Paperback"),
        ("hard","Hardcover"),
        ("electronic","Electronic"),
        ("other", "Other")],
        "Type")
    notes = fields.Text("Internal Notes")
    descr = fields.Html("Description")
    # Numeric fields:
    copies = fields.Integer(default=1)
    avg_rating = fields.Float("Average Rating", (3, 2))
    price = fields.Monetary("Price", "currency_id")
    # price helper
    currency_id = fields.Many2one("res.currency")
    # Date and time fields:
    date_published = fields.Date()
    last_borrow_date = fields.Datetime(
        "Last Borrowed On",
        default=lambda self: fields.Datetime.now())
    # Other fields:
    active = fields.Boolean("Active?", default=True)
    image = fields.Binary("Cover")
    # Relational Fields
    publisher_id = fields.Many2one(
        "res.partner", string="Publisher")
    author_ids = fields.Many2many(
        "res.partner", string="Authors")
  
    publisher_country_id = fields.Many2one(
        "res.country", string="Publisher Country",
        compute="_compute_publisher_country",
    )

    @api.depends("publisher_id.country_id")
    def _compute_publisher_country(self):
        for book in self:
            book.publisher_country_id = book.publisher_id.country_id


    # Define SQL constraints
    _sql_constraints = [
        ("library_book_name_date_uq",
         "UNIQUE (name, date_published)",
         "Title and publication date must be unique."),
        ("library_book_check_date",
         "CHECK (date_published <= current_date)",
         "Publication date must not be in the future.")
    ]
    
    # Python model constraints
    @api.constrains("isbn")
    def _check_isbn_validity(self):
        for book in self:
            if book.isbn and not book._check_isbn():
                raise ValidationError('%s is an invalid ISBN' % book.isbn)

    def _check_isbn(self):
        """
        This function checks the validity of an ISBN-13 code.

        Args:
            isbn: A string containing the ISBN-13 code.

        Returns:
            True if the ISBN-13 code is valid, False otherwise.
        """
        self.ensure_one()

        # Check if the length is 13 and only contains digits or 'X' (for the check digit)
        if not self.isbn or len(self.isbn) != 13 or not all(char in '0123456789X' for char in self.isbn):
            return False

        # Convert the ISBN to a list of integers (excluding hyphens)
        isbn_digits = [int(char) if char != 'X' else 10 for char in self.isbn if char.isdigit()]

        # Calculate the weighted sum for check digit validation
        weighted_sum = sum(digit * (3 if i % 2 else 1) for i, digit in enumerate(isbn_digits[:-1]))

        # Check digit is the remainder of dividing the weighted sum by 10
        check_digit = (10 - weighted_sum % 10) % 10

        # Valid ISBN-13 has the check digit matching the last digit (considering 'X' as 10)
        return check_digit == isbn_digits[-1]
    
    def button_check_isbn(self):
        for book in self:
            if not book.isbn:
                raise ValidationError('Please provide an ISBN for {}'.format(book.name))
            if book.isbn and not book._check_isbn():
                raise ValidationError('%s is an invalid ISBN' % book.isbn)
        return True
