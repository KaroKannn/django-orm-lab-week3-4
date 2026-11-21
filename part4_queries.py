from decimal import Decimal
import django.db
from django.db.models import Q, F
from core.models import Employee, Course

print("== Task 4.1: Q objects ==")
print("OR:", list(Employee.objects.filter(Q(department__code="IT") | Q(salary__gt=70000))))
print("AND NOT:", list(Employee.objects.filter(Q(first_name__icontains="John") & ~Q(department__code="HR"))))

print("\n== Task 4.2: F expression (10% raise for IT) ==")
Employee.objects.filter(department__code="IT").update(salary=F('salary') * Decimal('1.10'))
for emp in Employee.objects.filter(department__code="IT"):
    print(f"{emp.first_name} New Salary: {emp.salary}")

print("\n== Task 4.3: N+1 ==")
django.db.reset_queries()
for emp in Employee.objects.all():
    print(f"Employee: {emp.first_name}, Department: {emp.department.name}")
print("Queries (unoptimized):", len(django.db.connection.queries))

django.db.reset_queries()
for emp in Employee.objects.select_related('department').all():
    print(f"Employee: {emp.first_name}, Department: {emp.department.name}")
print("Queries (select_related):", len(django.db.connection.queries))

django.db.reset_queries()
for course in Course.objects.prefetch_related('attendees').all():
    names = [e.first_name for e in course.attendees.all()]
    print(f"Course: {course.code}, Attendees: {', '.join(names)}")
print("Queries (prefetch_related):", len(django.db.connection.queries))
