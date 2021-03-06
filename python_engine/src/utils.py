import webvtt
import difflib
import requests
import youtube_dl
from functools import lru_cache
from typing import List, Dict
from urllib.parse import urlparse, parse_qs


def get_overlap(s1, s2):
    s = difflib.SequenceMatcher(None, s1, s2)
    _, _, size = s.find_longest_match(0, len(s1), 0, len(s2))
    return size


@lru_cache(maxsize=100)
def get_transcript_yt(url: str) -> Dict:
    """A simple function to get transcript of a YouTube Video

    Parameters
    ----------
    url : str
        The URL of the YouTube video whose transcript is to be fetched

    Returns
    -------
    subtitle_data : dict
        A dict with keys "subtitles" and "type"
    """

    # Setting youtube_dl options to fetch subtitles
    ydl_options = {
        "writesubtitles": True,
        "allsubtitles": True,
        "writeautomaticsub": True,
    }
    # Creating a youtube_dl object
    subtitle_data = {"subtitles": None, "type": None}
    ydl = youtube_dl.YoutubeDL(ydl_options)

    # We try to fetch the subtitles but in case if it fails we
    # fake the response such that we return subtitle_data without any data.
    try:
        ydl_resp = ydl.extract_info(url, download=False)
    except:
        ydl_resp = {"requested_subtitles": {"en": False}}
        print(f"Error encountered")

    # Checking if the response from youtube_dl has got what we need or not.
    if all([ydl_resp["requested_subtitles"], ydl_resp["requested_subtitles"]["en"]]):

        subtitles_url = ydl_resp["requested_subtitles"]["en"]["url"]
        response = requests.get(subtitles_url, stream=True)

        subtitles_type = (
            "manual_captions"
            if len(ydl_resp["subtitles"]) > 0
            else "automatic_captions"
        )

        subtitle_data["subtitles"], subtitle_data["type"] = (
            response.text,
            subtitles_type,
        )

    return subtitle_data


def vtt_to_corpus(vtt_path: str) -> str:
    """
    This function coverts the vtt fetched from youtube into a
    text corpus

    Parameters
    ----------
    vtt_path : str
        Path where vtt file has been saved

    Returns
    -------
    str
        The extracted corpus
    """
    corpus = " ".join(
        [caption.text.strip(" ").lower() for caption in webvtt.read(vtt_path)]
    )
    return corpus


def convert_to_secs(ts: str) -> int:
    hour, mins, secs = map(float, ts.split(":"))
    total_seconds = int((hour * 3600) + (mins * 60) + secs)
    return total_seconds


def search_transcript(target: str, vtt_path: str) -> List[int]:
    """
    A function to search vtt files, and return relevant timestamps

    Parameters
    ----------
    target : str
        String to find
    vtt_path : str
        Path to vtt file to search

    Returns
    -------
    List[int]
        List of all matching points in seconds.
    """
    timestamps = list()
    for caption in webvtt.read(vtt_path):
        overlap_score = get_overlap(target, caption.text)
        if overlap_score > 0:
            timestamps.append({"start": caption.start, "overlap_score": overlap_score})
    timestamps = [
        convert_to_secs(ts["start"])
        for ts in sorted(timestamps, key=lambda t: t["overlap_score"], reverse=True)
    ]
    return timestamps


def get_video_id(value):

    query = urlparse(value)
    if query.hostname == "youtu.be":
        return query.path[1:]
    if query.hostname in ("www.youtube.com", "youtube.com"):
        if query.path == "/watch":
            p = parse_qs(query.query)
            return p["v"][0]
        if query.path[:7] == "/embed/":
            return query.path.split("/")[2]
        if query.path[:3] == "/v/":
            return query.path.split("/")[2]

    return None


# TODO: Remove the block below
if __name__ == "__main__":
    with open("subs.vtt", "w+") as f:
        f.write(get_transcript_yt("https://youtu.be/aFmwPiuElsE")["subtitles"])
    with open("subs.txt", "w+") as out:
        out.write(vtt_to_corpus("subs.vtt"))
    target = input("Enter the query: ")
    print(search_transcript(target, "subs.vtt"))
