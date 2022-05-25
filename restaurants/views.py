from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse

from menus.facade import menu_builder
from restaurants.forms import RestaurantForm
from restaurants.models import Restaurant


@login_required
def new_restaurant(request):
    if request.user.groups.filter(name="Customer").exists():
        messages.warning(request, "Você não pode acessar essa página")
        return redirect('orders_list')

    try:
        restaurant = Restaurant.objects.filter(manager=request.user)
        if restaurant:
            messages.warning(request, "Já existe um restaurante cadastrado")
            return redirect('dashboard')
    except Restaurant.DoesNotExist:
        pass

    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.manager = request.user
            restaurant.save()
            messages.success(request, "Novo restaurante cadastrado.")
            return redirect('dashboard')
    else:
        form = RestaurantForm()

    return render(request, 'restaurants/new.html', {'form': form})


@login_required
def restaurant_detail(request, pk):
    restaurant = Restaurant.objects.get(pk=pk)
    if restaurant.manager != request.user:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.manager = request.user
            restaurant.save()
            messages.success(request, "Restaurante atualizado.")
            return redirect('dashboard')
    else:
        form = RestaurantForm(instance=restaurant)

    return render(request, 'restaurants/new.html', {'form': form})


@login_required
def my_restaurant(request):
    restaurant = Restaurant.objects.get(manager=request.user)
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.manager = request.user
            restaurant.save()
            messages.success(request, "Restaurante atualizado.")
            return redirect('dashboard')
    else:
        form = RestaurantForm(instance=restaurant)

    return render(request, 'restaurants/new.html', {'form': form})


def restaurant_main(request, slug):
    restaurant = get_object_or_404(Restaurant, slug=slug)
    if restaurant.manager.is_active:
        pass
    else:
        messages.warning(request, 'Restaurante não encontrado')
        return render(request, 'menus/food-menu.html')

    menu_object = restaurant.menu_set.first()
    menu = menu_builder(pk=menu_object.pk)
    menu_url = reverse('restaurant_main', kwargs={'slug': slug})
    menu_complete_url = ''.join(
        ['https://', get_current_site(request).domain, menu_url])

    if restaurant.image:
        menu_image = restaurant.image.url
    else:
        menu_image = False

    context = {
        'menu_title': menu['title'],
        'menu': menu['itens'],
        'restaurant_pk': menu['restaurant_pk'],
        'variations_style': menu['variations_style'],
        'dark_mode': menu['dark_mode'],
        'menu_pk': menu_object.pk,
        'online_sales': menu['online_sale'],
        'menu_object': menu_object,
        'menu_complete_url': menu_complete_url,
        'restaurant': restaurant,
        'menu_image': menu_image,
    }

    return render(request, 'menus/food-menu.html', context=context)


def restaurant_menu(request, restaurant_slug, menu_slug):
    restaurant = get_object_or_404(Restaurant, slug=restaurant_slug)
    menu_object = restaurant.menu_set.get(slug=menu_slug)
    menu = menu_builder(pk=menu_object.pk)
    menu_url = reverse('restaurant_menu', kwargs={'restaurant_slug': restaurant_slug,
                                                  'menu_slug': menu_slug})
    menu_complete_url = ''.join(
        ['https://', get_current_site(request).domain, menu_url])

    if restaurant.image:
        menu_image = restaurant.image.url
    else:
        menu_image = False

    context = {
        'menu_title': menu['title'],
        'menu': menu['itens'],
        'restaurant_pk': menu['restaurant_pk'],
        'variations_style': menu['variations_style'],
        'dark_mode': menu['dark_mode'],
        'menu_pk': menu_object.pk,
        'online_sales': menu['online_sale'],
        'menu_object': menu_object,
        'menu_complete_url': menu_complete_url,
        'restaurant': restaurant,
        'menu_image': menu_image,
    }

    return render(request, 'menus/food-menu.html', context=context)
