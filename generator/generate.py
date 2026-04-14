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

    base_color = random.randint(0, 40)  # antes 5–15, ahora mucho más rango
    img = Image.new("RGB", (WIDTH, HEIGHT), (base_color, base_color, base_color))
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    text = quote["text"]

    wrapped = textwrap.fill(text, width=random.randint(26, 34))

    bbox = draw.multiline_textbbox((0, 0), wrapped, font=font, spacing=10)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    position_choice = random.choice(["top", "center", "bottom"])

    if position_choice == "top":
        y = HEIGHT * 0.18
    elif position_choice == "bottom":
        y = HEIGHT * 0.65
    else:
        y = (HEIGHT - h) / 2

    x = (WIDTH - w) / 2

    text_color = random.randint(150, 220)

    draw.multiline_text(
        (x, y),
        wrapped,
        font=font,
        fill=(text_color, text_color, text_color),
        spacing=10,
        align="center"
    )

    vignette_strength = random.uniform(1.2, 2.5)
    vignette_blur = random.randint(60, 140)

    vignette = Image.new("L", (WIDTH, HEIGHT), 0)
    for i in range(WIDTH):
        for j in range(HEIGHT):
            dist = ((i - WIDTH/2)**2 + (j - HEIGHT/2)**2)**0.5
            vignette.putpixel((i, j), int(min(255, dist / vignette_strength)))

    vignette = vignette.filter(ImageFilter.GaussianBlur(vignette_blur))
    img = Image.composite(img, Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0)), vignette)

    grain_intensity = random.randint(40, 120)
    noise = Image.effect_noise((WIDTH, HEIGHT), grain_intensity)
    noise = noise.convert("L").point(lambda x: x * random.uniform(0.3, 0.7))
    img = Image.blend(img, noise.convert("RGB"), random.uniform(0.25, 0.45))

    if random.random() < 0.4:
        img = img.filter(ImageFilter.GaussianBlur(random.randint(1, 3)))

    # Save
    img.save(f"images/ObserynX_{quote['id']}.jpg", quality=95)

print("Dark images generated with strong variations.")
