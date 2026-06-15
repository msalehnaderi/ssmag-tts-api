from flask import Flask, request, send_file
from gtts import gTTS
import os
import uuid

app = Flask(__name__)

@app.route('/api/tts', methods=['GET', 'POST'])
def tts():
    try:
        text = request.args.get('text') if request.method == 'GET' else request.form.get('text')
        if not text:
            return {"error": "متن ارسال نشده است"}, 400

        # ساخت نام تصادفی برای فایل
        unique_filename = f"{uuid.uuid4()}.mp3"
        output_file = os.path.join("/tmp", unique_filename)
        
        # استفاده از موتور صدای گوگل برای زبان فارسی
        tts_engine = gTTS(text, lang='fa')
        tts_engine.save(output_file)
        
        return send_file(output_file, mimetype="audio/mpeg")
        
    except Exception as e:
        return {"error": f"خطای داخلی: {str(e)}"}, 500

@app.route('/')
def home():
    return "سرور تبدیل متن به صدای نشریه (موتور گوگل) فعال است!"
