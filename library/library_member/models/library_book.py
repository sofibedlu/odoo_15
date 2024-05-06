from odoo import fields, models

class LibraryBook(models.Model):
    _inherit = "library.book"
    is_available = fields.Boolean("Is Available?")
    isbn = fields.Char(help="Use a valid ISBN-13 or ISBN-10.")
    publisher_id = fields.Many2one(index=True)

    def _check_isbn(self):
        self.ensure_one()

        digits = [int(x) for x in self.isbn if x.isdigit()]
        if len(digits) == 10:
            # Check if the length is 10 and only contains digits or 'X' (for the check digit)
            if not isbn or len(isbn) != 10 or not all(char in '0123456789X' for char in isbn):
                return False

            # Remove hyphens or spaces (optional for handling different formats)
            isbn = isbn.replace("-", "").replace(" ", "")

            # Convert the ISBN to a list of integers (excluding 'X')
            isbn_digits = [int(char) for char in isbn[:-1]]

            # Calculate the weighted sum for check digit validation
            weighted_sum = sum(digit * (10 - i) for i, digit in enumerate(isbn_digits))

            # Check digit is the remainder of dividing the weighted sum by 11
            check_digit = weighted_sum % 11

            # Valid ISBN-10 has the check digit as the last digit (considering 'X' as 10) 
            return (check_digit == 10 and isbn[-1] == 'X') or (0 <= check_digit < 10 and check_digit == int(isbn[-1]))
        else:
            return super()._check_isbn()
