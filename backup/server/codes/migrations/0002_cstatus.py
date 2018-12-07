# Generated by Django 2.1.3 on 2018-12-04 06:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('codes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cstatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(blank=True, default=0)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='codes.Client')),
            ],
        ),
    ]
