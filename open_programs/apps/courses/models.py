from django.db import models
from base.models import ObjectBaseClass
from django.utils.translation import ugettext_lazy as _


class Course(ObjectBaseClass):
    title = models.CharField(_("Название курса"), max_length=256, blank=False, default=_("Название курса"))
    description = models.TextField(_("Описание"), max_length=16384, blank=True, default=_("Здесь должно быть описание курса"))
    slug = models.SlugField(_("Код курса"), help_text=_("должен быть уникальным в рамках вуза"))
    #university = models.ForeignKey(University, related_name='university_courses', verbose_name=_("Университет"))  TODO: create University model
    #authors = models.ManyToManyField(Person, related_name='authors_courses', verbose_name=_("Автор"), blank=True)  TODO: import Person model
    authors_ordering = models.CharField(_("Порядок авторов"), max_length=500, blank=True,
                                        help_text=_("id авторов через пробел"))
    about = models.TextField(_("О курсе"), blank=True)

    #course_format = models.ForeignKey(Form)  TODO: create&rename Form model
    cover = models.ImageField(_("Обложка"), upload_to='cover', blank=True)
    video = models.URLField(_("Промовидео"), max_length=500, blank=True, default='',
                             help_text=_("URL видео"))
    video_cover = models.ImageField(_("Картинка для видео"), upload_to='video_cover', blank=True)
    workload = models.PositiveIntegerField(_("часов в неделю"), blank=True, null=True)
    points = models.PositiveIntegerField(_("зачётных единиц"), blank=True, null=True)
    duration = models.PositiveIntegerField(_("Длительность (недель)"), blank=True, null=True)

    def __str__(self):
        return '%s - %s' % (self.slug, self.title)

    @models.permalink
    def get_absolute_url(self):
        return None

    def all_sessions(self):
        return None


    class Session(models.Model):
        startdate = models.DateTimeField(_("Начало курса"))
        enddate = models.DateTimeField(_("Конец курса"))











