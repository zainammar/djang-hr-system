#!/bin/bash
# HR System Setup Script
# Run this once to install dependencies, migrate, and create superuser

echo "========================================"
echo "   HR System — Setup Script"
echo "========================================"

# Install Django
pip install django --break-system-packages -q

# Go to project directory
cd "$(dirname "$0")"

echo ""
echo "[1/4] Running migrations..."
python manage.py makemigrations employees
python manage.py migrate

echo ""
echo "[2/4] Creating superuser..."
echo "from django.contrib.auth.models import User; User.objects.filter(username='admin').delete(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | python manage.py shell

echo ""
echo "[3/4] Loading sample data..."
python manage.py shell << 'PYEOF'
from employees.models import Department, Employee
from datetime import date

# Create departments
dept_hr = Department.objects.get_or_create(name="Human Resources", code="HR", description="People & culture")[0]
dept_it = Department.objects.get_or_create(name="Information Technology", code="IT", description="Tech & engineering")[0]
dept_fin = Department.objects.get_or_create(name="Finance", code="FIN", description="Finance & accounting")[0]
dept_ops = Department.objects.get_or_create(name="Operations", code="OPS", description="Daily operations")[0]

# Create employees
Employee.objects.get_or_create(
    employee_id="EMP001",
    defaults=dict(first_name="Sarah", last_name="Johnson", email="sarah@company.com",
                  department=dept_hr, designation="HR Manager", date_joined=date(2022, 3, 1), status='active')
)
Employee.objects.get_or_create(
    employee_id="EMP002",
    defaults=dict(first_name="Ahmed", last_name="Khan", email="ahmed@company.com",
                  department=dept_it, designation="Senior Developer", date_joined=date(2021, 7, 15), status='active')
)
Employee.objects.get_or_create(
    employee_id="EMP003",
    defaults=dict(first_name="Fatima", last_name="Ali", email="fatima@company.com",
                  department=dept_fin, designation="Finance Analyst", date_joined=date(2023, 1, 10), status='active')
)
print("Sample data loaded successfully!")
PYEOF

echo ""
echo "[4/4] ✅ Setup complete!"
echo ""
echo "========================================"
echo "  Starting development server..."
echo "  URL:      http://127.0.0.1:8000"
echo "  Username: admin"
echo "  Password: admin123"
echo "========================================"
echo ""
python manage.py runserver
