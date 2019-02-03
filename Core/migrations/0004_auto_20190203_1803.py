# Generated by Django 2.1.5 on 2019-02-03 18:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0003_departamento_distrito_provincia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='distrito',
            name='id_provincia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tupa_office_begin', to='Core.Provincia'),
        ),
        migrations.AlterField(
            model_name='provincia',
            name='id_departamento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='provincia_departamento', to='Core.Departamento'),
        ),
    ]
