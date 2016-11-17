#!/bin/csh

# Process that is executed to create 2-hour and full day camera movies, executed via cronjob
# Creates a 2 hour movie (hour option) using all frames in the 2 hour window
# Creates a day movie (day option) using frame in first 10 sec of each minute

# Set time information

set yrz  = `date -u +%y`
set monz = `date -u +%m`
set dayz = `date -u +%d`
set hrz  = `date -u +%H`
set min  = `date -u +%M`

set day = `date -u +%Y%m%d`

# Set primary directories

set primaryin = "/uufs/chpc.utah.edu/common/home/horel-group/archive/${day}"
set primaryout = "/horel-local/web/station_cameras"
set scriptdir = "/horel-local/oper/stncameras"

# Set arrays of information for the camera names, increment the $loop number in the loop below when cameras are added/subtracted

set location = (mtnmet_cam armstrong_cam wbbw_cam wbbs_cam)

# Check to make sure we are not spawning extra processes on accident

if (-e ${scriptdir}/moviemake.status) then
	echo "Skipping a Camera Animation Generation Sequence: $yrz$monz$dayz/$hrz$min (UTC)"
	exit
endif

touch ${scriptdir}/moviemake.status

# Begin loop for each camera

@ loop = 1
while ($loop <= 4)

# Set individual directories

	set in = "${primaryin}/${location[$loop]}"
	set out = "${primaryout}/${location[$loop]}"
	#set tmpwebdir = "/uufs/chpc.utah.edu/common/home/u0035056/public_html/${location[$loop]}"
	set archivemoviedir = "/uufs/chpc.utah.edu/common/home/horel-group/stncameras/${location[$loop]}"

# Check to make sure a directory exists for the day, if it does execute a loop to make movies

	if (-d $in) then

		foreach length ( "hour" "day" )

# Change into archive directory and remove any old frame files

			cd $in
			rm -f frame*.jpg
		
# Set counter to 0 and create a list of needed files
		
			set count = 0
			if ( $length == "hour" ) then
				set files = `find *.jpg -type f -mmin -120 -size +1k | sort`
			else 
				set files = `find *.jpg -type f -mtime -1 -size +1k | sort`
			endif
		
# Figure out exactly what files are needed for each movie type, create symbolic links for them
		
			set filesexist = 0
			
			foreach file ( $files )
				if ( $length == "hour" ) then
					set counts = `printf "%04d" $count`
					ln -s $file frame_${counts}.jpg
					@ count = $count + 1
					set filesexist = 1
				else			
					set sec = `echo $file | cut -c13-14 | sed 's/^0*//'`
					if ($sec > 29) then
						if ($sec < 40) then
							set counts = `printf "%04d" $count`
							ln -s $file frame_${counts}.jpg
							@ count = $count + 1
							set filesexist = 1
						endif
					endif
				endif
			end
		
# Execute ffmpeg step to create new movie files to replace old ones

			if ( $filesexist == 1 ) then

				rm -f ${location[$loop]}_${length}_new.mov
				/usr/local/bin/ffmpeg -i frame_%04d.jpg -qmin 6 -qmax 6 ${location[$loop]}_${length}_new.mov
				cp ${location[$loop]}_${length}_new.mov ${out}/${location[$loop]}_${length}.mov
				chmod 664 ${out}/${location[$loop]}_${length}.mov

				rm -f ${location[$loop]}_${length}_new.mp4
				/usr/bin/ffmpeg -i ${location[$loop]}_${length}_new.mov -c:v libx264 ${location[$loop]}_${length}_new.mp4
				cp ${location[$loop]}_${length}_new.mp4 ${out}/${location[$loop]}_${length}.mp4
				chmod 664 ${out}/${location[$loop]}_${length}.mp4
		
# If working with daily movie, copy to archive directory for archiving purposes
		
				if ( $length == "day" ) then
					if ( -e ${out}/${location[$loop]}_${length}.mov ) then
						cp -r  ${out}/${location[$loop]}_${length}.mov ${archivemoviedir}/${location[$loop]}_${day}.mov
					endif
				endif

			endif
			
			rm -f frame*.jpg
		
# Remove symbolic link frames
	

		end

	else
		echo "Directory ${in} does not exist!: $yrz$monz$dayz/$hrz$min (UTC)"
	endif
	
	@ loop += 1
	
end

rm -f ${scriptdir}/moviemake.status

exit
