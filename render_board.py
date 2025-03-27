from PIL import Image, ImageDraw
import ctypes


def load_stone_image(png_path, size=None):
    img = Image.open(png_path).convert("RGBA")
    if size:
        # Resize the stone image if needed.
        img = img.resize((size, size), Image.Resampling.LANCZOS)
    return img


stone_size = 60
black_stone = load_stone_image("black_stone.png", stone_size)
white_stone = load_stone_image("white_stone.png", stone_size)

def get_screen_resolution():
    user32 = ctypes.windll.user32
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


def render_board_on_canvas(game, board_size=19):
    screen_width, screen_height = get_screen_resolution()

    # Set margins for the board drawing within the board image
    left_margin = right_margin = 40
    top_margin = 40
    bottom_margin = 80  # increased bottom margin

    # Determine available drawing area
    available_width = screen_width - left_margin - right_margin
    available_height = screen_height - top_margin - bottom_margin

    # Compute cell_size so that (board_size-1) intervals fit within the available space
    cell_size = min(available_width / (board_size - 1), available_height / (board_size - 1))

    # Calculate board image size (only the board, not the entire screen)
    board_img_width = int(left_margin + right_margin + (board_size - 1) * cell_size)
    board_img_height = int(top_margin + bottom_margin + (board_size - 1) * cell_size)

    board_img = Image.new("RGB", (board_img_width, board_img_height), "burlywood")
    draw = ImageDraw.Draw(board_img)

    # Draw horizontal grid lines (one per intersection row)
    for i in range(board_size):
        y = top_margin + i * cell_size
        draw.line([(left_margin, y), (left_margin + (board_size - 1) * cell_size, y)], fill="black")
    # Draw vertical grid lines (one per intersection column)
    for j in range(board_size):
        x = left_margin + j * cell_size
        draw.line([(x, top_margin), (x, top_margin + (board_size - 1) * cell_size)], fill="black")

    # Draw stones at intersections
    for row in range(board_size):
        for col in range(board_size):
            stone = game.board[row][col]
            if stone in ('B', 'W'):
                center_x = left_margin + col * cell_size
                center_y = top_margin + row * cell_size
                pos = (int(center_x - stone_size // 2), int(center_y - stone_size // 2))
                if stone == 'B':
                    board_img.paste(black_stone, pos, black_stone)
                else:
                    board_img.paste(white_stone, pos, white_stone)

    # Create a canvas matching the screen resolution and paste the board image centered
    canvas = Image.new("RGB", (screen_width, screen_height), "burlywood")
    paste_x = (screen_width - board_img_width) // 2
    paste_y = (screen_height - board_img_height) // 2
    canvas.paste(board_img, (paste_x, paste_y))
    return canvas

# Example usage:
# img = render_board(game)
# img.show()  # For testing; later save and set as wallpaper.
