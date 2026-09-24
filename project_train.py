import random
import time
import os

class Passenger:
    def __init__(self, name, age, pnr, travel_class):
        self.name = name
        self.age = int(age)
        self.pnr = pnr
        self.travel_class = travel_class

class Ticket:
    def __init__(self, pnr, status, seat_num, book_time):
        self.pnr = pnr
        self.status = status 
        self.seat_num = seat_num
        self.timestamp = book_time

class Train:
    def __init__(self, total_seats):
        self.total_seats = total_seats
        self.available_seats = list(range(1, total_seats + 1)) 
        self.waiting_list = [] 

class ReservationSystem:
    def __init__(self):
        self.passengers = [] 
        self.seat_status = {} 
        self.train = Train(total_seats=5)
        self.fares = {"Sleeper": 500, "AC 3-Tier": 1000, "AC 2-Tier": 1500, "First Class": 2000}
        self.load_data() 

    def calculate_fare(self, age, travel_class):
        base_fare = self.fares.get(travel_class, 500)
        if age <= 12:
            return base_fare * 0.5
        elif age >= 60:
            return base_fare * 0.8
        return base_fare

    def book_ticket(self, name, age, travel_class):
        for p in self.passengers:
            if p.name.lower() == name.lower():
                print(f"\nBooking failed: {name} already has an active booking.")
                return

        pnr = str(random.randint(100000, 999999))
        new_passenger = Passenger(name, age, pnr, travel_class)
        self.passengers.append(new_passenger)
        
        fare = self.calculate_fare(new_passenger.age, travel_class)

        if self.train.available_seats:
            seat_num = self.train.available_seats.pop(0)
            new_ticket = Ticket(pnr, "Confirmed", seat_num, time.time())
            self.seat_status[pnr] = new_ticket
            print(f"\nTicket Confirmed! PNR: {pnr} | Seat: {seat_num} | Fare: ₹{fare}")
        else:
            new_ticket = Ticket(pnr, "Waiting", "None", time.time())
            self.seat_status[pnr] = new_ticket
            self.train.waiting_list.append(new_passenger)
            print(f"\nTrain is full. Added to Waiting List. PNR: {pnr} | Fare: ₹{fare}")

    def cancel_ticket(self, pnr):
        if pnr not in self.seat_status:
            print("\nInvalid PNR. No booking found.")
            return

        ticket = self.seat_status[pnr]
        
        time_elapsed = time.time() - ticket.timestamp
        if time_elapsed < 60:
            print("\nTicket cancelled early. 10% cancellation charge applied.")
        else:
            print("\nTicket cancelled late. 50% cancellation charge applied.")

        if ticket.status == "Confirmed":
            freed_seat = ticket.seat_num
            print(f"Seat {freed_seat} is now free.")
            
            if self.train.waiting_list:
                promoted_passenger = self.train.waiting_list.pop(0)
                promoted_ticket = self.seat_status[promoted_passenger.pnr]
                promoted_ticket.status = "Confirmed"
                promoted_ticket.seat_num = freed_seat
                print(f"Waitlist Promotion: Passenger {promoted_passenger.name} (PNR: {promoted_passenger.pnr}) is assigned Seat {freed_seat}.")
            else:
                self.train.available_seats.append(freed_seat)
                self.train.available_seats.sort()

        self.passengers = [p for p in self.passengers if p.pnr != pnr]
        del self.seat_status[pnr]
        print("Cancellation successful.")

    def search_pnr(self, pnr):
        if pnr in self.seat_status:
            ticket = self.seat_status[pnr]
            for p in self.passengers:
                if p.pnr == pnr:
                    print(f"\nPNR: {pnr} | Name: {p.name} | Status: {ticket.status} | Seat: {ticket.seat_num}")
                    return
        print("\nInvalid PNR.")

    def search_passenger(self, name):
        found = False
        for p in self.passengers:
            if p.name.lower() == name.lower():
                ticket = self.seat_status[p.pnr]
                print(f"\nName: {p.name} | PNR: {p.pnr} | Status: {ticket.status}")
                found = True
        if not found:
            print("\nPassenger not found.")

    def display_waiting_list(self):
        print("\n--- Waiting List ---")
        if not self.train.waiting_list:
            print("The waiting list is empty.")
        else:
            for idx, p in enumerate(self.train.waiting_list):
                print(f"{idx + 1}. Name: {p.name} | PNR: {p.pnr}")

    def display_seat_availability(self):
        print(f"\nAvailable Seats: {len(self.train.available_seats)} / {self.train.total_seats}")
        if self.train.available_seats:
            print(f"Seat Numbers: {self.train.available_seats}")

    def save_data(self):
        with open("booking_data.txt", "w") as file:
            for p in self.passengers:
                ticket = self.seat_status[p.pnr]
                line = f"{p.pnr},{p.name},{p.age},{p.travel_class},{ticket.status},{ticket.seat_num},{ticket.timestamp}\n"
                file.write(line)
        print("\nData saved successfully.")

    def load_data(self):
        if os.path.exists("booking_data.txt"):
            with open("booking_data.txt", "r") as file:
                for line in file:
                    data = line.strip().split(',')
                    if len(data) == 7:
                        pnr, name, age, travel_class, status, seat_num, timestamp = data
                        
                        loaded_passenger = Passenger(name, age, pnr, travel_class)
                        self.passengers.append(loaded_passenger)
                        
                        seat_num = int(seat_num) if seat_num != "None" else "None"
                        loaded_ticket = Ticket(pnr, status, seat_num, float(timestamp))
                        self.seat_status[pnr] = loaded_ticket
                        
                        if status == "Confirmed" and seat_num in self.train.available_seats:
                            self.train.available_seats.remove(seat_num)
                        elif status == "Waiting":
                            self.train.waiting_list.append(loaded_passenger)
        else:
            print("No previous booking data found. Starting fresh.")

if __name__ == "__main__":
    system = ReservationSystem()

    while True:
        print("\n" + "="*40)
        print("🚂 RAILWAY RESERVATION SYSTEM 🚂")
        print("="*40)
        print("1. Book Ticket")
        print("2. Cancel Ticket")
        print("3. PNR Search")
        print("4. Passenger Search")
        print("5. Seat Availability")
        print("6. Display Waiting List")
        print("7. Exit")
        print("="*40)
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            name = input("Enter Passenger Name: ")
            
            while True:
                age = input("Enter Passenger Age: ")
                if age.isdigit():
                    break
                print("\nInvalid age. Please enter numbers only.")
                
            valid_classes = ["Sleeper", "AC 3-Tier", "AC 2-Tier", "First Class"]
            print("\nClasses:", ", ".join(valid_classes))
            
            while True:
                travel_class = input("Enter Travel Class: ")
                if travel_class in valid_classes:
                    break
                print("\nInvalid travel class selected. Please try again.")
                
            system.book_ticket(name, int(age), travel_class)
            
        elif choice == '2':
            pnr = input("Enter PNR to cancel: ")
            system.cancel_ticket(pnr)
            
        elif choice == '3':
            pnr = input("Enter PNR to search: ")
            system.search_pnr(pnr)
            
        elif choice == '4':
            name = input("Enter Passenger Name: ")
            system.search_passenger(name)
            
        elif choice == '5':
            system.display_seat_availability()
            
        elif choice == '6':
            system.display_waiting_list()
            
        elif choice == '7':
            system.save_data()
            print("Exiting System. Have a safe journey! 🚆")
            break
            
        else:
            print("\nInvalid choice. Please enter a number between 1 and 7.")
