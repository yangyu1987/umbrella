# Generated by Django 2.1.3 on 2018-12-04 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codes', '0002_cstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='cstatus',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
