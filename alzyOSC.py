# --------------------------------------------------- #
# This code was written by Alzy, dawg.
#.....................................
#---------------------------------------------------- #
from __future__ import with_statement
import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import *
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from ConfigurableButtonElement import ConfigurableButtonElement
from _Framework.SessionComponent import SessionComponent
from _Framework.TransportComponent import TransportComponent

from controlMaps import *

from alzyOSCSessionComponent import alzyOSCSessionComponent
from LO2MixerComponent import LO2MixerComponent
from LO2TransportComponent import LO2TransportComponent

from LO2Mixin import LO2Mixin
from LO2OSC import LO2OSC


class alzyOSC(ControlSurface):
    """script for MPD26: alzyOSC"""
    _active_instances = []


    def set_instance_properties(self):
        index = 0

        for instance in alzyOSC._active_instances:
            instance._instanceIndex = index
            index += 1 


    def set_instance_session_properties(self):
        track_offset = 0

        for instance in alzyOSC._active_instances:
            instance._session.set_offsets(track_offset, 0)
            track_offset += instance._session.width()


    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        with self.component_guard():
            # We keep track of which instance this is in case there
            # are multiple instances of this remote script loaded.
            # if this is the first index, it will handle all
            # functionality except for the second red box.
            # If this is the second instance or more, it will only 
            # handle it's red box and nothing else.
            self._instanceIndex = -1

            self._control_is_with_automap = False
            self._suggested_input_port = 'Loop Midi Port'
            self._suggested_output_port = 'Loop Midi Port'

            self.osc_handler = None
            self._mixer = None
            self._session = None
            self._transport = None

            if self not in alzyOSC._active_instances:
                alzyOSC._active_instances.append(self)

            self.set_instance_properties()
            self.log_message('Set: alzyOSC instance #'+str(self._instanceIndex))

            # if this is the first or only open instance of this
            # remote script, this one will handle all osc
            # functionality.
            if self._instanceIndex == 0:
                self.initOSC()
                self._session.name = "OSC_Session_Control"
                self._session.side = "a"
                # since the osc session will function as the osc controller
                # for side b as well, we will pass the _active_instances array
                # by reference so it may access side b's session component.
                self._session._active_instances = alzyOSC._active_instances
            else:
                self._session = SessionComponent(4, 4)
                self._session.name = 'Session_Control'
                self._session.side = "b"

            self.set_highlighting_session_component(self._session)
            self.set_instance_session_properties()


    def disconnect(self):
        """clean things up on disconnect"""
        alzyOSC._active_instances.remove(self)
        if self.osc_handler is not None:
            self.osc_handler.shutdown()

        ControlSurface.disconnect(self)
        return None


    def initOSC(self):
        LO2OSC.set_log(self.log_message)
        LO2OSC.set_message(self.show_message)
        self.osc_handler = LO2OSC()
        
        LO2Mixin.set_osc_handler(self.osc_handler)
        LO2Mixin.set_log(self.log_message)
        
        self._mixer = LO2MixerComponent(1)
        self._session = alzyOSCSessionComponent(4, 4)
        self._session.set_mixer(self._mixer)
        self._session._assigned_width = 4
        self._session._assigned_height = 4
        self._transport = LO2TransportComponent()
        
        self.parse()

        if not self.osc_handler.error():
            self.show_message('Ready')
            self.osc_handler.send('/live/startup', 1)


    def parse(self):
        self.osc_handler.process()
        self.schedule_message(1, self.parse)
