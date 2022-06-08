from django.db import models

# Create your models here.

class Mainparty(models.Model):
    mp_uid = models.AutoField(primary_key=True)
    mp_wdate = models.CharField(max_length=19)
    mp_writer = models.CharField(max_length=16)
    mp_title = models.CharField(max_length=20)
    mp_type = models.CharField(max_length=20)
    mp_place = models.CharField(max_length=20)
    mp_content = models.TextField()
    mp_pricem = models.IntegerField(db_column='mp_priceM')  # Field name made lowercase.
    mp_pricef = models.IntegerField(db_column='mp_priceF')  # Field name made lowercase.
    mp_ablem = models.SmallIntegerField(db_column='mp_ableM')  # Field name made lowercase.
    mp_ablef = models.SmallIntegerField(db_column='mp_ableF')  # Field name made lowercase.
    mp_condm = models.IntegerField(db_column='mp_condM')  # Field name made lowercase.
    mp_condf = models.IntegerField(db_column='mp_condF')  # Field name made lowercase.
    mp_like = models.IntegerField()
    mp_mdate = models.CharField(max_length=19)
    mp_support = models.CharField(max_length=45, blank=True, null=True)
    mp_image = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mainparty'

class Boardaddon(models.Model):
    ba_idx = models.AutoField(primary_key=True)
    ba_uuid = models.BinaryField(max_length=16, editable=True)
    ba_tablename = models.CharField(db_column='ba_tableName', max_length=15)  # Field name made lowercase.
    ba_type = models.CharField(max_length=15)
    ba_boardid = models.IntegerField(db_column='ba_boardID')  # Field name made lowercase.
    ba_commentid = models.IntegerField(db_column='ba_commentID', null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'boardAddon'