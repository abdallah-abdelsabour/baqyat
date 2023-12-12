from odoo import api, fields, models, _
from pprint import pprint


class InKindDonation(models.Model):
    _name = 'in.kind.donation'
    _description = 'in.kind.donation'

    name = fields.Char(required=True)