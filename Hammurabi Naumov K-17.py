import random
import pickle

class Hamurabi:
    def __init__(self):
        self.turn = 1
        self.population = 1000
        self.grain = 5000
        self.land = 10000
        self.tax_rate = 10
        self.game_over = False

        self.max_grain = self.land * 2
    
    def show_stats(self):
        print(f"Ход: {self.turn}\n" 
              f"Население: {self.population}\n"
              f"Запасы зерна: {self.grain}т\n"
              f"Доступная земля: {self.land}га\n"
              f"Уровень налогов: {self.tax_rate}%\n")
    
    def plant_grain(self):
        acres = int(input("Сколько гектаров земли посеять? "))
        if acres > self.land // 2:
            print("У вас недостаточно земли для посева.")
            return
        grain_used = acres * 2
        if grain_used > self.grain:
            print("У вас недостаточно зерна для посева.")
            return
        self.grain -= grain_used
        self.land -= acres
        print("Вы посадили зерно.")

        # Рандомизируем заболевших
        sick_people = int(self.population * random.randint(5, 10) / 100)
        self.population -= sick_people
        sick_msg = f"\033[91mНа вашум королевстве обрушилась эпидемия! Умерло {sick_people} человек.\033[0m"
        print(sick_msg)

        self.turn += 1
    
    def collect_grain(self):
        acres = int(input("Сколько гектаров земли собрать? "))
        if acres > self.land:
            print("У вас нет такой земли.")
            return
        grain_yield = acres * random.randint(1, 5)
        self.grain += grain_yield
        self.land += acres
        print(f"Вы собрали {grain_yield}т зерна.")

        # Рандомизируем урожай
        poor_harvest = random.choice([True, False])
        if poor_harvest:
            poor_harvest_msg = "\033[91mВ этом году у вас был плохой урожай. Собранное зерно было низкого качества.\033[0m"
            print(poor_harvest_msg)

        self.turn += 1

    def buy_grain(self):
        price_per_ton = random.randint(16, 28)
        print(f"Цена на зерно составляет {price_per_ton} монет за тонну, у вас есть {self.grain}т зерна.")

        tons = int(input("Сколько тонн зерна вы хотите купить? "))
        buy_total_price = tons * price_per_ton
        if buy_total_price > self.population:
            print("У вас недостаточно средств для покупки зерна.")
            return
        self.population -= buy_total_price
        self.grain += tons
        print(f"Вы купили {tons}т зерна за {buy_total_price} монет")

        self.turn += 1

    def sell_grain(self):
        price_per_ton = random.randint(6, 12)
        print(f"Цена на зерно составляет {price_per_ton} монет за тонну, у вас есть {self.grain}т зерна.")

        tons = int(input("Сколько тонн зерна вы хотите продать? "))
        if tons > self.grain:
            print("У вас нет столько зерна.")
            return
        sell_total_price = tons * price_per_ton
        self.population += sell_total_price
        self.grain -= tons
        print(f"Вы продали {tons}т зерна за {sell_total_price} монет")

        self.turn += 1
    
    def sign_treaty(self):
        you_get_grain = int(input("Сколько тонн зерна вы получите? "))
        you_give_away = int(input("Сколько монет/земли вы отдадите? "))

        if self.grain < you_give_away:
            print("У вас недостаточно зерна.")
            return
        if self.land < you_give_away:
            print("У вас недостаточно земли.")
            return
        self.grain -= you_give_away
        self.land -= you_give_away

        treaty_msg = f"Вы получили {you_get_grain}т зерна, отдав {you_give_away} монет и земли."
        print(treaty_msg)

        self.turn += 1

    def declare_war(self):
        enemy_population = int(self.population * random.randint(50, 150) / 100)
        enemy_grain = int(self.grain * random.randint(50, 150) / 100)
        enemy_land = int(self.land * random.randint(10, 30) / 100)

        war_choice = input(f"Ваша армия готова к сражению с противником, который имеет {enemy_population} населения, {enemy_grain}т зерна, и {enemy_land}га земли.\n"
                           "Вы готовы к войне? (y/n)")

        if war_choice.lower() == "y":
            army_win_chance = random.choice([True, False])
            if army_win_chance:
                message = "\033[92mВы победили противника и получили дополнительные зерновые запасы!\033[0m"
                self.grain += enemy_grain
            else:
                message = "\033[91mВы проиграли войну и потеряли значительно населения, запасов зерна и земли.\033[0m"
                self.grain -= enemy_grain
                self.population //= 2
                self.land //= 2
            print(message)
        else:
            print("Вы отказались от войны.")

        self.turn += 1

    def end_game(self):
        self.game_over = True
        print("Игра окончена. Спасибо за игру.")

def save_game(filename):
    with open(filename, 'wb') as out_file:
        pickle.dump(game, out_file)

def load_game(filename):
    with open(filename, 'rb') as in_file:
        return pickle.load(in_file)

game = Hamurabi()

while not game.game_over:
    action = input("Выберите действие:\n"
                   "1 - Посмотреть статистику\n"
                   "2 - Посадить зерно\n"
                   "3 - Собрать урожай\n"
                   "4 - Купить зерно\n"
                   "5 - Продать зерно\n"
                   "6 - Заключить договор с соседним государством\n"
                   "7 - Отправить армию на войну\n"
                   "8 - Завершить игру\n")

    if action == "1":
        game.show_stats()
    elif action == "2":
        game.plant_grain()
    elif action == "3":
        game.collect_grain()
    elif action == "4":
        game.buy_grain()
    elif action == "5":
        game.sell_grain()
    elif action == "6":
        game.sign_treaty()
    elif action == "7":
        game.declare_war()
    elif action == "8":
        save_game("savegame")
        game.end_game()
    elif action.lower() == "load":
        game = load_game("savegame")
        print("Игра загружена.")
    else:
        print("Введите корректное значение.")

save_game("savegame")
