# Generated by Django 3.2.12 on 2022-04-12 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('f_uid', models.AutoField(primary_key=True, serialize=False)),
                ('f_sort', models.CharField(max_length=10)),
                ('f_type', models.CharField(max_length=10)),
                ('f_name', models.CharField(max_length=20)),
                ('f_seq', models.IntegerField()),
            ],
            options={
                'db_table': 'filter',
                'managed': False,
            },
        ),
    ]