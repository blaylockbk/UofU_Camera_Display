#!/bin/csh

# This process collects hourly images from web cameras we have access to via Loggernet on our cloud server (images collected through Loggernet)

# Set time information

set yrz  = `date -u +%y`
set monz = `date -u +%m`
set dayz = `date -u +%d`
set hrz  = `date -u +%H`
set min  = `date -u +%M`

# Set directory spaces

set scriptdir = "/horel-local/oper/stncameras"
set primarywebdir = "/horel-local/web/station_cameras"
set primaryarchivedir = "/uufs/chpc.utah.edu/common/home/horel-group/archive"

cd ${scriptdir}

if (-e imagegrabftp.status) then
	echo "Skipping a Camera Image FTP Acquire Process: $yrz$monz$dayz/$hrz$min (UTC)"
	exit
endif

touch imagegrabftp.status

# Set arrays of information for both the camera name and the URL to grab the images from, increment the $loop number in the loops below when cameras are added/subtracted (3 loops below)

set day = `date -u +%Y%m%d`
set dayarchivedir = "${primaryarchivedir}/${day}"

set file = `date -u +%Y%m%d%H`0000.jpg

set camname = (kalf_plot_cam)
set camimagedir = ("UKALF")
set camimagelocaldir = ("${dayarchivedir}/${camname[1]}")
set camimagename = ("0055_Kalfplot.JPG")

# First loop through the camera directories making sure they exist

set day = `date -u +%Y%m%d`
@ loop = 1
while ($loop <= 1)
	set out = "${dayarchivedir}/${camname[$loop]}"
	if (-d $out) then
		set skip = 1
	else
		mkdir $out
		chmod 775 $out
	endif
	@ loop += 1
end

# Now FTP into our cloud server to retrieve the image(s_

set myftpuser = 'camimage'
set myftppw = 'g3^We3C@m5'

#ftp -n -v -d -i 69.25.178.11<<EOF
ftp -n -v -d -i 52.26.128.4<<EOF
user ${myftpuser} ${myftppw}
prompt
binary
lcd ${camimagelocaldir[1]}
cd ${camimagedir[1]}
get ${camimagename[1]} ${file}
delete ${camimagename[1]}
EOF
endif

# Now paste those images as current images for display purposes on the web!

@ loop = 1
while ($loop <= 1)
	if(-e "${camimagelocaldir[$loop]}/${file}") then
		cp ${camimagelocaldir[$loop]}/${file} ${primarywebdir}/${camname[$loop]}/${camname[$loop]}_current.jpg
	endif
	@ loop += 1
end

rm -f imagegrabftp.status

exit
