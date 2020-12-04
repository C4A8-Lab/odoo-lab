# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import AccessDenied, UserError

import logging
_logger = logging.getLogger(__name__)

class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def create(self, values):
        _logger.info("Event {module} create".format(module = self._inherit))  
        _logger.info(values)
        result = super(ResUsers, self).create(values)
        _logger.info("Verson 2")
        _logger.info(result)
        if ('oauth_provider_id' in values and 'login' in values and result.oauth_provider_id.name == 'Microsoft OAuth2'):
            empl = self.env['hr.employee'].search([['work_email','=',values['login']]], limit=1)
            if (empl):
                _logger.info("Link login {login} with user {user}({userid}).".format(login=values['login'], user = empl.name, userid = empl.id))
                empl.user_id = result.id
            else:
                _logger.info("No employee for login {login} found.".format(login=values['login']))

        return result