
import random
import json
from datetime import datetime

class Customer:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone


class Room:
    def __init__(self, number, room_type, price):
        self.number = number
        self.type = room_type
        self.price = price
        self.status = "Available"


class Reservation:
    def __init__(self, customer, room, days):
        self.id = random.randint(1000, 9999)
        self.customer = customer
        self.room = room
        self.days = days
        self.status = "Reserved"
        self.time = str(datetime.now())


class Hotel:
    def __init__(self):
        self.rooms = [
            Room(101, "Single", 1500),
            Room(102, "Double", 2500),
            Room(103, "Deluxe", 4000),
            Room(104, "Suite", 7000)
        ]
        self.customers = {}
        self.bookings = {}

    def add_customer(self):
        name = input("Name: ")
        phone = input("Phone: ")

        if not name or not phone.isdigit():
            print("Invalid details!")
            return

        customer_id = len(self.customers) + 1
        self.customers[customer_id] = Customer(name, phone)
        print("Customer ID:", customer_id)

    def book_room(self):
        try:
            customer_id = int(input("Customer ID: "))
            days = int(input("Number of days: "))
        except ValueError:
            print("Enter valid numbers!")
            return

        if customer_id not in self.customers or days <= 0:
            print("Invalid customer or days!")
            return

        room_type = input("Room type: ").title()

        for room in self.rooms:
            if room.type == room_type and room.status == "Available":
                booking = Reservation(
                    self.customers[customer_id], room, days
                )

                while booking.id in self.bookings:
                    booking.id = random.randint(1000, 9999)

                room.status = "Reserved"
                self.bookings[booking.id] = booking

                print("Booking ID:", booking.id)
                print("Room:", room.number)
                return

        print("Room not available!")

    def check_in(self):
        booking = self.find_booking()

        if booking and booking.status == "Reserved":
            booking.status = "Checked-In"
            booking.room.status = "Checked-In"
            print("Check-in successful!")

    def check_out(self):
        booking = self.find_booking()

        if not booking or booking.status != "Checked-In":
            print("Invalid booking!")
            return

        total = booking.room.price * booking.days

        if booking.days > 5:
            total *= 0.85

        if booking.days >= 2:
            total *= 1.10

        print("Room charge:", round(total, 2))

        late = input("Late checkout? (y/n): ").lower()
        if late == "y":
            total += 500
            print("Late fee: 500")

        print("Final bill:", round(total, 2))

        booking.status = "Checked-Out"
        booking.room.status = "Available"

    def cancel_booking(self):
        booking = self.find_booking()

        if booking and booking.status in ["Reserved", "Checked-In"]:
            fee = booking.room.price * booking.days * 0.20
            print("Cancellation fee:", round(fee, 2))

            booking.status = "Cancelled"
            booking.room.status = "Available"
            print("Booking cancelled!")

    def find_booking(self):
        try:
            booking_id = int(input("Booking ID: "))
        except ValueError:
            print("Invalid ID!")
            return None

        booking = self.bookings.get(booking_id)

        if not booking:
            print("Booking not found!")

        return booking

    def view_rooms(self):
        for room in self.rooms:
            print(room.number, room.type, room.status, room.price)

    def history(self):
        for booking_id, booking in self.bookings.items():
            print(
                booking_id,
                booking.room.number,
                booking.status,
                booking.time
            )

    def save(self):
        data = {}

        for booking_id, booking in self.bookings.items():
            data[booking_id] = {
                "room": booking.room.number,
                "type": booking.room.type,
                "days": booking.days,
                "status": booking.status,
                "time": booking.time,
                "customer": booking.customer.name
            }

        with open("hotel.json", "w") as file:
            json.dump(data, file, indent=4)

        print("Data saved!")


hotel = Hotel()

while True:
    print("\n1.Customer 2.Book 3.Check-in 4.Check-out")
    print("5.Cancel 6.Rooms 7.History 8.Save 9.Exit")

    choice = input("Choice: ")

    if choice == "1":
        hotel.add_customer()
    elif choice == "2":
        hotel.book_room()
    elif choice == "3":
        hotel.check_in()
    elif choice == "4":
        hotel.check_out()
    elif choice == "5":
        hotel.cancel_booking()
    elif choice == "6":
        hotel.view_rooms()
    elif choice == "7":
        hotel.history()
    elif choice == "8":
        hotel.save()
    elif choice == "9":
        print("Thank you!")
        break
    else:
        print("Invalid choice!")