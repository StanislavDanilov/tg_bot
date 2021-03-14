import telebot
from telebot import types
from pymongo import MongoClient

bot = telebot.TeleBot('1556596504:AAGHMHATIyXgmiYmooz0IjJZR4pMuLi7VvQ');

client = MongoClient('localhost', 27017)
db = client['Quicke']
users = db['Clients']

callback = "Если возникнут вопросы или проблемы,  Вы можете связаться с поддержкой. По вопросам сотрудничества и найма на работу связывайтесь с менеджером."
rules = "Правила просты, вы даете задание, мы его выполняем. Для того чтобы граммотно отставить заявку, нужно заполнить форму в соответсвии с требованиями и оплатить заказ.\n Срок выполнения зависит от сложности работы. Гарантия на наши работы от 7-14 дней в зависимости от сложности с момента сдачи заказа. Возврат средств возможен в случаи отказа работы в размере 80%  от суммы заказа."

job_one_five = "Вуз\nФакультет\nПредмет\nТема\nОригинальность\nСрок сдачи\nДополнительные требования\n\n Пример\n 1-5(Обязательно написать в начале)\n Вуз МГУ\nФакультет ХимФак\nПредмет Химия\nТема Органическая Химия\nОригинальность 90\nСрок сдачи 12.03.2020\nДополнительные требования Нет"
job_one_five_in = dict.fromkeys(["Вуз", "Факультет", "Предмет", "Тема", "Оригинальность", "Срок сдачи", "Дополнительные требования"])
job_sixty = "Предмет перевода \nСроки сдачи \nДополнительные требования "
job_seven = "Опишите подробно задание\n"
job_eight = "Вуз\nФакультет\nПредмет\nВремя сдачи экзамена\nФорма сдачи\nДополнительные требования"


job_txt = "Перечень услуг"

start_menu = telebot.types.ReplyKeyboardMarkup()
admin_menu = telebot.types.ReplyKeyboardMarkup()
job = telebot.types.ReplyKeyboardMarkup()
start_menu.row('Личный кабинет', 'Правила')
start_menu.row('Работы', 'Обратная связь')
job.row('Статья', 'Расчетные работы')
job.row('Дипломы', 'Переводы')
job.row('Курсовые работы', 'Иные работы')
job.row('Доклады', 'Помощь на зачетах/экзаменах')
job.row('Главное меню')

admin_menu.row('/answer', '/run')

@bot.message_handler(commands=['start'])
def cheak_users(message):
    client = users.find_one({"tg_id": message.from_user.id})
    if not client:
        bot.register_next_step_handler(message, start)
    else:
        global tg_id
        global name
        global email
        client = users.find_one({"tg_id": message.from_user.id})
        name = client["Name"]
        tg_id = client["tg_id"]
        email = client["Email"]
        print(tg_id, name, email)
        bot.send_message(message.from_user.id, "Добро пожаловать в главное меню", reply_markup=start_menu)
        bot.register_next_step_handler(message, menu)

def start(message):
    bot.send_message(message.from_user.id, "Как тебя зовут?")
    bot.register_next_step_handler(message, get_email)
    

def get_email(message):
    global nameReg
    nameReg = message.text
    bot.send_message(message.from_user.id, "Какая у тебя почта?")
    bot.register_next_step_handler(message, temp)
    
def temp(message):
    global emailReg
    emailReg = message.text
    insert_user(nameReg, emailReg, message.from_user.id)
    bot.register_next_step_handler(message, menu)

@bot.message_handler(commands=['answer'])
def start_answer(message):
    if message.from_user.id == 757639077:
        bot.send_message(message.from_user.id, "Почта пользователя")
        bot.register_next_step_handler(message, get_email_answer)
    else:
        bot.send_message(message.from_user.id, "Что-то пошло не так")

def get_email_answer(message): #получаем фамилию
    global nameClient
    nameClient = message.text
    client = users.find_one({"Email": nameClient})
    if not client:
        bot.send_message(message.from_user.id, "Что-то пошло не так")
        bot.register_next_step_handler(message, menu)
    else:
        bot.send_message(message.from_user.id, "Текст ответа")
        bot.register_next_step_handler(message, temp_answer)
    
def temp_answer(message):
    global answer
    global answer_tg_id
    answer = message.text
    client = users.find_one({"Email": nameClient})
    name = client["Name"]
    answer_tg_id = client["tg_id"]
    email = client["Email"]
    mess = message.text
    keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes_answer'); #кнопка «Да»
    keyboard.add(key_yes); #добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no_answer');
    keyboard.add(key_no);
    bot.reply_to(message, "Все верно?",  reply_markup=keyboard)

@bot.message_handler(commands=['run'])
def run(message):
    if message.from_user.id == 757639077:
        client = users.find({"run": "True"})
        for document in client:
            print(document)
            email = document["Email"]
            order = document["order"]
            bot.send_message(message.from_user.id, f"Емаил пользователя --->>\n{email}\n Заказ ---->>> \n{order}\n\n")
        
@bot.message_handler(commands=['admin'])
def menu(message):
    if message.from_user.id == 757639077:
        bot.send_message(message.from_user.id, "Добро пожаловать в админку", reply_markup=admin_menu)
    else:
        bot.send_message(message.from_user.id, "Что-то пошло не так")
