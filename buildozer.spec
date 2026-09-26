[app]

# (str) Title of your application
title = Satellite Controller

# (str) Package name
package.name = satellitecontroller

# (str) Package domain (needed for android packaging)
package.domain = org.receiver

# (str) Source files where the let's go (relative to directory of buildozer.spec)
source.dir = .

# (list) Source files to include (let's specify python files)
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
# تأكد من إضافة مكتبات بايثون التي يحتاجها سكربت main.py (مثل sockets و zlib وهي مدمجة، Kivy إذا كانت هناك واجهة)
requirements = python3,kivy

# (str) Supported orientation (landscape, portrait or all)
orientation = portrait

#
# Android specific
#

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support
android.min_api = 21

# (str) Android NDK version to use. 
# تم تحديد الإصدار ليطابق التوصية الحديثة أو تثبيته على إصدار مستقر لمنع أخطاء التنزيل
android.ndk = 25b

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# (str) python-for-android branch to use
p4a.branch = master

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (str) Path to build artifact storage, absolute or relative to spec file
build_dir = .buildozer

# (str) Path to build output (APK)
bin_dir = ./bin
