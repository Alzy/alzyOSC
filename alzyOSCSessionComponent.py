# This is a modified version of LiveOSC's session component

from _Framework.SessionComponent import SessionComponent
from _Framework.SceneComponent import SceneComponent

from LO2SceneComponent import LO2SceneComponent
from LO2Mixin import LO2Mixin, wrap_init

class alzyOSCSessionComponent(SessionComponent, LO2Mixin):

    scene_component_type = LO2SceneComponent
    
    @wrap_init
    def __init__(self, *args, **kwargs):
        self._scene_count = -1
        self._scenes_count = 0
        super(alzyOSCSessionComponent, self).__init__(*args, **kwargs)
        
        self._reassign_scenes()
        
        # Side A 
        self.add_callback('/live/session/a/offsets', self._session_a_offsets)

        self.add_callback('/live/session/a/bank/down', self._session_a_bank_down)
        self.add_callback('/live/session/a/bank/up', self._session_a_bank_up)

        self.add_callback('/live/session/a/clip/names', self._session_a_clip_names)
        self.add_callback('/live/session/a/clip/names/all', self._session_a_clip_names_all)

        self.add_callback('/live/session/a/launch', self._session_a_launch)


        # Side B
        self.add_callback('/live/session/b/offsets', self._session_b_offsets)

        self.add_callback('/live/session/b/bank/down', self._session_b_bank_down)
        self.add_callback('/live/session/b/bank/up', self._session_b_bank_up)

        self.add_callback('/live/session/b/clip/names', self._session_b_clip_names)
        self.add_callback('/live/session/b/clip/names/all', self._session_b_clip_names_all)

        self.add_callback('/live/session/b/launch', self._session_b_launch)


        # Other Callbacks
        self.add_callback('/live/scene/name/block', self._scene_name_block)
        self.add_callback('/live/clip/name/block', self._clip_name_block)

        self.add_callback('/live/clip/color/block', self._clip_color_block)

        self.add_function_callback('/live/scenes', self._lo2_on_scene_list_changed)

    
    
    def _create_scene(self):
        #obj = SceneComponent if self._scene_count == -1 else self.scene_component_type
        sc = self.scene_component_type(num_slots=self._num_tracks, tracks_to_use_callback=self.tracks_to_use, id=self._scene_count)
        
        self._scene_count += 1
        return sc
    
    
    def on_scene_list_changed(self):
        self._reassign_scenes()
    
    
    def _reassign_scenes(self):
        self.log_message('reassigning scenes')
        diff = len(self.song().scenes) - len(self._scenes)
        
        if diff > 0:
            for i in range(diff):
                self._scenes.append(self._create_scene())
        
        if diff < 0:
            for i in range(len(self._scenes)-1, len(self.song().scenes)-1, -1):
                self._scene[i].disconnect()
                self._scene.remove(self._scene[i])
        
        for i,sc in enumerate(self._scenes):
            sc.set_scene(self.song().scenes[i])

    
    
    # Listeners
    def _lo2_on_scene_list_changed(self):
        if len(self.song().scenes) != self._scenes_count:
            self.send('/live/scenes', len(self.song().scenes))
            self._scenes_count = len(self.song().scenes)


    def _lo2_on_selected_scene_changed(self):
        idx = list(self.song().scenes).index(self.song().view.selected_scene)
        self.send('/live/scene/select', idx)



    # Scene Callbacks
    def _scene_name_block(self, msg, src):
        """ Gets block of scene names
        """
        b = []
        for i in range(msg[2], msg[2]+msg[3]):
            if i < len(self._scenes):
                s = self.scene[i]
                b.append(i, s.scene_name)
            else:
                b.append(i, '')

        self.send('/live/scene/name/block', b)
    
    
    def _scene_selected(self, msg, src):
        """  Selects a scene to view
            /live/scene/selected (int track) """
        if self.has_arg(msg):
            if msg[2] < len(self.song().scenes):
                self.song().view.selected_scene = self.song().scenes[msg[2]]
        else:
            idx = list(self.song().scenes).index(self.song().view.selected_scene)
            self.send('/live/scene/selected', idx)





    # Clip Callbacks
    def _clip_name_block(self, msg, src):
        """ Gets a block of clip names
        """
        b = []
        for i in range(msg[2], msg[2]+msg[4]):
            if i < len(self._scenes):
                s = self._scenes[i]
                for j in range(msg[3], msg[3]+msg[5]):
                    if j < len(s._clip_slots):
                        c = s._clip_slots[j]
                        b.append(c._get_name())
                    else:
                        b.append('')
            else:
                b.append('')

        self.send('/live/clip/name/block', *b)

    
    def _clip_color_block(self, msg, src):
        """ Gets a block of clip colors
        """
        b = []
        for i in range(msg[2], msg[2]+msg[4]):
            if i < len(self._scenes):
                s = self._scenes[i]
                for j in range(msg[3], msg[3]+msg[5]):
                    if j < len(s._clip_slots):
                        c = s._clip_slots[j]
                        self.log_message(c._get_color())
                        b.append(c._get_color())
                    else:
                        b.append('')
            else:
                b.append('')
        
        self.send('/live/clip/color/block', *b)

    
    # SESSION A CALLBACKS
    def _session_a_bank_down(self, msg, src):
        self._bank_down()
        self._session_a_offsets(msg, src)

    def _session_a_bank_up(self, msg, src):
        self._bank_up()
        self._session_a_offsets(msg, src)

    def _session_a_launch(self, msg, src):
        track_num = msg[2] + self.track_offset()
        scene_num = msg[3] + self.scene_offset()
        cs = self._scenes[scene_num]._clip_slots[track_num]
        try:
            cs._clip_slot.clip.fire()
        except Exception as e:
            cs._clip_slot.fire()

    def _session_a_offsets(self, msg, src):
        offsets = [self.track_offset(), self.scene_offset()]
        self.send('/live/session/a/offsets', *offsets)

    def _session_a_clip_names(self, msg, src):
        """ Gets a block of clip names
        """
        b = []
        for i in range(self.scene_offset(), self._assigned_height):
            if i < len(self._scenes):
                s = self._scenes[i]
                for j in range(self.track_offset(), self._assigned_width):
                    if j < len(s._clip_slots):
                        c = s._clip_slots[j]
                        b.append(c._get_name())
                    else:
                        b.append('')
            else:
                b.append('')

        self.send('/live/session/a/clip/names', *b)

    def _session_a_clip_names_all(self, msg, src):
        """ Gets a block of clip names
        """
        b = []
        for i in range(0, len(self._scenes)):
            if i < len(self._scenes):
                s = self._scenes[i]
                for j in range(self.track_offset(), self._assigned_width):
                    if j < len(s._clip_slots):
                        c = s._clip_slots[j]
                        b.append(c._get_name())
                    else:
                        b.append('')
            else:
                b.append('')

        self.send('/live/session/a/clip/names/all', *b)



    # SESSION B CALLBACKS
    def _session_b_bank_down(self, msg, src):
        if self._active_instances[1]:
            self._active_instances[1]._session._bank_down()
            self._session_b_offsets(msg, src)

    def _session_b_bank_up(self, msg, src):
        if self._active_instances[1]:
            self._active_instances[1]._session._bank_up()
            self._session_b_offsets(msg, src)
    
    def _session_b_launch(self, msg, src):
        session_b = self._active_instances[1]._session
        track_num = msg[2] + session_b.track_offset()
        scene_num = msg[3] + session_b.scene_offset()
        cs = self._scenes[scene_num]._clip_slots[track_num]
        try:
            cs._clip_slot.clip.fire()
        except Exception as e:
            cs._clip_slot.fire()

    def _session_b_offsets(self, msg, src):
        session_b = self._active_instances[1]._session
        offsets = [session_b.track_offset(), session_b.scene_offset()]
        self.send('/live/session/b/offsets', *offsets)

    def _session_b_clip_names(self, msg, src):
        """ Gets a block of clip names
        """
        b = []
        session_b = self._active_instances[1]._session
        scene_offset = session_b.scene_offset()
        track_offset = session_b.track_offset()
        toScene = scene_offset + self._assigned_height
        toTrack = track_offset + self._assigned_width

        for i in range(scene_offset, toScene):
            if i < len(self._scenes):
                s = self._scenes[i]
                for j in range(track_offset, toTrack):
                    if j < len(s._clip_slots):
                        c = s._clip_slots[j]
                        b.append(c._get_name())
                    else:
                        b.append('')
            else:
                b.append('')

        self.send('/live/session/b/clip/names', *b)

    def _session_b_clip_names_all(self, msg, src):
        """ Gets a block of clip names
        """
        b = []
        session_b = self._active_instances[1]._session
        scene_offset = 0
        track_offset = session_b.track_offset()
        toScene = len(self._scenes)
        toTrack = track_offset + self._assigned_width

        for i in range(scene_offset, toScene):
            if i < len(self._scenes):
                s = self._scenes[i]
                for j in range(track_offset, toTrack):
                    if j < len(s._clip_slots):
                        c = s._clip_slots[j]
                        b.append(c._get_name())
                    else:
                        b.append('')
            else:
                b.append('')

        self.send('/live/session/b/clip/names/all', *b)

