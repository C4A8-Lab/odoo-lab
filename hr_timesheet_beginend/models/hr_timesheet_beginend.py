

from odoo import models, fields, api
from odoo.tools.float_utils import float_compare

class TimesheetDetails(models.Model):
    _inherit = 'account.analytic.line'

    time_begin = fields.Time(string='Begin')
    time_end = fields.Time(string='End')

    
    @api.onchange('time_begin', 'time_end')
    def onchange_hours_start_stop(self):
        if time_begin & time_end:
            if time_begin < time_end:
                return
            self.unit_amount = (time_end - time_begin).seconds / 3600