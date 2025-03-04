# Generated by Django 3.2.2 on 2021-10-30 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0009_auto_20211029_1255'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='socialpost',
            name='category',
        ),
        migrations.AddField(
            model_name='socialpost',
            name='category',
            field=models.ManyToManyField(to='social.Category'),
        ),
    ]
