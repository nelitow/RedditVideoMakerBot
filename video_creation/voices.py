from gtts import gTTS
from pathlib import Path
from mutagen.mp3 import MP3
from utils.console import print_step, print_substep
from rich.progress import track
from googletrans import Translator
from dotenv import load_dotenv

import os


def save_text_to_mp3(reddit_obj):
    """Saves Text to MP3 files.

    Args:
        reddit_obj : The reddit object you received from the reddit API in the askreddit.py file.
    """
    load_dotenv()

    translate = os.getenv("TRANSLATE", default="no").casefold()

    print_step("Saving Text to MP3 files...")
    length = 0

    # Create a folder for the mp3 files.
    Path("assets/mp3").mkdir(parents=True, exist_ok=True)

    # assign reddit_obj["thread_title"] to variable
    thread_title = reddit_obj["thread_title"]
    # translate the thread_title to Portuguese with googletrans
    translator = Translator()
    if translate == "yes":
        thread_title_pt = translator.translate(
            thread_title, src='en', dest='pt').text
    else:
        thread_title_pt = thread_title

    print(thread_title_pt)

    tts = gTTS(text=thread_title_pt,
               lang="pt-br", slow=False, tld="com.br")
    tts.save(f"assets/mp3/title.mp3")
    length += MP3(f"assets/mp3/title.mp3").info.length

    try:
        Path(f"assets/mp3/posttext.mp3").unlink()
    except OSError as e:
        pass

    if reddit_obj["thread_post"] != "":
        if translate == "yes":
            thread_post_pt = translator.translate(
                reddit_obj["thread_post"], src='en', dest='pt').text
        else:
            thread_post_pt = reddit_obj["thread_post"]

        tts = gTTS(text=thread_post_pt,
                   lang="pt-BR", slow=False, tld="com.br")
        tts.save(f"assets/mp3/posttext.mp3")
        length += MP3(f"assets/mp3/posttext.mp3").info.length

    for idx, comment in track(enumerate(reddit_obj["comments"]), "Saving..."):
        # ! Stop creating mp3 files if the length is greater than 90 seconds and there is at least one comment.
        if length > 90 and idx > 0:
            break
        print(comment["comment_body"])
        if translate == "yes":
            comment_body_pt = translator.translate(
                comment["comment_body"], src='en', dest='pt').text
        else:
            comment_body_pt = comment["comment_body"]

        print(comment_body_pt)
        tts = gTTS(text=comment_body_pt,
                   lang="pt-BR", slow=False, tld="com.br")
        tts.save(f"assets/mp3/{idx}.mp3")
        length += MP3(f"assets/mp3/{idx}.mp3").info.length

    print_substep("Saved Text to MP3 files successfully.", style="bold green")
    # ! Return the index so we know how many screenshots of comments we need to make.
    return length, idx
