from django.db import models
from django.urls import reverse
# Create your models here.


class Manager(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200,
                            unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    manager = models.ManyToManyField(Manager)
    name = models.CharField(max_length=200,
                            db_index=True)
    slug = models.SlugField(max_length=200,
                            unique=True)
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    '''def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])'''


class Product(models.Model):
    manager = models.ManyToManyField(Manager)
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    rootLink = models.URLField(null=True, blank=True)
    quantity = models.IntegerField()
    photo = models.ImageField(upload_to="products", default="")
    consegna = models.PositiveIntegerField()
    disponibile = models.BooleanField()
    idapi = models.CharField(max_length=200, db_index=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name
    """
    def get_absolute_url(self):
        return reverse('product_detail',
                       args=[self.slug])
    """
