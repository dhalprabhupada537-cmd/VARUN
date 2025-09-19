import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def generate_soil_images():
    """
    Generate soil type images if they don't exist
    """
    try:
        soil_colors = {
            "clay": (180, 120, 80),
            "loam": (160, 100, 60),
            "sand": (220, 200, 160),
            "silt": (200, 180, 140),
            "clay_loam": (170, 110, 70),
            "sandy_loam": (210, 190, 150),
            "silt_loam": (190, 170, 130)
        }
        
        os.makedirs("assets/soil_types", exist_ok=True)
        
        for soil_type, color in soil_colors.items():
            img_path = f"assets/soil_types/{soil_type}.png"
            if not os.path.exists(img_path):
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
                    font = ImageFont.truetype("arial.ttf", 40)
                except:
                    font = ImageFont.load_default()
                
                draw.text((120, 120), soil_type.upper().replace('_', ' '), fill=(255, 255, 255), font=font)
                img.save(img_path)
                
        return True
    except Exception as e:
        print(f"Error generating soil images: {e}")
        return False

def generate_logo():
    """
    Generate logo if it doesn't exist
    """
    try:
        if not os.path.exists("assets/logo.png"):
            img = Image.new('RGB', (400, 200), color=(46, 139, 87))
            draw = ImageDraw.Draw(img)
            
            # Draw VARUN text
            try:
                font = ImageFont.truetype("arial.ttf", 40)
            except:
                font = ImageFont.load_default()
            
            draw.text((120, 70), "VARUN", fill=(255, 255, 255), font=font)
            draw.text((130, 120), "ai", fill=(255, 215, 0), font=font)
            
            # Draw plant icon
            draw.ellipse([(30, 70), (90, 130)], fill=(255, 215, 0))  # Sun
            img.save("assets/logo.png")
            
        return True
    except Exception as e:
        print(f"Error generating logo: {e}")
        return False
