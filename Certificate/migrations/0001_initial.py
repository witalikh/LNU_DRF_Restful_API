# Generated by Django 3.2.9 on 2021-11-14 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=256)),
                ('international_passport', models.CharField(max_length=8)),
                ('date_of_birth', models.DateField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('vaccine', models.CharField(choices=[('Pfizer', 'Pfizer'), ('Moderna', 'Moderna'), ('AstraZeneca', 'AstraZeneca'), ('CoronaVac', 'CoronaVac'), ('CoviShield', 'CoviShield'), ('Jannsen', 'Jannsen')], max_length=64)),
            ],
        ),
    ]