import json
import subprocess

# Adjust these paths to your analysis engine, config, and model.
kata_analyze_path = r'C:\Workspace\gowallpaper\katago\katago.exe'
analysis_config_path = r'C:\Workspace\gowallpaper\katago\analysis_example.cfg'
analysis_model_path = r'C:\Workspace\gowallpaper\katago\b18c384nbt-humanv0.bin.gz'


def run_analysis(moves, board_size, komi, rules="tromp-taylor"):
    """
    Runs kata-analyze for the final game position.
    `moves` should be a list of [player, location] pairs in GTP format, e.g. ["B", "Q16"].
    """
    # Build the JSON query.
    query = {
        "id": "final_analysis",
        "moves": moves,
        "rules": rules,
        "komi": komi,
        "boardXSize": board_size,
        "boardYSize": board_size,
        "includeOwnership": True,  # Request ownership predictions
        "includeOwnershipStdev": True,
        "overrideSettings": {
            "humanSLProfile": "rank_3d"
        }
    }
    query_str = json.dumps(query)


    # Launch kata-analyze as a subprocess.
    proc = subprocess.Popen(
        [kata_analyze_path, "analysis", "-config", analysis_config_path, "-model", analysis_model_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        bufsize=1
    )

    # Send the query.
    proc.stdin.write(query_str + "\n")
    proc.stdin.flush()

    grid = []
    line = proc.stdout.readline()
    # Look for a line that starts with "ownership"
    line_obj = json.loads(line)
    # Convert such that all positive scores are for black, all negative are for white
    # Normalize to 1 and -1
    ownership = line_obj["ownership"]
    for r in range(board_size):
        row = ownership[r * board_size:(r + 1) * board_size]
        grid.append(row)


    proc.stdin.close()
    proc.stdout.close()
    proc.kill()
    return grid
