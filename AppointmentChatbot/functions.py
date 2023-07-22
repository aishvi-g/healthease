import speech_recognition as sr
import getpass
import io
import os
import mysql.connector

# Establish connection to MySQL database
mydb = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  password="yourpassword",
  database="yourdatabase"
)

def recognize_speech():
    # Use a speech recognition API or library to convert spoken input to text
    # Return the recognized text
    # Imports the Google Cloud client library
    from google.cloud import speech_v1p1beta1 as speech

    # Instantiates a client
    client = speech.SpeechClient()

    # The name of the audio file to transcribe
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources',
        'audio.raw')

    # Loads the audio into memory
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US')

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))


def authenticate_user():
    # Ask the user for their username and password
    # Check if the credentials are valid
    # Ask user to enter username and password
    username = input("Enter username: ")
    password = input("Enter password: ")

    # Retrieve user information from the database
    mycursor = mydb.cursor()
    sql = "SELECT * FROM users WHERE username = %s AND password = %s"
    val = (username, password)
    mycursor.execute(sql, val)
    user = mycursor.fetchone()

    # Check if user exists in the database
    if user:
        print("Login successful!")
    else:
        print("Invalid username or password.")

def patient_login():
    # Prompt the patient to log in with their username and password
    # Authenticate the user using the authenticate_user() function
    # If the authentication is successful, display the patient menu options
    # Else, display an error message
    # Retrieve doctor availability information from the database
    # establish database connection
    db = mysql.connector.connect(
    host="localhost",
    user="yourusername",
    password="yourpassword",
    database="yourdatabase"
    )

    # get doctor's username and password input
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM doctor_availability")
    doctor_availability = mycursor.fetchall()

    # Display available appointment slots for each doctor
    print("Doctor Availability:")
    for row in doctor_availability:
        print(row[0], row[1], row[2])

    # Ask user to select a doctor and appointment time
    doctor_id = input("Enter doctor ID: ")
    appointment_time = input("Enter appointment time (yyyy-mm-dd hh:mm:ss): ")

    # Check if selected appointment slot is available
    available = False
    for row in doctor_availability:
        if row[0] == doctor_id and row[1] == appointment_time:
            available = True
            break

    # Book the appointment if it is available
    if available:
        print("Appointment booked!")
        sql = "INSERT INTO appointments (doctor_id, appointment_time) VALUES (%s, %s)"
        val = (doctor_id, appointment_time)
        mycursor.execute(sql, val)
        mydb.commit()
    else:
        print("Sorry, that appointment slot is not available.")

def doctor_login():
    # Prompt the doctor to log in with their username and password
    # Authenticate the user using the authenticate_user() function
    # If the authentication is successful, display the doctor menu options
    # Else, display an error message
    # check if doctor exists in the database
    cursor = db.cursor()
    query = "SELECT * FROM Doctor_data WHERE username=%s AND password=%s"
    values = (username, password)
    cursor.execute(query, values)
    doctor = cursor.fetchone()

    if not doctor:
      print("Invalid login credentials")
    else:
      # display doctor's appointments
      query = "SELECT * FROM Appointments WHERE doctor_id=%s AND appointment_time>=NOW()"
      values = (doctor[0], )
      cursor.execute(query, values)
      appointments = cursor.fetchall()

      if not appointments:
        print("You have no appointments at the moment")
      else:
        print("Your appointments:")
        for appointment in appointments:
          print(appointment)

      # allow doctor to edit medicines database
      edit_choice = input("Do you want to edit the medicines database? (y/n): ")
      if edit_choice.lower() == 'y':
        query = "SELECT * FROM Medicines"
        cursor.execute(query)
        medicines = cursor.fetchall()

        print("Current medicines:")
        for medicine in medicines:
          print(medicine)

        medicine_name = input("Enter medicine name to edit: ")
        new_price = input("Enter new price for medicine: ")

        query = "UPDATE Medicines SET price=%s WHERE name=%s"
        values = (new_price, medicine_name)
        cursor.execute(query, values)
        db.commit()

        print(cursor.rowcount, "record(s) affected")

      # allow doctor to view patients and medical history
      query = "SELECT * FROM Patients WHERE doctor_id=%s"
      values = (doctor[0], )
      cursor.execute(query, values)
      patients = cursor.fetchall()

      if not patients:
        print("You have no patients at the moment")
      else:
        print("Your patients:")
        for patient in patients:
          print(patient)
      
        patient_id = input("Enter patient ID to view medical history: ")
    
        # join tables to show patient's medical history
        query = "SELECT Patients.name, Appointments.appointment_time, Medical_history.diagnosis, Medical_history.prescription FROM Patients JOIN Appointments ON Patients.id=Appointments.patient_id JOIN Medical_history ON Appointments.id=Medical_history.appointment_id WHERE Patients.id=%s"
        values = (patient_id, )
        cursor.execute(query, values)
        medical_history = cursor.fetchall()
    
        if not medical_history:
          print("No medical history found for this patient")
        else:
          print("Medical history:")
          for record in medical_history:
            print(record)

    # close database connection
    db.close()

