
from __future__ import annotations


class Car:
    def __init__(self, brand, model, year, price, condition):
        self.brand = brand
        self.model = model
        self.year = year
        self.price = float(price)
        self.condition = condition
        self.sold = False
        self.features = set()

    def add_feature(self, feature):
        self.features.add(feature)

    def apply_discount(self, percent):
        if percent < 0 or percent > 100:
            print("Неправильна знижка")
        else:
            old_price = self.price
            self.price = round(self.price * (1 - percent / 100), 2)
            print(f"{self.brand} {self.model}: {old_price:.0f} -> {self.price:.0f} грн")

    def show_info(self):
        print(f"{self.brand} {self.model} ({self.year}) — {self.price:.0f} грн")
        print(f"Стан: {self.condition}")
        for feature in sorted(self.features):
            print(f"  + {feature}")


class Customer:
    def __init__(self, name, age, balance):
        self.name = name
        self.age = age
        self.balance = float(balance)
        self.cars = []
        self.payments = {}
        self.favorites = set()

    def add_favorite(self, brand):
        self.favorites.add(brand)

    def can_buy(self, price):
        return self.age >= 18 and self.balance >= price

    def buy_car(self, car, price):
        self.balance -= price
        self.cars.append(car)
        self.payments[f"{car.brand} {car.model}"] = price

    def show_info(self):
        print(f"{self.name} ({self.age} років)")
        print(f"Баланс: {self.balance:.0f} грн")
        for car in self.cars:
            print(f"  Куплено: {car.brand} {car.model}")
        if self.favorites:
            print("  Улюблені марки:", ", ".join(sorted(self.favorites)))


class Dealer:
    def __init__(self, name, salary):
        self.name = name
        self.salary = float(salary)
        self.sales_count = 0
        self.active = True
        self.sales = []
        self.customers = set()
        self.bonuses = {}

    def add_sale(self, sale):
        self.sales.append(sale)
        self.sales_count += 1
        self.customers.add(sale.customer.name)
        self.bonuses[sale.number] = sale.price * 0.01

    def total_bonus(self):
        total = 0.0
        for bonus in self.bonuses.values():
            total += bonus
        return total

    def show_info(self):
        print(f"Продавець: {self.name}")
        print(f"Зарплата: {self.salary:.0f} грн")
        print(f"Продажів: {self.sales_count}")
        print(f"Клієнтів: {len(self.customers)}")
        print(f"Бонуси: {self.total_bonus():.0f} грн")
        for sale in self.sales:
            print(f"  Продано: {sale.car.brand} {sale.car.model}")


class Garage:
    def __init__(self, capacity):
        self.name = "AutoCity Garage"
        self.capacity = capacity
        self.repair_price = 5000.0
        self.opened = True
        self.queue = []
        self.records = {}
        self.brands = set()

    def add_car(self, car):
        if not self.opened:
            print("Гараж зачинений")
            return False
        elif len(self.queue) >= self.capacity:
            print("Гараж заповнений")
            return False
        elif car in self.queue:
            print("Автомобіль уже в черзі")
            return False
        else:
            self.queue.append(car)
            self.brands.add(car.brand)
            print(f"{car.brand} {car.model} додано в гараж")
            return True

    def finish_repair(self, car):
        if car in self.queue:
            self.queue.remove(car)
            self.records[f"{car.brand} {car.model}"] = "Відремонтовано"

    def show_queue(self):
        print("\n=== ЧЕРГА НА РЕМОНТ ===")
        if not self.queue:
            print("Черга порожня")
        else:
            for car in self.queue:
                print(f"{car.brand} {car.model}")


