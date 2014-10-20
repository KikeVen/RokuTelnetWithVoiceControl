RokuTelnetWithVoiceControl
==========================

Simple Python script to connect to voice control Roku over telnet connection

Full description available at: http://quantitate.blogspot.com/2014/10/voice-control-your-roku-player-with.html

Required Python Modules: PyAudio, SpeechRecognizer

Required Libraries: PortAudio, flac

Required hardware: Roku streaming player (any model)

usage: python RokuVoiceControl.py host port

positional arguments:
  host
  port

optional arguments:
  -h, --help  show this help message and exit

Roku player must have dev mode enabled.  Put Roku in development mode by pressing the following button sequence on your Roku remote: Home (three times), up (twice), right, left, right, left, right.
