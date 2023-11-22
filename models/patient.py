from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class ManagementPatient(models.Model):
    _name = 'management.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Management Patient'
    _order = 'id desc'

    @api.model
    def default_get(self, fields):
        res = super(ManagementPatient, self).default_get(fields)
        res['note'] = 'New patient Created'
        return res

    name = fields.Char(string='Name', required=True, tracking=True)
    reference = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))
    age = fields.Integer(string='Age', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], required=True, default='male', tracking=True)
    note = fields.Text(string='Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], default='draft', string="Status", tracking=True)
    responsible_id = fields.Many2one('res.partner', string="Responsible")
    appointment_count = fields.Integer(string='Appointment Count', compute='_compute_appointment_count')
    image = fields.Binary(string="Patient Image")
    appointment_ids = fields.One2many('management.appointment', 'patient_id', string= "Appointments")

    def action_confirm(self):
        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'

    def _compute_appointment_count(self):
        for rec in self:
            appointment_count = self.env['management.appointment'].search_count([('patient_id', '=', rec.id)])
            rec.appointment_count = appointment_count

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New patient'
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('management.patient') or _('new')
        res = super(ManagementPatient, self).create(vals)
        return res

    @api.constrains('name')
    def check_name(self):
        for rec in self:
            patients = self.env['management.patient'].search([('name', '=', rec.name), ('id', '!=', rec.id)])
            if patients:
                raise ValidationError(_("Name %s Already Exists" % rec.name))

    @api.constrains('age')
    def check_age(self):
        for rec in self:
            if rec.age == 0:
                raise ValidationError(_("Age cannot Be Zero"))

    def name_get(self):
        result = []
        for rec in self:
            name = '[' + rec.reference + ']'
            result.append((rec.id, name))
        return result

    def unlink(self):
        for request in self:
            if request.state != 'draft':
                raise UserError(_("You can only delete management in draft state."))
        return super(ManagementPatient, self).unlink()

    # def action_open_appointments(self):
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Appointments',
    #         'res_model': 'management.appointment',
    #         'domain': [('patient_id', '=', self.id)],
    #         'context': {'default_patient_id': self.id},
    #         'view_mode': 'tree, form',
    #         'target': 'current',
    #     }
