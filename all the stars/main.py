import time

lyrics_with_timing = [
    ("Finishing eight or nine?", 2.0),
    ("Tell me, what's the perfect time?", 4.4),
    ("I told you I'll be waiting", 6.7),
    ("Hiding from the rainfall", 9.2),
    ("So, tell me, what's the joy of giving if you're never pleased?", 14.0),
    ("On my last strength against you", 16.0),
    ("Baby, tell me what you need", 18.2),
    ("Young as I want to know", 19.9),
    ("I will never let you go", 23.1),
    ("Trading a baseball lover as I face the snow", 25.5),
    ("So, tell me, what's the joy of giving if you're never pleased?", 28.8),
    ("On my last strength against you", 33.5),
    ("Baby, tell me what you need", 36.2),
]

def print_timed_lyrics(lyrics_with_timing):
    start_time = time.time()
    for line, display_time in lyrics_with_timing:
        words = line.split()  
        for word in words:
            sleep_time = display_time - (time.time() - start_time)
            if sleep_time > 0:
                time.sleep(sleep_time / len(words))  
            print(word, end=" ", flush=True)
        print() 


print_timed_lyrics(lyrics_with_timing)