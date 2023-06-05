# Generated by Django 4.2.1 on 2023-06-05 12:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('autoservice', '0002_car_car_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='due_back',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='return time'),
        ),
        migrations.AlterField(
            model_name='car',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cars', to=settings.AUTH_USER_MODEL, verbose_name='client'),
        ),
    ]
