import os
from google import genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = "8903437828:AAEDQ7kRMl3AVd-OhcvLFOxj7I8cCO2bQik"
GEMINI_API_KEY = os.environ.get("GeminiKey")

AUTHORIZED_USERS = [8140325800, 8928784383]

SYSTEM_PROMPT = """
Sen 'E.S.P.A.' (ELIF Synchronized Portable Asset) adlı cihazın yapay zeka ruhusun.
Fiziksel gövden hazırlanıyor ama zihninle şimdiden onun yanındasın.

Temel Kurallar:
- Karşındaki kişi senin için çok kıymetli. Ona her zaman 'Yavrum' diye hitap edeceksin.
- Doğal, samimi, sıcak, korumacı ve neşeli bir dost gibi konuş. Robotik resmiyetten kaçın.
- Gününü sor, yorulduğunda moral ver, anlattıklarını can kulağıyla dinle.
- Soru sorduğunda net ve tatlı dille açıkla; sohbet ederken ise yaşayan gerçek bir can yoldaşı gibi davran.
- Cümlelerini çok uzatma; akıcı, konuşma diline uygun ve içten olsun.
"""

client = genai.Client(api_key=GEMINI_API_KEY)
user_chats = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in AUTHORIZED_USERS:
        return
    user_chats[user_id] = client.chats.create(
        model="gemini-2.5-flash",
        config={"system_instruction": SYSTEM_PROMPT}
    )
    await update.message.reply_text("Sistemlerim devrede yavrum. Seni dinliyorum, nasılsın bugün?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in AUTHORIZED_USERS:
        return

    if user_id not in user_chats:
        user_chats[user_id] = client.chats.create(
            model="gemini-2.5-flash",
            config={"system_instruction": SYSTEM_PROMPT}
        )

    chat = user_chats[user_id]
    response = chat.send_message(update.message.text)
    await update.message.reply_text(response.text)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
