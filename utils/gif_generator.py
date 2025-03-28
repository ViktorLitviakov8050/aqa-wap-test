import os
from PIL import Image
import logging

class GifGenerator:
    """Utility class for generating GIFs from test screenshots"""
    
    def __init__(self, output_dir='reports/gifs'):
        self.output_dir = output_dir
        self.logger = logging.getLogger(__name__)
        os.makedirs(output_dir, exist_ok=True)
    
    def create_gif_from_screenshots(self, screenshots_dir, output_name, duration=500):
        """
        Create a GIF from a directory of screenshots
        
        Args:
            screenshots_dir: Directory containing screenshots
            output_name: Name for the output GIF file
            duration: Duration for each frame in milliseconds
        """
        try:
            # Get all PNG files in the directory
            screenshots = sorted([f for f in os.listdir(screenshots_dir) if f.endswith('.png')])
            
            if not screenshots:
                self.logger.warning(f"No screenshots found in {screenshots_dir}")
                return
            
            # Open all images
            images = []
            for screenshot in screenshots:
                img_path = os.path.join(screenshots_dir, screenshot)
                images.append(Image.open(img_path))
            
            # Create output path
            output_path = os.path.join(self.output_dir, f"{output_name}.gif")
            
            # Save as GIF
            images[0].save(
                output_path,
                save_all=True,
                append_images=images[1:],
                duration=duration,
                loop=0
            )
            
            self.logger.info(f"GIF created successfully at {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Failed to create GIF: {str(e)}")
            raise 