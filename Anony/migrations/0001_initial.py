# Generated by Django 3.2.12 on 2022-04-15 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Anonyboard',
            fields=[
                ('ab_uid', models.AutoField(primary_key=True, serialize=False)),
                ('ab_writer_uuid', models.BinaryField(editable=True, max_length=16)),
                ('ab_writer_a', models.CharField(max_length=20)),
                ('ab_sex', models.CharField(max_length=1)),
                ('ab_type', models.CharField(max_length=20)),
                ('ab_title', models.CharField(max_length=45)),
                ('ab_content', models.TextField()),
                ('ab_wdate', models.CharField(max_length=19)),
                ('ab_udate', models.CharField(blank=True, max_length=19, null=True)),
                ('ab_ddate', models.CharField(blank=True, max_length=19, null=True)),
                ('ab_like', models.IntegerField()),
                ('ab_read', models.IntegerField()),
                ('ab_comment', models.IntegerField()),
                ('ab_image', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'anonyboard',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AnonyboardComment',
            fields=[
                ('ac_index', models.AutoField(primary_key=True, serialize=False)),
                ('ac_uid', models.IntegerField()),
                ('ac_replyer_uuid', models.BinaryField(editable=True, max_length=16)),
                ('ac_replyer_a', models.CharField(max_length=45)),
                ('ac_sex', models.CharField(max_length=1)),
                ('ac_wdate', models.CharField(max_length=19)),
                ('ac_content', models.TextField()),
                ('ac_like', models.IntegerField(blank=True, null=True)),
                ('ac_seqm', models.SmallIntegerField(db_column='ac_seqM')),
                ('ac_seqs', models.SmallIntegerField(db_column='ac_seqS')),
            ],
            options={
                'db_table': 'anonyboard_comment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Boardaddon',
            fields=[
                ('ba_uuid', models.BinaryField(editable=True, max_length=16, primary_key=True, serialize=False)),
                ('ba_tablename', models.CharField(db_column='ba_tableName', max_length=15)),
                ('ba_type', models.CharField(max_length=15)),
                ('ba_boardid', models.IntegerField(db_column='ba_boardID')),
                ('ba_m', models.SmallIntegerField(db_column='ba_M')),
                ('ba_s', models.SmallIntegerField(db_column='ba_S')),
            ],
            options={
                'db_table': 'boardAddon',
                'managed': False,
            },
        ),
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
        migrations.CreateModel(
            name='Firebasetoken',
            fields=[
                ('fbt_uid', models.AutoField(primary_key=True, serialize=False)),
                ('fbt_useruuid', models.BinaryField(db_column='fbt_userUUID', editable=True, max_length=16)),
                ('fbt_usertoken', models.CharField(db_column='fbt_userToken', max_length=200)),
                ('fbt_generdate', models.CharField(db_column='fbt_generDate', max_length=19)),
            ],
            options={
                'db_table': 'firebaseToken',
                'managed': False,
            },
        ),
    ]