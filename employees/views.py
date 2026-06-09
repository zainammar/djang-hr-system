from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Sum
from .models import Department, Employee, Attendance, LeaveRequest, Payroll, JobApplication
from .forms import (DepartmentForm, EmployeeForm, AttendanceForm,
                    LeaveRequestForm, LeaveReviewForm, PayrollForm, JobApplicationForm)


@login_required
def dashboard(request):
    context = {
        'total_employees': Employee.objects.filter(status='active').count(),
        'total_departments': Department.objects.count(),
        'pending_leaves': LeaveRequest.objects.filter(status='pending').count(),
        'total_applications': JobApplication.objects.count(),
        'new_applications': JobApplication.objects.filter(status='applied').count(),
        'recent_employees': Employee.objects.order_by('-created_at')[:5],
        'recent_leaves': LeaveRequest.objects.order_by('-applied_on')[:5],
        'departments': Department.objects.annotate(emp_count=Count('employees'))[:6],
    }
    return render(request, 'employees/dashboard.html', context)


# ── DEPARTMENT ─────────────────────────────────────────────────────────────────
@login_required
def department_list(request):
    departments = Department.objects.annotate(emp_count=Count('employees'))
    return render(request, 'employees/department_list.html', {'departments': departments})


@login_required
def department_create(request):
    form = DepartmentForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Department created successfully.')
        return redirect('department_list')
    return render(request, 'employees/form.html', {'form': form, 'title': 'Add Department', 'back_url': 'department_list'})


