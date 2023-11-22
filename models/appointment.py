from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class ManagementAppointment(models.Model):
    _name = 'management.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Management Appointment'
    _order = 'manager_id'

    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))
    patient_id = fields.Many2one('management.patient', string="Patient", required=True,)
    age = fields.Integer(string='Age', tracking=True)
    manager_id = fields.Many2one('management.manager', string='Manager', required=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], required=True, default='male', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], default='draft', string="Status", tracking=True)
    note = fields.Text(string='Description')
    date_appointment = fields.Date(string="Date")
    date_checkup = fields.Datetime(string="Check Up time")
    oder = fields.Text(string="Oder")
    oder_line_ids = fields.One2many('appointment.prescription.lines', 'appointment_id',
                                            string="Oder Lines")

    def action_confirm(self):
        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('management.appointment') or _('new')
        res = super(ManagementAppointment, self).create(vals)
        return res

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.gender = self.patient_id.gender
        self.age = self.patient_id.age

    def unlink(self):
        for request in self:
            if request.state != 'draft':
                raise UserError(_("You can only delete management in draft state."))
        return super(ManagementAppointment, self).unlink()


class AppointmentPrescriptionLines(models.Model):
    _name = 'appointment.prescription.lines'
    _description = 'Appointment Prescription Lines'

    name = fields.Char(string="Product", required=True)
    qty = fields.Integer(string="Quantity")
    appointment_id = fields.Many2one('management.appointment', string="Appointment")
