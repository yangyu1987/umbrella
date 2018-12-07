from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model,authenticate
User = get_user_model()

from django.db.models import Q


class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None
