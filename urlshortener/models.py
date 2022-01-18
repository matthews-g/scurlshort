from django.db import models
from datetime import datetime

import random
import string


# Create your models here.

class ShortUrlModel(models.Model):

    # This is the 'base' ShortUrlModel

    SHORT_CODE_LEN = 6
    CODE_CHARS = (
            string.ascii_uppercase
            + string.ascii_lowercase
            + string.digits + "_")
    shortcode = models.CharField(max_length=SHORT_CODE_LEN, unique=True, blank=False)
    url = models.URLField(blank=False, name="url")
    creation_date = models.DateTimeField(auto_now_add=True)  # GMT
    redirect_count = models.IntegerField(default=0)
    last_redirect = models.DateTimeField(auto_now_add=True)  # GMT

    class Meta:
        ordering = ('-creation_date',)

    def __str__(self):
        return f'<short id: {self.short_code} url: {self.url}>'

    def increment_redirect_count(self):
        """ When the shortcode is requested, we add to the count of the redirects and update the last redirect date"""
        self.last_redirect = datetime.now()  # GMT
        self.redirect_count += 1
        self.save()

    @classmethod
    def check_shortcode_rules(cls, short_code) -> bool:
        """ Check if the shortcode is satisfying the specified rules"""
        if len(short_code) != 6:
            return False
        charlist = list(cls.CODE_CHARS)
        for char in short_code:
            if char not in charlist:
                return False
        return True

    @classmethod
    def generate_short_code(cls, short_code="") -> str:
        """ Logic of generating the shortcode """
        if not short_code:
            short_code = "".join(random.sample(cls.CODE_CHARS, cls.SHORT_CODE_LEN))
        return short_code
