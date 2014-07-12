#!/usr/bin/env python
#
# Sound recording class for use in JT65 steganography
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import sys
import struct
import wave
import pyaudio

# Recording classes graciously borrowed from
# https://gist.github.com/sloria/5693955


class JT65Recorder(object):

    def __init__(self, channels=1, rate=12000, frames_per_buffer=1024):
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer

    def open(self, fname, mode='wb'):
        return JT65RecordingFile(fname, mode, self.channels, self.rate,
                                 self.frames_per_buffer)


class JT65RecordingFile(object):

    def __init__(self, fname, mode, channels,
                 rate, frames_per_buffer):
        self.fname = fname
        self.mode = mode
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
        self._pa = pyaudio.PyAudio()
        self.wavefile = self._prepare_file(self.fname, self.mode)
#    self._stream = None
        self._stream = self._pa.open(format=pyaudio.paInt16,
                                     channels=self.channels,
                                     rate=self.rate,
                                     input=True,
                                     frames_per_buffer=self.frames_per_buffer)

    def __enter__(self):
        return self

    def __exit__(self, exception, value, traceback):
        self.close()

    def record(self, duration):
        # Use a stream with no callback function in blocking mode
#    self._stream = self._pa.open(format=pyaudio.paInt16,
#                                channels=self.channels,
#                                rate=self.rate,
#                                input=True,
#                                frames_per_buffer=self.frames_per_buffer)
        self._stream.start_stream()

        audio = ""
        for _ in range(int(self.rate / self.frames_per_buffer * duration)):
#      print "inloop " + str(len(audio)) +"\n"
            audio += self._stream.read(self.frames_per_buffer)
#      self.wavefile.writeframes(audio)
        self._stream.stop_stream()
        self.wavefile.writeframes(audio)
        return None

    def start_recording(self):
        # Use a stream with a callback in non-blocking mode
        self._stream = self._pa.open(format=pyaudio.paInt16,
                                     channels=self.channels,
                                     rate=self.rate,
                                     input=True,
                                     frames_per_buffer=self.frames_per_buffer,
                                     stream_callback=self.get_callback())
        self._stream.start_stream()
        return self

    def stop_recording(self):
        print "Called stop_recording"
        self._stream.stop_stream()
        print "Returning from stop_recording"
        return self

    def get_callback(self):
        def callback(in_data, frame_count, time_info, status):
            print "In callback!"
            self.wavefile.writeframes(in_data)
            return in_data, pyaudio.paContinue
        return callback

    def close(self):
        packed_zeros = struct.pack('h', int(0))
        values = []

        self._stream.close()
        self._pa.terminate()

        # Finish out the minute with silence for the decoders to be happy with
        # the .wav file
        for i in range(0, (12000 * 59) - (126 * 4464)):
            values.append(packed_zeros)
        # Write to file
        value_str = ''.join(values)
        self.wavefile.writeframes(value_str)

        self.wavefile.close()

    def _prepare_file(self, fname, mode='wb'):
        wavefile = wave.open(fname, mode)
        wavefile.setnchannels(self.channels)
        wavefile.setsampwidth(self._pa.get_sample_size(pyaudio.paInt16))
        wavefile.setframerate(self.rate)
        return wavefile

rec = JT65Recorder(channels=1)

with rec.open(sys.argv[1], "wb") as recfile:
    recfile.record(duration=52)
