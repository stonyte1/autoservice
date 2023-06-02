from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

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
    client = models.CharField(_("client"), max_length=50, db_index=True)
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
        for line in order_line:
            total += line.quantity * line.price
        return total
    
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
        return f'{self.name} {self.price}'

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

    def __str__(self):
        return f"{self.service}"
    
    class Meta:
        ordering = ['car']
        verbose_name = _("order line")
        verbose_name_plural = _("order lines")

    def get_absolute_url(self):
        return reverse("order_line_detail", kwargs={"pk": self.pk})
