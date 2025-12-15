"""
Image Downloader and Manager for Yu-Gi-Oh! Card Images
Handles downloading, resizing, and validating card images from URLs
"""

import os
import requests
import shutil
from typing import Optional, Tuple
from pathlib import Path

try:
    from PIL import Image
    from io import BytesIO
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("Warning: Pillow not installed. Image resizing will be disabled.")
    print("Install with: pip install Pillow")


class ImageDownloader:
    """Manages card image downloading and processing"""
    
    # Recommended card image dimensions
    RECOMMENDED_WIDTH = 177
    RECOMMENDED_HEIGHT = 254
    
    def __init__(self, pics_directory: str = "../pics"):
        """
        Initialize image downloader
        
        Args:
            pics_directory: Directory where card images should be saved
        """
        self.pics_directory = pics_directory
        self._ensure_directory_exists()
    
    def _ensure_directory_exists(self):
        """Create pics directory if it doesn't exist"""
        if not os.path.exists(self.pics_directory):
            os.makedirs(self.pics_directory)
            print(f"Created directory: {self.pics_directory}")
    
    def download_image(self, url: str, card_id: int, resize: bool = True, 
                       overwrite: bool = False) -> Optional[str]:
        """
        Download an image from a URL and save it as the card image
        
        Args:
            url: URL of the image to download
            card_id: Card ID (used for filename)
            resize: Whether to resize the image to recommended dimensions
            overwrite: Whether to overwrite existing image files
        
        Returns:
            Path to saved image file or None if failed
        """
        try:
            # Check if image already exists
            existing_path = self.find_existing_image(card_id)
            if existing_path and not overwrite:
                print(f"Image already exists: {existing_path}")
                print(f"Use overwrite=True to replace it")
                return existing_path
            
            # Download image
            print(f"Downloading image from: {url}")
            response = requests.get(url, timeout=30, stream=True)
            response.raise_for_status()
            
            # Check content type
            content_type = response.headers.get('content-type', '')
            if 'image' not in content_type.lower():
                print(f"Warning: URL may not be an image (content-type: {content_type})")
            
            # Get image data
            image_data = response.content
            
            # Determine file extension
            extension = self._get_extension_from_url(url, content_type)
            if not extension:
                extension = '.jpg'  # Default to jpg
            
            # Save path
            save_path = os.path.join(self.pics_directory, f"{card_id}{extension}")
            
            # Process image if PIL is available and resize is requested
            if PIL_AVAILABLE and resize:
                try:
                    # Open image with PIL
                    img = Image.open(BytesIO(image_data))
                    
                    # Get original dimensions
                    orig_width, orig_height = img.size
                    print(f"Original image size: {orig_width}x{orig_height}")
                    
                    # Resize if necessary
                    if orig_width != self.RECOMMENDED_WIDTH or orig_height != self.RECOMMENDED_HEIGHT:
                        print(f"Resizing to recommended size: {self.RECOMMENDED_WIDTH}x{self.RECOMMENDED_HEIGHT}")
                        img = img.resize(
                            (self.RECOMMENDED_WIDTH, self.RECOMMENDED_HEIGHT),
                            Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else Image.LANCZOS
                        )
                    
                    # Convert to RGB if necessary (for PNG with transparency)
                    if img.mode in ('RGBA', 'LA', 'P'):
                        rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        rgb_img.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                        img = rgb_img
                    
                    # Save as JPEG
                    img.save(save_path, 'JPEG', quality=95)
                    print(f"✓ Image processed and saved: {save_path}")
                    
                except Exception as e:
                    print(f"Warning: Could not process image with PIL: {e}")
                    print(f"Saving original image without processing...")
                    # Save raw image data
                    with open(save_path, 'wb') as f:
                        f.write(image_data)
                    print(f"✓ Image saved (original): {save_path}")
            else:
                # Save raw image data without processing
                with open(save_path, 'wb') as f:
                    f.write(image_data)
                print(f"✓ Image saved: {save_path}")
            
            return save_path
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Error downloading image: {e}")
            return None
        except Exception as e:
            print(f"✗ Error saving image: {e}")
            return None
    
    def _get_extension_from_url(self, url: str, content_type: str = '') -> Optional[str]:
        """
        Determine file extension from URL or content type
        
        Args:
            url: Image URL
            content_type: HTTP content-type header
        
        Returns:
            File extension (e.g., '.jpg', '.png') or None
        """
        # Try to get extension from URL
        url_lower = url.lower()
        if '.jpg' in url_lower or '.jpeg' in url_lower:
            return '.jpg'
        if '.png' in url_lower:
            return '.png'
        if '.gif' in url_lower:
            return '.gif'
        if '.webp' in url_lower:
            return '.webp'
        
        # Try to get from content type
        if content_type:
            content_lower = content_type.lower()
            if 'jpeg' in content_lower or 'jpg' in content_lower:
                return '.jpg'
            if 'png' in content_lower:
                return '.png'
            if 'gif' in content_lower:
                return '.gif'
            if 'webp' in content_lower:
                return '.webp'
        
        return None
    
    def find_existing_image(self, card_id: int) -> Optional[str]:
        """
        Find an existing image file for a card
        
        Args:
            card_id: Card ID to search for
        
        Returns:
            Path to existing image or None if not found
        """
        extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        
        for ext in extensions:
            path = os.path.join(self.pics_directory, f"{card_id}{ext}")
            if os.path.exists(path):
                return path
        
        return None
    
    def verify_image(self, card_id: int) -> Tuple[bool, Optional[str]]:
        """
        Verify that a card image exists and get information about it
        
        Args:
            card_id: Card ID to verify
        
        Returns:
            Tuple of (exists: bool, info: str)
        """
        image_path = self.find_existing_image(card_id)
        
        if not image_path:
            return False, f"No image found for card ID {card_id}"
        
        # Get file size
        file_size = os.path.getsize(image_path)
        file_size_kb = file_size / 1024
        
        info = f"Image found: {image_path} ({file_size_kb:.2f} KB)"
        
        # Get dimensions if PIL is available
        if PIL_AVAILABLE:
            try:
                with Image.open(image_path) as img:
                    width, height = img.size
                    info += f"\nDimensions: {width}x{height}"
                    
                    if width != self.RECOMMENDED_WIDTH or height != self.RECOMMENDED_HEIGHT:
                        info += f"\nRecommended: {self.RECOMMENDED_WIDTH}x{self.RECOMMENDED_HEIGHT}"
            except Exception as e:
                info += f"\nWarning: Could not read image dimensions: {e}"
        
        return True, info
    
    def delete_image(self, card_id: int) -> bool:
        """
        Delete the image file for a card
        
        Args:
            card_id: Card ID whose image should be deleted
        
        Returns:
            True if deleted, False if not found or error
        """
        image_path = self.find_existing_image(card_id)
        
        if not image_path:
            print(f"No image found for card ID {card_id}")
            return False
        
        try:
            os.remove(image_path)
            print(f"✓ Deleted image: {image_path}")
            return True
        except Exception as e:
            print(f"✗ Error deleting image: {e}")
            return False
    
    def copy_local_image(self, source_path: str, card_id: int, resize: bool = True,
                        overwrite: bool = False) -> Optional[str]:
        """
        Copy a local image file to the pics directory
        
        Args:
            source_path: Path to the source image file
            card_id: Card ID (used for filename)
            resize: Whether to resize the image to recommended dimensions
            overwrite: Whether to overwrite existing image files
        
        Returns:
            Path to saved image file or None if failed
        """
        try:
            # Check if source file exists
            if not os.path.exists(source_path):
                print(f"✗ Source image file not found: {source_path}")
                return None
            
            # Check if image already exists
            existing_path = self.find_existing_image(card_id)
            if existing_path and not overwrite:
                print(f"Image already exists: {existing_path}")
                print(f"Use overwrite=True to replace it")
                return existing_path
            
            print(f"Copying image from: {source_path}")
            
            # Determine file extension from source
            source_ext = os.path.splitext(source_path)[1].lower()
            if not source_ext:
                source_ext = '.jpg'
            
            # Save path (always use .jpg after processing)
            save_path = os.path.join(self.pics_directory, f"{card_id}.jpg")
            
            # Process image if PIL is available and resize is requested
            if PIL_AVAILABLE and resize:
                try:
                    # Open image with PIL
                    with Image.open(source_path) as img:
                        # Get original dimensions
                        orig_width, orig_height = img.size
                        print(f"Original image size: {orig_width}x{orig_height}")
                        
                        # Resize if necessary
                        if orig_width != self.RECOMMENDED_WIDTH or orig_height != self.RECOMMENDED_HEIGHT:
                            print(f"Resizing to recommended size: {self.RECOMMENDED_WIDTH}x{self.RECOMMENDED_HEIGHT}")
                            img = img.resize(
                                (self.RECOMMENDED_WIDTH, self.RECOMMENDED_HEIGHT),
                                Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else Image.LANCZOS
                            )
                        
                        # Convert to RGB if necessary (for PNG with transparency)
                        if img.mode in ('RGBA', 'LA', 'P'):
                            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                            if img.mode == 'P':
                                img = img.convert('RGBA')
                            rgb_img.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                            img = rgb_img
                        
                        # Save as JPEG
                        img.save(save_path, 'JPEG', quality=95)
                        print(f"✓ Image processed and saved: {save_path}")
                        
                except Exception as e:
                    print(f"Warning: Could not process image with PIL: {e}")
                    print(f"Copying original image without processing...")
                    # Copy original file
                    shutil.copy2(source_path, save_path)
                    print(f"✓ Image copied (original): {save_path}")
            else:
                # Copy file without processing
                shutil.copy2(source_path, save_path)
                print(f"✓ Image copied: {save_path}")
            
            return save_path
            
        except Exception as e:
            print(f"✗ Error copying image: {e}")
            return None
    
    def download_with_retry(self, url: str, card_id: int, max_retries: int = 3,
                           resize: bool = True, overwrite: bool = False) -> Optional[str]:
        """
        Download an image with retry logic
        
        Args:
            url: URL of the image
            card_id: Card ID
            max_retries: Maximum number of retry attempts
            resize: Whether to resize image
            overwrite: Whether to overwrite existing files
        
        Returns:
            Path to saved image or None if all attempts failed
        """
        for attempt in range(1, max_retries + 1):
            if attempt > 1:
                print(f"Retry attempt {attempt}/{max_retries}...")
            
            result = self.download_image(url, card_id, resize, overwrite)
            
            if result:
                return result
            
            if attempt < max_retries:
                print(f"Download failed, retrying...")
        
        print(f"✗ All {max_retries} download attempts failed")
        return None


def download_card_image(url: str, card_id: int, pics_dir: str = "../pics", 
                       resize: bool = True) -> bool:
    """
    Convenience function to download a card image
    
    Args:
        url: Image URL
        card_id: Card ID
        pics_dir: Directory to save images
        resize: Whether to resize image
    
    Returns:
        True if successful, False otherwise
    """
    downloader = ImageDownloader(pics_dir)
    result = downloader.download_with_retry(url, card_id, resize=resize)
    return result is not None


if __name__ == "__main__":
    # Test the image downloader
    print("Image Downloader Test")
    print("=" * 60)
    
    # Example usage
    downloader = ImageDownloader("../pics")
    
    # Test URL (placeholder - replace with actual card image URL)
    test_url = "https://via.placeholder.com/177x254.jpg"
    test_card_id = 99999999
    
    print(f"\nTest: Downloading image for card {test_card_id}")
    result = downloader.download_image(test_url, test_card_id, resize=False)
    
    if result:
        print(f"\n✓ Test successful!")
        exists, info = downloader.verify_image(test_card_id)
        print(f"\nVerification:\n{info}")
    else:
        print(f"\n✗ Test failed")

