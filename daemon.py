from loguru import logger
import pyudev
import subprocess
import traceback
import time
import sys

from pathlib import Path

USBCLASS_HUB = 0x09 # https://www.usb.org/defined-class-codes

def usbip_bind(device):
    logger.info(f"Bind device {device}")

    # Check Hub class
    try:
        devClass = int(device.attributes.get("bDeviceClass").decode("ascii"))
        if devClass == USBCLASS_HUB:
            logger.warning("Ignore device: Device is a Hub")
        else:
            subprocess.run(args=["/usr/sbin/usbip", "bind", "-b", device.sys_name], capture_output=True, check=True)

    except Exception as exc:
        logger.error(f"Unable to bind device: {exc}")
        logger.debug(traceback.format_exc())


def load_ignore_list(fpath: Path):
    fpath = Path(fpath)
    logger.info(f"Load ignore list from {fpath}")

    r_set = set()
    with open(fpath, "r") as fhandle:
        for line in fhandle:
            line = line.strip()
            logger.info(f" -> Add dev {line}")
            r_set.add(line)

    return r_set

if __name__ == "__main__":
    logger.info("Hello world!")

    ignore_list = load_ignore_list(sys.argv[1]) if len(sys.argv) >= 2 else set()

    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem="usb", device_type="usb_device")

    logger.info("Bind already existing devices...")
    for dev in context.list_devices(subsystem="usb", DEVTYPE="usb_device"):
        if (dev.driver != "usbip-host"):
            if dev.sys_name in ignore_list:
                logger.warning(f"Ignore {dev}, which is in ignore list")
            else:
                usbip_bind(dev)


    logger.info("Listen for events...")
    for action, device in monitor:
        logger.debug(f"{action}: {device}")

        if (action == "bind") and (device.driver != "usbip-host"):
            if device.sys_name in ignore_list:
                logger.warn(f"{device} is in ignore list!")
            else:
                logger.info(f"Try bind action for {device}")
                usbip_bind(device)

        elif action=="unbind":
            logger.warning(f"Unbind event for {device}")
