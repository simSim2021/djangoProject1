# Generated by Django 4.0.4 on 2022-05-05 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Capital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capital_text', models.CharField(max_length=255)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
                ('correct', models.BooleanField(default=False)),
                ('capital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geography.capital')),
            ],
        ),
    ]