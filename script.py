
from __future__ import annotations


class Car:
    def __init__(self, brand: str, model: str, year: int, price: float, condition: str) -> None:
        self.brand = brand
        self.model = model
        self.year = year
        self.price = float(price)
        self.condition = condition
        self.sold = False
        self.features: set[str] = set()
        self.history: list[str] = []

    def add_feature(self, feature: str) -> None:
        self.features.add(feature)

    def apply_discount(self, percent: float) -> None:
        if not 0 <= percent <= 100:
            print("Знижка має бути від 0 до 100%")
            return

        old_price = self.price
        self.price = round(self.price * (1 - percent / 100), 2)
        self.history.append(f"Знижка {percent:g}%")
        print(f"{self.brand} {self.model}: {old_price:.0f} -> {self.price:.0f} грн")

    def show_info(self) -> None:
        print(f"{self.brand} {self.model} ({self.year}) — {self.price:.0f} грн")
        print(f"Стан: {self.condition}")

        for feature in sorted(self.features):
            print(f"  + {feature}")


class Customer:
    def __init__(self, name: str, age: int, balance: float) -> None:
        self.name = name
        self.age = age
        self.balance = float(balance)
        self.vip = False
        self.cars: list[Car] = []
        self.payments: dict[str, float] = {}
        self.favorites: set[str] = set()

    def add_favorite(self, brand: str) -> None:
        self.favorites.add(brand)

    def can_buy(self, price: float) -> bool:
        return self.age >= 18 and self.balance >= price

    def buy_car(self, car: Car) -> None:
        self.balance -= car.price
        self.cars.append(car)
        self.payments[f"{car.brand} {car.model}"] = car.price

    def show_info(self) -> None:
        print(f"{self.name} ({self.age} років), баланс: {self.balance:.0f} грн")

        for car in self.cars:
            print(f"  Куплено: {car.brand} {car.model}")

        if self.favorites:
            print("  Улюблені марки:", ", ".join(sorted(self.favorites)))


class Dealer:
    def __init__(self, name: str, salary: float) -> None:
        self.name = name
        self.salary = float(salary)
        self.sales_count = 0
        self.active = True
        self.sales: list[Sale] = []
        self.customers: set[str] = set()
        self.bonuses: dict[int, float] = {}

    def add_sale(self, sale: Sale) -> None:
        self.sales.append(sale)
        self.sales_count += 1
        self.customers.add(sale.customer.name)
        self.bonuses[sale.number] = sale.price * 0.01

    def total_bonus(self) -> float:
        total = 0.0

        for bonus in self.bonuses.values():
            total += bonus

        return total

    def show_info(self) -> None:
        print(f"Продавець: {self.name}, продажів: {self.sales_count}")

        for sale in self.sales:
            print(f"  {sale.car.brand} {sale.car.model}")

        print(f"Бонуси: {self.total_bonus():.0f} грн")


class Garage:
    def __init__(self, capacity: int) -> None:
        self.name = "AutoCity Garage"
        self.capacity = capacity
        self.repair_price = 5000.0
        self.opened = True
        self.queue: list[Car] = []
        self.records: dict[str, str] = {}
        self.brands: set[str] = set()

    def add_car(self, car: Car) -> bool:
        if not self.opened or len(self.queue) >= self.capacity or car in self.queue:
            print("Не вдалося додати автомобіль у гараж")
            return False

        self.queue.append(car)
        self.brands.add(car.brand)
        print(f"{car.brand} {car.model} додано в гараж")
        return True

    def finish_repair(self, car: Car) -> None:
        if car in self.queue:
            self.queue.remove(car)
            self.records[f"{car.brand} {car.model}"] = "Відремонтовано"

    def show_queue(self) -> None:
        print("\n=== ЧЕРГА НА РЕМОНТ ===")

        if not self.queue:
            print("Черга порожня")

        for car in self.queue:
            print(f"{car.brand} {car.model}")


class Mechanic:
    def __init__(self, name: str) -> None:
        self.name = name
        self.experience = 5
        self.salary = 25000.0
        self.available = True
        self.repairs: list[Car] = []
        self.skills: set[str] = {"Двигун", "Гальма"}
        self.work_log: dict[str, float] = {}

    def add_skill(self, skill: str) -> None:
        self.skills.add(skill)

    def repair(self, car: Car, garage: Garage) -> None:
        if car not in garage.queue or not self.available:
            print("Ремонт зараз неможливий")
            return

        car.condition = "Хороший"
        car.history.append("Ремонт")
        self.repairs.append(car)
        self.work_log[f"{car.brand} {car.model}"] = garage.repair_price

        garage.finish_repair(car)
        print(f"{self.name} відремонтував {car.brand} {car.model}")

    def show_info(self) -> None:
        print(f"Механік: {self.name}, ремонтів: {len(self.repairs)}")

        for car in self.repairs:
            print(f"  {car.brand} {car.model}")


