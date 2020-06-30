from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from restaurants.forms import RestaurantForm
from restaurants.models import Restaurant


@login_required
def new_restaurant(request):
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
