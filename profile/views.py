from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


def login_view(request):
    if not request.user.is_anonymous:
        return redirect('blog:list')
    form = AuthenticationForm(request)
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_path = request.GET.get('next')
            if next_path:
                return redirect(next_path)
            return redirect('blog:list')
    ctx = {
        'form': form
    }
    return render(request, 'profile/login.html', ctx)


def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('profile:login')
    if request.method == 'POST':
        logout(request)
        return redirect("profile:login")
    return render(request, 'profile/logout.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('blog:list')
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('profile:login')
    context = {
        'form': form
    }
    return render(request, 'profile/register.html', context)


