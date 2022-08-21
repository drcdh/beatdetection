import os

import librosa

from common import DEFAULT_FILE_PATH


def get_onset_times(file_path: str = DEFAULT_FILE_PATH):
    x, sr = librosa.load(file_path)
    onset_frames = librosa.onset.onset_detect(
        x, sr=sr, wait=1, pre_avg=1, post_avg=1, pre_max=1, post_max=1
    )
    onset_times = librosa.frames_to_time(onset_frames)
    return onset_times


def main(file_path: str = DEFAULT_FILE_PATH):
    onset_times = get_onset_times(file_path)
    # remove extension, .mp3, .wav etc.
    file_name_no_extension, _ = os.path.splitext(file_path)
    output_name = file_name_no_extension + ".librosa.beatmap.txt"
    with open(output_name, "wt") as f:
        f.write("\n".join(["%.4f" % onset_time for onset_time in onset_times]))


if __name__ == "__main__":
    main()
