# Downloader for Windows environment.
# Requires powershell.exe

import json
import subprocess
import os
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askopenfilenames
from tkinter.filedialog import askdirectory


# Download MP3 from Youtube
def yt_dl(ytdlp_path, ffmpeg_path, dest_path, map_name, filename, yt_id):
    yt_dlp_cmd = [
        'powershell.exe', 
        '&', f'"{ytdlp_path}"', # Call yt-dlp.exe from absolute path
        '-x', # Extract audio only
        '-q', # Quiet mode
        '--audio-format', 'mp3', # Output format to be MP3
        '--audio-quality' ,'0', # Best audio quality
        '--ffmpeg-location', f'"{ffmpeg_path}"', 
        '-P', f'"{dest_path}/{map_name}"', # Specify the bgm map
        '-o', f'"{filename}.noMeta.%(ext)s"', # Output file name
        f'{yt_id}' # YT ID of the video
    ]

    subprocess.run(yt_dlp_cmd, check=True, stderr=subprocess.STDOUT)
    return f'{filename}.noMeta.mp3'

# Apply metadata to downloaded MP3
def apply_metadata(ffmpeg_path, file_path, map_name, mp3_file, metadata):
    title = metadata.get('title', '')
    artist = metadata.get('artist', '')
    albumArtist = metadata.get('albumArtist', '')
    year = metadata.get('year', '')
    
    output_file = mp3_file.replace('.noMeta.mp3', '.mp3')
    ffmpeg_cmd = [
        'powershell.exe', 
        '&', f'"{ffmpeg_path}"', 
        '-i', f'"{file_path}/{map_name}/{mp3_file}"',
        '-metadata', f'title="{title}"',
        '-metadata', f'artist="{artist}"',
        '-metadata', f'album_artist="{albumArtist}"',
        '-metadata', f'year="{year}"',
        '-metadata', f'description="{desc}"',
        '-codec', 'copy',
        '-loglevel quiet', # Do not print any output from ffmpeg
        '-n', # Do not overwrite file if file already exist
        f'"{file_path}/{map_name}/{output_file}"'
    ]

    del_noMetaMP3_cmd = [
        'powershell.exe',
        'rm', f'"{file_path}/{map_name}/{mp3_file}"'
    ]

    subprocess.run(ffmpeg_cmd, check=True, stderr=subprocess.STDOUT)
    subprocess.run(del_noMetaMP3_cmd, check=True, stderr=subprocess.STDOUT)
    return output_file

# Process JSON file
def process_json(ytdlp_path, ffmpeg_path, json_files, dest_path):
    for json_file in json_files:

        # Read JSON file
        with open(json_file, 'r') as file:
            data = json.load(file)

        # Check if file contains single entry only
        if isinstance(data, dict):
            data = [data]

        # Process each entry in the JSON
        for entry in data:
            # Extract data from JSON
            yt_id = entry.get('youtube')
            map_name = entry.get('mark')
            metadata = entry.get('metadata', {})
            filename = metadata.get('title')
            
            # Check if the file already exists
            if os.path.isfile(f'{dest_path}/{map_name}/{filename}.mp3'):
                print(f'"{map_name}/{filename}" ALREADY EXISTS!!!')
                continue

            else:
                # Download MP3 from Youtube using data from JSON
                print(f'Downloading {map_name}/{filename}.mp3')
                mp3_file = yt_dl(ytdlp_path, ffmpeg_path, dest_path, map_name, filename, yt_id)

                # Apply metadata to MP3 files
                print(f'Applying metadata to {map_name}/{filename}.mp3')
                apply_metadata(ffmpeg_path, dest_path, map_name, mp3_file, metadata)
        



if __name__ == '__main__':
    json_path = output_path = ytdlp_path = ffmpeg_path = None
    # output_path = None
    while not ytdlp_path:
        print('Please choose the path to yt-dlp.exe:')
        ytdlp_path = askopenfilename()
    while not ffmpeg_path:
        print('Please choose the path to ffmpeg.exe:')
        ffmpeg_path = askopenfilename()
    while not json_path:
        print('Please specify the JSON file(s):')
        json_path = askopenfilenames()

    while not output_path:
        print("Please specify the output directory:")
        output_path = askdirectory()
    
    process_json(ytdlp_path, ffmpeg_path, json_path, output_path)
    
