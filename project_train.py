import random
import string
import json
import time
import os


class Passenger:
    def __init__(self, name, age, passenger_type):
        self.name = name
        self.age = age
        self.passenger_type = passenger_type


class Ticket:
    def __init__(self, pnr, passenger, train_name, travel_class,
                 seat_number, fare, status="Confirmed"):
        self.pnr = pnr
        self.passenger = passenger
        self.train_name = train_name
        self.travel_class = travel_class
        self.seat_number = seat_number
        self.fare = fare
        self.status = status
        self.booking_time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.cancellation_time = None

    def to_dict(self):
        return {
            "pnr": self.pnr,
            "passenger": self.passenger.__dict__,
            "train_name": self.train_name,
            "travel_class": self.travel_class,
            "seat_number": self.seat_number,
            "fare": self.fare,
            "status": self.status,
            "booking_time": self.booking_time,
            "cancellation_time": self.cancellation_time
        }


class Train:
    def __init__(self, train_number, train_name):
        self.train_number = train_number
        self.train_name = train_name

        self.seats = {
            "Sleeper": {i: None for i in range(1, 6)},
            "AC 3-Tier": {i: None for i in range(1, 4)},
            "AC 2-Tier": {i: None for i in range(1, 3)},
            "First Class": {i: None for i in range(1, 3)}
        }

        self.fare_rates = {
            "Sleeper": 500,
            "AC 3-Tier": 1000,
            "AC 2-Tier": 1500,
            "First Class": 2000
        }

    def available_seats(self, travel_class):
        available = []

        for seat_number, pnr in self.seats[travel_class].items():
            if pnr is None:
                available.append(seat_number)

        return available

    def display_seat_availability(self):
        print("\n--- Seat Availability ---")

        for travel_class, seats in self.seats.items():
            available = self.available_seats(travel_class)
            print(f"{travel_class}: {len(available)} seats available")
            print(f"Available seat numbers: {available}")
            

