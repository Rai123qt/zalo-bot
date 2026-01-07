from flask import Flask, request
from zalo_bot import Bot, Update
from zalo_bot.ext import Dispatcher, MessageHandler, filters

BOT_TOKEN = "3222229135581534944:CTggeFHwGxfZaLeIBppjLsapWDhrNHaoSiLhhvfeuFmOdgrhdIYmabRTKofimvOU"
SECRET_TOKEN = "new_secret_123"

app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)

def echo(update, context):
    update.message.reply_text(f"Bạn vừa nói: {update.message.text}")

dispatcher = Dispatcher(bot, None, workers=0)
dispatcher.add_handler(MessageHandler(filters.TEXT, echo))

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)

    # In payload để debug
    print("=== WEBHOOK PAYLOAD ===")
    print(data)

    payload = data.get("result")
    if not payload:
        return "ok"

    # 🔴 CHỈ TRẢ LỜI KHI LÀ TIN NHẮN CHỮ
    if payload.get("event_name") != "message.text.received":
        return "ok"

    update = Update.de_json(payload, bot)
    dispatcher.process_update(update)
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
