# Generated by Django 3.2.2 on 2021-10-26 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialpost',
            name='category',
            field=models.CharField(choices=[('WEB', 'WEB'), ('ALGORITMOS', 'ALGORITMOS'), ('REDES', 'REDES'), ('SEGURIDAD', 'SEGURIDAD'), ('DESKTOP', 'DESKTOP'), ('LINUX', 'LINUX')], default='ALGORITMOS', max_length=15),
        ),
    ]
