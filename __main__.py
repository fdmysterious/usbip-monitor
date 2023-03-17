from loguru import logger
import pyudev

if __name__ == "__main__":
    logger.info("Hello world!")

    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem="usb")

    for action, device in monitor:
        logger.info(f"{action}: {device}")
