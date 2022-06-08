from django.db import models

# Create your models here.
class Filter(models.Model):
    f_uid = models.AutoField(primary_key=True)
    f_sort = models.CharField(max_length=10)
    f_type = models.CharField(max_length=10)
    f_name = models.CharField(max_length=20)
    f_seq = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'filter'