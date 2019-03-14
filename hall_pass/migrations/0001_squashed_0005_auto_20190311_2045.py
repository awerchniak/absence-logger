# Generated by Django 2.1.7 on 2019-03-14 23:13

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import hall_pass.models


class Migration(migrations.Migration):

    replaces = [('hall_pass', '0001_initial'), ('hall_pass', '0002_auto_20190310_1711'), ('hall_pass', '0003_auto_20190310_1720'), ('hall_pass', '0004_auto_20190310_1733'), ('hall_pass', '0005_auto_20190311_2045')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Absence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_in', models.DateTimeField(verbose_name='time in')),
                ('time_out', models.DateTimeField(blank=True, default=None, null=True, verbose_name='time out')),
                ('reason', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('meetings', django.contrib.postgres.fields.jsonb.JSONField(validators=[hall_pass.models.schedule_validator], verbose_name='Meeting Times')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('current_absence', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='hall_pass.Absence')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher_id', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TimberlaneSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('block', models.CharField(choices=[('A Block', 'A Block'), ('B Block', 'B Block')], max_length=10)),
                ('period', models.CharField(choices=[('1st Period', '1st Period'), ('2nd Period', '2nd Period'), ('3rd Period', '3rd Period'), ('4th Period', '4th Period'), ('5th Period', '5th Period')], max_length=20)),
                ('schedule', models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='hall_pass.Schedule')),
            ],
        ),
        migrations.CreateModel(
            name='TimberlaneSemester',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(choices=[('2019', '2019'), ('2020', '2020'), ('2021', '2021'), ('2022', '2022')], max_length=4)),
                ('season', models.CharField(choices=[('Fall', 'Fall'), ('Spring', 'Spring')], max_length=6)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('days_off', models.ManyToManyField(blank=True, default=list, null=True, to='hall_pass.DaysOff')),
            ],
        ),
        migrations.AddField(
            model_name='timberlaneschedule',
            name='semester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hall_pass.TimberlaneSemester'),
        ),
        migrations.AddField(
            model_name='course',
            name='schedule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hall_pass.Schedule'),
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(to='hall_pass.Student'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hall_pass.Teacher'),
        ),
        migrations.AddField(
            model_name='absence',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hall_pass.Course'),
        ),
        migrations.AddField(
            model_name='absence',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hall_pass.Student'),
        ),
        migrations.CreateModel(
            name='TimberlaneDaysOff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('start_date', models.DateField(verbose_name='start date')),
                ('end_date', models.DateField(verbose_name='end date')),
            ],
        ),
        migrations.AlterField(
            model_name='absence',
            name='time_in',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='time in'),
        ),
        migrations.AlterField(
            model_name='absence',
            name='time_out',
            field=models.DateTimeField(default='2019-03-11 21:45', verbose_name='time out'),
            preserve_default=False,
        ),
    ]
