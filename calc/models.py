from django.db import models

class Status(models.Model):
    ap = models.IntegerField(null=True)
    hp = models.IntegerField(null=True)
    mp = models.IntegerField(null=True)
    event = models.CharField(max_length=100, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return u"{0}:{1}... ".format(self.id, self.hp)
        
class Index(models.Model):
    lossap = models.IntegerField(null=True)
    dmg = models.IntegerField(null=True)
    usemp = models.IntegerField(null=True)
    behavior = models.CharField(max_length=100, null=True, blank=True)
    time
    def __str__(self):
        return u"{0}:{1}... ".format(self.id, self.lossap)
