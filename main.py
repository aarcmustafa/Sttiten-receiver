import socket
import zlib
import binascii

# إعدادات الاتصال بالرسيفر
IP = "192.168.1.2"
PORT = 20000

def send_command(command_str):
    try:
        # إنشاء اتصال TCP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((IP, PORT))
        
        # تجهيز التغليف (Start + Length + End + Payload) بناءً على البروتوكول المكتشف
        payload = f'{{"request":"{command_str}"}}'
        header_prefix = "Start"
        header_suffix = "End"
        
        # حساب طول الطلب وتنسيقه بـ 7 خانات
        length_str = f"{len(payload):07d}"
        wrapped_data = f"{header_prefix}{length_str}{header_suffix}{payload}"
        
        print(f"[*] جاري إرسال الأمر: {command_str}...")
        s.sendall(wrapped_data.encode('utf-8'))
        
        # استقبال الرد من الرسيفر
        response = s.recv(4096)
        print(f"[*] تم استقبال الرد الخام بحجم: {len(response)} بايت")
        
        s.close()
        return response
    except Exception as e:
        print(f"[!] حدث خطأ أثناء الاتصال: {e}")
        return None

def extract_and_decompress(response_bytes):
    if not response_bytes:
        return
    
    try:
        # البحث عن توقيع ضغط Zlib الشهير (789c) في الرد الخام
        hex_data = binascii.hexlify(response_bytes).decode('utf-8')
        zlib_signature = "789c"
        
        pos = hex_data.find(zlib_signature)
        if pos != -1:
            # اقتطاع البيانات ابتداءً من توقيع Zlib
            compressed_hex = hex_data[pos:]
            
            # تحويل السداسي إلى بايتات وفك الضغط
            compressed_bytes = binascii.unhexlify(compressed_hex)
            decompressed_data = zlib.decompress(compressed_bytes)
            
            print("[+] تم فك ضغط البيانات بنجاح:")
            print(decompressed_data.decode('utf-8'))
        else:
            print("[-] لم يتم العثور على بيانات مضغوطة بـ Zlib في الاستجابة.")
            # محاولة طباعة الرد كـ نص عادي إذا لم يوجد ضغط
            print(response_bytes.decode('utf-8', errors='ignore'))
            
    except Exception as e:
        print(f"[!] خطأ أثناء معالجة وفك ضغط البيانات: {e}")

if __name__ == "__main__":
    # تجربة إرسال الأمر 19 (أو يمكنك تغييره إلى 405)
    target_command = "19"
    raw_response = send_command(target_command)
    extract_and_decompress(raw_response)
        
