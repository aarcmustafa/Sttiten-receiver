from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

# 1. استاستدعاء ملف الهرتزية والمنطق المستقل من الجذر
from receiver_core import SttitenReceiverCore

class SttitenReceiverAppUI(BoxLayout):
    def __init__(self, **kwargs):
        super(SttitenReceiverAppUI, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 30
        self.spacing = 20

        # تهيئة كلاس التحكم الخاص بالترددات والـ 22kHz
        self.receiver = SttitenReceiverCore()

        # عنوان التطبيق
        self.add_widget(Label(
            text='Sttiten Receiver - 22kHz Control',
            font_size=22,
            size_hint_y=None,
            height=50
        ))

        # حقل إدخال التردد
        self.add_widget(Label(text='أدخل التردد بالميجا هرتز (مثال: 11900):', size_hint_y=None, height=30))
        self.freq_input = TextInput(
            text='11900',
            multiline=False,
            input_filter='int',
            size_hint_y=None,
            height=50
        )
        self.add_widget(self.freq_input)

        # زر الفحص والتنفيذ
        self.tune_btn = Button(
            text='ضبط القناة وفحص الهرتزية أوتوماتيكياً',
            size_hint_y=None,
            height=60,
            background_color=(0.1, 0.5, 0.8, 1)
        )
        self.tune_btn.bind(on_press=self.on_tune_pressed)
        self.add_widget(self.tune_btn)

        # مكان عرض النتائج
        self.result_label = Label(
            text='النتيجة ستظهر هنا...',
            font_size=16,
            halign='center',
            valign='middle'
        )
        self.result_label.bind(size=self.result_label.setter('text_size'))
        self.add_widget(self.result_label)

    def on_tune_pressed(self, instance):
        try:
            # قراءة التردد المدخل وتحويله لرقم صحيح
            freq = int(self.freq_input.text)
            
            # افتراض الاستقطاب أفقي H للتجربة (يمكن ربطه بـ Spinner لاحقاً)
            polarization = "H"

            # 2. استدعاء دوال الكلاس المستقل (الهرتزية والترددات أوتوماتيكياً)
            channel_data = self.receiver.tune_channel(freq, polarization)

            # عرض النتائج مباشرة على شاشة التطبيق
            info_text = (
                f"التردد: {channel_data['frequency_mhz']} MHz\n"
                f"النطاق: {channel_data['band']}\n"
                f"حالة 22kHz: {channel_data['tone_status']}\n"
                f"الاستقطاب والجهد: {channel_data['polarization']} ({channel_data['voltage_v']}V)\n"
                f"التردد الوسيط (IF): {channel_data['if_frequency_mhz']} MHz"
            )
            self.result_label.text = info_text

        except ValueError:
            self.result_label.text = "خطأ: يجيب إدخال رقم صحيح للتردد!"

class SttitenReceiverApp(App):
    def build(self):
        self.title = "Sttiten Receiver"
        return SttitenReceiverAppUI()

if __name__ == '__main__':
    SttitenReceiverApp().run()
                        
