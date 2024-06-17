# Generated by Django 4.2.13 on 2024-06-17 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productincart',
            name='amount',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='productincart',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cartproducts', to='shop.shoppingcart', verbose_name='Корзина'),
        ),
        migrations.AlterField(
            model_name='productincart',
            name='products',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cartproducts', to='shop.product', verbose_name='Продукты'),
        ),
    ]