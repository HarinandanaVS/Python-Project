import random
import time
import os

class Customer:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

class Room:
    def __init__(self, room_number, room_type, price):
        self.room_number = room_number
        self.room_type = room_type
        self.price = price
        self.status = "Available"

class Reservation:
    def __init__(self, booking_id, customer, room, days):
        self.booking_id = booking_id
        self.customer = customer
        self.room = room
        self.days = int(days)
        self.status = "Reserved"
        self.reservation_time = time.time()
        self.check_in_time = 0.0
        self.check_out_time = 0.0

class Hotel:
    def __init__(self):
        self.rooms = []
        self.reservations = {}
        self.setup_rooms()
        self.load_data()

    def setup_rooms(self):
        prices = {"Single": 1000, "Double": 1500, "Deluxe": 2500, "Suite": 4000}
        for i in range(101, 104):
            self.rooms.append(Room(str(i), "Single", prices["Single"]))
        for i in range(201, 204):
            self.rooms.append(Room(str(i), "Double", prices["Double"]))
        for i in range(301, 303):
            self.rooms.append(Room(str(i), "Deluxe", prices["Deluxe"]))
        for i in range(401, 402):
            self.rooms.append(Room(str(i), "Suite", prices["Suite"]))

    def book_room(self, name, phone, room_type, days):
        assigned_room = None
        for room in self.rooms:
            if room.room_type == room_type and room.status == "Available":
                assigned_room = room
                break
                
        if not assigned_room:
            print("\nSorry, no rooms of that type are available.")
            return

        while True:
            booking_id = str(random.randint(1000, 9999))
            if booking_id not in self.reservations:
                break

        customer = Customer(name, phone)
        reservation = Reservation(booking_id, customer, assigned_room, days)
        
        assigned_room.status = "Reserved"
        self.reservations[booking_id] = reservation
        
        print(f"\nRoom {assigned_room.room_number} booked successfully! Booking ID: {booking_id}")

    def cancel_booking(self, booking_id):
        if booking_id in self.reservations:
            reservation = self.reservations[booking_id]
            if reservation.status == "Reserved":
                reservation.status = "Cancelled"
                reservation.room.status = "Available"
                
                time_elapsed = time.time() - reservation.reservation_time
                if time_elapsed < 60:
                    print("\nBooking cancelled. No charges applied.")
                else:
                    print("\nBooking cancelled. Late cancellation charge of 500 applied.")
            else:
                print("\nOnly 'Reserved' bookings can be cancelled.")
        else:
            print("\nInvalid Booking ID.")

    def check_in(self, booking_id):
        if booking_id in self.reservations:
            reservation = self.reservations[booking_id]
            if reservation.status == "Reserved":
                reservation.status = "Checked-In"
                reservation.room.status = "Checked-In"
                reservation.check_in_time = time.time()
                print(f"\nCheck-in successful for Room {reservation.room.room_number}.")
            else:
                print("\nBooking is not in 'Reserved' status.")
        else:
            print("\nInvalid Booking ID.")

    def check_out(self, booking_id, weekend_days, late_checkout):
        if booking_id in self.reservations:
            reservation = self.reservations[booking_id]
            if reservation.status == "Checked-In":
                reservation.status = "Completed"
                reservation.room.status = "Available"
                reservation.check_out_time = time.time()
                
                base_total = reservation.room.price * reservation.days
                weekend_charge = int(weekend_days) * 500
                total = base_total + weekend_charge
                
                if reservation.days > 5:
                    total = total - (total * 0.10)
                    
                if late_checkout == "y":
                    total = total + 1000
                    
                print(f"\nCheck-out complete! Total Bill: {total}")
            else:
                print("\nGuest is not checked in.")
        else:
            print("\nInvalid Booking ID.")

    def search_bookings(self, phone):
        found = False
        for res in self.reservations.values():
            if res.customer.phone == phone:
                print(f"\nID: {res.booking_id} | Room: {res.room.room_number} | Status: {res.status}")
                found = True
        if not found:
            print("\nNo bookings found for that phone number.")

    def view_history(self):
        print("\n--- Booking History ---")
        for res in self.reservations.values():
            if res.status == "Completed" or res.status == "Cancelled":
                print(f"ID: {res.booking_id} | Name: {res.customer.name} | Status: {res.status}")

    def save_data(self):
        with open("hotel_data.txt", "w") as file:
            for res in self.reservations.values():
                line = f"{res.booking_id},{res.customer.name},{res.customer.phone},{res.room.room_number},{res.room.room_type},{res.days},{res.status},{res.reservation_time}\n"
                file.write(line)
        print("\nData saved successfully.")

    def load_data(self):
        if os.path.exists("hotel_data.txt"):
            with open("hotel_data.txt", "r") as file:
                for line in file:
                    data = line.strip().split(',')
                    if len(data) == 8:
                        booking_id, name, phone, room_num, room_type, days, status, res_time = data
                        
                        target_room = None
                        for r in self.rooms:
                            if r.room_number == room_num:
                                target_room = r
                                break
                                
                        if target_room:
                            customer = Customer(name, phone)
                            reservation = Reservation(booking_id, customer, target_room, int(days))
                            reservation.status = status
                            reservation.reservation_time = float(res_time)
                            
                            if status == "Reserved" or status == "Checked-In":
                                target_room.status = status
                                
                            self.reservations[booking_id] = reservation
        else:
            print("No previous hotel data found. Starting fresh.")


if __name__ == "__main__":
    hotel = Hotel()

    while True:
        print("1. Book Room")
        print("2. Cancel Booking")
        print("3. Check In")
        print("4. Check Out")
        print("5. Search Bookings")
        print("6. View Booking History")
        print("7. Exit")
        print("="*40)
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            name = input("Enter Customer Name: ")
            phone = input("Enter Phone Number: ")
            
            valid_types = ["Single", "Double", "Deluxe", "Suite"]
            print("\nRoom Types: Single, Double, Deluxe, Suite")
            
            while True:
                room_type = input("Enter Room Type (Single/Double/Deluxe/Suite): ").capitalize()
                if room_type in valid_types:
                    break
                print("\nInvalid room type selected. Please try again.")
                
            while True:
                days = input("Enter Number of Days: ")
                if days.isdigit():
                    break
                print("\nInvalid input. Please enter numbers only.")
                
            hotel.book_room(name, phone, room_type, int(days))
            
        elif choice == '2':
            booking_id = input("Enter Booking ID to cancel: ")
            hotel.cancel_booking(booking_id)
            
        elif choice == '3':
            booking_id = input("Enter Booking ID to check in: ")
            hotel.check_in(booking_id)
            
        elif choice == '4':
            booking_id = input("Enter Booking ID to check out: ")
            
            while True:
                weekend_days = input("How many weekend days were included in the stay?: ")
                if weekend_days.isdigit():
                    break
                print("\nInvalid input. Please enter numbers only.")
                
            late_checkout = input("Is this a late check-out? (y/n): ")
            hotel.check_out(booking_id, weekend_days, late_checkout.lower())
            
        elif choice == '5':
            phone = input("Enter Phone Number to search: ")
            hotel.search_bookings(phone)
            
        elif choice == '6':
            hotel.view_history()
            
        elif choice == '7':
            hotel.save_data()
            print("Exiting System. Have a great day!")
            break
            
        else:
            print("\nInvalid choice. Please enter a number between 1 and 7.")
