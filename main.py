import pandas
import datetime as dt
import random
import glob
import smtplib

EMAIL = "Put the From emial[your email]"
PASSWORD = "Put the password [Your password]"


def fetch_letter():
    letters = glob.glob("letter_templates/*.txt")
    if letters:
        chosen_letter = random.choice(letters)

    return chosen_letter


def create_letter(letter, details):
    with open(letter, "r") as file:
        letter_content = file.read()

    content = letter_content.replace("[NAME]", details["name"])

    return content


def send_email(email, letter):
    try:
        with smtplib.SMTP("smtp.gmail.com") as conn:
            conn.starttls()
            conn.login(EMAIL, PASSWORD)
            conn.sendmail(
                from_addr=EMAIL,
                to_addrs=email,
                msg=f"Subject: Happy Birthday! \n\n {letter}",
            )
        return {"status": True, "message": "Email sent successfully"}
    except smtplib.SMTPException as e:
        return {
            "status": False,
            "message": "Email Not sent",
            "error": f"Email delivery failed (SMTP error): {e}",
        }
    except OSError as e:
        return {
            "status": False,
            "message": "Email Not sent",
            "error": f"Network connection failed (Server unreachable): {e}",
        }


# Read Data
bday_data = pandas.read_csv("birthdays.csv")
bday_dict = bday_data.to_dict(orient="records")

# 2. Get Current Date
today = dt.datetime.now()
current_month = today.month
current_day = today.day

# 3. Find Today's Birthday Persons
bday_persons = []
for data in bday_dict:
    if current_month == int(data["month"]) and current_day == int(data["day"]):
        details = {
            "name": data["name"],
            "email": data["email"],
        }
        bday_persons.append(details)

# 4. Process and Send Letters
if bday_persons:
    for person in bday_persons:
        letter_path = fetch_letter()
        print(letter_path)
        email = person["email"]
        if letter_path:
            final_letter = create_letter(letter_path, person)

            print(f"--- Sending to {person['name']} ---")

            sending = send_email(email, final_letter)

            print(sending)
