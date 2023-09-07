#!/bin/sh
##############################################################################################################
##
## Script Purpose:
##		Download and install IPK/DEB (Py2/Py3)
##
## Command: wget https://raw.githubusercontent.com/biko-73/E2IPlayer/main/installer.sh -O - | /bin/sh
##
##############################################################################################################


##############################################################################################################
# Plugin	... Enter Manually
##############################################################################################################

MY_IPK_PY2="enigma2-plugin-extensions-e2iplayer_2023.08.18.01_all_Py2.ipk"
MY_IPK_PY3="enigma2-plugin-extensions-e2iplayer_2023.08.18.01_all_Py3.ipk"

PACKAGE_DIR='E2IPlayer/main'

##############################################################################################################
# Auto ... Do not change
##############################################################################################################
MY_MAIN_URL="https://raw.githubusercontent.com/biko-73/"

PYTHON_VERSION=$(python -c 'import sys; print(sys.version_info[0])')

# Decide : which package ?
if which dpkg > /dev/null 2>&1; then
	#if [ "$PYTHON_VERSION" -eq "2" ]; then
	#	MY_FILE=$MY_DEB_PY2
	#else
	#	MY_FILE=$MY_DEB_PY3
	#fi;
	echo "No DEB Package available at the momnet."
	echo ""
	echo " >>> Installation failed <<< "
	exit 0
else
	if [ "$PYTHON_VERSION" -eq "2" ]; then
		MY_FILE=$MY_IPK_PY2
	else
		MY_FILE=$MY_IPK_PY3
	fi;
fi

# If no suitable package available
if [ -z "$MY_FILE" ]; then
	echo ''
	echo '************************************************************'
	echo '**          NO Suitable Version Found ON Server           **'
	echo '************************************************************'
	echo ''
	exit 0
fi

MY_URL=$MY_MAIN_URL$PACKAGE_DIR'/'$MY_FILE
MY_TMP_FILE="/tmp/"$MY_FILE

echo ''
echo '************************************************************'
echo '**                         STARTED                        **'
echo '************************************************************'
echo "**                 Uploaded by: Biko_73                   **"
echo "**  https://www.tunisia-sat.com/forums/threads/4120814/   **"
echo "************************************************************"
echo ''

# Remove previous file (if any)
rm -f $MY_TMP_FILE > /dev/null 2>&1

# Download package file
MY_SEP='============================================================='
echo $MY_SEP
echo 'Downloading '$MY_FILE' ...'
echo $MY_SEP
echo ''
wget -T 2 $MY_URL -P "/tmp/"

# Check download
if [ -f $MY_TMP_FILE ]; then
	# Install
	echo ''
	echo $MY_SEP
	echo 'Installation started'
	echo $MY_SEP
	echo ''
	if which dpkg > /dev/null 2>&1; then
		apt-get install --reinstall $MY_TMP_FILE -y
	else
		# Remove old copies
		opkg --force-remove enigma2-plugin-extensions-e2iplayer > /dev/null 2>&1
		opkg --force-remove enigma2-plugin-extensions-e2iplayer-py2 > /dev/null 2>&1
		opkg --force-remove enigma2-plugin-extensions-e2iplayer-py3 > /dev/null 2>&1
		opkg --force-remove enigma2-plugin-extensions-e2iplayer-deps > /dev/null 2>&1
		opkg -force-depends enigma2-plugin-extensions-e2iplayer > /dev/null 2>&1
		opkg -force-depends enigma2-plugin-extensions-e2iplayer-py2 > /dev/null 2>&1
		opkg -force-depends enigma2-plugin-extensions-e2iplayer-py3 > /dev/null 2>&1
		opkg -force-depends enigma2-plugin-extensions-e2iplayer-deps > /dev/null 2>&1

		# Remove new copies
		opkg install --force-reinstall $MY_TMP_FILE
	fi
	MY_RESULT=$?

	# Remove Installation file
	rm -f $MY_TMP_FILE > /dev/null 2>&1

	# Result
	echo ''
	echo ''
	if [ $MY_RESULT -eq 0 ]; then
		echo "   >>>>   SUCCESSFULLY INSTALLED   <<<<"
		echo ''
		echo "   >>>>         RESTARING         <<<<"
		if which systemctl > /dev/null 2>&1; then
			sleep 2; systemctl restart enigma2
		else
			init 4; sleep 4; init 3;
		fi
	else
		echo "   >>>>   INSTALLATION FAILED !   <<<<"
	fi;
	echo ''
	echo '**************************************************'
	echo '**                   FINISHED                   **'
	echo '**************************************************'
	echo ''
	exit 0
else
	echo ''
	echo "Download failed !"
	exit 1
fi

# ------------------------------------------------------------------------------------------------------------
