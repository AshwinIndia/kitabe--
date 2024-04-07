from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from mainapp.helpers import is_bookid_invalid, is_rating_invalid, get_rated_bookids
import BookRecSystem.settings as settings
from mainapp.models import UserRating, SaveForLater
from bs4 import BeautifulSoup
import pandas as pd
import os
import json
import requests

"""
    Production File Path :  staticfiles_storage.url(file)
    Developement File Path : settings.STATICFILES_DIRS[0] + 'app/.../file'
"""
book_path = os.path.join(settings.STATICFILES_DIRS[0] + "/mainapp/dataset/books.csv")
user_ratings_path = os.path.join(
    settings.STATICFILES_DIRS[0] + "/mainapp/csv/userratings.csv"
)


def is_ajax(request):
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


def search(request):
    """
    AJAX request for search bar functionality
    """
    if request.method == "POST" and is_ajax(request=request):
        query = request.POST.get("bookName", None)
        if not query:
            return JsonResponse({"success": False}, status=200)
        df_book = pd.read_csv(book_path)
        top5_result = df_book[
            df_book["original_title"].str.contains(query, regex=False, case=False)
        ][:5]
        top5_result = json.dumps(top5_result.to_dict("records"))

        return JsonResponse({"success": True, "top5_result": top5_result}, status=200)


def book_summary(request):
    """
    AJAX request for book summary
    """
    if request.method == "POST" and is_ajax(request=request):
        bookid = request.POST.get("bookid", None)
        if is_bookid_invalid(bookid):
            return JsonResponse({"success": False}, status=200)
        URL = "https://www.goodreads.com/book/show/" + bookid
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        div_container = soup.find(id="description")
        full_book_summary = ""
        if not div_container:
            return JsonResponse({"success": False}, status=200)
        for spantag in div_container.find_all("span"):
            try:
                # When text is too long, consider till last complete sentence
                full_book_summary += spantag.text[: spantag.text.rindex(".")] + ". "
            except ValueError:
                full_book_summary += spantag.text + " "
            break
        part_summary = " ".join(full_book_summary.split()[:65]) + " . . ."
        return JsonResponse({"success": True, "booksummary": part_summary}, status=200)


def get_book_details(request):
    """
    AJAX request for book details
    """
    if request.method == "POST" and is_ajax(request=request):
        bookid = request.POST.get("bookid", None)
        if is_bookid_invalid(bookid):
            return JsonResponse({"success": False}, status=200)

        df_book = pd.read_csv(book_path)
        book_details = df_book[df_book["book_id"] == int(bookid)]
        if not len(book_details):
            return JsonResponse({"success": False}, status=200)

        book_details = json.dumps(book_details.to_dict("records"))
        return JsonResponse({"success": True, "book_details": book_details}, status=200)


@login_required
def user_rate_book(request):
    """
    AJAX request when user rates book
    """
    if request.method == "POST" and is_ajax(request=request):
        bookid = request.POST.get("bookid", None)
        bookrating = request.POST.get("bookrating", None)
        if is_bookid_invalid(bookid) or is_rating_invalid(bookrating):
            return JsonResponse({"success": False}, status=200)

        # Using Inbuilt Model
        query = UserRating.objects.filter(user=request.user).filter(bookid=bookid)
        if not query:
            # Create Rating
            UserRating.objects.create(
                user=request.user, bookid=bookid, bookrating=bookrating
            )
        else:
            # Update Rating
            rating_object = query[0]
            rating_object.bookrating = bookrating
            rating_object.save()
        return JsonResponse({"success": True}, status=200)


def save_book(request):
    """AJAX request when user saves book"""
    if request.method == "POST" and is_ajax(request=request):
        bookid = request.POST.get("bookid", None)
        user_ratings = list(UserRating.objects.filter(user=request.user))
        rated_books = set(get_rated_bookids(user_ratings))
        if is_bookid_invalid(bookid) or bookid in rated_books:
            return JsonResponse({"success": False}, status=200)

        SaveForLater.objects.create(user=request.user, bookid=bookid)
        return JsonResponse({"success": True}, status=200)


def remove_saved_book(request):
    """AJAX request when user removes book"""
    if request.method == "POST" and is_ajax(request=request):
        bookid = request.POST.get("bookid", None)
        if is_bookid_invalid(bookid):
            return JsonResponse({"success": False}, status=200)

        saved_book = SaveForLater.objects.filter(user=request.user, bookid=bookid)
        saved_book.delete()
        return JsonResponse({"success": True}, status=200)

#CHANGED----------CHANGED-----------CHANGED
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from mainapp.models import CartItem, Order, OrderItem
from mainapp.forms import CheckoutForm

@login_required
def add_to_cart(request):
    if request.method == "POST" and is_ajax(request=request):
        book_id = request.POST.get("book_id")
        # Add the book to the user's cart
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            book_id=book_id,
            defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})

@login_required
def get_cart_items(request):
    if request.method == "GET" and is_ajax(request=request):
        cart_items = CartItem.objects.filter(user=request.user)
        cart_data = [
            {
                'book_id': item.book_id,
                'quantity': item.quantity,
                # Add other necessary fields
            }
            for item in cart_items
        ]
        return JsonResponse({"success": True, "cart_data": cart_data})
    return JsonResponse({"success": False})

@login_required
def update_cart_item(request, item_id):
    if request.method == "POST" and is_ajax(request=request):
        quantity = request.POST.get("quantity")
        try:
            cart_item = CartItem.objects.get(id=item_id, user=request.user)
            cart_item.quantity = quantity
            cart_item.save()
            return JsonResponse({"success": True})
        except CartItem.DoesNotExist:
            return JsonResponse({"success": False})

@login_required
def remove_from_cart(request, item_id):
    if request.method == "POST" and is_ajax(request=request):
        try:
            cart_item = CartItem.objects.get(id=item_id, user=request.user)
            cart_item.delete()
            return JsonResponse({"success": True})
        except CartItem.DoesNotExist:
            return JsonResponse({"success": False})

@login_required
def checkout(request):
    if request.method == "POST" and is_ajax(request=request):
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Process the form data
            # Create an order and order items based on the cart items
            cart_items = CartItem.objects.filter(user=request.user)
            order = Order.objects.create(user=request.user)
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    book_id=cart_item.book_id,
                    quantity=cart_item.quantity
                )
            # Clear the user's cart
            cart_items.delete()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    return JsonResponse({"success": False})