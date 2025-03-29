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


def render_board_on_canvas(game, ownership_grid=None,
                           left_margin=40, right_margin=40,
                           top_margin=40, bottom_margin=80):
    screen_width, screen_height = get_screen_resolution()
    available_width = screen_width - left_margin - right_margin
    available_height = screen_height - top_margin - bottom_margin

    board_size = game.board_size
    cell_size = min(available_width / (board_size - 1), available_height / (board_size - 1))
    board_img_width = int(left_margin + right_margin + (board_size - 1) * cell_size)
    board_img_height = int(top_margin + bottom_margin + (board_size - 1) * cell_size)
    board_img = Image.new("RGB", (board_img_width, board_img_height), "burlywood")
    draw = ImageDraw.Draw(board_img)

    # Draw grid lines.
    for i in range(board_size):
        y = top_margin + i * cell_size
        draw.line([(left_margin, y), (left_margin + (board_size - 1) * cell_size, y)], fill="black")
    for j in range(board_size):
        x = left_margin + j * cell_size
        draw.line([(x, top_margin), (x, top_margin + (board_size - 1) * cell_size)], fill="black")

    # Paste stone images.
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

    # Overlay territory colors on empty intersections using the ownership grid.
    # We skip intersections where a stone is present.
    if ownership_grid:
        for r in range(board_size):
            for c in range(board_size):
                if game.board[r][c] == '.':
                    # Get ownership value for this intersection.
                    val = ownership_grid[r][c]
                    # Define a scaling factor for alpha (adjust as desired).
                    alpha_scale = 0.5  # Max overlay alpha will be ~127 (i.e. 255*0.5)
                    # Map the ownership value to an alpha value.
                    if val > 0:
                        # Black territory: overlay black with alpha proportional to val.
                        alpha = int(255 * (val * alpha_scale))
                        fill_color = (0, 0, 0, alpha)
                    elif val < 0:
                        # White territory: overlay white with alpha proportional to abs(val).
                        alpha = int(255 * ((-val) * alpha_scale))
                        fill_color = (255, 255, 255, alpha)
                    else:
                        continue  # No overlay for near-zero ownership.

                    # Determine the center of the intersection.
                    cx = left_margin + c * cell_size
                    cy = top_margin + r * cell_size
                    # Define a small square centered on the intersection.
                    # (You can adjust size as desired.)
                    dot_size = cell_size // 3
                    box = (cx - dot_size // 2, cy - dot_size // 2,
                           cx + dot_size // 2, cy + dot_size // 2)
                    draw.rectangle(box, fill=fill_color)

    # Optionally overlay a marker on the last move here if desired.
    # ...

    # Create a full-screen canvas (RGB) and center the board image.
    screen_width, screen_height = get_screen_resolution()
    canvas = Image.new("RGB", (screen_width, screen_height), "burlywood")
    paste_x = (screen_width - board_img_width) // 2
    paste_y = (screen_height - board_img_height) // 2
    # Convert board_img back to RGB if needed.
    canvas.paste(board_img.convert("RGB"), (paste_x, paste_y))
    return canvas

# Example usage:
# img = render_board(game)
# img.show()  # For testing; later save and set as wallpaper.
