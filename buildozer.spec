[app]

# (str) Title of your application
title = Sttiten Receiver

# (str) Package name
package.name = sttitenreceiver

# (str) Package domain (needed for android packaging)
package.domain = org.sttiten

# (str) Source directory where the application files are located
source.dir = .

# (list) Source files to include (let it empty to include all files)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of directory to include (optional)
source.include_dirs = 

# (list) Source files to exclude (optional)
source.exclude_exts = spec

# (list) List of inclusions using a glob pattern
source.exclude_patterns = license,images/*.jpg

# (list) Application requirements
requirements = python3,kivy

# (str) Version of the application
version = 1.0

# (list) Supported orientations
orientation = portrait

# (list) List of permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 24

# (str) Android NDK version to use (تم التحديث لتفادي خطأ 404 للروابط القديمة)
android.ndk = 25b

# (list) The Android arch to build for
android.archs = armeabi-v7a

[buildozer]

# (int) Log level (0 = error, 1 = info, 2 = debug (with command output))
log_level = 2

# (str) Path to build artifact, storage where the android SDK will be downloaded
bin_dir = ./bin
