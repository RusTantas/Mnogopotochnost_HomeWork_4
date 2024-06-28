"""Задание:
Моделирование работы сети кафе с несколькими столиками и потоком посетителей, прибывающих для заказа пищи и уходящих после завершения приема.

Есть сеть кафе с несколькими столиками. Посетители приходят, заказывают еду, занимают столик, употребляют еду и уходят. Если столик свободен, новый посетитель принимается к обслуживанию, иначе он становится в очередь на ожидание.

Создайте 3 класса:
Table - класс для столов, который будет содержать следующие атрибуты: number(int) - номер стола, is_busy(bool) - занят стол или нет.

Cafe - класс для симуляции процессов в кафе. Должен содержать следующие атрибуты и методы:
Атрибуты queue - очередь посетителей (создаётся внутри init), tables список столов (поступает из вне).
Метод customer_arrival(self) - моделирует приход посетителя(каждую секунду).
Метод serve_customer(self, customer) - моделирует обслуживание посетителя. Проверяет наличие свободных столов, в случае наличия стола - начинает обслуживание посетителя (запуск потока), в противном случае - посетитель поступает в очередь. Время обслуживания 5 секунд.
Customer - класс (поток) посетителя. Запускается, если есть свободные столы.

Так же должны выводиться текстовые сообщения соответствующие событиям:
Посетитель номер <номер посетителя> прибыл.
Посетитель номер <номер посетителя> сел за стол <номер стола>. (начало обслуживания)
Посетитель номер <номер посетителя> покушал и ушёл. (конец обслуживания)
Посетитель номер <номер посетителя> ожидает свободный стол. (помещение в очередь)

Пример работы:
# Создаем столики в кафе
table1 = Table(1)
table2 = Table(2)
table3 = Table(3)
tables = [table1, table2, table3]

# Инициализируем кафе
cafe = Cafe(tables)

# Запускаем поток для прибытия посетителей
customer_arrival_thread = threading.Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()

# Ожидаем завершения работы прибытия посетителей
customer_arrival_thread.join()

Вывод на консоль (20 посетителей [ограничение выставить в методе customer_arrival]):
Посетитель номер 1 прибыл
Посетитель номер 1 сел за стол 1
Посетитель номер 2 прибыл
Посетитель номер 2 сел за стол 2
Посетитель номер 3 прибыл
Посетитель номер 3 сел за стол 3
Посетитель номер 4 прибыл
Посетитель номер 4 ожидает свободный стол
Посетитель номер 5 прибыл
Посетитель номер 5 ожидает свободный стол
......
Посетитель номер 20 прибыл
Посетитель номер 20 ожидает свободный стол
Посетитель номер 17 покушал и ушёл.
Посетитель номер 20 сел за стол N.
Посетитель номер 18 покушал и ушёл.
Посетитель номер 19 покушал и ушёл.
Посетитель номер 20 покушал и ушёл.
"""





import threading
import time
from queue import Queue

# Класс для столов
class Table:
    def __init__(self, number):
        self.number = number
        self.is_busy = False

# Класс для симуляции работы кафе
class Cafe:
    def __init__(self, tables):
        self.queue = Queue()
        self.tables = tables

    def customer_arrival(self):
        customer_number = 1
        while customer_number <= 10:
            print(f"Посетитель номер {customer_number} прибыл.")
            customer_thread = Customer(customer_number, self)
            customer_thread.start()  # Используем start() для начала потока
            customer_number += 1
            time.sleep(1)  # Искусственная задержка между приходами посетителей

    def serve_customer(self, customer):
        table_found = False
        for table in self.tables:
            if not table.is_busy:
                table.is_busy = True
                print(f"Посетитель номер {customer.number} сел за стол {table.number}. (начало обслуживания)")
                time.sleep(5)  # Время обслуживания 5 секунд
                table.is_busy = False  # Освободили столик после обслуживания
                print(f"Посетитель номер {customer.number} покушал и ушёл.(конец обслуживания)")
                table_found = True
                break
        if not table_found:
            print(f"Посетитель номер {customer.number} ожидает свободный стол. ")
            self.queue.put(customer)
            self.queue.get()
            time.sleep(3)
            for table in self.tables:
                if not table.is_busy:
                    table.is_busy = True
                    print(f"Посетитель номер {customer.number} сел за стол {table.number}. (начало обслуживания)")
                    time.sleep(5)  # Время обслуживания 5 секунд
                    table.is_busy = False  # Освободили столик после обслуживания
                    print(f"Посетитель номер {customer.number} покушал и ушёл.(конец обслуживания)")
                    table_found = True



# Класс для посетителей
class Customer(threading.Thread):
    def __init__(self, number, cafe):
        super().__init__()
        self.number = number
        self.cafe = cafe

    def run(self):
        self.cafe.serve_customer(self)

# Создаем столы в кафе
table1 = Table(1)
table2 = Table(2)
table3 = Table(3)
tables = [table1, table2, table3]

# Инициализируем кафе
cafe = Cafe(tables)

# Запускаем поток для прибытия посетителей
customer_arrival_thread = threading.Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()

# Ожидаем завершения работы прибытия посетителей
customer_arrival_thread.join()