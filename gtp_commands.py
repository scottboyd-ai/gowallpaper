import subprocess
import threading
import queue


def enqueue_output(out, out_queue):
    # Read lines until EOF and put them in a queue.
    for line in iter(out.readline, ''):
        out_queue.put(line)
    out.close()


# def send_gtp_command(engine, command):
#     # Ensure the command ends with a newline
#     if not command.endswith('\n'):
#         command += '\n'
#     engine.stdin.write(command)
#     engine.stdin.flush()
#     response = []
#     # Read until a blank line or end of output
#     while True:
#         line = engine.stdout.readline()
#         if not line:
#             break
#         line = line.strip()
#         response.append(line)
#         if line == "":
#             break
#     return response

def send_gtp_command(engine, command, timeout=10):
    engine.stdin.write(command + "\n")
    engine.stdin.flush()

    output_lines = []
    # Read output until we get a line starting with '=' or '?'
    while True:
        line = engine.stdout.readline()
        if not line:  # EOF reached
            break
        line = line.strip()
        # Skip initial empty lines
        if line == "" and not output_lines:
            continue
        output_lines.append(line)
        if line.startswith('=') or line.startswith('?'):
            # Assume that once we have a response indicator, the response is complete.
            break
    return output_lines


# Example: Request a move from an engine (you’ll need to handle proper GTP command formatting)
def request_move(engine, current_player):
    # Construct a command like "genmove B" or "genmove W"
    # Here, board_state could be used to update engine's internal representation via 'loadsgf' or similar.
    response = send_gtp_command(engine, f"genmove {current_player}")
    # Parse response; this example assumes the engine returns a coordinate like "D4"
    move = response[-1].strip()
    return move


# Helper to convert GTP coordinates to board indices (if needed)
def gtp_to_index(gtp_move, board_size=19):
    # Remove leading '=' if present, and strip whitespace.
    if gtp_move.startswith('='):
        move_str = gtp_move[1:].strip()
    else:
        move_str = gtp_move.strip()

    if move_str.lower() == 'pass':
        return 'pass'
    if move_str.lower() == 'resign':
        return 'resign'
    letter = move_str[0].upper()
    number = int(move_str[1:].strip())
    if letter >= 'I':
        col = ord(letter) - ord('A') - 1
    else:
        col = ord(letter) - ord('A')
    row = board_size - number
    return (row, col)


