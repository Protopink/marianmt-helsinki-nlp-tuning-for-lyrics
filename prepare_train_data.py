# print("Grabbing OpenSubtitles data...");

# with open("fetch_opensubtitles.py") as fetch_opensubtitles:
#     exec(fetch_opensubtitles.read())

print("Grabbing LyricsTranslate data...");

with open("fetch_lyricstranslate.py") as fetch_opensubtitles:
    exec(fetch_opensubtitles.read())

print("Preparing train data...")

def clean_text(text):
    """Cleans and normalizes text for training"""
    text = re.sub(r"\s+", " ", text)  # Normalize spaces
    text = text.replace("’", "'").replace("“", '"').replace("”", '"')  # Fix punctuation
    return text.strip()

def preprocess_file(input_file, output_file):
    """Applies text cleaning to each line in the dataset"""
    with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
        for line in infile:
            outfile.write(clean_text(line) + "\n")

def combine_files(input_files, output_file):
    with open(output_file, 'w') as outfile:
        for file_name in input_files:
            with open(file_name) as infile:
                outfile.write(infile.read())
                outfile.write("\n")

combine_files(["tuning-lyricstranslate/source.txt", "tuning-opensubtitles/source.txt"], "tuning/source.txt")
combine_files(["tuning-lyricstranslate/target.txt", "tuning-opensubtitles/target.txt"], "tuning/target.txt")

preprocess_file("tuning/source.txt", "tuning/clean_source.txt")
preprocess_file("tuning/target.txt", "tuning/clean_target.txt")

print("Train data preprocessing complete! Loading dataset...")
