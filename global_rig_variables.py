#################################
# math for framerates and times #
#################################
#How many frames can be captured in one full rotation?
frames_per_second = 30
full_rotation_time = 2.60
frames_per_full_rotation = frames_per_second * full_rotation_time

#How many degrees are there between frames?
degrees_between_frames = 360 / frames_per_full_rotation

#How many seconds are there in one degree?
seconds_per_degree = full_rotation_time / 360

#How many seconds are there in degrees between frames?
seconds_per_degrees_between_frames = degrees_between_frames * seconds_per_degree