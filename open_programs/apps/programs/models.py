import uuid
from itertools import chain

from django.db import models
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from base.models import ObjectBaseClass
from django.utils.translation import ugettext_lazy as _

from modules.models import Module, GeneralBaseModulesPool, EducationalProgramTrajectoriesPool, ChoiceModulesPool
from persons.models import Person
from disciplines.models import Discipline
from professions.models import Profession
from competences.models import Competence


class Program(ObjectBaseClass):
    """
    Чё у нас тут есть:
    - общепрофессиональные базовые модули
    - траектория образовательной программы
    - модули по выбору
    - майноры
    - всякая практика, которой пока нет
    """

    LEVELS = (
        ("b", _("бакалавриат")),
        ("m", _("магистратура")),
        ("s", _("специалитет")),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    level = models.CharField(_("Уровень программы"), max_length=1, choices=LEVELS, default="b")
    title = models.CharField(_('Название образовательной программы'), blank=False, max_length=256, default=_(''))
    chief = models.OneToOneField(Person, verbose_name=_('Руководитель образовательной программы'), blank=True, null=True)

    #general_base_modules = models.ManyToManyField(GeneralBaseModulesPool, blank=True, verbose_name=_("Общепрофессиональные базовые модули"))
    modules = models.ManyToManyField(Module, blank=True, verbose_name=_("Модули программы"))
    educational_program_trajectories = models.ManyToManyField(EducationalProgramTrajectoriesPool, blank=True, verbose_name=_("Траектории образовательной программы"))
    choice_modules = models.ManyToManyField(ChoiceModulesPool, blank=True, verbose_name=_("Пул модулей по выбору"))
    module_dependencies = models.ManyToManyField("ModuleDependency", blank=True, verbose_name=_("Зависимости модулей"))

    def get_all_general_base_modules(self):
        return "\n".join([str(module) for module in self.general_base_modules.all()])

    def get_all_educational_program_trajectories(self):
        return "\n".join([str(module) for module in self.educational_program_trajectories.all()])

    def get_all_choice_modules(self):
        return "\n".join([str(module) for module in self.choice_modules.all()])

    class Meta:
        verbose_name = 'программа'
        verbose_name_plural = 'программы'

    def __str__(self):
        return self.title

    def all_modules(self):

        # choice_modules = []
        # for pull in self.choice_modules.all():
        #     choice_modules += list(pull.modules.all().values_list('id', flat=True))
        #
        # general_base_modules = []
        # for pull in self.general_base_modules.all():
        #     choice_modules += list(pull.modules.all().values_list('id', flat=True))
        #
        # educational_program_trajectories = []
        # for pull in self.educational_program_trajectories.all():
        #     choice_modules += list(pull.modules.all().values_list('id', flat=True))
        #
        # modules = choice_modules + general_base_modules + educational_program_trajectories

        return self.modules.all()

    def labor_percent(self):
        labor = 0
        for module in self.modules.all():
            for discipline in Discipline.objects.filter(module=module):
                if discipline.courses is not None:
                    labor += discipline.points
        if self.level == "b":
            return labor / 240
        elif self.level == "s":
            return labor / 300
        elif self.level == "m":
            return labor / 120

    def profs_count(self):
        results = []
        results_program = []
        profs = []
        for module in self.modules.all():
            for discipline in Discipline.objects.filter(module=module):
                for course in discipline.courses.all():
                    results.append(list(course.results.all()))
        for r in results:
            results_program += r

        for profession in Profession.objects.all():
            for comp in Competence.objects.filter(profession=profession):
                for r in comp.results.all():
                    if r in results_program:
                        if profession not in profs:
                            profs.append(profession)
        return len(profs)




class ModuleDependency(models.Model):
    DEPENDENCY_TYPES = (
        ("soft", _("мягкая")),
        ("hard", _("строгая")),
    )
    module = models.ForeignKey(Module, related_name="module")
    modules = models.ManyToManyField(Module, related_name="modules", blank=True)
    type = models.CharField(_("Тип зависимости"), max_length=4, default="hard", choices=DEPENDENCY_TYPES)

    class Meta:
        verbose_name = 'зависимость'
        verbose_name_plural = 'зависимости'

    def __str__(self):
        try:
            return self.type + '-' + str(self.module) + "-" + "-".join([str(module) for module in self.modules.all()])
        except:
            return self.type


class ModuleDependencyForm(forms.ModelForm):

    class Meta:
        model = ModuleDependency
        exclude = ['modules', ]

    modules = forms.ModelMultipleChoiceField(
        Module.objects.none(),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(ModuleDependencyForm, self).__init__(*args, **kwargs)
        if "initial" not in kwargs and kwargs['instance']:
            program = Program.objects.get(module_dependencies__in=[self.instance])
            self.fields['modules'] = forms.ModelMultipleChoiceField(
                queryset=program.all_modules(),
                required=False,
                widget=FilteredSelectMultiple(
                    verbose_name=_("Модули"),
                    is_stacked=False
                )
            )
