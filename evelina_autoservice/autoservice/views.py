from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.db.models import Q
from django.db.models.query import QuerySet
from django.core.paginator import Paginator
from . models import Order, Service, Car, OrderLine

def index(request):

    num_service = Service.objects.all().count()
    num_order = Order.objects.all().count()
    num_car = Car.objects.all().count()

    context = {
        'num_service' : num_service,
        'num_order' : num_order,
        'num_car' : num_car
    }

    return render(request, 'autoservice/index.html', context)

def car_list(request):
    qs = Car.objects
    query = request.GET.get('query')
    if query:
        qs = qs.filter(
            Q(client__icontains=query) |
            Q(license_plate__icontains=query)
        )
    else:
        qs = qs.all()
    paginator = Paginator(qs, 3)
    car_list = paginator.get_page(request.GET.get('page'))
    return render(request, 'autoservice/cars.html', {
        'car_list': car_list 
    })

def car_details(request, pk: int):
    return render(request, 'autoservice/car_details.html', {
        'car': get_object_or_404(Car, pk=pk)
    })

class OrderListView(generic.ListView):
    model = OrderLine
    paginate_by = 3
    template_name = 'autoservice/orderline_list.html'
    context_object_name = 'order_lines'

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            qs = qs.filter(
                Q(car__car_model__brand__icontains=query) |
                Q(car__client__icontains=query)
            )
        return qs

class OrderDetailView(generic.DetailView):
    model = OrderLine
    template_name = 'autoservice/orderline_detail.html'
    context_object_name = 'order_line'


