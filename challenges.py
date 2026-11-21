from decimal import Decimal
from django.db.models import Q, F, Case, When, DecimalField
from django.db.models.lookups import GreaterThan
from core.models import Category, Product

# ---- test data ----
Product.objects.all().delete(); Category.objects.all().delete()
elec = Category.objects.create(name="Electronics")
gad = Category.objects.create(name="Gadgets")
def P(name, cat, price, maxp, stock, reorder, promo, status, country):
    return Product.objects.create(name=name, category=cat, price=price, max_allowed_price=maxp,
        stock_quantity=stock, reorder_level=reorder, is_promotional=promo, status=status, warehouse_country=country)
P("Laptop", elec, 25000, 30000, 5, 10, False, "NORMAL", "China")
P("Cable", elec, 300, 500, 100, 10, False, "DISCOUNTED", "Thailand")
P("Phone", elec, 12000, 15000, 15, 10, True, "NORMAL", "Japan")
P("Drone", gad, 1000, 1100, 50, 10, False, "NORMAL", "China")     # 1150 -> capped to 1100
P("Watch", gad, 2000, 5000, 8, 10, False, "CLEARANCE", "Vietnam")  # 2300

# ---- Challenge 1 ----
c1 = Product.objects.filter(
    Q(category__name='Electronics', price__gt=10000) |
    (Q(status='DISCOUNTED') & ~Q(warehouse_country='China'))
)
print("C1:", list(c1))

# ---- Challenge 2 ----
c2 = Product.objects.filter(
    Q(stock_quantity__lte=F('reorder_level')) |
    Q(is_promotional=True, stock_quantity__lt=F('reorder_level') * 2)
)
print("C2:", list(c2))

# ---- Challenge 3 ----
new_price = F('price') * Decimal('1.15')
Product.objects.filter(category__name='Gadgets').update(
    price=Case(
        When(GreaterThan(new_price, F('max_allowed_price')), then=F('max_allowed_price')),
        default=new_price,
        output_field=DecimalField(max_digits=10, decimal_places=2),
    )
)
print("C3:", [(p.name, p.price) for p in Product.objects.filter(category__name='Gadgets')])

# ---- Challenge 4 ----
def purchase(product_id, qty):
    updated = Product.objects.filter(pk=product_id, stock_quantity__gte=qty).update(
        stock_quantity=F('stock_quantity') - qty,
        total_sold=F('total_sold') + qty,
        total_revenue=F('total_revenue') + F('price') * qty,
    )
    if updated == 0:
        raise ValueError("Purchase failed: insufficient stock")
    return True

watch = Product.objects.get(name="Watch")
print("C4 success:", purchase(watch.pk, 3))
try:
    purchase(watch.pk, 999)
except ValueError as e:
    print("C4 guard:", e)
watch.refresh_from_db()
print("C4 result:", watch.stock_quantity, watch.total_sold, watch.total_revenue)
