import uuid
from itertools import chain

from django.db import models
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from base.models import ObjectBaseClass
from django.utils.translation import ugettext_lazy as _

from modules.models import Module, GeneralBaseModulesPool, EducationalProgramTrajectoriesPool, ChoiceModulesPool
from persons.models import Person


class Program(ObjectBaseClass):
    """
    Чё у нас тут есть:
    - общепрофессиональные базовые модули
    - траектория образовательной программы
    - модули по выбору
    - майноры
    - всякая практика, которой пока нет
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(_('Название образовательной программы'), blank=False, max_length=256, default=_(''))
    chief = models.OneToOneField(Person, verbose_name=_('Руководитель образовательной программы'), blank=False, null=True)

    general_base_modules = models.ManyToManyField(GeneralBaseModulesPool, verbose_name=_("Общепрофессиональные базовые модули"))
    educational_program_trajectories = models.ManyToManyField(EducationalProgramTrajectoriesPool, verbose_name=_("Траектории образовательной программы"))
    choice_modules = models.ManyToManyField(ChoiceModulesPool, verbose_name=_("Пул модулей по выбору"))
    module_dependencies = models.ManyToManyField("ModuleDependency", verbose_name=_("Зависимости модулей"))

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
        choice_modules = []
        for pull in self.choice_modules.all():
            choice_modules += list(pull.modules.all().values_list('id', flat=True))

        general_base_modules = []
        for pull in self.general_base_modules.all():
            choice_modules += list(pull.modules.all().values_list('id', flat=True))

        educational_program_trajectories = []
        for pull in self.educational_program_trajectories.all():
            choice_modules += list(pull.modules.all().values_list('id', flat=True))

        modules = choice_modules + general_base_modules + educational_program_trajectories

        return Module.objects.filter(id__in=modules)


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
