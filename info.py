import re
from os import environ

id_pattern = re.compile(r'^.\d+$')

# Bot information
SESSION = environ.get('SESSION', 'TechVJBot')
API_ID = int(environ.get('API_ID', '26042863'))
API_HASH = environ.get('API_HASH', 'd4fabc00b0345cd3f0ccdc0c9b750f6e')
BOT_TOKEN = environ.get('BOT_TOKEN', "")

# Bot settings
PORT = environ.get("PORT", "8080")

# Online Stream and Download
MULTI_CLIENT = False
SLEEP_THRESHOLD = int(environ.get('SLEEP_THRESHOLD', '60'))
PING_INTERVAL = int(environ.get("PING_INTERVAL", "1200"))  # 20 minutes
if 'DYNO' in environ:
    ON_HEROKU = True
else:
    ON_HEROKU = False
URL = environ.get("URL", "")

# Admins, Channels & Users
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', '-1001994332079'))
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '919169586').split()]

# --- Force Subscribe Info ---
# এখানে আপনার চ্যানেলের আইডি দিন। এটি অবশ্যই -100 দিয়ে শুরু হবে।
AUTH_CHANNEL = int(environ.get('AUTH_CHANNEL', '-1001877309572')) 

# MongoDB information
DATABASE_URI = environ.get('DATABASE_URI', "mongodb+srv://SGBACKUP14:SGBACKUP@cluster0.8ub0b.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DATABASE_NAME = environ.get('DATABASE_NAME', "techvjautobot")

# Shortlink Info
SHORTLINK = bool(environ.get('SHORTLINK', False)) # Set True Or False
SHORTLINK_URL = environ.get('SHORTLINK_URL', '')
SHORTLINK_API = environ.get('SHORTLINK_API', '')
