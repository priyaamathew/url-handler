from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
import string, random

def generate_short_code():
    length = 6
    chars = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choices(chars, k=length))
        if not URL.objects.filter(short_code=code).exists():
            return code

class URL(models.Model):
    original_url = models.URLField()
    short_code = models.CharField(max_length=8, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def is_expired(self):
        return self.expires_at and timezone.now() > self.expires_at

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = generate_short_code()
        super().save(*args, **kwargs)
