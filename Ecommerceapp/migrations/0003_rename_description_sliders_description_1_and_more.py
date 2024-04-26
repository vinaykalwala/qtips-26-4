# Generated by Django 4.2.7 on 2024-01-09 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        (
            "Ecommerceapp",
            "0002_alter_categorie_slug_alter_main_categorie_slug_and_more",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="sliders",
            old_name="Description",
            new_name="Description_1",
        ),
        migrations.RenameField(
            model_name="sliders",
            old_name="Brand_name",
            new_name="Description_2",
        ),
        migrations.RenameField(
            model_name="sliders",
            old_name="Image",
            new_name="image",
        ),
        migrations.RemoveField(
            model_name="banners",
            name="category",
        ),
        migrations.AddField(
            model_name="categorie",
            name="popular",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="discount_deal",
            name="Discount",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="discount_deal",
            name="slug",
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="moving_text",
            name="section",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="Ecommerceapp.section",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="Deals",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="Ecommerceapp.discount_deal",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="original_price",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="section",
            name="contains_products",
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name="Top_Featured",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Ecommerceapp.product",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Deal_of_the_day",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("discount", models.FloatField(default=0)),
                ("deal_datetime", models.DateTimeField(blank=True, null=True)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Ecommerceapp.product",
                    ),
                ),
            ],
        ),
    ]