from __future__ import unicode_literals
from copy import copy
from email.mime.image import MIMEImage
import os
from datetime import datetime
import random
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from guests.models import Party


SAVE_THE_DATE_TEMPLATE = 'guests/email_templates/save_the_date.html'
SAVE_THE_DATE_CONTEXT_MAP = {
        'kissing': {
            'title': 'Kissing Booth',
            'header_filename': 'hearts.png',
            'main_image': 'kissing_booth.jpg',
            'main_color': '#baccde',
            'font_color': '#000000',
        },
        'petite': {
            'title': 'Pick Me Up!',
            'header_filename': 'hearts.png',
            'main_image': 'petite.jpg',
            'main_color': '#baccde',
            'font_color': '#000000',
        },
        'ring': {
            'title': "Ring Closeup",
            'header_filename': 'hearts.png',
            'main_image': 'ring.jpg',
            'main_color': '#666666',
            'font_color': '#ffffff',
        },
        'shenzhen': {
            'title': "Learning Mandarin",
            'header_filename': 'hearts.png',
            'main_image': 'shenzen.jpg',
            'main_color': '#c4ccd4',
            'font_color': '#000000',
        },
        'sunset': {
            'title': "Cherry Creek Sunset",
            'header_filename': 'hearts.png',
            'main_image': 'sunset.jpg',
            'main_color': '#666666',
            'font_color': '#FFFFFF',
        },
        'presque': {
            'title': 'Presque Isle Walk',
            'header_filename': 'hearts.png',
            'main_image': 'presque_walk.jpg',
            'main_color': '#003d71',
            'font_color': '#d6d6d4',
        }
    }


def send_all_save_the_dates(test_only=True, mark_as_sent=False):
    to_send_to = Party.in_default_order().filter(save_the_date_sent=None)
    for party in to_send_to:
        send_save_the_date_to_party(party, test_only=test_only)
        if mark_as_sent:
            party.save_the_date_sent = datetime.now()
            party.save()


def send_save_the_date_to_party(party, test_only=True):
    context = get_save_the_date_context(get_template_id_from_party(party))
    recipients = party.guest_emails
    if not recipients:
        print '===== WARNING: no valid email addresses found for {} ====='.format(party)
    else:
        send_save_the_date_email(
            context,
            recipients,
            test_only=test_only
        )


def get_template_id_from_party(partyType):
    if partyType == 'family':
        # all formal guests get formal invites
        return random.choice(['lions-head', 'ski-trip'])
    else:
        all_options = SAVE_THE_DATE_CONTEXT_MAP.keys()
        return random.choice(all_options)


def get_save_the_date_context(template_id):
    template_id = (template_id or '').lower()
    if template_id not in SAVE_THE_DATE_CONTEXT_MAP:
        #logger.error("How is this template not in the save the date map? {}".format(template_id))
        template_id = get_template_id_from_party('')
    context = copy(SAVE_THE_DATE_CONTEXT_MAP[template_id])
    context['name'] = template_id
    context['page_title'] = 'Steve and Allie - Save the Date!'
    context['preheader_text'] = (
        "The date that you've eagerly been waiting for is finally here. "
        "Steve and Allie are getting married! Save the date!"
    )
    return context


def send_save_the_date_email(context, recipients, test_only=True):
    context['email_mode'] = True
    template_html = render_to_string(SAVE_THE_DATE_TEMPLATE, context=context)
    template_text = "Save the date for Steve and Allie's wedding! August 18, 18. River Falls, WI"
    subject = 'Save the Date for the Jarvises!'
    # https://www.vlent.nl/weblog/2014/01/15/sending-emails-with-embedded-images-in-django/
    msg = EmailMultiAlternatives(subject, template_text, 'Steve and Allie <barneyandjolene@jarvises4.life>', recipients,
                                 reply_to=['barneyandjolene@jarvises4.life'])
    msg.attach_alternative(template_html, "text/html")
    msg.mixed_subtype = 'related'
    for filename in (context['header_filename'], context['main_image']):
        attachment_path = os.path.join(os.path.dirname(__file__), 'static', 'save-the-date', 'images', filename)
        with open(attachment_path, "rb") as image_file:
            msg_img = MIMEImage(image_file.read())
            msg_img.add_header('Content-ID', '{}'.format(filename))
            msg.attach(msg_img)

    print 'sending {} to {}'.format(context['name'], ', '.join(recipients))
    if not test_only:
        msg.send()


def clear_all_save_the_dates():
    for party in Party.objects.exclude(save_the_date_sent=None):
        party.save_the_date_sent = None
        party.save()
