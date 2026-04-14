from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json
import os

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
    # Deep dark background
    img = Image.new("RGB", (WIDTH, HEIGHT), (10, 10, 10))
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    text = quote["text"]

    # Center text
    w, h = draw.textsize(text, font=font)
    x = (WIDTH - w) / 2
    y = (HEIGHT - h) / 2

    # Cold gray text
    draw.text((x, y), text, font=font, fill=(180, 180, 180))

    # Vignette effect
    vignette = Image.new("L", (WIDTH, HEIGHT), 0)
    for i in range(WIDTH):
        for j in range(HEIGHT):
            dist = ((i - WIDTH/2)**2 + (j - HEIGHT/2)**2)**0.5
            vignette.putpixel((i, j), int(min(255, dist / 2)))
    vignette = vignette.filter(ImageFilter.GaussianBlur(80))
    img.putalpha(255)
    img = Image.composite(img, Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0)), vignette)

    # Heavy grain
    noise = Image.effect_noise((WIDTH, HEIGHT), 40)
    noise = noise.convert("L").point(lambda x: x * 0.5)
    img = Image.blend(img, noise.convert("RGB"), 0.25)

    # Save
    img.save(f"images/ObserynX_{quote['id']}.jpg", quality=95)

print("Dark images generated.")
