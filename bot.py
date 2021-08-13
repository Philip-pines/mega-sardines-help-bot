import sys
import telebot
import mysql.connector
from mysql.connector import errorcode
from telebot import types
from datetime import datetime

bot = telebot.TeleBot("1793723978:AAGfCaUVyD86NV2d91nfxpzfhy_L-cteDV8")
group_resv = -1001185634802
group_cancel = -1001185634802

#  "id": -1001185634802,
#             "title": "TAL MEAL RESERVATION",

# -548047611
#"id": -1001373893510,
#"title": "CAWIT MEAL RESERVATION",

# "chat": { Sample group
#             "id": -567736523,

#-1001569219760
#print(bot.get_chat('@Oujodevgroup').id)

# cursor.execute("CREATE DATABASE dbbot")

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Oujobombita",
        port="3306",
        database="dbbot"
)
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
    sys.exit()
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
    sys.exit()
  else:
    print(err)
    sys.exit()


cursor = db.cursor()

#cursor.execute("CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, \
#first_name VARCHAR(255), last_name VARCHAR(255), telegram_user_id INT(11) UNIQUE)")

# cursor.execute("CREATE DATABASE youtube")
# cursor.execute("SHOW DATABASES")

# for x in cursor:
#    print(x)

# cursor.execute("CREATE TABLE claim (id INT AUTO_INCREMENT PRIMARY KEY, first_name VARCHAR(255), last_name VARCHAR(255), month_day VARCHAR(255), meal VARCHAR(255), claim VARCHAR(255), date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")

# cursor.execute("SHOW TABLES")

# for x in cursor:
#  print(x)

# cursor.execute("ALTER TABLE customers ADD COLUMN (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT UNIQUE)")

#sql = "INSERT INTO customers (first_name, last_name, user_id) VALUES (%s, %s, %s)"
#val = ("firstName", "lastName", 3210008)
#cursor.execute(sql, val)
#db.commit()

#print(cursor.rowcount, "record inserted.")

#sql = "INSERT INTO customers (first_name, last_name, user_id) VALUES (%s, %s, %s)"
#val = [
#  ('Peter', 'Lowstreet', 1234568),
#  ('Amy', 'Apple', 3216548),
#  ('Hannah', 'Mountain', 6593248),
#]

#cursor.executemany(sql, val)
#db.commit()

#print(cursor.rowcount, "was inserted.")

################### JOINING ###################################
#cursor.execute("CREATE TABLE user_groups (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255))")
#sql = "INSERT INTO user_groups (title) VALUES (%s)"
#val = [("Bob", ), ("Builder", ), ("yo", )]
#cursor.executemany(sql, val)
#db.commit()

#cursor.execute("ALTER TABLE customers ADD COLUMN (user_group_id INT)")

#sql = "SELECT \
#    users.first_name AS user, \
#    user_groups.title AS user_group \
#    FROM users \
#    INNER JOIN user_groups ON users.user_group_id = user_groups.id"

#cursor.execute(sql)
#users = cursor.fetchall()

#for user in users:
#    print(user)

# LEFT JOIN #
#sql = "SELECT \
#    users.first_name AS user, \
#    user_groups.title AS user_group \
#    FROM users \
#    LEFT JOIN user_groups ON users.user_group_id = user_groups.id"

#cursor.execute(sql)
#users = cursor.fetchall()

#for user in users:
#    print(user)

# RIGHT JOIN #
#sql = "SELECT \
#    users.first_name AS user, \
#    user_groups.title AS user_group \
#    FROM users \
#    RIGHT JOIN user_groups ON users.user_group_id = user_groups.id"

#cursor.execute(sql)
#users = cursor.fetchall()

#for user in users:
#    print(user)

user_data = {}

class User:
    def __init__(self, first_name):
        self.first_name = first_name
        self.last_name = ''
        self.reservation = ''
        self.bu = ''
        self.shift = ''
        self.cancel = ''
        self.claim = ''
        self.no = ''

@bot.message_handler(commands=['no'])
def no(message):
    try:
        bot.reply_to(message, message.from_user.first_name + " does not want to reserve meal.")
        bot.send_message(group_resv, message.from_user.first_name + ' ' + message.from_user.last_name + " does not want meal reservation.")
    except Exception as e:
        bot.reply_to(message, 'oooops')

@bot.message_handler(commands=['claim'])
def send_claim(message):
        msg = bot.send_message(message.chat.id, "Enter first name")
        bot.register_next_step_handler(msg, process_sfirstname_step)

