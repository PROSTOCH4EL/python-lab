
# 1. Клас для автомобіля
class Vehicle:

  def __init__(self, plate: str):
    self.plate: str = plate


# 2. Клас для фіксації початку сесії
class ParkingSession:

  def __init__(self, plate: str, start_minute: int):
    self.plate: str = plate
    self.start_minute: int = start_minute


# 3. Клас для розрахунку вартості
class FeeCalculator:

  @staticmethod
  def calculate(parking_time: int, hourly_rate: float) -> float:
    if parking_time <= 15:
      return 0.0
    hours = (parking_time + 59) // 60
    return float(hours * hourly_rate)


# 4. Клас для керування історією
class ParkingHistory:

  def __init__(self):
    self.records: list[tuple[str, int, float]] = []

  def add(self, record: tuple[str, int, float]):
    self.records.append(record)


# 5. Головний клас парковки (менеджер)
class ParkingLot:

  def __init__(self, capacity: int, hourly_rate: float):
    self.capacity: int = capacity
    self.hourly_rate: float = hourly_rate
    self.parked: dict[str, int] = {}
    self.history: ParkingHistory = ParkingHistory()

  def enter(self, plate: str, minutes: int):
    if plate in self.parked:
      print(f"{plate}: уже на стоянці")
    elif len(self.parked) >= self.capacity:
      print(f"{plate}: немає вільних місць")
    else:
      self.parked[plate] = minutes
      h = minutes // 60
      m = minutes % 60
      print(f"{plate}: в'їзд о {h:02d}:{m:02d}")

  def leave(self, plate: str, minutes: int):
    if plate not in self.parked:
      print(f"{plate}: автомобіль не знайдено")
      return

    start_minute = self.parked.pop(plate)
    parking_time = minutes - start_minute

    fee = FeeCalculator.calculate(parking_time, self.hourly_rate)

    self.history.add((plate, parking_time, fee))
    print(f"{plate}: {parking_time} хв, до сплати {fee:.2f} грн")

  def total_revenue(self) -> float:
    # Використовуємо вбудований sum() замість дублюючого циклу
    return sum(record[2] for record in self.history.records)

  def longest_stay(self) -> tuple[str, int, float] | None:
    if not self.history.records:
      return None
    # Використовуємо вбудований max() для пошуку за хвилинами (індекс 1)
    return max(self.history.records, key=lambda x: x[1])


# --- Тестування програми ---
lot = ParkingLot(2, 40.0)

lot.enter("AB1234CD", 9 * 60)
lot.enter("AI7777AA", 10 * 60)
lot.enter("BX0001BX", 11 * 60)  # Немає місць

lot.leave("AB1234CD", 12 * 60)
lot.enter("BX0001BX", 12 * 60)

print("Зайнято місць:", len(lot.parked))
print(f"Загальна виручка: {lot.total_revenue():.2f} грн")

longest_car = lot.longest_stay()
if longest_car is not None:
  print(f"Найдовше стояв: {longest_car[0]}, {longest_car[1]} хв")
