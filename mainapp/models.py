# from django.db import models
# from django.contrib.auth.models import User
# from mainapp.helpers import get_book_title

# import BookRecSystem.settings as settings
# import pandas as pd
# import os

# book_path = os.path.join(settings.STATICFILES_DIRS[0] + "/mainapp/dataset/books.csv")
# df_book = pd.read_csv(book_path)


# class UserRating(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_rating")
#     bookid = models.IntegerField()
#     bookrating = models.IntegerField()

#     def __str__(self):
#         return (
#             self.user.username.capitalize()
#             + "- "
#             + get_book_title(self.bookid)
#             + "  - "
#             + str(self.bookrating)
#         )


# class SaveForLater(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     bookid = models.IntegerField()

#     def __str__(self):
#         return self.user.username.capitalize() + "- " + get_book_title(self.bookid)

from django.db import models
from django.contrib.auth.models import User
from mainapp.helpers import get_book_title

import BookRecSystem.settings as settings
import pandas as pd
import os

book_path = os.path.join(settings.STATICFILES_DIRS[0] + "/mainapp/dataset/books.csv")
df_book = pd.read_csv(book_path)


class UserRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_rating")
    bookid = models.IntegerField()
    bookrating = models.IntegerField()

    def __str__(self):
        return (
            self.user.username.capitalize()
            + "- "
            + get_book_title(self.bookid)
            + "  - "
            + str(self.bookrating)
        )


class SaveForLater(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bookid = models.IntegerField()

    def __str__(self):
        return self.user.username.capitalize() + "- " + get_book_title(self.bookid)

#CHANGED---------------CHANGED----------CHANGED

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bookid = models.IntegerField()
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Add price field

    def __str__(self):
        return (
            f"{self.user.username.capitalize()} - {get_book_title(self.bookid)} - Quantity: {self.quantity}"
        )


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    is_ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"Order for {self.user.username} - Total Amount: {self.total_amount}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    bookid = models.IntegerField()
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Add price field

    def __str__(self):
        return f"Order: {self.order.id} - {get_book_title(self.bookid)} - Quantity: {self.quantity}"


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order: {self.order.id} - Method: {self.payment_method} - Amount Paid: {self.amount_paid}"


class OrderHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order History for {self.user.username} - Order: {self.order.id} - Date: {self.date_ordered}"