def process_sfirstname_step(message):
    try:
        user_id = message.from_user.id
        user_data[user_id] = User(message.text)
        msg = bot.send_message(message.chat.id, 'Enter last name')
        bot.register_next_step_handler(msg, process_slastname_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_slastname_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.last_name = message.text

        msg = bot.send_message(message.chat.id, 'Enter \"month\" and \"day\" when the meal is reserved.')
        bot.register_next_step_handler(msg, process_monthday_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_monthday_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.monthday = message.text
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Breakfast', 'Lunch', 'Dinner')

        msg = bot.send_message(message.chat.id, 'What type of meal?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_meal_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_meal_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.meal = message.text
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('claimed', 'not claimed')

        msg = bot.send_message(message.chat.id, 'What type of meal?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_claim_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_claim_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.claim = message.text
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        sql = "SELECT * FROM users WHERE telegram_user_id = {0}".format(user_id)
        cursor.execute(sql)
        existsUser = cursor.fetchone()
        print(existsUser)

        if (existsUser == None):
               sql = "INSERT INTO users (first_name, last_name, telegram_user_id) \
                                  VALUES (%s, %s, %s)"
               val = (message.from_user.first_name, message.from_user.last_name, user_id)
               cursor.execute(sql, val)

        sql = "INSERT INTO claim (first_name, last_name, month_day, meal, claim, date_time) \
                                      VALUES (%s, %s, %s, %s, %s, %s)"
        val = (user.first_name, user.last_name, user.monthday, user.meal, user.claim, timestamp)
        cursor.execute(sql, val)
        db.commit()
        user_data.clear()

        bot.send_message(message.chat.id, 'Your input has been successfully logged!')
        bot.send_message(group_cancel, user.first_name + ' ' + user.last_name + " has " + user.claim + " their " + user.meal + ".")

        # photo = open('img/sad.jpg', 'rb')
        bot.send_video(message.chat.id, "https://i.giphy.com/9JtaAvOgQUNQiobxyW.gif")
        # photo.close()
    except Exception as e:
        bot.reply_to(message, 'oooops')

@bot.message_handler(commands=['cancel'])
def send_cancel(message):
        msg = bot.send_message(message.chat.id, "Enter first name")
        bot.register_next_step_handler(msg, process_cfirstname_step)

def process_cfirstname_step(message):
    try:
        user_id = message.from_user.id
        user_data[user_id] = User(message.text)
        msg = bot.send_message(message.chat.id, 'Enter last name')
        bot.register_next_step_handler(msg, process_clastname_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_clastname_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.last_name = message.text
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Cancel')

        msg = bot.send_message(message.chat.id, 'Would you like to cancel your meal?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_cancel_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_cancel_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.shift = message.text
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        sql = "SELECT * FROM users WHERE telegram_user_id = {0}".format(user_id)
        cursor.execute(sql)
        existsUser = cursor.fetchone()
        print(existsUser)

        if (existsUser == None):
               sql = "INSERT INTO users (first_name, last_name, telegram_user_id) \
                                  VALUES (%s, %s, %s)"
               val = (message.from_user.first_name, message.from_user.last_name, user_id)
               cursor.execute(sql, val)

        sql = "INSERT INTO cancelled (first_name, last_name, date_time) \
                                      VALUES (%s, %s, %s)"
        val = (user.first_name, user.last_name, timestamp)
        cursor.execute(sql, val)
        db.commit()
        user_data.clear()

        bot.send_message(message.chat.id, 'Your input has been successfully logged!')
        bot.send_message(group_cancel, user.first_name + ' ' + user.last_name + " cancelled their meal.")

        photo = open('img/sad.jpg', 'rb')
        bot.send_photo(message.chat.id, photo)
        photo.close()
    except Exception as e:
        bot.reply_to(message, 'oooops')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
        bot.send_message(message.chat.id, "Hi! I can help you create meal reservations.\n\nPlease use one of the following commands:\n\nMeal reservation? Press /eat\nMeal cancellation? Press /cancel\n\nFor canteen users:\nPlease press /claim to report if a user hasn't claimed a meal reservation.")

@bot.message_handler(commands=['eat'])
def send_welcome(message):
        msg = bot.send_message(message.chat.id, "Enter first name")
        bot.register_next_step_handler(msg, process_firstname_step)

def process_firstname_step(message):
    try:
        user_id = message.from_user.id
        user_data[user_id] = User(message.text)
        msg = bot.send_message(message.chat.id, 'Enter last name')
        bot.register_next_step_handler(msg, process_lastname_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_lastname_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.last_name = message.text
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('For pick up', 'Canteen', 'HQ')

        msg = bot.send_message(message.chat.id, 'Where would you like to eat your meal?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_reservation_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_reservation_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.reservation = message.text
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Ayala', 'Cawit', 'Talisayan')

        msg = bot.send_message(message.chat.id, 'What BU?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_bu_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_bu_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.bu = message.text
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Night Shift', 'Day Shift')

        msg = bot.send_message(message.chat.id, 'What Shift?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_shift_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_shift_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.shift = message.text
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        sql = "SELECT * FROM users WHERE telegram_user_id = {0}".format(user_id)
        cursor.execute(sql)
        existsUser = cursor.fetchone()
        print(existsUser)

        if (existsUser == None):
               sql = "INSERT INTO users (first_name, last_name, telegram_user_id) \
                                  VALUES (%s, %s, %s)"
               val = (message.from_user.first_name, message.from_user.last_name, user_id)
               cursor.execute(sql, val)

        sql = "INSERT INTO mealresv (first_name, last_name, reservation, bu, shift, date_time) \
                                      VALUES (%s, %s, %s, %s, %s, %s)"
        val = (user.first_name, user.last_name, user.reservation, user.bu, user.shift, timestamp)
        cursor.execute(sql, val)
        db.commit()
        user_data.clear()

        bot.send_message(message.chat.id, 'Your input has been successfully logged!')
        if (user.reservation == "HQ"):
                bot.send_message(group_resv, user.first_name + ' ' + user.last_name + " wants to have their meal delivered to HQ for " + user.shift + " at " + user.bu)
                # photo = open('img/dog.jpg', 'rb')
                bot.send_video(message.chat.id, "https://i.giphy.com/5YaAkiAnRLATMBKjbW.gif")
                # photo.close()
        elif (user.reservation == "For pick up"):
                bot.send_message(group_resv, user.first_name + ' ' + user.last_name + " will pick up their meal for " + user.shift + " at " + user.bu)
                # photo = open('img/big.gif', 'rb')
                bot.send_video(message.chat.id, "https://i.giphy.com/mUHyDqFpPmEEg.gif")
                # photo.close()
        elif (user.reservation == "Canteen"):
                bot.send_message(group_resv, user.first_name + ' ' + user.last_name + " will eat at canteen for " + user.shift + " at " + user.bu)
                # photo = open('img/penguin.jpg', 'rb')
                bot.send_video(message.chat.id, "https://i.giphy.com/euLLY1YkgZGCc.gif")
                # photo.close()
        else:
                bot.send_message(message.chat.id, "Please use the predefined keyboard.")
                bot.send_message(message.chat.id, "Please /start again.")

    except Exception as e:
        bot.reply_to(message, 'oooops')

@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, "I don't understand \"" + m.text + "\"\n\nMaybe try the help page at /help\nMeal reservation? Press /eat\nMeal reservation cancellation? Press /cancel\nReport unclaimed meal? Press /claim")


bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()

if __name__=='__main__':
    bot.polling(none_stop=True)

############################################### BACKUP #################################################################

# user_data = {}

# class User:
#     def __init__(self, first_name):
#         self.first_name = first_name
#         self.last_name = ''
#         self.description = ''

# @bot.message_handler(commands=['start', 'help'])
# def send_welcome(message):
#         msg = bot.send_message(message.chat.id, "Enter first name")
#         bot.register_next_step_handler(msg, process_firstname_step)

# def process_firstname_step(message):
#     try:
#         user_id = message.from_user.id
#         user_data[user_id] = User(message.text)
#         msg = bot.send_message(message.chat.id, 'Enter last name')
#         bot.register_next_step_handler(msg, process_lastname_step)
#     except Exception as e:
#         bot.reply_to(message, 'oooops')

# def process_lastname_step(message):
#     try:
#         user_id = message.from_user.id
#         user = user_data[user_id]
#         user.last_name = message.text
#         markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
#         markup.add('YES', 'NO', 'HQ', 'CANCEL')

#         msg = bot.send_message(message.chat.id, 'Where do you want to eat?', reply_markup=markup)
#         bot.register_next_step_handler(msg, process_description_step)
#     except Exception as e:
#         bot.reply_to(message, 'oooops')

# def process_description_step(message):
#     try:
#         user_id = message.from_user.id
#         user = user_data[user_id]
#         user.description = message.text
        
#         sql = "SELECT * FROM users WHERE telegram_user_id = {0}".format(user_id)
#         cursor.execute(sql)
#         existsUser = cursor.fetchone()
#         print(existsUser)

#         if (existsUser == None):
#                sql = "INSERT INTO users (first_name, last_name, telegram_user_id) \
#                                   VALUES (%s, %s, %s)"
#                val = (message.from_user.first_name, message.from_user.last_name, user_id)
#                cursor.execute(sql, val)

#         sql = "INSERT INTO regs (first_name, last_name, description, user_id) \
#                                       VALUES (%s, %s, %s, %s)"
#         val = (user.first_name, user.last_name, user.description, user_id)
#         cursor.execute(sql, val)
#         db.commit()
#         user_data.clear()

#         bot.send_message(message.chat.id, 'Your input has been successfully logged!')
#         bot.send_message(group_id, user.first_name + ' ' + user.last_name + " wants to eat at: " + user.description)

#         photo = open('img/dog.jpg', 'rb')
#         bot.send_photo(group_id, photo)
#         photo.close()
#     except Exception as e:
#         bot.reply_to(message, 'oooops')


# # Enable saving next step handlers to file "./.handlers-saves/step.save".
# # Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# # saving will hapen after delay 2 seconds.
# bot.enable_save_next_step_handlers(delay=2)

# # Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# # WARNING It will work only if enable_save_next_step_handlers was called!
# bot.load_next_step_handlers()

# if __name__=='__main__':
#     bot.polling(none_stop=True)

