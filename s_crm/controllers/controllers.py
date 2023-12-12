# -*- coding: utf-8 -*-
# from odoo import http


# class SCrm(http.Controller):
#     @http.route('/s_crm/s_crm', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/s_crm/s_crm/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('s_crm.listing', {
#             'root': '/s_crm/s_crm',
#             'objects': http.request.env['s_crm.s_crm'].search([]),
#         })

#     @http.route('/s_crm/s_crm/objects/<model("s_crm.s_crm"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('s_crm.object', {
#             'object': obj
#         })
