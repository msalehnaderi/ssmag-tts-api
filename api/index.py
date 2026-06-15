from http.server import BaseHTTPRequestHandler
import urllib.parse
import urllib.request
import textwrap

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # دریافت متنی که در لینک ارسال شده
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)
        text = query_params.get('text', [''])[0]

        if not text:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("متن برای خواندن ارسال نشده است!".encode('utf-8'))
            return

        try:
            # تکه‌تکه کردن متن
            chunks = textwrap.wrap(text, 150)
            audio_data = bytearray()
            
            for chunk in chunks:
                encoded_text = urllib.parse.quote(chunk)
                
                # 🌟 تغییر طلایی: استفاده از آدرس توسعه‌دهندگان گوگل (googleapis) که هرگز مسدود نمی‌شود
                url = f"https://translate.googleapis.com/translate_tts?ie=UTF-8&tl=fa&client=gtx&q={encoded_text}"
                
                # یک هدر ساده برای رد شدن از سدهای اولیه
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                
                with urllib.request.urlopen(req) as response:
                    audio_data.extend(response.read())

            # ارسال فایل صوتی به مرورگر شما
            self.send_response(200)
            self.send_header('Content-type', 'audio/mpeg')
            self.send_header('Access-Control-Allow-Origin', '*') # اجازه دسترسی از داخل اپلیکیشن
            self.end_headers()
            self.wfile.write(bytes(audio_data))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(f"Server Error: {str(e)}".encode('utf-8'))
