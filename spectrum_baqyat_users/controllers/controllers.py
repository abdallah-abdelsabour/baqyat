# -*- coding: utf-8 -*-
# from odoo import http


# class SpectrumBaqyatUsers(http.Controller):
#     @http.route('/spectrum_baqyat_users/spectrum_baqyat_users', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/spectrum_baqyat_users/spectrum_baqyat_users/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('spectrum_baqyat_users.listing', {
#             'root': '/spectrum_baqyat_users/spectrum_baqyat_users',
#             'objects': http.request.env['spectrum_baqyat_users.spectrum_baqyat_users'].search([]),
#         })

#     @http.route('/spectrum_baqyat_users/spectrum_baqyat_users/objects/<model("spectrum_baqyat_users.spectrum_baqyat_users"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('spectrum_baqyat_users.object', {
#             'object': obj
#         })
