import argparse
from urllib.parse import urlparse

from src.extract import extract_youtube_videos


def extract(given_list: list, **kwargs):
    if given_list:
        _follow = "Please follow the CONTRIBUTING.md guidelines."
        for url in given_list:
            parsed = urlparse(url)
            assert "youtube.com" in parsed.hostname, "Must be a YouTube link"
            assert parsed.path == "/playlist", f"Must be an Uploads playlist. {_follow}"
            assert "list" in parsed.query, f'"list" query missing in the url. {_follow}'
    else:
        given_list = [
            # American/Me-Perspective Liberal
            "https://www.youtube.com/playlist?list=UUBi2mrWuNuyYy4gbM6fU18Q",  # ABC
            "https://www.youtube.com/playlist?list=UUupvZG-5ko_eiXAupbDfxWw",  # CNN
            "https://www.youtube.com/playlist?list=UUaXkIU1QidjPwiAYu6GcHjg",  # MSNBC
            "https://www.youtube.com/playlist?list=UUeY0bbntWzzVIaj2z3QigXg",  # NBC
            # American/Me-Perspective Conservative honestly depressing having just one:(
            "https://www.youtube.com/playlist?list=UUXIJgqnII2ZOINSWNOGFThA",  # FOX
        ]
    extract_youtube_videos(given_list, **kwargs)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-e",
        "--extract",
        nargs="+",
        type=str,
        help="Playlists to extract",
    )
    parser.add_argument(
        "--skip-extract",
        action="store_true",
        default=False,
        help="Skip extracting information",
    )
    parser.add_argument(
        "-t",
        "--threaded",
        action="store_true",
        default=False,
        help="Execute program with multiple threads",
    )
    parser.add_argument(
        "--do-not-overwrite",
        action="store_true",
        default=False,
        help=(
            "On extraction, adding this flag will make sure that JSON data files "
            "are not overwritten."
        ),
    )
    parser.add_argument(
        "--save-as-json",
        action="store_true",
        default=False,
        help="Store the data as JSON",
    )
    parser.add_argument(
        "--save-in-dolt",
        action="store_true",
        default=False,
        help="Store the data as JSON",
    )
    parser.add_argument(
        "--db_uri",
        type=str,
        help="A specific DB uri to use instead of the default Dolt version",
    )
    args = vars(parser.parse_args())
    if not args.get("save_as_json") and not args.get("save_in_dolt"):
        print("You must save either as  json or in Dolt.")
        quit(1)
    if not args.get("skip_extract"):
        extract(args.get("extract"), **args)


if __name__ == "__main__":
    main()
