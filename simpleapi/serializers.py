from rest_framework import serializers


class ProductSerializer(serializers.Serializer):
    """ Serializes the Product data """

    product = serializers.CharField()
    quantity = serializers.IntegerField()

    def validate_quantity(self, value):
        """ external validator to check quantity"""
        if not 0 < value < 6:
            raise serializers.ValidationError('quantity must be greater than 0 and less than 5 for product')
        return value


class ChildProductSerializer(serializers.Serializer):
    """ Serializes the child Product data """

    product = serializers.CharField()
    quantity = serializers.IntegerField()


class OrderSerializer(serializers.Serializer):
    """ Serializes the Order data """

    source_choices = [('amazon', 'amazon'), ('flipkart', 'flipkart'), ('jiomart', 'jiomart')]

    source = serializers.ChoiceField(choices=source_choices)
    order_id = serializers.IntegerField()
    lines = serializers.ListSerializer(child=ChildProductSerializer())
