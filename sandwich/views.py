import json

from django.views import View
from django.http import JsonResponse

from .models import *

class SandwichView(View):
    def post(self, request):
        try:
            data    = json.loads(request.body)
            bread   = data['bread']
            topping = data['topping']
            cheese  = data['cheese']
            source  = data['source']

            bread   = Bread.objects.get(name=bread)
            topping = Topping.objects.get(name=topping)
            cheese  = Cheese.objects.get(name=cheese)
            source  = Source.objects.get(name=source)

            if bread.quantity_left == 0:
                return JsonResponse({"MESSAGE" : "BREAD_QUANTITY_DOES_NOT_EXIST"}, status=404)
            if topping.quantity_left == 0:
                return JsonResponse({"MESSAGE" : "TOPPING_QUANTITY_DOES_NOT_EXIST"}, status=404)
            if cheese.quantity_left == 0:
                return JsonResponse({"MESSAGE" : "CHEESE_QUANTITY_DOES_NOT_EXIST"}, status=404)
            if source.quantity_left == 0:
                return JsonResponse({"MESSAGE" : "SOURCE_QUANTITY_DOES_NOT_EXIST"}, status=404)
        
            Sandwich.objects.create(
                bread_id   = bread.id,
                topping_id = topping.id,
                cheese_id  = cheese.id,
                source_id  = source.id 
            )
            
            bread.quantity_left -= 1
            bread.save()
            topping.quantity_left -= 1
            topping.save()
            cheese.quantity_left -= 1
            cheese.save()
            source.quantity_left -= 1
            source.save()
            return JsonResponse({"MESSAGE" : "SUCCESS"}, status=201)     

        except Bread.DoesNotExist:
            return JsonResponse({"MESSAGE" : "BREAD_DOES_NOT_EXIST"}, status=404)
        except Topping.DoesNotExist:
            return JsonResponse({"MESSAGE" : "TOPPING_DOES_NOT_EXIST"}, status=404)
        except Cheese.DoesNotExist:
            return JsonResponse({"MESSAGE" : "CHEESE_DOES_NOT_EXIST"}, status=404)
        except Source.DoesNotExist:
            return JsonResponse({"MESSAGE" : "SOURCE_DOES_NOT_EXIST"}, status=404)

        except KeyError:
            return JsonResponse({"MESSAGE" : "KEY_ERROR"}, status=400)        

    def get(self, request):
        try:
            number         = request.GET.get("number")
            bread_search   = request.GET.get("bread_name")
            topping_search = request.GET.get("topping_name")
            cheese_search  = request.GET.get("cheese_name")
            source_search  = request.GET.get("source_name")
            OFFSET         = int(request.GET.get("offset", 0))
            LIMIT          = int(request.GET.get("limit", 10))
            sandwiches     = Sandwich.objects.all()

            if number:
                sandwich = sandwiches.get(id=number)
                Result = {
                    "bread"   : sandwich.bread.name,
                    "topping" : sandwich.topping.name,
                    "cheese"  : sandwich.cheese.name,
                    "source"  : sandwich.source.name,
                    "price"   : sandwich.bread.price + sandwich.topping.price + sandwich.cheese.price + sandwich.source.price
                }

            if bread_search:
                sandwiches = sandwiches.filter(bread__name__contains=bread_search)
            if topping_search:
                sandwiches = sandwiches.filter(topping__name__contains=topping_search)
            if cheese_search:
                sandwiches = sandwiches.filter(cheese__name__contains=cheese_search)
            if source_search:
                sandwiches = sandwiches.filter(source__name__contains=source_search)
            
            sandwiches = sandwiches[OFFSET:OFFSET+LIMIT]

            Result = [{
                    "id"      : sandwich.id,
                    "bread"   : sandwich.bread.name,
                    "topping" : sandwich.topping.name,
                    "cheese"  : sandwich.cheese.name,
                    "source"  : sandwich.source.name,
                    "price"   : sandwich.bread.price + sandwich.topping.price + sandwich.cheese.price + sandwich.source.price
                }for sandwich in sandwiches]
            
            return JsonResponse({"Result":Result}, status=200)
        except Sandwich.DoesNotExist:
            return JsonResponse({"MESSAGE":"SANDWICH_DOES_NOT_EXIST"}, status=404)

    def delete(self, request):
        try:
            number   = request.GET.get("number")
            sandwich = Sandwich.objects.get(id=number)
            sandwich.delete()
            bread = sandwich.bread
            bread.quantity_left += 1
            bread.save()
            topping = sandwich.topping
            topping.quantity_left += 1
            topping.save()
            cheese = sandwich.cheese
            cheese.quantity_left += 1
            cheese.save()
            source = sandwich.source
            source.quantity_left += 1
            source.save()

            return JsonResponse({"MESSAGE":"DELETE"}, status=204)
        
        except Bread.DoesNotExist:
            return JsonResponse({"MESSAGE":"SANDWICH_DOES_NOT_EXIST"}, status=404)

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