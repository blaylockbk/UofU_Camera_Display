# Brian Blaylock
# 29 November 2018

"""
Generate time lapse video from MesoWest cameras for a custom date range.

Must run on meteo1 in order to generate MPEG-4 videos

Camera Names:
    Neil Armstrong Academy            - armstrong_cam
    Boniville Salt Flats              - bflat_cam
    Gunnison Island                   - gunnison_cam
    Alta Study Plot                   - kalf_plot_cam
    William Browning Building (west)  - wbbw_cam
    William Browning Building (south) - wbbs_cam

"""

import os
from datetime import datetime, timedelta

# Specify the name of the camera
camera = 'wbbw_cam'

# Camera image file time is in UTC.
# (please, don't make a movie longer than a day or two)
sDATE = datetime(2018, 11, 29, 7)
eDATE = datetime(2018, 11, 29, 19)

# Generate a list of dates so we can grab images from different directories.
DATES = [sDATE] + [sDATE+timedelta(days=i) for i in range((eDATE-sDATE).days)]

# Loop through all archive directory days.
img_list = []
for d in DATES:
    # Look in this directory...
    DIR = '/uufs/chpc.utah.edu/common/home/horel-group/archive/%s/%s/' % (d.strftime('%Y%m%d'), camera)
    # Get a list of files
    all_files = os.listdir(DIR)
    # Filter out not .jpg files
    jpg_files = list(filter(lambda x: x[-3:]=='jpg', all_files))
    # Filter out images not within daterange
    requested_files = list(filter(lambda x: datetime.strptime(x, '%Y%m%d%H%M%S.jpg') > sDATE and
                                            datetime.strptime(x, '%Y%m%d%H%M%S.jpg') < eDATE, jpg_files))
    # Attach directory path to file name:
    file_paths = [DIR+i for i in requested_files]
    # Append image list
    img_list += file_paths

img_list.sort()

############################## Generate movie #################################

# The easiest way to generate a movie is from sequentially named files. 
# We will make a symbolic link for all our images for this task.
for num, img in enumerate(img_list):
    os.system('ln -s %s frame_%010d.jpg' % (img, num))

mov_video = './%s_s%s_e%s.mov' % (camera, sDATE.strftime('%Y%m%d-%H%M'), eDATE.strftime('%Y%m%d-%H%M'))
mp4_video = mov_video.split('.mov')[0]+'.mp4'

# Convert frames to .mov
os.system('/usr/local/bin/ffmpeg -i frame_%%010d.jpg -qmin 6 -qmax 6 %s' % (mov_video))
os.system('chmod 664 %s' % mov_video)

# Convert .mov to .mp4
os.system('/usr/bin/ffmpeg -i %s -c:v libx264 %s' % (mov_video, mp4_video))
os.system('chmod 664 %s' % mp4_video)

# Remove all the linked images
os.system('rm -f ./*.jpg')