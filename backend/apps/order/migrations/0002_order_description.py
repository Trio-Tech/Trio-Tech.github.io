# Generated by Django 3.2.11 on 2022-02-04 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='description',
            field=models.TextField(default=''),
        ),
    ]
