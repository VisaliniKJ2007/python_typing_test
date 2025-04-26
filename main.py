from pyodide import js
import random
import time
from pyodide.ffi import create_proxy
from difflib import SequenceMatcher

# Predefined sentences (no database needed in browser)
sentences = {
    "easy": [
        "The bright yellow sunflowers swayed gently in the cool morning breeze.",
        "Every morning, she enjoys a warm cup of coffee while watching the birds chirp.",
        "A little boy happily played with his toy train, watching it go around the track.",
        "The fresh scent of rain filled the air as tiny droplets trickled down the windowpane.",
        "Butterflies of all colors fluttered gracefully in the garden."
    ],
    "medium": [
        "Reading books is a great way to expand knowledge and explore new ideas.",
        "A balanced diet, regular exercise, and proper sleep are essential for good health.",
        "Learning a new language improves cognitive abilities and cultural experiences.",
        "Technology continues to evolve, making communication more efficient than ever.",
        "Solving a complex puzzle brings accomplishment and strengthens problem-solving skills."
    ],
    "hard": [
        "The theory of relativity fundamentally changed our understanding of space, time, and gravity.",
        "Deep learning enables machines to recognize patterns and make decisions autonomously.",
        "Exploring the mysteries of the deep ocean remains one of the greatest scientific challenges.",
        "Space missions require extensive planning, precise calculations, and advanced technology.",
        "The intricate process of DNA replication ensures genetic information is passed accurately."
    ]
}

start_time = None

def get_random_sentence(difficulty):
    return random.choice(sentences[difficulty])

def calculate_accuracy(original, typed):
    matcher = SequenceMatcher(None, original.split(), typed.split())
    return round(matcher.ratio() * 100, 2)

def start_typing(event):
    global start_time
    username = js.document.getElementById("username").value or "Guest"
    difficulty = js.document.getElementById("difficulty").value
    sentence = get_random_sentence(difficulty)

    js.document.getElementById("sentence").innerText = sentence
    js.document.getElementById("test-area").style.display = "block"
    js.document.getElementById("results").style.display = "none"

    js.localStorage.setItem("username", username)
    js.localStorage.setItem("target_sentence", sentence)

    start_time = time.time()

    # Play start sound
    js.playSound("start.mp3")

def submit_typing(event):
    global start_time
    end_time = time.time()
    typed_text = js.document.getElementById("inputText").value
    target_sentence = js.localStorage.getItem("target_sentence")
    username = js.localStorage.getItem("username")

    elapsed_time = max(end_time - start_time, 1)  # Avoid division by zero
    wpm = round(len(typed_text.split()) / (elapsed_time / 60))
    accuracy = calculate_accuracy(target_sentence, typed_text)

    # Calculate stars based on WPM and Accuracy
    if wpm >= 60 and accuracy >= 90:
        stars = 5
    elif wpm >= 50 and accuracy >= 80:
        stars = 4
    elif wpm >= 40 and accuracy >= 70:
        stars = 3
    elif wpm >= 30 and accuracy >= 60:
        stars = 2
    else:
        stars = 1

    points = (wpm * accuracy) // 10

    # Update the result area
    js.document.getElementById("stars").innerText = stars
    js.document.getElementById("points").innerText = points
    js.document.getElementById("result-details").innerText = (
        f"Username: {username}\n"
        f"Time: {round(elapsed_time, 2)} sec\n"
        f"WPM: {wpm}\n"
        f"Accuracy: {accuracy}%"
    )

    js.document.getElementById("results").style.display = "block"
    js.document.getElementById("test-area").style.display = "none"

    # Play submit sound
    js.playSound("submit.mp3")

# Attach events
js.document.getElementById("start").addEventListener("click", create_proxy(start_typing))
js.document.getElementById("submit").addEventListener("click", create_proxy(submit_typing))
