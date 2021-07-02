from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from django.views.generic import ListView,CreateView
from .models import User,Item,CommentItem, BidItem, WatchList,Category, Profile
from .forms import createItemForm, updateItemForm,commentForm, bidForm
from django.contrib import messages


class ItemListView(ListView):
    model = Item
    template_name = "auctions/items_list.html"

def ItemDetail(request, pk):
    added = False
    is_active = True
    item = Item.objects.get(id=pk)
    update_form = updateItemForm(instance=item)
    comment_form = commentForm(instance=item)
    bid_form = bidForm(instance=item) 
    currentUser = WatchList.objects.filter(watching_item=item, watcher= request.user)
    if(currentUser):
        added= True
    context ={
    "added":added,    
    "item":item,    
    "update_form":update_form,
    "comment_form":comment_form,
    "bid_form":bid_form
    }
    return render(request, "auctions/items_detail.html", context)


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("item-list"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("item-list"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("item-list"))
    else:
        return render(request, "auctions/register.html")


class CreateItem(CreateView):
    model = Item
    template_name = 'auctions/items_create.html'
    fields = ['title','description','category','starting_bid', 'image']
    template_name = "auctions/items_create.html"
    success_url = "/"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    
def update(request,pk):
    item = Item.objects.get(id=pk)
    if request.method == "POST":
        update_form = updateItemForm(request.POST, request.FILES, instance=item)
        if update_form.is_valid():
            update_form.save()
            messages.success(request, "The item has been updated.")
            context={"messages":messages}
            return redirect(f"/{pk}", context)
        else:
            messages.warning(request, "Form validation failed.")
            return redirect (f"/{pk}")
    else:
        update_form = updateItemForm(instance=item)
        return redirect("/")

def comment(request, pk):
    item = Item.objects.get(id=pk)
    if request.method == "POST":
        comment_form = commentForm(request.POST)
        if comment_form.is_valid:
            comment = request.POST.get("comment")
            Comment = CommentItem.objects.create(comment = comment, commentor = request.user, item = item)
            Comment.save()
            messages.success(request, "Comment has been added successfully.")
            return redirect(f"/{pk}")
        else:
            messages.warning(request, "Form validation has failed.")
            return redirect(f"/{pk}")
    else:
            messages.warning(request, "You should submit the form!")
            return redirect(f"/{pk}")


def bid(request,pk):
    item = Item.objects.get(id = pk)
    bid_form = bidForm(request.POST, instance=item)
    if request.method == "POST":
        bid_form = bidForm(request.POST, instance=item)
        if bid_form.is_valid:
            bidoffered = request.POST.get("newbid")
            if int(item.starting_bid) >= int(bidoffered):
                messages.warning(request,"Your bid should be higher than the current!")
                return redirect(f"/{pk}")
            else:
                item.starting_bid = bidoffered    
                bid = BidItem.objects.create(newbid= bidoffered, bid_maker = request.user, item=item)
                bid.save()
                item.save()
                messages.success(request, "Your bid saved succesfully! ")
                return redirect(f"/{pk}")
        else:
            return HttpResponse("comment validation failed.")
    else:
        bidoffered = request.POST.get("newbid")
        item.starting_bid = bidoffered    
        return HttpResponse(str(bidoffered) + " , "+ str(item.starting_bid))


def show_watchlist(request):
    user = request.user
    item_list = WatchList.objects.filter(watcher = user)
    context ={
    "item_list":item_list,
    }
    return render(request, "auctions/watchlist.html", context)


def add_watchlist(request,pk):
    if request.method == "POST":
        item = Item.objects.get(id = pk)
        user = request.user
        NewWatch = WatchList.objects.create(watcher = user, watching_item = item)
        NewWatch.save()
        return redirect("show-watchlist")
 
def rem_watchlist(request,pk):
    if request.method == "POST":
        item = Item.objects.get(id=pk)
        WatchList.objects.filter(watcher=request.user, watching_item = item).delete()
        added = True
        context = {
            "added":added,
        }
        return redirect(f"item-list")

def list_categories(request):
    categories = Category.objects.filter(parent=None)
    context = {
        "categories":categories
    }
    return render(request, "auctions/listcategories.html", context)

def categorydetail(request,pk):
    category = Category.objects.get(id = pk)
    item_list = Item.objects.filter(category = category)
    
    context = {
        "category":category,
        "item_list":item_list,
    }
    return render(request, "auctions/category_detail.html", context)

def profile(request):
    return render(request, "auctions/profile.html")