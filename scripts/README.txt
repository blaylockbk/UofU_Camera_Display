These scripts are copied over from meso1 on 17 November 2016.
The run on the meso1 crontab. It would be nice to rewrite these in python.

10 18 * * * /horel-local/oper/stncameras/acquire_camera_images.csh >& /dev/null
10 * * * * /horel-local/oper/stncameras/acquire_camera_images_ftp.csh >& /horel-local/oper/stncameras/FTP_ACQUIRE.LOG
03,08,13,18,23,28,33,38,43,48,53,58 * * * * /horel-local/oper/stncameras/process_camera_movies.csh >& /horel-local/oper/stncameras/MOVIE_PROCESS.LOG
