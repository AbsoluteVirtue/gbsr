import random


allowed_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_*!@#$%^&*()+="


def strrand(length):
    return ''.join(random.choices(allowed_chars, k=length))
