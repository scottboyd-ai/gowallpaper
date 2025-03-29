import time

from GoGame import GoGame
from gtp_commands import request_move, gtp_to_index, send_gtp_command
from render_board import render_board_on_canvas
from run_analysis import run_analysis
from save_image import save_board_image
from set_wallpaper import set_wallpaper
from start_engine import start_engine

# Example paths (adjust to your setup):
engine_path = r'C:\Workspace\gowallpaper\katago\katago.exe'
model_path = r'C:\Workspace\gowallpaper\katago\b18c384nbt-humanv0.bin.gz'
config_path = r'C:\Workspace\gowallpaper\katago\gtp_human5k_example.cfg'


def main_game_loop():
    game = GoGame()
    # Assume kata_engine is black, leela_engine is white.

    black_engine = start_engine(engine_path, model_path, config_path)
    white_engine = start_engine(engine_path, model_path, config_path)

    engines = {'B': black_engine, 'W': white_engine}

    for engine in engines.values():
        send_gtp_command(engine, "boardsize 19")
        send_gtp_command(engine, "clear_board")
        send_gtp_command(engine, "komi 7.5")

    while True:
        current_engine = engines[game.current_player]
        # Request move from current engine
        gtp_move = request_move(current_engine, game.current_player)
        move_str = gtp_move.lstrip("= ").strip()  # e.g. "Q16"
        move = gtp_to_index(gtp_move, game.board_size)

        # For simplicity, assume 'pass' means end of game.
        if move_str.lower() == 'pass':
            print("Game ended with a pass.")
            break
        if move_str.lower() == 'resign':
            resigner = 'B' if game.current_player == 'W' else 'W'
            print(f"Game ended, {resigner}+R")
            break

        try:
            game.apply_move(move)
        except ValueError as e:
            print(f"Invalid move: {e}")
            break

        # Update both engines with the move that was played.
        # The move was played by the player opposite of game.current_player (since apply_move toggles it).
        played_color = 'B' if game.current_player == 'W' else 'W'
        for engine in engines.values():
            send_gtp_command(engine, f"play {played_color} {move_str}")

        # Render board, save image, update wallpaper
        img = render_board_on_canvas(game)
        image_path = save_board_image(img)
        set_wallpaper(image_path)

    # At game end:
    ownership_grid = run_analysis(game.moves, game.board_size, komi=7.5)

    # Optionally, get the final score from one of the GTP engines.
    score_response = send_gtp_command(black_engine, "final_score")
    score = score_response[-1].lstrip("= ").strip()
    print("Final Score:", score)

    final_img = render_board_on_canvas(game, ownership_grid=ownership_grid)
    final_image_path = save_board_image(final_img, filename="final_board.png")
    set_wallpaper(final_image_path)


def main_loop():
    while True:
        main_game_loop()
        print("Game finished. Waiting 60 seconds before starting a new game...")
        time.sleep(60)


if __name__ == "__main__":
    main_loop()
