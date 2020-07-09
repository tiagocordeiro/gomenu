from menus.models import Menu
from products.models import Product, Category


def get_dashboard_data_summary(user):
    if user.is_superuser:
        menus = Menu.objects.all()
        products = Product.objects.all()
        categories = Category.objects.all()
    else:
        menus = Menu.objects.filter(restaurant__manager=user)
        products = Product.objects.filter(restaurant__manager=user)
        categories = Category.objects.filter(restaurant__manager=user)
    return {"total_products": len(products),
            "total_categories": len(categories),
            "total_menus": len(menus), }
