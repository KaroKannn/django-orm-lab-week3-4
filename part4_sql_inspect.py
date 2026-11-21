import django.db
from django.db.models import Q
from core.models import Employee, Course

qs = Employee.objects.filter(Q(department__code="IT") | Q(salary__gt=70000))
print("Q OR query SQL:\n", qs.query, "\n")

django.db.reset_queries()
list(Employee.objects.select_related('department').all())
print("select_related queries:", len(django.db.connection.queries))
for q in django.db.connection.queries:
    print(f"SQL: {q['sql']} | Time: {q['time']}s")

django.db.reset_queries()
for c in Course.objects.prefetch_related('attendees'):
    list(c.attendees.all())
print("\nprefetch_related queries:", len(django.db.connection.queries))
for q in django.db.connection.queries:
    print(f"SQL: {q['sql']} | Time: {q['time']}s")
