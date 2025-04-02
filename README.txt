💰 Telegram Bot for Payment Processing with Stripe

Accept payments through Telegram? Now it's easy! 💳
Want to automate payments for products or services? With this bot, clients can pay directly in chat!

✅ How does it work?

• 🛍️ The client selects a product
• 💳 Pays via Stripe
• ✅ Receives a payment confirmation
• 📊 You track orders in real time

🔧 Features

✅ Stripe API support
✅ Receipt generation and sending to the client
✅ Secure data storage via .env

📩 Want a bot like this?

Message me on Telegram, and I'll help you automate your payments! 🚀

# INSTRUCTIONS FOR INSTALLING AND LAUNCHING THE TELEGRAM BOT FOR PAYMENTS

## INSTALLING ON WINDOWS

### Step 1: Installing Python 3.9
1. Download Python 3.9 from the official website: https://www.python.org/downloads/release/python-3913/
- Scroll down to the "Files" section and select "Windows installer (64-bit)"
- **IMPORTANT:** During installation, check the "Add Python 3.9 to PATH" box

2. Check the Python installation. Open a command prompt (press Win+R, type "cmd" and press Enter), then type:
```
python --version
```
You should see something like "Python 3.9.13"

### Step 2: Downloading the project
1. Create a new folder for the bot, for example, C:\telegram-payment-bot
2. Copy all the project files to this folder:
- main.py
- database.py
- payments.py
- receipts.py

### Step 3: Creating a virtual environment
1. Open a command prompt and go to the project folder:
```
cd C:\telegram-payment-bot
```

2. Create a virtual environment:
```
python -m venv venv
```

3. Activate the virtual environment:
```
venv\Scripts\activate
```
After activation, at the beginning of the line will appear (venv)

### Step 4: Installing Dependencies
Enter the following command to install all the required libraries:
```
pip install python-telegram-bot==20.4 stripe==5.4.0 python-dotenv==1.0.0 reportlab==3.6.12
```

### Step 5: Setting up API Keys
1. Create a .env file in the project folder (C:\telegram-payment-bot\.env)
2. Open the file in Notepad and add the following lines:
```
TELEGRAM_TOKEN=your_telegram_bot_token
STRIPE_API_KEY=your_stripe_api_key
```

3. To get the TELEGRAM_TOKEN:
- Find the @BotFather bot in Telegram
- Send it the /newbot command
- Follow the instructions to create a new bot
- Copy the received token to the .env file

4. To get the STRIPE_API_KEY:
- Register on the Stripe website (https://stripe.com)
- In the control panel, find the "Developers" section and then "API keys"
- Copy the "Secret key" (starts with sk_test_ for test mode)
- Paste the key into the .env file

### Step 6: Launch the bot
1. Make sure the virtual environment is activated (there should be (venv) at the beginning of the line)
2. Enter the command:
```
python main.py
```
3. You will see the message "Bot launched. Press Ctrl+C to stop."
4. Now the bot is running and ready to process commands in Telegram

## INSTALLATION ON LINUX (Ubuntu/Debian)

### Step 1: Install Python 3.9
1. Open terminal (Ctrl+Alt+T)
2. Run the following commands:
```
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.9 python3.9-venv python3.9-dev
```

3. Check the installation:
```
python3.9 --version
```

### Step 2: Download the project
1. Create a folder for the project:
```
mkdir ~/telegram-payment-bot
cd ~/telegram-payment-bot
```

2. Copy all project files to this folder:
- main.py
- database.py
- payments.py
- receipts.py

### Step 3: Create a virtual environment
1. Go to the project folder (if you are not there already):
```
cd ~/telegram-payment-bot
```

2. Create a virtual environment:
```
python3.9 -m venv venv
```

3. Activate it:
```
source venv/bin/activate
```
After activation, (venv) will appear at the beginning of the line

### Step 4: Install dependencies
Enter the following command:
```
pip install python-telegram-bot==20.4 stripe==5.4.0 python-dotenv==1.0.0 reportlab==3.6.12
```

### Step 5: Configure the API keys
1. Create a .env file:
```
nano .env
```

2. Add the following lines:
```
TELEGRAM_TOKEN=your_telegram_bot_token
STRIPE_API_KEY=your_stripe_api_key
```

3. Save the file: press Ctrl+O, then Enter, then Ctrl+X

4. Get the TELEGRAM_TOKEN:
- Find the @BotFather bot in Telegram
- Send it the /newbot command
- Follow the instructions to create a new bot
- Copy the received token to the .env file

5. Get the STRIPE_API_KEY:
- Register on the Stripe website (https://stripe.com)
- In the control panel, find the "Developers" section and then "API keys"
- Copy the "Secret key" (starts with sk_test_ for test mode)
- Paste the key into the .env file

### Step 6: Starting the bot
1. Make sure the virtual environment is activated (there should be (venv) at the beginning of the line)
2. Enter the command:
```
python main.py
```
3. You will see the message "Bot started. Press Ctrl+C to stop."
4. The bot is now running and ready to process commands in Telegram

## USING THE BOT

1. Find your bot in Telegram (by the name you specified when creating it)
2. Send the command `/start` to start working with the bot
3. Use the command `/pay` to create a new payment:
- Enter the payment amount
- Enter the payment description
- The bot will create the payment and send you a link for payment
4. Use the command `/payments` to view the payment history

## ADDITIONAL INFORMATION

1. If you want the bot to run permanently on the server, look into ways to run scripts in the background (e.g. using systemd on Linux or a Windows service on Windows).

2. The bot saves all payment data to a SQLite database file (payments.db), which is created in the project folder.

3. If you want to use the bot in a production environment, don't forget to replace the Stripe test API key with a live one (starts with sk_live_).

## TROUBLESHOOTING

1. If Python is not found in the Windows command line:
- Make sure you checked "Add Python 3.9 to PATH" during installation
- Restart the command line

2. If you get errors installing dependencies:
- Make sure you are using Python 3.9
- Try updating pip: `python -m pip install --upgrade pip`

3. If the bot does not start due to an error with API keys:
- Check that the .env file is in the same folder as main.py
- Make sure there are no typos or extra spaces in the file

4. If the bot starts but does not respond in Telegram:
- Check that you entered the Telegram token correctly
- Make sure the bot has not been blocked by the user
- Try writing to the bot first (/start)

5. If you have problems with payments:
- Check that the Stripe API key is valid and active
- Make sure you don't use Cyrillic characters in the product name

For other issues, please refer to the Python documentation, python-telegram-bot and Stripe API.
