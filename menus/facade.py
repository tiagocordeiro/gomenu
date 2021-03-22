from products.models import Product, ProductVariation
from .models import Menu


def get_menu(pk):
    return Menu.objects.get(pk=pk)


def menu_builder(pk):
    menu = get_menu(pk=pk)

    menu_itens = []
    category_count = 0

    for category in menu.menucategory_set.select_related('category'):
        menu_itens.append({"category": category.category.name,
                           "description": category.category.description,
                           "show_in_menu": category.show_in_menu,
                           "itens": [], })
        product_count = 0

        for product in Product.objects.filter(category=category.category):
            if product.description:
                menu_itens[category_count]["itens"].append(
                    {"product": {"pk": product.pk,
                                 "name": product.name,
                                 "description": product.description,
                                 "price": product.price}})
            else:
                menu_itens[category_count]["itens"].append(
                    {"product": {"pk": product.pk,
                                 "name": product.name,
                                 "price": product.price}})

            variations = ProductVariation.objects.filter(product=product)
            if variations:
                menu_itens[category_count]["itens"][product_count]["product"][
                    "price"] = []

                for variation in variations:
                    variacao = ProductVariation.objects.get(pk=variation.pk)
                    menu_itens[category_count]["itens"][product_count][
                        "product"]["price"].append(
                        {
                            "variation_pk": variacao.pk,
                            "variation_name": variacao.variation,
                            "variation_price": variation.price
                        })

            product_count += 1
        category_count += 1

    return {'title': menu.name,
            'itens': menu_itens,
            'restaurant_pk': menu.restaurant.pk,
            'online_sale': menu.restaurant.online_sales,
            'variations_style': str(menu.variations_display_style),
            'dark_mode': menu.dark_mode}
