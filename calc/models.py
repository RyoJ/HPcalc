from django.db import models

class Status(models.Model):
    ap = models.IntegerField(null=True)
    hp = models.IntegerField(null=True)
    mp = models.IntegerField(null=True)
    food = models.IntegerField(null=True)
    medicine = models.IntegerField(null=True)
    sleep = models.IntegerField(null=True)
    happy = models.IntegerField(null=True)
    stress = models.IntegerField(null=True)
    worry = models.IntegerField(null=True)
    iritate = models.IntegerField(null=True)
    tired = models.IntegerField(null=True)
    refuresh = models.IntegerField(null=True)
    event = models.CharField(max_length=100, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    detail = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return u"{0}:{1}... ".format(self.id, self.hp)

""" 入力値を計算して指標を作るためのテーブル """
class Index(models.Model):
    lossap = models.IntegerField(null=True)
    dmg = models.IntegerField(null=True)
    usemp = models.IntegerField(null=True)
    behavior = models.CharField(max_length=100, null=True, blank=True)
    time = models.DateTimeField(null=True)#テーブルを作る時刻から前回のレコードの時刻を引いて求める
    
    def __str__(self):
        return u"{0}:{1}... ".format(self.id, self.lossap)
