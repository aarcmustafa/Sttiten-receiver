import socket
import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.clock import Clock

class ReceiverControllerApp(BoxLayout):
    def __init__(self, **kwargs):
        super(ReceiverControllerApp, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15

        # عنوان التطبيق
        self.add_widget(Label(text='Sttiten receiver - by Djellouli Mustafa', font_size=20, bold=True))

        # إدخال عنوان الـ IP والبورت
        ip_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        ip_layout.add_widget(Label(text='Receiver IP:'))
        self.ip_input = TextInput(text='192.168.1.100', multiline=False)
        ip_layout.add_widget(self.ip_input)
        self.add_widget(ip_layout)

        # زر الاتصال والاكتشاف الآلي
        self.connect_btn = Button(text='بحث وا اتصال (Port: 20000)', size_hint_y=None, height=50)
        self.connect_btn.bind(on_press=self.connect_to_receiver)
        self.add_widget(self.connect_btn)

        # قائمة الأقمار الصناعية المنسدلة
        self.add_widget(Label(text='اختر القمر الصناعي والترددات:'))
        self.sat_spinner = Spinner(
            text='Nilesat 7°W',
            values=('Nilesat 7°W', 'Astra 19.2°E', 'Hotbird 13°E', 'Badr 26°E'),
            size_hint_y=None, height=50
        )
        self.sat_spinner.bind(text=self.on_satellite_select)
        self.add_widget(self.sat_spinner)

        # عرض حالة الإشارة
        self.signal_label = Label(text='قوة الإشارة (SNR / AGC): غير متصل', font_size=16)
        self.add_widget(self.signal_label)

    def connect_to_receiver(self, instance):
        ip = self.ip_input.text
        port = 20000
        try:
            # محاولة الاتصال بالرسيفر عبر البورت الافتراضي 20000
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(2)
            client_socket.connect((ip, port))
            self.signal_label.text = f"متصل بنجاح مع الرسيفر: {ip}:{port}"
            client_socket.close()
        except Exception as e:
            self.signal_label.text = "فشل الاتصال، تحقق من شبكة الواي فاي."

    def on_satellite_select(self, spinner, text):
        # تحميل الترددات الخاصة بالقمر المختار
        self.signal_label.text = f"تم تحميل ترددات قمر: {text}"

class SttitenReceiverApp(App):
    def build(self):
        return ReceiverControllerApp()

if __name__ == '__main__':
    SttitenReceiverApp().run()
                 
