# Generated by Django 3.2.16 on 2023-07-16 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpreadsheetData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=200)),
                ('buzzword', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=200)),
            ],
        ),
    ]