# Generated by Django 2.2.2 on 2019-07-14 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0004_index_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='detail',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
