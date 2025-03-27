import time

from GoGame import GoGame
from gtp_commands import request_move, gtp_to_index
from render_board import render_board_on_canvas
from save_image import save_board_image
from set_wallpaper import set_wallpaper
from start_engine import kata_engine


def main_game_loop():
    game = GoGame()
    # Assume kata_engine is black, leela_engine is white.
    engines = {'B': kata_engine, 'W': kata_engine}

    while True:
        current_engine = engines[game.current_player]
        # Request move from current engine
        gtp_move = request_move(current_engine, game)
        move = gtp_to_index(gtp_move, game.board_size)

        # For simplicity, assume 'pass' means end of game.
        if move == 'pass':
            print("Game ended with a pass.")
            break
        if move == 'resign':
            resigner = 'B'
            if game.current_player == 'B':
                resigner = 'W'
            print(f"Game ended, {resigner}+R")
            break

        try:
            game.apply_move(move)
        except ValueError as e:
            print(f"Invalid move: {e}")
            break

        # Render board, save image, update wallpaper
        img = render_board_on_canvas(game)
        image_path = save_board_image(img)
        set_wallpaper(image_path)

        # Optional: delay between moves
        # time.sleep(2)

        # # Optionally print board to console for debugging
        # game.display_board()


def main_loop():
    while True:
        main_game_loop()
        print("Game finished. Waiting 60 seconds before starting a new game...")
        time.sleep(60)


if __name__ == "__main__":
    main_loop()
