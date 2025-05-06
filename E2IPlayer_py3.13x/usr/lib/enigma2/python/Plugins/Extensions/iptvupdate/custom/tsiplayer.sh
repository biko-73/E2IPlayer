#!/bin/sh
rm -r -f $2/tsiplayer/
mkdir $2/tsiplayer
cp $1/iptvupdate/custom/tsiplayer.sh $2/iptvupdate/custom/tsiplayer.sh
cp $1/hosts/hosttsiplayer.py $2/hosts/
cp $1/icons/logos/tsiplayerlogo.png $2/icons/logos/
cp $1/icons/PlayerSelector/tsiplayer*.png $2/icons/PlayerSelector/ 
cp -r -f $1/tsiplayer/* $2/tsiplayer/
status=$?
if [ $status -ne 0 ]; then
	echo ">> !! TSIplayer could not be copied, error[$status]."
else
	echo ">> Duplication Tsiplayer OK"
fi
if [ -x /usr/bin/fullwget ] ; then
	/usr/bin/fullwget --no-check-certificate https://gitlab.com/Rgysoft/iptv-host-e2iplayer/repository/master/archive.tar.gz -q -O /tmp/iptv-host-e2iplayer.tar.gz
else
	wget --no-check-certificate https://gitlab.com/Rgysoft/iptv-host-e2iplayer/repository/master/archive.tar.gz -q -O /tmp/iptv-host-e2iplayer.tar.gz
fi
	if [ -s /tmp/iptv-host-e2iplayer.tar.gz ] ; then
		echo ">> Download TSiplayer tar.gz OK"
		tar -xzf /tmp/iptv-host-e2iplayer.tar.gz -C /tmp 
		status=$?
		if [ $status -ne 0 ]; then
			echo ">> !! Problem with tar cmd in your system!!"
		else
			echo ">> Unpacking Tsiplayer OK"
			cp -r -f /tmp/iptv-host-e2iplayer-master*/IPTVPlayer/icons/PlayerSelector/* $2/icons/PlayerSelector/
			cp -r -f /tmp/iptv-host-e2iplayer-master*/IPTVPlayer/icons/logos/* $2/icons/logos/
			cp -r -f /tmp/iptv-host-e2iplayer-master*/IPTVPlayer/iptvupdate/custom/* $2/iptvupdate/custom/
			cp -r -f /tmp/iptv-host-e2iplayer-master*/IPTVPlayer/hosts/* $2/hosts/
			cp -r -f /tmp/iptv-host-e2iplayer-master*/IPTVPlayer/tsiplayer/* $2/tsiplayer/	
			rm -r -f /tmp/iptv-host-e2iplayer*
		fi		
	else
		echo "Download Tsiplayer tar.gz Failed"
	fi	
echo " >>>>> End Script with Successful. <<<<<"
exit 0
