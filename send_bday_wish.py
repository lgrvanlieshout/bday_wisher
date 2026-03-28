import os
import time
import requests
import datetime
import csv
import random
from emoji import emojize


def birthday_wish(name: str) -> str:
    """Generates a birthday wish.

    Args:
        name (str): Name of the person whose birthday it is

    Returns:
        str: Birthday wish.
    """
    wish = random.choice(
        [
            "Happy birthday",
            "Van harte gefeliciteerd met je verjaardag",
            "Gefeliciteerd",
            "Gefeliciteerd",
            "Van harte gefeliciteerd",
        ]
    )
    msg = [wish]

    # 80% chance name is mentioned
    if random.random() <= 0.8:
        msg.append(f" {name}")

    # Choose number of exclamation marks
    if random.random() <= 0.9:
        msg.append("!")
    else:
        msg.append("!!!")

    if random.random() <= 0.2:
        msg.append(" Ik wens je een hele leuke dag vandaag!")

    # Add emojis
    if random.random() <= 0.7:
        msg.append(":party_popper:")

    if random.random() <= 0.4:
        msg.append(
            random.choice(
                [
                    ":partying_face:",
                    ":wrapped_gift:",
                    ":fireworks:",
                    ":sparkler:",
                    ":birthday_cake:",
                    ":shortcake:",
                ]
            )
        )

    return emojize("".join(msg))


def already_run_today() -> bool:
    """Checks whether this script has already run today.

    Checks whether the date in `last_run.txt` is today. If it isn't,
    returns False and overwrites the date in `last_run.txt` with the
    current date. If the date matches the current date, returns True.

    Returns:
        bool: Whether this script has already run today.
    """
    today = datetime.datetime.now().strftime("%d-%m")

    # Create file if it doesn't exists
    if not os.path.exists("last_run.txt"):
        with open("last_run.txt", "x") as f:
            f.write(today)
            return False

    with open("last_run.txt", "r+") as f:
        last_run = f.read()
        if last_run == today:
            return True
        else:
            f.seek(0)  # Go to the beginning of the file
            f.write(today)  # Overwrite with current date
            f.truncate()  # Remove any remaining old characters
            return False


def send_msg(msg: str, group_id: str) -> None:
    """Sends a Whatsapp message.

    Args:
        msg (str): The message you want to send.
        group_id (str): The ID of the group you want to send to.
    """
    time.sleep(1 + random.random())  # Timeout to prevent race conditions
    requests.post(
        "http://localhost:3000/send", json={"group": group_id, "message": msg}
    )


def send_msg_from_csv():
    """Sends a message if today is someone's birthday.

    Reads the `birthdays.csv` file and checks for all dates whether it
    matches the current date. If it does, it generates a birthday message
    and sends it to them.
    """
    today = datetime.datetime.now().strftime("%d-%m")

    # Do not send a birthday wish more than once a day
    if already_run_today():
        return

    with open("birthdays.csv") as f:
        for row in csv.DictReader(f, ["person", "date", "group_id"], delimiter=";"):
            # If someone's birthday is today
            if row["date"] == today:
                # Generate birthday wish
                message = birthday_wish(row["person"])

                send_msg(message, row["group_id"])


if __name__ == "__main__":
    send_msg_from_csv()
