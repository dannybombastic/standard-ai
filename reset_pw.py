import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'standarcloud.settings.development')
django.setup()
from django.contrib.auth.models import User
try:
    u = User.objects.get(username='admin')
    u.set_password('Admin1234!')
    u.save()
    print(f'Password reset OK for user: {u.username} (pk={u.pk}, active={u.is_active})')
except User.DoesNotExist:
    print('User admin not found')
    for u in User.objects.all():
        print(f'  - {u.username}')
