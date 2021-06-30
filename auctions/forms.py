from django.forms import ModelForm
from django import forms 
from .models import Item, CommentItem, BidItem

# Create the form class.
class createItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'

class updateItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields ="__all__"
        exclude = ['date_published', "publisher"]

class commentForm(forms.ModelForm):
    class Meta:
        model = CommentItem
        fields = "__all__"
        exclude = ["item", "comment_date", "commentor"]
class bidForm(forms.ModelForm):
    class Meta:
        model = BidItem
        fields = ["newbid"]
