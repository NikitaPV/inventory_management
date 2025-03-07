import csv
from django.core.files.storage import default_storage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Member, Inventory, Booking
import datetime

MAX_BOOKINGS = 2


# Upload Users from CSV
class UploadUsersCSV(APIView):
    def post(self, request):
        if "csv_file" not in request.FILES:
            return Response({"error": "No CSV file provided"}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES["csv_file"]
        file_path = default_storage.save("temp_users.csv", file)

        with open(file_path, newline="", encoding="utf-8-sig") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row
            for row in reader:
                if '' not in row:
                    name, surname, booking_count, date_joined = row
                    Member.objects.get_or_create(name=name.strip(), surname=surname.strip(), booking_count=booking_count,
                                                 date_joined=date_joined)

        return Response({"message": "Users imported successfully"}, status=status.HTTP_201_CREATED)


# Upload Inventory from CSV
class UploadInventoryCSV(APIView):
    def post(self, request):
        if "csv_file" not in request.FILES:
            return Response({"error": "No CSV file provided"}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES["csv_file"]
        file_path = default_storage.save("temp_inventory.csv", file)

        with open(file_path, newline="") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row
            for row in reader:
                if '' not in row:
                    title, description, remaining_count, expiration_date = row
                    expiration_date = datetime.datetime.strptime(expiration_date.strip(), "%d-%m-%Y").strftime("%Y-%m-%d")
                    Inventory.objects.get_or_create(title=title, description=description,
                                                    remaining_count=remaining_count, expiration_date=expiration_date )

        return Response({"message": "Inventory imported successfully"}, status=status.HTTP_201_CREATED)


# Book Inventory
class BookInventory(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        inventory_id = request.data.get("inventory_id")
        quantity = int(request.data.get("quantity", 0))

        if not user_id or not inventory_id or quantity <= 0:
            return Response({"error": "Invalid input"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Member.objects.get(id=user_id)
            inventory = Inventory.objects.get(id=inventory_id)
            if user.booking_count >= MAX_BOOKINGS:
                return Response({"error": "Member has reached max bookings"}, status=status.HTTP_400_BAD_REQUEST)

            if inventory.remaining_count >= quantity:
                Booking.objects.create(member=user, inventory=inventory, booking_date=datetime.datetime.now())
                inventory.remaining_count -= quantity
                inventory.save()
                return Response({"message": "Booking successful"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Not enough inventory available"}, status=status.HTTP_400_BAD_REQUEST)

        except (Member.DoesNotExist, Inventory.DoesNotExist):
            return Response({"error": "User or Inventory not found"}, status=status.HTTP_404_NOT_FOUND)


class CancelBookingAPIView(APIView):
    def post(self, request):
        booking_ref = request.data.get("booking_ref")  # Get booking reference from request

        if not booking_ref:
            return Response({"error": "Booking reference is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            booking = Booking.objects.get(id=booking_ref)  # Fetch booking by reference
            booking.delete()  # Delete the booking
            return Response({"message": "Booking canceled successfully"}, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

