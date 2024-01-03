from odoo import api, fields, models, _, exceptions

from pprint import pprint


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # constrain phone number
    _sql_constraints = [
        ('phone_uniq', 'UNIQUE(phone)',
         'The phone Number  must be unique for each Contact!')
    ]

    # _inherit = ['res.partner','mail.thread']
    user_id = fields.Many2one('res.users', string='Salesperson',
                              help='The internal user in charge of this contact &.', default=lambda self: self.env.user)

    # main_division = fields.Many2one('spectrum_crm.spectrum_crm', ondelete='cascade')
    job_category = fields.Many2one('job.category')
    division = fields.Many2one('division.crm' ,string="division")
    sub_program = fields.Selection([
        ('شركات', 'شركات'),
        ('بنوك', 'بنوك'),
        ('جامعات', 'جامعات'),
        ('مدارس', 'مدارس'),
        ('نوادي', 'نوادي'),
        ('فنادق', 'فنادق'),
        ('مؤسسات', 'مؤسسات'),
        ('متطوعين', 'متطوعين'),
        ('افراد', 'افراد'),
    ],"sub_program")
    program = fields.Selection([
        ('شركات', 'شركات'),
        ('بنوك', 'بنوك'),
        ('جامعات', 'جامعات'),
        ('مدارس', 'مدارس'),
        ('نوادي', 'نوادي'),
        ('فنادق', 'فنادق'),
        ('مؤسسات', 'مؤسسات'),
        ('متطوعين', 'متطوعين'),
        ('افراد', 'افراد'),
    ],"program")
    sub_division = fields.Many2one('sub_division.crm',string='sub_division')
    followup_method = fields.Many2one('followup.method')
    religion = fields.Selection([
        ("مسلم", "مسلم"),
        ("مسيحى", "مسيحى"),
    ])
    sale_person_seq = fields.Char('contact sequnce')


    gender = fields.Selection([
        ("ذكر", "ذكر"),
        ("انثى", "انثى"),
    ])

    birthday = fields.Date('Date of Birth', required=False)
    phone2 = fields.Char(unique=True)
    expected_donation = fields.Float(required=False)
    international_phone = fields.Char()
    mobile2 = fields.Char()
    mobile3 = fields.Char()
    full_address = fields.Text(string='Full Address', compute='_compute_full_address')
    company_name = fields.Char()
    company_type_crm = fields.Selection([
        (" ", " "),
        ("Private", "Private"),
        ("Public", "Public"),
    ], string='company type')
    # program = fields.Selection([
    #     (" ", " "),
    #     ("صدقة", "صدقة"),
    #     ("كفالة مريض", "كفالة مريض"),
    #     ("كفالة علاج", "كفالة علاج"),
    #     ("تغذيه علاجية", "تغذيه علاجية"),
    #     ("عشور", "عشور"),
    # ], string=' program')



    company_size = fields.Selection([
        (" ", " "),
        ("Small", "Small"),
        ("Medium", "Medium"),
        ("Big", "Big"),
    ])
    user_status = fields.Selection([
        ("تم تحديث البيانات", "تم تحديث البيانات"),
        ("غير موجود بالخدمة", "غير موجود بالخدمة"),
        ("الرقم خطأ", "الرقم خطأ"),
        ("رفض التواصل", "رفض التواصل"),
        ("متفاعل", "متفاعل"),
        ("مغلق", "مغلق"),
        ("لم يتم الرد", "لم يتم الرد"),
        ("طلب التاجيل", "طلب التاجيل"),
    ], required=False, string="Status")

    segmentation = fields.Selection([
        ('0 : 1000', '0 : 1000'),
        ('1000 : 10000', '1000 : 10000'),
        ('10000 : 20000', '10000 : 20000'),
        ('20000 : 50000', '20000 : 50000'),
        ('50000 : 100000', '50000 : 100000'),
        ('100000 : 500000', '100000 : 500000'),
        ('500000 : ~ ', '500000 : ~'),

    ])

    def update_seq(self):
        contact_seq = self.env['ir.sequence'].search([('code', '=', self.env.user.email)])
        if len(contact_seq) < 1:
            seq = self.env['ir.sequence'].sudo().create({
                'code': self.env.user.email,
                'name': self.env.user.name,
                'implementation': 'no_gap',
                'prefix': self.env.user.name + '-',
                'suffix': '',
                'padding': 4,

            })


        recs = self.env['res.partner'].search([('user_id','=',self.env.user.id)])
        for rec in recs:
            rec.sale_person_seq=self.env.user.name + '-' + self.env['ir.sequence'].next_by_code(self.env.user.email)



    @api.model
    def create(self, vals):
        mobiles = [ 'phone2', 'mobile', 'mobile2', 'mobile3']



        for item in mobiles :

            get_phone = self.env['res.partner'].search(['|','|','|','|',
                                                        ('phone','=',vals[item]),
                                                        ('phone2','=',vals[item]),
                                                        ('mobile','=',vals[item]),
                                                        ('mobile3','=',vals[item]),
                                                        ('mobile2','=',vals[item])])
            if get_phone and vals[item] :
                raise exceptions.ValidationError("phone number already exist before  ")
        # handle contact sequence for user
        # check if user has sequence befor


        self.update_seq()

        contact_seq = self.env['ir.sequence'].search([('code','=',self.env.user.email)])
        if len(contact_seq) < 1 :
           seq =  self.env['ir.sequence'].sudo().create({
                'code':self.env.user.email,
                'name':self.env.user.name,
               'implementation': 'no_gap',
               'prefix': self.env.user.name + '-',
               'suffix': '',
               'padding': 4,

            })


        vals['sale_person_seq']=self.env.user.name + '-'+ self.env['ir.sequence'].next_by_code(self.env.user.email)

        return super(ResPartner, self).create(vals)

    @api.onchange('division')
    def division_change_domain(self):
        self.sub_division=None
        sub_vision_domain = [('division_id','=',self.division.id)]

        return {
            'domain':{
                'sub_division':sub_vision_domain
            }
        }

    @api.depends('street', 'street2', 'city', 'state_id', 'zip', 'country_id')
    def _compute_full_address(self):
        for partner in self:
            full_address = ''
            if partner.street:
                full_address += partner.street
            if partner.street2:
                full_address += '-' + partner.street2
            if partner.city:
                full_address += '-' + partner.city
            if partner.state_id:
                full_address += '-' + partner.state_id.name
            if partner.zip:
                full_address += ' ' + partner.zip
            if partner.country_id:
                full_address += '-' + partner.country_id.name
            partner.full_address = full_address

    class division_crm(models.Model):
        _name = 'division.crm'
        _description = 'division.crm'

        name = fields.Char(required=True)
        sub_division = fields.One2many('sub_division.crm', 'division_id')

    class sub_division_crm(models.Model):
        _name = 'sub_division.crm'
        _description = 'sub_division.crm'

        name = fields.Char(required=True)
        division_id = fields.Many2one('division.crm')

    class FollowupMethod(models.Model):
        _name = 'followup.method'
        _description = 'followup.method'

        name = fields.Char(required=True)

    class JobCategory(models.Model):
        _name = 'job.category'
        _description = 'job.category'

        name = fields.Char(required=True)
