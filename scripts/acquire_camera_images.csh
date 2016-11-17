#!/bin/csh

# This process collects images from cameras located across the valley and stores them in the archive space

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

if (-e imagegrab.status) then
	mail -s "Camera Image Capture Process: Skipping Start Sequence" atmos-mesowest@lists.utah.edu <<EOF
	Skipping a Camera Image Capture Start Sequence: $yrz$monz$dayz/$hrz$min (UTC)
EOF
	echo "Skipping a Camera Image Capture Start Sequence: $yrz$monz$dayz/$hrz$min (UTC)"
	exit
endif

touch imagegrab.status

# Set arrays of information for both the camera name and the URL to grab the images from, increment the $loop number in the loops below when cameras are added/subtracted (3 loops below)

set camname = (mtnmet_cam armstrong_cam wbbw_cam wbbs_cam)
set camurl = ("http://155.97.226.135/axis-cgi/jpg/image.cgi" "http://205.124.147.71/axis-cgi/jpg/image.cgi" "http://155.98.55.211/axis-cgi/jpg/image.cgi" "http://155.98.55.212/axis-cgi/jpg/image.cgi")

# First loop through the camera directories making sure they exist

set day = `date -u +%Y%m%d`
@ loop = 1
while ($loop <= 4)
	set dayout = "${primaryarchivedir}/${day}"
	if (-d $dayout) then
		set skip = 1
	else
		mkdir $dayout
		chmod 775 $dayout
	endif
	set out = "${primaryarchivedir}/${day}/${camname[$loop]}"
	if (-d $out) then
		set skip = 1
	else
		mkdir $out
		chmod 775 $out
	endif
	@ loop += 1
end

# Now start up conditional loop that will continuously run until condition is met (i.e. when we reach a new day it should kick out)

set ctr = 0

while ( $ctr == 0 )

	@ loop = 1
	while ($loop <= 4)

		set day = `date -u +%Y%m%d`
		set file = `date -u +%Y%m%d%H%M%S`.jpg

		set out = "${primaryarchivedir}/${day}/${camname[$loop]}"

		if (-d $out) then
			wget -nv -T 5 "${camurl[$loop]}" -O $out/$file
			chmod 664 $out/$file
			convert $out/$file -resize 500x500 ${primarywebdir}/${camname[$loop]}/${camname[$loop]}_current.jpg
		else
			set ctr = 1
			if(-e ${primarywebdir}/${camname[$loop]}/${camname[$loop]}_day.mp4) then	
				cp ${primarywebdir}/${camname[$loop]}/${camname[$loop]}_day.mp4 ${primarywebdir}/${camname[$loop]}/${camname[$loop]}_yesterday.mp4
			endif
			# rm -f imagegrab.status
			# exit
		endif

		@ loop += 1
	end

	sleep 10
	
end

@ loop = 1
while ($loop <= 4)
	if(-e ${primarywebdir}/${camname[$loop]}/${camname[$loop]}_day.mp4) then	
		cp ${primarywebdir}/${camname[$loop]}/${camname[$loop]}_day.mp4 ${primarywebdir}/${camname[$loop]}/${camname[$loop]}_yesterday.mp4
	endif
	@ loop += 1
end

rm -f imagegrab.status

exit
