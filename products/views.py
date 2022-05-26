from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from products.facade import get_product, get_from_category
from products.forms import CategoryForm, ProductVariationForm, ProductForm
from products.models import Category, Product, ProductVariation
from restaurants.models import Restaurant, RestaurantIntegrations


@login_required
def categories_list(request):
    if request.user.groups.filter(name="Customer").exists():
        messages.warning(request, "Você não pode acessar essa página")
        return redirect('orders_list')

    categories = Category.objects.filter(restaurant__manager=request.user)
    context = {'categories': categories}

    return render(request, 'products/list_categories.html', context)


@login_required
def category_new(request):
    if request.user.groups.filter(name="Customer").exists():
        messages.warning(request, "Você não pode acessar essa página")
        return redirect('orders_list')

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


def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.user.is_superuser or request.user == category.restaurant.manager:
        pass
    else:
        messages.warning(request, "Você não tem permissão.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)

        try:
            if form.is_valid():
                form.save()
                messages.success(request, "Categoria atualizada")
                return redirect('category_update', pk=pk)
        except Exception as e:
            messages.warning(request,
                             'Ocorreu um erro ao atualizar: {}'.format(e))

    else:
        form = CategoryForm(instance=category)

    return render(request, 'products/category_update.html', {'form': form})


@login_required
def products_list(request):
    if request.user.groups.filter(name="Customer").exists():
        messages.warning(request, "Você não pode acessar essa página")
        return redirect('orders_list')

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
def products_sort(request, category=None):
    if category is None:
        products = Product.objects.all().order_by('order', 'category__name', 'name').filter(
            restaurant__manager=request.user)
    else:
        products = Product.objects.all().order_by('order', 'category__name', 'name').filter(
            restaurant__manager=request.user, category=category)

    context = {'products': products,
               'category': category}
    return render(request, 'products/sort_products.html', context=context)


@login_required
@require_POST
def save_new_ordering(request):
    ordered_ids = request.POST["ordering"]
    category = request.POST["categoryfilter"]

    if len(ordered_ids) < 1:
        messages.success(request, "Nenhum produto para atualizar")
        return redirect('products_sort')

    current_order = 10
    for lookup_id in ordered_ids.split(","):
        product = Product.objects.get(pk=lookup_id)
        product.order = current_order
        product.save()
        current_order += 10

    messages.success(request, "Ordem de produtos atualizada.")
    if category == "None":
        return redirect('products_sort')

    return redirect('products_sort', category)


@login_required
def product_new(request):
    if request.user.groups.filter(name="Customer").exists():
        messages.warning(request, "Você não pode acessar essa página")
        return redirect('orders_list')

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
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.user.is_superuser or request.user == product.restaurant.manager:
        pass
    else:
        messages.warning(request, "Você não tem permissão.")
        return redirect('products_list')

    if request.method == 'POST':
        product.delete()
        messages.success(request, "Produto excluido")
        return redirect('products_list')

    return render(request, 'products/product_delete.html', {'product': product})


@login_required
def import_from_woocommerce(request, product_id):
    if request.user.groups.filter(name="Customer").exists():
        messages.warning(request, "Você não pode acessar essa página")
        return redirect('orders_list')

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
    if request.user.groups.filter(name="Customer").exists():
        messages.warning(request, "Você não pode acessar essa página")
        return redirect('orders_list')

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
