# Brian Blaylock
# 29 November 2018

"""
Generate time lapse video from MesoWest cameras for a custom date range.

STITCH TOGETHER TWO CAMERA IMAGES SIDE BY SIDE
This assumes that there is an equal number of images from each camera.

Must run on meso1 in order to generate MPEG-4 videos

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
camera_left = 'wbbs_cam'
camera_right = 'wbbw_cam'

# Camera image file time is in UTC.
# (please, don't make a movie longer than a day or two)
sDATE = datetime(2018, 11, 29, 7)
eDATE = datetime(2018, 11, 29, 19)

# Generate a list of dates so we can grab images from different directories.
DATES = [sDATE] + [sDATE+timedelta(days=i) for i in range((eDATE-sDATE).days)]

# Loop through all archive directory days.
img_list_left = []
for d in DATES:
    # Look in this directory...
    DIR = '/uufs/chpc.utah.edu/common/home/horel-group/archive/%s/%s/' % (d.strftime('%Y%m%d'), camera_left)
    # Get a list of files
    all_files = os.listdir(DIR)
    # Filter out non .jpg files. File name must begin with 2 (not frame)
    jpg_files = list(filter(lambda x: x[-3:]=='jpg', all_files))
    jpg_files = list(filter(lambda x: x[0]=='2', all_files))
    # Filter out images not within daterange
    requested_files = list(filter(lambda x: datetime.strptime(x, '%Y%m%d%H%M%S.jpg') > sDATE and
                                            datetime.strptime(x, '%Y%m%d%H%M%S.jpg') < eDATE, jpg_files))
    # Attach directory path to file name:
    file_paths = [DIR+i for i in requested_files]
    # Append image list
    img_list_left += file_paths

img_list_left.sort()

# Loop through all archive directory days.
img_list_right = []
for d in DATES:
    # Look in this directory...
    DIR = '/uufs/chpc.utah.edu/common/home/horel-group/archive/%s/%s/' % (d.strftime('%Y%m%d'), camera_right)
    # Get a list of files
    all_files = os.listdir(DIR)
    # Filter out not .jpg files
    jpg_files = list(filter(lambda x: x[-3:]=='jpg', all_files))
    jpg_files = list(filter(lambda x: x[0]=='2', all_files))
    # Filter out images not within daterange
    requested_files = list(filter(lambda x: datetime.strptime(x, '%Y%m%d%H%M%S.jpg') > sDATE and
                                            datetime.strptime(x, '%Y%m%d%H%M%S.jpg') < eDATE, jpg_files))
    # Attach directory path to file name:
    file_paths = [DIR+i for i in requested_files]
    # Append image list
    img_list_right += file_paths

img_list_right.sort()

############################## Generate movie #################################

print('len(cam1) == len(cam2)', len(img_list_right)==len(img_list_left))

# The easiest way to generate a movie is from sequentially named files. 
# Use convert to stictch together images side-by-side
for num, img in enumerate(zip(img_list_left, img_list_right)):
    os.system('convert %s %s +append ./frame_%010d.jpg' % (img[0], img[1], num))

mov_video = './STITCH_%s-%s_s%s_e%s.mov' % (camera_left, camera_right, sDATE.strftime('%Y%m%d-%H%M'), eDATE.strftime('%Y%m%d-%H%M'))
mp4_video = mov_video.split('.mov')[0]+'.mp4'

# Convert frames to .mov
os.system('/usr/local/bin/ffmpeg -i frame_%%010d.jpg -qmin 6 -qmax 6 %s' % (mov_video))
os.system('chmod 664 %s' % mov_video)

# Convert .mov to .mp4
os.system('/usr/bin/ffmpeg -i %s -c:v libx264 %s' % (mov_video, mp4_video))
os.system('chmod 664 %s' % mp4_video)

# Remove all the linked images
os.system('rm -f ./*.jpg')