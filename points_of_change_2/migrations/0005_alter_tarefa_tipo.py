# Generated by Django 5.2.1 on 2025-05-13 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('points_of_change_2', '0004_alter_tarefa_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarefa',
            name='tipo',
            field=models.CharField(default='Avulso', max_length=20),
        ),
    ]
