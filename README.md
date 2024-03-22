# Lab-Monitoring-System

Optical systems often have numerous components whose proper functioning is essential to the health of the system as a whole. Without a convenient way to check the status of these components, troubleshooting any problems with the system can be extremely inefficient, which could put expensive components at risk. This repository includes the code that makes up a low-cost, quick-to-implement solution to this problem, which we've called the "Lab Monitoring System".

Our iteration of the Lab Monitoring System can be best represented by the following system diagram:

![image](https://github.com/mmcmaster13/Lab-Monitoring-System/assets/41704102/1c49dc68-0f07-4f87-9968-162d879ac9c8)

Our system consists of four Raspberry Pis: one central Pi, called the "Collector", and three Pis at each of our main optical tables (generally called the "measurers"). Each Pi is acting as a [Mosquitto](https://mosquitto.org/) broker, with the Collector Pi subscribed to the "results" topic corresponding to each measurer and each measurer subscribed to its own "inquiries" topic. Then, the general operating procedure of the system is as follows:

1. At regular intervals, the Collector Pi asks each measurer in turn for their measurements by posting a message to the corresponding "inquiries" topic.
2. The measurer Pi that was asked by the Collector Pi for data grabs the data from various devices, formats it correctly, and posts it to its "results" topic.
3. Once each measurer has sent its results to the Collector Pi, it formats the data appropriately and posts a request to [IFTTT](ifttt.com), a webservice that allows you to automate various tasks. In our case, we use Webhooks to write the data to a Google Sheets spreadsheet.
4. The Collector Pi also checks each of the data points it receives to make sure that none of them are above their thresholds. If a data point is above its threshold for too long (approximately 20 minutes), the Collector Pi will send a message to our Discord server via [discord.py](https://discordpy.readthedocs.io/en/stable/), notifying us that a component needs attention.
5. The Collector Pi takes a rest, as continuous monitoring is superfluous, before repeating the process.

# How to use this repo

Each Raspberry Pi has its own folder in the repository. Inside, there is the Pi's main script, and various other .py files that contain the functions and classes the main scripts employ. The folders for logger2, logger3, and logger4 also have some scripts we used to determine the locked/unlocked thresholds for the various lasers we need to monitor. Since each lab has different needs, this repo serves mainly as an example of a Lab Monitoring System implementation. The files can be used for guidance on the networking using Mosquitto or for ideas about interfacing various pieces of lab equipment with Python.

# Understanding the essentials

## Setting up the Mosquitto brokers

The most essential component of the Lab Monitoring System is Mosquitto. To configure each Pi as a Mosquitto broker, first install the requirements for Mosquitto itself:

`sudo apt-get install mosquitto mosquitto-clients -y`

Then, install the Python library that we use:

`pip install paho-mqtt`

Now, we need to modify the Mosquitto configuration so the Pis can communicate with each other. Add the following lines to `/etc/mosquitto/conf.d/custom.conf`:

- `listener 1883`
- `allow_anonymous true`

The first line tells Mosquitto to listen on port 1883 (this is the default, but is often included for redundancy) and the second line tells Mosquitto to allow connections from any clients. Each Pi will serve as both a client and a broker (receiver that distributes posts to clients). To start the broker, run the following on each Pi:

`sudo mosquitto -c /etc/mosquitto/conf.d/custom.conf`

Now, we can start writing Python scripts using `paho-mqtt` to send information back and forth between the Pis.

## Working with IFTTT

IFTTT can be configured in a number of ways, but our iteration of the Lab Monitoring System uses IFTTT to get a Webhook from the Collector Pi, then publish the data it receives to a Google Sheets file. 

## Posting messages to Discord with Python



## Interfacing a Pi with an USB-equipped oscilloscope

Many of our monitoring strategies involve collecting waveform data from oscilloscopes over USB. Thankfully, most scopes have extensive documentation for computer control and communication over USB, which makes the setup relatively easy in most cases. (Our scopes of choice are in the Rigol 2000-series.) However, interfacing scopes with a Raspberry Pi requires some extra steps upon setup. To manage this communication with a Python script, first do the following:

- `pip install pyusb`
- `pip install pyvisa`
- `pip install pyvisa-py`

It's important to note that [PyVISA](https://pyvisa.readthedocs.io/en/latest/) technically requires a NI-VISA backend, which is not available for the Raspberry Pi. This is why, in the scripts that require the use of PyVISA, we need to add the "@py" argument to ResourceManager: `resources = visa.ResourceManager("@py")`. [Tektronix](https://download.tek.com/document/1KW-61463-0__Raspberry_Pi_3_Save_Lab_Space_%20Cost_Application_Note_090718.pdf) explains that "the ‘@py’ argument allows PyVISA to bypass the default National Instruments backend", and instead the PyVISA-py backend is used, which is available to the Pi, assuming it's installed.

Then, to finish setting up the Pi-scope communication, we need to do two more things. First, add a group called "usbusers" to the 99-com.rules file. Open using a text editor:

`nano  /etc/udev/rules.d/99-com.rules`

Add the group:

`SUBSYSTEM=="usb", MODE="0666", GROUP="usbusers"`

Then restart the Pi. Upon restart, create the group called "usbuers":

`sudo groupadd usbusers`

And lastly, add yourself to the group by inserting the following into the file:

`sudo usermod -a -G usbusers USERNAME`

and restart the Pi again. These steps were inspired by [this StackOverflow question](https://stackoverflow.com/questions/52256123/unable-to-get-full-visa-address-that-includes-the-serial-number). After all of these steps are completed, your Pi should be able to communicate with the scope. The "standard" PyVISA workflow used in our scripts is outlined briefly in the above article from Tektronix and in more detail [here](https://pyvisa.readthedocs.io/en/latest/introduction/communication.html/).
