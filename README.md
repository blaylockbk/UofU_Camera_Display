# ![MesoWest 20th Anniversary](MesoWest_20th_black.png) Camera Display

A web interface for viewing weather cameras deployed by the 
[MesoWest group](http://meso1.chpc.utah.edu/mesowest_overview/) at 
the University of Utah.

### View the live product at [http://home.chpc.utah.edu/~u0553130/Camera_Display/](http://home.chpc.utah.edu/~u0553130/Camera_Display/)

## Homepage
On the home page you can view all the cameras in real time.
This code uses Bootstrap columns, so the number layout of
the camera windows responses to your window size. On large monitor, the cameras
are shown in three columns. On a mobile device or small windows, the cameras 
are shown in a single column.  
![Homepage ScreenShot](homepage.PNG)

## Timelapse Videos
You can view time lapse videos by clicking the camera you want on the homepage.
Each camera timelaspe page has it's own page.  
![Timelapse ScreenShot](timelapse.PNG)

## Temperature Ticker
The black bar at the top of each page displays the current temperature at each
of the camera sites. These data are retrieved from the MesoWest API found in 
the `mesowest_api.js` and `CurrentTemp.js` scripts.
* WBB - William Browning Building
* MTMET - Moutain Meteorology Lab
* NAA - Neil Armstrong Academy
* FPS - Flight Park South
* FPS - Flight Park North
* GNI - Gunnison Island (PELICam)
* EYSC - Eyring Science Center at BYU (camera looking at Timpanogos)
