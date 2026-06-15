from flask import Flask, request, send_file
import edge_tts
import asyncio
import os

app = Flask(__name__)

async def generate_audio(text, output_file):
    # استفاده از صدای "فرید" برای زبان فارسی (مرد). برای صدای زن از "fa-IR-DilaraNeural" استفاده کن.
    communicate = edge_tts.Communicate(text, "fa-IR-FaridNeural")
    await communicate.save(output_file)

@app.route('/api/tts', methods=['GET', 'POST'])
def tts():
    # دریافت متن خبر از اپلیکیشن اندروید شما
    text = request.args.get('text') if request.method == 'GET' else request.form.get('text')
    
    if not text:
        return {"error": "متن برای خواندن ارسال نشده است!"}, 400

    # ورسل به عنوان فضای موقت فقط اجازه نوشتن در پوشه tmp را می‌دهد
    output_file = "/tmp/output.mp3" 
    
    # اجرای عملیات تبدیل متن به صدا
    asyncio.run(generate_audio(text, output_file))
    
    # برگرداندن فایل صوتی آماده به اپلیکیشن به صورت استریم
    return send_file(output_file, mimetype="audio/mpeg")

if __name__ == '__main__':
    app.run(debug=True)