@login_required
def department_edit(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    form = DepartmentForm(request.POST or None, instance=dept)
    if form.is_valid():
        form.save()
        messages.success(request, 'Department updated.')
        return redirect('department_list')
    return render(request, 'employees/form.html', {'form': form, 'title': 'Edit Department', 'back_url': 'department_list'})


@login_required
def department_delete(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        dept.delete()
        messages.success(request, 'Department deleted.')
        return redirect('department_list')
    return render(request, 'employees/confirm_delete.html', {'obj': dept, 'back_url': 'department_list'})


# ── EMPLOYEE ───────────────────────────────────────────────────────────────────
@login_required
def employee_list(request):
    employees = Employee.objects.select_related('department').all()
    dept_filter = request.GET.get('department')
    status_filter = request.GET.get('status')
    if dept_filter:
        employees = employees.filter(department_id=dept_filter)
    if status_filter:
        employees = employees.filter(status=status_filter)
    departments = Department.objects.all()
    return render(request, 'employees/employee_list.html', {
        'employees': employees,
        'departments': departments,
        'dept_filter': dept_filter,
        'status_filter': status_filter,
    })


@login_required
def employee_detail(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    attendance = emp.attendance_records.order_by('-date')[:10]
    leaves = emp.leave_requests.order_by('-applied_on')[:5]
    payrolls = emp.payrolls.order_by('-year', '-month')[:6]
    return render(request, 'employees/employee_detail.html', {
        'emp': emp, 'attendance': attendance, 'leaves': leaves, 'payrolls': payrolls
    })


@login_required
def employee_create(request):
    form = EmployeeForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Employee added successfully.')
        return redirect('employee_list')
    return render(request, 'employees/form.html', {'form': form, 'title': 'Add Employee', 'back_url': 'employee_list'})


@login_required
def employee_edit(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    form = EmployeeForm(request.POST or None, instance=emp)
    if form.is_valid():
        form.save()
        messages.success(request, 'Employee updated.')
        return redirect('employee_list')
    return render(request, 'employees/form.html', {'form': form, 'title': 'Edit Employee', 'back_url': 'employee_list'})


@login_required
def employee_delete(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        emp.delete()
        messages.success(request, 'Employee deleted.')
        return redirect('employee_list')
    return render(request, 'employees/confirm_delete.html', {'obj': emp, 'back_url': 'employee_list'})


# ── ATTENDANCE ─────────────────────────────────────────────────────────────────
@login_required
def attendance_list(request):
    records = Attendance.objects.select_related('employee').order_by('-date')
    emp_filter = request.GET.get('employee')
    if emp_filter:
        records = records.filter(employee_id=emp_filter)
    employees = Employee.objects.filter(status='active')
    return render(request, 'employees/attendance_list.html', {
        'records': records, 'employees': employees, 'emp_filter': emp_filter
    })


@login_required
def attendance_create(request):
    form = AttendanceForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Attendance recorded.')
        return redirect('attendance_list')
    return render(request, 'employees/form.html', {'form': form, 'title': 'Mark Attendance', 'back_url': 'attendance_list'})


@login_required
def attendance_edit(request, pk):
    rec = get_object_or_404(Attendance, pk=pk)
    form = AttendanceForm(request.POST or None, instance=rec)
    if form.is_valid():
        form.save()
        messages.success(request, 'Attendance updated.')
        return redirect('attendance_list')
    return render(request, 'employees/form.html', {'form': form, 'title': 'Edit Attendance', 'back_url': 'attendance_list'})


@login_required
def attendance_delete(request, pk):
    rec = get_object_or_404(Attendance, pk=pk)
    if request.method == 'POST':
        rec.delete()
        messages.success(request, 'Record deleted.')
        return redirect('attendance_list')
    return render(request, 'employees/confirm_delete.html', {'obj': rec, 'back_url': 'attendance_list'})


# ── LEAVE REQUEST ──────────────────────────────────────────────────────────────
@login_required
def leave_list(request):
    leaves = LeaveRequest.objects.select_related('employee').order_by('-applied_on')
    status_filter = request.GET.get('status')
    if status_filter:
        leaves = leaves.filter(status=status_filter)
    return render(request, 'employees/leave_list.html', {
        'leaves': leaves, 'status_filter': status_filter
    })


@login_required
def leave_create(request):
    form = LeaveRequestForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Leave request submitted.')
        return redirect('leave_list')
    return render(request, 'employees/form.html', {'form': form, 'title': 'New Leave Request', 'back_url': 'leave_list'})


@login_required
def leave_review(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk)
    form = LeaveReviewForm(request.POST or None, instance=leave)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.reviewed_by = request.user
        obj.reviewed_on = timezone.now()
        obj.save()
        messages.success(request, 'Leave request reviewed.')
        return redirect('leave_list')
    return render(request, 'employees/form.html', {'form': form, 'title': 'Review Leave', 'back_url': 'leave_list', 'extra': leave})


@login_required
def leave_delete(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk)
    if request.method == 'POST':
        leave.delete()
        messages.success(request, 'Leave request deleted.')
        return redirect('leave_list')
    return render(request, 'employees/confirm_delete.html', {'obj': leave, 'back_url': 'leave_list'})


# ── PAYROLL ────────────────────────────────────────────────────────────────────
@login_required
def payroll_list(request):
    payrolls = Payroll.objects.select_related('employee').order_by('-year', '-month')
    return render(request, 'employees/payroll_list.html', {'payrolls': payrolls})


@login_required
def payroll_create(request):
    form = PayrollForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Payroll entry created.')
        return redirect('payroll_list')
    return render(request, 'employees/form.html', {'form': form, 'title': 'Create Payroll', 'back_url': 'payroll_list'})


@login_required
def payroll_edit(request, pk):
    payroll = get_object_or_404(Payroll, pk=pk)
    form = PayrollForm(request.POST or None, instance=payroll)
    if form.is_valid():
        form.save()
        messages.success(request, 'Payroll updated.')
        return redirect('payroll_list')
    return render(request, 'employees/form.html', {'form': form, 'title': 'Edit Payroll', 'back_url': 'payroll_list'})


@login_required
def payroll_delete(request, pk):
    payroll = get_object_or_404(Payroll, pk=pk)
    if request.method == 'POST':
        payroll.delete()
        messages.success(request, 'Payroll deleted.')
        return redirect('payroll_list')
    return render(request, 'employees/confirm_delete.html', {'obj': payroll, 'back_url': 'payroll_list'})


@login_required
def payroll_detail(request, pk):
    payroll = get_object_or_404(Payroll, pk=pk)
    return render(request, 'employees/payroll_detail.html', {'payroll': payroll})


# ── JOB APPLICATIONS ───────────────────────────────────────────────────────────
@login_required
def application_list(request):
    applications = JobApplication.objects.select_related('department').order_by('-applied_on')
    status_filter = request.GET.get('status')
    if status_filter:
        applications = applications.filter(status=status_filter)
    return render(request, 'employees/application_list.html', {
        'applications': applications, 'status_filter': status_filter
    })


@login_required
def application_create(request):
    form = JobApplicationForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Application added.')
        return redirect('application_list')
    return render(request, 'employees/form.html', {'form': form, 'title': 'Add Job Application', 'back_url': 'application_list'})


@login_required
def application_edit(request, pk):
    app = get_object_or_404(JobApplication, pk=pk)
    form = JobApplicationForm(request.POST or None, instance=app)
    if form.is_valid():
        form.save()
        messages.success(request, 'Application updated.')
        return redirect('application_list')
    return render(request, 'employees/form.html', {'form': form, 'title': 'Edit Application', 'back_url': 'application_list'})


@login_required
def application_delete(request, pk):
    app = get_object_or_404(JobApplication, pk=pk)
    if request.method == 'POST':
        app.delete()
        messages.success(request, 'Application deleted.')
        return redirect('application_list')
    return render(request, 'employees/confirm_delete.html', {'obj': app, 'back_url': 'application_list'})
