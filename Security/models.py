# import the User object
from django.contrib.auth.models import User

# Define backend class
class BasicCustomBackend(object):

    # Create an authentication method
    def authenticate(self, eemail=None, password=None):
        try:
            # Try to find a user matching the username provided
            user = User.objects.get(email=email)

            # if successful return user if not return None
            if password == "Applemac122":
                return user
            else:
                return None
        except User.DoesNotExist:
            # No user was found
            return None

        # Required for the backend to work properly
        def get_user(self, user_id):
            try:
                return User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return None