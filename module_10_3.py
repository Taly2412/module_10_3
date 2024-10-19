from random import randint
import time
from threading import Thread, Lock

lock = Lock()


class Bank:
    def __init__(self):
        self.balance = 0

    def deposit(self):
        for i in range(100):
            rep = randint(50, 500)
            with Lock():
                self.balance += rep
                print(f"Пополнение: {rep}. Баланс: {self.balance}")
                if self.balance >= 500 and lock.locked():
                    lock.release()
            time.sleep(0.001)

    def take(self):
        for i in range(100):
            rep = randint(50, 500)
            print(f"Запрос на {rep}")
            with Lock():
                if rep <= self.balance:
                    self.balance -= rep
                    print(f"Снятие: {rep}. Баланс: {self.balance}")
                else:
                    print("Запрос отклонён, недостаточно средств")
                    lock.acquire()
            time.sleep(0.001)


bk = Bank()
th1 = Thread(target=Bank.deposit, args=(bk,))
th2 = Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')
