# Generated by Django 4.2.1 on 2023-05-26 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pessoa',
            name='sobre_nome',
            field=models.CharField(max_length=1000, verbose_name='Segundo nome'),
        ),
    ]