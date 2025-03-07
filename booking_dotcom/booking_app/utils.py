import csv
from .models import Member, Inventory


def import_members_from_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for row in reader:
            name, surname, booking_count, date_joined, total_bookings = row
            Member.objects.get_or_create(name=name, surname=surname, booking_count=booking_count,
                                         date_joined=date_joined, total_bookings=0)


def import_inventory_from_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for row in reader:
            title, description, remaining_count, expiration_date = row
        Inventory.objects.get_or_create(title=title, description=description,
                                        remaining_count=int(remaining_count), expiration_date=expiration_date)
