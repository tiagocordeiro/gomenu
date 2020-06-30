from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from products.forms import CategoryForm
from products.models import Category, Product, ProductVariation
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

    products_simple = products.filter(productvariation__isnull=True)

    variations = ProductVariation.objects.all().filter(
        product__restaurant__manager=request.user)

    context = {
        'products_simple': products_simple,
        'variations': variations,
    }
    return render(request, 'products/list_products.html', context=context)
