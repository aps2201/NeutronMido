from PySide6.QtWidgets import (QApplication, QCheckBox, QPushButton, QLabel, QWidget,
                               QVBoxLayout, QHBoxLayout, QComboBox, QGridLayout)
from neutron_mido import (ls_ports, port_out, port_in,
                          check_version, reset,
                          osc1_pot_bypass, osc2_pot_bypass,
                          osc_sync, osc_paraphonic, osc1_autoglide, osc2_autoglide, key_split,
                          lfo_blend, lfo_oneshot, lfo_keysync, clock_sync,
                          midi_table, semitone_table)
from PySide6.QtCore import Slot, Qt
import sys


@Slot()
def ver():
    version_ = check_version()
    version.setText(version_)
    print("Version: ",version_)


@Slot()
def bypass1():
    response = str()
    if osc1_bypass_chk.isChecked():
        response = osc1_pot_bypass("on")
    elif not osc1_bypass_chk.isChecked():
        response = osc1_pot_bypass("off")
    print(response)


@Slot()
def bypass2():
    response = str()
    if osc2_bypass_chk.isChecked():
        response = osc2_pot_bypass("on")
    elif not osc2_bypass_chk.isChecked():
        response = osc2_pot_bypass("off")
    print(response)


@Slot()
def paraphonic():
    response = str()
    if paraphonic_chk.isChecked():
        response = osc_paraphonic("on")
        key_split_widget.setVisible(True)
    elif not paraphonic_chk.isChecked():
        response = osc_paraphonic("off")
    if not paraphonic_chk.isChecked():
        key_split_widget.setVisible(False)
    print(response)


@Slot()
def sync():
    response = str()
    if sync_chk.isChecked():
        response = osc_sync("on")
    elif not sync_chk.isChecked():
        response = osc_sync("off")
    print(response)

@Slot()
def restore():
    reset()


@Slot()
def keysplit():
    note = key_split_combo.currentText()
    midi = midi_table.get(note)
    response = key_split(midi)
    print(response)


def autoglide1():
    semitone = autoglide1_combo.currentText()
    midi = semitone_table.get(semitone)
    response = osc1_autoglide(midi)
    print(response)


def autoglide2():
    semitone = autoglide2_combo.currentText()
    midi = semitone_table.get(semitone)
    response = osc2_autoglide(midi)
    print(response)


@Slot()
def blend_lfo():
    response = str()
    if blend_lfo_chk.isChecked():
        response = lfo_blend("on")
    elif not blend_lfo_chk.isChecked():
        response = lfo_blend("off")
    print(response)


@Slot()
def oneshot_lfo():
    response = str()
    if oneshot_lfo_chk.isChecked():
        response = lfo_oneshot("on")
    elif not oneshot_lfo_chk.isChecked():
        response = lfo_oneshot("off")
    print(response)


@Slot()
def keysync_lfo():
    response = str()
    if keysync_lfo_chk.isChecked():
        response = lfo_keysync("on")
        oneshot_lfo_chk.setVisible(True)
    elif not keysync_lfo_chk.isChecked():
        response = lfo_keysync("off")
    if not keysync_lfo_chk.isChecked():
        oneshot_lfo_chk.setVisible(False)
    print(response)


@Slot()
def clocksync_lfo():
    response = str()
    if clocksync_lfo_chk.isChecked():
        response = clock_sync("on")
    elif not clocksync_lfo_chk.isChecked():
        response = clock_sync("off")
    print(response)


@Slot()
def device_refresh():
    global ports_list
    ports_list = ls_ports()
    print(ports_list)


@Slot()
def device_select():
    #global neutron_port_out
    neutron_port_out = port_out(device_combo.currentText())
    neutron_port_in = port_in(device_combo.currentText())
    print(neutron_port_out,"\n",neutron_port_in)

# Application Start
app = QApplication(sys.argv)
app.setApplicationName = "Neutron MIDO"
version = QLabel()
version.setAlignment(Qt.AlignCenter)

device_layout = QHBoxLayout()
device_label = QLabel("Device")
device_combo = QComboBox()
device_refresh()
device_combo.addItems(ports_list)
device_btn = QPushButton("Refresh Devices")
device_combo.currentTextChanged.connect(device_select)
device_btn.clicked.connect(device_refresh)
device_layout.addWidget(device_label, 1)
device_layout.addWidget(device_combo, 1)
device_layout.addWidget(device_btn, 1)
device_widget = QWidget()
device_widget.setLayout(device_layout)

version_check = QPushButton("Check Version")
version_check.clicked.connect(ver)

reset_btn = QPushButton("Reset")
reset_btn.clicked.connect(restore)

# OSC SECTION
osc_title = QLabel("OSCILLATOR")

