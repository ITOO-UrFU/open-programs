import uuid
from itertools import chain

from django.db import models
from django import forms
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
    #module_dependencies = models.ManyToManyField("ModuleDependency", verbose_name=_("Зависимости модулей"))

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
        choice_modules = [pull.modules.all().values('id') for pull in self.choice_modules.all()]
        general_base_modules = [pull.modules.all().values('id') for pull in self.general_base_modules.all()]
        educational_program_trajectories = [pull.modules.all().values('id') for pull in
                              [track for track in self.educational_program_trajectories.all()]]

        modules = list(chain(choice_modules, general_base_modules, educational_program_trajectories))
        print(modules)  # ПОЛОМАТО!


        return Module.objects.filter(title__in=modules)



class ModuleDependency(models.Model):
    DEPENDENCY_TYPES = (
        ("soft", _("мягкая")),
        ("hard", _("строгая")),
    )
    program = models.ForeignKey(Program, null=True)
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
        if hasattr(self, 'instance'):
            self.fields['modules'].queryset = self.instance.program.all_modules()
            #     program = Program.objects.get(title=self.instance.program)
            #     modules = program.all_modules()
            #     print(modules)
            #     w = self.fields['modules'].widget
            #     choices = []
            #     for module in modules:
            #         choices.append((module.id, module.title))
            #     w.choices = modules
            # except:
            #     pass
            #self.initial['modules'] = None  #  self.instance.program.all_modules()


