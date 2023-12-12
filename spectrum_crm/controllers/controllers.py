# -*- coding: utf-8 -*-
# from odoo import http


# class SpectrumCrm(http.Controller):
#     @http.route('/spectrum_crm/spectrum_crm', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/spectrum_crm/spectrum_crm/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('spectrum_crm.listing', {
#             'root': '/spectrum_crm/spectrum_crm',
#             'objects': http.request.env['spectrum_crm.spectrum_crm'].search([]),
#         })

#     @http.route('/spectrum_crm/spectrum_crm/objects/<model("spectrum_crm.spectrum_crm"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('spectrum_crm.object', {
#             'object': obj
#         })
