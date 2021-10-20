# Create your views here.
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


from .models import Product, Order, OrderItem
from .serializers import ProductSerializer, OrderSerializer



class SimpleApi(APIView):
    """ This will receive the data and sends the response"""

    product_serializer_class = ProductSerializer
    order_serializer_class = OrderSerializer

    def get(self, request):
        """ This will be executed when get request is made """
        return Response('hello')

    def post(self, request):
        """ This will post the data to database after validation"""
        serializer = self.order_serializer_class(data=request.data)
        orders = list()
        errors = list()
        not_available = None
        # check whether the order we received from marketplace is valid or not
        if serializer.is_valid():
            order = Order.objects.create(order_id=serializer.validated_data['order_id'],
                                         source=serializer.validated_data['source'])
            order.save()
            for product in request.data['lines']:
                # check whether the products inside the order or valid or not
                serializer = self.product_serializer_class(data=product)

                if serializer.is_valid():
                    if Product.objects.filter(product_name=serializer.validated_data['product']).exists() and Product.objects.get(product_name=serializer.validated_data['product']).is_available():
                        # process the product as a order_item if it passes all validations
                        p = Product.objects.get(product_name=serializer.validated_data['product'])
                        order_item = OrderItem.objects.create(product=p, order=order,
                                                              quantity=serializer.validated_data['quantity'])

                        # reduce the stock if it is a valid product
                        p.stock = p.stock - serializer.validated_data['quantity']
                        p.save()
                        orders.append(product)
                    elif not Product.objects.filter(product_name=serializer.validated_data['product']).exists():
                        # if the product does not exists in our warehouse
                        errors.append('Requested product does not exists')
                    else:
                        # return 422 error if the product is out of stock
                        not_available = status.HTTP_422_UNPROCESSABLE_ENTITY
                else:
                    # return all the errors if any
                    errors.append(serializer.errors)
            return Response({'orders': orders, 'errors': errors, 'status': not_available if not_available else status.HTTP_400_BAD_REQUEST})
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)