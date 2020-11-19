# Copyright 2015 Camptocamp SA - Guewen Baconnier
# Copyright 2017 Tecnativa, S.L. - Luis M. Ontalba
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from datetime import timedelta
import logging

_logger = logging.getLogger(__name__)

from odoo import _, api, exceptions, fields, models
from odoo.tools.float_utils import float_compare


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"
    _order = "date desc, time_start desc, id desc"

    datetime_start = fields.Datetime(compute= "_compute_datetime_start", inverse="", string="Begin", store=False)
    datetime_stop = fields.Datetime(compute= "_compute_datetime_stop", string="End", store=False)

    @api.multi
    def _compute_datetime_start(self):
        start = timedelta(hours=self.time_start)
        self.datetime_start = self.date + start
    
    @api.multi
    def _compute_datetime_stop(self):
        stop = timedelta(hours=self.time_stop)
        self.datetime_stop = self.date + stop
        
    @api.multi
    def _update_datetime_start(self):
        _logger.debug("_update_datetime_start triggered")
        _logger.warning("_update_datetime_start triggered")
        _logger.error("_update_datetime_start triggered")
        
    @api.multi
    def _update_datetime_stop(self):
        _logger.debug("_update_datetime_stop triggered")
        _logger.warning("_update_datetime_stop triggered")
        _logger.error("_update_datetime_stop triggered")
