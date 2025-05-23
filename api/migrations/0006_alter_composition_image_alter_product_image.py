# Generated by Django 5.1.6 on 2025-03-13 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='composition',
            name='image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='composition_images/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='products/'),
        ),
    ]
