from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

class ExpertQuerySet(models.QuerySet):
    def search(self, query, place):
        lookup = (
            Q(firstname__icontains=query) |
            Q(lastname__icontains=query) |
            Q(practices__name__icontains=query) |
            Q(city__icontains=place) |
            Q(country__icontains=place) |
            Q(district__icontains=place) |
            Q(province__icontains=place)
        )
        return self.filter(lookup)

class ExpertManager(models.Manager):
    def get_queryset(self):
        return ExpertQuerySet(self.model, using=self._db)

    def search(self, query=None, place=None):
        if query is None and place is None:
            return self.get_queryset().none()
        return self.get_queryset().search(query, place)


class OfficeQuerySet(models.QuerySet):
    def search(self, query, place):
        lookup = (
            Q(name__icontains=query) |
            Q(practices__name__icontains=query) |
            Q(city__icontains=place) |
            Q(country__icontains=place) |
            Q(district__icontains=place) |
            Q(province__icontains=place)
        )
        return self.filter(lookup)

class OfficeManager(models.Manager):
    def get_queryset(self):
        return OfficeQuerySet(self.model, using=self._db)

    def search(self, query=None, place=None):
        if query is None and place is None:
            return self.get_queryset().none()
        return self.get_queryset().search(query, place)



class Practice(models.Model):
    name = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.name


class Firm(models.Model):
    user        = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    offices     = models.ManyToManyField("Office", related_name='offices', blank=True)
    name        = models.CharField(max_length=120)
    logo        = models.ImageField(default="default.png", null=True, blank=True)
    updated     = models.DateTimeField(auto_now_add=True)
    timestamp   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Office(models.Model):
    name        = models.CharField(max_length=120)
    slug        = models.SlugField(unique=True)
    firm        = models.ForeignKey("Firm", null=True, related_name='firm', on_delete=models.SET_NULL)
    experts     = models.ManyToManyField("Expert", related_name='experts', blank=True)
    practices   = models.ManyToManyField("Practice", related_name='office_practices', blank=True)
    city        = models.CharField(max_length=120, null=True)
    country     = models.CharField(max_length=120, null=True)
    district    = models.CharField(max_length=120, null=True)
    province    = models.CharField(max_length=120, null=True)
    logo        = models.ImageField(default="default.png", null=True, blank=True)
    updated     = models.DateTimeField(auto_now_add=True)
    timestamp   = models.DateTimeField(auto_now=True)

    objects = OfficeManager()

    def __str__(self):
        return f"{self.name} - {self.firm.name}"

    def get_absolute_url(self):
        return f"/bureau/{self.slug}"

    class Meta:
        ordering = ["-name", "-firm__name", "-timestamp"]


class Expert(models.Model):
    # STATUS = (
    #     ('Pending', 'Pending'),
    #     ('Out for delivery', 'Out for delivery'),
    #     ('Delivery', 'Delivery'),
    # )
    # status          = models.CharField(max_length=200, null=True, choices=STATUS)
    office          = models.ForeignKey("Office", null=True, related_name='office', on_delete=models.SET_NULL)
    user            = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    firstname       = models.CharField(max_length=30, blank=False, null=False)
    lastname        = models.CharField(max_length=30, blank=False, null=False)
    about           = models.TextField(blank=True, null=True) 
    slug            = models.SlugField(unique=True, blank=False, null=False)
    email           = models.EmailField(blank=False, null=False)
    phone_number    = models.CharField(max_length=15 ,blank=True, null=True)
    price           = models.FloatField(blank=True, null=True)
    currency        = models.CharField(max_length=10, blank=True, null=True)
    practices       = models.ManyToManyField("Practice", related_name='expert_practices', blank=True)
    city            = models.CharField(max_length=120, null=True)
    country         = models.CharField(max_length=120, null=True)
    district        = models.CharField(max_length=120, null=True)
    province        = models.CharField(max_length=120, null=True)
    avatar          = models.ImageField(default="default.png", null=True, blank=True)
    updated         = models.DateTimeField(auto_now_add=True)
    timestamp       = models.DateTimeField(auto_now=True)

    objects = ExpertManager()

    def __str__(self):
        return self.firstname + ' ' + self.lastname

    def get_absolute_url(self):
        return f"/expert/{self.slug}"

    class Meta:
        ordering = ["-firstname", "-lastname", "-timestamp"]


class Profile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, null=False)
    first_name  = models.CharField(max_length=200, null=True, blank=True)
    last_name   = models.CharField(max_length=200, null=True, blank=True)
    phone       = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.user)

