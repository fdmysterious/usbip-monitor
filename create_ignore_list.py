from loguru  import logger
from pathlib import Path

import pyudev

if __name__ == "__main__":
    logger.info("Create ignore list from all connected USB devices.")
    logger.warning("Please ensure all external devices are disconnected!")

    ctx = pyudev.Context()

    with open("ignore_list", "w") as fhandle:
        for device in ctx.list_devices(subsystem="usb", DEVTYPE="usb_device"):
            if device.driver != "usbip-host":
                logger.info(f"Add {device} to list")
                print(device.sys_name, file=fhandle)

    logger.info("Done!")
