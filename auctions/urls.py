from django.urls import path
from . import views
from auctions.views import ItemListView,login_view, logout_view, register, CreateItem, update, comment, bid, show_watchlist,list_categories,categorydetail, profile



urlpatterns = [
    path("", ItemListView.as_view(), name="item-list"),
    path("<int:pk>", views.ItemDetail, name="item-detail"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.CreateItem.as_view(), name="create"),
    path("update/<int:pk>", views.update, name = "update-item"),
    path("comment/<int:pk>", views.comment, name = "comment-item"),
    path("bid/<int:pk>", views.bid, name = "bid-item"),
    path("watchlist", views.show_watchlist, name = "show-watchlist"),
    path("addwatchlist/<int:pk>", views.add_watchlist, name = "add-watchlist"),
    path("remwatchlist/<int:pk>", views.rem_watchlist, name = "rem-watchlist"),
    path("listcategories", views.list_categories, name = "list-categories"),
    path("category/<int:pk>", views.categorydetail, name = "category-detail"),
    path("profile", views.profile, name = "profile"),
]
