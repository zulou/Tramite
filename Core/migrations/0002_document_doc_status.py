# Generated by Django 2.1.5 on 2019-02-24 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='doc_status',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
