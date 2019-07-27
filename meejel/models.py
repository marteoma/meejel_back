from django.db import models
from django.contrib.auth.models import User, Group
from .extras import GRADE_CHOICES, PRINCIPLE_CHOICES, EVIDENCE_CHOICES


class Assessment(models.Model):
    """
    An assessment related to an specific user
    """
    name = models.CharField(null=False, max_length=100)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Evaluación"
        verbose_name_plural = "Evaluaciones"
        unique_together = ("name", "owner")


class Principle(models.Model):
    """
    Modelo correspondiente a los principios
    """
    principle = models.IntegerField(null=False, choices=PRINCIPLE_CHOICES)
    grade = models.IntegerField(null=False, choices=GRADE_CHOICES)
    justification = models.CharField(max_length=150, null=False)
    assessment = models.ForeignKey(Assessment, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Principio"
        verbose_name_plural = "Principios"
        unique_together = ("assessment", "principle")


class Evidence(models.Model):
    """
    Represents all the evidence of a principle on an strategy
    """
    sort_of = models.IntegerField(null=False, choices=EVIDENCE_CHOICES)
    description = models.CharField(null=False, max_length=250)
    principle = models.ForeignKey(Principle, on_delete=models.PROTECT)

    def __str__(self):
        return self.description
