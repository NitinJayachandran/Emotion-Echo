import subprocess

def convert_webm_to_wav(input_file, output_file):
    try:
        # Replace '/full/path/to/ffmpeg' with the actual path on your system
        ffmpeg_path = '/opt/homebrew/bin/ffmpeg'
        
        # Run FFmpeg command with the full path
        subprocess.run([ffmpeg_path, '-i', input_file, output_file], check=True)
        print(f'Conversion completed: {output_file}')
    except subprocess.CalledProcessError as e:
        print(f'Error during conversion: {e}')

# Replace 'input.webm' and 'output.wav' with your file names
input_webm_file = 'audio.webm'
output_wav_file = 'output.wav'