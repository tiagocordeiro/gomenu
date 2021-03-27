from menus.models import Menu
from orders.models import Order
from products.models import Product, Category


def get_dashboard_data_summary(user):
    if user.groups.filter(name="Customer").exists():
        total_products = 0
        total_categories = 0
        total_menus = 0
        pedidos = Order.objects.filter(customer=user)
        total_pedidos = len(pedidos)

    else:
        if user.is_superuser:
            menus = Menu.objects.all()
            products = Product.objects.all()
            categories = Category.objects.all()
            pedidos = Order.objects.all().exclude(status="pending")

        else:
            menus = Menu.objects.filter(restaurant__manager=user)
            products = Product.objects.filter(restaurant__manager=user)
            categories = Category.objects.filter(restaurant__manager=user)
            pedidos = Order.objects.filter(restaurant__manager=user)

        total_products = len(products)
        total_categories = len(categories)
        total_menus = len(menus)
        total_pedidos = len(pedidos)

    return {"total_products": total_products,
            "total_categories": total_categories,
            "total_menus": total_menus,
            "total_pedidos": total_pedidos, }
