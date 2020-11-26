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
            stop = timedelta(hours=rec.time_start) + timedelta(hours=rec.unit_amount)
            dt = datetime.combine(rec.date, time(0)) + stop
            rec.datetime_stop =  dt - self._get_user_timezone().utcoffset(dt)
            rec.time_stop =  stop.seconds / 3600
            
    @api.onchange('date', 'unit_amount')
    def _onchange_datetime_stop_duration(self):
        _logger.info("Triggered _onchange_datetime_stop_duration")
        _logger.info(self)
       
        for rec in self:
            _logger.info(rec.time_start)
            _logger.info(rec.time_stop)
            _logger.info(rec.datetime_start)
            _logger.info(rec.datetime_stop)
            _logger.info(rec.unit_amount)
            stop = timedelta(hours=rec.time_start) + timedelta(hours=rec.unit_amount)
            dt = datetime.combine(rec.date, time(0)) + stop
            rec.datetime_stop =  dt - self._get_user_timezone().utcoffset(dt)
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

 