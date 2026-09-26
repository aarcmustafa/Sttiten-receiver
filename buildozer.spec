[app]

# اسم التطبيق
title = Satellite Controller

# اسم الحزمة
package.name = satellitecontroller

# نطاق الحزمة
package.domain = org.receiver

# إصدار التطبيق
version = 1.0

# مجلد المشروع
source.dir = .

# الملفات التي سيتم تضمينها
source.include_exts = py,png,jpg,jpeg,kv,atlas,json

# المتطلبات
requirements = python3,kivy

# اتجاه الشاشة
orientation = portrait

# Android
android.api = 33
android.minapi = 21
android.ndk = 25b

# التخزين الخاص بالتطبيق
android.private_storage = True

# الصلاحيات
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# python-for-android
p4a.branch = master


[buildozer]

# مستوى السجل
log_level = 2

# مجلد البناء
build_dir = .buildozer

# مجلد APK النهائي
bin_dir = ./bin
