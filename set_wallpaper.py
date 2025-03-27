import ctypes
import os


def set_wallpaper(image_path):
    SPI_SETDESKWALLPAPER = 20
    abs_path = os.path.abspath(image_path)
    result = ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, abs_path, 3)
    if not result:
        raise Exception("Failed to set wallpaper")

# Example usage:
# set_wallpaper(image_path)
