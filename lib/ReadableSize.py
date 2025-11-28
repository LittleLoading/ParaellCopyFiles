


def get_readable_size(size_in_bytes):
    """
    Converts bytesize into readable size.
    :param size_in_bytes: int/float amount of bytes
    :return: string readable size
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.2f} TB"
