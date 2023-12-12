
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from pprint import pprint
class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
      # Add your custom code here to modify the domain or result fields as needed
      # Example: add a domain filter to only return active partners

      previous_menu_action = self.env.context.get('previous_menu_action')

      call_center_group = "call_center_user"
      marketing_group = "marketing_user"
      sale_group = "Administrator"
      call_center_group_id = self.env['res.groups'].search_read([('name', '=', call_center_group)], ['id'])[0]['id']
      marketing_group_id = self.env['res.groups'].search_read([('name', '=', marketing_group)], ['id'])[0]['id']
      sale_group_id =  self.env['res.groups'].search_read([('name', '=', sale_group)], ['id'])[0]['id']



      user = self.env.user
      group_ids = user.groups_id.ids
      user_id = user.id
      # add if user admin to
      if user_id ==2 or sale_group_id in group_ids:
        result = super(ResPartner, self).search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)
        return result
      if call_center_group_id in group_ids and domain == []:
        domain.append(('id', '=', 0))
      elif call_center_group_id in group_ids and domain != []:
        result = super(ResPartner, self).search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)
        return result
      domain.append(('active', '=', True))
      # ____________________

      allowed_contacts = self.env['res.partner'].search(domain)
      if marketing_group_id in group_ids and domain == [('active', '=', True)]:
        domain.append(('user_id', '=', user_id))
        result = super(ResPartner, self).search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)
        return result
      elif marketing_group_id in group_ids and domain != [('active', '=', True)]:
          domain.append(('user_id', '=', user_id))
          result = super(ResPartner, self).search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)
          contacts_difference = len(allowed_contacts)-len(result)
          if contacts_difference > 0:
              phone_present = False
              mobile_present = False

              # Iterate through the elements in the list
              for item in domain:
                  if isinstance(item, list):
                      # If the element is a list, check its contents
                      if 'phone' in item:
                          phone_present = True
                      if 'mobile' in item:
                          mobile_present = True

              # Check the results
              if phone_present and mobile_present:
                  # if contacts_difference == 1:
                      missing_contacts =[]
                      for record in allowed_contacts.ids :
                          if record not in result :
                              missing_contacts.append(self.env['res.partner'].browse(record))
                      for rec in missing_contacts:
                          raise UserError(_(f'Error this contact  in  {rec.user_id.name} contact`s \n ask for admin help '))



          return result




