import cleaner
import random
import telebot
from telebot import types
from others import *
from payment_dict import *

bot = telebot.TeleBot("5287199162:AAGPWx8TlcZfLFOik1eKWVaa3nFLE8nDZ5c", parse_mode=None)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    adding_statement(str(message.chat.id) + ' 1')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    callback_button = types.InlineKeyboardButton(text="ну что ж, начнем", callback_data="1")
    keyboard.add(callback_button)

    bot.send_message(message.chat.id, '''Добро пожаловать! Это бот "мой бар", призванный упростить вашу жизнь, 
    порадовать себя и близких вкуснейшими, необычными рецептами из того, что есть у вас дома''',
                     reply_markup=keyboard)


@bot.message_handler()
def start_proccesing(message):
    st = check_statement(message.chat.id)
    don_status = check_don(message.chat.id)
    if st == '1' and message.text != 'Начать процесс поиска рецептов по вашим компонентам' and message.text != 'Оформить ежемесячную подписку на наш сервис' or message.text == '/start' or message.text == 'Вернуться на начальное окно':
        replace_statement(message.chat.id, ' 1')
        markup = types.ReplyKeyboardMarkup()
        itembtn1 = types.KeyboardButton('Начать процесс поиска рецептов по вашим компонентам')
        itembtn2 = types.KeyboardButton('Оформить ежемесячную подписку на наш сервис')
        markup.add(itembtn1, itembtn2)
        bot.send_message(message.chat.id, """Инструкция по работе с ботом:
1)Заполнить список того, что у вас есть, вбивая поочередно все компоненты(только алкоголь, фрукты\специи\овощи\соки бот не учитывает)
2)выбрать из списка предложенных рецептов тот, который вам по душе, увидев коктейль, который вы бы хотели выпить.
3)насладиться вкуснейшим коктейлем. Здесь вы можете найти как классику так и нечто новое:)

P.S. наличие шейкера не обязательно, если у вас достаточно умелые руки)
P.P.S. Вы можете оформить подписку на наш сервис за 30р, чтобы обеспечить себе пожиззненный PRO status, добавляющий вас в особый канал спонсоров и снимающий ограничение на количество использований бота в день
P.P.P.S. Оформлять подписку можно многократно в целях поддержать наш проект.""", reply_markup=markup)
    elif st == '1' and message.text == 'Оформить ежемесячную подписку на наш сервис':
        markup = types.ReplyKeyboardMarkup()
        itembtn1 = types.KeyboardButton('Вернуться на начальное окно')
        itembtn2 = types.KeyboardButton('Проверить оплату')
        markup.add(itembtn1, itembtn2)
        current_url = create_de_trans(message.chat.id)
        bot.send_message(message.chat.id, 'Ссылка для оплаты:' + current_url, reply_markup=markup)
        replace_statement(message.chat.id, ' 5')


    elif st == '5' and message.text == 'Проверить оплату':
        itog = check_status(message.chat.id)
        if itog == 'PAID':
            a = open('dons', 'r').readline()
            a += str(message.chat.id) + '|'
            replace_statement(message.chat.id, ' 1')
            b = open('dons', 'w')
            b.write(a)
            b.close()
            bot.send_message(message.chat.id, '''
Оплата прошла успешно!
Ссылка на чат донов: https://t.me/+06Ck1ywrqBgzZTY6
Благодарим за покупку и удачного пользования
(Для перехода на начальный экран отправьте любое сообщение)
''')
        elif itog == 'WAITING':
            markup = types.ReplyKeyboardMarkup()
            itembtn1 = types.KeyboardButton('Вернуться на начальное окно')
            itembtn2 = types.KeyboardButton('Проверить оплату')
            markup.add(itembtn1, itembtn2)
            bot.send_message(message.chat.id, 'Оплата пока не прошла, повторите нажатие кнопки через несколько секунд',
                             reply_markup=markup)
        else:
            replace_statement(message.chat.id, ' 1')
            bot.send_message(message.chat.id, 'К сожалению, срок оплаты уже прошел. Повторите снова чуть позже')



    elif st == '4':
        f = open(message.text, 'r', encoding='utf-8')
        bot.send_message(message.chat.id, ''.join(f))
        bot.send_photo(message.chat.id, open(message.text + '.jpg', 'rb'))
        replace_statement(str(message.chat.id), ' 1')
        bot.send_message(message.chat.id, 'Для продолжения отправьте любое сообщение:)')
        discard_pplfood(message.chat.id)
        if don_status == 0:
            e = open('already used', 'r').readline().split('|')
            t = open('already used', 'w')
            t.write('|'.join(e) + str(message.chat.id) + '|')
        pass

    elif message.text == 'Начать процесс поиска рецептов по вашим компонентам':
        e = open('already used', 'r').readline().split('|')
        if str(message.chat.id) not in e:
            replace_statement(str(message.chat.id), ' 2')
            bot.send_message(message.chat.id,
                             'Прекрасно, теперь присылайте список того, что у вас есть(1 сообщение - 1 компонент)')
        else:
            bot.send_message(message.chat.id,
                             'Вы уже использовали бота сегодня. Подождите до 00:00 по Мск времени, чтобы обновилась ваша попытка или оформите донство')


    elif message.text == 'Остановить добавление компонентов' and st == '2':
        cocktails = searching(message.chat.id)
        if len(cocktails) == 0:
            replace_statement(message.chat.id, ' 1')
            discard_pplfood(message.chat.id)
            bot.send_message(message.chat.id,'К сожалению по вашим ингридиентам не подходит ни один коктейль. Повторите попытку изменив список')
        else:
            markup = types.ReplyKeyboardMarkup()
            for u in range(5):
                markup.add(random.choice(cocktails))
            replace_statement(str(message.chat.id), ' 4')
            bot.send_message(message.chat.id,
                             "Выберите правильный вариант, в противном случае, бот не сможет определлить нужный вам коктейль и будет очень грустить",
                             reply_markup=markup)
        # тут будет поиск рецептов!!!!!!!

    elif st == '2':
        markup = types.ReplyKeyboardMarkup()
        for t in best_of_five(message.text):
            markup.add(t)
        markup.add('Нет в списке')
        bot.send_message(message.chat.id,
                         "Выберите правильный вариант, в противном случае, бот не сможет учитывать данный компонент",
                         reply_markup=markup)
        replace_statement(str(message.chat.id), ' 3')

    elif st == '3' and message.text == 'Нет в списке':
        bot.send_message(message.chat.id, 'Жаль, тогда придется пропустить данный компонент. продолжайте ввод')
        replace_statement(str(message.chat.id), ' 2')

    elif st == '3':
        add_to_cart(str(message.chat.id), message.text)
        replace_statement(str(message.chat.id), ' 2')
        bot.send_message(message.chat.id, 'Прдолжайте в том же духе!')
        bucket = open('pplfood', 'r').readlines()
        print(bucket)
        for k in bucket:
            if str(message.chat.id) == k.split('|')[0]:
                bucket = '\n'.join(k.split('|')[1::])
                break
        markup = types.ReplyKeyboardMarkup()
        itembtn1 = types.KeyboardButton('Остановить добавление компонентов')
        markup.add(itembtn1)
        bot.send_message(message.chat.id, 'Ваш бар: \n' + bucket, reply_markup=markup)

    else:
        bot.send_message(message.chat.id,
                         'Что то пошло не так. Пропишите, пожалуйста  команду /start и свяжитесь с тех поддержкой.')


bot.infinity_polling()

# по итогу 1 дня мы сформировали приветствие, старт сбора данных об ингридиентах, разработали алгоритм подбора пяти и работы с фазами
