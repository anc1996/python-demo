# Generated by Django 4.1.13 on 2024-05-21 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinfo',
            options={'verbose_name': '图书表', 'verbose_name_plural': '图书表'},
        ),
        migrations.AlterModelOptions(
            name='peopleinfo',
            options={'verbose_name': '人物表', 'verbose_name_plural': '人物表'},
        ),
    ]