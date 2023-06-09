from django import forms
from . import models

class DateInput(forms.DateInput):
    input_type = 'date'

class OrderChatForm(forms.ModelForm):
    
    class Meta:
        model = models.OrderChat
        fields = ('message', 'order', 'user')
        widgets = {
            'order': forms.HiddenInput(attrs={'readonly': True}),
            'user': forms.HiddenInput(),
        }

class CarForm(forms.ModelForm):
    class Meta:
        model = models.Car
        fields = ('car_model', 'client', 'VIN_code', 'license_plate', 'car_image')
        widgets = {
            'client': forms.HiddenInput()
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = ('car', 'due_back', 'status')
        # widgets = {
        #     'car': forms.HiddenInput(),
        #     'due_back': forms.HiddenInput(),
        #     'status': forms.HiddenInput()
        # }