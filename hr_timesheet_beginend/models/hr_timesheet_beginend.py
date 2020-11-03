

from odoo import models, fields, api
from odoo.tools.float_utils import float_compare

class TimesheetDetails(models.Model):
    _inherit = 'account.analytic.line'

    begin_timestamp = fields.Datetime(string='Begin')
    end_timestamp = fields.Datetime(string='End')

    
    @api.onchange('begin_timestamp', 'end_timestamp')
    def onchange_hours_start_stop(self):
#        start = timedelta(hours=self.time_start)
#        stop = timedelta(hours=self.time_stop)
        if stop < start:
            return
        self.unit_amount = (stop - start).seconds / 3600