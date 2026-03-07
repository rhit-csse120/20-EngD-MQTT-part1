"""
Example showing for tkinter and ttk:
  -- MQTT for communicating with another device through the Internet.
  -- Use the  mqtt_helper  module to communicate with the other device.

This module is the GUI by which they communicate.
See   main.py   for the main function.
See   mqtt_helper_pc.py   for the MQTT code.

Authors: David Mutchler and his colleagues
         at Rose-Hulman Institute of Technology.
"""

from tkinter import ttk


class Gui(ttk.Frame):
    def __init__(self, root, mqtt_client):
        super().__init__(root)
        self.root = root
        self.mqtt_client = mqtt_client

        # Frame that covers the root Toplevel.
        frame = ttk.Frame(root)
        frame.grid()

        # Entry box with data to send to the other computer.
        entry = ttk.Entry(frame)
        entry.grid()

        # Button that sends data in the Entry box to the other computer.
        button = ttk.Button(frame, text="Send Entry box data to the other computer")
        button.grid()
        button["command"] = lambda: self.mqtt_client.send_message(entry.get())

        # Label that shows data sent from the other computer, as it arrives.
        self.label = ttk.Label(frame, text="No data yet")
        self.label.grid()

    def receive_message(self, message):
        """Put the given message onto the label. Called by the MqttClient."""
        self.label["text"] = message
