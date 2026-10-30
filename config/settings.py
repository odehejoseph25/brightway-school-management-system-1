import os
from pathlib import Path
import dj_database_url
BASE_DIR=Path(__file__).resolve().parent.parent
SECRET_KEY=os.getenv('DJANGO_SECRET_KEY','unsafe-dev-key-change-before-deployment')
DEBUG=os.getenv('DEBUG','True').lower()=='true'
ALLOWED_HOSTS=[x.strip() for x in os.getenv('ALLOWED_HOSTS','127.0.0.1,localhost').split(',') if x.strip()]
CSRF_TRUSTED_ORIGINS=[x.strip() for x in os.getenv('CSRF_TRUSTED_ORIGINS','').split(',') if x.strip()]
INSTALLED_APPS=['django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles','school']
MIDDLEWARE=['django.middleware.security.SecurityMiddleware','whitenoise.middleware.WhiteNoiseMiddleware','django.contrib.sessions.middleware.SessionMiddleware','django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware','django.contrib.auth.middleware.AuthenticationMiddleware','django.contrib.messages.middleware.MessageMiddleware','django.middleware.clickjacking.XFrameOptionsMiddleware']
ROOT_URLCONF='config.urls'
TEMPLATES=[{'BACKEND':'django.template.backends.django.DjangoTemplates','DIRS':[],'APP_DIRS':True,'OPTIONS':{'context_processors':['django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages']}}]
WSGI_APPLICATION='config.wsgi.application'
DATABASE_URL=os.getenv('DATABASE_URL','')
DATABASES={'default':dj_database_url.parse(DATABASE_URL,conn_max_age=600,ssl_require=not DEBUG)} if DATABASE_URL else {'default':{'ENGINE':'django.db.backends.sqlite3','NAME':BASE_DIR/'db.sqlite3'}}
AUTH_PASSWORD_VALIDATORS=[{'NAME':'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},{'NAME':'django.contrib.auth.password_validation.MinimumLengthValidator'},{'NAME':'django.contrib.auth.password_validation.CommonPasswordValidator'},{'NAME':'django.contrib.auth.password_validation.NumericPasswordValidator'}]
LANGUAGE_CODE='en-ng'; TIME_ZONE='Africa/Lagos'; USE_I18N=True; USE_TZ=True
STATIC_URL='static/'; STATIC_ROOT=BASE_DIR/'staticfiles'
STORAGES={'default':{'BACKEND':'django.core.files.storage.FileSystemStorage'},'staticfiles':{'BACKEND':'whitenoise.storage.CompressedManifestStaticFilesStorage'}}
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'; LOGIN_URL='login'; LOGIN_REDIRECT_URL='dashboard'; LOGOUT_REDIRECT_URL='login'
SESSION_COOKIE_HTTPONLY=True; SECURE_CONTENT_TYPE_NOSNIFF=True; X_FRAME_OPTIONS='DENY'
if not DEBUG:
 SECURE_SSL_REDIRECT=True; SESSION_COOKIE_SECURE=True; CSRF_COOKIE_SECURE=True
