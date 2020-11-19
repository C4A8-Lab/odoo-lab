# Copyright 2015 Camptocamp SA - Guewen Baconnier
# Copyright 2017 Tecnativa, S.L. - Luis M. Ontalba
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from datetime import timedelta, datetime, time
import logging

_logger = logging.getLogger(__name__)

from odoo import _, api, exceptions, fields, models
from odoo.tools.float_utils import float_compare


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"
    _order = "date desc, time_start desc, id desc"

    datetime_start = fields.Datetime(compute= "_compute_datetime_start", inverse="_update_datetime_start", string="Begin")
    datetime_stop = fields.Datetime(compute= "_compute_datetime_stop", inverse="_update_datetime_stop", string="End")

    @api.depends('date', 'time_start')
    def _compute_datetime_start(self):
        for rec in self:

            start = timedelta(hours=rec.time_start)
            rec.datetime_start = datetime.combine(rec.date, time(0)) + start
    
    @api.depends('date', 'time_stop')
    def _compute_datetime_stop(self):
        for rec in self:
            stop = timedelta(hours=rec.time_stop)
            rec.datetime_stop = datetime.combine(rec.date, time(0)) + stop
            _logger.info(rec.datetime_stop)
            
    def _update_datetime_start(self):
        for rec in self:
            rec.time_start = (rec.datetime_start.time - time(0)).hours
         
    def _update_datetime_stop(self):
        for rec in self:
            rec.time_stop = (rec.datetime_stop.time - time(0)).hours
 