class Sale:
    def __init__(self, number: int, car: Car, customer: Customer, dealer: Dealer) -> None:
        self.number = number
        self.car = car
        self.customer = customer
        self.dealer = dealer
        self.price = car.price
        self.completed = True
        self.services: list[str] = []
        self.details: dict[str, str] = {}
        self.tags: set[str] = set()

    def add_service(self, service: str) -> None:
        self.services.append(service)
        self.tags.add("Додаткова послуга")

    def make_receipt(self) -> None:
        self.details = {
            "Автомобіль": f"{self.car.brand} {self.car.model}",
            "Покупець": self.customer.name,
            "Продавець": self.dealer.name,
            "Ціна": f"{self.price:.0f} грн",
        }

    def show_receipt(self) -> None:
        print(f"\n--- ЧЕК №{self.number} ---")

        for key, value in self.details.items():
            print(f"{key}: {value}")

        for service in self.services:
            print(f"Послуга: {service}")


class Showroom:
    def __init__(self, name: str) -> None:
        self.name = name
        self.capacity = 10
        self.revenue = 0.0
        self.opened = True
        self.cars: list[Car] = []
        self.sales: list[Sale] = []
        self.customers: dict[str, Customer] = {}
        self.brands: set[str] = set()

    def add_car(self, car: Car) -> None:
        if len(self.cars) >= self.capacity or car in self.cars:
            print("Немає місця або автомобіль уже доданий")
            return

        self.cars.append(car)
        self.brands.add(car.brand)

    def show_cars(self) -> None:
        print("\n=== АВТОМОБІЛІ В ПРОДАЖУ ===")

        for car in self.cars:
            if not car.sold:
                car.show_info()
                print()

    def sell_car(self, car: Car, customer: Customer, dealer: Dealer) -> bool:
        if not self.opened or not dealer.active:
            print("Автосалон або продавець недоступні")
            return False

        if car not in self.cars:
            print(
                f"{customer.name} хотів купити {car.brand} {car.model}, "
                f"але автомобіля немає в салоні"
            )
            return False

        if car.sold:
            print(
                f"{customer.name} хотів купити {car.brand} {car.model}, "
                f"але автомобіль уже продано"
            )
            return False

        if car.condition != "Хороший":
            print(
                f"{customer.name} хотів купити {car.brand} {car.model}, "
                f"але автомобіль потребує ремонту"
            )
            return False

        if customer.age < 18:
            print(
                f"{customer.name} хотів купити {car.brand} {car.model}, "
                f"але покупка недоступна за віком ({customer.age} років)"
            )
            return False

        if not customer.can_buy(car.price):
            print(
                f"{customer.name} хотів купити {car.brand} {car.model}, "
                f"але недостатньо грошей"
            )
            return False

        sale = Sale(len(self.sales) + 1, car, customer, dealer)
        sale.add_service("Оформлення документів")
        sale.make_receipt()

        customer.buy_car(car)
        car.sold = True
        self.sales.append(sale)
        dealer.add_sale(sale)
        self.revenue += sale.price
        self.customers[customer.name] = customer

        print(f"{customer.name} купив {car.brand} {car.model}")
        return True

    def report(self) -> None:
        print("\n=== ЗВІТ АВТОСАЛОНУ ===")
        print("Продано машин:", len(self.sales))
        print(f"Виручка: {self.revenue:.0f} грн")

        available = 0

        for car in self.cars:
            if not car.sold:
                available += 1

        print("Залишилося машин:", available)

        for sale in self.sales:
            sale.show_receipt()


def main() -> None:
    showroom = Showroom("AutoCity")
    garage = Garage(3)
    mechanic = Mechanic("Іван")
    dealer = Dealer("Олег", 20000)

    car1 = Car("BMW", "M5", 2020, 1500000, "Хороший")
    car2 = Car("Audi", "RS7", 2021, 1800000, "Потребує ремонту")
    car3 = Car("Toyota", "Camry", 2018, 700000, "Хороший")
    car4 = Car("Mercedes", "E63", 2022, 2100000, "Хороший")

    car1.add_feature("Шкіряний салон")
    car1.add_feature("Камера")
    car2.add_feature("Повний привід")
    car3.add_feature("Клімат-контроль")
    car4.add_feature("Підігрів сидінь")

    for car in [car1, car2, car3, car4]:
        showroom.add_car(car)

    customer1 = Customer("Денис", 20, 2000000)
    customer2 = Customer("Саша", 19, 900000)
    customer3 = Customer("Макс", 17, 3000000)
    customer4 = Customer("Артем", 25, 2500000)

    customer1.add_favorite("BMW")
    customer2.add_favorite("Toyota")
    customer3.add_favorite("Mercedes")
    customer4.add_favorite("Audi")

    showroom.show_cars()

    print("\n=== РЕМОНТ ===")
    garage.add_car(car2)
    garage.show_queue()
    mechanic.repair(car2, garage)

    print("\n=== ЗНИЖКИ ===")
    car2.apply_discount(10)

    print("\n=== ПОКУПКИ ===")

    orders = [
        (car1, customer1),
        (car3, customer2),
        (car4, customer3),
        (car2, customer4),
        (car1, customer2),
    ]

    index = 0

    while index < len(orders):
        car, customer = orders[index]
        showroom.sell_car(car, customer, dealer)
        index += 1

    print("\n=== КЛІЄНТИ ===")

    for customer in [customer1, customer2, customer3, customer4]:
        customer.show_info()
        print()

    showroom.show_cars()

    print("\n=== ПРАЦІВНИКИ ===")
    dealer.show_info()
    mechanic.show_info()

    showroom.report()


if __name__ == "__main__":
    main()
