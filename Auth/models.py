from django.db import models

# Create your models here.
class User(models.Model):
    u_uid = models.AutoField(primary_key=True)
    u_uuid = models.BinaryField(max_length=16, editable=True)
    u_grade = models.CharField(max_length=1)
    u_id = models.CharField(max_length=25)
    u_pw = models.CharField(max_length=255)
    u_phone = models.CharField(max_length=11)
    u_sex = models.CharField(max_length=1)
    u_mainpic = models.TextField(db_column='u_mainPic')  # Field name made lowercase.
    u_point = models.IntegerField(blank=True, null=True)
    u_emailnotify = models.BinaryField(db_column='u_emailNotify', max_length=1, editable=True)  # Field name made lowercase.
    u_smsnotify = models.BinaryField(db_column='u_smsNotify', max_length=1, editable=True)  # Field name made lowercase.
    u_pushnotify = models.BinaryField(db_column='u_pushNotify', max_length=1, editable=True)  # Field name made lowercase.
    u_registerdate = models.CharField(db_column='u_registerDate', max_length=19)  # Field name made lowercase.
    u_withdrawaldate = models.CharField(db_column='u_withdrawalDate', max_length=19, blank=True, null=True)  # Field name made lowercase.
    u_lastlogin = models.CharField(db_column='u_lastLogin', max_length=19)  # Field name made lowercase.
    u_introcode = models.CharField(db_column='u_introCode', max_length=15)  # Field name made lowercase.
    u_appversion = models.CharField(db_column='u_appVersion', max_length=15)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user'

class Userprofile(models.Model):
    up_uid = models.AutoField(primary_key=True)
    up_useruuid = models.BinaryField(db_column='up_userUUID', max_length=16, editable=True)  # Field name made lowercase.
    up_name = models.CharField(max_length=20)
    up_sex = models.CharField(max_length=1)
    up_birth = models.CharField(max_length=6)
    up_height = models.CharField(max_length=3)
    up_body = models.CharField(max_length=2)
    up_edu = models.CharField(max_length=20)
    up_eduname = models.CharField(max_length=20, blank=True, null=True)
    up_live = models.CharField(max_length=20)
    up_religion = models.CharField(max_length=2)
    up_smoke = models.CharField(max_length=2)
    up_alcohol = models.CharField(max_length=2)
    up_nickname = models.CharField(max_length=20)
    up_selfintro = models.TextField(blank=True, null=True)
    up_character = models.TextField(blank=True, null=True)
    up_hobby = models.TextField(blank=True, null=True)
    up_interest = models.TextField(blank=True, null=True)
    up_datestyle = models.TextField(blank=True, null=True)
    up_requirepic = models.TextField(db_column='up_requirePic')  # Field name made lowercase.
    up_extrapic = models.TextField(db_column='up_extraPic', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'userprofile'

class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'

class Userjwttoken(models.Model):
    ujt_useruuid = models.BinaryField(primary_key=True, max_length=16, editable=True)
    ujt_key = models.TextField()

    class Meta:
        managed = False
        db_table = 'userjwttoken'

class Firebasetoken(models.Model):
    fbt_uid = models.AutoField(primary_key=True)
    fbt_useruuid = models.BinaryField(db_column='fbt_userUUID', max_length=16, editable=True)  # Field name made lowercase.
    fbt_usertoken = models.CharField(db_column='fbt_userToken', max_length=200)  # Field name made lowercase.
    fbt_generdate = models.CharField(db_column='fbt_generDate', max_length=19)  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'firebaseToken'

class Userauthlist(models.Model):
    ual_useruuid = models.BinaryField(db_column='ual_userUUID', primary_key=True, max_length=16, editable=True)  # Field name made lowercase.
    ual_type = models.CharField(max_length=15)
    ual_require = models.CharField(max_length=19)
    ual_confirm = models.CharField(max_length=19, blank=True, null=True)
    ual_return = models.CharField(max_length=19, blank=True, null=True)
    ual_image = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'userAuthList'
        unique_together = (('ual_useruuid', 'ual_type'),)