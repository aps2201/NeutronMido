# Behringer Neutron Cross Platform App

A _potentially_ cross platform app for the Behringer Neutron. Ideally this would be a drop in of the official app,
however as you can see it is just bare bones mostly. This was built in Python:3.13.2 based on [Mido](https://mido.readthedocs.io/en/stable/)
with the [RTMidi](https://pypi.org/project/python-rtmidi/) backend. The GUI is Qt by way of [PySide6](https://doc.qt.io/qtforpython-6/).
The release only has a Linux binary but the `pyside6-deploy neutron_qt.py --name NeutronMido` command can potentially [create a NeutronMido binary in Linux, Windows, or Mac](https://doc.qt.io/qtforpython-6/deployment/index.html).

The `sysex()` and `sysex_msg()` does most of the heavy lifting since mido communicates in midi values while the commands
are in hex. Here is a simple format on sending messages to the device.

```commandline
msg = sysex([SysEx_Command])
sysex_msg(msg)
```

This is my attempt to have a reason to use Qt after all this time. 
Also the Neutron app doesn't work on linux, which is my primary OS. At the moment I'm only implementing features that 
I use regularly but I've also added a list of SysEx Commands directly from the manual so go ahead and fork your own.
Will probably develop this again if I have the time, but one thing I couldn't figure out is 
how to access the tuners like in the official app. Would be great if that can happen through SysEx.

# List of SysEx Commands:
___Removed F0 and F7 for convenience___

___Note that ID will almost always be 00___ 

| Command                        | Sysex                      | Notes                                                                                                                                                                                 |
|--------------------------------|----------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Set MIDI channel (*)           | 00 20 32 28 ID 0A 00 MM    | MM = 0-F --> MIDI channel 1-16 Note: using this command to set the MIDI channel will automatically disable the DIP switches(which will persist across power cycles) on the back panel |
| Set Key Priority               | 00 20 32 28 ID 0A 01 MM    | MM = 0-LO, 1-HI, 2-Last. Default:2-Last                                                                                                                                               |
| Set Pitch Bend Range (*)       | 00 20 32 28 ID 0A 03 MM    | MM = 0-24 (semitones). Default:2                                                                                                                                                      |
| Set ASSIGN out                 | 00 20 32 28 ID 0A 04 MM    | MM = 0-OSC 1 CV, 1-OSC 2 CV, 2-"Note On" velocity, 3-Modwheel, 4-Aftertouch. Default:0                                                                                                |
| Set Envelope retriggering      | 00 20 32 28 ID 0A 05 MM    | MM = 1-Enabled, 0-Disabled. Default:0-Disabled                                                                                                                                        |
| Reset Min/Max MIDI notes       | 00 20 32 28 ID 0A 06 MM    | MM = not used                                                                                                                                                                         |
| Set Polychain Mode             | 00 20 32 28 ID 0A 08 MM    | MM = 0-Disabled, 1-Enabled. Default:0                                                                                                                                                 |
| Set Device ID                  | 00 20 32 28 ID 0A 09 MM    | MM = 0-F --> MIDI ID 1-16. Default:0                                                                                                                                                  |
| Disable MIDI DIP switches      | 00 20 32 28 ID 0A 0A MM    | MM = 0-Enabled, 1-Disabled. Default:0-Enabled                                                                                                                                         |
| Set Mute Out-Of-Range notes    | 00 20 32 28 ID 0A 0B MM    | MM = 1-mute, 0-not mute. Default:0-not mute                                                                                                                                           |
| Set Min MIDI note              | 00 20 32 28 ID 0A 0C MM    | MM = MIDI note number. Default:24                                                                                                                                                     |
| Set Max MIDI note              | 00 20 32 28 ID 0A 0D MM    | MM = MIDI note number. Default:96                                                                                                                                                     |
| Set OSC Sync                   | 00 20 32 28 ID 0A 0E MM    | MM = 0-Enabled, 1-Disabled. Default:0-Enabled                                                                                                                                         |
| Set Paraphonic Mode            | 00 20 32 28 ID 0A 0F MM    | MM = 0-Monophonic, 1-Paraphonic. Default:0-Monophonic                                                                                                                                 |
| Set VCF mode                   | 00 20 32 28 ID 0A 10 MM    | MM = 0-HP, 1-BP, 2-LP                                                                                                                                                                 |
| Set VCF keytrack               | 00 20 32 28 ID 0A 11 MM    | MM = 0-Disabled, 1-Enabled. Default:0                                                                                                                                                 |
| Set VCF mod src                | 00 20 32 28 ID 0A 12 MM    | MM = 0-Disabled, 1-aftertouch, 2-modwheel, 3-velocity                                                                                                                                 |
| Set VCF mod depth              | 00 20 32 28 ID 0A 14 MM    | MM = 0-3F where 0 is the minimum & 3F(63dec) is the maximum (100%)                                                                                                                    |
| Set OSC 1 shape blend          | 00 20 32 28 ID 0A 20 MM    | MM = 1-No blend, 0-Blend. Default:0-Blend                                                                                                                                             |
| Set OSC 2 shape blend          | 00 20 32 28 ID 0A 21 MM    | MM = 1-No blend, 0-Blend. Default:0-Blend                                                                                                                                             |
| Set OSC 1 tune pot bypass      | 00 20 32 28 ID 0A 22 MM    | MM = 0-Not bypassed, 1-Bypassed. Default:0-Not bypassed                                                                                                                               |
| Set OSC 2 tune pot bypass      | 00 20 32 28 ID 0A 23 MM    | MM = 0-Not bypassed, 1-Bypassed. Default:0-Not bypassed                                                                                                                               |
| Set OSC 1 autoglide            | 00 20 32 28 ID 0A 24 MM    | MM = 0-24 Range is -12->+12 so 12 is no autoglide. Default:12-No autoglide                                                                                                            |
| Set OSC 2 autoglide            | 00 20 32 28 ID 0A 25 MM    | MM = 0-24 Range is -12->+12 so 12 is no autoglide. Default:12-No autoglide                                                                                                            |
| Set OSC 1 range                | 00 20 32 28 ID 0A 26 MM    | MM = 0[32'], 1[16'], 2[8'] & 3[+/- 10 oct mode]                                                                                                                                       |
| Set OSC 2 range                | 00 20 32 28 ID 0A 27 MM    | MM = 0[32'], 1[16'], 2[8'] & 3[+/- 10 oct mode]                                                                                                                                       |
| Set OSC key split (*)          | 00 20 32 28 ID 0A 28 MM    | MM = 0, 24-88. Key split note#, 0-off. Default:0-off. NB key split note# is the start of OSC2 range                                                                                   |
| Set LFO shape blend            | 00 20 32 28 ID 0A 30 MM    | MM = 1-No blend, 0-Blend. Default:0-Blend                                                                                                                                             |
| Set LFO One shot mode          | 00 20 32 28 ID 0A 31 MM    | MM = 1-Enabled, 0-Disabled. Default:0-Disabled                                                                                                                                        |
| Set LFO rate key track key (*) | 00 20 32 28 ID 0A 32 MM    | MM = LFO rate root MIDI note number 12-108. 0 – Disabled                                                                                                                              |
| Set LFO depth                  | 00 20 32 28 ID 0A 34 MM    | MM = 0-20%, 1-40%, 2-60%, 3-80%, 4-100%. Default:4-100%                                                                                                                               |
| Set LFO ignore MIDI CLK sync   | 00 20 32 28 ID 0A 35 MM    | MM = 0-CLK sync, 1-ignore CLK sync. Default:0-CLK sync                                                                                                                                |
| Set LFO key sync               | 00 20 32 28 ID 0A 37 MM    | MM = 0-Enabled, 1-Disabled. Default:0-Enabled                                                                                                                                         |
| Set LFO Shape order (2)        | 00 20 32 28 ID 0A 38 MM    | MM = LFO Slot index: =0..4 NN = LFO shape value: = 0..4                                                                                                                               |
| Restore LFO Shape order        | 00 20 32 28 ID 0A 39 MM    | MM - Not used                                                                                                                                                                         |
| Set LFO Shape phase            | 00 20 32 28 ID 0A 3A MM NN | MM = LFO Shape index: =0..4 NN = LFO phase value: = 0..7 - in eighths of 2*PI (or 45 degrees)                                                                                         |
| Set LFO retrigger              | 00 20 32 28 ID 0A 3B MM    | MM = 0-overlapping notes will not retrigger the LFO, 1-overlapping notes will retrigger the LFO.                                                                                      |



















