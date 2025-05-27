import os, subprocess
ffmpeg_snippet = """
ffmpeg -y -hide_banner -loglevel error -i "{}" -filter_complex \
"[0:v]split=3[v1][v2][v3]; \
 [v1]scale=w=1920:h=1080[v1out]; \
 [v2]scale=w=1280:h=720[v2out]; \
 [v3]scale=w=854:h=480[v3out]" \
-map "[v1out]" -c:v:0 libx264 -b:v:0 5000k -preset veryfast -g 48 -sc_threshold 0 -keyint_min 48 -x264-params "scenecut=0" -map a:0? -c:a:0 aac -b:a:0 128k \
-map "[v2out]" -c:v:1 libx264 -b:v:1 2800k -preset veryfast -g 48 -sc_threshold 0 -keyint_min 48 -x264-params "scenecut=0" -map a:0? -c:a:1 aac -b:a:1 128k \
-map "[v3out]" -c:v:2 libx264 -b:v:2 1400k -preset veryfast -g 48 -sc_threshold 0 -keyint_min 48 -x264-params "scenecut=0" -map a:0? -c:a:2 aac -b:a:2 128k \
-f hls -hls_time 6 -hls_playlist_type vod \
-hls_segment_filename "{}/segment_%03d.ts" \
-master_pl_name master.m3u8 \
-var_stream_map "v:0,a:0 v:1,a:1 v:2,a:2" {}/prog.m3u8
"""

ROOT_MEDIA_PATH = "/Users/aniketsarkar/Desktop/movies"  # Change this to your media path

def convert_video(input_file:str, output_dir:str):
    """
    Convert a video file to HLS format with multiple resolutions.
    Args:
        input_file (str): Path to the input video file.
        output_dir (str): Directory where the output files will be saved.
    """
    # Get the movie name without extension
    movie_name = os.path.splitext(os.path.basename(input_file))[0]
    # Create a subfolder for the movie inside the output_dir
    movie_output_dir = os.path.join(output_dir, movie_name)
    if not os.path.exists(movie_output_dir):
        os.makedirs(movie_output_dir)

    output_file = os.path.join(movie_output_dir, "prog.m3u8")
    # Format ffmpeg command for any input file type
    command = ffmpeg_snippet.format(input_file, movie_output_dir, movie_output_dir)
    
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Conversion completed: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during conversion: {e}")

def main():
    input_file = os.path.join(ROOT_MEDIA_PATH, "tt4425200.mkv")  # Replace with your input video file
    output_dir = "output_hls"  # Replace with your desired output directory
    convert_video(input_file, output_dir)

if __name__ == "__main__":
    main()
# This script converts any video file to HLS format with three different resolutions.
# It uses ffmpeg to create the HLS segments and playlists.
# Ensure ffmpeg is installed and available in your PATH.
# The script creates an output directory if it does not exist and handles errors during the conversion process.
# The output will include a master playlist and three variant streams for different resolutions.
# The resolutions are 1920x1080, 1280x720, and 854x480.
# The audio is encoded in AAC format with a bitrate of 128k for each variant.
# The script can be run directly, and it will convert the specified input video file.