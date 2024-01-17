# Lab-Monitoring-System

Optical systems often have numerous components whose proper functioning is essential to the health of the system as a whole. Without a convenient way to check the status of these components, troubleshooting any problems with the system can be extremely inefficient, which could put expensive components at risk. This repository includes the code that makes up a low-cost, quick-to-implement solution to this problem, which we've called the "Lab Monitoring System".

Our iteration of the Lab Monitoring System can be best represented by the following system diagram:

![image](https://github.com/mmcmaster13/Lab-Monitoring-System/assets/41704102/1c49dc68-0f07-4f87-9968-162d879ac9c8)

Our system consists of four Raspberry Pis: one central Pi, called the "Collector", and three Pis at each of our main optical tables (generally called the "measurers"). Each Pi is acting as a Mosquitto broker, with the Collector Pi subscribed to the "results" topic corresponding to each measurer and each measurer subscribed to its own "inquiries" topic. Then, the general operating procedure of the system is as follows:

1. At regular intervals, the Collector Pi asks each measurer in turn for their measurements by posting a message to the corresponding "inquiries" topic.
2. The measurer Pi that was asked by the Collector Pi for data grabs the data from various devices, formats it correctly, and posts it to its "results" topic.
3. Once each measurer has sent its results to the Collector Pi, it formats the data appropriately and posts a request to [IFTTT](ifttt.com), a webservice that allows you to automate various tasks. In our case, we use Webhooks to write the data to a Google Sheets spreadsheet.
4. The Collector Pi also checks each of the data points it receives to make sure that none of them are above their thresholds. If a data point is above its threshold for too long (approximately 20 minutes), the Collector Pi will send a message to our Discord server via [discord.py](https://discordpy.readthedocs.io/en/stable/), notifying us that a component needs attention.
5. The Collector Pi takes a rest, as continuous monitoring is superfluous, before repeating the process.

# How to use this repo

