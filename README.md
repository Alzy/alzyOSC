# alzyOSC

An Ableton Live remote script based on LiveOSC2 which mimics a two-deck DJ setup on a multi-touch screen laptop. An Ableton Live project template and an Open Stage Control template are included to complete the setup. Else, you can create your own OSC controller using touchOSC or something similar though your milage may vary.



## About

This script seperates your Ableton Session View into two by using two individually controlled red boxes controlled by one OSC server. Bindings for these redboxes are set to '/live/session/a/*' and '/live/session/b/*' respectively. 


## Installation

### Remote Script

Copy all the .py files in the root directory into your Ableton remote script folder (this will vary depending on your OS). These will be automatically compiled when Ableton Live is started. Next, in Ableton Live open Preferences and set TWO alzyOSC controllers. The first controller will startup an OSC server while the second one will act as a slave to the first.

Finally, open the included Ableton Live project in the "ableton_project_template" folder.


### OSC Controller

Download and install Open Stage Control. When you open the program you will be greeted with configuration window. Set the following:

    send: 127.0.0.1:9001
    load: ../openstagecontrol_template/alzyOSC.json
    custom-module: ../openstagecontrol_template/alzyOSC-custom-module.json
    port: 9000

Press start, then click on tab2 then the two buttons within it.This will recieve all session information from Ableton. If all is done properly, you should be able to move along The ableton session view with two redboxes, each moving individually.



TADA! You now have a two deck, 4 channel DJ set in ableton without the need for an external midi controller.
