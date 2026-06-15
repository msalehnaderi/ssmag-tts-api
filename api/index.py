from flask import Flask, request, send_file
import edge_tts
import asyncio
import os
import uuid

app = Flask(__name__)

async def generate_audio(text, output_file):
    communicate = edge_tts.Communicate(text, "fa-IR-FaridNeural")
    await communicate.save(output_file)

@app.route('/api/tts', methods=['GET', 'POST'])
def tts():
    try:
        # دریافت متن
        text = request.args.get('text') if request.method == 'GET' else request.form.get('text')
        
        if not text:
            return {"error": "متن ارسال نشده است"}, 400

        # تولید یک نام فایل کاملاً اختصاصی (رندوم) برای جلوگیری از تداخل
        unique_filename = f"{uuid.uuid4()}.mp3"
        output_file = os.path.join("/tmp", unique_filename)
        
        # روش کاملاً ایمن برای اجرای کدهای Async در محیط Serverless ورسل
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(generate_audio(text, output_file))
        
        # ارسال فایل به مرورگر/اپلیکیشن
        return send_file(output_file, mimetype="audio/mpeg")
        
    except Exception as e:
        # با این کار اگر باز هم خطایی رخ دهد، به جای ارور گنگ 500، دقیقاً می‌فهمیم مشکل کجاست
        return {"error": f"خطای داخلی: {str(e)}"}, 500

@app.route('/')
def home():
    return "سرور تبدیل متن به صدای نشریه (نسخه انتشار عمومی) با موفقیت فعال است!"
