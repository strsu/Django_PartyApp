from django.db import models


class Acquainblock(models.Model):
    db_uuid = models.BinaryField(primary_key=True, max_length=16, editable=True)
    db_phone = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'acquainBlock'
        unique_together = (('db_uuid', 'db_phone'),)


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


class Couponlist(models.Model):
    cl_couponid = models.CharField(db_column='cl_couponID', primary_key=True, max_length=20)  # Field name made lowercase.
    cl_title = models.CharField(max_length=45)
    cl_createdate = models.CharField(db_column='cl_createDate', max_length=19)  # Field name made lowercase.
    cl_issuedate = models.CharField(db_column='cl_issueDate', max_length=19)  # Field name made lowercase.
    cl_expiredate = models.CharField(db_column='cl_expireDate', max_length=19, blank=True, null=True)  # Field name made lowercase.
    cl_couponcode = models.TextField(db_column='cl_couponCode', blank=True, null=True)  # Field name made lowercase.
    cl_func = models.TextField()
    cl_image = models.TextField()

    class Meta:
        managed = False
        db_table = 'couponList'

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


class Introblock(models.Model):
    ib_blocker = models.BinaryField(primary_key=True, max_length=16)
    ib_type = models.CharField(max_length=45)
    ib_blocked = models.BinaryField(max_length=16, editable=True)

    class Meta:
        managed = False
        db_table = 'introBlock'
        unique_together = (('ib_blocker', 'ib_blocked'),)


class Mainparty(models.Model):
    mp_uid = models.AutoField(primary_key=True)
    mp_wdate = models.CharField(max_length=19)
    mp_writer = models.CharField(max_length=16, editable=True)
    mp_title = models.CharField(max_length=20)
    mp_type = models.CharField(max_length=20)
    mp_place = models.CharField(max_length=20)
    mp_content = models.TextField()
    mp_minage = models.IntegerField()  # Field name made lowercase.
    mp_maxage = models.IntegerField()  # Field name made lowercase.
    mp_like = models.IntegerField()
    mp_mdate = models.CharField(max_length=19)
    mp_support = models.CharField(max_length=45, blank=True, null=True)
    mp_image = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mainparty'


class MainpartyAttend(models.Model):
    mpa_uid = models.AutoField(primary_key=True)
    mpa_boardid = models.IntegerField(db_column='mpa_boardID')  # Field name made lowercase.
    mpa_useruuid = models.CharField(db_column='mpa_userUUID', max_length=16)  # Field name made lowercase.
    mpa_timeline = models.CharField(max_length=13)
    mpa_signtime = models.CharField(max_length=24)

    class Meta:
        managed = False
        db_table = 'mainparty_attend'


class MainpartyReviewQna(models.Model):
    mprq_uid = models.AutoField(primary_key=True)
    mprq_boardid = models.IntegerField()
    mprq_type = models.CharField(max_length=1)
    mprq_uuid = models.BinaryField(max_length=16, editable=True)
    mprq_nickname = models.CharField(max_length=20)
    mprq_content = models.TextField()
    mprq_date = models.CharField(max_length=19)
    mprq_adminuuid = models.CharField(max_length=16, blank=True, null=True, editable=True)
    mprq_admincontent = models.TextField(blank=True, null=True)
    mprq_admindate = models.CharField(max_length=19, blank=True, null=True)
    mprq_score = models.IntegerField()
    mprq_helpcnt = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'mainparty_review_qna'


class MainpartyTimeline(models.Model):
    mpt_uid = models.AutoField(primary_key=True)
    mpt_boardid = models.IntegerField()
    mpt_time = models.CharField(max_length=13)
    mpt_signm = models.SmallIntegerField()
    mpt_signw = models.SmallIntegerField()
    mpt_attendm = models.SmallIntegerField()
    mpt_attendw = models.SmallIntegerField()
    mpt_pricem = models.IntegerField()
    mpt_pricew = models.IntegerField()
    mpt_minagem = models.IntegerField()
    mpt_maxagem = models.IntegerField()
    mpt_minagew = models.IntegerField()
    mpt_maxagew = models.IntegerField()
    mpt_deadline = models.CharField(max_length=11)
    mpt_condm = models.CharField(max_length=20, blank=True, null=True)
    mpt_condw = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mainparty_timeline'



