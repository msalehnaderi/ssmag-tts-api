from http.server import BaseHTTPRequestHandler
import urllib.parse
import urllib.request
import textwrap

# در روش بومی، ورسل مستقیماً دنبال کلاس handler می‌گردد
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # ۱. دریافت متنی که در لینک ارسال شده
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)
        text = query_params.get('text', [''])[0]

        # اگر متنی نبود، ارور ۴۰۰ برگردان
        if not text:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("متن برای خواندن ارسال نشده است!".encode('utf-8'))
            return

        try:
            # ۲. تکه‌تکه کردن متن (چون گوگل متن‌های خیلی طولانی را در یک مرحله قبول نمی‌کند)
            chunks = textwrap.wrap(text, 150)
            audio_data = bytearray()
            
            for chunk in chunks:
                encoded_text = urllib.parse.quote(chunk)
                url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl=fa&client=tw-ob&q={encoded_text}"
                
                # جا زدن سرور به عنوان یک مرورگر واقعی
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'})
                
                # دریافت فایل صوتی از گوگل و چسباندن آن به تکه‌های قبلی
                with urllib.request.urlopen(req) as response:
                    audio_data.extend(response.read())

            # ۳. ارسال فایل صوتی یکپارچه به خروجی (با کد موفقیت ۲۰۰)
            self.send_response(200)
            self.send_header('Content-type', 'audio/mpeg')
            self.end_headers()
            self.wfile.write(bytes(audio_data))
            
        except Exception as e:
            # مدیریت خطا بدون کرش کردنِ سرور ورسل
            self.send_response(500)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(f"Server Error: {str(e)}".encode('utf-8'))
