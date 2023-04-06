from kivy import platform
from kivy.core.window import Window

# This code block is checking if the platform running the program is Android,
# and if so, it requests read and 
# write permissions to the external storage of the device using the android.
# permissions module. This is necessary because on Android, 
# apps need to request permissions to access sensitive data 
# such as external storage.

if platform == "android":
    from android.permissions import request_permissions, Permission
    request_permissions([
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.READ_EXTERNAL_STORAGE,
        Permission.MANAGE_EXTERNAL_STORAGE,
    ])