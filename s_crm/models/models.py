# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SimpleCrm(models.TransientModel):
    _name = 'simple.crm.wizard'
    _description = "simple wizart opprtunity create"
    contact = fields.Many2one('res.partner')
    expected_donation = fields.Float(string='Expected Donation')
    # program = fields.Many2one('division.crm')
    # sub_program = fields.Many2one('sub_division.crm')
    division = fields.Selection([
        ('شركات', 'شركات'),
        ('بنوك', 'بنوك'),
        ('جامعات', 'جامعات'),
        ('مدارس', 'مدارس'),
        ('نوادي', 'نوادي'),
        ('فنادق', 'فنادق'),
        ('مؤسسات', 'مؤسسات'),
        ('متطوعين', 'متطوعين'),
        ('افراد', 'افراد'),
    ])
    sub_division = fields.Selection([
        ('شركات', 'شركات'),
        ('بنوك', 'بنوك'),
        ('جامعات', 'جامعات'),
        ('مدارس', 'مدارس'),
        ('نوادي', 'نوادي'),
        ('فنادق', 'فنادق'),
        ('مؤسسات', 'مؤسسات'),
        ('متطوعين', 'متطوعين'),
        ('افراد', 'افراد'),
    ])
    sales_person = fields.Many2one('res.users')
    donation_preferred = fields.Datetime('Donation Preferred')
    divided = fields.Boolean("تبرع مقسم")
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

    def save(self):
        print('save')
        # update_contact_with_new info
        contact = self.env['res.partner'].search([('id', '=', self.contact.id)])
        if contact:
            contact.write({

                'program': self.division,
                'sub_program': self.sub_division,
            })

        opp = self.env['crm.lead'].create({
            'user_id': self.env.user.id,
            'phone': self.contact.phone,
            'partner_id': self.contact.id,
            'name': self.contact.name + "'s opportunity",
            # 'date_deadline':self.donation_preferred,
            "division": self.division,
            "sub_division": self.sub_division,
            "expected_donation": self.expected_donation,
            "d_electricty": self.d_electricty,
            "d_celling": self.d_celling,
            "d_drainage": self.d_drainage,
            "d_Blankets": self.d_Blankets,
            "d_food": self.d_food,
            "d_marriage": self.d_marriage,
            "d_water": self.d_water,
            "d_Orphan": self.d_Orphan,
            "d_redemption": self.d_redemption,
            "d_Shrouds": self.d_Shrouds,
            "d_Gaza": self.d_Gaza,


        })

    def cancel(self):
        print('cancle')

    # @api.onchange('division')
    # def division_change_domain(self):
    #     self.sub_division = None
    #     sub_vision_domain = [('division_id', '=', self.division.id)]
    #
    #     return {
    #         'domain': {
    #             'sub_division': sub_vision_domain
    #         }
    #     }


class Contactmodel(models.Model):
    _inherit = 'res.partner'


    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        print('search', args)
        # add all fieds to search
        args = args or []
        if len(args) >= 2 and len(args) != 9 and args[0] == '|':
            name = args[2][2]
        else :
            name = ''
        domains = [field[0] for field in args if len(field) == 3 and field[0] not in [ 'phone', 'phone2','mobile','mobile2','mobile3']] +[ 'phone', 'phone2','mobile','mobile2','mobile3']
        if len(args) >= 2 and len(args) != 9 and args[0] == '|':
            args = []
            for index in range(0,len(domains) -1 ):
                if index == 0:

                    args.append([domains[index],'ilike',name])
                elif index == len(domains)-1:

                    args.append([domains[index],'ilike',name])
                else:
                    # args.append('|')
                    args.insert(0, '|')
                    args.append([domains[index],'ilike',name])
        return super(Contactmodel, self)._search(args, offset, limit, order, count, access_rights_uid)

    @api.model
    def create(self, vals):
        phone_count = 0
        for phone in ['phone', 'phone2', 'mobile', 'mobile2', 'mobile3']:
            if vals[phone]:
                phone_count += 1
        if not phone_count:
            raise UserError(_("contact must have one phone number at lease"))
        return super(Contactmodel, self).create(vals)

    def add_opp(self):
        print('add opp button')
        # return action to open form

        return {
            'type': 'ir.actions.act_window',
            'name': _('create_new Opprtunity'),
            'res_model': 'simple.crm.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_id': self.id,
                        'default_contact': self.id,
                        'default_sales_person': self.env.user.id,
                        'default_division': self.program,
                        'default_sub_division': self.sub_program,
                        # 'default_user_status':self.user_status,
                        'default_program': self.division.id,
                        'default_sub_program': self.sub_division.id,
                        # 'default_user_status':self.user_status,

                        }

            # 'views': [['form']]
        }


class CrmLead(models.Model):
    _inherit = 'crm.lead'
    expected_donation = fields.Float(string='Expected Donation')

    # program = fields.Selection([
    #     (" ", " "),
    #     ("صدقة", "صدقة"),
    #     ("كفالة مريض", "كفالة مريض"),
    #     ("كفالة علاج", "كفالة علاج"),
    #     ("تغذيه علاجية", "تغذيه علاجية"),
    #     ("عشور", "عشور"),
    # ], string=' program')

    # def write(self,vals):
    #
    #     print('toste',vals)
    #     if vals.get('stage_id') == 3:
    #         # check cash vals
    #             if self.cash_amount or self.cheque_amount or self.in_kind_donation_value :
    #                 return super(CrmLead, self).write(vals)
    #             raise UserError(_("cant collect without cash or in_kind amount"))

    division = fields.Selection([
        ('شركات', 'شركات'),
        ('بنوك', 'بنوك'),
        ('جامعات', 'جامعات'),
        ('مدارس', 'مدارس'),
        ('نوادي', 'نوادي'),
        ('فنادق', 'فنادق'),
        ('مؤسسات', 'مؤسسات'),
        ('متطوعين', 'متطوعين'),
        ('افراد', 'افراد'),
    ])
    sub_division = fields.Selection([
        ('شركات', 'شركات'),
        ('بنوك', 'بنوك'),
        ('جامعات', 'جامعات'),
        ('مدارس', 'مدارس'),
        ('نوادي', 'نوادي'),
        ('فنادق', 'فنادق'),
        ('مؤسسات', 'مؤسسات'),
        ('متطوعين', 'متطوعين'),
        ('افراد', 'افراد'),
    ])



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

    # @api.model
    # def create(self,vals):
    #     print("create258",vals)
    #     return  super(CrmLead,self).create(vals)
    #
