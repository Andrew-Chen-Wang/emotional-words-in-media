import pickle
import threading
from pathlib import Path

import youtube_dl


BASE_DIR = Path(__file__).resolve().parent


channels = [
    ("ABC", "https://www.youtube.com/channel/UCBi2mrWuNuyYy4gbM6fU18Q"),
    ("CNN", "https://www.youtube.com/user/CNN"),
    ("MSNBC", "https://www.youtube.com/channel/UCaXkIU1QidjPwiAYu6GcHjg"),
    ("NBC", "https://www.youtube.com/channel/UCeY0bbntWzzVIaj2z3QigXg")
]

independent_conservative_channels = []


def independent_conservative():
    threads = []

    def download_task(channel, url):
        path = BASE_DIR / "data" / "youtube" / f"{channel}.pickle"
        with youtube_dl.YoutubeDL({'ignoreerrors': True}) as ydl:
            playd = ydl.extract_info(url, download=False)
            with path.open("wb") as fp:
                pickle.dump(playd, fp, pickle.HIGHEST_PROTOCOL)

    for playlist in independent_conservative_channels:
        thread = threading.Thread(target=download_task, args=playlist)
        threads.append(thread)

    # Actually start downloading
    for thread in threads:
        thread.start()

    # Wait for all the downloads to complete
    for thread in threads:
        thread.join()


def extract_youtube_videos():
    for channel, playlist_id in channels:
        with youtube_dl.YoutubeDL({'ignoreerrors': True}) as ydl:
            playd = ydl.extract_info(playlist_id, download=False)
            path = BASE_DIR / "data" / "youtube" / f"{channel}.pickle"
            with path.open("wb") as fp:
                pickle.dump(playd, fp, pickle.HIGHEST_PROTOCOL)


def main():
    extract_youtube_videos()
    independent_conservative()


if __name__ == "__main__":
    main()
