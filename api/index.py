from flask import Flask, request, Response
import urllib.parse
import urllib.request
import textwrap

app = Flask(__name__)

@app.route('/api/tts', methods=['GET', 'POST'])
def tts():
    try:
        # دریافت متن
        text = request.args.get('text') if request.method == 'GET' else request.form.get('text')
        if not text:
            return {"error": "متن ارسال نشده است"}, 400

        # تکه‌تکه کردن متن به قطعات ۱۵۰ کاراکتری برای عبور از محدودیت گوگل
        chunks = textwrap.wrap(text, 150)
        audio_data = bytearray()
        
        for chunk in chunks:
            # درخواست خام و مستقیم از API آزاد گوگل (بدون استفاده از کتابخانه)
            encoded_text = urllib.parse.quote(chunk)
            url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl=fa&client=tw-ob&q={encoded_text}"
            
            # جا زدن خودمان به عنوان یک مرورگر واقعی برای فریب فایروال گوگل
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'})
            with urllib.request.urlopen(req) as response:
                audio_data.extend(response.read())
        
        # برگرداندن فایل صوتی یکپارچه
        return Response(bytes(audio_data), mimetype="audio/mpeg")
        
    except Exception as e:
        return {"error": f"خطا در ارتباط با گوگل: {str(e)}"}, 500

@app.route('/')
def home():
    return "سرور تبدیل صدای مستقیم گوگل فعال است!"
