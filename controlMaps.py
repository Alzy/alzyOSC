"""
This file contains all constants representing the midi and
OSC maps for the specified parameters.
"""

# SIDE A

# SESSION
SIDE_A_MATRIX_KEYS = {
	'midi_key': [
		0, 1, 2, 3,
		4, 5, 6, 7,
		8, 9, 10, 11,
		12, 13, 14, 15
	],
	'osc_address': '/matrix_side_a' # #concat(, [n]) n
}

SIDE_A_SESSION_UP_BUTTON = {
	'midi_key': 28,
	'osc_address': '/session_up_side_a'
}

SIDE_A_SESSION_DOWN_BUTTON = {
	'midi_key': 29,
	'osc_address': '/session_down_side_a'
}

# TRACK
SIDE_A_TRACK_STOP_KEYS = {
	'midi_key': [16, 17, 18, 19],
	'osc_address': '/live/track/stop' # n: 0-4
}

SIDE_A_TRACK_MUTE_KEYS = {
	'midi_key': [20, 21, 22, 23],
	'osc_address': '/live/track/mute' # n: 0-4
}

SIDE_A_TRACK_SOLO_KEYS = {
	'midi_key': [24, 25, 26, 27],
	'osc_address': '/live/track/solo' # n: 0-4
}

SIDE_A_TRACK_VOLUME_CONTROLS = {
	'midi_cc': [0, 1, 2, 3],
	'osc_address': '/live/track/volume' # n: 0-4, n: 0-1
}

SIDE_A_VOLUME_CONTROL = {
	'midi_cc': 4,
	'osc_address': '/live/track/volume' # n: 9
}

SIDE_A_FLUSH_CONTROL = {
	'midi_cc': 5,
	'osc_address': '/flush_side_a'
}



# SIDE B

# SESSION
SIDE_B_MATRIX_KEYS = {
	'midi_key': [
		50, 51, 52, 53,
		54, 55, 56, 57,
		58, 59, 60, 61,
		62, 63, 64, 65
	],
	'osc_address': '/matrix_side_b' # #concat(, [n]) n
}

SIDE_B_SESSION_UP_BUTTON = {
	'midi_key': 78,
	'osc_address': '/session_up_side_b'
}

SIDE_B_SESSION_DOWN_BUTTON = {
	'midi_key': 79,
	'osc_address': '/session_down_side_b'
}

# TRACK
SIDE_B_TRACK_STOP_KEYS = {
	'midi_key': [66, 67, 68, 69],
	'osc_address': '/live/track/stop' # n: 0-4
}

SIDE_B_TRACK_MUTE_KEYS = {
	'midi_key': [70, 71, 72, 73],
	'osc_address': '/live/track/mute' # n: 0-4
}

SIDE_B_TRACK_SOLO_KEYS = {
	'midi_key': [74, 75, 76, 77],
	'osc_address': '/live/track/solo' # n: 0-4
}

SIDE_B_TRACK_VOLUME_CONTROLS = {
	'midi_cc': [50, 51, 52, 53],
	'osc_address': '/live/track/volume' # n: 0-4, n: 0-1
}

SIDE_B_VOLUME_CONTROL = {
	'midi_cc': 54,
	'osc_address': '/live/track/volume' # n: 9
}

SIDE_B_FLUSH_CONTROL = {
	'midi_cc': 55,
	'osc_address': '/flush_side_b'
}




