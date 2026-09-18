# 1. Клас для автомобіля
class Vehicle:

  def __init__(self, plate):
    self.plate = plate


# 2. Клас для фіксації початку сесії
class ParkingSession:

  def __init__(self, plate, start_minute):
    self.plate = plate
    self.start_minute = start_minute


# 3. Клас для розрахунку вартості (з 15 хв безкоштовно)
class FeeCalculator:

  @staticmethod
  def calculate(parking_time, hourly_rate):
    if parking_time <= 15:
      return 0.0
    # Округлюємо хвилини до годин у більшу сторону
    hours = (parking_time + 59) // 60
    return hours * hourly_rate


# 4. Клас для керування історією
class ParkingHistory:

  def __init__(self):
    self.records = []  # список кортежів з історією

  def add(self, record):
    self.records.append(record)


# 5. Головний клас парковки (менеджер)
class ParkingLot:

  def __init__(self, capacity, hourly_rate):
    self.capacity = capacity
    self.hourly_rate = hourly_rate
    self.parked = {}  # словник: номер -> хвилини в'їзду
    self.history = ParkingHistory()  # об'єкт історії

  def enter(self, plate, minutes):
    if plate in self.parked:
      print(f"{plate}: уже на стоянці")
    elif len(self.parked) >= self.capacity:
      print(f"{plate}: немає вільних місць")
    else:
      self.parked[plate] = minutes
      h = minutes // 60
      m = minutes % 60
      print(f"{plate}: в'їзд о {h:02d}:{m:02d}")

  def leave(self, plate, minutes):
    if plate not in self.parked:
      print(f"{plate}: автомобіль не знайдено")
      return

    start_minute = self.parked.pop(plate)
    parking_time = minutes - start_minute

    # Використовуємо інший клас для підрахунку ціни
    fee = FeeCalculator.calculate(parking_time, self.hourly_rate)

    self.history.add((plate, parking_time, fee))
    print(f"{plate}: {parking_time} хв, до сплати {fee:.2f} грн")

  def total_revenue(self):
    total = 0.0
    for record in self.history.records:
      total += record[2]  # сума лежить на 3-му місці (індекс 2)
    return total

  def longest_stay(self):
    if not self.history.records:
      return None
    longest = self.history.records[0]
    for record in self.history.records:
      if record[1] > longest[1]:  # порівнюємо хвилини (індекс 1)
        longest = record
    return longest


# --- Тестування програми ---
lot = ParkingLot(2, 40.0)

lot.enter("AB1234CD", 9 * 60)
lot.enter("AI7777AA", 10 * 60)
lot.enter("BX0001BX", 11 * 60)  # Немає місць

lot.leave("AB1234CD", 12 * 60)
lot.enter("BX0001BX", 12 * 60)

print("Зайнято місць:", len(lot.parked))
print(f"Загальна виручка: {lot.total_revenue():.2f} грн")

longest = lot.longest_stay()
if longest:
  print(f"Найдовше стояв: {longest[0]}, {longest[1]} хв")
