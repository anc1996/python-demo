# Generated by Django 5.1 on 2025-05-28 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_alter_formpage_options_formpage_email_priority_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formpage',
            name='email_priority',
        ),
        migrations.RemoveField(
            model_name='formpage',
            name='send_admin_notification',
        ),
        migrations.AlterField(
            model_name='formpage',
            name='send_confirmation_email',
            field=models.BooleanField(default=True, help_text='是否向提交者发送确认邮件（异步发送，同时抄送管理员）'),
        ),
    ]
