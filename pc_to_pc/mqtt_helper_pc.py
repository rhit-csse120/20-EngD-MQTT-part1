"""
Library built on top of  paho.mqtt.client  for two devices to communicate
through the Internet, using a MQTTT Broker as the intermediary.

This library is for a PC as one of the two devices.
See   mqtt_helper_pico   for the corresponding library for a Pico.

Authors: David Mutchler and his colleagues
         at Rose-Hulman Institute of Technology.
"""

import paho.mqtt.client

UNIQUE_ID = "DavidMutchler1019"  # Use something that no one else will use
BROKER = "broker.emqx.io"  # Or: "broker.hivemq.com", but must match Pico
TCP_PORT = 1883


class MqttClient(paho.mqtt.client.Client):
    def __init__(self, suffix1="pc", suffix2="device"):
        super().__init__(paho.mqtt.client.CallbackAPIVersion.VERSION2)

        self.suffix1 = suffix1
        self.suffix2 = suffix2
        self.pc_to_device_topic = UNIQUE_ID + "/" + suffix1 + "_to_" + suffix2
        self.device_to_pc_topic = UNIQUE_ID + "/" + suffix2 + "_to_" + suffix1
        self.on_connect = self.on_connect
        self.on_message = self.on_message
        self.broker = BROKER
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
        Called when a connection to the Broker has been established,
        or the code has given up trying to do so (timeout).
        """
        if reason_code == 0:
            print(f"CONNECTED to MQTT broker {self.broker}")
        else:
            print("Failed to connect to broker, return code %d\n", reason_code)

    def on_message(self, mqtt_client, userdata, message_packet):
        """Called when a message arrives.  Display it on Console and in GUI."""
        message = message_packet.payload.decode()
        print("Received message:", message)  # Shows on the Console, for debugging as needed
        self.message_dispatcher.receive_message(message)

    def send_message(self, message):
        """Publish (send to other device) the given string."""
        print("Sending", message)  # Shows on the Console, for debugging as needed
        self.publish(self.pc_to_device_topic, message)
