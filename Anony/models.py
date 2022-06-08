from django.db import models

# Create your models here.

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
        
class Anonyboard(models.Model):
    ab_uid = models.AutoField(primary_key=True)
    ab_writer_uuid = models.BinaryField(max_length=16, editable=True)
    ab_writer_a = models.CharField(max_length=20)
    ab_sex = models.CharField(max_length=1)
    ab_type = models.CharField(max_length=20)
    ab_title = models.CharField(max_length=45)
    ab_content = models.TextField()
    ab_wdate = models.CharField(max_length=19)
    ab_udate = models.CharField(max_length=19, blank=True, null=True)
    ab_ddate = models.CharField(max_length=19, blank=True, null=True)
    ab_like = models.IntegerField()
    ab_read = models.IntegerField()
    ab_comment = models.IntegerField()
    ab_image = models.TextField(blank=True, null=True)

    #ab_uid = models.ForeignKey(Boardaddon, on_delete=models.CASCADE)
    #boardaddon = models.OneToOneField(Boardaddon, on_delete=models.SET_NULL, null=True)

    class Meta:
        managed = False
        db_table = 'anonyboard'


class AnonyboardComment(models.Model):
    ac_uid = models.AutoField(primary_key=True)
    ac_refid = models.IntegerField()
    ac_replyer_uuid = models.BinaryField(max_length=16, editable=True)
    ac_replyer_a = models.CharField(max_length=45)
    ac_sex = models.CharField(max_length=1)
    ac_wdate = models.CharField(max_length=26)
    ac_content = models.TextField()
    ac_like = models.IntegerField()
    ac_seqm = models.SmallIntegerField(db_column='ac_seqM')  # Field name made lowercase.
    ac_issub = models.IntegerField(db_column='ac_isSub')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'anonyboard_comment'


class Filter(models.Model):
    f_uid = models.AutoField(primary_key=True)
    f_sort = models.CharField(max_length=10)
    f_type = models.CharField(max_length=10)
    f_name = models.CharField(max_length=20)
    f_seq = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'filter'


class Firebasetoken(models.Model):
    fbt_uid = models.AutoField(primary_key=True)
    fbt_useruuid = models.BinaryField(db_column='fbt_userUUID', max_length=16, editable=True)  # Field name made lowercase.
    fbt_usertoken = models.CharField(db_column='fbt_userToken', max_length=200)  # Field name made lowercase.
    fbt_generdate = models.CharField(db_column='fbt_generDate', max_length=19)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'firebaseToken'