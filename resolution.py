import time
import subprocess
import wmi
from win32api import EnumDisplaySettings, ChangeDisplaySettings
from win32con import DM_PELSWIDTH, DM_PELSHEIGHT, DM_DISPLAYFREQUENCY

# Function to check if HDMI is connected (more than one active monitor)
def is_hdmi_connected():
    try:
        c = wmi.WMI(namespace="root\\WMI")
        monitors = c.WmiMonitorConnectionParams()
        active_monitors = len([m for m in monitors if m.Active])
        return active_monitors > 1
    except Exception:
        return False

# Function to check if in extend mode (multiple monitors with different resolutions or positions)
def is_extend_mode():
    try:
        c = wmi.WMI()
        displays = c.Win32_VideoController()
        if len(displays) <= 1:
            return False
        # Check if resolutions differ or positions suggest extend
        monitors = c.Win32_DesktopMonitor()
        if len(monitors) > 1:
            res1 = (displays[0].CurrentHorizontalResolution, displays[0].CurrentVerticalResolution)
            res2 = (displays[1].CurrentHorizontalResolution, displays[1].CurrentVerticalResolution)
            return res1 != res2 or len(monitors) > 1
        return False
    except Exception:
        return False

# Function to set resolution using Windows API (requires pywin32)
def set_resolution(width, height, refresh_rate=60):
    try:
        devmode = EnumDisplaySettings(None, -1)  # Get current settings
        devmode.PelsWidth = width
        devmode.PelsHeight = height
        devmode.DisplayFrequency = refresh_rate
        devmode.Fields = DM_PELSWIDTH | DM_PELSHEIGHT | DM_DISPLAYFREQUENCY
        result = ChangeDisplaySettings(devmode, 0)
        return result == 0  # 0 means success
    except Exception as e:
        print(f"Resolution change failed: {e}")
        return False

# Function to set duplicate mode using DisplaySwitch.exe (non-admin if pre-allowed)
def set_duplicate_mode():
    try:
        subprocess.run("C:\\Windows\\System32\\DisplaySwitch.exe /clone", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(1)  # Wait for mode switch
    except Exception:
        pass

# Function to get current resolution
def get_current_resolution():
    try:
        c = wmi.WMI()
        display = c.Win32_VideoController()[0]
        return display.CurrentHorizontalResolution, display.CurrentVerticalResolution
    except Exception:
        return None, None

# Main logic
initial_hdmi_connect = False

while True:
    hdmi_connected = is_hdmi_connected()
    is_extend = is_extend_mode()
    current_width, current_height = get_current_resolution()

    if hdmi_connected:
        if not initial_hdmi_connect:
            if current_width != 1920 or current_height != 1080:
                set_duplicate_mode()
                set_resolution(1920, 1080, 60)
            initial_hdmi_connect = True
        elif is_extend:
            if current_width != 1920 or current_height != 1200:
                set_resolution(1920, 1200, 60)
        else:
            if current_width != 1920 or current_height != 1080:
                set_resolution(1920, 1080, 60)
    else:
        if current_width != 1920 or current_height != 1200:
            set_resolution(1920, 1200, 60)
        initial_hdmi_connect = False

    time.sleep(5)  # Check every 5 seconds
