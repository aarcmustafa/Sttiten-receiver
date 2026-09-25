#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket

class SttitenReceiverCore:
    def __init__(self):
        # ترددات المذبذب المحلي القياسية لـ Universal LNB (بالميجا هرتز)
        self.LO_LOW = 9750   # النطاق المنخفض (Low Band < 11700 MHz)
        self.LO_HIGH = 10600 # النطاق العالي (High Band >= 11700 MHz)

    def process_channel_frequency(self, frequency_mhz, polarization="H"):
        """
        معالجة تردد القناة أوتوماتيكياً:
        1. تحديد النطاق (High / Low)
        2. التفعيل التلقائي أو الإيقاف لنغمة 22 kHz
        3. حساب التردد الوسيط (IF)
        4. تحديد الجهد الكهربائي للقطعة (Polarization Voltage)
        """
        
        # --- التحكم التلقائي في نغمة 22 كيلو هرتز بناءً على التردد ---
        if frequency_mhz >= 11700:
            band = "High Band"
            tone_22khz = True       # تفعيل النغمة أوتوماتيكياً للترددات العالية
            active_lo = self.LO_HIGH
        else:
            band = "Low Band"
            tone_22khz = False      # إيقاف النغمة أوتوماتيكياً للترددات المنخفضة
            active_lo = self.LO_LOW

        # حساب التردد الوسيط (IF Frequency) للاستقبال الدقيق
        if_frequency = abs(frequency_mhz - active_lo)

        # تحديد الجهد بناءً على الاستقطاب (13 فولت للعمودي V، 18 فولت للأفقي H)
        voltage = 18.0 if polarization.upper() == "H" else 13.0

        # تجميع حزمة إعدادات القناة كاملة
        channel_config = {
            "frequency_mhz": frequency_mhz,
            "band": band,
            "tone_22khz": tone_22khz,
            "tone_status": "ON (22 kHz Active)" if tone_22khz else "OFF (0 kHz)",
            "local_oscillator_lo": active_lo,
            "if_frequency_mhz": if_frequency,
            "polarization": polarization.upper(),
            "voltage_v": voltage
        }

        return channel_config

    def send_command_to_receiver(self, receiver_ip, port=20000, payload=b"\x00\x01\x00\x00"):
        """
        إرسال حزم البيانات والأوامر المستخرجة من التصنت إلى الرسيفر عبر الشبكة المحلية
        """
        try:
            # إنشاء اتصال Socket عبر TCP
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3) # مهلة زمنية للاتصال لتجنب تعليق التطبيق
            s.connect((receiver_ip, port))
            
            # إرسال الحزمة الفعلية
            s.sendall(payload)
            
            # استقبال رد الرسيفر (حالة الإشارة أو الاستجابة)
            response = s.recv(1024)
            s.close()
            
            return {"status": "success", "response": response}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def tune_channel(self, frequency_mhz, polarization="H", receiver_ip=None, port=20000):
        """
        محاكاة عملية ضبط القناة، حساب الهرتزية، وإرسال الأوامر للرسيفر إن وجد الـ IP
        """
        config = self.process_channel_frequency(frequency_mhz, polarization)
        
        print(f"[*] جاري ضبط القناة على التردد: {config['frequency_mhz']} MHz")
        print(f"    - النطاق: {config['band']}")
        print(f"    - حالة نغمة 22 kHz: {config['tone_status']}")
        print(f"    - الاستقطاب والجهد: {config['polarization']} ({config['voltage_v']}V)")
        print(f"    - التردد الوسيط (IF): {config['if_frequency_mhz']} MHz")
        
        # إذا تم تمرير عنوان الـ IP الخاص بالرسيفر، يتم إرسال الأوامر شبكياً
        if receiver_ip:
            print(f"[*] جاري إرسال الأوامر إلى الرسيفر على IP: {receiver_ip}:{port} ...")
            # يمكنك هنا تحويل قيم التردد إلى البايتات المستخرجة من ملفات hcy الخاصة بك
            network_result = self.send_command_to_receiver(receiver_ip, port)
            print(f"    - حالة الاتصال: {network_result['status']}")
        
        print("-" * 50)
        return config


# ==========================================
# نقطة التشغيل والاختبار للتطبيق
# ==========================================
if __name__ == "__main__":
    receiver = SttitenReceiverCore()

    # تجربة محلية مع محاكاة إرسال الأوامر (استبدل 192.168.1.X بـ IP الرسيفر الحقيقي لديك)
    receiver.tune_channel(11900, polarization="H", receiver_ip="192.168.1.50")
            
