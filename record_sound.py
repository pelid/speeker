import pyaudio
import wave
import io
import logging

logger = logging.getLogger('record_sound')

def record(duration=5, device_index=None):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    # FORMAT = pyaudio.get_format_from_width(wf.getsampwidth())
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = duration

    py_audio = pyaudio.PyAudio()

    stream = py_audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=device_index,
                    frames_per_buffer=CHUNK)

    logger.debug('* recording')

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    logger.debug('* done recording')

    stream.stop_stream()
    stream.close()
    py_audio.terminate()

    audio_buffer = b''.join(frames)

    wave_output = io.BytesIO()
    # WAVE_OUTPUT_FILENAME='sound.wav'
    wave_obj = wave.open(wave_output, 'wb')
    wave_obj.setnchannels(CHANNELS)
    wave_obj.setsampwidth(py_audio.get_sample_size(FORMAT))
    wave_obj.setframerate(RATE)
    wave_obj.writeframes(b''.join(frames))
    wave_obj.close()

    return wave_output.getvalue() # WAV format
