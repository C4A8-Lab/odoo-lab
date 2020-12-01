# Copyright 2015 Camptocamp SA - Guewen Baconnier
# Copyright 2017 Tecnativa, S.L. - Luis M. Ontalba
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import pytz
from datetime import timedelta, datetime, time
from odoo import _, api, exceptions, fields, models
from odoo.tools.float_utils import float_compare

import logging
_logger = logging.getLogger(__name__)



class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"
    _order = "date desc, time_start desc, id desc"

    datetime_start = fields.Datetime(compute= "_compute_datetime_start", inverse="_update_datetime_start", string="Begin")
    datetime_stop = fields.Datetime(compute= "_compute_datetime_stop", inverse="_update_datetime_stop", string="End")

    @api.model
    def create(self, values):
        _logger.info("Event {module} create".format(module = self._inherit))  
        _logger.info(values)
        
        if ('unit_amount' in values):
            if ('time_start' not in values or values['time_start'] == 0):
                start = 8
                employeeId = self.env['hr.employee'].search([('user_id','=',self.env.user.id)], limit=1)
                               
                _logger.info("Employee_id")
                _logger.info(employeeId)
                if ('employee_id' in values and 'date' in values):
                    otherWork = self.env[self._inherit].search([['employee_id','=',values['employee_id']],['date','=',values['date']]], order='date desc,time_stop desc', limit=1)
                    _logger.info(otherWork)
                    if (otherWork.time_stop != 0):
                        start = otherWork.time_stop

                _logger.info("Set start time to {start}".format(start = start))  
                values['time_start'] = start
                values['time_stop'] = start + values['unit_amount']
            else:
                 _logger.info("Set Stop")
                 values['time_stop'] = values['time_start'] + values['unit_amount']

        result = super(AccountAnalyticLine, self).create(values)
        return result

    @api.model
    def copy(self, values):
        _logger.info("Event {module} copy".format(module = self._inherit))  
        _logger.info(values)  
        
        values['time_start'] = 0
        values['time_stop'] = values['unit_amount']
        _logger.info(values)  
        
        result = super(AccountAnalyticLine, self).copy(values)
        
#        for rec in result:
#            _logger.info(rec)  
#            rec.time_start = 0
#            rec.time_stop = rec['unit_amount']
        
        _logger.info("/Event {module} copy".format(module = self._inherit))  
        _logger.info(result)  
        return result

    @api.model
    def write(self, values):
        _logger.info("Event {module} write".format(module = self._inherit))  
        _logger.info(values)  
        
        if ('unit_amount' in values):
#            if ('time_start' not in values and self.time_start == 0):
#                otherWork = self.env[self._inherit].search([['employee_id','=',self.employee_id[0].id],['date','=',self.date]], order='date desc,time_stop desc', limit=1)
#                if (otherWork.time_stop != 0):
#                    values['time_start'] = otherWork.time_stop
#                else:
#                    values['time_start'] = 8

            if ('time_start' in values):
                values['time_stop'] = values['time_start'] + values['unit_amount']
            else:
                values['time_stop'] = self.time_start + values['unit_amount']
        _logger.info(values)  
        result = super(AccountAnalyticLine, self).write(values)
        _logger.info("/Event {module} write".format(module = self._inherit))  
        _logger.info(result)  
        return result
    
    @api.model
    def default_get(self, fields_list):
        _logger.info("Event {module} default_get".format(module = self._inherit))  
        _logger.info(fields_list)  
        result = super(AccountAnalyticLine, self).default_get(fields_list)
        
#        if ('time_start' in fields_list):
#            result['time_start'] = 0
#            
#        if ('time_stop' in fields_list):
#            result['time_stop'] = 0
            
        _logger.info(result)
        
#        if ('time_start' in result):
#            start = 8
#            if (otherWork):
#                start = otherWork[0].time_stop
#            _logger.info("Set start time to {start}".format(start = start))  
#            values['time_start'] = start
#            values['time_stop'] = start + values['unit_amount']        
        
#        if ('datetime_start' in result):
#            start = result['time_start'] - datetime.combine(result['datetime_start'].date(), time(0))
#            result['time_start'] = start.seconds / 3600
#            
#        if (result.datetime_stop):
#            stop = result['time_stop'] - datetime.combine(result['datetime_stop'].date(), time(0))
#            result['time_stop'] = stop.seconds / 3600
       
        _logger.info("/Event {module} default_get".format(module = self._inherit))  
        _logger.info(result)  
        return result

    

    def _get_user_timezone(self):
        context = self._context
        current_uid = context.get('uid')
        user = self.env['res.users'].browse(current_uid)
        return  pytz.timezone(user.partner_id.tz)

    @api.depends('date', 'time_start')
    def _compute_datetime_start(self):
        _logger.info("Triggered _compute_datetime_start")

        for rec in self:
            start = timedelta(hours=rec.time_start)
            dt = datetime.combine(rec.date, time(0)) + start
            rec.datetime_start =  dt - self._get_user_timezone().utcoffset(dt)
    
    @api.depends('date', 'time_stop')
    def _compute_datetime_stop(self):
        _logger.info("Triggered _compute_datetime_stop")
        for rec in self:
            stop = timedelta(hours=rec.time_stop)
            dt = datetime.combine(rec.date, time(0)) + stop
            rec.datetime_stop =  dt - self._get_user_timezone().utcoffset(dt)

    
    
    @api.depends('date', 'unit_amount')
    def _compute_datetime_stop_duration(self):
        _logger.info("Triggered _compute_datetime_stop_duration")
        _logger.info(self)
        for rec in self:
            _logger.info(rec.employee_id)
            _logger.info(rec.time_start)
            _logger.info(rec.time_stop)
            _logger.info(rec.datetime_start)
            _logger.info(rec.datetime_stop)
            _logger.info(rec.unit_amount)

