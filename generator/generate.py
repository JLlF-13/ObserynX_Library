from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json
import os
import textwrap
import math
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "quotes.json"))
FONT_PATH = os.path.join(BASE_DIR, "font.ttf")
IMAGES_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "images"))

os.makedirs(IMAGES_DIR, exist_ok=True)

with open(DATA_PATH, "r", encoding="utf-8") as f:
    quotes = json.load(f)

WIDTH, HEIGHT = 1080, 1080
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2

PALETTE = {
    1: (18, 18, 20),
    2: (35, 90, 65),
    3: (40, 85, 140)
}

def radial_gradient(color):
    img = Image.new("RGB", (WIDTH, HEIGHT), color)
    pixels = img.load()

    max_dist = math.sqrt(CENTER_X**2 + CENTER_Y**2)

    for y in range(HEIGHT):
        for x in range(WIDTH):
            dx = x - CENTER_X
            dy = y - CENTER_Y

            dist = math.sqrt(dx*dx + dy*dy)
            t = dist / max_dist

            base = 1 - (t * 0.75)
            light = (x / WIDTH) * 0.18

            factor = base + light

            pixels[x, y] = (
                int(color[0] * factor),
                int(color[1] * factor),
                int(color[2] * factor),
            )

    return img

def add_spots(img, color, intensity=60):
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    for _ in range(random.randint(10, 20)):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)

        r = random.randint(120, 420)

        alpha = random.randint(18, intensity)

        draw.ellipse(
            (x - r, y - r, x + r, y + r),
            fill=(*color, alpha)
        )

    overlay = overlay.filter(ImageFilter.GaussianBlur(45))
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

def add_vignette(img):
    overlay = Image.new("L", (WIDTH, HEIGHT), 0)
    draw = ImageDraw.Draw(overlay)

    for y in range(HEIGHT):
        for x in range(WIDTH):
            dx = x - CENTER_X
            dy = y - CENTER_Y
            dist = math.sqrt(dx*dx + dy*dy)

            value = int(min(255, dist / 2.8))
            draw.point((x, y), value)

    overlay = overlay.filter(ImageFilter.GaussianBlur(120))
    return Image.composite(img, Image.new("RGB", img.size, (0,0,0)), overlay)

def get_template(qtype):
    if qtype == 1:
        return "minimal_dark"
    elif qtype == 2:
        return "calm_editorial"
    else:
        return "bold_quote"


for quote in quotes:

    output_path = os.path.join(IMAGES_DIR, f"ObserynX_{quote['id']}.jpg")

    if os.path.exists(output_path):
        print(f"Saltando {output_path}")
        continue

    qtype = quote.get("type", 1)
    template = get_template(qtype)

    base_color = PALETTE.get(qtype, PALETTE[1])

    img = Image.new("RGB", (WIDTH, HEIGHT), base_color)

    if qtype == 1:
        img = add_spots(img, (140, 40, 40), intensity=70)
        img = add_vignette(img)

    elif qtype == 2:
        img = add_spots(img, (210, 240, 210), intensity=55)
        img = add_vignette(img)

    else:
        img = add_spots(img, (255, 255, 255), intensity=50)
        img = add_vignette(img)

    draw = ImageDraw.Draw(img)

    text = quote["text"]

    if template == "minimal_dark":
        font_size = 56
        wrap = 28
        spacing = 10
        stroke = 4

    elif template == "calm_editorial":
        font_size = 52
        wrap = 32
        spacing = 14
        stroke = 3

    else:
        font_size = 68
        wrap = 22
        spacing = 12
        stroke = 5

    font = ImageFont.truetype(FONT_PATH, font_size)
    wrapped = textwrap.fill(text, width=wrap)

    bbox = draw.multiline_textbbox((0, 0), wrapped, font=font, spacing=spacing)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    x = (WIDTH - w) / 2 + random.randint(-2, 2)
    y = (HEIGHT - h) / 2 + random.randint(-2, 2)

    if qtype == 1:
        text_color = (235, 220, 185)
    elif qtype == 2:
        text_color = (210, 245, 225)
    else:
        text_color = (220, 235, 255)

    outline_color = (
        int(base_color[0] * 0.15),
        int(base_color[1] * 0.15),
        int(base_color[2] * 0.15)
    )

    draw.multiline_text(
        (x, y),
        wrapped,
        font=font,
        fill=text_color,
        spacing=spacing,
        align="center",
        stroke_width=stroke,
        stroke_fill=outline_color
    )

    grain = Image.effect_noise((WIDTH, HEIGHT), 28)
    grain = grain.convert("L").point(lambda x: x * 0.2)
    img = Image.blend(img, grain.convert("RGB"), 0.12)

    img = img.filter(ImageFilter.GaussianBlur(0.5))

    img.save(output_path, quality=95)