class Mechanic:
    def __init__(self, name):
        self.name = name
        self.salary = 25000.0
        self.available = True
        self.repairs = []
        self.skills = {"Двигун", "Гальма"}
        self.work_log = {}

    def add_skill(self, skill):
        self.skills.add(skill)

    def repair(self, car, garage):
        if not self.available:
            print("Механік зайнятий")
        elif car not in garage.queue:
            print("Автомобіля немає в гаражі")
        else:
            car.condition = "Хороший"
            self.repairs.append(car)
            self.work_log[f"{car.brand} {car.model}"] = garage.repair_price
            garage.finish_repair(car)
            print(f"Вартість ремонту: {garage.repair_price:.0f} грн")
            print(f"{self.name} відремонтував {car.brand} {car.model}")

    def show_info(self):
        print(f"Механік: {self.name}")
        print(f"Зарплата: {self.salary:.0f} грн")
        print("Доступний:", "Так" if self.available else "Ні")
        print("Навички:", ", ".join(sorted(self.skills)))
        print(f"Ремонтів: {len(self.repairs)}")
        for name, price in self.work_log.items():
            print(f"  {name}: {price:.0f} грн")


class Sale:
    def __init__(self, number, car, customer, dealer, price):
        self.number = number
        self.car = car
        self.customer = customer
        self.dealer = dealer
        self.price = price
        self.services = []
        self.details = {}

    def add_service(self, service):
        self.services.append(service)

    def make_receipt(self):
        self.details = {
            "Автомобіль": f"{self.car.brand} {self.car.model}",
            "Покупець": self.customer.name,
            "Продавець": self.dealer.name,
            "Ціна": f"{self.price:.0f} грн",
        }

    def show_receipt(self):
        print(f"\n--- ЧЕК №{self.number} ---")
        for key, value in self.details.items():
            print(f"{key}: {value}")
        for service in self.services:
            print(f"Послуга: {service}")


class Showroom:
    def __init__(self, name):
        self.name = name
        self.capacity = 10
        self.revenue = 0.0
        self.opened = True
        self.cars = []
        self.sales = []
        self.customers = {}

    def add_car(self, car):
        if len(self.cars) >= self.capacity:
            print("У салоні немає місця")
        elif car in self.cars:
            print("Автомобіль уже доданий")
        else:
            self.cars.append(car)

    def show_cars(self):
        print("\n=== АВТОМОБІЛІ В ПРОДАЖУ ===")
        for car in self.cars:
            if not car.sold:
                car.show_info()
                print()

    def sell_car(self, car, customer, dealer):
        if not self.opened or not dealer.active:
            print("Автосалон або продавець недоступні")
            return False
        elif car not in self.cars:
            print(f"{customer.name} хотів купити {car.brand} {car.model}, але автомобіля немає")
            return False
        elif car.sold:
            print(f"{customer.name} хотів купити {car.brand} {car.model}, але автомобіль уже продано")
            return False
        elif car.condition != "Хороший":
            print(f"{customer.name} хотів купити {car.brand} {car.model}, але потрібен ремонт")
            return False
        elif customer.age < 18:
            print(f"{customer.name} хотів купити {car.brand} {car.model}, але покупка недоступна за віком")
            return False
        else:
            final_price = car.price

            if not customer.can_buy(final_price):
                print(f"{customer.name} хотів купити {car.brand} {car.model}, але недостатньо грошей")
                return False

            sale = Sale(len(self.sales) + 1, car, customer, dealer, final_price)
            sale.add_service("Оформлення документів")
            sale.make_receipt()

            customer.buy_car(car, final_price)
            car.sold = True
            self.sales.append(sale)
            dealer.add_sale(sale)
            self.revenue += final_price
            self.customers[customer.name] = customer

            print(f"{customer.name} купив {car.brand} {car.model} за {final_price:.0f} грн")
            return True

    def report(self):
        print("\n=== ЗВІТ АВТОСАЛОНУ ===")
        print("Продано машин:", len(self.sales))
        print(f"Виручка: {self.revenue:.0f} грн")

        available = 0
        for car in self.cars:
            if not car.sold:
                available += 1

        print("Залишилося машин:", available)
        print("Покупців:", len(self.customers))

        for sale in self.sales:
            sale.show_receipt()


def main():
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
    mechanic.add_skill("Електроніка")
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

    print("\n=== ПРАЦІВНИКИ ===")
    dealer.show_info()
    mechanic.show_info()
    showroom.report()


if __name__ == "__main__":
    main()
