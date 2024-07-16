def print_function_name(func):
    def wrapper(*args, **kwargs):
        print(f"Executing function: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
