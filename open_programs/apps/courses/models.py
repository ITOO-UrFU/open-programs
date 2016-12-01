from django.db import models
from django.utils.translation import ugettext_lazy as _


class Course(models.Model):
    STATUSES = (
        ('h', _("Скрыт")),
        ('p', _("Опубликован")),
    )
    title = models.CharField(_("Название курса"), max_length="256", blank=False, default=_("Название курса"))
    description = models.TextField(_("Описание"), max_length="16384", blank=True, default=_("Здесь должно быть описание курса"))
    slug = models.SlugField(_("Код курса"), help_text=_("должен быть уникальным в рамках вуза"))
    #university = models.ForeignKey(University, related_name='university_courses', verbose_name=_("Университет"))  TODO: create University model
    archived = models.BooleanField(_("В архиве"), default=False)
    #authors = models.ManyToManyField(Person, related_name='authors_courses', verbose_name=_("Автор"), blank=True)  TODO: import Person model
    authors_ordering = models.CharField(_("Порядок авторов"), max_length=500, blank=True,
                                        help_text=_("id авторов через пробел"))
    status = models.CharField(_("Статус публикации"), max_length=1, choices=STATUSES, default='h')
    about = models.TextField(_("О курсе"), blank=True)


    #course_format = models.ForeignKey(_("Форма проведения курса"))









