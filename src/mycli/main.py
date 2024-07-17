import re
import sys
import pathlib
import time
import click
import keyboard
import queue

import sounddevice as sd
import soundfile as sf
import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)

DESCRIPTORS_PATH_IN = "AcknowDescriptors.ndf"
DESCRIPTORS_PATH_OUT = "StratVOMod/GameData/Generated/Sound/AcknowDescriptors.ndf"
MOD_SOUNDS_BASEPATH = "C:\dev\warno-mods\StratVOMod\GameData\Assets\Sons\Acknows"

q = queue.Queue()

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())

def main():

    print("Record Warno VO")
    # TODO go through each voice line one by one
    # TODO press spacebar to start/stop the recording of each and save to the right place as an ogg file
    # TODO have a param to filter files by filename/prefix, to overwrite them or not so we can continue where we left off,
    ls = []
    txt = ""
    with open(DESCRIPTORS_PATH_IN) as input_file:
        txt = input_file.read()
        ls = re.findall("Identifier = '([^']+)'", txt)
    # TODO make this filter a parameter
    ls = [l for l in ls if l.startswith("FR/")]
    samplerate = 48000
    channels = 1
    sd.default.device = ("Microphone (Blue Snowball), Windows WASAPI", None)
    sd.default.samplerate = samplerate
    sd.default.channels = channels
    wasapi_exclusive = sd.WasapiSettings(exclusive=True)
    sd.default.extra_settings = wasapi_exclusive
    for identifier in ls:
        # TODO I need to add these files but change their path slightly and and change the folder or filename so that warno detects the new file instead of using the old one
        output_filepath = pathlib.Path(MOD_SOUNDS_BASEPATH, f"{identifier}_strat.ogg")
        if output_filepath.exists():
            print(f"{output_filepath} already exists, skipping to next file")
            continue
        restart_recording = True
        skip_file = False
        while restart_recording:
            output_filepath.unlink(missing_ok=True)
            restart_recording = False
            q = queue.Queue()
            print(f"Recording for: {identifier}")
            print("...")
            time.sleep(1)
            print("..")
            time.sleep(1)
            print(".")
            time.sleep(1)
            print("Go!")
            try:
                # Make sure the file is opened before recording anything:
                with sf.SoundFile(output_filepath, mode='x', samplerate=samplerate,
                                channels=channels) as file:
                    with sd.InputStream(samplerate=samplerate, callback=callback):
                        print('#' * 80)
                        print('Press r to restart the recording. Press s to skip this file. Press Spacebar to stop the recording')
                        print('#' * 80)
                        while True:
                            file.write(q.get())
                            if keyboard.is_pressed('r'):
                                restart_recording = True
                                break
                            if keyboard.is_pressed('s'):
                                skip_file = True
                                break
                            if keyboard.is_pressed(' '):
                                break
            except KeyboardInterrupt as e:
                output_filepath.unlink(missing_ok=True)
                raise
            except Exception as e:
                output_filepath.unlink(missing_ok=True)
                raise
            if skip_file:
                output_filepath.unlink(missing_ok=True)


try:
    #main()
    pass
except KeyboardInterrupt as e:
    sys.exit()
except Exception as e:
    sys.exit(type(e).__name__ + ': ' + str(e))
finally:
    # update acknow file
    valid_identifiers = []
    for x in pathlib.Path(MOD_SOUNDS_BASEPATH).glob('**/*'):
        if x.is_file():
            print(f"{x.parts[-2]}/{x.parts[-1].replace('_strat.ogg', '')}")
    output = ""
    with open(DESCRIPTORS_PATH_IN) as input_file:
        content = input_file.read()
        for ident in valid_identifiers:
            content = re.sub(ident, f"{ident}_strat", content, flags = re.M)
    print(content)
    sys.exit()
    with open(DESCRIPTORS_PATH_OUT) as output_file:
        output_file.write(output)