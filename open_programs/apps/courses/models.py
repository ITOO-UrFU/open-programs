import json
import datetime
from django.db import models
from base.models import ObjectBaseClass

from persons.models import Person

from django.utils.translation import ugettext_lazy as _


class Course(ObjectBaseClass):
    title = models.CharField(_("Название курса"), max_length=256, blank=False, default=_("Название курса"))
    description = models.TextField(_("Описание"), max_length=16384, blank=True, default=_("Здесь должно быть описание курса"))
    slug = models.SlugField(_("Код курса"), help_text=_("должен быть уникальным в рамках вуза"))
    #university = models.ForeignKey(University, related_name='university_courses', verbose_name=_("Университет"))  TODO: create University model
    authors = models.ManyToManyField(Person, related_name='authors_courses', verbose_name=_("Автор"), blank=True)
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
    sessions = models.ManyToManyField('Session', verbose_name="Сессии", blank=True, null=True)

    def __str__(self):
        return '%s - %s' % (self.slug, self.title)

    @models.permalink
    def get_absolute_url(self):
        return None

    def all_sessions(self):
        return json.dumps([str(session) for session in self.sessions.all()])

    def all_sessions_colors(self):
        sessions = []
        for session in self.sessions.filter(enddate__lte=datetime.datetime.now()):
            sessions.append("<p style=\"color:red\">" + str(session) + "</p>")
        for session in self.sessions.filter(startdate__lte=datetime.datetime.now(), enddate__gte=datetime.datetime.now()):
            sessions.append("<p style=\"color:green\">" + str(session) + "</p>")
        for session in self.sessions.filter(startdate__gte=datetime.datetime.now()):
            sessions.append("<p style=\"color:blue\">" + str(session) + "</p>")


        return "".join(sessions)


    #  "<br />".join([str(session) for session in self.sessions.all()])

    all_sessions_colors.allow_tags = True
    # TODO: active sessions, expired sessions


class Session(ObjectBaseClass):
    slug = models.SlugField(_("Код сессии"), help_text=_("Например, winter_2016, fall_2015"))
    startdate = models.DateTimeField(_("Начало сессии курса"))
    enddate = models.DateTimeField(_("Конец сессии курса"))

    def __str__(self):
        return '%s: %s - %s' % (self.slug, self.startdate.strftime("%d %b %Y"), self.enddate.strftime("%d %b %Y"))