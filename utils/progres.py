def progress_bar(percentage, length=20):
    """
    Returns a string representing a progress bar.
    percentage: 0-100
    length: number of characters in the bar
    """
    filled_length = int(length * percentage // 100)
    bar = "█" * filled_length + "-" * (length - filled_length)
    return f"[{bar}] {percentage:.0f}%"
