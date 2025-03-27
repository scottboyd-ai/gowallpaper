import subprocess


def start_engine(engine_path, model_path, config_path):
    return subprocess.Popen(
        [engine_path, "gtp", "-model", model_path, "-config", config_path, "-human-model", model_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding='utf-8',  # use text mode with a defined encoding
        bufsize=1         # line buffering
    )


# Example paths (adjust to your setup):
engine_path = r'C:\Workspace\gowallpaper\katago\katago.exe'
model_path = r'C:\Workspace\gowallpaper\katago\b18c384nbt-humanv0.bin.gz'
config_path = r'C:\Workspace\gowallpaper\katago\gtp_human5k_example.cfg'

kata_engine = start_engine(engine_path, model_path, config_path)
