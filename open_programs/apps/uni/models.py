from django.db import models


class Qualification(models.Model):
    title = models.CharField(max_length=32, blank=False)

    def __str__(self):
        return self.title


class Speciality(models.Model):
    uid = models.CharField(max_length=32, blank=False)
    okso = models.CharField(max_length=8, blank=False)
    title = models.CharField(max_length=1024, blank=False)
    ministerialCode = models.CharField(max_length=8, blank=False)
    ugnTitle = models.CharField(max_length=64, blank=False)
    standard = models.CharField(max_length=32, blank=False)
    qualifications = models.ManyToManyField("Qualification")

