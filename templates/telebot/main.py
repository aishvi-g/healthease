import telebot
import os
from pymongo import MongoClient
from telebot import types
import re
import bcrypt

from MedEase import generate_response, target_language_code

my_secret = os.environ['TELEGRAM_BOT_TOKEN']
bot = telebot.TeleBot(my_secret)

MONGO_URL = os.environ.get("MONGO_URL")
if not MONGO_URL:
  raise ValueError("MONGO_URL environment variable is not set")
client = MongoClient(MONGO_URL)
db = client.mydatabase

patients_collection = db['patients']
doctors_collection = db['doctors']
appointments_collection = db['appointments']
current_patient_id = None

user_state = {}


def show_register_login_menu(user_id):
  markup = types.ReplyKeyboardMarkup(row_width=2)
  markup.add(types.KeyboardButton('/register'), types.KeyboardButton('/login'))
  bot.send_message(
      user_id,
      "Welcome! Please choose one of the options: /register or /login",
      reply_markup=markup)


@bot.message_handler(func=lambda message: message.text.lower() == 'logout')
def logout_command(message):
  user_id = message.chat.id
  reset_user_state(user_id)
  current_patient_id = None
  show_register_login_menu(user_id)


# Function to handle the /start command
@bot.message_handler(commands=['start'])
def start_command(message):
  user_id = message.chat.id
  markup = types.ReplyKeyboardMarkup(row_width=2)
  markup.add(types.KeyboardButton('/register'), types.KeyboardButton('/login'))
  bot.send_message(
      user_id,
      "Welcome! Please choose one of the options: /register or /login",
      reply_markup=markup)


def show_main_menu(user_id):
  markup = types.ReplyKeyboardMarkup(row_width=1)
  markup.add(types.KeyboardButton('Book an Appointment'),
             types.KeyboardButton('View Appointments'),
             types.KeyboardButton('Talk to MedEase'),
             types.KeyboardButton('Logout'))
  bot.send_message(user_id, "Please choose an option:", reply_markup=markup)


# Function to handle the /register command
@bot.message_handler(commands=['register'])
def register_command(message):
  user_id = message.chat.id
  markup = types.ReplyKeyboardRemove()
  bot.send_message(
      user_id,
      "Please provide your details to complete the registration process.")
  bot.send_message(user_id, "Enter your full name:")
  bot.register_next_step_handler(message, process_name_step)


def process_name_step(message):
  user_id = message.chat.id
  full_name = message.text.strip()
  bot.send_message(user_id, "Enter your age:")
  bot.register_next_step_handler(message, process_age_step, full_name)


def process_age_step(message, full_name):
  user_id = message.chat.id
  age = message.text.strip()
  bot.send_message(user_id, "Enter your username:")
  bot.register_next_step_handler(message, process_username_step, full_name,
                                 age)


def process_username_step(message, full_name, age):
  user_id = message.chat.id
  username = message.text.strip()
  bot.send_message(user_id, "Enter your password:")
  bot.register_next_step_handler(message, process_password_step, full_name,
                                 age, username)


def process_password_step(message, full_name, age, username):
  user_id = message.chat.id
  password = message.text.strip()

 
  if not is_secure_password(password):
    bot.send_message(
        user_id,
        "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character."
    )
    bot.register_next_step_handler(message, process_password_step, full_name,
                                   age, username)
    return

  hashed_password = bcrypt.hashpw(password.encode('utf-8'),
                                  bcrypt.gensalt()).decode(
                                      'utf-8')  # Convert bytes to str

  bot.send_message(user_id, "Enter your email address:")
  bot.register_next_step_handler(message, process_email_step, full_name, age,
                                 username, hashed_password)


def is_secure_password(password):
  if len(password) < 8:
    return False

  has_uppercase = any(char.isupper() for char in password)
  has_lowercase = any(char.islower() for char in password)
  has_digit = any(char.isdigit() for char in password)
  has_special_char = any(char in "!@#$%^&*()-_=+[]{}|;:'\"<>,.?/~`"
                         for char in password)

  return has_uppercase and has_lowercase and has_digit and has_special_char


def process_email_step(message, full_name, age, username, password):
  user_id = message.chat.id
  email = message.text.strip()

