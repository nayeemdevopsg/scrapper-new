# Generated by Django 3.2.19 on 2023-07-01 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ad_model',
            fields=[
                ('ad_id', models.AutoField(primary_key=True, serialize=False)),
                ('query', models.CharField(blank=True, max_length=200)),
                ('ad_url', models.CharField(blank=True, max_length=200)),
                ('ad_title', models.CharField(blank=True, max_length=200)),
                ('ad_description', models.CharField(blank=True, max_length=200)),
                ('screenshot', models.FileField(blank=True, default=None, max_length=250, upload_to='')),
                ('company_board_members', models.CharField(blank=True, max_length=200)),
                ('company_contact_number', models.CharField(blank=True, max_length=200)),
                ('company_email', models.CharField(blank=True, max_length=200)),
                ('company_board_member_role', models.CharField(blank=True, max_length=200)),
                ('notes', models.CharField(blank=True, max_length=200)),
                ('ad_new', models.BooleanField(default=True)),
                ('disposition', models.CharField(blank=True, max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('whois', models.CharField(blank=True, max_length=200)),
                ('secondary_contact', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='company_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=200)),
                ('company_address', models.CharField(max_length=200)),
                ('company_phone', models.CharField(max_length=200)),
                ('company_email', models.CharField(max_length=200)),
                ('company_website', models.CharField(max_length=200)),
                ('company_description', models.CharField(max_length=200)),
                ('company_category', models.CharField(max_length=200)),
                ('company_url', models.CharField(max_length=200)),
                ('company_id', models.CharField(max_length=200)),
            ],
        ),
    ]