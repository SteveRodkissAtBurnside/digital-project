import os
from datetime import timezone

SECRET_KEY_FILENAME = "secretkey.dat"
BCRYPT_ROUNDS = 14

APP_DIR = os.path.dirname(os.path.abspath(__file__) ) #This is the directory of the project
PROJECTS_FOLDER = os.path.join(APP_DIR,"projects")

SHARE_URL_SIZE = 12

TIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f %Z"
TIMEZONE = timezone.utc

THUMBNAIL_EXTENSIONS = ["png","jpeg","jpg","gif"]

ALLOWED_EMAIL_DOMAINS = ["burnside.school.nz"]

#Google Login id and secret
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = ("https://accounts.google.com/.well-known/openid-configuration")

#Error responses:

VIOLATION_ERROR = ("You do not have permission to perform this request.", 403)

#Max file sizes in megabytes:
THUMBNAIL_MAX_SIZE_MB = 1
CONTENT_MAX_SIZE_MB = 20
DOWNLOAD_MAX_SIZE_MB = 20

UPLOAD_MAX_SIZE_MB = max(THUMBNAIL_MAX_SIZE_MB, CONTENT_MAX_SIZE_MB, DOWNLOAD_MAX_SIZE_MB)