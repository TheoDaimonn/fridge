import telebot
from others import *
from telebot import types
bot = telebot.TeleBot("5287199162:AAGPWx8TlcZfLFOik1eKWVaa3nFLE8nDZ5c", parse_mode=None)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    adding_statement(str(message.chat.id) + ' 1')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    callback_button = types.InlineKeyboardButton(text="ну что ж, начнем", callback_data="1")
    keyboard.add(callback_button)

    bot.send_message(message.chat.id,  '''
Добро пожаловать!
Это бот "мой холодильник", призванный упростить вашу жизнь, порадовать себя и близких вкуснейшими, необычными рецептами из того, что есть у вас дома''', reply_markup=keyboard)


@bot.message_handler()
def start_proccesing(message):
    st = check_statement(message.chat.id)

    if st == '1' and message.text != 'Начать процесс поиска рецептов по вашим компонентам':
        markup = types.ReplyKeyboardMarkup()
        itembtn1 = types.KeyboardButton('Начать процесс поиска рецептов компонентам')
        itembtn2 = types.KeyboardButton('Оформить ежемесячную подписку на наш сервис')
        markup.add(itembtn1, itembtn2)
        bot.send_message(message.chat.id, """Инструкция по работе с ботом:
1)Заполнить список того, что у вас есть, вбивая поочередно все компоненты(только алкоголь, фрукты\специи\овощи\соки бот не учитывает)
2)выбрать из списка предложенных рецептов тот, который вам по душе, увидев коктейль, который вы бы хотели выпить.
3)насладиться вкуснейшим коктейлем. Здесь вы можете найти как классику так и нечто новое:)

P.S. наличие шейкера не обязательно, если у вас достаточно умелые руки)""", reply_markup=markup)

    elif message.text == 'Начать процесс поиска рецептов по вашим компонентам':
        replace_statement(str(message.chat.id), ' 2')
        bot.send_message(message.chat.id, 'Прекрасно, теперь присылайте список того, что у вас есть(1 сообщение - 1 компонент)')

    elif message.text == 'Остановить добавление компонентов':
        replace_statement(str(message.chat.id), '4')
        #тут будет поиск рецептов!!!!!!!

    elif st == '2':
        markup = types.ReplyKeyboardMarkup()
        for t in best_of_five(message.text):
            markup.add(t)
        markup.add('Нет в списке')
        bot.send_message(message.chat.id, "Выберите правильный вариант, в противном случае, бот не сможет учитывать данный компонент", reply_markup=markup)
        replace_statement(str(message.chat.id), ' 3')

    elif st == '3' and message.text == 'Нет в списке':
        bot.send_message(message.chat.id, 'Жаль, тогда придется пропустить данный компонент. продолжайте ввод')
        replace_statement(str(message.chat.id), ' 2')

    elif st == '3':
        add_to_cart(str(message.chat.id),message.text)
        replace_statement(str(message.chat.id), ' 2')
        bot.send_message(message.chat.id, 'Прдолжайте в том же духе!')
        bucket = open('pplfood', 'r').readlines()
        for k in bucket:
            if str(message.chat.id) == k.split('|')[0]:
                bucket = '\n'.join(k.split('|')[1::])
                break
        markup = types.ReplyKeyboardMarkup()
        itembtn1 = types.KeyboardButton('Остановить добавление компонентов')
        markup.add(itembtn1)
        bot.send_message(message.chat.id, 'Ваш бар: \n' + bucket, reply_markup=markup)
bot.infinity_polling()

#по итогу 1 дня мы сформировали приветствие, старт сбора данных об ингридиентах, разработали алгоритм подбора пяти и работы с фазами