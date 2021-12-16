"""
File containing simple server-side validators in form of functors
"""
from rest_framework import serializers
import re


class ValidatePattern:
    """
    Functor class for validating string pattern
    Using Regular Expressions
    """
    def __init__(self, pattern: str, msg: str = None):
        self.pattern = pattern
        self.msg = msg

    def __call__(self, value):
        if not re.fullmatch(self.pattern, value):
            raise serializers.ValidationError(self.msg)


class ValidateName:
    """
    Functor class for validating real name
    Based on word count limit and checking symbols different from letters and hyphens
    """
    def __init__(self, min_words=2, max_words=3, msg: str = None):
        self.min_words = min_words
        self.max_words = max_words

        self.msg = msg

    def __call__(self, value):
        words = value.split()
        if not (self.min_words <= len(words) <= self.max_words):
            raise serializers.ValidationError(self.msg)

        for word in words:
            if not word.isalpha():
                sub_words = word.split("-")

                for sub_word in sub_words:
                    if not sub_word.isalpha():
                        raise serializers.ValidationError(self.msg)
