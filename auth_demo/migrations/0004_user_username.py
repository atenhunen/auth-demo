# Generated by Django 3.0.6 on 2020-05-05 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_demo', '0003_auto_20200505_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=100, verbose_name='username'),
        ),
    ]
