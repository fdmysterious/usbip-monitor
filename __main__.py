from loguru import logger
import pyudev

if __name__ == "__main__":
    logger.info("Hello world!")

    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem="usb", device_type="usb_device")

    for action, device in monitor:
        logger.debug(f"{action}: {device}")

        if action == "bind":
            logger.info(f"Bind action for {device.sys_name}")

        elif action=="unbind":
            logger.warning(f"Unbind action for {device.sys_name}")


