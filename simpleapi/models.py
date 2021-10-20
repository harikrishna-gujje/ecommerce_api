from django.db import models


# Create your models here.
class Order(models.Model):
    """ model for order"""
    source_choices = [('amazon', 'amazon'), ('flipkart', 'flipkart'), ('jiomart', 'jiomart')]
    order_id = models.IntegerField()
    source = models.CharField(max_length=255, choices=source_choices)

    objects = models.Manager()

    def __str__(self):
        return self.source


class Product(models.Model):
    """Product model"""
    product_name = models.CharField(max_length=255)
    stock = models.IntegerField()

    objects = models.Manager()

    def is_available(self):
        """ checks whether the product is available or not"""
        if self.serializable_value(field_name='stock') > 0:
            return True
        return False

    def __str__(self):
        return self.product_name


class OrderItem(models.Model):
    """ order item model """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    objects = models.Manager()
