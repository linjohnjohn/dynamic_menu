from django.db import models

# Create your models here.

class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return None

class Item(models.Model):
    name = models.CharField(max_length=200)
    second_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(blank=True)
    category = models.ForeignKey(to=Category, on_delete=models.SET_NULL, null=True, related_name='items')
    ingredients = models.ManyToManyField(to=Ingredient, blank=True)

    def __str__(self):
        return self.name
    
    @property
    def available(self):
        ingredients = self.ingredients.all()
        for i in ingredients:
            if i.available is False:
                return False
        return True

    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return ''

class Variant(models.Model):
    name = models.CharField(max_length=200)
    internal_name = models.CharField(max_length=200)
    markup = models.DecimalField(max_digits=10, decimal_places=2)
    item = models.ManyToManyField(to=Item, blank=True, related_name='variants')
    ingredients = models.ManyToManyField(to=Ingredient, blank=True)
    
    def __str__(self):
        return self.internal_name

    @property
    def available(self):
        ingredients = self.ingredients.all()
        for i in ingredients:
            if i.available is False:
                return False
        return True

class Modifier(models.Model):
    name = models.CharField(max_length=200)
    internal_name = models.CharField(max_length=200)
    markup = models.DecimalField(max_digits=10, decimal_places=2)
    item = models.ManyToManyField(to=Item, blank=True, related_name="modifiers")
    ingredients = models.ManyToManyField(to=Ingredient, blank=True)

    def __str__(self):
        return self.internal_name