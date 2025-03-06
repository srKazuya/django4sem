# Generated by Django 5.1.6 on 2025-02-28 10:32

import django.db.models.deletion
import filer.fields.image
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_attribute_options_alter_cart_options_and_more'),
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='product',
        ),
        migrations.AlterModelOptions(
            name='productattribute',
            options={'verbose_name': 'Атрибут продукта', 'verbose_name_plural': 'Атрибуты продуктов'},
        ),
        migrations.RemoveField(
            model_name='category',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=filer.fields.image.FilerImageField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_images', to=settings.FILER_IMAGE_MODEL),
        ),
        migrations.AddField(
            model_name='product',
            name='sku',
            field=models.CharField(default='000000', max_length=50, unique=True, verbose_name='Артикул'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='first_name',
            field=models.CharField(default='Имя', max_length=255),
        ),
        migrations.AlterField(
            model_name='customer',
            name='last_name',
            field=models.CharField(default='Фамилия', max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='productattribute',
            name='value',
            field=models.CharField(default='N/A', max_length=255),
        ),
        migrations.CreateModel(
            name='Composition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('designer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compositions', to='api.customer')),
                ('image', filer.fields.image.FilerImageField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='composition_images', to=settings.FILER_IMAGE_MODEL)),
            ],
            options={
                'verbose_name': 'Композиция',
                'verbose_name_plural': 'Композиции',
            },
        ),
        migrations.CreateModel(
            name='CompositionItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('composition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='api.composition')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.product')),
            ],
            options={
                'verbose_name': 'Товар в композиции',
                'verbose_name_plural': 'Товары в композиции',
            },
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='api.category')),
            ],
            options={
                'verbose_name': 'Подкатегория',
                'verbose_name_plural': 'Подкатегории',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='api.subcategory'),
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
