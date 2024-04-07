from django.urls import path
from mainapp import views, views_ajax

urlpatterns = [
    path("", views.index, name="index"),
    path("genre_books/<genre>", views.genre_books, name="genre_books"),
    path("explore_books/", views.explore_books, name="explore_books"),
    path(
        "book_recommendations/", views.book_recommendations, name="book_recommendations"
    ),
    path("library/rated_books", views.read_books, name="read_books"),
    path("library/saved_books", views.SaveList, name="to_read"),

    #CHANGED---------CHANGED--------CHANGED

    path('checkout/', views.checkout_view, name='checkout'),
    path('thank-you/', views.thank_you_view, name='thank_you'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('place_order/', views.create_order, name='place_order'),
    path('payment/', views.process_payment, name='payment'),
    path('order_history/', views.order_history_view, name='order_history'),
    path('get-cart-items/', views_ajax.get_cart_items, name='get_cart_items'),

    #-----END OF CHANGED-------cls
    

]

# Ajax Views
urlpatterns += [
    path("search_ajax/", views_ajax.search, name="search_ajax"),
    path("book_summary_ajax/", views_ajax.book_summary, name="summary_ajax"),
    path("book_details_ajax/", views_ajax.get_book_details, name="book_details"),
    path("user_rate_book/", views_ajax.user_rate_book, name="user_rate_book"),
    path("save_book/", views_ajax.save_book, name="save_book"),
    path("remove_saved_book/", views_ajax.remove_saved_book, name="remove_saved_book"),
    path("add_to_cart/",views_ajax.add_to_cart, name="add_to_cart"),
    path("get_cart_items/", views_ajax.get_cart_items, name="get_cart_items"),
    path("update_cart_item/<int:item_id>/", views_ajax.update_cart_item, name="update_cart_item"),
    path("remove_from_cart/", views_ajax.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views_ajax.checkout, name="checkout"),    
]
