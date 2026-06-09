from django.contrib import admin
from .models import Department, Employee, Attendance, LeaveRequest, Payroll, JobApplication

admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(Attendance)
admin.site.register(LeaveRequest)
admin.site.register(Payroll)
admin.site.register(JobApplication)
