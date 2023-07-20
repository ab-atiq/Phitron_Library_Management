from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from library.forms import UserCreationForm
from library.models import Reservation, Borrowing, Fine, WishList


def user_registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_login')
    else:
        form = UserCreationForm()
    return render(request, 'registration.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('book_search')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('user_login')


@login_required
def user_dashboard(request):
    user_reservations = Reservation.objects.filter(user=request.user)
    user_borrowings = Borrowing.objects.filter(user=request.user)
    user_fines = Fine.objects.filter(user=request.user)
    user_wishlist = WishList.objects.filter(user=request.user)

    return render(request, 'user_dashboard.html', {
        'user_reservations': user_reservations,
        'user_borrowings': user_borrowings,
        'user_fines': user_fines,
        'user_wishlist': user_wishlist,
    })
