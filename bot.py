from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from PIL import Image, ImageEnhance
import os

# ==== CẤU HÌNH BOT ====
BOT_TOKEN = "8079392466:AAHfpNVUEAXtbTN6jfoEIE7QVm8_njAF9ZI"

# ==== HÀM LÀM NÉT ẢNH ====
def enhance_image(input_path: str, output_path: str):
    img = Image.open(input_path)
    enhancer = ImageEnhance.Sharpness(img)
    enhanced_img = enhancer.enhance(2.0)
    enhanced_img.save(output_path)

# ==== LỆNH /start ====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Chào bạn! Gõ /hd để làm nét ảnh nha!")

# ==== LỆNH /hd ====
async def hd_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Gửi ảnh bạn muốn làm nét nào!")
    context.user_data['waiting_for_hd'] = True

# ==== XỬ LÝ ẢNH ====
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('waiting_for_hd'):
        photo = update.message.photo[-1]
        file = await photo.get_file()
        
        user_id = update.message.from_user.id
        input_path = f"input_{user_id}.jpg"
        output_path = f"output_{user_id}.png"

        await file.download_to_drive(input_path)
        enhance_image(input_path, output_path)

        await update.message.reply_photo(photo=open(output_path, 'rb'), caption="Xong rồi nè! Ảnh đã được làm nét.")
        
        os.remove(input_path)
        os.remove(output_path)
        context.user_data['waiting_for_hd'] = False

# ==== KHỞI CHẠY BOT ====
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hd", hd_command))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("Bot đang chạy... Nhấn Ctrl+C để dừng.")
    app.run_polling()

if __name__ == "__main__":
    main()
