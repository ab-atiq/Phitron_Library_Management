from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    GENRE_CHOICES = [
        ('Fiction', 'Fiction'),
        ('Non-Fiction', 'Non-Fiction'),
        ('Science Fiction', 'Science Fiction'),
        ('Fantasy', 'Fantasy'),
        ('Mystery', 'Mystery'),
        ('Thriller', 'Thriller'),
        ('Romance', 'Romance'),
        ('Westerns', 'Westerns'),
    ]
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField()
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    no_of_books_available = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reserved_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"


class Borrowing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"


class Fine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fine_amount = models.DecimalField(max_digits=8, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}"


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
