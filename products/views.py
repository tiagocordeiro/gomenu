from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from products.facade import get_product, get_from_category
from products.forms import CategoryForm, ProductVariationForm, ProductForm
from products.models import Category, Product, ProductVariation
from restaurants.models import Restaurant, RestaurantIntegrations


@login_required
def categories_list(request):
    categories = Category.objects.filter(restaurant__manager=request.user)
    context = {'categories': categories}

    return render(request, 'products/list_categories.html', context)


@login_required
def category_new(request):
    try:
        restaurant = Restaurant.objects.get(manager=request.user)
    except Restaurant.DoesNotExist:
        messages.warning(request, "Você precisa cadastrar um restaurante")
        return redirect('new_restaurant')

    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.restaurant = restaurant
            category.save()
            messages.success(request, "Nova categoria cadastrada.")
            return redirect(categories_list)
    else:
        form = CategoryForm()

    return render(request, 'products/category_new.html', {'form': form})


@login_required
def products_list(request):
    products = Product.objects.all().order_by('category__name', 'name').filter(
        restaurant__manager=request.user)

    simple_products = products.filter(productvariation__isnull=True)

    variation_products = ProductVariation.objects.all().filter(
        product__restaurant__manager=request.user)

    context = {
        'simple_products': simple_products,
        'variation_products': variation_products,
    }
    return render(request, 'products/list_products.html', context=context)


@login_required
def product_new(request):
    try:
        restaurant = Restaurant.objects.get(manager=request.user)
    except Restaurant.DoesNotExist:
        messages.warning(request, "Você precisa cadastrar um restaurante")
        return redirect('new_restaurant')

    product_form = Product()
    variations_formset = inlineformset_factory(Product, ProductVariation,
                                               form=ProductVariationForm,
                                               extra=1)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product_form, prefix='main')
        form.fields["category"].queryset = Category.objects.filter(
            restaurant__manager=request.user)

        formset = variations_formset(request.POST, instance=product_form,
                                     prefix='product')

        if form.is_valid() and formset.is_valid():
            novo_produto = form.save(commit=False)
            novo_produto.restaurant = restaurant
            novo_produto.save()
            formset.save()

            messages.success(request, "Novo produto cadastrado.")
            return redirect(products_list)

    else:
        form = ProductForm(instance=product_form, prefix='main')
        form.fields["category"].queryset = Category.objects.filter(
            restaurant__manager=request.user)
        formset = variations_formset(instance=product_form, prefix='product')

    return render(request, 'products/product_new.html', {'form': form,
                                                         'formset': formset})


@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.user.is_superuser or request.user == product.restaurant.manager:
        pass
    else:
        messages.warning(request, "Você não tem permissão.")
        return redirect('dashboard')

    variations_formset = inlineformset_factory(Product, ProductVariation,
                                               form=ProductVariationForm,
                                               extra=1)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product, prefix='main')
        formset = variations_formset(request.POST, instance=product,
                                     prefix='product')

        try:
            if form.is_valid() and formset.is_valid():
                form.save()
                formset.save()
                messages.success(request, "Produto atualizado")
                return redirect('product_update', pk=pk)
        except Exception as e:
            messages.warning(request,
                             'Ocorreu um erro ao atualizar: {}'.format(e))

    else:
        form = ProductForm(instance=product, prefix='main')
        formset = variations_formset(instance=product, prefix='product')

    return render(request, 'products/product_update.html', {'form': form,
                                                            'formset': formset, })


@login_required
def import_from_woocommerce(request, product_id):
    try:
        restaurant = Restaurant.objects.get(manager=request.user)
    except Restaurant.DoesNotExist:
        messages.warning(request, "Você precisa cadastrar um restaurante")
        return redirect('new_restaurant')

    try:
        woo_integration_data = restaurant.restaurantintegrations_set
        consumer_key = woo_integration_data.get().wc_consumer_key
        consumer_secret = woo_integration_data.get().wc_consumer_secret
        woo_commerce_url = woo_integration_data.get().woo_commerce_url
    except RestaurantIntegrations.DoesNotExist:
        messages.warning(request, "Solicite a integração para o suporte")
        return redirect('dashboard')

    product = get_product(product_id=product_id,
                          consumer_key=consumer_key,
                          consumer_secret=consumer_secret,
                          woo_commerce_url=woo_commerce_url)
    return JsonResponse(product.json())


@login_required
def import_all_from_woocommerce_category(request, category_id):
    try:
        restaurant = Restaurant.objects.get(manager=request.user)
    except Restaurant.DoesNotExist:
        messages.warning(request, "Você precisa cadastrar um restaurante")
        return redirect('new_restaurant')

    try:
        woo_integration_data = restaurant.restaurantintegrations_set
        consumer_key = woo_integration_data.get().wc_consumer_key
        consumer_secret = woo_integration_data.get().wc_consumer_secret
        woo_commerce_url = woo_integration_data.get().woo_commerce_url
    except RestaurantIntegrations.DoesNotExist:
        messages.warning(request, "Solicite a integração para o suporte")
        return redirect('dashboard')

    products = get_from_category(category_id, restaurant=restaurant,
                                 consumer_key=consumer_key,
                                 consumer_secret=consumer_secret,
                                 woo_commerce_url=woo_commerce_url)
    return JsonResponse(products)
