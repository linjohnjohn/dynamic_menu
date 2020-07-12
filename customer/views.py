from django.shortcuts import render

from .forms import CreateUserForm

# Create your views here.
def login(request):
    if request.method == 'GET':
        cart_entries, order = cart_details(request)
        form = CreateUserForm()
        context = {'order': order}
        return render(request, 'orders/login.html', context)
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            django_login(request, user)
            messages.success(request, 'Welcome back %s' % user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR Password is Incorrect')
            return render(request, 'orders/login.html')

def logout(request):
    django_logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('login')

def register(request):
    if request.method == 'GET':
        order, cart_entries = cart_details(request)
        form = CreateUserForm()
        context = {'form': form, 'order': order}
        return render(request, 'orders/register.html', context)
    elif request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            django_login(request, user)
            messages.success(request, 'Account was created for ' + user.email)
            return redirect('home')
        else:
            context = {'form': form}
            return render(request, 'orders/register.html', context)