osc1_bypass_chk = QCheckBox("OSC 1 Tune Pot Bypass")
osc1_bypass_chk.stateChanged.connect(bypass1)

osc2_bypass_chk = QCheckBox("OSC 2 Tune Pot Bypass")
osc2_bypass_chk.stateChanged.connect(bypass2)

paraphonic_chk = QCheckBox("PARAPHONIC")
paraphonic_chk.stateChanged.connect(paraphonic)

sync_chk = QCheckBox("SYNC")
sync_chk.stateChanged.connect(sync)

key_split_layout = QHBoxLayout()
key_split_label = QLabel("Key Split")
key_split_combo = QComboBox()
key_split_combo.addItems(list(midi_table.keys()))
key_split_combo.setCurrentText("OFF")
key_split_combo.currentTextChanged.connect(keysplit)
key_split_layout.addWidget(key_split_label, 1)
key_split_layout.addWidget(key_split_combo, 1)
key_split_widget = QWidget()
key_split_widget.setLayout(key_split_layout)

autoglide_layout = QHBoxLayout()

autoglide1_label = QLabel("Autoglide OSC1")
autoglide1_label.setAlignment(Qt.AlignLeft)
autoglide1_combo = QComboBox()
autoglide1_combo.addItems(list(semitone_table.keys()))
autoglide1_combo.setCurrentText("0")
autoglide1_combo.currentTextChanged.connect(autoglide1)

autoglide2_label = QLabel("Autoglide OSC2")
autoglide2_label.setAlignment(Qt.AlignRight)
autoglide2_combo = QComboBox()
autoglide2_combo.addItems(list(semitone_table.keys()))
autoglide2_combo.setCurrentText("0")
autoglide2_combo.currentTextChanged.connect(autoglide2)

autoglide_layout.addWidget(autoglide1_combo, 1)
autoglide_layout.addWidget(autoglide1_label, 1)
autoglide_layout.addWidget(autoglide2_label, 1)
autoglide_layout.addWidget(autoglide2_combo, 1)
autoglide_widget = QWidget()
autoglide_widget.setLayout(autoglide_layout)

# LFO SECTION
lfo_title = QLabel("LFO")

blend_lfo_chk = QCheckBox("LFO Blend")
blend_lfo_chk.stateChanged.connect(blend_lfo)

keysync_lfo_chk = QCheckBox("LFO Key Sync")
keysync_lfo_chk.stateChanged.connect(keysync_lfo)

oneshot_lfo_chk = QCheckBox("LFO One Shot")
oneshot_lfo_chk.stateChanged.connect(oneshot_lfo)

clocksync_lfo_chk = QCheckBox("LFO MIDI Clock Sync")
clocksync_lfo_chk.stateChanged.connect(clocksync_lfo)

# Conditions
if not paraphonic_chk.isChecked():
    key_split_widget.setVisible(False)


if not keysync_lfo_chk.isChecked():
    oneshot_lfo_chk.setVisible(False)


class Widget(QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        main_layout = QGridLayout()

        layout = QVBoxLayout()
        # layout.addWidget()
        # layout.addWidget(version_check)
        # layout.addWidget(reset_btn)
        layout.addWidget(osc_title)
        layout.addWidget(osc1_bypass_chk)
        layout.addWidget(osc2_bypass_chk)
        layout.addWidget(sync_chk)
        layout.addWidget(paraphonic_chk)
        layout.addWidget(key_split_widget)
        layout.addWidget(autoglide_widget)
        layout_osc = QWidget()
        layout_osc.setLayout(layout)

        layout1 = QVBoxLayout()
        layout1.addWidget(lfo_title)
        layout1.addWidget(blend_lfo_chk)
        layout1.addWidget(keysync_lfo_chk)
        layout1.addWidget(oneshot_lfo_chk)
        layout1.addWidget(clocksync_lfo_chk)
        layout1.setAlignment(Qt.AlignTop)
        layout_lfo = QWidget()
        layout_lfo.setLayout(layout1)

        main_layout.setColumnMinimumWidth(1, 200)
        main_layout.addWidget(device_widget, 0, 0)
        main_layout.addWidget(version, 1, 0)
        main_layout.addWidget(version_check, 2, 0)
        main_layout.addWidget(layout_osc, 3, 0)
        main_layout.addWidget(layout_lfo, 3, 1)
        main_layout.addWidget(reset_btn, 4, 1)

        self.setLayout(main_layout)


@Slot()
def cleanup():
    neutron_port_out.close()
    # neutron_port_in.close()

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    w = Widget()
    w.setMinimumWidth(400)
    w.show()
    #app.exec()
    app.aboutToQuit.connect(cleanup)
    # Run the main Qt loop
    sys.exit(app.exec())


