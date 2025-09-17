# generate_images.py
# generate_images.py
from PIL import Image, ImageDraw
import numpy as np
import os

def generate_logo():
    img = Image.new('RGB', (400, 200), color=(46, 139, 87))
    draw = ImageDraw.Draw(img)
    
    # Draw VARUN text
    try:
        from PIL import ImageFont
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = None
    
    draw.text((120, 70), "VARUN", fill=(255, 255, 255), font=font)
    draw.text((130, 120), "ai", fill=(255, 215, 0), font=font)
    
    # Draw plant icon
    draw.ellipse([(30, 70), (90, 130)], fill=(255, 215, 0))
    img.save("assets/logo.png")
    print("Generated logo.png")

def generate_soil_images():
    soil_colors = {
        "clay": (180, 120, 80),
        "loam": (160, 100, 60),
        "sand": (220, 200, 160),
        "silt": (200, 180, 140)
    }
    
    os.makedirs("assets/soil_types", exist_ok=True)
    
    for soil_type, color in soil_colors.items():
        img = Image.new('RGB', (400, 300), color=color)
        draw = ImageDraw.Draw(img)
        
        # Add texture
        for _ in range(800):
            x = np.random.randint(0, 400)
            y = np.random.randint(0, 300)
            size = np.random.randint(2, 8)
            draw.ellipse([(x, y), (x+size, y+size)], 
                       fill=tuple(max(0, c-30) for c in color))
        
        # Add text
        try:
            from PIL import ImageFont
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = None
        
        draw.text((120, 120), soil_type.upper(), fill=(255, 255, 255), font=font)
        img.save(f"assets/soil_types/{soil_type}.png")
        print(f"Generated {soil_type}.png")

if __name__ == "__main__":
    os.makedirs("assets", exist_ok=True)
    generate_logo()
    generate_soil_images()
    print("All images generated successfully!")