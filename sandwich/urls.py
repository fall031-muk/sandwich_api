from django.urls import path
from .views import *

urlpatterns = [
    # path('', QuestionView.as_view()),
    path('/breads', BreadView.as_view()),
    path('/toppings', ToppingView.as_view()),
    path('/cheeses', CheeseView.as_view()),
    path('/sources', SourceView.as_view()),
    path('/sandwiches', SandwichView.as_view()),
]