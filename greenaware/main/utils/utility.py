import random
import string
from ..models import CustomUser

def generate_unique_user_id(length=10):
    characters = string.ascii_letters + string.digits
    user_id = ''.join(random.choice(characters) for _ in range(length))

    # Check if the generated user_id already exists in the CustomUser table
    while CustomUser.objects.filter(user_id=user_id).exists():
        # If it exists, generate a new one until a unique user_id is found
        user_id = ''.join(random.choice(characters) for _ in range(length))

    return user_id.lower()
