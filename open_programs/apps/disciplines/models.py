import uuid
import json
from django.db import models
from django.utils.safestring import mark_safe
from base.models import ObjectBaseClass
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField

from results.models import Result


class Discipline(ObjectBaseClass):
    FORMS = (
        ('e', _('Экзамен')),
        ('z', _('Зачет'))
        )
    title = models.CharField(_('Название дисциплины'), max_length=256, blank=False, default='')
    description = models.TextField(_("Короткое описание"), max_length=16384, blank=True, null=True)
    module = models.ForeignKey("modules.Module", blank=True, null=True)
    labor = models.PositiveIntegerField(_("зачётных единиц"), blank=False, default=0)
    period = models.IntegerField(_("Период освоения в модуле"), default=1)
    form = models.CharField(_("Форма контроля"), max_length=1, choices=FORMS, default='z')
    results = models.ManyToManyField(Result, verbose_name=_("Результаты обучения"), blank=True)
    results_text = models.TextField(_("Результаты обучения"), max_length=16384, blank=True, default="")

    uni_uid = models.CharField(max_length=256, blank=True, null=True)
    uni_discipline = models.CharField(max_length=256, blank=True, null=True)
    uni_number = models.CharField(max_length=256, blank=True, null=True)
    uni_section = models.CharField(max_length=256, blank=True, null=True)
    uni_file = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        verbose_name = 'дисциплина'
        verbose_name_plural = 'дисциплины'

    def __str__(self):
        return self.title

    def num_courses(self):
        return len(self.courses.all())


class TrainingTerms(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('Наименование срока обучения'), max_length=256, blank=False, default='')
    limit = models.PositiveIntegerField(_("Лимит ЗЕ в год"), default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'срок обучения'
        verbose_name_plural = 'сроки обучения'


class Semester(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    discipline = models.ForeignKey("Discipline")
    program = models.ForeignKey("programs.Program")
    year = models.PositiveIntegerField(_("Год поступления"), default=1970)
    admission_semester = models.PositiveIntegerField(_("Семестр поступления"), default=0)
    training_semester = models.PositiveIntegerField(_("Семестр изучения"), default=0)
    term = models.ForeignKey("TrainingTerms", blank=True, null=True)

    def __str__(self):
        return f"{self.program} - {self.discipline} - {self.year} - {self.training_semester} сем."

    class Meta:
        verbose_name = 'семестр изучения дисциплины'
        verbose_name_plural = 'семестры изучения дисциплины'


class Variant(ObjectBaseClass):
    def __str__(self):
        return f"{self.id} - {self.discipline.title}"

    class Meta:
        verbose_name = 'вариант реализации дисциплин'
        verbose_name_plural = 'варианты реализации дисциплин'

    PARITY = (('1', 'Осенний'), ('2', 'Весенний'), ('3', 'Любой'))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    discipline = models.ForeignKey("Discipline", null=True, blank=True)
    program = models.ForeignKey("programs.Program", null=True, blank=True)
    diagram = models.ForeignKey("Diagram", null=True, blank=True)
    technology = models.ForeignKey("Technology", null=True, blank=True)
    course = models.ForeignKey("courses.Course", null=True, blank=True)
    semester = models.ForeignKey("Semester", null=True, blank=True)
    parity = models.CharField(_("Четность семестра дисциплины"), max_length=2, choices=PARITY, null=True, blank=True)
    link = models.CharField(_("Ссылка на страницу дисциплины"), max_length=512, blank=True, null=True)


class Diagram(ObjectBaseClass):
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'график варианта'
        verbose_name_plural = 'графики варианта'

    title = models.CharField(_("Название графика"), max_length=512)
    diagram = JSONField(verbose_name=_("График"), null=True, blank=True)

    def get_diagram(self):
        lists = []
        for row in self.diagram:
            lists.append(list(row.values()))
        response = list(zip(*lists))
        response.insert(0, list(WorkingType.objects.all().values_list("color", flat=True)))
        return json.dumps(response)

    def get_diagram_display(self):
        lists = []
        for row in self.diagram:
            lists.append(list(row.values()))
        response = list(zip(*lists))
        response.insert(0, list(WorkingType.objects.all().values_list("color", flat=True)))

        r = """
            <div id="diagram_{id}"></div>
            <script>
            var data = JSON.parse('{data}')
            var colors = data[0]
            var titles = data[1]
            var drawSize = [300, 150]
            var xOffset = 10
            var xStep = 3
            data.splice(0, 2)

            var maxValue = findMaxSum(data)
            var step = drawSize[1]/maxValue
            var draw = SVG('diagram_{id}').size(drawSize[0], drawSize[1])
            var verticalOffset;

            for (var i=0; i<maxValue; i++){{
                draw.rect(drawSize[0], 1).fill('#aaa').move(0, 149-(step*i))
            }}

            for (var colIndex = 0; colIndex < data.length; colIndex++) {{
                if (colIndex != 0) {{
                    var moveX = (drawSize[0] - xOffset)/20*colIndex+xStep/2+xOffset;
                }}
                else {{var moveX = xOffset;}}
                var width = (drawSize[0] - xOffset)/20 - xStep/2;
                for (var segmentIndex = 0; segmentIndex < data[colIndex].length; segmentIndex++){{
                    if (segmentIndex != 0) {{
                        verticalOffset += data[colIndex][segmentIndex - 1]*step
                    }}
                    else {{verticalOffset = 0;}}
                    var moveY = drawSize[1] - (verticalOffset + data[colIndex][segmentIndex]*step);
                    var height = data[colIndex][segmentIndex]*step;
                    var color = colors[segmentIndex];
                    draw.rect(width, height).fill(color).move(moveX, moveY)
                }}
            }}
            function findMaxSum(array) {{
                var maxArray = [];
                for (var index = 0; index < array.length; index++) {{
                     maxArray.push(array[index].reduce(function(a, b) {{ return a + b; }}, 0));
                }}
                return Math.max.apply(Math, [].concat.apply([], maxArray))
            }}
            </script>""".format(data=json.dumps(response), id=self.id)
        return mark_safe(r)

    get_diagram_display.allow_tags = True


class WorkingType(models.Model):
    title = models.CharField(_("Название вида работы"), max_length=512)
    color = models.CharField(_("Цвет вида работы"), max_length=16, blank=True, null=True)


class Technology(ObjectBaseClass):
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'технология'
        verbose_name_plural = 'технологии'

    def get_color(self):
        return f"<div style='background-color:{self.color};width:6em;height:1.3em'></div>"

    get_color.allow_tags = True
    get_color.short_description = _("Цвет технологии")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_("Название технологии"), max_length=512)
    description = models.TextField(_("Описание технологии"), max_length=16384, blank=True, null=True)
    contact_work_category = models.CharField(_("Категория контактной работы"), max_length=512, blank=True, null=True)
    color = models.CharField(_("Цвет технологии"), max_length=16, blank=True, null=True)
