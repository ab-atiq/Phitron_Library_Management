from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils import timezone

from library.models import Book, Reservation, Borrowing, Fine, WishList


def book_search(request):
    query = request.GET.get('query') or ''
    query = Q(title__icontains=query) | Q(author__icontains=query) | Q(isbn__icontains=query) | Q(genre__icontains=query)
    books = Book.objects.filter(query)
    return render(request, 'book_search.html', {'books': books, 'query': request.GET.get('query', '')})


@login_required
def book_reservation(request, book_id):
    book = Book.objects.get(pk=book_id)
    if book.no_of_books_available < 1:
        return render(request, 'reservation_error.html', {'message': 'Book not available for reservation'})
    if Reservation.objects.filter(user=request.user, book=book).exists():
        return render(request, 'reservation_error.html', {'message': 'Book already reserved'})
    Reservation.objects.create(user=request.user, book=book)
    book.no_of_books_available -= 1
    book.save()
    return render(request, 'reservation_success.html', {'book': book})


@login_required
def borrow_book(request, book_id):
    book = Book.objects.get(pk=book_id)
    if book.no_of_books_available < 1:
        return redirect('book_search')

    due_date = timezone.now() + timezone.timedelta(days=14)
    Borrowing.objects.create(user=request.user, book=book, due_date=due_date)

    book.no_of_books_available -= 1
    book.save()

    return render(request, 'borrow_success.html', {'book': book, 'due_date': due_date})


@login_required
def return_book(request, borrowing_id):
    borrowing = Borrowing.objects.get(pk=borrowing_id)
    book = borrowing.book

    if borrowing.user != request.user:
        return redirect('user_dashboard')

    if borrowing.due_date < timezone.now().date():
        days_late = (timezone.now().date() - borrowing.due_date).days
        fine_amount = days_late * 2.5
        fine_amount = min(fine_amount, 100)
        Fine.objects.create(user=request.user, fine_amount=fine_amount)

    book.no_of_books_available += 1
    book.save()
    borrowing.delete()
    # Send email to user who reserve that book
    for reserve in Reservation.objects.filter(book=book):
        reserved_user = reserve.user
        send_mail(
            'Book available',
            f'The book {book.title} you reserved for is now available for borrowing',
            settings.EMAIL_HOST_USER,
            [reserved_user.email])
    return redirect('user_dashboard')


@login_required
def add_to_wishlist(request, book_id):
    if not WishList.objects.filter(user=request.user, book_id=book_id).exists():
        book = Book.objects.get(pk=book_id)
        WishList.objects.create(user=request.user, book=book)
    return redirect('user_dashboard')
