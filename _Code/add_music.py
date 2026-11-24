"""
add_music.py — put the background music under the rendered video.

    python add_music.py <video.mp4> <music.mp3> <output.mp4>

Music: "Thinking Music" by Kevin MacLeod (incompetech.com),
licensed under Creative Commons: By Attribution 4.0.

Steps:
  1. read the music file into an array of samples
  2. the track is 3:16 but the video is 5:00, so repeat it with a 4-second crossfade
  3. fade in at the start, fade out at the end, and turn it down (-6 dB) so the voice stays clear
  4. copy the video picture unchanged and add the music as the sound track
"""
import sys

import av
import numpy as np

VOLUME_DB = -6           # how much quieter than the original track the music is (lands around -31 dB)
CROSSFADE = 4.0          # seconds of overlap when the track repeats


def read_audio(path):
    """Decode an audio file into a (samples, 2) float array, plus its sample rate."""
    with av.open(path) as f:
        stream = f.streams.audio[0]
        rate = stream.rate
        chunks = [frame.to_ndarray() for frame in f.decode(stream)]
    audio = np.concatenate(chunks, axis=1).T.astype(np.float32)   # -> (samples, channels)
    if audio.shape[1] == 1:
        audio = np.repeat(audio, 2, axis=1)
    return audio, rate


def loop_to_length(audio, rate, seconds):
    """Repeat the track (with a smooth crossfade at each join) until it is `seconds` long."""
    need = int(seconds * rate)
    overlap = int(CROSSFADE * rate)
    fade_out = np.linspace(1, 0, overlap)[:, None]
    fade_in = np.linspace(0, 1, overlap)[:, None]
    result = audio.copy()
    while len(result) < need:
        joined = result[-overlap:] * fade_out + audio[:overlap] * fade_in
        result = np.concatenate([result[:-overlap], joined, audio[overlap:]])
    return result[:need]


def main(video_path, music_path, out_path):
    video = av.open(video_path)
    duration = float(video.duration) / av.time_base

    music, rate = read_audio(music_path)
    music = loop_to_length(music, rate, duration)
    t = np.arange(len(music)) / rate
    fade = np.minimum(1, t / 2.0) * np.clip((duration - t) / 4.0, 0, 1)   # 2 s fade in, 4 s fade out
    music = (music * fade[:, None] * 10 ** (VOLUME_DB / 20)).astype(np.float32)

    out = av.open(out_path, "w")
    video_in = video.streams.video[0]
    video_out = out.add_stream_from_template(video_in)     # picture is copied, not re-encoded
    audio_out = out.add_stream("aac", rate=rate)
    audio_out.layout = "stereo"
    audio_out.bit_rate = 192000

    # encode the music into AAC packets
    audio_packets = []
    for start in range(0, len(music), 1024):
        frame = av.AudioFrame.from_ndarray(np.ascontiguousarray(music[start:start + 1024].T),
                                           format="fltp", layout="stereo")
        frame.sample_rate = rate
        frame.pts = start
        audio_packets += audio_out.encode(frame)
    audio_packets += audio_out.encode(None)

    # write video and audio packets in time order
    a = 0
    for packet in video.demux(video_in):
        if packet.dts is None:
            continue
        now = float(packet.pts * video_in.time_base)
        while a < len(audio_packets) and float(audio_packets[a].pts * audio_packets[a].time_base) <= now:
            out.mux(audio_packets[a])
            a += 1
        packet.stream = video_out
        out.mux(packet)
    for packet in audio_packets[a:]:
        out.mux(packet)
    out.close()
    video.close()
    print("saved", out_path)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
