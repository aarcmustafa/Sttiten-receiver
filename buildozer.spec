[app]

# (str) Title of your application
title = Sttiten receiver

# (str) Package name
package.name = sttitenreceiver

# (str) Package domain (needed for android packaging)
package.domain = org.djellouli

# (str) Source files where the app lives (relative to directory of buildozer.spec)
source.dir = .

# (list) Source files to include (let blank to include all files)
source.include_exts = py,png,jpg,kv,atlas,json,hcy

# (list) Application requirements
requirements = python3,kivy,socket

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET, ACCESS_WIFI_STATE, ACCESS_NETWORK_STATE

# (str) Supported platforms
supported.platforms = android

[buildozer]
log_level = 2
warn_on_root = 1
