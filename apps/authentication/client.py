from django.contrib.auth import get_user_model

User = get_user_model()

class AuthenticationClient:
    """
    Public interface for the Authentication app.
    """
    
    def get_user_by_id(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    def is_active_user(self, user):
        return user and user.is_authenticated and user.is_active
