import subprocess
import os.path
import global_rig_variables

image_directory = os.path.dirname(os.path.abspath(__file__)) + "/input/images/"

#deletes all images in the images directory.
for file in os.listdir(image_directory):
	if file.endswith(".png"):
		os.remove(image_directory + file)

frame_time = 0.000
degree_count = 0.000

for i in range(1, int(global_rig_variables.frames_per_full_rotation) + 1):
	file_name = str(degree_count).replace(".","_")
	subprocess.call(['ffmpeg', '-loglevel', 'panic', '-i', 'input/video/scan.h264', '-ss', 
        	         '00:00:0'+str(frame_time), '-vframes', '1', 'input/images/'+str(file_name)+'.png'])
	frame_time += global_rig_variables.seconds_per_degrees_between_frames
	degree_count += global_rig_variables.degrees_between_frames
