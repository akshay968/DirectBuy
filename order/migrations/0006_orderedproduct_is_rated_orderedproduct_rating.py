# Generated by Django 4.2 on 2023-06-22 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0005_remove_orderedproduct_shipping_address_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderedproduct",
            name="is_rated",
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name="orderedproduct",
            name="rating",
            field=models.FloatField(default=0),
        ),
    ]
