from django.db import models
from django.contrib.auth.models import User, Group
from .extras import GRADE_CHOICES, PRINCIPLE_CHOICES, EVIDENCE_CHOICES, GRADE_LEVEL, DIFFICULTY_CHOICES


class Category(models.Model):
    name = models.CharField(null=False, blank=False, max_length=100, verbose_name='Nombre', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'


class Instrument(models.Model):
    name = models.CharField(null=False, blank=False, max_length=100, verbose_name='Nombre')
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='instruments',
                              verbose_name='Dueño', null=True)
    description = models.TextField(verbose_name='Descripción', null=True, blank=True)
    associated_concepts = models.TextField(verbose_name='Conceptos Relacionados', null=True, blank=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, verbose_name="Dificultad",
                                  null=True, blank=True)
    time = models.IntegerField(verbose_name="Tiempo de duración", null=True, blank=True)
    groups = models.IntegerField(verbose_name="Grupos", null=True, blank=True)
    winner_selection = models.TextField(verbose_name="Criterio selección ganador", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='instruments',
                                 verbose_name='Categoría', null=True)
    purpose_teaching = models.BooleanField(verbose_name="Es para enseñar", default=False)
    purpose_reinforce = models.BooleanField(verbose_name="Es para reforzar", default=False)
    purpose_check = models.BooleanField(verbose_name="Es para comprobar", default=False)
    purpose_social = models.BooleanField(verbose_name="Es para socializar", default=False)
    attachments = models.TextField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    update_date = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    public = models.BooleanField(default=True, verbose_name="Público")

    def level(self):
        total = 0
        for i in self.principles.all():
            total += i.weight
        return total / 50

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
        unique_together = ('name', 'owner')
        verbose_name = 'Instrumento'
        verbose_name_plural = 'Instrumentos'


class Principle(models.Model):
    """
    Principle composing an instrument
    """
    principle = models.CharField(max_length=30, null=False, choices=PRINCIPLE_CHOICES, verbose_name='Principio')
    grade = models.CharField(max_length=30, null=False, choices=GRADE_CHOICES, verbose_name='Nivel')
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, related_name='principles', verbose_name='Instrumento')

    @property
    def weight(self):
        n = Component.objects.filter(component_type='Objetivos', instrument=self.instrument).count()
        x = Evidence.objects.filter(principle=self, component__component_type='Objetivos').count()
        tlg = (40 / n) * x if n > 0 else 0
        m = Component.objects.filter(component_type='Reglas', instrument=self.instrument).count()
        y = Evidence.objects.filter(principle=self, component__component_type='Reglas').count()
        tru = (30 / m) * y if m > 0 else 0 # 3.75
        tro = Evidence.objects.filter(principle=self, component__component_type='Roles').count()
        tma = Evidence.objects.filter(principle=self, component__component_type='Materiales').count()
        tst = Evidence.objects.filter(principle=self, component__component_type='Pasos').count()
        r = 10 if tro > 0 else 0
        s = 5 if tst > 0 else 0
        m = 5 if tma > 0 else 0
        return (r + s + m + tru + tlg) * GRADE_LEVEL[self.grade]

    class Meta:
        ordering = ['-id']
        verbose_name = "Principio"
        verbose_name_plural = "Principios"
        unique_together = ("instrument", "principle")

    def __str__(self):
        return '{}: {}'.format(self.instrument.name, self.principle)


class Component(models.Model):
    description = models.TextField(verbose_name='Nombre')
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, related_name='components', verbose_name='Instrumento')
    component_type = models.CharField(max_length=20, choices=EVIDENCE_CHOICES, verbose_name='Tipo')

    def __str__(self):
        return '{}: {}'.format(self.component_type, self.description)

    class Meta:
        ordering = ['-id']
        verbose_name = "Componente"
        verbose_name_plural = "Componentes"


class Evidence(models.Model):
    """
    Represents all the evidence of a principle on an strategy
    """
    principle = models.ForeignKey(Principle, on_delete=models.CASCADE, related_name='evidences', verbose_name='Principio')
    component = models.ForeignKey(Component, on_delete=models.CASCADE, verbose_name='Componente')

    def __str__(self):
        return '{}: {}'.format(self.principle.principle, self.component.description)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = 'Evidencias'
        verbose_name = 'Evidencia'
        unique_together = ('principle', 'component')
