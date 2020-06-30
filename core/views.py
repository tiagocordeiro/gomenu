from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect

from core.forms import ProfileForm
from core.models import UserProfile


def index(request):
    return render(request, 'base.html')


def dashboard(request):
    return render(request, 'base.html')


@login_required
def profile(request):
    profile_inline_formset = inlineformset_factory(User, UserProfile,
                                                   fields=('avatar',))
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user)
        formset = profile_inline_formset(request.POST, request.FILES,
                                         instance=request.user)

        if form.is_valid():
            perfil = form.save(commit=False)
            formset = profile_inline_formset(request.POST, request.FILES,
                                             instance=perfil)

            if formset.is_valid():
                perfil.save()
                formset.save()
                return redirect('dashboard')

    else:
        form = ProfileForm(instance=request.user)
        formset = profile_inline_formset(instance=request.user)

    context = {'form': form, 'formset': formset, }

    return render(request, 'profile.html', context)
