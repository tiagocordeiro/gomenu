from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.shortcuts import redirect, render
from django.urls import reverse

from menus.models import Menu
from orders.forms import OrderItemsForm, OrderForm
from orders.models import Order, OrderItem
from products.models import Product, ProductVariation
from restaurants.models import Restaurant


def order_add_item(request, pk, restaurant_pk, menu_pk, **kwargs):
    product = Product.objects.get(pk=pk)
    menu = Menu.objects.get(pk=menu_pk)
    restaurant = Restaurant.objects.get(pk=restaurant_pk)
    if request.user.is_authenticated:
        pass
        # TODO: Lógica para usuários autenticados

    try:
        order_slug = request.session["order_slug"]
    except KeyError:
        order = Order(restaurant=restaurant)

        order.save()
        request.session["order_slug"] = order_slug = order.slug

    order = Order.objects.get(slug=order_slug)
    if order.orderitem_set.all().filter(item=product).exists():

        item = OrderItem.objects.get(order=order, item=product)
        item.quantity = item.quantity + 1
        item.save()
        messages.info(request,
                      f'{product.name} Já está no pedido. '
                      f'<a href="/orders/cart/{order_slug}/" '
                      f'class="alert-link">Ver pedido</a>.')

        return redirect(reverse('restaurant_menu', kwargs={'restaurant_slug': restaurant.slug,
                                                           'menu_slug': menu.slug}))

    else:
        item = OrderItem(order=order, item=product, unity_price=product.price)
        item.save()

    messages.success(request, f'{item.item.name} adicionado ao pedido. '
                              f'<a href="/orders/cart/{order_slug}/" '
                              f'class="alert-link">Ver pedido</a>.')

    return redirect(reverse('restaurant_menu', kwargs={'restaurant_slug': restaurant.slug,
                                                       'menu_slug': menu.slug}))


def order_add_var_item(request, pk, var_pk, restaurant_pk, menu_pk, **kwargs):
    product = Product.objects.get(pk=pk)
    variation = ProductVariation.objects.get(pk=var_pk)
    menu = Menu.objects.get(pk=menu_pk)
    restaurant = Restaurant.objects.get(pk=restaurant_pk)
    if request.user.is_authenticated:
        pass
        # TODO: Lógica para usuários autenticados

    try:
        order_slug = request.session["order_slug"]
    except KeyError:
        order = Order(restaurant=restaurant)

        order.save()
        request.session["order_slug"] = order_slug = order.slug

    order = Order.objects.get(slug=order_slug)
    if order.orderitem_set.all().filter(item=product,
                                        variation=variation).exists():

        item = OrderItem.objects.get(order=order, item=product, variation=variation)
        item.quantity = item.quantity + 1
        item.save()
        messages.info(request,
                      f'{product.name} Já está no pedido. '
                      f'<a href="/orders/cart/{order_slug}/" '
                      f'class="alert-link">Ver pedido</a>.')

        return redirect(reverse('restaurant_menu', kwargs={'restaurant_slug': restaurant.slug,
                                                           'menu_slug': menu.slug}))

    else:
        item = OrderItem(order=order, item=product, unity_price=variation.price, variation=variation)
        item.save()

    messages.success(request, f'{item.item.name} adicionado ao pedido. '
                              f'<a href="/orders/cart/{order_slug}/" '
                              f'class="alert-link">Ver pedido</a>.')
    return redirect(reverse('restaurant_menu', kwargs={'restaurant_slug': restaurant.slug,
                                                       'menu_slug': menu.slug}))


def cart(request, slug):
    order = Order.objects.get(slug=slug)
    if order.status != "pending":
        return redirect(reverse('order_detail', kwargs={'slug': slug}))

    order_items = OrderItem.objects.filter(order=order)
    order_total = 0
    for item in order_items:
        subtotal = item.quantity * item.unity_price
        order_total = order_total + subtotal

    order_items_formset = inlineformset_factory(
        Order, OrderItem, form=OrderItemsForm, extra=0, can_delete=True)

    if request.method == "POST":
        form = OrderForm(request.POST, instance=order, prefix='main')
        formset = order_items_formset(request.POST, instance=order,
                                      prefix='product')

        try:
            if form.is_valid() and formset.is_valid():
                form.save()
                formset.save()
                messages.success(request, "Pedido atualizado")
                return redirect(reverse('cart', kwargs={'slug': slug}))
        except Exception as e:
            messages.warning(request,
                             'Ocorreu um erro ao atualizar: {}'.format(e))

    else:
        form = OrderForm(instance=order, prefix='main')
        formset = order_items_formset(instance=order, prefix='product')

    return render(request, 'orders/cart.html', {'order': order,
                                                'order_items': order_items,
                                                'order_total': order_total,
                                                'form': form,
                                                'formset': formset, })


@login_required
def checkout(request, slug):
    order = Order.objects.get(slug=slug)
    order_items = OrderItem.objects.filter(order=order)
    order_total = 0
    order_items_total = 0
    order.customer = request.user
    for item in order_items:
        subtotal = item.quantity * item.unity_price
        order_total = order_total + subtotal
        order_items_total = order_items_total + item.quantity

    if order.status == "pending":
        order.status = "on_hold"
        order.save()

        restaurant = order.restaurant
        order = Order(restaurant=restaurant)

        order.save()
        request.session["order_slug"] = order.slug

    context = {
        'order': order,
        'order_items': order_items,
        'order_total': order_total,
        'order_items_total': order_items_total,
    }
    return render(request, 'orders/simple_checkout.html', context=context)


@login_required
def orders_list(request):
    template = 'orders/list.html'
    cart_items = 0
    order_slug = False
    if request.user.is_superuser:
        orders = Order.objects.all().order_by('-modified').exclude(status="pending")
    elif request.user.groups.filter(name="Customer").exists():
        template = 'orders/my_orders.html'
        orders = Order.objects.all().filter(customer=request.user).order_by('-modified').exclude(status="pending")

        try:
            order_slug = request.session["order_slug"]
            order = Order.objects.get(slug=order_slug)
            cart_items = len(order.orderitem_set.all())
        except KeyError:
            pass

    else:
        orders = Order.objects.all().filter(restaurant__manager=request.user).order_by('-modified').exclude(
            status="pending")

    return render(request, template, {'orders': orders, 'order_slug': order_slug, 'cart_items': cart_items})


def order_detail(request, slug):
    order = Order.objects.get(slug=slug)
    order_items = OrderItem.objects.filter(order=order)
    order_total = 0
    order_items_total = 0
    for item in order_items:
        subtotal = item.quantity * item.unity_price
        order_total = order_total + subtotal
        order_items_total = order_items_total + item.quantity

    context = {
        'order': order,
        'order_items': order_items,
        'order_total': order_total,
        'order_items_total': order_items_total,
    }
    return render(request, 'orders/detail.html', context=context)
