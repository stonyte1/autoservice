from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import datetime
from tinymce.models import HTMLField
import pytz

User = get_user_model()
utc = pytz.UTC

class CarModel(models.Model):
    brand = models.CharField(_("brand"), max_length=50, db_index=True)
    model = models.CharField(_("model"), max_length=50, db_index=True)
    year = models.PositiveIntegerField(_("year of manufacture"), db_index=True)
    engine = models.CharField(_("engine"), max_length=50, db_index=True)

    class Meta:
        ordering = ['brand']
        verbose_name = _("car model")
        verbose_name_plural = _("car models")

    def __str__(self):
        return f'{self.brand} - {self.model}'

    def get_absolute_url(self):
        return reverse("car_model_details", kwargs={"pk": self.pk})

class Car(models.Model):
    license_plate = models.CharField(_("license plate"), max_length=10, db_index=True)
    car_model = models.ForeignKey(
        CarModel,
        verbose_name=_('car model'),
        on_delete=models.CASCADE,
        related_name='cars'
    )
    VIN_code = models.CharField(_("VIN code"), max_length=17, db_index=True)
    client = models.ForeignKey(
        User, 
        verbose_name=_("client"), 
        on_delete=models.CASCADE,
        related_name='cars',
        null=True,
        blank=True
        )
    car_image = models.ImageField(
        _("image"), 
        upload_to='autoservice/car_images',
        null=True,
        blank=True)
    
    class Meta:
        ordering = ['client']
        verbose_name = _("car")
        verbose_name_plural = _("cars")

    def __str__(self):
        return f'{self.license_plate} - {self.client}'

    def get_absolute_url(self):
        return reverse("car_detail", kwargs={"pk": self.pk})

class Order(models.Model):
    date = models.DateField(_("date"), auto_now_add=True, db_index=True)
    car = models.ForeignKey(
        Car, 
        verbose_name=_("car"), 
        on_delete=models.CASCADE,
        related_name="orders"
        )
    total = models.FloatField(_("total"), db_index=True)
    due_back = models.DateTimeField(_("return time"), null=True, blank=True, db_index=True)
    about_order = HTMLField(_("Order description"), max_length=4000, default='Enter order decription')

    STATUS = (
        ('c', 'Confirmed'),
        ('p', 'In procces'),
        ('a', 'Completed'),
        ('d', 'Denied'),
    )

    status = models.CharField(
        max_length=1,
        choices=STATUS,
        blank=True,
        default='c',
        help_text='Status',
    )

    @property
    def total(self):
        order_line = OrderLine.objects.filter(order=self.id)
        total = 0
        for order in order_line:
            total += order.quantity * order.price
        return total
    
    @property 
    def is_overdue(self):
        if self.due_back and datetime.today().replace(tzinfo=utc) > self.due_back.replace(tzinfo=utc):
            return True
        return False

    class Meta:
        ordering = ['date']
        verbose_name = _("order")
        verbose_name_plural = _("orders")

    def __str__(self):
        return f'{self.date}'

    def get_absolute_url(self):
        return reverse("order_detail", kwargs={"pk": self.pk})

class Service(models.Model):
    name = models.CharField(_("name"), max_length=100, db_index=True)
    price = models.IntegerField(_("price"), db_index=True)
    
    class Meta:
        ordering = ['price']
        verbose_name = _("service")
        verbose_name_plural = _("services")

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse("service_detail", kwargs={"pk": self.pk})

class OrderLine(models.Model):
    service = models.ForeignKey(
        Service, 
        verbose_name=_("service"), 
        on_delete=models.CASCADE,
        related_name="order_lines"
    )
    car = models.ForeignKey(
        Car, 
        verbose_name=_("car"), 
        on_delete=models.CASCADE,
        related_name="order_lines"
    )
    quantity = models.FloatField(_("quantity"), db_index=True)
    price = models.IntegerField(_("price"), db_index=True)  # Uncomment this line
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE,
        related_name='order_lines'
    )

    def save(self, *args, **kwargs):
        service_price = self.service.price
        self.price = service_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.service}"
    
    class Meta:
        ordering = ['car']
        verbose_name = _("order line")
        verbose_name_plural = _("order lines")

    def get_absolute_url(self):
        return reverse("order_line_detail", kwargs={"pk": self.pk})

class OrderChat(models.Model):
    order = models.ForeignKey(
        Order, 
        verbose_name=_("order"), 
        on_delete=models.CASCADE,
        related_name='order_chats'
        )
        
    user = models.ForeignKey(
        User, 
        verbose_name=_("user"), 
        on_delete=models.SET_NULL,
        related_name='order_chats',
        null=True,
        blank=True
        )
    message_at = models.DateField(_("messaged at"), auto_now_add=True)
    message = models.TextField(_("meesage"), max_length=4000)

    class Meta:
        ordering = ['-message_at']
        verbose_name = _("order chat")
        verbose_name_plural = _("order chats")

    def __str__(self):
        return f'{self.message_at}: {self.user}'

    def get_absolute_url(self):
        return reverse("orderreview_detail", kwargs={"pk": self.pk})

