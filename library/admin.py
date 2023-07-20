from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db.models import Sum

from . import models
from .models import Fine


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'no_of_books_available')
    list_editable = ('no_of_books_available',)


# unregister the Group model from admin.
admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'total_fine')
    list_editable = ('is_staff', 'is_active')
    ordering = ('username',)
    search_fields = ('username', 'email', 'first_name', 'last_name')

    def total_fine(self, obj):
        return Fine.objects.filter(user=obj).aggregate(total_fine=Sum('fine_amount'))['total_fine'] or 0


admin.site.register(models.Borrowing)
admin.site.register(models.Fine)
admin.site.register(models.Reservation)
