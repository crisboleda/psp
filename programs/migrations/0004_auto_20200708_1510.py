# Generated by Django 3.0.5 on 2020-07-08 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0003_program_total_lines'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='finish_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='program',
            name='start_date',
            field=models.DateField(),
        ),
    ]
