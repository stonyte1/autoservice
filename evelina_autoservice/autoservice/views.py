from django.shortcuts import render, get_object_or_404
from django.views import generic
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
    paginator = Paginator(Car.objects.all(), 3)
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

class OrderDetailView(generic.DetailView):
    model = OrderLine
    template_name = 'autoservice/orderline_detail.html'
    context_object_name = 'order_line'


