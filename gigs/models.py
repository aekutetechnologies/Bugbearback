from django.db import models
from django.db.models import Q
from django.db.models.deletion import CASCADE
from buguser.models import User


class GigQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(user__username__icontains=query)
            )
            qs = self.filter(or_lookup).distinct()
        return qs


class GigManager(models.Manager):
    def get_queryset(self):
        return GigQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query)


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Gig(models.Model):
    user = models.ForeignKey(
        User, on_delete=CASCADE, blank=True, related_name="gigs_user"
    )
    name = models.CharField(max_length=90)
    price = models.FloatField(null=True)
    description = models.CharField(max_length=90, null=True)
    quantity = models.IntegerField(default=0)
    image = models.ImageField(upload_to="gigs", null=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(
        Category, blank=True, related_name="gigs_category"
    )

    objects = GigManager()

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name="comments_user")
    gig = models.ForeignKey(Gig, on_delete=CASCADE, related_name="comments_gig")
    body = models.CharField(max_length=255)
    rating = models.IntegerField()
    dateCreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.gig} - {self.user} - {self.rating}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name="orders_user")
    gig = models.ForeignKey(Gig, on_delete=CASCADE, related_name="orders_gig")
    delivered = models.BooleanField(default=False)
    ordered = models.BooleanField(default=False)
    dateCreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.gig} - {self.user}"
