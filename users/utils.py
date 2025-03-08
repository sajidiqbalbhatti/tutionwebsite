from PIL import Image

def save_profile_image(image_file, path):
    img = Image.open(image_file)

    # Optional: Agar resizing zaroori hai (for thumbnails), tab bhi quality ko preserve karo
    img = img.convert('RGB')  # Ensure compatibility (only for JPG, not PNG)

    # Save with high quality
    img.save(path, format='JPEG', quality=95)  # 95 is very high
