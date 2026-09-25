[app]

# (str) Title of your application
title = Sttiten Receiver

# (str) Package name
package.name = sttitenreceiver

# (str) Package domain (needed for android packaging)
package.domain = org.sttiten

# (str) Source directory where the application files are located
source.dir = .

# (str) Application versioning (version number or string)
version = 0.1

# (list) Source files to include (let it match your python files and assets)
source.include_exts = py,png,jpg,kv,atlas,json

# (list) Application requirements
requirements = python3,kivy

# (str) Supported orientations
orientation = portrait

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 24

# (int) Android NDK version to use (محدد هنا لضمان الاستقرار وعدم جلب إصدار تالف)
android.ndk = 25b

# (str) Android NDK API to use.
android.ndk_api = 24
