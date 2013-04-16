from celery.execute import send_task
from django.contrib import admin
from djcelery import admin as djcelery_admin
from djcelery.models import PeriodicTask
import json

class ExtendedPeriodicTaskAdmin(djcelery_admin.PeriodicTaskAdmin):
    actions = djcelery_admin.PeriodicTaskAdmin.actions + ['run_task']

    def run_task(self, request, queryset):
        if request.user.is_admin:
            for task in queryset.all():
                send_task(task.task, args=json.loads(task.args), kwargs=json.loads(task.kwargs))
            self.message = 'Tasks are running'
        else:
            self.message = 'You must be an admin to perform this action.'
    run_task.short_description = 'Run Task'

admin.site.unregister(PeriodicTask)
admin.site.register(PeriodicTask, ExtendedPeriodicTaskAdmin)

