def validate_file_extensions(file_name: str) -> bool:
    if file_name.endswith("jpg"):
        return True
    else:
        return False

