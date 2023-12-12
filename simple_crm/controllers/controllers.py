# -*- coding: utf-8 -*-
# from odoo import http


# class SimpleCrm(http.Controller):
#     @http.route('/simple_crm/simple_crm', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/simple_crm/simple_crm/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('simple_crm.listing', {
#             'root': '/simple_crm/simple_crm',
#             'objects': http.request.env['simple_crm.simple_crm'].search([]),
#         })

#     @http.route('/simple_crm/simple_crm/objects/<model("simple_crm.simple_crm"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('simple_crm.object', {
#             'object': obj
#         })
