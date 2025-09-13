# PSP Media Metadata Writer

A Python tool that adds metadata to MP4 videos for optimal viewing on PlayStation Portable (PSP) devices. The program supports both movies and TV shows, automatically detects cover images, and creates PSP-compatible thumbnails.

**Features:**
- ✅ **Movie Support** - Adds movie titles to MP4 metadata
- ✅ **TV Show Support** - Adds show names, episode titles, and episode numbers
- ✅ **Smart Episode Detection** - Extracts episode numbers from various filename formats
- ✅ **Cover Image Detection** - Automatically finds and converts cover images
- ✅ **PSP Thumbnail Generation** - Creates .THM files compatible with PSP
- ✅ **Cross-Platform** - Works on macOS, Linux, and Windows

## Features

- **Movie Support**: Adds movie titles to MP4 metadata
- **TV Show Support**: Adds show names, episode titles, and episode numbers
- **Cover Image Detection**: Automatically finds and converts cover images to PSP thumbnails
- **PSP Thumbnail Generation**: Creates `.THM` files compatible with PSP
- **Smart Episode Detection**: Extracts episode numbers from various filename formats
- **Tab Completion**: Directory input with tab completion (like terminal)
- **Cross-Platform**: Works on macOS and Linux

## Prerequisites

### FFmpeg Installation

The program requires FFmpeg to be installed on your system:

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**Linux (CentOS/RHEL):**
```bash
sudo yum install ffmpeg
```

## Installation

1. Clone or download this repository
2. Make the script executable:
   ```bash
   chmod +x psp_metadata_writer.py
   ```

## Usage

Run the script:

```bash
python3 psp_metadata_writer.py
```

Or make it executable and run directly:

```bash
./psp_metadata_writer.py
```

### Interactive Mode

The program will guide you through the process:

1. **Enter Directory**: Specify the folder containing your MP4 files
2. **Content Type**: Choose between Movie (M) or TV Show (T)
3. **TV Show Name**: If processing a TV show, enter the show name
4. **Processing**: The program will automatically process all MP4 files

**Note**: While this version doesn't have tab completion, it provides a reliable, cross-platform solution that works consistently across all operating systems.

### Example Session

```
=== PSP Media Metadata Writer ===
This tool will add metadata to your MP4 videos for optimal PSP viewing.

Enter the directory containing the video files: /path/to/my/videos
Is the content a (M)ovie or a (T)V show? [M/T]: T
Enter the TV show name: Breaking Bad

Processing TV show 'Breaking Bad' in: /path/to/my/videos
Found cover image: cover.jpg
✓ Cover image converted to PSP thumbnail
Found 5 MP4 files

Processing: S01E01 - Pilot.mp4
  Episode: S01E01
✓ Metadata added to S01E01 - Pilot.mp4
✓ PSP thumbnail created for S01E01 - Pilot.mp4

Processing: S01E02 - Cat's in the Bag.mp4
  Episode: S01E02
✓ Metadata added to S01E02 - Cat's in the Bag.mp4
✓ PSP thumbnail created for S01E02 - Cat's in the Bag.mp4

=== Processing Complete ===
Your videos are now ready for PSP viewing!
```

## File Structure

### Input Directory Structure

```
your_video_directory/
├── movie.mp4                    # For movies
├── cover.jpg                    # Optional cover image
├── S01E01 - Episode Name.mp4    # For TV shows
├── S01E02 - Episode Name.mp4
└── ...
```

### Output

The program modifies your MP4 files in place and creates:

- **Updated MP4 files** with embedded metadata
- **`.THM` files** for PSP thumbnails (one per video file)
- **`thumbnail.jpg`** (temporary file, can be deleted)

## Supported Metadata

### Movies
- `title`: Movie title (from filename)
- `album`: "Movies"

### TV Shows
- `title`: Episode title (from filename)
- `album`: TV show name
- `show`: TV show name
- `episode_id`: Episode number (if detected from filename)

## Episode Number Detection

The program automatically detects episode numbers from various filename formats:

- `S01E01 - Episode Name.mp4` → `S01E01`
- `1x01 - Episode Name.mp4` → `S01E01`
- `EP01 - Episode Name.mp4` → `S01E01` (assumes Season 1)
- `01 - Episode Name.mp4` → `S01E01` (assumes Season 1)
- `Episode 1 - Episode Name.mp4` → `E01`
- `Ep 1 - Episode Name.mp4` → `E01`
- `1 - Episode Name.mp4` → `E01`

## Cover Image Support

The program looks for cover images with these names (case-semi-insensitive):
- `cover.jpg`
- `cover.jpeg`
- `cover.png`
- `cover.bmp`
- `cover.gif`

If found, it converts the image to a PSP-compatible thumbnail (160x120 pixels) and creates `.THM` files for each video.

## PSP Thumbnail Format

- **Size**: 160x120 pixels
- **Format**: JPEG
- **Extension**: `.THM`
- **Naming**: Same as video file (e.g., `movie.mp4` → `movie.THM`)

## Error Handling

The program includes comprehensive error handling:

- Validates directory existence and MP4 file presence
- Checks FFmpeg availability
- Handles metadata writing failures gracefully
- Provides clear error messages and success indicators

## Troubleshooting

### FFmpeg Not Found
```
Error: FFmpeg is not installed or not available in PATH.
```
**Solution**: Install FFmpeg using the commands in the Prerequisites section.

### No MP4 Files Found
```
No MP4 files found in '/path/to/directory'.
```
**Solution**: Ensure your directory contains `.mp4` files.

### Permission Errors
```
Error adding metadata to video.mp4: Permission denied
```
**Solution**: Ensure you have write permissions to the video files and directory.

## License

This project is open source. Feel free to modify and distribute as needed.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## Support

If you encounter any issues or have questions, please check the troubleshooting section or create an issue in the repository.
