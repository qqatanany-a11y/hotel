import os 
from pathlib import Path 

BASE_DIR =Path (__file__ ).resolve ().parent .parent 

SECRET_KEY ='django-insecure-your-secret-key-here-change-in-production'

DEBUG =True 

ALLOWED_HOSTS =['*']

INSTALLED_APPS =[
'django.contrib.admin',
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.messages',
'django.contrib.staticfiles',
'hotel',
'crispy_forms',
'crispy_bootstrap4',
]

MIDDLEWARE =[
'django.middleware.security.SecurityMiddleware',
'django.contrib.sessions.middleware.SessionMiddleware',
'django.middleware.common.CommonMiddleware',
'django.middleware.csrf.CsrfViewMiddleware',
'django.contrib.auth.middleware.AuthenticationMiddleware',
'django.contrib.messages.middleware.MessageMiddleware',
'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF ='hotel_project.urls'

TEMPLATES =[
{
'BACKEND':'django.template.backends.django.DjangoTemplates',
'DIRS':[BASE_DIR /'templates'],
'APP_DIRS':True ,
'OPTIONS':{
'context_processors':[
'django.template.context_processors.debug',
'django.template.context_processors.request',
'django.contrib.auth.context_processors.auth',
'django.contrib.messages.context_processors.messages',
'django.template.context_processors.i18n',
],
},
},
]

WSGI_APPLICATION ='hotel_project.wsgi.application'

DATABASES ={
'default':{
'ENGINE':'django.db.backends.mysql',
'NAME':'hotel',
'USER':'root',
'PASSWORD':'qwsa12ed',
'HOST':'localhost',
'PORT':'3306',
'OPTIONS':{
'charset':'utf8mb4',
},
}
}


AUTH_PASSWORD_VALIDATORS =[
{
'NAME':'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
},
{
'NAME':'django.contrib.auth.password_validation.MinimumLengthValidator',
},
{
'NAME':'django.contrib.auth.password_validation.CommonPasswordValidator',
},
{
'NAME':'django.contrib.auth.password_validation.NumericPasswordValidator',
},
]

LANGUAGE_CODE ='en-us'
TIME_ZONE ='Asia/Amman'
USE_I18N =False 
USE_TZ =True 

LANGUAGES =[
('en','English'),
]

LOCALE_PATHS =[
BASE_DIR /'locale',
]

STATIC_URL ='/static/'
STATIC_ROOT =BASE_DIR /'staticfiles'
STATICFILES_DIRS =[
BASE_DIR /'static',
]

MEDIA_URL ='/media/'
MEDIA_ROOT =BASE_DIR /'media'

DEFAULT_AUTO_FIELD ='django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS ="bootstrap4"
CRISPY_TEMPLATE_PACK ="bootstrap4"

LOGIN_URL ='login'
LOGIN_REDIRECT_URL ='/'
LOGOUT_REDIRECT_URL ='/'



EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST ='smtp.gmail.com'
EMAIL_PORT =587 
EMAIL_USE_TLS =True 
EMAIL_HOST_USER ='qqatanany@gmail.com'
EMAIL_HOST_PASSWORD ='gixljwjearbqvykq'
DEFAULT_FROM_EMAIL ='Hotel Booking System <qqatanany@gmail.com>'

HOTEL_NAME =" Amman Golden Hotel"
HOTEL_ADDRESS ="Amman, Jordan"
HOTEL_PHONE ="+962 782182081"
HOTEL_EMAIL ="ammangoldenhotel@gmail.com"


STATIC_URL ='/static/'
STATICFILES_DIRS =[
BASE_DIR /"static",
]

ADMIN_SITE_HEADER ="Hotel Management"
ADMIN_SITE_TITLE ="Hotel Management"
ADMIN_INDEX_TITLE ="Hotel Management"


