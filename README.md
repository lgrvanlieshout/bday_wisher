# Installation

Install uv: https://docs.astral.sh/uv/getting-started/installation/

Once downloaded, open this repo and do `uv sync`.

Install npm packages:
```bash
npm init -y
npm install whatsapp-web.js express qrcode-terminal
```

Most people running Node services use PM2.
It keeps your server alive, restarts it if it crashes, and runs it in the background.
```bash
npm install -g pm2
```
In case you are on Windows:
```bash
npm install -g pm2-windows-startup
pm2-startup install
```


# Starting the whatsapp server

Open logs:
```bash
pm2 logs
```

Start the whatsapp web client in a different terminal:
```bash
pm2 start server.js --name whatsapp-bot --instances 1
pm2 save
```

Now, look at the logs. You should see a QR-code. Scan it with Whatsapp.
Shortly after, it should print "Whatsapp ready" and a list of group apps 
with the corresponding group id. You can use these group ids in the
`birthdays.csv` to determine in which group apps the messages are sent.
For personal messages, the app id is simply the phone number of that person
`phone_number@c.us` (for example: for Dutch people, it will be 316xxxxxxxx@c.us)


# Adding people to send birthday wishes to

In order to send people a birthday wish, you'll have to enter them into
a `birthdays.csv` file. The `birthdays_template.csv` gives an example on how
to fill it in. It requires each person on a separate line formatted like this:
```
name;birthday in format dd-mm;group-id
```


# Run send_bday_wish.py daily

The last step is to add the send_bday_wish.py script to the Windows Task
Scheduler or turn it into a cron job.

In case you add it to Windows Task Scheduler, under Action, you enter the path
to the `run.bat` script in the `Program/script` field and the path to this repo
in the `Start in (optional)` field.


# Edit birthday wishes

The current `send_bday_wish.py` sends birthday wishes in Dutch, since I'm
Dutch and I don't expect a lot of people to come across this repo.
You can edit the birthday wishes and probabilities in `send_bday_wish.py`.