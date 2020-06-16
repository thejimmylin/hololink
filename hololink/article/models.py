from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def now():
    return timezone.localtime(timezone.now())


class Article(models.Model):
    hash = models.CharField(
        verbose_name=_('Hash'),
        max_length=128,
        blank=True,
    )
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=256,
        blank=True,
    )
    content = models.TextField(
        verbose_name=_('Content'),
        max_length=262144,
        blank=True,
    )
    from_url = models.URLField(
        verbose_name=_('URL'),
        max_length=1024,
        blank=True,
    )
    recommendation = models.BooleanField(
        verbose_name=_('Recommendation'),
        default=False,
    )
    project = models.CharField(
        verbose_name=_('Project'),
        max_length=256,
        blank=True,
    )
    created_by = models.ForeignKey(
        verbose_name=_('Created by'),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        verbose_name=_('Created at'),
    )
