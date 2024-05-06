from odoo import fields, models, api, exceptions

class Checkout(models.Model):
    _name = 'library.checkout'
    _description = 'Checkout Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Title")
    fold = fields.Boolean('Folded', default=True)
    member_id = fields.Many2one('library.member', required=True)
    member_image = fields.Binary(related='member_id.image_128')
    user_id = fields.Many2one('res.users', string='Librarian', default=lambda s: s.env.user)
    request_date = fields.Date(default=lambda s: fields.Date.today(),
                                store=True,
                                readonly=False,
                                compute='_compute_request_date_onchange',)
    line_ids = fields.One2many('library.checkout.line', 'checkout_id', string='Borrowed Books')

    kanban_state = fields.Selection(
        [('normal', 'In Progress'), ('blocked', 'Blocked'), ('done', 'Ready for next stage')],
        'Kanban State',
        default='normal'
    )

    @api.model
    def _default_stage_id(self):
        Stage = self.env['library.checkout.stage']
        return Stage.search([('state', '=', 'new')], limit=1).id
    
    @api.model
    def _group_expand_stage_id(self, stages, domain, order):
        return stages.search([], order=order)

    stage_id = fields.Many2one('library.checkout.stage', default=_default_stage_id, group_expand='_group_expand_stage_id')
    state = fields.Selection(related='stage_id.state')

    checkout_date = fields.Date(readonly=True)
    close_date = fields.Date(readonly=True)

    count_checkouts = fields.Integer(compute='_compute_count_checkouts')

    def _compute_count_checkouts(self):
        for checkout in self:
            domain = [
                ('member_id', '=', checkout.member_id.id),
                ('state', 'not in', ['done', 'cancel']),
            ]        
            checkout.count_checkouts = self.search_count(domain)
    
    num_books = fields.Integer(compute="_compute_num_books", store=True)

    @api.depends("line_ids")
    def _compute_num_books(self):
        for record in self:
            record.num_books = len(record.line_ids)

    color = fields.Integer()
    priority = fields.Selection(
        [('0', 'Low'),
         ('1', 'Normal'),
         ('2', 'High')],
        default='2'
    )

    def write(self, vals):
        # reset kanban state to normal when stage_id changes
        if 'stage_id' in vals and 'kanban_state' not in vals:
            vals['kanban_state'] = 'normal'

        # Code before write: 'self' has the old values
        if 'stage_id' in vals:
            new_stage = self.env['library.checkout.stage'].browse(vals['stage_id'])
            if new_stage.state != self.stage_id.state:
                if new_stage.state == 'open':
                    vals['checkout_date'] = fields.Date.today()
                elif new_stage.state == 'done':
                    vals['close_date'] = fields.Date.today()
        return super().write(vals)

    @api.model
    def create(self, vals):
        # Code before create: should use the 'vals' dict
        new_record = super().create(vals)
        # Code after create: can use the 'new_record' created
        if new_record.stage_id.state in ("open", "cancel"):
            raise exceptions.UserError("State not allowed for new checkouts.")
        return new_record
    
    """
    @api.onchange("member_id")
    def _onchange_member_id(self):
        today_date = fields.Date.today()
        if self.request_date != today_date:
            self.request_date = today_date
            return {
                'warning': {
                    'title': "Changed Request Date",
                    'message': "Request date changed to today."
                }
            }
    """
    @api.depends("member_id")
    def _compute_request_date_onchange(self):
        today_date = fields.Date.today()
        if self.request_date != today_date:
            self.request_date = today_date
            return {
                'warning': {
                    'title': "Changed Request Date",
                    'message': "Request date changed to today."
                }
            }
        
    def button_done(self):
        Stage = self.env['library.checkout.stage']
        done_stage = Stage.search([('state', '=', 'done')], limit=1)
        for checkout in self:
            checkout.stage_id = done_stage
        return True