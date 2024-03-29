# Generated by Django 5.0.2 on 2024-03-29 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showtimes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='showtime',
            name='ticket_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6, verbose_name='Ticket Price'),
        ),
    ]