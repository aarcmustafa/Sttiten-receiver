#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
            "tone_22khz": tone_22khz,                               # الحالة الأوتوماتيكية للـ 22 هرتز (True / False)
            "tone_status": "ON (22 kHz Active)" if tone_22khz else "OFF (0 kHz)",
            "local_oscillator_lo": active_lo,
            "if_frequency_mhz": if_frequency,
            "polarization": polarization.upper(),
            "voltage_v": voltage
        }

        return channel_config

    def tune_channel(self, frequency_mhz, polarization="H"):
        """
        محاكاة عملية ضبط القناة وإرسال أوامر التحكم (الهرتزية + الاستقطاب)
        """
        config = self.process_channel_frequency(frequency_mhz, polarization)
        
        print(f"[*] جاري ضبط القناة على التردد: {config['frequency_mhz']} MHz")
        print(f"    - النطاق: {config['band']}")
        print(f"    - حالة نغمة 22 kHz: {config['tone_status']}")
        print(f"    - الاستقطاب والجهد: {config['polarization']} ({config['voltage_v']}V)")
        print(f"    - التردد الوسيط (IF): {config['if_frequency_mhz']} MHz")
        print("-" * 50)
        
        # هنا يمكنك لاحقاً إضافة الكود الخاص بإرسال هذه الأوامر عبر Sockets أو واجهة الأجهزة
        return config


# ==========================================
# نقطة التشغيل والاختبار للتطبيق
# ==========================================
if __name__ == "__main__":
    receiver = SttitenReceiverCore()

    # تجربة 1: تردد من النطاق المنخفض (سيتم إيقاف الـ 22 kHz أوتوماتيكياً)
    receiver.tune_channel(10930, polarization="V")

    # تجربة 2: تردد من النطاق العالي (سيتم تفعيل الـ 22 kHz أوتوماتيكياً لمنع فقدان الإشارة)
    receiver.tune_channel(11900, polarization="H")

    # تجربة 3: تردد آخر عالي للتأكد من الثبات
    receiver.tune_channel(12523, polarization="H")
        
