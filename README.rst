===================================================================
Simple daemon to automatically bind USB devices on an USB/IP server
===================================================================

:Authors: - Florian Dupeyron <florian.dupeyron@mugcat.fr>
:Date: March 2023

This is a simple dumb daemon that binds usb devices to a running USB/IP server.

Requirements
============

- `ubsipd`
- `pyudev`
- `loguru`

Usage
=====

- First, use the `create_ignore_list.py` script to create an `ignore_list` file. This file lists
  devices to ignore, and this should correspond to the static list of important static devices of your
  server. For instance: root hubs, usb/ethernet adapters on a raspberry pi, a mouse, etc.

- Then, you can launch the `daemon.py`:

  .. code:: bash

     python3 daemon.py ignore_list
