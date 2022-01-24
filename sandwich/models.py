from django.db import models

class Sandwich(models.Model):
    bread   = models.ForeignKey('Bread', on_delete=models.CASCADE)
    topping = models.ForeignKey('Topping', on_delete=models.CASCADE)
    cheese  = models.ForeignKey('Cheese', on_delete=models.CASCADE)
    source  = models.ForeignKey('Source', on_delete=models.CASCADE)

    class Meta:
        db_table = 'sandwiches'

class Bread(models.Model):
    name          = models.CharField(max_length=30)
    quantity_left = models.PositiveIntegerField(default=0)
    price         = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'breads'

class Topping(models.Model):
    name          = models.CharField(max_length=30)
    quantity_left = models.PositiveIntegerField(default=0)
    price         = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'toppings'

class Cheese(models.Model):
    name          = models.CharField(max_length=30)
    quantity_left = models.PositiveIntegerField(default=0)
    price         = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'cheeses'

class Source(models.Model):
    name          = models.CharField(max_length=30)
    quantity_left = models.PositiveIntegerField(default=0)
    price         = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'sources'