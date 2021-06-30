from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from PIL import Image


class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    img = models.ImageField(default='profile_pics/profile_default.jpg', upload_to = 'profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile' 

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.img.path)
        if img.height > 300 or img.width > 300:
            size = (300,300)
            img.thumbnail(size)
            img.save(self.img.path) 

class Item(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    starting_bid = models.IntegerField()
    image = models.ImageField(default="item_pics/default.jpg", upload_to = 'item_pics')
    publisher = models.ForeignKey(User, on_delete = models.CASCADE)
    date_published = models.DateTimeField(default=now)
    is_active = models.BooleanField(default = True)
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title    

    def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            size = (300,300)
            img.thumbnail(size)
            img.save(self.image.path)

class Category(models.Model):
    name = models.CharField(max_length=150)
    parent = models.ForeignKey('self', blank = True, null = True, on_delete=models.CASCADE)

    def __str__(self):                           
        full_path = [self.name]                  
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])

class CommentItem(models.Model):
    commentor = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    comment = models.TextField()
    comment_date = models.DateTimeField(default=now)
    item = models.ForeignKey(Item, blank= False, on_delete=models.CASCADE, related_name="comments")
    
    class Meta:
        ordering = ['comment_date']

    def __str__(self):
        return 'Comment on {} by {}'.format(self.item, self.commentor)

class WatchList(models.Model):
    watching_item = models.ForeignKey(Item, on_delete = models.CASCADE)
    watcher = models.ForeignKey(User, on_delete = models.CASCADE, default="admin")

    def __str__(self):
        return "{} is in watchlist of {}".format(self.watching_item, self.watcher)


class BidItem(models.Model):
    bid_maker = models.ForeignKey(User, blank= False, on_delete=models.CASCADE)
    newbid = models.IntegerField()
    item = models.ForeignKey(Item, blank=False,on_delete = models.CASCADE, related_name="bids")

    def __str__(self):
        return "Bid for {} by {} is {}".format(self.item, self.bid_maker, self.newbid)