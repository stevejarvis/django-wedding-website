from __future__ import unicode_literals
import datetime
import uuid

from django.db import models
from django.dispatch import receiver

# these will determine the default formality of correspondence
ALLOWED_TYPES = [
    ('friends', 'friends'),
    ('family', 'family'),
]


def _random_uuid():
    return uuid.uuid4().hex


class Party(models.Model):
    """
    A party consists of one or more guests.
    """
    name = models.TextField()
    category = models.CharField(max_length=10, choices=ALLOWED_TYPES, default=ALLOWED_TYPES[0][0])
    save_the_date_sent = models.DateTimeField(null=True, blank=True, default=None)
    save_the_date_opened = models.DateTimeField(null=True, blank=True, default=None)
    invitation_id = models.CharField(max_length=32, db_index=True, default="", unique=True)
    invitation_sent = models.DateTimeField(null=True, blank=True, default=None)
    invitation_opened = models.DateTimeField(null=True, blank=True, default=None)
    rehearsal_dinner = models.BooleanField(default=False)
    is_attending = models.NullBooleanField(default=None)
    comments = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return 'Party: {}'.format(self.name)

    @classmethod
    def in_default_order(cls):
        return cls.objects.order_by('category', '-is_attending', 'name')

    @property
    def ordered_guests(self):
        return self.guest_set.order_by('is_child', 'pk')

    @property
    def any_guests_attending(self):
        return any(self.guest_set.values_list('is_attending', flat=True))

    @property
    def guest_emails(self):
        return filter(None, self.guest_set.values_list('email', flat=True))


class Guest(models.Model):
    """
    A single guest
    """
    party = models.ForeignKey(Party)
    first_name = models.TextField()
    last_name = models.TextField(null=True, blank=True)
    email = models.TextField(null=True, blank=True)
    is_attending = models.NullBooleanField(default=None)
    has_plus_one = models.BooleanField(default=False)
    plus_one_attending = models.NullBooleanField(default=None)
    is_child = models.BooleanField(default=False)
    home_address = models.TextField(null=True, blank=True)

    @property
    def name(self):
        return u'{} {}'.format(self.first_name, self.last_name)

    @property
    def unique_id(self):
        # convert to string so it can be used in the "add" templatetag
        return unicode(self.pk)

    def __unicode__(self):
        return 'Guest: {} {}'.format(self.first_name, self.last_name)
