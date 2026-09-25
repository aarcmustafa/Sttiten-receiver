[app]

# (str) Title of your application
title = Sttiten receiver

# (str) Package name
package.name = sttitenreceiver

# (str) Package domain (needed for android packaging)
package.domain = org.djellouli

# (str) Application version
version = 0.1

# (str) Source files where the app lives (relative to directory of buildozer.spec)
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,json,hcy

# (list) Application requirements
requirements = python3,kivy,socket

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET, ACCESS_WIFI_STATE, ACCESS_NETWORK_STATE

# (str) Android build tools version to avoid license halts
android.build_tools_version = 33.0.0

# (str) Supported platforms
supported.platforms = android

[buildozer]
log_level = 2
warn_on_root = 1
