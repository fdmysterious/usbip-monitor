from loguru import logger
import pyudev
import subprocess
import traceback
import time

def usbip_bind(device_name):
    logger.info(f"Bind device {device_name}")
    time.sleep(1)
    ret = subprocess.run(args=["/usr/sbin/usbip", "bind", "-b", device_name], capture_output=True, check=True)
    logger.info(ret)

if __name__ == "__main__":
    logger.info("Hello world!")

    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem="usb", device_type="usb_device")

    for action, device in monitor:
        logger.debug(f"{action}: {device}")

        if action == "bind":
            logger.info(f"Bind action for {device.sys_name}")
            try:
                usbip_bind(device.sys_name)
            except Exception as exc:
                logger.error(f"Unable to bind device: {exc}")
                logger.debug(traceback.format_exc())

        elif action=="unbind":
            logger.warning(f"Unbind action for {device.sys_name}")
            # Auto unbound from usbip


