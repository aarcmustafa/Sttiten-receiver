import socket
import json
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.recycleview import RecycleView
from kivy.uix.popup import Popup

# ملف محلي لتخزين الترددات المضافة/المعدلة
FREQS_FILE = "frequencies_db.json"

class FrequencyManager:
    @staticmethod
    def load_data():
        if os.path.exists(FREQS_FILE):
            try:
                with open(FREQS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        # القاعدة الافتراضية للأقمار المطلوبة
        return {
            "Nilesat 7°W": [{"freq": "11900", "sr": "27500", "pol": "V"}, {"freq": "12303", "sr": "27500", "pol": "H"}],
            "Astra 19.2°E": [{"freq": "11836", "sr": "27500", "pol": "H"}, {"freq": "11493", "sr": "22000", "pol": "H"}],
            "Hotbird 13°E": [{"freq": "10853", "sr": "29900", "pol": "H"}, {"freq": "11034", "sr": "27500", "pol": "V"}],
            "Badr 26°E": [{"freq": "11785", "sr": "27500", "pol": "V"}, {"freq": "12015", "sr": "27500", "pol": "H"}]
        }

    @staticmethod
    def save_data(data):
        with open(FREQS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

class ReceiverControllerApp(BoxLayout):
    def __init__(self, **kwargs):
        super(ReceiverControllerApp, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 15
        self.spacing = 10

        self.freqs_db = FrequencyManager.load_data()

        # عنوان التطبيق
        self.add_widget(Label(text='Sttiten receiver - by Djellouli Mustafa', font_size=18, bold=True, size_hint_y=None, height=40))

        # إدخال عنوان الـ IP
        ip_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=45, spacing=10)
        ip_layout.add_widget(Label(text='Receiver IP:', size_hint_x=0.4))
        self.ip_input = TextInput(text='192.168.1.100', multiline=False, size_hint_x=0.6)
        ip_layout.add_widget(self.ip_input)
        self.add_widget(ip_layout)

        # زر الاتصال
        self.connect_btn = Button(text='بحث والاتصال (Port: 20000)', size_hint_y=None, height=45)
        self.connect_btn.bind(on_press=self.connect_to_receiver)
        self.add_widget(self.connect_btn)

        # قائمة الأقمار الصناعية
        sat_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=45, spacing=10)
        sat_layout.add_widget(Label(text='اختر القمر:', size_hint_x=0.4))
        self.sat_spinner = Spinner(
            text='Nilesat 7°W',
            values=list(self.freqs_db.keys()),
            size_hint_x=0.6
        )
        self.sat_spinner.bind(text=self.update_freq_display)
        sat_layout.add_widget(self.sat_spinner)
        self.add_widget(sat_layout)

        # شاشة عرض الترددات الخاصة بالقمر المختار
        self.add_widget(Label(text='الترددات المتاحة للقمر المختار:', size_hint_y=None, height=30))
        
        self.freq_list_label = Label(text='', valign='top', halign='left')
        self.freq_list_label.bind(size=self.freq_list_label.setter('text_size'))
        self.add_widget(self.freq_list_label)
        self.update_freq_display(None, self.sat_spinner.text)

        # أزرار إدارة الترددات (إضافة، تعديل، حذف)
        btn_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        
        add_btn = Button(text='إضافة تردد')
        add_btn.bind(on_press=self.open_add_popup)
        btn_layout.add_widget(add_btn)

        del_btn = Button(text='حذف تردد')
        del_btn.bind(on_press=self.open_delete_popup)
        btn_layout.add_widget(del_btn)

        self.add_widget(btn_layout)

        # حالة الإشارة
        self.signal_label = Label(text='قوة الإشارة (SNR / AGC): غير متصل', size_hint_y=None, height=40, bold=True)
        self.add_widget(self.signal_label)

    def connect_to_receiver(self, instance):
        ip = self.ip_input.text
        port = 20000
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(2)
            client_socket.connect((ip, port))
            self.signal_label.text = f"متصل بنجاح مع الرسيفر: {ip}:{port}"
            client_socket.close()
        except:
            self.signal_label.text = "فشل الاتصال، تحقق من الشبكة والـ IP."

    def update_freq_display(self, spinner, text):
        sat = self.sat_spinner.text
        freqs = self.freqs_db.get(sat, [])
        text_display = ""
        for i, f in enumerate(freqs):
            text_display += f"[{i+1}] التردد: {f['freq']} | الترميز: {f['sr']} | الاستقطاب: {f['pol']}\n"
        self.freq_list_label.text = text_display if text_display else "لا توجد ترددات مسجلة."

    def open_add_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        f_input = TextInput(hint_text='التردد (مثال: 11430)', multiline=False)
        s_input = TextInput(hint_text='معدل الترميز (مثال: 27500)', multiline=False)
        p_input = TextInput(hint_text='الاستقطاب (V أو H)', multiline=False)
        
        save_btn = Button(text='حفظ التردد الجديد', size_hint_y=None, height=40)
        
        content.add_widget(f_input)
        content.add_widget(s_input)
        content.add_widget(p_input)
        content.add_widget(save_btn)

        popup = Popup(title='إضافة تردد جديد', content=content, size_hint=(0.8, 0.6))

        def save_new_freq(btn):
            sat = self.sat_spinner.text
            new_item = {"freq": f_input.text, "sr": s_input.text, "pol": p_input.text.upper()}
            if sat in self.freqs_db:
                self.freqs_db[sat].append(new_item)
            else:
                self.freqs_db[sat] = [new_item]
            FrequencyManager.save_data(self.freqs_db)
            self.update_freq_display(None, sat)
            popup.dismiss()

        save_btn.bind(on_press=save_new_freq)
        popup.open()

    def open_delete_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        idx_input = TextInput(hint_text='أدخل رقم التردد للحذف (مثال: 1)', multiline=False)
        del_confirm_btn = Button(text='تأكيد الحذف', size_hint_y=None, height=40)
        
        content.add_widget(idx_input)
        content.add_widget(del_confirm_btn)

        popup = Popup(title='حذف تردد', content=content, size_hint=(0.8, 0.4))

        def delete_freq(btn):
            sat = self.sat_spinner.text
            try:
                idx = int(idx_input.text) - 1
                if sat in self.freqs_db and 0 <= idx < len(self.freqs_db[sat]):
                    self.freqs_db[sat].pop(idx)
                    FrequencyManager.save_data(self.freqs_db)
                    self.update_freq_display(None, sat)
            except:
                pass
            popup.dismiss()

        del_confirm_btn.bind(on_press=delete_freq)
        popup.open()

class SttitenReceiverApp(App):
    def build(self):
        return ReceiverControllerApp()

if __name__ == '__main__':
    SttitenReceiverApp().run()
        