@bot.message_handler(content_types=['text'])
def menu(message):
    client = users.find_one({"tg_id": message.from_user.id})
    if not client:
        bot.register_next_step_handler(message, start)
    else:
        global tg_id
        global name
        global email
        client = users.find_one({"tg_id": message.from_user.id})
        name = client["Name"]
        tg_id = client["tg_id"]
        email = client["Email"]
        print(tg_id, name, email)
    global mess
    mess = message.text
#    i = 0
#    key = ""
#    value = ""
#    d = {}
#    for ln in message.text:
#        while mess[i] != " ":
#            key += mess[i]
#            i+=1
#        i+=1
#        while i < len(ln):
#            value += mess[i]
#            i+=1
#        d[key] = value
#        key = ""
#        value = ""
#        i = 0
    if message.text == "Обратная связь":
        bot.send_message(message.from_user.id, callback)
    elif message.text == "Правила":
        bot.send_message(message.from_user.id, rules, reply_markup=start_menu)
    elif message.text == "1":
        find_Mongo(message.from_user.id)
    elif message.text == "Главное меню":
        bot.send_message(message.from_user.id, rules, reply_markup=start_menu)
    elif message.text == "Работы":
        bot.send_message(message.from_user.id, job_txt, reply_markup=job)
    elif message.text == "Статья":
        bot.send_message(message.from_user.id, job_one_five, reply_markup=job)
    elif message.text == "Расчетные работы":
        bot.send_message(message.from_user.id, job_one_five, reply_markup=job)
    elif message.text == "Дипломы":
        bot.send_message(message.from_user.id, job_one_five, reply_markup=job)
    elif message.text == "Переводы":
        bot.send_message(message.from_user.id, job_one_five, reply_markup=job)
    elif message.text == "Курсовые работы":
        bot.send_message(message.from_user.id, job_one_five, reply_markup=job)
    elif message.text == "Иные работы":
        bot.send_message(message.from_user.id, job_sixty, reply_markup=job)
    elif message.text == "Доклады":
        bot.send_message(message.from_user.id, job_seven, reply_markup=job)
    elif message.text == "Delete":
        delete_mongo(message.from_user.id)
    elif message.text == "Помощь на зачетах/экзаменах":
        bot.send_message(message.from_user.id, job_eight)
    elif message.text == "Главное меню":
        bot.send_message(message.from_user.id, job_one_five, reply_markup=menu)
    elif message.text == "sd45df67fg89":
        bot.send_message(message.from_user.id, "Сюда отправить выгрузку excel" )
        excelpull()
#    elif message.text in job_one_five:
#        mess = message.text
#        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
#        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes'); #кнопка «Да»
#        keyboard.add(key_yes); #добавляем кнопку в клавиатуру
#        key_no = types.InlineKeyboardButton(text='Нет', callback_data='no');
#        keyboard.add(key_no);
#        bot.reply_to(message, "Все верно?",  reply_markup=keyboard)
#    elif message.text in job_sixty:
#        mess = message.text
#        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
#        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes'); #кнопка «Да»
#        keyboard.add(key_yes); #добавляем кнопку в клавиатуру
#        key_no = types.InlineKeyboardButton(text='Нет', callback_data='no');
#        keyboard.add(key_no);
#        bot.reply_to(message, "Все верно?",  reply_markup=keyboard)
#    elif message.text in job_seven:
#        mess = message.text
#        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
#        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes'); #кнопка «Да»
#        keyboard.add(key_yes); #добавляем кнопку в клавиатуру
#        key_no = types.InlineKeyboardButton(text='Нет', callback_data='no');
#        keyboard.add(key_no);
#        bot.reply_to(message, "Все верно?",  reply_markup=keyboard)
#    elif message.text in job_eight:
#        mess = message.text
#        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
#        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes'); #кнопка «Да»
#        keyboard.add(key_yes); #добавляем кнопку в клавиатуру
#        key_no = types.InlineKeyboardButton(text='Нет', callback_data='no');
#        keyboard.add(key_no);
#        bot.reply_to(message, "Все верно?",  reply_markup=keyboard)
    
def excelpull():
    pass
    
def insert_user(name,email,tg_id):
    db.Clients.insert_one({
    "Name": name,
    "Email": email,
    "tg_id": tg_id
                          })
def find_Mongo(tg_id):
    find = users.find_one({"run": "True"})
    order = find["Email"]
    print(order)
def delete_mongo(tg_id):
    a = users.delete_one({"tg_id": tg_id})
    print(a)
def add_orders():
    users.update_one({"tg_id" : tg_id },{"$set" : {"order": mess, "run": "True"}})
    print("add")
    
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, "Благодарим " + name +" за оформление заказа! Ваш заказ в обработке, ваш личный менеджер с вами свяжеться в течении 10-15 минут.")
        add_orders()
        bot.send_message(757639077, str(mess)+"\n"+str(email))
    elif call.data == "no":
        bot.send_message(call.message.chat.id, "Вы отказались от заказа")
    if call.data == "yes_answer":
        bot.send_message(answer_tg_id, answer)
        users.update_one({"tg_id" : answer_tg_id },{"$set" : {"order_answer": answer, "run": "False"}})
    
bot.polling(none_stop=True, interval=0)

