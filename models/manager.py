from odoo import api, fields, models, _


class ManagementManager(models.Model):
    _name = 'management.manager'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Management Manager'
    _rec_name = 'manager_name'

    manager_name = fields.Char(string='Name', required=True, tracking=True)
    age = fields.Integer(string='Age', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], required=True, default='male', tracking=True)
    note = fields.Text(string='Description')
    image = fields.Binary(string="Patient Image")
    appointment_count = fields.Integer(string='Appointment Count', compute='_compute_appointment_count')
    active = fields.Boolean(string="Active", default=True)

    def copy(self, default=None):
        if default is None:
            default ={}
        if not default.get('manager_name'):
            default['manager_name'] = _("%s (Copy)", self.manager_name)
        default['note'] = "copied Record"
        return super(ManagementManager, self).copy(default)

    def _compute_appointment_count(self):
        for rec in self:
            appointment_count = self.env['management.appointment'].search_count([('manager_id', '=', rec.id)])
            rec.appointment_count = appointment_count
