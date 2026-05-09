import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'standarcloud.settings.development')
django.setup()

from django.contrib.auth.models import User

u = User.objects.get(username='admin')
u.set_password('admin1234')
u.save()
print('Password reset to: admin1234')
