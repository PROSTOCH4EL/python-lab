class Movie:
    def __init__(self, title: str, duration: int, age_limit: int):
        self.title = title
        self.duration = duration
        self.age_limit = age_limit

    def is_long(self) -> bool:
        return self.duration >= 120

    def show(self) -> None:
        print(self.title, "-", self.duration, "хв | вік:", str(self.age_limit) + "+")


class Customer:
    def __init__(self, name: str, age: int, balance: float):
        self.name = name
        self.age = age
        self.balance = balance
        self.tickets = []

    def can_buy(self, price: float) -> bool:
        return self.balance >= price

    def show(self) -> None:
        print(self.name, "| вік:", self.age, "| баланс:", self.balance, "грн")


class Session:
    def __init__(self, movie: Movie, price: float, seats: int):
        self.movie = movie
        self.price = price
        self.seats = seats
        self.busy = []

    def free_seats(self) -> int:
        return self.seats - len(self.busy)

    def show_seats(self) -> None:
        seat_number = 1

        while seat_number <= self.seats:
            if seat_number in self.busy:
                status = "зайняте"
            else:
                status = "вільне"

            print("Місце", seat_number, "-", status)
            seat_number += 1


class Ticket:
    def __init__(self, movie: str, owner: str, seat: int, price: float):
        self.movie = movie
        self.owner = owner
        self.seat = seat
        self.price = price
        self.used = False

    def show(self) -> None:
        print(
            self.movie,
            "| власник:", self.owner,
            "| місце:", self.seat,
            "| ціна:", self.price, "грн"
        )

    def use(self) -> None:
        self.used = True


class Cinema:
    def __init__(self, name: str):
        self.name = name
        self.sessions: list[Session] = []
        self.customers: dict[str, Customer] = {}
        self.tickets: list[Ticket] = []

    def buy(self, name: str, session_index: int) -> bool:
        customer = self.customers[name]
        selected_session = self.sessions[session_index]

        if customer.age < selected_session.movie.age_limit:
            print(
                name,
                "- відмова, потрібен вік",
                str(selected_session.movie.age_limit) + "+"
            )
            return False

        if not customer.can_buy(selected_session.price):
            print(name, "- не вистачає грошей")
            return False

        if selected_session.free_seats() == 0:
            print(name, "- немає вільних місць")
            return False

        seat = len(selected_session.busy) + 1

        new_ticket = Ticket(
            selected_session.movie.title,
            name,
            seat,
            selected_session.price
        )

        customer.balance -= selected_session.price
        customer.tickets.append(new_ticket)
        selected_session.busy.append(seat)
        self.tickets.append(new_ticket)

        print(
            name,
            "купив",
            selected_session.movie.title,
            "| місце:", seat,
            "| ціна:", selected_session.price, "грн"
        )

        return True

    def report(self) -> None:
        income = 0.0

        for report_ticket in self.tickets:
            income += report_ticket.price

        print("Продано квитків:", len(self.tickets))
        print("Дохід:", income, "грн")


spiderman = Movie("Людина-павук", 148, 12)
shrek = Movie("Шрек", 90, 0)
joker = Movie("Джокер", 122, 18)

cinema = Cinema("Cinema City")

cinema.sessions = [
    Session(spiderman, 150.0, 5),
    Session(shrek, 100.0, 5),
    Session(joker, 170.0, 5)
]

cinema.customers = {
    "Денис": Customer("Денис", 19, 500.0),
    "Саша": Customer("Саша", 14, 300.0),
    "Макс": Customer("Макс", 16, 400.0)
}


print("=== Фільми ===")

for current_session in cinema.sessions:
    current_session.movie.show()
    print("Ціна квитка:", current_session.price, "грн")

    if current_session.movie.is_long():
        print("Довгий фільм")
    else:
        print("Короткий фільм")

    print()


print("=== Клієнти ===")

for current_customer in cinema.customers.values():
    current_customer.show()


print("\n=== Покупки ===")

cinema.buy("Денис", 0)
cinema.buy("Саша", 1)
cinema.buy("Макс", 2)


print("\n=== Квитки ===")

for current_ticket in cinema.tickets:
    current_ticket.show()


print("\n=== Місця на Людину-павука ===")
cinema.sessions[0].show_seats()


print("\n=== Місця на Шрека ===")
cinema.sessions[1].show_seats()


print("\n=== Місця на Джокера ===")
cinema.sessions[2].show_seats()


print("\n--- Звіт ---")
cinema.report()