class ReservationSystem:
    def __init__(self):
        self.train = Train("12601", "Kochi Express")
        self.tickets = []
        self.waiting_list = []
        self.cancelled_tickets = []

        self.load_data()

    def generate_pnr(self):
        while True:
            pnr = ''.join(random.choices(string.digits, k=6))

            if not any(ticket.pnr == pnr for ticket in self.tickets):
                return pnr

    def calculate_fare(self, travel_class, passenger_type):
        fare = self.train.fare_rates[travel_class]

        if passenger_type == "Senior Citizen":
            fare = fare * 0.8       # 20% discount
        elif passenger_type == "Child":
            fare = fare * 0.5       # 50% discount

        return round(fare, 2)

    def duplicate_booking(self, name):
        for ticket in self.tickets:
            if (ticket.passenger.name.lower() == name.lower()
                    and ticket.status == "Confirmed"):
                return True

        for passenger in self.waiting_list:
            if passenger["passenger"].name.lower() == name.lower():
                return True

        return False

    def book_ticket(self):
        print("\n--- Book Ticket ---")

        name = input("Enter passenger name: ").strip()

        if not name:
            print("Name cannot be empty.")
            return

        if self.duplicate_booking(name):
            print("This passenger already has an active booking.")
            return

        try:
            age = int(input("Enter passenger age: "))

            if age <= 0:
                print("Invalid age.")
                return

        except ValueError:
            print("Age must be a number.")
            return

        print("\nPassenger Types:")
        print("1. Adult")
        print("2. Senior Citizen")
        print("3. Child")

        type_choice = input("Choose passenger type: ")

        passenger_types = {
            "1": "Adult",
            "2": "Senior Citizen",
            "3": "Child"
        }

        if type_choice not in passenger_types:
            print("Invalid passenger type.")
            return

        passenger_type = passenger_types[type_choice]

        print("\nTravel Classes:")
        print("1. Sleeper")
        print("2. AC 3-Tier")
        print("3. AC 2-Tier")
        print("4. First Class")

        class_choice = input("Choose travel class: ")

        classes = {
            "1": "Sleeper",
            "2": "AC 3-Tier",
            "3": "AC 2-Tier",
            "4": "First Class"
        }

        if class_choice not in classes:
            print("Invalid travel class.")
            return

        travel_class = classes[class_choice]

        passenger = Passenger(name, age, passenger_type)
        available = self.train.available_seats(travel_class)

        if available:
            seat_number = available[0]
            pnr = self.generate_pnr()
            fare = self.calculate_fare(travel_class, passenger_type)

            ticket = Ticket(
                pnr,
                passenger,
                self.train.train_name,
                travel_class,
                seat_number,
                fare
            )

            self.tickets.append(ticket)
            self.train.seats[travel_class][seat_number] = pnr

            self.save_data()

            print("\nTicket booked successfully!")
            self.display_ticket(ticket)

        else:
            waiting_entry = {
                "passenger": passenger,
                "train_name": self.train.train_name,
                "travel_class": travel_class,
                "waiting_time": time.strftime("%Y-%m-%d %H:%M:%S")
            }

            self.waiting_list.append(waiting_entry)
            self.save_data()

            print("No seats available.")
            print("Passenger added to the waiting list.")
            print(f"Waiting list position: {len(self.waiting_list)}")

    def display_ticket(self, ticket):
        print("\n-----------------------------")
        print("        TICKET DETAILS")
        print("-----------------------------")
        print(f"PNR: {ticket.pnr}")
        print(f"Passenger: {ticket.passenger.name}")
        print(f"Age: {ticket.passenger.age}")
        print(f"Passenger Type: {ticket.passenger.passenger_type}")
        print(f"Train: {ticket.train_name}")
        print(f"Class: {ticket.travel_class}")
        print(f"Seat Number: {ticket.seat_number}")
        print(f"Fare: ₹{ticket.fare}")
        print(f"Status: {ticket.status}")
        print(f"Booking Time: {ticket.booking_time}")
        print("-----------------------------")

    def search_by_pnr(self):
        print("\n--- Search by PNR ---")
        pnr = input("Enter PNR: ").strip()

        for ticket in self.tickets:
            if ticket.pnr == pnr:
                self.display_ticket(ticket)
                return

        for ticket in self.cancelled_tickets:
            if ticket.pnr == pnr:
                print("This ticket is cancelled.")
                self.display_ticket(ticket)
                return

        print("Invalid PNR. Ticket not found.")

    def search_passenger(self):
        print("\n--- Search Passenger ---")
        name = input("Enter passenger name: ").strip().lower()

        found = False

        for ticket in self.tickets:
            if ticket.passenger.name.lower() == name:
                self.display_ticket(ticket)
                found = True

        for entry in self.waiting_list:
            if entry["passenger"].name.lower() == name:
                print("\nPassenger is on the waiting list.")
                print(f"Class: {entry['travel_class']}")
                print(f"Waiting Time: {entry['waiting_time']}")
                found = True

        if not found:
            print("Passenger not found.")

    def cancel_ticket(self):
        print("\n--- Cancel Ticket ---")
        pnr = input("Enter PNR to cancel: ").strip()

        ticket_to_cancel = None

        for ticket in self.tickets:
            if ticket.pnr == pnr:
                ticket_to_cancel = ticket
                break

        if ticket_to_cancel is None:
            print("Invalid PNR or ticket already cancelled.")
            return

        print("\nCancellation Policy:")
        print("More than 48 hours: 10% charge")
        print("24 to 48 hours: 25% charge")
        print("Less than 24 hours: 50% charge")

        try:
            hours = float(input("How many hours before travel? "))

            if hours < 0:
                print("Invalid hours.")
                return

        except ValueError:
            print("Please enter a valid number.")
            return

        if hours > 48:
            charge_percentage = 0.10
        elif hours >= 24:
            charge_percentage = 0.25
        else:
            charge_percentage = 0.50

        cancellation_charge = round(
            ticket_to_cancel.fare * charge_percentage, 2
        )
        refund = round(ticket_to_cancel.fare - cancellation_charge, 2)

        travel_class = ticket_to_cancel.travel_class
        seat_number = ticket_to_cancel.seat_number

        self.train.seats[travel_class][seat_number] = None

        ticket_to_cancel.status = "Cancelled"
        ticket_to_cancel.cancellation_time = time.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        self.tickets.remove(ticket_to_cancel)
        self.cancelled_tickets.append(ticket_to_cancel)

        print("\nTicket cancelled successfully.")
        print(f"Cancellation charge: ₹{cancellation_charge}")
        print(f"Refund amount: ₹{refund}")

        self.promote_waiting_passenger(travel_class, seat_number)

        self.save_data()

    def promote_waiting_passenger(self, travel_class, seat_number):
        for entry in self.waiting_list:
            if entry["travel_class"] == travel_class:
                passenger = entry["passenger"]

                pnr = self.generate_pnr()
                fare = self.calculate_fare(
                    travel_class,
                    passenger.passenger_type
                )

                ticket = Ticket(
                    pnr,
                    passenger,
                    self.train.train_name,
                    travel_class,
                    seat_number,
                    fare
                )

                self.tickets.append(ticket)
                self.train.seats[travel_class][seat_number] = pnr

                self.waiting_list.remove(entry)

                print("\nWaiting-list promotion!")
                print(
                    f"{passenger.name} has been promoted "
                    f"to a confirmed ticket."
                )
                print(f"New PNR: {pnr}")
                print(f"Seat Number: {seat_number}")

                return

        print("No eligible passenger found in the waiting list.")

    def display_waiting_list(self):
        print("\n--- Waiting List ---")

        if not self.waiting_list:
            print("Waiting list is empty.")
            return

        for index, entry in enumerate(self.waiting_list, start=1):
            passenger = entry["passenger"]

            print(
                f"{index}. {passenger.name} | "
                f"Class: {entry['travel_class']} | "
                f"Age: {passenger.age} | "
                f"Type: {passenger.passenger_type}"
            )

    def display_all_tickets(self):
        print("\n--- Confirmed Tickets ---")

        if not self.tickets:
            print("No confirmed tickets.")
            return

        for ticket in self.tickets:
            self.display_ticket(ticket)

    def save_data(self):
        data = {
            "tickets": [ticket.to_dict() for ticket in self.tickets],
            "cancelled_tickets": [
                ticket.to_dict() for ticket in self.cancelled_tickets
            ],
            "waiting_list": [
                {
                    "passenger": entry["passenger"].__dict__,
                    "train_name": entry["train_name"],
                    "travel_class": entry["travel_class"],
                    "waiting_time": entry["waiting_time"]
                }
                for entry in self.waiting_list
            ]
        }

        with open("railway_data.json", "w") as file:
            json.dump(data, file, indent=4)

    def load_data(self):
        if not os.path.exists("railway_data.json"):
            return

        try:
            with open("railway_data.json", "r") as file:
                data = json.load(file)

            for item in data.get("tickets", []):
                passenger_data = item["passenger"]

                passenger = Passenger(
                    passenger_data["name"],
                    passenger_data["age"],
                    passenger_data["passenger_type"]
                )

                ticket = Ticket(
                    item["pnr"],
                    passenger,
                    item["train_name"],
                    item["travel_class"],
                    item["seat_number"],
                    item["fare"],
                    item["status"]
                )

                ticket.booking_time = item["booking_time"]
                ticket.cancellation_time = item["cancellation_time"]

                self.tickets.append(ticket)

                if ticket.seat_number in self.train.seats[ticket.travel_class]:
                    self.train.seats[ticket.travel_class][
                        ticket.seat_number
                    ] = ticket.pnr

            for item in data.get("cancelled_tickets", []):
                passenger_data = item["passenger"]

                passenger = Passenger(
                    passenger_data["name"],
                    passenger_data["age"],
                    passenger_data["passenger_type"]
                )

                ticket = Ticket(
                    item["pnr"],
                    passenger,
                    item["train_name"],
                    item["travel_class"],
                    item["seat_number"],
                    item["fare"],
                    item["status"]
                )

                ticket.booking_time = item["booking_time"]
                ticket.cancellation_time = item["cancellation_time"]

                self.cancelled_tickets.append(ticket)

            for item in data.get("waiting_list", []):
                passenger_data = item["passenger"]

                passenger = Passenger(
                    passenger_data["name"],
                    passenger_data["age"],
                    passenger_data["passenger_type"]
                )

                self.waiting_list.append({
                    "passenger": passenger,
                    "train_name": item["train_name"],
                    "travel_class": item["travel_class"],
                    "waiting_time": item["waiting_time"]
                })

        except (json.JSONDecodeError, KeyError, TypeError):
            print("Saved data could not be loaded correctly.")
            

def main():
    system = ReservationSystem()

    while True:
        print("\n======================================")
        print(" RAILWAY TICKET RESERVATION SYSTEM")
        print("======================================")
        print("1. Book Ticket")
        print("2. Cancel Ticket")
        print("3. Search by PNR")
        print("4. Search Passenger")
        print("5. Display Seat Availability")
        print("6. Display Waiting List")
        print("7. Display All Confirmed Tickets")
        print("8. Exit")
        print("======================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            system.book_ticket()

        elif choice == "2":
            system.cancel_ticket()

        elif choice == "3":
            system.search_by_pnr()

        elif choice == "4":
            system.search_passenger()

        elif choice == "5":
            system.train.display_seat_availability()

        elif choice == "6":
            system.display_waiting_list()

        elif choice == "7":
            system.display_all_tickets()

        elif choice == "8":
            system.save_data()
            print("Thank you for using the Railway Reservation System!")
            break
    

        else:
            print("Invalid menu choice. Please try again.")


if __name__ == "__main__":
    main()
