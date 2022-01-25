import json

from django.views import View
from django.http import JsonResponse

from .models import *


class BreadView(View):
    def get(self, request):
        breads = Bread.objects.all()

        Result = [{
            "name"          : bread.name,
            "quantity_left" : bread.quantity_left,
            "price"         : bread.price
        }for bread in breads]

        return JsonResponse({"Result":Result}, status=200)

    def post(self, request):
        data     = json.loads(request.body)
        name     = data['name']
        quantity = data['quantity']
        price    = data['price']
        bread    = Bread.objects.filter(name=name)

        if not bread.exists():
            Bread.objects.create(
                name = name,
                quantity_left=quantity,
                price=price
            )
            return JsonResponse({"MESSAGE":"SUCCESS"}, status=201)

        count = Bread.objects.get(name=name)
        count.quantity_left += quantity
        count.save()   

        return JsonResponse({"MESSAGE":"SUCCESS"}, status=201)
    
    def put(self, request):
        data     = json.loads(request.body)
        name     = data['name']
        quantity = data['quantity']
        price    = data['price']
        bread    = Bread.objects.filter(name=name)
        if not bread.exists():
            return JsonResponse({"MESSAGE":"BREAD_DOES_NOT_EXIST"}, status=404)
        
        bread.update(name=name, quantity_left=quantity, price=price)
        return JsonResponse({"MESSAGE":"SUCCESS"}, status=201)

    def delete(self, request):
        try:
            name  = request.GET.get("name")
            bread = Bread.objects.get(name=name)
            bread.delete()

            return JsonResponse({"MESSAGE":"DELETE"}, status=204)
        
        except Bread.DoesNotExist:
            return JsonResponse({"MESSAGE":"BREAD_DOES_NOT_EXIST"}, status=404)

class ToppingView(View):
    def get(self, request):
        toppings = Topping.objects.all()

        Result = [{
            "name"          : topping.name,
            "quantity_left" : topping.quantity_left,
            "price"         : topping.price
        }for topping in toppings]

        return JsonResponse({"Result":Result}, status=200)

    def post(self, request):
        data     = json.loads(request.body)
        name     = data['name']
        quantity = data['quantity']
        price    = data['price']
        topping  = Topping().objects.filter(name=name)

        if not bread.exists():
            topping.objects.create(
                name = name,
                quantity_left=quantity,
                price=price
            )
            return JsonResponse({"MESSAGE":"SUCCESS"}, status=201)

        count = Topping.objects.get(name=name)
        count.quantity_left += quantity
        count.save()   

        return JsonResponse({"MESSAGE":"SUCCESS"}, status=201)
    
    def put(self, request):
        data     = json.loads(request.body)
        name     = data['name']
        quantity = data['quantity']
        price    = data['price']
        topping    = Topping.objects.filter(name=name)
        if not topping.exists():
            return JsonResponse({"MESSAGE":"TOPPING_DOES_NOT_EXIST"}, status=404)
        
        topping.update(name=name, quantity_left=quantity, price=price)
        return JsonResponse({"MESSAGE":"SUCCESS"}, status=201)

    def delete(self, request):
        try:
            name  = request.GET.get("name")
            topping = Topping.objects.get(name=name)
            topping.delete()

            return JsonResponse({"MESSAGE":"DELETE"}, status=204)
        
        except Topping.DoesNotExist:
            return JsonResponse({"MESSAGE":"TOPPING_DOES_NOT_EXIST"}, status=404)

class CheeseView(View):
    def get(self, request):
        cheeses = Cheese.objects.all()

        Result = [{
            "name"          : cheese.name,
            "quantity_left" : cheese.quantity_left,
            "price"         : cheese.price
        }for cheese in cheeses]

        return JsonResponse({"Result":Result}, status=200)

    def post(self, request):
        data     = json.loads(request.body)
        name     = data['name']
        quantity = data['quantity']
        price    = data['price']
        cheese   = Cheese.objects.filter(name=name)

        if not cheese.exists():
            Cheese.objects.create(
                name = name,
                quantity_left=quantity,
                price=price
            )
            return JsonResponse({"MESSAGE":"SUCCESS"}, status=201)

        count = Cheese.objects.get(name=name)
        count.quantity_left += quantity
        count.save()   

        return JsonResponse({"MESSAGE":"SUCCESS"}, status=201)
    
    def put(self, request):
        data     = json.loads(request.body)
        name     = data['name']
        quantity = data['quantity']
        price    = data['price']
        cheese   = Cheese.objects.filter(name=name)
        if not bread.exists():
            return JsonResponse({"MESSAGE":"CHEESE_DOES_NOT_EXIST"}, status=404)
        
        cheese.update(name=name, quantity_left=quantity, price=price)
        return JsonResponse({"MESSAGE":"SUCCESS"}, status=201)

    def delete(self, request):
        try:
            name   = request.GET.get("name")
            cheese = Cheese.objects.get(name=name)
            cheese.delete()

            return JsonResponse({"MESSAGE":"DELETE"}, status=204)
        
        except Cheese.DoesNotExist:
            return JsonResponse({"MESSAGE":"CHEESE_DOES_NOT_EXIST"}, status=404)

class SourceView(View):
    def get(self, request):
        sources = Source.objects.all()

        Result = [{
            "name"          : source.name,
            "quantity_left" : source.quantity_left,
            "price"         : source.price
        }for source in sources]

        return JsonResponse({"Result":Result}, status=200)

    def post(self, request):
        data     = json.loads(request.body)
        name     = data['name']
        quantity = data['quantity']
        price    = data['price']
        source   = Source.objects.filter(name=name)

        if not source.exists():
            Source.objects.create(
                name = name,
                quantity_left=quantity,
                price=price
            )
            return JsonResponse({"MESSAGE":"SUCCESS"}, status=201)

        count = Source.objects.get(name=name)
        count.quantity_left += quantity
        count.save()   

        return JsonResponse({"MESSAGE":"SUCCESS"}, status=201)
    
    def put(self, request):
        data     = json.loads(request.body)
        name     = data['name']
        quantity = data['quantity']
        price    = data['price']
        source   = Source.objects.filter(name=name)
        if not source.exists():
            return JsonResponse({"MESSAGE":"SOURCE_DOES_NOT_EXIST"}, status=404)
        
        source.update(name=name, quantity_left=quantity, price=price)
        return JsonResponse({"MESSAGE":"SUCCESS"}, status=201)

    def delete(self, request):
        try:
            name   = request.GET.get("name")
            source = Source.objects.get(name=name)
            source.delete()

            return JsonResponse({"MESSAGE":"DELETE"}, status=204)
        
        except Source.DoesNotExist:
            return JsonResponse({"MESSAGE":"SOURCE_DOES_NOT_EXIST"}, status=404)