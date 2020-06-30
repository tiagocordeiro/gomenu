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
    menus = Menu.objects.filter(restaurant__manager=request.user)

    return render(request, 'menus/list.html', context={'menus': menus})


@login_required
def new_menu(request):
    try:
        restaurant = Restaurant.objects.get(manager=request.user)
    except Restaurant.DoesNotExist:
        messages.warning(request, "Você precisa cadastrar um restaurante")
        return redirect('new_restaurant')

    menu_form = Menu()
    categories_menu_formset = inlineformset_factory(
        Menu, MenuCategory,
        form=MenuCategoriesForm, extra=1
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

    context = {'form': form, 'formset': formset}
    return render(request, 'menus/new.html', context=context)


def menu_display(request, slug, pk):
    menu_object = get_object_or_404(Menu, slug=slug, pk=pk)
    menu = menu_builder(pk=menu_object.pk)

    context = {
        'menu_title': menu['title'],
        'menu': menu['itens'],
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


@login_required
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
    }

    return render(request, 'menus/food-menu-print.html', context=context)


def menu_json(request, pk):
    menu = menu_builder(pk=pk)

    context = {
        'menu_title': menu['title'],
        'menu': menu['itens'],
    }

    return JsonResponse(context)
