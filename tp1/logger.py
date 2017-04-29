DEBUG = 0
def log(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)
