import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'standarcloud.settings.development')
django.setup()

from django.contrib.auth.models import User

u = User.objects.filter(username='admin').first()
if u:
    print('User exists: True')
    print('is_active:', u.is_active)
    print('is_staff:', u.is_staff)
    print('check_password 606197854:', u.check_password('606197854'))
else:
    print('User admin does NOT exist')
    print('All users:', list(User.objects.values_list('username', flat=True)))
