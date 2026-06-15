from flask import Flask, request, Response
import edge_tts
import asyncio

app = Flask(__name__)

# تابع جدید: تولید صدا در حافظه RAM (بدون درگیری با فایل و هارد)
async def generate_audio_bytes(text):
    communicate = edge_tts.Communicate(text, "fa-IR-FaridNeural")
    audio_data = bytearray()
    # دریافت تکه‌تکه صدا از مایکروسافت و چسباندن آن‌ها به هم
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data.extend(chunk["data"])
    return bytes(audio_data)

@app.route('/api/tts', methods=['GET', 'POST'])
def tts():
    try:
        # دریافت متن
        text = request.args.get('text') if request.method == 'GET' else request.form.get('text')
        
        if not text:
            return {"error": "متن ارسال نشده است"}, 400

        # اجرای عملیات در یک حلقه امن
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        audio_bytes = loop.run_until_complete(generate_audio_bytes(text))
        loop.close()
        
        # ارسال مستقیم بایت‌های صدا به مرورگر/اپلیکیشن
        return Response(audio_bytes, mimetype="audio/mpeg")
        
    except Exception as e:
        # اگر خطایی رخ دهد، ارور دقیق را چاپ می‌کند تا مشکل را بفهمیم
        return {"error": f"خطای داخلی: {str(e)}"}, 500

@app.route('/')
def home():
    return "سرور تبدیل متن به صدای نشریه فعال است!"
