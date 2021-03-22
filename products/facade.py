import re

from wordpress import API

from products.models import Category, Product, ProductVariation


def setup_wp_api(consumer_key, consumer_secret, woo_commerce_url):
    wpapi = API(
        url=woo_commerce_url,
        api="wp-json",
        version="wc/v3",
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
    )
    return wpapi


def get_products(consumer_key, consumer_secret, woo_commerce_url):
    wpapi = setup_wp_api(consumer_key, consumer_secret, woo_commerce_url)
    products = wpapi.get("products")
    return products


def get_product(product_id, consumer_key, consumer_secret, woo_commerce_url):
    wpapi = setup_wp_api(consumer_key, consumer_secret, woo_commerce_url)
    product = wpapi.get(f"products/{product_id}")
    return product


def get_product_variations(product_id, consumer_key, consumer_secret, woo_commerce_url):
    wpapi = setup_wp_api(consumer_key, consumer_secret, woo_commerce_url)
    variations = wpapi.get(f"products/{product_id}/variations")
    return variations.json()


def get_category_name(category_id, consumer_key, consumer_secret, woo_commerce_url):
    wpapi = setup_wp_api(consumer_key, consumer_secret, woo_commerce_url)
    category = wpapi.get(f"products/categories/{category_id}")
    return category.json()["name"]


def get_from_category(
    category_id, restaurant, consumer_key, consumer_secret, woo_commerce_url
):
    wpapi = setup_wp_api(consumer_key, consumer_secret, woo_commerce_url)
    products = wpapi.get(f"products?category={category_id}&per_page=100")

    new_products = []
    old_products = []
    new_products_variations = []
    old_products_variations = []
    category_name = get_category_name(
        category_id, consumer_key, consumer_secret, woo_commerce_url
    )

    for product in products.json():
        name = product["name"]
        tag_re = re.compile(r"<[^>]+>")
        description = tag_re.sub("", product["description"])
        price = product["price"]

        try:
            old_category = Category.objects.get(
                name=category_name, restaurant=restaurant
            )
            category = old_category
        except Category.DoesNotExist:
            new_category = Category.objects.create(
                name=category_name, restaurant=restaurant
            )
            new_category.save()
            category = new_category

        try:
            old_product = Product.objects.get(name=name, restaurant=restaurant)
            old_product.description = description
            old_product.price = price
            old_product.category = category
            old_products.append(old_product)
        except Product.DoesNotExist:
            new_product = Product(
                name=name,
                description=description,
                price=price,
                category=category,
                restaurant=restaurant,
            )
            new_products.append(new_product)
            new_product.save()

        if product["type"] == "variable":
            variations = get_product_variations(
                product["id"], consumer_key, consumer_secret, woo_commerce_url
            )
            for variation in variations:
                variation_name = variation["attributes"][0]["option"]
                variation_price = variation["price"]

                try:
                    product_variation = ProductVariation.objects.get(
                        product__name=name,
                        variation=variation_name,
                        product__restaurant=restaurant,
                    )
                    product_variation.price = variation_price
                    product_variation.save()
                    old_products_variations.append(product_variation)
                except ProductVariation.DoesNotExist:
                    product_base = Product.objects.get(name=name, restaurant=restaurant)
                    new_product_variation = ProductVariation(
                        product=product_base,
                        variation=variation_name,
                        price=variation_price,
                    )
                    new_products_variations.append(new_product_variation)
                    new_product_variation.save()

    Product.objects.bulk_update(old_products, ["description", "price", "category"])

    ProductVariation.objects.bulk_update(old_products_variations, ["price"])

    return {"products": products.json()}
