import tkinter as tk
from tkinter import messagebox
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords

# Safe NLTK download
def safe_download(pkg):
    try:
        nltk.data.find(pkg)
    except LookupError:
        nltk.download(pkg.split('/')[-1])

safe_download('corpora/stopwords')
safe_download('sentiment/vader_lexicon')

# Initialize once (important)
STOP_WORDS = set(stopwords.words('english'))
sia = SentimentIntensityAnalyzer()

# Cleaner but VADER-friendly text cleaning
def clean_text(text):
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.lower()

    words = [w for w in text.split() if w not in STOP_WORDS]
    return " ".join(words)

def get_sentiment(text):
    cleaned = clean_text(text)
    score = sia.polarity_scores(cleaned)
    compound = score['compound']

    if compound >= 0.05:
        sentiment = "Positive"
        color = "green"
    elif compound <= -0.05:
        sentiment = "Negative"
        color = "red"
    else:
        sentiment = "Neutral"
        color = "orange"

    return sentiment, compound, color

def analyze_sentiment():
    review = review_entry.get("1.0", tk.END).strip()

    if not review:
        messagebox.showerror("Error", "Please enter a movie review.")
        return

    sentiment, score, color = get_sentiment(review)

    result_label.config(
        text=f"Sentiment: {sentiment}\nScore: {score:.3f}",
        fg=color
    )

# GUI setup
window = tk.Tk()
window.title("Sentiment Analysis App")
window.geometry("520x420")
window.configure(bg="#f2f2f2")

label = tk.Label(window, text="Enter a movie review:", font=("Arial", 14), bg="#f2f2f2")
label.pack(pady=10)

review_entry = tk.Text(window, height=8, width=55, font=("Arial", 12))
review_entry.pack(pady=10)

analyze_button = tk.Button(
    window,
    text="Analyze Sentiment",
    command=analyze_sentiment,
    font=("Arial", 14),
    bg="#4CAF50",
    fg="white"
)
analyze_button.pack(pady=10)

result_label = tk.Label(window, text="", font=("Arial", 14, "bold"), bg="#f2f2f2")
result_label.pack(pady=10)

window.mainloop()
