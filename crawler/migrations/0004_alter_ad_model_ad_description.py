# Generated by Django 5.0.2 on 2024-02-10 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0003_alter_ad_model_screenshot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad_model',
            name='ad_description',
            field=models.TextField(blank=True, null=True),
        ),
    ]