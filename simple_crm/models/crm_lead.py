from odoo import api, fields, models, _
from odoo.exceptions import UserError


class CrmLead(models.Model):
    _inherit = 'crm.lead'
    contact_status = fields.Selection([
        ("مغلق", "مغلق"),
        ("لم يتم الرد", "لم يتم الرد"),
        ("طلب التاجيل", "طلب التاجيل"),
    ], string="Contact Status")

    l_status = fields.Selection([
        ("مغلق", "مغلق"),
        ("لم يتم الرد", "لم يتم الرد"),
        ("طلب التاجيل", "طلب التاجيل")
    ])

    donation_type = fields.Selection([
        ("Cash", "Cash"),
        ("Cheque", "Cheque"),
        ("In-Kind", "In-Kind"),
        ("on-Site", "on-Site"),
    ])
    division = fields.Selection([
        ('صدقة', 'صدقة'),
        ('صدقة جارية', 'صدقة جارية'),
        ('زكاة', 'زكاة')
    ], string=' division')

    sub_division = fields.Selection([
        ('شركات', 'شركات'),
        ('بنوك', 'بنوك'),
        ('جامعات', 'جامعات'),
        ('مدارس', 'مدارس'),
        ('نوادي', 'نوادي'),
        ('فنادق', 'فنادق'),
        ('مؤسسات', 'مؤسسات'),
        ('متطوعين', 'متطوعين'),
        ('افراد', 'افراد'), ], string=' sub division')

    cheque_no = fields.Char()
    receipt_book_no = fields.Char()
    receipt_book = fields.Char()
    bank_name = fields.Char()
    cheque_date = fields.Date()
    cheque_due_date = fields.Date()
    cheque_amount = fields.Float("cheque amount")
    cash_amount = fields.Float("Cash Amount")
    total_donation = fields.Float(compute='_total_amount', store=True)
    in_kind_donation = fields.Many2one('in.kind.donation', ondelete='set null')
    in_kind_donation_value = fields.Float("inkind Donation value")
    address_type = fields.Selection(
        [('contact', 'Contact'),
         ('invoice', 'Invoice Address'),
         ('delivery', 'Delivery Address'),
         ('other', 'Other Address'),
         ("private", "Private Address"),
         ], string='Address Type',
        default='contact',
        help="Invoice & Delivery addresses are used in sales orders. Private addresses are only visible by authorized users.")

    currency_id = fields.Many2one('res.currency', string='Account Currency',
                                  help="Forces all moves for this account to have this account currency.",
                                  tracking=True)
    diffrence_expected = fields.Float(string='diffrent  expection', compute='_diffrenc_count')

    cancel_reason = fields.Text("cancel Reason")

    d_electricty = fields.Float(string='كهرباء')
    d_celling = fields.Float(string='اسقف')
    d_drainage = fields.Float(string='صرف صحي')
    d_Blankets = fields.Float(string='بطاطين')
    d_food = fields.Float(string='اطعام')
    d_marriage = fields.Float(string='تزويج عرائس')
    d_water = fields.Float(string='وصلات مياه')

    d_Orphan = fields.Float(string='كفالات أيتام')
    d_redemption = fields.Float(string='كفارة يمين')
    d_Shrouds = fields.Float(string='أكفان')
    d_Gaza = fields.Float(string='غزة')
    d_a = fields.Float(string='زهايمر')
    d_b = fields.Float(string='المستشفى أجهزة طبيه ')
    d_c = fields.Float(string='أطراف صناعيه')
    d_d = fields.Float(string='صكوك')


    @api.depends('cheque_amount', 'cash_amount', 'in_kind_donation_value')
    def _total_amount(self):

        for record in self:
            record.total_donation = record.cheque_amount + record.cash_amount + record.in_kind_donation_value

    @api.depends('stage_id')
    def _diffrenc_count(self):
        for record in self:
            record.diffrence_expected = record.total_donation - record.expected_donation

    @api.onchange('stage_id')
    def _check_stage(self):
        cancel_id = self.env['crm.stage'].search([('name', '=', 'Cancelled')])
        if cancel_id and self.stage_id.id == cancel_id.id:
            if not self.cancel_reason:
                raise UserError(_("please add cancel reason first"))

        # if not self.l_status :
        #     raise UserError(_("please set user status before change state"))

    # def write(self, vals):
    #
    #     if vals.get('stage_id', '') and vals.get('stage_id', '') != 1:
    #         print(self.l_status,"user status======",vals)
    #         if not self.l_status :
    #             raise UserError(_("please set user status before change state"))
    #
    #
    #
    #     if vals.get('stage_id',None) and vals.get('stage_id',None) ==4:
    #         if not self.cancel_reason :
    #             raise   UserError(_("please add cancel reason first"))
    #
    #
    #     return super().write(vals)
