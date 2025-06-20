import telebot
from telebot import types

# 🔐 Replace this with your NEW TOKEN from BotFather
TOKEN = '7923416562:AAGOOVlwvPepVidWvNUL9ikeo8T5KOi39Bc'
ADMIN_ID = 6471363546

bot = telebot.TeleBot(TOKEN)
user_data = {}
orders = []

stock = {
    "25 💎": 100,
    "50 💎": 100,
    "115 💎": 50,
    "240 💎": 30,
    "610 💎": 20,
    "1240 💎": 10,
    "2530 💎": 5,
    "Weekly": 50,
    "Monthly": 20
}

prices = {
    "25 💎": 24,
    "50 💎": 38,
    "115 💎": 80,
    "240 💎": 162,
    "610 💎": 415,
    "1240 💎": 825,
    "2530 💎": 1640,
    "Weekly": 160,
    "Monthly": 780
}

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    if chat_id not in user_data:
        user_data[chat_id] = {'uid': '', 'orders': 0}
    bot.send_message(chat_id, f"Hello {message.from_user.first_name}!!\nWelcome to Sahuu TopUp Bot 🛒\n\nThe bot is in development by @Sahuu_Official\n\n➡️ Please enter your Free Fire UID to continue:")
    bot.register_next_step_handler(message, save_uid)

def save_uid(message):
    uid = message.text
    chat_id = message.chat.id
    user_data[chat_id]['uid'] = uid
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📋 Menu")
    bot.send_message(chat_id, "✅ UID Saved!\nClick Menu to continue.", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "📋 Menu")
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("👤 Profile", "🛍️ Shop")
    bot.send_message(message.chat.id, "Select an option:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "👤 Profile")
def profile(message):
    chat_id = message.chat.id
    data = user_data.get(chat_id, {'uid': 'Not set', 'orders': 0})
    bot.send_message(chat_id, f"👤 USER NAME: {message.from_user.first_name}\n🎮 UID NO: {data['uid']}\n🛒 TOTAL ORDER: {data['orders']}")

@bot.message_handler(func=lambda m: m.text == "🛍️ Shop")
def shop(message):
    text = """📦 *PRODUCT LIST WITH PRICE* 📦

☞ 25 💎 ➪ 24 Tk
☞ 50 💎 ➪ 38 Tk
☞ 115 💎 ➪ 80 Tk
☞ 240 💎 ➪ 162 Tk
☞ 610 💎 ➪ 415 Tk
☞ 1240 💎 ➪ 825 Tk
☞ 2530 💎 ➪ 1640 Tk
☞ Weekly Membership ➪ 160 Tk
☞ Monthly Membership ➪ 780 Tk

💰 Stock: 50000+ 💎 Available
📩 PLEASE CLICK THE AMOUNT YOU WANT TO BUY"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = list(stock.keys())
    for i in range(0, len(buttons), 3):
        markup.add(*buttons[i:i+3])
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text in stock)
def select_quantity(message):
    user_data[message.chat.id]['selected_product'] = message.text
    bot.send_message(message.chat.id, "HOW MUCH DO YOU WANT TO BUY?\nType quantity like: 1, 2, 3:")
    bot.register_next_step_handler(message, confirm_order)

def confirm_order(message):
    chat_id = message.chat.id
    try:
        quantity = int(message.text)
        product = user_data[chat_id].get('selected_product', 'N/A')
        if stock[product] >= quantity:
            stock[product] -= quantity
            user_data[chat_id]['orders'] += 1
            total_price = prices[product] * quantity
            order_info = {
                "user": message.from_user.username or message.from_user.first_name,
                "uid": user_data[chat_id]['uid'],
                "product": product,
                "quantity": quantity
            }
            orders.append(order_info)
            msg = f"""✅ New Order Placed!
🧾 Product: {product}
🔢 Quantity: {quantity}
💸 Total Price: {total_price} Tk
🎮 UID: {user_data[chat_id]['uid']}
📦 Remaining Stock: {stock[product]}
📲 Payment via Bkash/Nagad (Personal)
➡️ +8801619-038113
📷 After payment, send screenshot here or contact @Sahuu_Official
⏳ Please wait 10 minutes for top-up."""
            bot.send_message(chat_id, msg)

            admin_msg = f"""📥 New Order Received!
👤 @{message.from_user.username or message.from_user.first_name}
🎮 UID: {user_data[chat_id]['uid']}
💎 Product: {product}
🔢 Quantity: {quantity}
💰 Total: {total_price} Tk
📦 Stock Left: {stock[product]}"""
            bot.send_message(ADMIN_ID, admin_msg)
        else:
            bot.send_message(chat_id, f"⚠️ Sorry! Not enough stock.\nAvailable: {stock[product]}")
    except:
        bot.send_message(chat_id, "❌ Invalid quantity. Please enter a number.")

@bot.message_handler(commands=['orders'])
def orders_list(message):
    if message.chat.id == ADMIN_ID:
        if not orders:
            bot.send_message(message.chat.id, "📦 No orders found.")
        else:
            text = "🧾 All Orders:\n\n"
            for i, o in enumerate(orders, 1):
                text += f"{i}. 👤 {o['user']}\n🎮 UID: {o['uid']}\n💎 {o['product']} × {o['quantity']}\n\n"
            bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, "⛔ You are not authorized!")

@bot.message_handler(commands=['stock'])
def stock_check(message):
    if message.chat.id == ADMIN_ID:
        text = "📦 Current Stock:\n"
        for item, qty in stock.items():
            text += f"{item}: {qty}\n"
        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, "⛔ You are not authorized!")

# ✅ Stable polling
bot.infinity_polling()
