# Generated by Django 3.0.5 on 2020-06-12 06:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('programs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DefectType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Phase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Phase name', max_length=50)),
                ('abbreviation', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TimeLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.CharField(blank=True, max_length=100, null=True)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('delta_time', models.IntegerField(default=0)),
                ('finish_date', models.DateTimeField(null=True)),
                ('last_restart_time', models.DateTimeField(auto_now_add=True)),
                ('is_paused', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('phase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phase_log_time', to='logs.Phase')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='program_log_time', to='programs.Program')),
            ],
        ),
        migrations.CreateModel(
            name='DefectLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('time_reparation', models.IntegerField(default=0)),
                ('description', models.TextField(max_length=500)),
                ('solution', models.TextField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cousing_defect', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cousing_defect_defect', to='logs.DefectLog')),
                ('defect', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='logs.DefectType')),
                ('phase_injected', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phase_defect_found', to='logs.Phase')),
                ('phase_removed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phase_defect_removed', to='logs.Phase')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_defects', to='programs.Program')),
            ],
        ),
    ]
