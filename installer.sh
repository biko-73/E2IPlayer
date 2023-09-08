#!/bin/sh
##############################################################################################################
##
## Download and install IPK/DEB (Py2/Py3)
##
## Command: wget https://raw.githubusercontent.com/biko-73/E2IPlayer/main/installer.sh -O - | /bin/sh
##
##############################################################################################################


##############################################################################################################
# PACKAGE DETAILS
##############################################################################################################

INTRO=(
	"ETIPLAYER"
	 ""
	 "Uploaded by: Biko_73"
	 "Support: https://www.tunisia-sat.com/forums/threads/3951696/"
)

MY_IPK_PY2="e2iplayer_py2_2023.08.18.01_all.ipk"
MY_IPK_PY3="e2iplayer_py3_2023.08.18.01_all.ipk"

MY_DEB_PY2="e2iplayer_py2_2023.08.18.01_all.deb"
MY_DEB_PY3="e2iplayer_py3_2023.08.18.01_all.deb"

PACKAGE_URL="https://raw.githubusercontent.com/biko-73/E2IPlayer/main"


##############################################################################################################
# DO NOT CHANGE THE FOLLOWING CODE
##############################################################################################################

# ------------------------------------------------
# Functions
# ------------------------------------------------
SEP1="#############################################################################"
SEP1="@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
SEP2="---------------------------------"
function showSep() { echo $SEP1; echo $SEP1; }
function showTxt() { TXT="$@"; printf "%*s$TXT\n" $(( (${#SEP1} - ${#TXT}) / 2)); }
function showTitle() { echo $SEP2; echo $1; echo $SEP2; }
function showHead() { TXT="$@"; printf "@@ %*s$TXT\n" $(( (${#SEP1} - ${#TXT}) / 2 - 2)); }
function showIntro() { echo ""; showSep; showHead; arr=("$@"); for i in "${arr[@]}"; do showHead "$i"; done; showHead; showSep; echo "";}
function Finish() {
	echo ""
	showSep
	showHead ""
	showHead "FINISHED"
	showHead ""
	showSep
	rm -f $MY_TMP_FILE > /dev/null 2>&1			# Remove installation file
	exit $1
}

# ------------------------------------------------
# Introduction
# ------------------------------------------------
showIntro "${INTRO[@]}"

# ------------------------------------------------
# URL
# ------------------------------------------------

# File to download
PYTHON_VERSION=$(python -c "import sys; print(sys.version_info[0])")	# PYTHON_VERSION = 2 or 3
if which dpkg > /dev/null 2>&1; then		# Or : if [ -f /etc/apt/apt.conf ] ; then
	if [ "$PYTHON_VERSION" -eq "2" ]; then MY_FILE=$MY_DEB_PY2; else MY_FILE=$MY_DEB_PY3; fi;	# DEB
	ADD_CMD="dpkg -i --force-overwrite"
	REM_CMD1="dpkg --purge --force-all"
	REM_CMD2=$REM_CMD1						# Or : "dpkg --remove --force-depends"
else
	if [ "$PYTHON_VERSION" -eq "2" ]; then MY_FILE=$MY_IPK_PY2; else MY_FILE=$MY_IPK_PY3; fi;	# IPK
	ADD_CMD="opkg install --force-overwrite"
	REM_CMD1="opkg remove --force-remove"
	REM_CMD2="opkg remove --force-depends"
fi

# If no suitable package available
if [ -z "$MY_FILE" ]; then
	echo ""
	showTxt ">>>>>>>> NO Suitable Version Found ON Server <<<<<<<<"
	echo ""
	Finish 1
fi

# Download params
MY_URL=$PACKAGE_URL"/"$MY_FILE			# Package URL
MY_TMP_FILE="/tmp/"$MY_FILE				# File to save as

# ------------------------------------------------
# Download package file
showTitle "Downloading "$MY_FILE" ..."
echo ""
rm -f $MY_TMP_FILE > /dev/null 2>&1			# Remove old download
wget -T 2 $MY_URL -P "/tmp/"				# Download package file
echo ""

# Check downloaded file
if [ -f $MY_TMP_FILE ]; then
	showTxt "******** Downloaded successfully ********"
	echo ""
else
	showTxt ">>>>>>>> DOWNLOAD FAILED ! <<<<<<<<"
	Finish 1
fi

# ------------------------------------------------
# Remove old copies
OLD_LST=(
	"enigma2-plugin-extensions-e2iplayer"
	"enigma2-plugin-extensions-e2iplayer-py2"
	"enigma2-plugin-extensions-e2iplayer-py3"
	"enigma2-plugin-extensions-e2iplayer-deps"
)
for i in "${OLD_LST[@]}"; do
	eval "$REM_CMD1 $i" > /dev/null 2>&1
	if [ $? -ne 0 ]; then
		eval "$REM_CMD2 $i" > /dev/null 2>&1
		if [ $? -ne 0 ]; then
			showTxt ">>>>>>>> Error <<<<<<<<"
			echo ""
			echo "Cannot remove exisiting package : $i"
			echo ""
			Finish 1
		fi
	fi
done

# ------------------------------------------------
# Check download
# Install
showTitle "Installation started"
eval "$ADD_CMD $MY_TMP_FILE"
MY_RESULT=$?

# ------------------------------------------------
# Result
echo ""
if [ $MY_RESULT -eq 0 ]; then
	showTxt "******** SUCCESSFULLY INSTALLED ********"
	Finish 0
else
	showTxt "******** INSTALLATION FAILED ********"
	Finish 1
fi;

# ------------------------------------------------------------------------------------------------------------
