from datasets import load_dataset

dataset = load_dataset("open_subtitles", lang1="en", lang2="ru", split="train", trust_remote_code=True)

print("OpenSubtitles dataset loaded!", dataset.info)

with open("tuning/source.txt", "w", encoding="utf-8") as src, open("tuning/target.txt", "w", encoding="utf-8") as dest:
    for r in dataset:
        src.write(r["translation"]["en"] + "\n")
        dest.write(r["translation"]["ru"] + "\n")

print("OpenSubtitles dataset extracted and saved to `./tuning` folder!")