existing_patient = patients_collection.find_one({"username": username})
  if existing_patient:
    bot.send_message(
        user_id,
        "The username is already taken. Please choose a different username:")
    bot.register_next_step_handler(message, process_username_step, full_name,
                                   age)
    return

  patients_collection.insert_one({
      "user_id": user_id,
      "full_name": full_name,
      "age": age,
      "username": username,
      "password": password,
      "email": email,
      "role": "patient"
  })
  bot.send_message(user_id, "Patient registration completed successfully!")


# Function to handle the /login command
@bot.message_handler(commands=['login'])
def login_command(message):
  user_id = message.chat.id
  bot.send_message(user_id, "Please enter your username to log in:")
  bot.register_next_step_handler(message, login_process_username)


def login_process_username(message):
  user_id = message.chat.id
  username = message.text.strip()
  bot.send_message(user_id, "Enter your password:")
  bot.register_next_step_handler(message, login_process_password, username)


def login_process_password(message, username):
  user_id = message.chat.id
  password = message.text.strip()

 patient = patients_collection.find_one({"username": username})
  if patient and bcrypt.checkpw(password.encode('utf-8'),
                                patient['password'].encode('utf-8')):
    global current_patient_id
    current_patient_id = patient["_id"]
    show_main_menu(user_id)
  else:
    bot.send_message(user_id, "Invalid username or password for patient.")


@bot.message_handler(
    func=lambda message: message.text.lower() == 'talk to medease')
def talk_to_medease_menu(message):
  user_id = message.chat.id
  bot.send_message(user_id, "Sure, go ahead and ask your question:")
  user_state[user_id] = {
      "action": "ask_question"
  } 


def show_departments_menu(user_id):
  markup = types.ReplyKeyboardMarkup(row_width=2)
  departments = doctors_collection.distinct("department_id")
  for dept_id in departments:
    dept_name = doctors_collection.find_one({"department_id":
                                             dept_id})["department"]
    markup.add(types.KeyboardButton(dept_name))
  bot.send_message(user_id, "Please choose a department:", reply_markup=markup)
  user_state[user_id] = "choose_department"


def show_departments_menu(user_id):
  markup = types.ReplyKeyboardMarkup(row_width=2)
  departments = doctors_collection.distinct("department")
  for dept_name in departments:
    markup.add(types.KeyboardButton(dept_name))
  bot.send_message(user_id, "Please choose a department:", reply_markup=markup)
  user_state[user_id] = "choose_department"


# # Function to show available departments and allow the patient to choose one
# def show_departments_menu(user_id):
#   markup = types.ReplyKeyboardMarkup(row_width=2)
#   departments = doctors_collection.distinct("department_id")
#   for dept_id in departments:
#     dept_name = doctors_collection.find_one({"department_id":
#                                              dept_id})["department"]
#     markup.add(types.KeyboardButton(dept_name))
#   bot.send_message(user_id, "Please choose a department:", reply_markup=markup)
#   user_state[user_id] = "choose_department"


# Function to show doctors within a selected department 
def show_doctors_in_department(user_id, department):
  markup = types.ReplyKeyboardMarkup(row_width=2)
  doctors = doctors_collection.find({"department": department})
  for doctor in doctors:
    markup.add(types.KeyboardButton(doctor["full_name"]))
  bot.send_message(
      user_id,
      f"Please choose a doctor from the '{department}' department:",
      reply_markup=markup)
  user_state[user_id] = "choose_doctor"


# Function to reset user_state
def reset_user_state(user_id):
  if user_id in user_state:
    del user_state[user_id]


@bot.message_handler(
    func=lambda message: message.text.lower() == 'book an appointment')
def book_appointment_menu(message):
  user_id = message.chat.id
  show_departments_menu(user_id)


