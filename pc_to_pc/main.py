"""
Example showing for tkinter and ttk:
  -- MQTT for communicating with another device through the Internet.
  -- Use the  mqtt_helper  module to communicate with the other device.

This example shows communication between two PC's.  To run it:
  -- Run it once with    main(1)   as the call to main
          (last line of this module).
  -- Run it again with   main(2)   as the call to main.

Two GUIs will appear (one on top of the other).  Do what they suggest.
The Console output will appear on TWO Run windows in PyCharm.

Authors: David Mutchler and his colleagues
         at Rose-Hulman Institute of Technology.
"""

import tkinter
import mqtt_helper_pc
import GUI


def main(which_pc):
    # MqttClient object, properly initialized.
    if which_pc == 1:
        mqtt_client = mqtt_helper_pc.MqttClient("pc1", "pc2")
    else:
        mqtt_client = mqtt_helper_pc.MqttClient("pc2", "pc1")

    # Root (main) window.
    root = tkinter.Tk()
    root.title("MQTT example")

    # Make the GUI.  # It is the dispatcher for the MqttClient
    # (i.e., it acts upon messages from the MqttClient).
    gui = GUI.Gui(root, mqtt_client)  # The ttk.Frame that covers the root
    mqtt_client.set_dispatcher(gui)

    # Start the event loop for the MqttClient, in its own thread.
    mqtt_client.start()

    # Stay in the event loop for the rest of the program's run.
    root.mainloop()


# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main(2)  # 1 or 2 to indicate which pc
