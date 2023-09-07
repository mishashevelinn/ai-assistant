#!/bin/bash

#Based on gist by https://gist.github.com/varqox
#gist: https://gist.github.com/varqox/c1a5d93d4d685ded539598676f550be8
# Sinks are for output, sources are for input. To stream source to sink a loopback must be created.

# Step 1
# Create output sink that will be recorded
# Our output sink will be named recording.
pacmd load-module module-null-sink sink_name=recording sink_properties=device.description=recording

#Step 2
#Create output sink that will forward data to recording and the default sink -- your headphones
#using speakers is not a good idea because they will be recorded by microphone for the second time

#First we have to locate our output sink:
echo "Enter the number of your output device. Headphones are preferable (usually bluez_sink.* for BT headphones):"
out_devices=`pacmd list-sinks | egrep '^\s+name: .*'`
pacmd list-sinks | egrep '^\s+name: .*' | cat -n
read sink_choise
arrIN=(${out_devices//"name:"/ })
chosen_device=${arrIN[(sink_choise - 1)]}
chosen_device="${chosen_device:1:-1}"
echo "Chosen output device: $chosen_device"

#Now we can combine it with our new recording sink into combined sink:

pacmd load-module module-combine-sink sink_name=combined sink_properties=device.description=combined slaves=recording,$chosen_device



#Step 3
# Attach microphone to recording sink
# First we have to locate our microphone as a source
echo "Enter the number of your mic device:"
sources=`pacmd list-sources | egrep '^\s+name: .*' | grep input`
pacmd list-sources | egrep '^\s+name: .*' | grep input | cat -n
read mic_choice
arrINm=(${sources//"name:"/ })
chosen_mic=${arrINm[(sink_choise - 1)]}
chosen_mic="${chosen_mic:1:-1}"
chosen_mic='alsa_input.pci-0000_00_1f.3.analog-stereo'
echo "Chosen mic: $chosen_mic"

#Now we attach the mic to redording sink:
#pacmd load-module module-loopback source=alsa_input.pci-0000_00_1f.3.analog-stereo sink=recording latency_msec=1
pacmd load-module module-loopback source="$chosen_mic" sink=recording latency_msec=1

# Step 4
#echo "In PulseAudioVolumeControl, channel the app(s), you want to record to combined sink"
#read

# Step 5
# With the above setup, you can start and stop recording at any time by terminating the script
#parecord --channels=2 -d recording.monitor wav.wav





