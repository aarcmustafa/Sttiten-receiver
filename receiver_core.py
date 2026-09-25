# استيراد الكلاس من الملف الذي أنشأته
from receiver_core import SttitenReceiverCore

# إنشاء كائن للتحكم
receiver = SttitenReceiverCore()

# عندما يختار المستخدم قناة أو يدخل التردد يدوياً، قم باستدعاء الدالة هكذا:
channel_data = receiver.tune_channel(11900, polarization="H")

# يمكنك الآن استخدام النتائج (مثل معرفة هل نغمة 22kHz مفعلة أم لا)
if channel_data["tone_22khz"]:
    print("النغمة مفعلة - التردد يتبع النطاق العالي")
else:
    print("النغمة متوقفة - التردد يتبع النطاق المنخفض")
  