class Recommanduser(models.Model):
    ru_uuida = models.BinaryField(db_column='ru_uuidA', primary_key=True, max_length=16, editable=True)  # Field name made lowercase.
    ru_uuidb = models.BinaryField(db_column='ru_uuidB', max_length=16, editable=True)  # Field name made lowercase.
    ru_rcmdate = models.CharField(db_column='ru_rcmDate', max_length=19)  # Field name made lowercase.
    ru_dateatob = models.CharField(db_column='ru_dateAtoB', max_length=19, blank=True, null=True)  # Field name made lowercase.
    ru_datebtoa = models.CharField(db_column='ru_dateBtoA', max_length=19, blank=True, null=True)  # Field name made lowercase.
    ru_scoreatob = models.CharField(db_column='ru_scoreAtoB', max_length=3, blank=True, null=True)  # Field name made lowercase.
    ru_scoebtoa = models.CharField(db_column='ru_scoeBtoA', max_length=3, blank=True, null=True)  # Field name made lowercase.
    ru_isreject = models.CharField(db_column='ru_isReject', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'recommandUser'


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
    u_emailnotify = models.CharField(db_column='u_emailNotify', max_length=1)  # Field name made lowercase.
    u_smsnotify = models.CharField(db_column='u_smsNotify', max_length=1)  # Field name made lowercase.
    u_pushnotify = models.CharField(db_column='u_pushNotify', max_length=1)  # Field name made lowercase.
    u_registerdate = models.CharField(db_column='u_registerDate', max_length=19)  # Field name made lowercase.
    u_withdrawaldate = models.CharField(db_column='u_withdrawalDate', max_length=19, blank=True, null=True)  # Field name made lowercase.
    u_lastlogin = models.CharField(db_column='u_lastLogin', max_length=19)  # Field name made lowercase.
    u_introcode = models.CharField(db_column='u_introCode', max_length=15)  # Field name made lowercase.
    u_appversion = models.CharField(db_column='u_appVersion', max_length=15)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user'


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


class Usercoupon(models.Model):
    uc_idx = models.AutoField(primary_key=True)
    uc_useruuid = models.BinaryField(db_column='uc_userUUID', max_length=16, editable=True)  # Field name made lowercase.
    uc_couponid = models.CharField(db_column='uc_couponID', max_length=20)  # Field name made lowercase.
    uc_receivedate = models.CharField(db_column='uc_receiveDate', max_length=19)  # Field name made lowercase.
    uc_expiredate = models.CharField(db_column='uc_expireDate', max_length=19)  # Field name made lowercase.
    uc_isuse = models.CharField(db_column='uc_isUse', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'userCoupon'


class Userjwttoken(models.Model):
    ujt_useruuid = models.BinaryField(primary_key=True, max_length=16, editable=True)
    ujt_key = models.TextField()

    class Meta:
        managed = False
        db_table = 'userjwttoken'

class Userparty(models.Model):
    up_uid = models.AutoField(primary_key=True)
    up_useruuid = models.BinaryField(db_column='up_userUUID', max_length=16, editable=True)  # Field name made lowercase.
    up_nickname = models.CharField(max_length=45)
    up_sex = models.CharField(max_length=1)
    up_tags = models.CharField(max_length=45)
    up_title = models.CharField(max_length=45)
    up_content = models.TextField()
    up_state = models.CharField(max_length=1)
    up_wdate = models.CharField(max_length=19)
    up_udate = models.CharField(max_length=19, blank=True, null=True)
    up_ddate = models.CharField(max_length=19, blank=True, null=True)
    up_mdate = models.CharField(max_length=19, blank=True, null=True)
    up_like = models.IntegerField()
    up_read = models.IntegerField()
    up_image = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'userparty'


class UserpartyAttend(models.Model):
    upa_uid = models.AutoField(primary_key=True)
    upa_boardid = models.IntegerField(db_column='upa_boardID')  # Field name made lowercase.
    upa_ownuuid = models.BinaryField(db_column='upa_ownUUID', max_length=16, editable=True)  # Field name made lowercase.
    upa_useruuid = models.BinaryField(db_column='upa_userUUID', max_length=16, editable=True)  # Field name made lowercase.
    upa_attend = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'userparty_attend'


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
