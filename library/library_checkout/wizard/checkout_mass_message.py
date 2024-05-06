from odoo import api, fields, models, exceptions
import logging

_logger = logging.getLogger(__name__)

class CheckoutMassMessage(models.TransientModel):
    _name = 'library.checkout.massmessage'
    _description = 'Send Message to Borrowers'
    
    checkout_ids = fields.Many2many('library.checkout', string='Checkouts')
    message_subject = fields.Char()
    message_body = fields.Html()
    
    @api.model
    def default_get(self, field_names):
        defaults_dict = super().default_get(field_names)
        active_ids = self.env.context.get("active_ids")
        if active_ids:
            # Create recordsets from the active_ids
            checkout_ids = self.env['library.checkout'].browse(active_ids)
            defaults_dict["checkout_ids"] = checkout_ids
        return defaults_dict

    def button_send(self):
        self.ensure_one()
        if not self.checkout_ids:
            raise exceptions.UserError("No Checkouts were selected.")
        if not self.message_body:
            raise exceptions.UserError("Please provide a message body.")
        for checkout in self.checkout_ids:
            checkout.message_post(
                body=self.message_body,
                subject=self.message_subject,
                subtype_xmlid='mail.mt_comment')
        
        _logger.info("Message sent to %d checkouts: %s", len(self.checkout_ids), str(self.checkout_ids))
        return True