# Function to show available time slots 
def show_available_slots(user_id, doctor_name):
  doctor = doctors_collection.find_one({"full_name": doctor_name})
  if not doctor:
    bot.send_message(user_id, f"Doctor '{doctor_name}' not found.")
    show_main_menu(user_id)
    return

  available_slots = doctor.get("available_slots", [])
  if not available_slots:
    bot.send_message(
        user_id, f"Doctor '{doctor_name}' has no available slots for booking.")
    show_main_menu(user_id)
    return

  booked_slots = appointments_collection.find({"doctor_name": doctor_name}, {
      "_id": 0,
      "appointment_time": 1
  })
  booked_slots = [slot["appointment_time"] for slot in booked_slots]

  available_slots = [
      slot for slot in available_slots if slot not in booked_slots
  ]

  if not available_slots:
    bot.send_message(user_id, f"All slots for {doctor_name} are booked.")
    show_main_menu(user_id)
    return
    markup = types.ReplyKeyboardMarkup(row_width=2)
  for slot in available_slots:
    markup.add(types.KeyboardButton(slot))

  bot.send_message(user_id,
                   f"Please choose a time slot for {doctor_name}:",
                   reply_markup=markup)
  user_state[user_id] = {
      "action": "book_appointment",
      "doctor_name": doctor_name
  }


# Function to book an appointment with the selected doctor and time slot
def book_appointment(user_id, doctor_name, appointment_time):
 
  doctor = doctors_collection.find_one({"full_name": doctor_name})
  if not doctor:
    bot.send_message(user_id, f"Doctor '{doctor_name}' not found.")
    return


  global current_patient_id

  if not current_patient_id:
    bot.send_message(user_id, "Please log in first.")
    show_main_menu(user_id)
    return

  doctor_id = doctor["_id"]
  appointment_data = {
      "user_id": user_id,
      "patient_id":
      current_patient_id,  
      "doctor_id": doctor_id,
      "doctor_name": doctor_name,
      "appointment_time": appointment_time,
  }
  appointments_collection.insert_one(appointment_data)
  doctors_collection.update_one({"_id": doctor_id},
                                {"$push": {
                                    "booked_slots": appointment_time
                                }})

  bot.send_message(
      user_id,
      f"Appointment with {doctor_name} at {appointment_time} has been booked successfully!"
  )
  reset_user_state(user_id)
  show_main_menu(user_id)




# Function to handle user responses and dispatch them to appropriate functions
@bot.message_handler(func=lambda message: message.chat.id in user_state)
def handle_user_response(message):
  user_id = message.chat.id
  state = user_state[user_id]

  if state == "choose_department":
    department = message.text.strip()
    show_doctors_in_department(user_id, department)

  elif state == "choose_doctor":
    doctor_name = message.text.strip()
    show_available_slots(user_id, doctor_name)

  elif state.get("action") == "book_appointment":
    doctor_name = state["doctor_name"]
    appointment_time = message.text.strip()

    doctor = doctors_collection.find_one({"full_name": doctor_name})
    available_slots = doctor.get("available_slots", [])
    if appointment_time not in available_slots:
      bot.send_message(
          user_id,
          f"The selected time slot is not available. Please choose a different time slot."
      )
      show_available_slots(user_id, doctor_name)
      return

    book_appointment(user_id, doctor_name, appointment_time)

  elif state.get("action") == "ask_question":
    user_question = message.text.strip()
    response = generate_response(user_question, target_language_code)

    bot.send_message(user_id, response)
    show_main_menu(user_id)


# Function to handle the "View Appointments" option from the main menu
@bot.message_handler(
    func=lambda message: message.text.lower() == 'view appointments')
def view_appointments_menu(message):
  user_id = message.chat.id

  global current_patient_id

  if not current_patient_id:
    bot.send_message(user_id, "Please log in first.")
    show_main_menu(user_id)
    return

  # Retrieve the patient's booked appointments from the database based on the patient's _id
  appointments = appointments_collection.find(
      {"patient_id": current_patient_id})
  appointments_list = list(appointments)

  if not appointments_list:
    bot.send_message(user_id, "You have no booked appointments.")
  else:
    # Display the booked appointments to the user
    message_text = "Your booked appointments:\n"
    for appointment in appointments_list:
      doctor_name = appointment.get("doctor_name", "Unknown Doctor")
      appointment_time = appointment.get("appointment_time", "Unknown Time")
      doctor = doctors_collection.find_one({"full_name": doctor_name})
      department = doctor.get("department", "Unknown Department")
      message_text += f"Doctor: {doctor_name}\n"
      message_text += f"Department: {department}\n"
      message_text += f"Time: {appointment_time}\n\n"

  bot.send_message(user_id, message_text)

  show_main_menu(user_id)


# Start the bot
bot.polling()
