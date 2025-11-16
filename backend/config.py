# Statement for enabling the development environment
DEBUG = False

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database 
#SQLALCHEMY_DATABASE_URI = "mysql://root:password@localhost/balans"

SQLALCHEMY_DATABASE_URI = "mysql://root:password@localhost/mystl"

DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 10

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "kamnakosyonBaljIpMishlanUnEvosbo"

# Secret key for signing cookies
SECRET_KEY = "ew0BlawpAcyajNirshesUvonViUjEbs1"

# Token key
TOKEN_KEY = "OogyejIvumNasAdUbBishkOudGajnicPiWrymagAbthucradocviOrmosOvDerow"

# Server nonce
SERVER_NONCE = "RabroyllIjhywofuckcorwojnamvowAg"

# Validity of the token in days
JWT_VALIDITY_IN_DAYS = 30

# Report directory
#REPORT_OUTPUT_FOLDER = "/opt/balans/output/"
#REPORT_OUTPUT_FOLDER = "C:\\Work\\balance\\backend\\output\\"
REPORT_OUTPUT_FOLDER = "/Users/dmitriykuptsov/workspace/front-end-development/balance/backend/output"

# File storage
#SUPPLEMENT_FILE_STORAGE = "/opt/balans/repository/"
#SUPPLEMENT_FILE_STORAGE = "C:\\Work\\balance\\repository\\"
SUPPLEMENT_FILE_STORAGE = "/Users/dmitriykuptsov/workspace/front-end-development/balance/repository"
ALLOWED_EXTENSIONS = ['str', 'dat', 'doc', 'docx', 'tridb', 'jpeg', 'jpg', 'png']

MAX_CONTENT_PATH = 30*1024*1024;

IMPORT_FILE_STORAGE = "/Users/dmitriykuptsov/workspace/front-end-development/balance/backend/import"
