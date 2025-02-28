import json
import random
import string
import struct
import hashlib
from functools import wraps

def calculate_checksum(data):
    """Calculate a simple checksum for data integrity verification"""
    if isinstance(data, str):
        data = data.encode()
    return hashlib.md5(data).hexdigest()[:8]  # Using first 8 chars of MD5 as a simple checksum

def generate_id(length=6):
    """Generate a random ID string"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def debug_layer(func):
    """Decorator to add debug output for layer operations"""
    @wraps(func)
    def wrapper(self, data, **kwargs):
        direction = "⬇️" if func.__name__ == "send_down" else "⬆️"
        print(f"{direction} {self.name}: Processing data")
        result = func(self, data, **kwargs)
        return result
    return wrapper