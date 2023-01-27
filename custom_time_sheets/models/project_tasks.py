from odoo import fields, models, api


class ProjectTasks(models.Model):
    _inherit = "project.task"

    warranty_hours = fields.Float(string="Warranty Hours",
                                  compute="_compute_warranty_hours",
                                  compute_sudo=True,
                                  store=True)
    normal_hours = fields.Float(string="Normal Hours", compute="_compute_normal_hours", store=True)

    @api.depends('timesheet_ids.unit_amount', 'timesheet_ids.type_hours')
    def _compute_warranty_hours(self):
        if not any(self._ids):
            for task in self:
                task.warranty_hours = sum(task.timesheet_ids.filtered(lambda x: x.type_hours == 'warranty_hours')
                                          .mapped('unit_amount'))
                return
        timesheet_read_group = self.env['account.analytic.line'].read_group([('task_id', 'in', self.ids),
                                                                             ('type_hours', '=', 'warranty_hours')],
                                                                            ['unit_amount', 'task_id',
                                                                             'type_hours'], ['task_id'])
        timesheets_per_task = {res['task_id'][0]: res['unit_amount'] for res in timesheet_read_group}
        for task in self:
            task.warranty_hours = round(timesheets_per_task.get(task.id, 0.0), 2)

    @api.depends('timesheet_ids.unit_amount', 'timesheet_ids.type_hours')
    def _compute_normal_hours(self):
        if not any(self._ids):
            for task in self:
                task.normal_hours = sum(task.timesheet_ids.filtered(lambda x: x.type_hours != 'warranty_hours')
                                        .mapped('unit_amount'))
                return
        timesheet_read_group = self.env['account.analytic.line'].read_group([('task_id', 'in', self.ids),
                                                                             ('type_hours', '!=', 'warranty_hours')],
                                                                            ['unit_amount', 'task_id',
                                                                             'type_hours'], ['task_id'])
        timesheets_per_task = {res['task_id'][0]: res['unit_amount'] for res in timesheet_read_group}
        for task in self:
            task.normal_hours = round(timesheets_per_task.get(task.id, 0.0), 2)


        # task.normal_hours = round(sum(task.timesheet_ids.filtered(lambda x: x.type_hours == 'normal_hours')
        #                               .mapped('unit_amount')), 2)
