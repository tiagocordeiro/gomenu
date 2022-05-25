from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from qr_code.qrcode.utils import QRCodeOptions

from menus.facade import menu_builder
from menus.forms import MenuCategoriesForm, MenuForm
from menus.models import Menu, MenuCategory
from products.models import Category
from restaurants.models import Restaurant


@login_required
def menu_list(request):
    if request.user.is_superuser:
        menus = Menu.objects.all()
    else:
        menus = Menu.objects.filter(restaurant__manager=request.user)

    return render(request, 'menus/list.html', context={'menus': menus})


@login_required
def new_menu(request):
    if request.user.groups.filter(name="Customer").exists():
        messages.warning(request, "Você não pode acessar essa página")
        return redirect('orders_list')

    try:
        restaurant = Restaurant.objects.get(manager=request.user)
    except Restaurant.DoesNotExist:
        messages.warning(request, "Você precisa cadastrar um restaurante")
        return redirect('new_restaurant')

    categories = Category.objects.filter(restaurant__manager=request.user)
    menu_form = Menu()
    categories_menu_formset = inlineformset_factory(
        Menu, MenuCategory,
        form=MenuCategoriesForm,
        extra=len(categories), max_num=len(categories)
    )
    if request.method == 'POST':
        form = MenuForm(request.POST, instance=menu_form, prefix='main')
        formset = categories_menu_formset(request.POST,
                                          instance=menu_form,
                                          prefix='product')

        for formulario in formset:
            formulario.fields['category'].queryset = Category.objects.filter(
                restaurant__manager=request.user)

        try:
            if form.is_valid() and formset.is_valid():
                novo_cardapio = form.save(commit=False)
                novo_cardapio.restaurant = restaurant
                novo_cardapio.save()
                formset.save()

                messages.success(request, "Novo cardápio cadastrado.")
                return redirect('menu_list')
        except Exception as e:
            messages.warning(request, f'Ocorreu um erro ao atualizar: {e}')

    else:
        form = MenuForm(instance=menu_form, prefix='main')
        formset = categories_menu_formset(instance=menu_form, prefix='product')

        for formulario in formset:
            formulario.fields['category'].queryset = Category.objects.filter(
                restaurant__manager=request.user)

    # TODO: Aplicar queryset no formset antes.

    context = {'form': form, 'formset': formset}
    return render(request, 'menus/new.html', context=context)


@login_required
def update_menu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    categories = Category.objects.filter(restaurant__manager=request.user)
    if request.user.is_superuser or request.user == menu.restaurant.manager:
        pass
    else:
        messages.warning(request, "Você não tem permissão.")
        return redirect('dashboard')

    menu_categories_formset = inlineformset_factory(Menu, MenuCategory,
                                                    form=MenuCategoriesForm,
                                                    extra=len(categories),
                                                    max_num=len(categories),
                                                    can_delete=True)

    if request.method == 'POST':
        form = MenuForm(request.POST, instance=menu, prefix='main')
        formset = menu_categories_formset(request.POST, instance=menu,
                                          prefix='product')

        # TODO: Aplicar queryset no formset antes.
        for formulario in formset:
            formulario.fields['category'].queryset = Category.objects.filter(
                restaurant__manager=request.user)

        try:
            if form.is_valid() and formset.is_valid():
                form.save()
                formset.save()
                messages.success(request, "Cardápio atualizado.")
                return redirect('update_menu', pk=pk)
        except Exception as e:
            messages.warning(request,
                             'Ocorreu um erro ao atualizar: {}'.format(e))

    else:
        form = MenuForm(instance=menu, prefix='main')
        formset = menu_categories_formset(instance=menu, prefix='product')

        # TODO: Aplicar queryset no formset antes.
        for formulario in formset:
            formulario.fields['category'].queryset = Category.objects.filter(
                restaurant__manager=request.user)

    return render(request, 'menus/update.html', {'form': form,
                                                 'formset': formset})


def menu_display(request, slug, pk):
    menu_object = get_object_or_404(Menu, slug=slug, pk=pk)
    menu = menu_builder(pk=menu_object.pk)
    restaurant = menu_object.restaurant
    if restaurant.manager.is_active:
        pass
    else:
        messages.warning(request, 'Cardápio não disponível')
        return render(request, 'menus/food-menu.html')

    menu_url = reverse('menu_display', kwargs={'slug': slug, 'pk': pk})
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
        'menu_pk': pk,
        'online_sales': menu['online_sale'],
        'menu_object': menu_object,
        'menu_complete_url': menu_complete_url,
        'restaurant': restaurant,
        'menu_image': menu_image,
    }

    return render(request, 'menus/food-menu.html', context=context)


@login_required
def menu_qrcode_gen(request, pk):
    menu = Menu.objects.get(pk=pk)
    menu_url = reverse('menu_display', kwargs={'slug': menu.slug,
                                               'pk': menu.pk})
    complete_url = ''.join(
        ['https://', get_current_site(request).domain, menu_url])
    qrcode_options = QRCodeOptions(size='M')

    context = {
        'menu': menu,
        'complete_url': complete_url,
        'qrcode_options': qrcode_options,
    }
    return render(request, 'menus/qr-gen.html', context=context)


def qr_sheet_gen(request, pk, size):
    """
    Gera uma folha de QR codes.

    :param request:
    :param pk:
    :param size: passado para gerar o qrcode, pode ser:
    s - small
    m - medium (default)
    l - large
    ou um inteiro, exemplo: 50
    :return:
    """
    size = size
    menu = Menu.objects.get(pk=pk)
    menu_url = reverse('menu_display', kwargs={'slug': menu.slug,
                                               'pk': menu.pk})
    complete_url = ''.join(
        ['https://', get_current_site(request).domain, menu_url])
    qrcode_options = QRCodeOptions(size=size)
    if size.lower() == 's':
        loop_time = range(0, 15)
    elif size.lower() == 'm':
        loop_time = range(0, 6)
    elif size.lower() == 'l':
        loop_time = range(0, 2)
    else:
        loop_time = range(0, 1)

    context = {
        'menu': menu,
        'menu_url': menu_url,
        'complete_url': complete_url,
        'qrcode_options': qrcode_options,
        'loop_time': loop_time,
    }
    return render(request, 'menus/qr-sheet-gen.html', context=context)


@login_required
def menu_print(request, pk):
    menu = menu_builder(pk=pk)

    context = {
        'menu_title': menu['title'],
        'menu': menu['itens'],
        'restaurant_pk': menu['restaurant_pk'],
    }

    return render(request, 'menus/food-menu-print.html', context=context)


def menu_json(request, pk):
    menu = menu_builder(pk=pk)

    context = {
        'menu_title': menu['title'],
        'menu': menu['itens'],
        'restaurant_pk': menu['restaurant_pk'],
    }

    return JsonResponse(context)
