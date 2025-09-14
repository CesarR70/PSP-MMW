#!/usr/local/bin/python3
"""
PSP Media Metadata Writer
A tool to write metadata to MP4 videos for optimal PSP viewing experience.
Supports both movies and TV shows with thumbnail generation.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from typing import Optional, List, Dict
import argparse


class PSPMetadataWriter:
    """Main class for handling PSP video metadata writing."""
    
    def __init__(self):
        self.ffmpeg_available = self._check_ffmpeg()
        if not self.ffmpeg_available:
            print("Error: FFmpeg is not installed or not available in PATH.")
            print("Please install FFmpeg:")
            print("  macOS: brew install ffmpeg")
            print("  Linux: sudo apt-get install ffmpeg")
            sys.exit(1)
    
    def _check_ffmpeg(self) -> bool:
        """Check if FFmpeg is available in the system."""
        try:
            subprocess.run(['ffmpeg', '-version'], 
                         capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def get_directory(self) -> Path:
        """Get video directory from user input."""
        while True:
            directory = input("Enter the directory containing the video files: ").strip()
            if not directory:
                print("Please enter a valid directory path.")
                continue
            
            # Expand tilde to home directory
            directory = os.path.expanduser(directory)
            path = Path(directory)
            
            if not path.exists():
                print(f"Directory '{directory}' does not exist.")
                continue
            
            if not path.is_dir():
                print(f"'{directory}' is not a directory.")
                continue
            
            # Check if directory contains MP4 files
            mp4_files = list(path.glob("*.mp4"))
            if not mp4_files:
                print(f"No MP4 files found in '{directory}'.")
                continue
            
            print(f"✓ Found {len(mp4_files)} MP4 files in '{directory}'")
            return path
    
    def get_content_type(self) -> str:
        """Get content type (movie or TV show) from user input."""
        while True:
            content_type = input("Is the content a (M)ovie or a (T)V show? [M/T]: ").strip().upper()
            if content_type in ['M', 'MOVIE']:
                return 'movie'
            elif content_type in ['T', 'TV', 'TV SHOW', 'SHOW']:
                return 'tv_show'
            else:
                print("Invalid input. Please enter 'M' for Movie or 'T' for TV show.")
    
    def get_tv_show_name(self) -> str:
        """Get TV show name from user input."""
        while True:
            show_name = input("Enter the TV show name: ").strip()
            if show_name:
                return show_name
            print("Please enter a valid TV show name.")
    
    def find_cover_image(self, directory: Path) -> Optional[Path]:
        """Find cover image in the directory."""
        # Common cover image extensions and names
        cover_patterns = [
            "cover.jpg", "cover.jpeg", "cover.png", "cover.bmp", "cover.gif",
            "Cover.jpg", "Cover.jpeg", "Cover.png", "Cover.bmp", "Cover.gif",
            "COVER.jpg", "COVER.jpeg", "COVER.png", "COVER.bmp", "COVER.gif"
        ]
        
        for pattern in cover_patterns:
            cover_path = directory / pattern
            if cover_path.exists():
                return cover_path
        
        return None
    
    def convert_to_psp_thumbnail(self, image_path: Path, output_path: Path) -> bool:
        """Convert image to PSP-compatible thumbnail (160x120 JPEG)."""
        try:
            cmd = [
                'ffmpeg', '-i', str(image_path),
                '-vf', 'scale=160:120',
                '-q:v', '2',  # High quality
                '-y',  # Overwrite output file
                str(output_path)
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error converting image to thumbnail: {e}")
            return False
    
    def extract_episode_number(self, filename: str) -> Optional[str]:
        """Extract episode number from filename."""
        import re
        # Look for patterns like S01E01, 1x01, Episode 1, EP01, etc.
        # Order matters - more specific patterns first
        
        # Season and episode patterns
        s_e_match = re.search(r'S(\d+)E(\d+)', filename, re.IGNORECASE)
        if s_e_match:
            season_num = int(s_e_match.group(1))
            episode_num = int(s_e_match.group(2))
            return f"S{season_num:02d}E{episode_num:02d}"
        
        # Season x Episode patterns
        s_x_e_match = re.search(r'(\d+)x(\d+)', filename, re.IGNORECASE)
        if s_x_e_match:
            season_num = int(s_x_e_match.group(1))
            episode_num = int(s_x_e_match.group(2))
            return f"S{season_num:02d}E{episode_num:02d}"
        
        # EP patterns (assumes Season 1)
        ep_match = re.search(r'EP(\d+)', filename, re.IGNORECASE)
        if ep_match:
            episode_num = int(ep_match.group(1))
            return f"S01E{episode_num:02d}"
        
        # Number-dash patterns at start (assumes Season 1)
        dash_match = re.search(r'^(\d+)-', filename)
        if dash_match:
            episode_num = int(dash_match.group(1))
            return f"S01E{episode_num:02d}"
        
        # Episode patterns
        episode_match = re.search(r'Episode\s*(\d+)', filename, re.IGNORECASE)
        if episode_match:
            episode_num = int(episode_match.group(1))
            return f"E{episode_num:02d}"
        
        # Ep patterns
        ep_short_match = re.search(r'Ep\s*(\d+)', filename, re.IGNORECASE)
        if ep_short_match:
            episode_num = int(ep_short_match.group(1))
            return f"E{episode_num:02d}"
        
        # Just a number (fallback)
        number_match = re.search(r'(\d+)', filename)
        if number_match:
            episode_num = int(number_match.group(1))
            return f"E{episode_num:02d}"
        
        return None
    
    def add_metadata_to_video(self, video_path: Path, metadata: Dict[str, str]) -> bool:
        """Add metadata to MP4 video file."""
        try:
            # Create temporary output file
            temp_path = video_path.with_suffix('.temp.mp4')
            
            # Build FFmpeg command
            cmd = ['ffmpeg', '-i', str(video_path), '-c', 'copy']
            
            # Add metadata
            for key, value in metadata.items():
                cmd.extend(['-metadata', f'{key}={value}'])
            
            cmd.extend(['-y', str(temp_path)])  # -y to overwrite
            
            # Run FFmpeg
            subprocess.run(cmd, check=True, capture_output=True)
            
            # Replace original with updated file
            shutil.move(str(temp_path), str(video_path))
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"Error adding metadata to {video_path.name}: {e}")
            if temp_path.exists():
                temp_path.unlink()  # Clean up temp file
            return False
    
    def create_psp_thumbnail_file(self, video_path: Path, thumbnail_path: Path) -> bool:
        """Create PSP .THM thumbnail file for the video."""
        try:
            thm_path = video_path.with_suffix('.THM')
            shutil.copy2(str(thumbnail_path), str(thm_path))
            return True
        except Exception as e:
            print(f"Error creating THM file for {video_path.name}: {e}")
            return False
    
    def process_movies(self, directory: Path) -> None:
        """Process movie files in the directory."""
        print(f"\nProcessing movies in: {directory}")
        
        # Check for cover image
        cover_image = self.find_cover_image(directory)
        thumbnail_path = None
        
        if cover_image:
            print(f"✓ Found cover image: {cover_image.name}")
            thumbnail_path = directory / "thumbnail.jpg"
            if self.convert_to_psp_thumbnail(cover_image, thumbnail_path):
                print("✓ Cover image converted to PSP thumbnail")
            else:
                print("✗ Failed to convert cover image")
                thumbnail_path = None
        else:
            print("No cover image found")
        
        # Process each MP4 file
        mp4_files = list(directory.glob("*.mp4"))
        print(f"Found {len(mp4_files)} MP4 files")
        
        for video_file in mp4_files:
            print(f"\nProcessing: {video_file.name}")
            
            # Create metadata
            metadata = {
                'title': video_file.stem,  # Use filename without extension as title
                'album': 'Movies'
            }
            
            # Add metadata to video
            if self.add_metadata_to_video(video_file, metadata):
                print(f"✓ Metadata added to {video_file.name}")
                
                # Create PSP thumbnail file if we have one
                if thumbnail_path and thumbnail_path.exists():
                    if self.create_psp_thumbnail_file(video_file, thumbnail_path):
                        print(f"✓ PSP thumbnail created for {video_file.name}")
                    else:
                        print(f"✗ Failed to create PSP thumbnail for {video_file.name}")
            else:
                print(f"✗ Failed to add metadata to {video_file.name}")
        
        # Clean up temporary files for PSP compatibility
        self.cleanup_for_psp(directory)
    
    def process_tv_show(self, directory: Path, show_name: str) -> None:
        """Process TV show files in the directory."""
        print(f"\nProcessing TV show '{show_name}' in: {directory}")
        
        # Check for cover image
        cover_image = self.find_cover_image(directory)
        thumbnail_path = None
        
        if cover_image:
            print(f"✓ Found cover image: {cover_image.name}")
            thumbnail_path = directory / "thumbnail.jpg"
            if self.convert_to_psp_thumbnail(cover_image, thumbnail_path):
                print("✓ Cover image converted to PSP thumbnail")
            else:
                print("✗ Failed to convert cover image")
                thumbnail_path = None
        else:
            print("No cover image found")
        
        # Process each MP4 file
        mp4_files = list(directory.glob("*.mp4"))
        print(f"Found {len(mp4_files)} MP4 files")
        
        for video_file in mp4_files:
            print(f"\nProcessing: {video_file.name}")
            
            # Extract episode number and title
            episode_number = self.extract_episode_number(video_file.stem)
            episode_title = video_file.stem
            
            # Create metadata
            metadata = {
                'title': episode_title,
                'album': show_name,
                'show': show_name
            }
            
            if episode_number:
                metadata['episode_id'] = episode_number
                print(f"  Episode: {episode_number}")
            
            # Add metadata to video
            if self.add_metadata_to_video(video_file, metadata):
                print(f"✓ Metadata added to {video_file.name}")
                
                # Create PSP thumbnail file if we have one
                if thumbnail_path and thumbnail_path.exists():
                    if self.create_psp_thumbnail_file(video_file, thumbnail_path):
                        print(f"✓ PSP thumbnail created for {video_file.name}")
                    else:
                        print(f"✗ Failed to create PSP thumbnail for {video_file.name}")
            else:
                print(f"✗ Failed to add metadata to {video_file.name}")
        
        # Clean up temporary files for PSP compatibility
        self.cleanup_for_psp(directory)
    
    def cleanup_for_psp(self, directory: Path) -> None:
        """Clean up temporary files to ensure PSP XMB compatibility."""
        print(f"\nCleaning up temporary files for PSP compatibility...")
        
        # Files to remove (temporary files that PSP XMB doesn't like)
        files_to_remove = [
            "thumbnail.jpg",  # Temporary thumbnail file
            "cover.jpg", "cover.jpeg", "cover.png", "cover.bmp", "cover.gif",
            "Cover.jpg", "Cover.jpeg", "Cover.png", "Cover.bmp", "Cover.gif",
            "COVER.jpg", "COVER.jpeg", "COVER.png", "COVER.bmp", "COVER.gif"
        ]
        
        removed_count = 0
        for filename in files_to_remove:
            file_path = directory / filename
            if file_path.exists():
                try:
                    file_path.unlink()
                    print(f"✓ Removed: {filename}")
                    removed_count += 1
                except Exception as e:
                    print(f"✗ Failed to remove {filename}: {e}")
        
        if removed_count > 0:
            print(f"✓ Cleaned up {removed_count} temporary file(s)")
            print("✓ Directory is now PSP XMB compatible")
        else:
            print("✓ No temporary files to clean up")
    
    def run(self) -> None:
        """Main program execution."""
        print("=== PSP Media Metadata Writer ===")
        print("This tool will add metadata to your MP4 videos for optimal PSP viewing.\n")
        
        try:
            # Get directory
            directory = self.get_directory()
            
            # Get content type
            content_type = self.get_content_type()
            
            # Process based on content type
            if content_type == 'movie':
                self.process_movies(directory)
            else:  # tv_show
                show_name = self.get_tv_show_name()
                self.process_tv_show(directory, show_name)
            
            print("\n=== Processing Complete ===")
            print("Your videos are now ready for PSP viewing!")
            
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            sys.exit(1)


def main():
    """Entry point for the program."""
    parser = argparse.ArgumentParser(
        description="Add metadata to MP4 videos for PSP viewing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python psp_metadata_writer.py
  python psp_metadata_writer.py --help
        """
    )
    
    args = parser.parse_args()
    
    # Create and run the metadata writer
    writer = PSPMetadataWriter()
    writer.run()


if __name__ == "__main__":
    main()

