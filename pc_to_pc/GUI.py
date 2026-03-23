"""
Example showing for tkinter and ttk:
  -- MQTT for communicating with another device through the Internet.
  -- Use the  mqtt_helper  module to communicate with the other device.

This module is the GUI by which they communicate.
See   main.py   for the main function, as well as main1.py and main2.py,
which call  main  in main.py with arguments 1 and 2, respectively.

See   mqtt_helper_pc.py   for the MQTT code.

Authors: David Mutchler and his colleagues
         at Rose-Hulman Institute of Technology.
"""

from tkinter import ttk


class Gui:
    """The GUI by which PC 1 and PC 2 communicate in this example."""

    def __init__(self, root, mqtt_client):
        # Required instance variables:
        self.root = root
        self.mqtt_client = mqtt_client

        # Frame that covers the root Toplevel.
        frame = ttk.Frame(root, padding=10)
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
        """
        This is the specially-named method that the MqttClient will call
        when the MqttClient receives a message from the Broker.
        In this case, the method puts the given message onto the label.
        """
        self.label["text"] = message
