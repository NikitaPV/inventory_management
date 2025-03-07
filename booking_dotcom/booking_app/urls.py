from django.urls import path
# from booking_app.views import upload_members_csv, upload_inventory_csv, book_inventory
# /Users/nikita/Documents/Ten_Tech/booking_dotcom/booking_app/views.py
# from .views import upload_members_csv, upload_inventory_csv, book_inventory
#
# urlpatterns = [
#     path("upload/users/", upload_members_csv, name="upload_members"),
#     path("upload/inventory/", upload_inventory_csv, name="upload_inventory"),
#     path("book/", book_inventory, name="book_inventory"),
#     ]

from django.urls import path
from .views import UploadUsersCSV, UploadInventoryCSV, BookInventory, CancelBookingAPIView

urlpatterns = [
    path("upload/users/", UploadUsersCSV.as_view(), name="upload_members"),
    path("upload/inventory/", UploadInventoryCSV.as_view(), name="upload_inventory"),
    path("book/", BookInventory.as_view(), name="book_inventory"),
    path("cancel/", CancelBookingAPIView.as_view(), name="cancel_booking"),
]