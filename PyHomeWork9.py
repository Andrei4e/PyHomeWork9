import telebot
import random
from telebot import types

bot = telebot.TeleBot("6138342216:AAHw1_gwU1-BdQ7uM6kCbudM2yD227WayVM")

candies = 150
maxCandies = 28
candiesPlayer = 0
candiesBot = 0
flag = ""

@bot.message_handler(commands = ["start"])
def start(message):
    bot.send_message(message.chat.id, "hello)")


@bot.message_handler(commands = ["startGame"])
def startGame(message):
    global flag, candies
    candies = 150
    bot.send_message(message.chat.id, "Начинаем игру")
    bot.send_message(message.chat.id, f"В игре {candies} конфет")
    flag = random.choice(["player", "bot"])
    bot.send_message(message.chat.id, f"Первым ходит {flag}")
    Controller(message)


def Controller(message):
    global flag
    if candies > 0:
        if flag == "player":
            bot.send_message(message.chat.id, f"Вы ходите, введите количество конфет от 0 до {maxCandies}")
            bot.register_next_step_handler(message, PlayerMove)
        else:
            BotMove(message)
    else:
        flag = "player" if flag == "bot" else "bot"
        bot.send_message(message.chat.id, f"Победил {flag}")        

def PlayerMove(message):
    global flag, candies, candiesPlayer
    candiesPlayer = int(message.text)
    candies -= candiesPlayer
    flag = "player" if flag == "bot" else "bot"
    Controller(message)

def BotMove(message):
    global flag, candies, candiesBot
    if candies <= maxCandies:
        candiesBot = candies
    elif candies % maxCandies == 0:
        candiesBot = maxCandies -1
    else:
        candiesBot = candies % maxCandies - 1
        if candiesBot == 0:
            candiesBot = 1
    candies -= candiesBot
    bot.send_message(message.chat.id, f"bot взял {candiesBot} конфет")
    bot.send_message(message.chat.id, f"Осталось {candies} конфет")
    flag = "player" if flag == "bot" else "bot"
    Controller(message)


bot.infinity_polling()