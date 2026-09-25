[app]

# (str) Title of your application
title = Sttiten Receiver

# (str) Package name
package.name = sttitenreceiver

# (str) Package domain (needed for android packaging)
package.domain = org.sttiten

# (list) Source files to include (let it match your python files and assets)
source.include_exts = py,png,jpg,kv,atlas,json

# (list) Application requirements
# تأكد من تضمين kivy واللغات المطلوبة
requirements = python3,kivy

# (str) Supported orientations
orientation = portrait

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 24

# (int) Android NDK version to use
ndk = 25b

# (str) Android NDK API to use.
android.ndk_api = 24

# (str) Android entry point
# (أو اتركها فارغة حسب نقطة بداية تطبيقك main.py)
# android.entrypoint = org.kivy.android.PythonActivity
