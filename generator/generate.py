from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json
import os
import textwrap
import random

# Load quotes
with open("data/quotes.json", "r", encoding="utf-8") as f:
    quotes = json.load(f)

# Create folder if missing
os.makedirs("images", exist_ok=True)

WIDTH = 1080
HEIGHT = 1080
FONT_PATH = "generator/font.ttf"
FONT_SIZE = 58

for quote in quotes:
    # Deep dark background with slight random variation
    base_color = random.randint(5, 15)
    img = Image.new("RGB", (WIDTH, HEIGHT), (base_color, base_color, base_color))
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    text = quote["text"]

    # Auto-wrap text
    wrapped = textwrap.fill(text, width=32)

    # Calculate multiline text size
    bbox = draw.multiline_textbbox((0, 0), wrapped, font=font, spacing=10)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    # Center text
    x = (WIDTH - w) / 2
    y = (HEIGHT - h) / 2

    # Draw text
    draw.multiline_text(
        (x, y),
        wrapped,
        font=font,
        fill=(180, 180, 180),
        spacing=10,
        align="center"
    )

    # Vignette effect
    vignette = Image.new("L", (WIDTH, HEIGHT), 0)
    for i in range(WIDTH):
        for j in range(HEIGHT):
            dist = ((i - WIDTH/2)**2 + (j - HEIGHT/2)**2)**0.5
            vignette.putpixel((i, j), int(min(255, dist / 1.8)))
    vignette = vignette.filter(ImageFilter.GaussianBlur(90))
    img = Image.composite(img, Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0)), vignette)

    # Grain
    noise = Image.effect_noise((WIDTH, HEIGHT), random.randint(20, 50))
    noise = noise.convert("L").point(lambda x: x * 0.4)
    img = Image.blend(img, noise.convert("RGB"), 0.25)

    # Save
    img.save(f"images/ObserynX_{quote['id']}.jpg", quality=95)

print("Dark images generated successfully.")
