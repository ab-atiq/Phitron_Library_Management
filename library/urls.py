from django.urls import path

from .views import authentication, management, views

urlpatterns = [
    path('', views.home, name='home'),
    path('user/registration/', authentication.user_registration, name='user_registration'),
    path('user/login/', authentication.user_login, name='user_login'),
    path('user/logout/', authentication.user_logout, name='user_logout'),
    path('book/search/', management.book_search, name='book_search'),
    path('book/<int:book_id>/reserve/', management.book_reservation, name='book_reservation'),
    path('book/<int:book_id>/borrow/', management.borrow_book, name='borrow_book'),
    path('borrowing/<int:borrowing_id>/return/', management.return_book, name='return_book'),
    path('user/dashboard/', authentication.user_dashboard, name='user_dashboard'),
    path('book/<int:book_id>/wishlist/', management.add_to_wishlist, name='add_to_wishlist')
]
