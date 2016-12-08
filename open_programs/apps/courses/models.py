import json
import datetime
from django.db import models
from django.template.defaultfilters import truncatewords_html
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from base.models import ObjectBaseClass

from permission import add_permission_logic
from permission.logics import AuthorPermissionLogic
from permission.logics import CollaboratorsPermissionLogic

from persons.models import Person
from results.models import Result

from django.utils.translation import ugettext_lazy as _


class Course(ObjectBaseClass):

    def get_cover_path(self, filename):
        return str(self.slug) + "/cover/" + filename

    def get_video_cover_path(self, filename):
        return str(self.slug) + "/poster/" + filename

    title = models.CharField(_("Название курса"), max_length=256, blank=False, default=_("Название курса"))
    description = models.TextField(_("Короткое описание"), max_length=16384, blank=True, default=_("Здесь должно быть описание курса"))
    slug = models.SlugField(_("Код курса"), help_text=_("должен быть уникальным в рамках вуза"))
    #university = models.ForeignKey(University, related_name='university_courses', verbose_name=_("Университет"))  TODO: create University model
    authors = models.ManyToManyField(Person, related_name='course_authors', verbose_name=_("Автор"), blank=True)
    authors_ordering = models.CharField(_("Порядок авторов"), max_length=500, blank=True,
                                        help_text=_("id авторов через пробел"))
    about = models.TextField(_("О курсе"), blank=True)

    #course_format = models.ForeignKey(Form)  TODO: create&rename Form model
    cover = models.ImageField(_("Обложка"), upload_to=get_cover_path, blank=True)
    video = models.URLField(_("Промовидео"), max_length=500, blank=True, default='',
                             help_text=_("URL видео"))
    video_cover = models.ImageField(_("Картинка для видео"), upload_to=get_video_cover_path, blank=True)
    workload = models.PositiveIntegerField(_("часов в неделю"), blank=True, null=True)
    points = models.PositiveIntegerField(_("зачётных единиц"), blank=True, null=True)
    duration = models.PositiveIntegerField(_("Длительность (недель)"), blank=True, null=True)
    sessions = models.ManyToManyField('Session', verbose_name="Сессии", blank=True)
    staff = models.ManyToManyField(Person, related_name='course_staff', verbose_name=_("Команда курса"), blank=True)  # TODO: auto add course author and course authors
    results = models.ManyToManyField(Result, verbose_name=_("Результаты обучения"), blank=True)
    results_text = models.TextField(_("Результаты обучения"), max_length=16384, blank=True, default="")

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'

    def __str__(self):
        return '%s - %s' % (self.slug, self.title)

    @models.permalink
    @classmethod
    def get_absolute_url(self):
        return None

    def all_sessions(self):
        return json.dumps([str(session) for session in self.sessions.all()])

    def all_sessions_colors(self):
        sessions = []
        for session in self.sessions.filter(enddate__lte=datetime.datetime.now()):
            sessions.append("<p style=\"color:red\">" + str(session) + "</p>")
        for session in self.sessions.filter(startdate__lte=datetime.datetime.now(), enddate__gte=datetime.datetime.now()):
            sessions.append("<p style=\"color:blue\">" + str(session) + "</p>")
        for session in self.sessions.filter(startdate__gte=datetime.datetime.now()):
            sessions.append("<p style=\"color:green\">" + str(session) + "</p>")


        return "".join(sessions)

    def short_description(self):
        return truncatewords_html(self.description, 20)

    def short_about(self):
        return truncatewords_html(self.about, 20)

    def get_cover(self):
        if self.cover:
            return "<img height=\"100\" src=\"" + self.cover.url + "\"></img>"
        else:
            return _("Без обложки")

    def get_video(self):
        if self.video and self.video_cover:
            return "<video controls=\"controls\" poster=\"" + self.video_cover.url + "\"  height=\"100\"><source src=\"" + str(self.video) + "\"></video>"
        elif self.video and not self.video_cover:
            return "<video controls=\"controls\" height=\"100\"><source src=\"" + str(self.video) + "\"></video>"
        else:
            return "<center><img  height=\"100\" src=\"/static/img/no_video.png\"/></center>"

    all_sessions_colors.allow_tags = True
    short_description.allow_tags = True
    short_about.allow_tags = True
    get_video.allow_tags = True
    get_cover.allow_tags = True

    short_description.short_description = _("Короткое описание")
    short_about.short_description = _("О курсе")
    get_cover.short_description = _("Обложка")
    all_sessions_colors.short_description = _("Сессии курса")
    get_video.short_description = _("Промовидео")
    # TODO: active sessions, expired sessions


class Session(ObjectBaseClass):
    slug = models.SlugField(_("Код сессии"), help_text=_("Например, winter_2016, fall_2015"))
    startdate = models.DateTimeField(_("Начало сессии курса"))
    enddate = models.DateTimeField(_("Конец сессии курса"))

    class Meta:
        verbose_name = 'сессия'
        verbose_name_plural = 'сессии'

    def __str__(self):
        return '%s: %s - %s' % (self.slug, self.startdate.strftime("%d %b %Y"), self.enddate.strftime("%d %b %Y"))


add_permission_logic(Course, AuthorPermissionLogic())
add_permission_logic(Course, CollaboratorsPermissionLogic(
    field_name='staff',
    any_permission=False,
    change_permission=True,
    delete_permission=False,
))


@receiver(pre_delete, sender=Course)
def course_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.cover.delete(False)