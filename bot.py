import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
import pdfplumber
import os

TOKEN = os.getenv("8052976481:AAG8hgvPv2VjF_NDbwSK1vtlphYORdGXBdA")

print("TOKEN:", TOKEN)  # debug
# store extracted names
names_list = []

# 📄 PDF read function
def read_pdf(file_path):
    names = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines = text.split("\n")
                for line in lines:
                    names.append(line.strip().lower())
    return names

# 📥 start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📄 Baga Nagaan Dhufte!\n\n"
        "Mee jalqaba PDF faayila keessan ergi.\n"
        "Erga sana booda maqaa kee barreessi."
    )

# 📄 handle PDF upload
async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global names_list

    file = await update.message.document.get_file()
    file_path = "data.pdf"

    await file.download_to_drive(file_path)

    names_list = read_pdf(file_path)

    await update.message.reply_text(
        "✅ Faayilaan keessan ergameera.\n"
        "Mee amma maqaa kee galchi."
    )

# 🔍 handle name search
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip().lower()

    if not names_list:
        await update.message.reply_text("⚠️ Mee jalqaba PDF ergi!")
        return

    found = False

    for name in names_list:
        if user_input in name:
            found = True
            break

    if found:
        await update.message.reply_text("✅ Passportiin Keessan Bahe Jira")
    else:
        await update.message.reply_text("❌ Passportiin Keessan Hin Bane")

# 🚀 main function
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.PDF, handle_pdf))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
