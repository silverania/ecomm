from django.db import models
from django.urls import reverse
# Create your models here.
from user.models import Profile


class Manager(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200,
                            unique=True)

    def __str__(self):
        return self.name


class List(models.Model):
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])


class Category(models.Model):
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
    manager = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        related_name="products",
        null=True,
        blank=True,
    )
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


class Order(models.Model):
    nome = models.CharField(max_length=50)
    cognome = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    via = models.CharField(max_length=250)
    postal = models.CharField(max_length=20)
    città = models.CharField(max_length=100)
    creato = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    pagato = models.BooleanField(default=False, blank=True, null=True)
    prodotto = models.ForeignKey(
        Product, on_delete=models.CASCADE, blank=True, null=True)
    infovarie = models.CharField(max_length=2000,  blank=True, null=True)

    class Meta:
        ordering = ('-creato',)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)


def __str__(self):
    return str(self.id)


def get_cost(self):
    return self.price * self.quantity
