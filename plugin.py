# -*- coding: utf-8 -*-
###################################################
# E2iPlayer Main Plugin File - Patched for TSiplayer/TSIBaseHosts
###################################################

from Plugins.Extensions.IPTVPlayer.components.ihost import IHost, CHostBase, CBaseHostClass
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG, printExc
import os

# Try to import TSiplayer's TSCBaseHostClass if available
try:
    from Plugins.Extensions.IPTVPlayer.libs.tstools import TSCBaseHostClass
    TSI_SUPPORT = True
except Exception:
    TSCBaseHostClass = None
    TSI_SUPPORT = False

HOSTS_DIR = os.path.join(os.path.dirname(__file__), "hosts")

def getHostClassFromFile(host_path):
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("hostmodule", host_path)
        hostModule = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(hostModule)
    except Exception:
        printExc()
        return None, None

    for attr in dir(hostModule):
        obj = getattr(hostModule, attr)
        if isinstance(obj, type):
            # Check for TSiplayer host
            if TSI_SUPPORT and TSCBaseHostClass and issubclass(obj, TSCBaseHostClass) and obj != TSCBaseHostClass:
                return obj, "TSI"
            # Check for E2iPlayer host
            if issubclass(obj, CBaseHostClass) and obj != CBaseHostClass:
                return obj, "E2I"
    return None, None

def getHostsList():
    hosts = []
    if not os.path.isdir(HOSTS_DIR):
        printDBG("Hosts directory not found: %s" % HOSTS_DIR)
        return hosts
    for fname in os.listdir(HOSTS_DIR):
        if fname.startswith("host_") and fname.endswith(".py"):
            hosts.append(fname)
    return hosts

def main(session, **kwargs):
    # Load hosts (optional, for debugging)
    hosts = getHostsList()
    host_objs = []
    for host_file in hosts:
        host_path = os.path.join(HOSTS_DIR, host_file)
        host_class, host_type = getHostClassFromFile(host_path)
        if host_class:
            try:
                host_instance = host_class()
                host_obj = CHostBase(host_instance, True, [])
                host_objs.append((host_obj, host_file, host_type))
            except Exception:
                printExc("Error loading host: %s" % host_file)
    printDBG("Loaded hosts:")
    for obj, fname, htype in host_objs:
        printDBG(" - %s [%s]" % (fname, htype))

    # Open the main E2iPlayer GUI (correct import for Lululla fork)
    try:
        from Plugins.Extensions.IPTVPlayer.iptvplayerwidget import IPTVPlayerWidget
        session.open(IPTVPlayerWidget)
    except Exception as e1:
        try:
            from Plugins.Extensions.IPTVPlayer.iptvplayerwidget import IPTVPlayerMainScreen
            session.open(IPTVPlayerMainScreen)
        except Exception as e2:
            from Screens.MessageBox import MessageBox
            import traceback
            msg = "Could not find main E2iPlayer GUI class.\n"
            msg += "Error 1:\n" + str(e1) + "\n\n"
            msg += "Error 2:\n" + str(e2) + "\n\n"
            msg += "Traceback:\n" + traceback.format_exc()
            session.open(MessageBox, msg, MessageBox.TYPE_ERROR)

def Plugins(**kwargs):
    from Plugins.Plugin import PluginDescriptor
    return [
        PluginDescriptor(
            name="E2iPlayer",
            description="Watch IPTV streams",
            where=PluginDescriptor.WHERE_PLUGINMENU,
            icon="plugin.png",
            fnc=main
        )
    ]

# If run directly for testing (not needed on Enigma2)
if __name__ == "__main__":
    class DummySession(object):
        def open(self, what, *a, **k):
            print("Would open:", what, a, k)
    main(DummySession())