from typing import Any, Dict, Optional, Type
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.db.models import Q
from django.db.models.query import QuerySet
from django.core.paginator import Paginator
from . models import Order, Service, Car, OrderLine
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from . forms import OrderChatForm, OrderForm, CarForm
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from datetime import datetime, timedelta

def index(request):

    num_service = Service.objects.all().count()
    num_order = Order.objects.all().count()
    num_car = Car.objects.all().count()
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_service' : num_service,
        'num_order' : num_order,
        'num_car' : num_car,
        'num_visits': num_visits
    }

    return render(request, 'autoservice/index.html', context)

def car_list(request):
    qs = Car.objects
    query = request.GET.get('query')
    if query:
        qs = qs.filter(
            Q(client__first_name__icontains=query) |
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
                Q(car__client__first_name__icontains=query)
            )
        return qs

class OrderDetailView(generic.edit.FormMixin, generic.DetailView):
    model = OrderLine
    template_name = 'autoservice/orderline_detail.html'
    context_object_name = 'order_line'
    form_class = OrderChatForm

    def get_initial(self):
        initial = super().get_initial()
        initial['order'] = self.get_object().order
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chats'] = self.object.order.order_chats.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.order = self.object.order
        form.instance.user = self.request.user
        form.save()
        messages.success(self.request, _('Message sent!'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('orderline_detail', kwargs={'pk': self.object.pk})


class UserOrderListView(LoginRequiredMixin, generic.ListView):
    model = OrderLine
    template_name = "autoservice/user_order_list.html"
    context_object_name = 'order_lines'
    paginate_by = 3

    def get_queryset(self):
        # Retrieve the order lines for the currently logged-in user
        return OrderLine.objects.filter(car__client=self.request.user)

class UserCarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    template_name = "autoservice/user_car_list.html"
    context_object_name = 'cars'
    paginate_by = 3

    def get_queryset(self):
        # Retrieve the order lines for the currently logged-in user
        return Car.objects.filter(client=self.request.user)


class CarCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    form_class = CarForm
    template_name = 'autoservice/car_form.html'
    success_url = reverse_lazy('user_car_list')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['car'] = self.object
        return context

    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()
        initial['client'] = self.request.user
        return initial

    def form_valid(self, form):
        form.instance.client = self.request.user
        messages.success(self.request, 'Car Added!')
        return super().form_valid(form)

class OrderCreateView(LoginRequiredMixin, generic.CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'autoservice/order_form.html'
    success_url = reverse_lazy('user_order_list')

    def get_form(self, form_class: Type[BaseModelForm] | None = form_class) -> BaseModelForm:
        form = super().get_form(form_class)
        if not form.is_bound:
            form.fields['car'].queryset = Car.objects.filter(client=self.request.user)
        return form

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['order'] = self.object
        return context

    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()
        initial['due_back'] = datetime.today() + timedelta(days=14)
        initial['status'] = 'p'
        return initial

    def form_valid(self, form):
        form.instance.status = 'p'
        messages.success(self.request, 'Order Added')
        return super().form_valid(form)

class CarUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Car
    form_class = CarForm
    template_name = 'autoservice/car_form.html'
    success_url = reverse_lazy('user_car_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['car'] = self.get_object()
        return context

    def form_valid(self, form):
        form.instance.client = self.request.user
        messages.success(self.request, 'Car is updated')
        return super().form_valid(form)

    def test_func(self):
        obj = self.get_object()
        return obj.client == self.request.user

class OrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Order
    template_name = 'autoservice/user_order_cancel.html'
    success_url = reverse_lazy('user_order_list')

    def form_valid(self, form):
        messages.success(self.request, 'Order is deleted')
        return super().form_valid(form)
    
    def test_func(self) -> bool | None:
        obj = self.get_object()
        return obj.car.client == self.request.user
