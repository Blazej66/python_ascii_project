import PIL.Image
from PIL import ImageDraw, ImageFont
import random

# High-definition ASCII palette (70 characters) sorted from darkest to lightest
ASCII_CHARS = list(" .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$")


def resize_image(image, new_width=100):
    width, height = image.size
    aspect_ratio = height / width / 1.65
    new_height = int(new_width * aspect_ratio)
    return image.resize((new_width, new_height))


def draw_retro_star(draw, x, y, font, char_width, char_height):
    color = (random.randint(140, 240), random.randint(140, 240), random.randint(140, 240))
    star_type = random.choices(
        ['tiny', 'medium', 'o-ring', 'cross', 'glitter', 'spark', 'ufo'],
        weights=[45, 25, 10, 8, 5, 5, 2],
        k=1
    )[0]

    if star_type == 'tiny':
        draw.text((x, y), random.choice([".", ",", "'", "`"]), font=font, fill=color)
    elif star_type == 'medium':
        draw.text((x, y), random.choice(["*", "o"]), font=font, fill=color)
    elif star_type == 'o-ring':
        pattern = random.choice(["-o-", "-)-", "(-o-)"])
        draw.text((x, y), pattern, font=font, fill=color)
    elif star_type == 'cross':
        draw.text((x + char_width, y), "|", font=font, fill=color)
        draw.text((x, y + char_height), "-o-", font=font, fill=color)
        draw.text((x + char_width, y + (2 * char_height)), "|", font=font, fill=color)
    elif star_type == 'glitter':
        draw.text((x + char_width, y), ".", font=font, fill=color)
        draw.text((x, y + char_height), "+", font=font, fill=color)
        draw.text((x + (2 * char_width), y + char_height), ".", font=font, fill=color)
    elif star_type == 'spark':
        draw.text((x, y), "*", font=font, fill=color)
        draw.text((x + char_width, y + char_height), ".", font=font, fill=color)


def convert_to_colored_ascii_image(image_path, output_path="ascii_art.jpg", new_width=150):
    try:
        image = PIL.Image.open(image_path)
    except Exception as e:
        print(f"Error: Unable to open {image_path}.")
        return

    # Resize and ensure RGB color mode
    image = resize_image(image, new_width).convert("RGB")
    width, height = image.size

    font = ImageFont.load_default()
    char_width = 6
    char_height = 10

    out_img_width = width * char_width
    out_img_height = height * char_height

    # Upgraded to 4K resolution canvas for maximum detail
    screen_width, screen_height = 3840, 2160
    output_image = PIL.Image.new("RGB", (screen_width, screen_height), color=(10, 10, 12))
    draw = ImageDraw.Draw(output_image)

    offset_x = (screen_width - out_img_width) // 2
    offset_y = (screen_height - out_img_height) // 2

    # Exclusion zone to protect the main image
    exclusion_margin = 60
    safe_left = offset_x - exclusion_margin
    safe_right = offset_x + out_img_width + exclusion_margin
    safe_top = offset_y - exclusion_margin
    safe_bottom = offset_y + out_img_height + exclusion_margin

    print("[PROCESSING] Generating detailed 4K starfield...")

    # Increased star count to fill the massive 4K canvas
    for _ in range(1200):
        star_x = random.randint(20, screen_width - 60)
        star_y = random.randint(20, screen_height - 60)

        if (safe_left < star_x < safe_right) and (safe_top < star_y < safe_bottom):
            continue

        draw_retro_star(draw, star_x, star_y, font, char_width, char_height)

    print("[PROCESSING] Drawing high-resolution ASCII image onto canvas...")

    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))
            brightness = int(0.299 * r + 0.587 * g + 0.114 * b)

            if brightness < 18:
                continue

            # Map brightness (0-255) to the new 70-character palette
            char_index = int((brightness / 255) * (len(ASCII_CHARS) - 1))
            char = ASCII_CHARS[char_index]

            draw.text((x * char_width + offset_x, y * char_height + offset_y), char, font=font, fill=(r, g, b))

    output_image.save(output_path)
    print(f"[SUCCESS] High-res colored ASCII art saved to {output_path}")


if __name__ == "__main__":
    target_image = "talia_rain.jpg"
    # new_width set to 450 to utilize the 4K canvas and heavily increase detail
    convert_to_colored_ascii_image(target_image, output_path="colored_ascii_output_4k.jpg", new_width=260)