def record_medication():
    # Prompt the doctor to enter the details of the prescribed medicine
    # Store the details in the database

    # Connect to the database
    cnx = mysql.connector.connect(user='your_username', password='your_password',
                              host='localhost',
                              database='your_database')
    cursor = cnx.cursor()

    # Create a list of doctor data
    doctor_data = [('Dr. John Smith', 'Cardiology', 'New York'),
                   ('Dr. Jane Doe', 'Pediatrics', 'Los Angeles'),
                   ('Dr. William Johnson', 'Dermatology', 'Chicago'),
                   ('Dr. Emily Davis', 'Oncology', 'Houston'),
                   ('Dr. Michael Brown', 'Neurology', 'Philadelphia'),
                   ('Dr. Sarah Wilson', 'Psychiatry', 'Phoenix'),
                   ('Dr. David Lee', 'Orthopedics', 'San Antonio'),
                   ('Dr. Samantha Clark', 'Endocrinology', 'San Diego'),
                   ('Dr. James Garcia', 'Gastroenterology', 'Dallas'),
                   ('Dr. Olivia Rodriguez', 'Rheumatology', 'San Jose'),
                   ('Dr. Ethan Martinez', 'Urology', 'Austin'),
                   ('Dr. Ava Hernandez', 'Nephrology', 'Jacksonville'),
                   ('Dr. Benjamin Perez', 'Allergy and Immunology', 'Indianapolis'),
                   ('Dr. Mia Flores', 'Hematology', 'Fort Worth'),
                   ('Dr. Lucas Gonzalez', 'Infectious Disease', 'Columbus')]

    # Insert the doctor data into the table using a for loop
    add_doctor = ("INSERT INTO doctor "
                  "(name, specialty, location) "
                  "VALUES (%s, %s, %s)")
    for data in doctor_data:
        cursor.execute(add_doctor, data)

    # Make sure to commit changes and close the connection
    cnx.commit()
    cursor.close()
    cnx.close()
import mysql.connector

def get_patient_medication():
    # establish connection to the database
    mydb = mysql.connector.connect(
      host="localhost",
      user="yourusername",
      password="yourpassword",
      database="yourdatabase"
    )

    # create a cursor object
    mycursor = mydb.cursor()

    # execute the SQL query to join the patient and medication tables
    mycursor.execute("SELECT p.patient_name, m.medication_name FROM patient p JOIN medication m ON p.patient_id = m.patient_id")

    # fetch all the rows returned by the query
    results = mycursor.fetchall()

    # close the cursor and database connections
    mycursor.close()
    mydb.close()

    # return the results
    return results


def view_medication():
    # Prompt the patient to select a date range for viewing their medication records
    # Retrieve the medication records from the database within the selected date range
    # Display the records to the patient
    cnx = mysql.connector.connect(user='your_username', password='your_password',
                                  host='your_host', database='your_database')
    # Prompt the patient to select a date range for viewing their medication records
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")
    
    # Retrieve the medication records from the database within the selected date range
    cursor = cnx.cursor()
    query = ("SELECT m.med_name, m.dosage, p.date "
             "FROM medicines m "
             "JOIN patient p ON m.patient_id = p.id "
             "WHERE p.date BETWEEN %s AND %s")
    cursor.execute(query, (start_date, end_date))
    medication_records = cursor.fetchall()
    
    # Display the records to the patient
    if len(medication_records) == 0:
        print("No medication records found for the selected date range.")
    else:
        for record in medication_records:
            print(f"Medication: {record[0]} | Dosage: {record[1]} | Date: {record[2]}")
    
    # Close the database connection
    cnx.close()

# Main program
while True:
    # Prompt the user to choose between patient login and doctor login
    # Call the appropriate login function
    # Depending on the user type, display the menu options and handle the selected option using the corresponding function
