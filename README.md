# MarianMT Helsinki-NLP

Example is based on `Helsinki-NLP/opus-mt-en-ru` model. We geather date from OpenSubtitles dataset and LyricsTranslate website to improve song lyrics translation from English to Russian.

## Setup

```bash
conda create -n env_pytorch python=3.8
conda activate env_pytorch
conda install torchvision transformers sentencepiece tqdm requests beautifulsoup4 bs4
```

## Usage

```bash
# Prepare train data
python3 prepare_train_data.py
# Fine-tune model
python3 fine_tune.py
# Translate all files in `input` folder
python3 translate.py
```

## Useful links

* [ChatGPT conversation](https://chatgpt.com/share/679bd2b4-0d4c-800f-9792-b9fe727e15a6)
* [Fine-tune train data from OpenSiubtitles and LyricsTranslate](https://drive.google.com/file/d/1UQzTR0R5ORymVsLrjwHTqXXHgWJfPgXT/view?usp=drive_link)
