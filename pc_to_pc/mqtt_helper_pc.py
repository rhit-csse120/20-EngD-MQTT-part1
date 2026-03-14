"""
Library built on top of  paho.mqtt.client  for two devices to communicate
through the Internet, using a MQTT Broker as the intermediary.

This library is for a PC as one of the two devices.
See   mqtt_helper_pico   for the corresponding library for a Pico.

See the  main_on_pc.py  file in this project for how to USE
this library on a PC (laptop).  See the  main_on_pico.py  file
in a subsequent project for how to USE its corresponding library
on a Pico.

USAGE: In both cases, the key steps in USING this library
in your project are simply:

  1. In main, create an instance of the MqttClient class below.
     Let's call that instance mqtt_client.

  2. The applications using this library will need mqtt_client
     to call its  send_message  method to send messages
     from one device to the other device.

     For example, on the PC the application will be the GUI.
     It will need  mqtt_client  to send messages to the Pico.
     So, pass the  mqtt_client  object to the GUI
     when it is constructed.

  3. Additionally, the application will need the
     mqtt_client  object to use its  set_dispatcher  method
     to establish the GUI (in the case of the PC) as the
     object to "dispatch" messages.

     In this protocol, the GUI must have a method
     called  receive_message  that is the method that
     the  mqtt_object  invokes on the GUI when the  mqtt_object
     receives a message.  The GUI can then do what it wants
     with the message received by its  receive_message  method.

  4. After the above, main must call the  start  method
     on the  mqtt_client  object to start the  mqtt_client's
     event loop (receiving messages) in its own thread.

Using the  mqtt_helper_pico  library on the Pico is similar.

Authors: David Mutchler and his colleagues
         at Rose-Hulman Institute of Technology.
"""

import paho.mqtt.client

UNIQUE_ID = "DavidMutchler1019"  # Use something that no one else will use
BROKER = "broker.emqx.io"  # Or: "broker.hivemq.com", but must match Pico
TCP_PORT = 1883


class MqttClient(paho.mqtt.client.Client):
    def __init__(self, suffix1="pc", suffix2="device", broker=BROKER):
        """
        suffix1 is the suffix used in the topic to which the pc PUBLISHES.
        suffix2 is the suffix used in the topic to which the pc SUBSCRIBES.
        """
        super().__init__(paho.mqtt.client.CallbackAPIVersion.VERSION2)

        self.suffix1 = suffix1
        self.suffix2 = suffix2
        self.pc_to_device_topic = UNIQUE_ID + "/" + suffix1 + "_to_" + suffix2
        self.device_to_pc_topic = UNIQUE_ID + "/" + suffix2 + "_to_" + suffix1
        self.on_connect = self.on_connect
        self.on_message = self.on_message
        self.broker = broker
        self.message_dispatcher = None  # Set later

        self.print_who_am_i()

    def print_who_am_i(self):
        print(f"I am {self.suffix1}, talking to {self.suffix2}\n")

    def set_dispatcher(self, message_dispatcher):
        self.message_dispatcher = message_dispatcher

    def start(self):
        print("Connecting to the broker...")
        self.connect(BROKER, TCP_PORT)
        self.loop_start()
        self.subscribe(self.device_to_pc_topic)

    def on_connect(self, mqtt_client, userdata, flags, reason_code, properties):
        """
        Called when a connection to the Broker has been established
        or when the code has given up trying to do so (timeout).
        """
        if reason_code == "Success":
            print(f"CONNECTED to MQTT broker {self.broker}")
        else:
            print(f"Failed to connect to broker {self.broker}.\n")
            print(f"The return code was {reason_code}.\n")

    def on_message(self, mqtt_client, userdata, message_packet):
        """
        Called when a message arrives.  Display it on Console.
        Send it to the dispatcher (e.g. the GUI) for processing.
        """
        message = message_packet.payload.decode()

        # Show the message on the Console, for debugging as needed.
        print(f"Received message: {message}")
        self.message_dispatcher.receive_message(message)

    def send_message(self, message: str):
        """Publish (send to other device) the given message."""
        print("Sending", message)  # Shows on the Console, for debugging as needed
        self.publish(self.pc_to_device_topic, message)
