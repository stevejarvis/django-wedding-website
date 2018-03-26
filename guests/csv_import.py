import csv
import StringIO
import uuid
from guests.models import Party, Guest


def import_guests(path):
    with open(path, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        first_row = True
        for row in reader:
            if first_row:
                first_row = False
                continue
            party_name, first_name, last_name, has_plus_one, _, category, is_child, email, mailing_address = row[:9]
            if not party_name:
                print 'skipping row {}'.format(row)
                continue
            # Make the party
            party = Party.objects.get_or_create(name=party_name)[0]
            party.category = category
            if not party.invitation_id:
                party.invitation_id = party_name
            party.save()
            # Make the guest object
            if email:
                guest, created = Guest.objects.get_or_create(party=party, email=email)
                guest.first_name = first_name
                guest.last_name = last_name
            else:
                guest = Guest.objects.get_or_create(party=party, first_name=first_name, last_name=last_name)[0]
            guest.has_plus_one = _is_true(has_plus_one)
            if not guest.has_plus_one:
                guest.plus_one_attending = False
            guest.is_child = _is_true(is_child)
            guest.home_address = mailing_address
            guest.save()


def export_guests():
    headers = [
        'party_name', 'first_name', 'last_name', 'plus_one', 'category',
        'is_child', 'email', 'mailing_address', 'is_attending', 'plus_one_attending',
        'comments'
    ]
    file = StringIO.StringIO()
    writer = csv.writer(file)
    writer.writerow(headers)
    for party in Party.in_default_order():
        for guest in party.guest_set.all():
            writer.writerow([
                party.name,
                guest.first_name,
                guest.last_name,
                guest.has_plus_one,
                party.category,
                guest.is_child,
                guest.email,
                guest.home_address,
                guest.is_attending,
                guest.plus_one_attending,
                party.comments,
            ])
    return file


def _is_true(value):
    value = value or ''
    return value.lower() in ('y', 'yes')
