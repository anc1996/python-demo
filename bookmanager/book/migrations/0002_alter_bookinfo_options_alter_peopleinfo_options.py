# Generated by Django 4.1.13 on 2024-04-16 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinfo',
            options={'verbose_name': '图书表'},
        ),
        migrations.AlterModelOptions(
            name='peopleinfo',
            options={'verbose_name': '人物表'},
        ),
    ]