#            otherWork = self.env[self._inherit].search([['employee_id','=',rec.employee_id[0].id],['date','=',rec.date]], order='date desc,time_stop desc')
#            _logger.info(otherWork)
#            
#            if (rec.time_start == 0):
#                start = 8
#                if (otherWork):
#                    start = otherWork[0].time_stop
#                rec.time_start = start

            stop = timedelta(hours=rec.time_start) + timedelta(hours=rec.unit_amount)
#            dt = datetime.combine(rec.date, time(0)) + stop
#            rec.datetime_stop =  dt - self._get_user_timezone().utcoffset(dt)
            rec.time_stop =  stop.seconds / 3600
            
    @api.onchange('date', 'unit_amount')
    def _onchange_datetime_stop_duration(self):
        _logger.info("Triggered _onchange_datetime_stop_duration")
        _logger.info(self)
       
        for rec in self:
            _logger.info(rec.employee_id)
            _logger.info(rec.employee_id[0])
            _logger.info(rec.time_start)
            _logger.info(rec.time_stop)
            _logger.info(rec.datetime_start)
            _logger.info(rec.datetime_stop)
            _logger.info(rec.unit_amount)

            
#            otherWork = self.env[self._inherit].search([['employee_id','=',rec.employee_id[0].id],['date','=',rec.date]], order='date desc,time_stop desc')
#            _logger.info(otherWork)
#            
#            if (rec.time_start == 0):
#                start = 8
#                if (otherWork):
#                    start = otherWork[0].time_stop
#                rec.time_start = start
#            
            stop = timedelta(hours=rec.time_start) + timedelta(hours=rec.unit_amount)
            dt = datetime.combine(rec.date, time(0)) + stop
#            rec.datetime_stop =  dt - self._get_user_timezone().utcoffset(dt)
            rec.time_stop =  stop.seconds / 3600
                        

    @api.constrains("time_start", "time_stop", "unit_amount")
    def _check_time_start_stop(self):
        return True


    @api.onchange('datetime_start', 'datetime_stop')
    def _onchange_datetime_start(self):
        _logger.info("Triggered onchange_datetime_start")
        _logger.info(self)
        for rec in self:
            start = rec.datetime_start - datetime.combine(rec.datetime_start.date(), time(0))
            stop = rec.datetime_stop - datetime.combine(rec.datetime_stop.date(), time(0))
            
            rec.time_start = start.total_seconds() / 3600
            rec.time_stop = stop.total_seconds() / 3600
            rec.unit_amount = (stop - start).seconds / 3600
            rec.date = rec.datetime_start.date()
             
    def _update_datetime_start(self):
        _logger.info("Triggered _update_datetime_start")
        _logger.info(self)
        for rec in self:
            tzone = self._get_user_timezone()
            start = rec.datetime_start - datetime.combine(rec.datetime_start.date(), time(0)) + tzone.utcoffset(rec.datetime_start)
            #stop = rec.datetime_stop - datetime.combine(rec.datetime_stop.date(), time(0)) + tzone.utcoffset(rec.datetime_stop)
            
            rec.time_start = start.total_seconds() / 3600
            #rec.time_stop = stop.total_seconds() / 3600
            #rec.unit_amount = (stop - start).seconds / 3600
            rec.date = rec.datetime_start.date()

        _logger.info("Completed _update_datetime_start")
        
    def _update_datetime_stop(self):
        _logger.info("Triggered _update_datetime_stop")
        _logger.info(self)
        for rec in self:
            tzone = self._get_user_timezone()
            start = timedelta(hours=rec.time_start)
            stop = rec.datetime_stop - datetime.combine(rec.datetime_stop.date(), time(0)) + tzone.utcoffset(rec.datetime_stop)
            
           # rec.time_start = start.total_seconds() / 3600
            rec.time_stop = stop.total_seconds() / 3600
            rec.unit_amount = (stop - start).seconds / 3600
            #rec.date = rec.datetime_start.date()

        _logger.info("Completed _update_datetime_stop")
         
#    @api.onchange("datetime_start", "datetime_stop")
#    def onchange_hours_start_stop(self):
#        _logger.info("Triggered onchange_hours_start_stop")
#        start = self.datetime_start - datetime.combine(self.datetime_start.date(), time(0))
#        stop = self.datetime_stop - datetime.combine(self.datetime_stop.date(), time(0))
#        if stop < start:
#            return
#        self.unit_amount = (stop - start).seconds / 3600

 #   def _update_datetime_stop(self):
 #       for rec in self:
 #           dif = rec.datetime_stop - datetime.combine(rec.datetime_stop.date(), time(0))
 #           rec.time_stop = dif.total_seconds() / 3600

 