(function(){

    // Do whatever you want, initialize some variables, declare some functions, ...
    var HOST = 'localhost'
    var PORT = 9000
    var PORT_OUT = 9001

    var SESSION_A_OFFSETS = {
      'TRACK': 0,
      'SCENE': 0
    }
    var SESSION_A_CLIPMAP = []

    var SESSION_B_OFFSETS = {
      'TRACK': 4,
      'SCENE': 0
    }
    var SESSION_B_CLIPMAP = []

    var REDRAW_COUNT = 0
    // 

    function set_session_a_offsets(args) {
      SESSION_A_OFFSETS['TRACK'] = args[0]['value']
      SESSION_A_OFFSETS['SCENE'] = args[1]['value']
    }

    function set_session_b_offsets(args) {
      SESSION_B_OFFSETS['TRACK'] = args[0]['value']
      SESSION_B_OFFSETS['SCENE'] = args[1]['value']
    }

    function set_session_a_clipmap_names(args) {
      for(let i=0; i < args.length; i++){
        try {
          SESSION_A_CLIPMAP[i]['name'] = args[i]['value']
        } catch(e) {
          SESSION_A_CLIPMAP[i] = {
            'name': args[i]['value'],
            'state': 0
          }
        }
      }
    }

    function set_session_b_clipmap_names(args) {
      for(let i=0; i < args.length; i++){
        try {
          SESSION_B_CLIPMAP[i]['name'] = args[i]['value']
        } catch(e) {
          SESSION_B_CLIPMAP[i] = {
            'name': args[i]['value'],
            'state': 0
          }
        }
      }
    }



    /////////////////
    // CLIP COLORS //
    /////////////////
    // UTILS
    function decimalToHexString(number)
    {
      if (number < 0)
      {
        number = 0xFFFFFFFF + number + 1
      }

      return number.toString(16).toUpperCase().padStart(6, '0')
    }
    function hexToRgb(hex) {
        var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex)
        return (result ? {
            r: parseInt(result[1], 16),
            g: parseInt(result[2], 16),
            b: parseInt(result[3], 16)
        } : null)
    }
    function getColorBrightness(r, g, b){
        return (r * 299 + g * 587 + b * 114) / 1000
    }
    function getBrightnessCompliment(hexColor) {
        var rgbColor = hexToRgb(hexColor)
        var brightnessValue = getColorBrightness(rgbColor.r, rgbColor.g, rgbColor.b)
        return (brightnessValue > 150 ? 'black': 'white')
    }
    // SETTING
    function set_session_a_clipmap_colors(args) {
      for(let i=0; i < args.length; i++){
        var colorInHex = '#' + decimalToHexString(args[i]['value'])
        if (args[i]['value'] == 0) {colorInHex = '#a2a2a2'}
        var labelColor = getBrightnessCompliment(colorInHex)

        try {
          SESSION_A_CLIPMAP[i]['color'] = colorInHex
          SESSION_A_CLIPMAP[i]['labelColor'] = labelColor
        } catch(e) {
          SESSION_A_CLIPMAP[i] = {
            'color': colorInHex,
            'labelColor': labelColor,
            'state': 0
          }
        }
      }
    }

    function set_session_b_clipmap_colors(args) {
      for(let i=0; i < args.length; i++){
        var colorInHex = '#' + decimalToHexString(args[i]['value'])
        if (args[i]['value'] == 0) {colorInHex = '#a2a2a2'}
        var labelColor = getBrightnessCompliment(colorInHex)

        try {
          SESSION_B_CLIPMAP[i]['color'] = colorInHex
          SESSION_B_CLIPMAP[i]['labelColor'] = labelColor
        } catch(e) {
          SESSION_B_CLIPMAP[i] = {
            'color': colorInHex,
            'labelColor': labelColor,
            'state': 0
          }
        }
      }
    }

    function handle_track_state_change(args) {
      var affected_track = args[0]['value']
      var isSessionA = (affected_track < 4)
      var track_state = args[1]['value']
      var is_playing = (track_state < 0 ? 0 : 1)
      // track states:
      // -2 == stopped
      // 1 == playing
      for(var i=0; i < SESSION_A_CLIPMAP.length; i++){
        if(i % 4 == affected_track) {
          if(track_state == -2) {
            // stop all clips in this track if this track set to stop
            if (isSessionA) {
              SESSION_A_CLIPMAP[i]['state'] = 0
            } else {
              SESSION_B_CLIPMAP[i]['state'] = 0
            }
          }
        }
      }

      var oscAddress = '/track_state_'
      if (isSessionA) {
        redraw_session_a()
        oscAddress += 'a_' + affected_track
      } else {
        affected_track = affected_track - 4
        redraw_session_b()
        // compensate 4 tracks since session b starts at track 4 (5)
        oscAddress += 'b_' + affected_track
      }
      sendOsc({
        address: oscAddress,
        args: [{type: 'i', value: is_playing}],
        host: HOST,
        port: PORT
      })
    }

    function handle_clip_state_change(args) {
      var track = (args[0]['value'])
      var isSessionA = (track < 4)
      if(!isSessionA){
        track = track - 4
      }

      var scene = (args[1]['value'])

      var affected_clip =  track + (scene * 4)

      var clip_state = args[2]['value']
      // clip states:
      // 2 == playing
      // 1 == stopped?
      if(clip_state == 2) {
        // stop this clip if this clip set to stop
        if (isSessionA) {
          SESSION_A_CLIPMAP[affected_clip]['state'] = 1
        } else {
          SESSION_B_CLIPMAP[affected_clip]['state'] = 1
        }
      } else{
        if (isSessionA) {
          SESSION_A_CLIPMAP[affected_clip]['state'] = 0
        } else {
          SESSION_B_CLIPMAP[affected_clip]['state'] = 0
        }
      }

      if (isSessionA) {
        redraw_session_a()
      } else {
        redraw_session_b()
      }
    }


    /**
     * Unclicks the button in the matrix.
     * (Trying to set this through props doesn't work)
     *
     * sessionLetter == 'A' or 'B'
     * index == [0-15]
     */
    function unsetMatrixButton(sessionLetter, index){
      var oscAddress = ''
      if(sessionLetter == 'A') {
        oscAddress = '/side_a_matrix/' + index
      } else {
        oscAddress = '/side_b_matrix/' + index
      }

      sendOsc({
        address: oscAddress,
        args: [{type: 'i', value: 0}],
        host: HOST,
        port: PORT
      })
    }


    /**
     * Moves the session down number of skipCount.
     */
    function sceneDownSkip (sessionLetter, skipCount) {
      sessionLetter = sessionLetter.toLowerCase()
      var address = '/live/session/' + sessionLetter + '/bank/down'

      for (var i = 0; i < skipCount; i++) {      
        sendOsc({
          address: address,
          args: [
            {type: 'i', value: 1},
          ],
          host: HOST,
          port: PORT_OUT
        })      
      };
    }
    /**
     * Moves the session down number of skipCount.
     */
    function sceneUpSkip (sessionLetter, skipCount) {
      sessionLetter = sessionLetter.toLowerCase()
      var address = '/live/session/' + sessionLetter + '/bank/up'

      for (var i = 0; i < skipCount; i++) {      
        sendOsc({
          address: address,
          args: [
            {type: 'i', value: 1},
          ],
          host: HOST,
          port: PORT_OUT
        })      
      };
    }



    function redraw_session_a () {
      var start_pos = SESSION_A_OFFSETS['SCENE'] * 4
      var end_pos = start_pos + 20

      var labels = []
      for(var i = start_pos; i < end_pos; i++){
        labels.push('"' + SESSION_A_CLIPMAP[i]['name'] + '"')
      }
      var states = []
      for(var i = start_pos; i < end_pos; i++){
        states.push(SESSION_A_CLIPMAP[i]['state'])
      }
      var colors = []
      for(var i = start_pos; i < end_pos; i++){
        colors.push('"background-color: '+SESSION_A_CLIPMAP[i]['color']+'; color: '+SESSION_A_CLIPMAP[i]['labelColor']+';"')
      }

      var propsMsg = `
        #{
          props = {\\}
          labelValues = [${String(labels)}];
          values = [${String(states)}];
          colors = [${String(colors)}];
          props.value = values[\$];
          props.label = labelValues[\$];
          props.css = colors[\$];
        }
      `
      msg = {"props": propsMsg}

      sendOsc({
        address: '/EDIT',
        args: [
          {type: 's', value: 'side_a_matrix'},
          {type: 's', value: JSON.stringify(msg)}
        ],
        host: HOST,
        port: PORT
      })
    }

    function redraw_session_b () {
      var start_pos = SESSION_B_OFFSETS['SCENE'] * 4
      var end_pos = start_pos + 20

      var labels = []
      for(var i = start_pos; i < end_pos; i++){
        labels.push('"' + SESSION_B_CLIPMAP[i]['name'] + '"')
      }
      var states = []
      for(var i = start_pos; i < end_pos; i++){
        states.push(SESSION_B_CLIPMAP[i]['state'])
      }
      var colors = []
      for(var i = start_pos; i < end_pos; i++){
        colors.push('"background-color: '+SESSION_B_CLIPMAP[i]['color']+'; color: '+SESSION_B_CLIPMAP[i]['labelColor']+';"')
      }

      var propsMsg = `
        #{
          props = {\\}
          labelValues = [${String(labels)}];
          values = [${String(states)}];
          colors = [${String(colors)}];
          props.value = values[\$];
          props.label = labelValues[\$];
          props.css = colors[\$];
        }
      `
      msg = {"props": propsMsg}

      sendOsc({
        address: '/EDIT',
        args: [
          {type: 's', value: 'side_b_matrix'},
          {type: 's', value: JSON.stringify(msg)}
        ],
        host: HOST,
        port: PORT
      })
    }


    return {
      init: function(){
        // this will be executed once when the osc server starts
      },
      oscInFilter:function(data){
        // Filter incomming osc messages
        // address = string
        // args = array of {value, type} objects
        // host = string
        // port = integer
        var {address, args, host, port} = data

        // do what you want
        // console.log('recieved:')
        // console.log(address)
        // console.log(args)

        switch (address.trim()) {
          case '/live/session/a/offsets':
            set_session_a_offsets(args);
            redraw_session_a();
            break;
          case '/live/session/a/clip/names/all':
            set_session_a_clipmap_names(args);
            redraw_session_a();
            break;
          case '/live/session/a/clip/colors/all':
            set_session_a_clipmap_colors(args);
            redraw_session_a();
            break;
          case '/live/session/b/offsets':
            set_session_b_offsets(args);
            redraw_session_b();
            break;
          case '/live/session/b/clip/names/all':
            set_session_b_clipmap_names(args);
            redraw_session_b();
            break;
          case '/live/session/b/clip/colors/all':
            set_session_b_clipmap_colors(args);
            redraw_session_b();
            break;
          case '/live/track/state':
            handle_track_state_change(args);
            break;
          case '/live/clip/state':
            handle_clip_state_change(args);
            break;
        }


        // return data if you want the message to be processed
        return {address, args, host, port}

      },
      oscOutFilter:function(data){
        // Filter outgoing osc messages

        var {address, args, host, port} = data

        if(address.search('side_a_matrix') >= 0){
          var btnPressed = parseInt(address.split('/side_a_matrix/')[1])
          var btnColumn = btnPressed % 4
          var btnRow = Math.floor(btnPressed/4)

          // quick hack to check if a STOP clip was activated. If so, unclick the 
          // button in the button matrix
          var clipArrayIndex = SESSION_A_OFFSETS['SCENE'] * 4 + btnPressed
          var clipName = SESSION_A_CLIPMAP[clipArrayIndex]['name']
          if (clipName == ''){unsetMatrixButton('A', btnPressed)}

          address = '/live/session/a/launch'
          args = [
            {
              'type': 'i',
              'value': btnColumn
            },
            {
              'type': 'i',
              'value': btnRow
            }
          ]
        }

        if(address.search('side_a_cue') >= 0){
          address = '/live/track/solo'
          var side_a_cue_track = 9
          var side_a_cue_value = args[0]

          args = [
            {
              'type': 'i',
              'value': side_a_cue_track
            },
            {
              'type': 'i',
              'value': side_a_cue_value.value
            }
          ]
        }
        if(address.search('side_b_cue') >= 0){
          address = '/live/track/solo'
          var side_b_cue_track = 10
          var side_b_cue_value = args[0]

          args = [
            {
              'type': 'i',
              'value': side_b_cue_track
            },
            {
              'type': 'i',
              'value': side_b_cue_value.value
            }
          ]
        }

        if(address.search('side_b_matrix') >= 0){
          var btnPressed = parseInt(address.split('/side_b_matrix/')[1])
          var btnColumn = btnPressed % 4
          var btnRow = Math.floor(btnPressed/4)

          // quick hack to check if a STOP clip was activated. If so, unclick the 
          // button in the button matrix
          var clipArrayIndex = SESSION_B_OFFSETS['SCENE'] * 4 + btnPressed
          var clipName = SESSION_B_CLIPMAP[clipArrayIndex]['name']
          if (clipName == ''){unsetMatrixButton('B', btnPressed)}

          address = '/live/session/b/launch'
          args = [
            {
              'type': 'i',
              'value': btnColumn
            },
            {
              'type': 'i',
              'value': btnRow
            }
          ]
        }



        if(address.search('side_a_down_4') >= 0 || address.search('side_b_down_4') >= 0) {
          var sessionLetter = (address.search('side_a_down_4') >= 0 ? 'a': 'b')
          sceneDownSkip(sessionLetter, 4)
        }
        if(address.search('side_a_up_4') >= 0 || address.search('side_b_up_4') >= 0) {
          var sessionLetter = (address.search('side_a_up_4') >= 0 ? 'a': 'b')
          sceneUpSkip(sessionLetter, 4)
        }

        // return data if you want the message to be and sent
        return {address, args, host, port}
      }
    }

})()