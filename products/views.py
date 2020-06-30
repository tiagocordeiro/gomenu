from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect

from products.forms import CategoryForm, ProductVariationForm, ProductForm, \
    VariationForm
from products.models import Category, Product, ProductVariation, Variation
from restaurants.models import Restaurant


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

    restaurnt_variations = Variation.objects.filter(restaurant=restaurant)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product_form, prefix='main')
        form.fields["category"].queryset = Category.objects.filter(
            restaurant__manager=request.user)

        formset = variations_formset(request.POST, instance=product_form,
                                     prefix='product')

        for formulario in formset:
            formulario.fields['variation'].queryset = restaurnt_variations

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

        for formulario in formset:
            formulario.fields['variation'].queryset = restaurnt_variations

    return render(request, 'products/product_new.html', {'form': form,
                                                         'formset': formset})


@login_required
def variations_list(request):
    variations = Variation.objects.all().filter(
        restaurant__manager=request.user)
    context = {'variations': variations}

    return render(request, 'products/list_variations.html', context)


@login_required
def variation_new(request):
    try:
        restaurant = Restaurant.objects.get(manager=request.user)
    except Restaurant.DoesNotExist:
        messages.warning(request, "Você precisa cadastrar um restaurante")
        return redirect('new_restaurant')

    if request.method == "POST":
        form = VariationForm(request.POST)
        if form.is_valid():
            variation = form.save(commit=False)
            variation.restaurant = restaurant
            variation.save()

            messages.success(request, "Nova variação cadastrada.")
            return redirect(variations_list)
    else:
        form = VariationForm()

    return render(request, 'products/variation_new.html', {'form': form})
