import os

from aubio import source, onset

from common import DEFAULT_FILE_PATH


def get_onset_times(file_path: str = DEFAULT_FILE_PATH):
    window_size = 1024  # FFT size
    hop_size = window_size // 4

    sample_rate = 0
    src_func = source(file_path, sample_rate, hop_size)
    sample_rate = src_func.samplerate
    onset_func = onset("default", window_size, hop_size)

    duration = float(src_func.duration) / src_func.samplerate

    onset_times = []  # seconds
    while True:  # read frames
        samples, num_frames_read = src_func()
        if onset_func(samples):
            onset_time = onset_func.get_last_s()
            if onset_time < duration:
                onset_times.append(onset_time)
            else:
                break
        if num_frames_read < hop_size:
            break

    return onset_times


def main(file_path: str = DEFAULT_FILE_PATH):
    onset_times = get_onset_times(file_path)
    # remove extension, .mp3, .wav etc.
    file_name_no_extension, _ = os.path.splitext(file_path)
    output_name = file_name_no_extension + ".aubio.beatmap.txt"
    with open(output_name, "wt") as f:
        f.write("\n".join(["%.4f" % onset_time for onset_time in onset_times]))


if __name__ == "__main__":
    main()
