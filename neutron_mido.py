import mido
import mido.backends.rtmidi

# ports 'Neutron(1):Neutron(1) MIDI 1 xx:0'
def ls_ports():
    ls_ports = mido.get_output_names()
    return ls_ports


def port_out(port):
    global neutron_port_out
    neutron_port_out = mido.open_output(port)
    return neutron_port_out


def port_in(port):
    global neutron_port_in
    neutron_port_in = mido.open_input(port)
    return neutron_port_in


# functions
def sysex(hex):
    hex=hex
    hex_ls = hex.split(" ")
    sysex = []
    for n in hex_ls:
        sysex.append(int(n, 16))
    return sysex


def sysex_msg(sysex):
    m = mido.Message('sysex', data=sysex)
    neutron_port_out.send(m)
    return m


def check_version():
    version = "00 20 32 28 00 73"
    msg = sysex(version)
    sysex_msg(msg)
    rec = neutron_port_in.receive()
    ver = list(rec.data)[7:12]
    ver_ = []
    for n in ver:
        ver_.append(chr(n))
    return "".join(ver_)


def key_press(key: int):
    m = mido.Message('note_on', note=key, time = 1.0)
    neutron_port_out.send(m)


def key_off():
    neutron_port_out.panic()


def osc1_pot_bypass(status: str):
    if status == "on":
        osc1_bypass = "00 20 32 28 00 0A 22 01"
    if status == "off":
        osc1_bypass = "00 20 32 28 00 0A 22 00"
    msg = sysex(osc1_bypass)
    sysex_msg(msg)
    return "bypass "+status


def osc2_pot_bypass(status: str):
    if status == "on":
        osc2_bypass = "00 20 32 28 00 0A 23 01"
    if status == "off":
        osc2_bypass = "00 20 32 28 00 0A 23 00"
    msg = sysex(osc2_bypass)
    sysex_msg(msg)
    return "bypass "+status


def osc1_autoglide(semitone: int):  # value 0-24 --> -12 +12 semitones
    val = hex(semitone).replace('0x', '')
    osc1_glide = "00 20 32 28 00 0A 24 "+val
    msg = sysex(osc1_glide)
    sysex_msg(msg)
    return "autoglide "+str(semitone)


def osc2_autoglide(semitone: int):  # value 0-24 --> -12 +12 semitones
    val = hex(semitone).replace('0x', '')
    semitone_ = range(-12, 13)
    osc2_glide = "00 20 32 28 00 0A 25 "+val
    msg = sysex(osc2_glide)
    sysex_msg(msg)
    return "autoglide "+str(semitone_[semitone])

def osc_sync(status:str):
    if status == "off":
        osc_sync_ = "00 20 32 28 00 0A 0E 00"
    if status == "on":
        osc_sync_ = "00 20 32 28 00 0A 0E 01"
    msg = sysex(osc_sync_)
    sysex_msg(msg)
    return "OSC Sync " + status.title()

def osc_paraphonic(status:str):
    if status == "off":
        osc_para = "00 20 32 28 00 0A 0F 00"
    if status == "on":
        osc_para = "00 20 32 28 00 0A 0F 01"
    msg = sysex(osc_para)
    sysex_msg(msg)
    return "OSC Paraphonic " + status.title()


def vcf_mode(mode:int):
    vcf_mode_ = "00 20 32 28 00 0A 0F "+str(mode)  # mode : 0-HP, 1-BP, 2-LP
    msg = sysex(vcf_mode_)
    sysex_msg(msg)
    if mode == 0:
        status = "Highpass"
    if mode == 1:
        status = "Bandpass"
    if mode == 2:
        status = "Lowpass"
    return "VCF " + status.title()


def key_split(key: int):
    val = hex(key).replace('0x','')
    split = "00 20 32 28 00 0A 28 "+val  #  key: 24-88. Key split note#, 0-off.
    msg = sysex(split)
    sysex_msg(msg)
    return "Split on "+str(key)

def lfo_blend(status):
    if status == "off":
        blend = "00 20 32 28 00 0A 30 01"
    if status == "on":
        blend = "00 20 32 28 00 0A 30 00"
    msg = sysex(blend)
    sysex_msg(msg)
    return "LFO Blend " + status.title()


def lfo_oneshot(status):
    if status == "off":
        oneshot = "00 20 32 28 00 0A 31 00"
    if status == "on":
        oneshot = "00 20 32 28 00 0A 31 01"
    msg = sysex(oneshot)
    sysex_msg(msg)
    return "Oneshot " + status.title()

def lfo_keysync(status):
    if status == "off":
        keysync = "00 20 32 28 00 0A 37 00"
    if status == "on":
        keysync = "00 20 32 28 00 0A 37 01"
    msg = sysex(keysync)
    sysex_msg(msg)
    return "Key Sync " + status.title()


def clock_sync(status):

    if status == "off":
        clocksync = "00 20 32 28 00 0A 35 00"
    if status == "on":
        clocksync = "00 20 32 28 00 0A 35 01"
    msg = sysex(clocksync)
    sysex_msg(msg)
    return "Clock Sync " + status.title()


def reset():
    msg = sysex("00 20 32 28 00 0B")
    sysex_msg(msg)
    return "RESET"

notes = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]*5
octaves = [1, 2, 3, 4, 5]*12
octaves.sort()
midi_notes_ = zip(notes, octaves)
midi_notes_ = list(midi_notes_)
midi_notes = []
for mn in midi_notes_:
    ls = list(mn)
    n = ls[0]+str(ls[1])
    midi_notes.append(n)
midi_val = list(range(24, 84))
midi_table = zip(midi_notes, midi_val)
midi_table = dict(midi_table)
midi_table.update({"OFF": 0})

semitone = list(range(-12, 13))
semitone_val = list(range(25))
semitone_str = []
for s in semitone:
    semitone_str.append(str(s))
semitone_table = zip(semitone_str, semitone_val)
semitone_table = dict(semitone_table)



def key_midi(note:str):
    return midi_table.get(note)



