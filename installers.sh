#!/bin/bash
# ###########################################
# SCRIPT : DOWNLOAD AND INSTALL E2IPLAYER_TSiplayer
# ###########################################
#
#### scripte CREATED by dreamsat panel fouad
#
# ###########################################
versions="18.08.2023"
# Define variables
TMPDIR='/tmp'
PLUGINPATH='/usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer'
SETTINGS='/etc/enigma2/settings'
URL='https://raw.githubusercontent.com'

PYTHON_VERSION=$(python -c "import platform; print(platform.python_version())")

# Function to install packages
install() {
    if [ -f /etc/opkg/opkg.conf ]; then
        STATUS='/var/lib/opkg/status'
        OSTYPE='Opensource'
        OPKG='opkg update'
        OPKGINSTALL='opkg install'
    elif [ -f /etc/apt/apt.conf ]; then
        STATUS='/var/lib/dpkg/status'
        OSTYPE='DreamOS'
        OPKG='apt-get update'
        OPKGINSTALL='apt-get install'
    fi

    if ! grep -qs "Package: $1" $STATUS; then
        $OPKG >/dev/null 2>&1
        echo "   >>>>   Need to install $1   <<<<"
        echo
        if [ $OSTYPE = "Opensource" ]; then
            $OPKGINSTALL "$1"
            sleep 1
            clear
        elif [ $OSTYPE = "DreamOS" ]; then
            $OPKGINSTALL "$1" -y
            sleep 1
            clear
        fi
    fi
}

# Determine platform
case $(uname -m) in
    armv7l*) PLATFORM="armv7" ;;
    mips*) PLATFORM="mipsel" ;;
    aarch64*) PLATFORM="ARCH64" ;;
    sh4*) PLATFORM="sh4" ;;
esac

echo "Detected Python version: $PYTHON_VERSION"

# Define plugins based on Python version
case $PYTHON_VERSION in
    3.11.0|3.11.1|3.11.2|3.11.3|3.11.4|3.11.5|3.11.6)
        PLUGIN='enigma2-plugin-extensions-e2iplayer-py3.tar.gz';;
    *)
        PLUGIN='enigma2-plugin-extensions-e2iplayer-py2.tar.gz';;
esac

# Remove unnecessary files
rm -rf $PLUGINPATH
rm -rf /etc/enigma2/iptvplaye*.json
rm -rf /etc/tsiplayer_xtream.conf
rm -rf /iptvplayer_rootfs
rm -rf /usr/lib/enigma2/python/Components/Input.py
rm -rf /usr/bin/lsdir



# Install required packages based on Python version
if [[ $PYTHON_VERSION == *2.* ]]; then
    for pkg in enigma2-plugin-systemplugins-serviceapp ffmpeg gstplayer duktape wget; do
        install $pkg
    done
elif [[ $PYTHON_VERSION == *3.* ]]; then
    for pkg in enigma2-plugin-systemplugins-serviceapp ffmpeg gstplayer duktape wget python3-sqlite3; do
        install $pkg
    done
else
    echo "Unsupported Python version: $PYTHON_VERSION"
    exit 1
fi

# Download and install IPTVPlayer
echo "Downloading and installing IPTVPlayer-$PYTHON_VERSION plugin, please wait..."
echo
wget --show-progress $URL/biko-73/E2IPlayer/$PLUGIN -qP $TMPDIR
tar -xzf $TMPDIR/$PLUGIN -C /

# Configure settings
if [ -d $PLUGINPATH ]; then
    echo ":Your Device IS $(uname -m) processor ..."
    echo "Add Setting To ${SETTINGS} ..."
    sleep 3
    init 4
    sleep 1
    sed -i '/iptvplayer/d' /etc/enigma2/settings
    sed -e s/config.plugins.iptvplayer.*//g -i ${SETTINGS}
    sleep 1
    {
        echo "config.plugins.iptvplayer.AktualizacjaWmenu=false"
        echo "config.plugins.iptvplayer.SciezkaCache=/etc/IPTVCache/"
        echo "config.plugins.iptvplayer.alternative${PLATFORM^^}MoviePlayer=extgstplayer"
        echo "config.plugins.iptvplayer.alternative${PLATFORM^^}MoviePlayer0=extgstplayer"
        echo "config.plugins.iptvplayer.buforowanie_m3u8=false"
        echo "config.plugins.iptvplayer.default${PLATFORM^^}MoviePlayer=exteplayer"
        echo "config.plugins.iptvplayer.default${PLATFORM^^}MoviePlayer0=exteplayer"
        echo "config.plugins.iptvplayer.remember_last_position=true"
        echo "config.plugins.iptvplayer.extplayer_skin=line"
        echo "config.plugins.iptvplayer.extplayer_infobanner_clockformat=24"       
        echo "config.plugins.iptvplayer.plarform=${PLATFORM}"
        echo "config.plugins.iptvplayer.preferredupdateserver="
        echo "config.plugins.iptvplayer.dukpath=/usr/bin/duk"
        echo "config.plugins.iptvplayer.wgetpath=wget"
    } >>${SETTINGS}
fi

# Clean up and restart
rm -rf $TMPDIR/$PLUGIN
sync
echo ""
echo "***********************************************************************"
echo "**                                                                    *"
echo "**                       TSIPlayer  : $VERSION                      *"
echo "**                       Uploaded by: Biko_73                        *"
echo "**  Support    : https://www.tunisia-sat.com/forums/threads/3951696/  *"
echo "**                                                                    *"
echo "***********************************************************************"
echo ""
if [ $OSTYPE = "DreamOS" ]; then
    sleep 2
    systemctl restart enigma2
else
    init 3
fi
exit 0
