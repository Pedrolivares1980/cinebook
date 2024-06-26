# Generated by Django 5.0.2 on 2024-03-12 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cinema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Cinema Name')),
                ('address', models.TextField(verbose_name='Address')),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone Number')),
            ],
            options={
                'verbose_name': 'Cinema',
                'verbose_name_plural': 'Cinemas',
            },
        ),
    ]
