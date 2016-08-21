# House, M.C.
# (Generation of random text that sounds like Dr. House)

# Packages:
import urllib.request  # for grabbing the text off the internet
import os       # to help save the files of text
import re       # for replacement via regular expressions
import nltk     # for splitting text into words
import random   # for picking random words

# Create a directory to store episode transcripts (if it doesn't already exist):
try:
    os.mkdir('texts')
except FileExistsError:
    pass

# Get a list of transcript filenames:
with open("filenames.txt", "r") as namesfile:
    filenames = namesfile.readlines()
filenames = [name.strip('\n') for name in filenames]

 

# Store the episode transcripts locally (if they don't already exist):
# WARNING -- There are 177 files, totaling 36.2 MB.
warned = False
for name in filenames:
    if not (os.path.isfile('texts/' + name)):
        if not warned:
            print('Retrieving transcripts from every House episode ever...')
            print('(This could take several minutes!)')
            warned = True
        urllib.request.urlretrieve('http://community.livejournal.com/clinic_duty/' + name, 'texts/' + name)

print('Here comes your text...')

# Characters that will need to be removed or altered:
replacements = {
    "&rsquo;" : "'",
    "&#39;" : "",
    "&hellip;" : "...",
    "\\" : "",
    '“' : '',
    '”' : '',
    "’" : "'",
    '"' : '',
    '&lt;' : '',
    " -- " : " — ",
    " - " : " — "
}

# Extract a list of the complete text spoken by Dr. House in every episode:
episodes = []
for name in filenames:
    with open('texts/' + name, 'r', encoding="utf8") as myfile:
        data = myfile.read().replace('\n', '').split('<br />')
        data = ' '.join([
            re.sub(r'\[(.*?)\]|\<(.*?)\>|\((.*?)\)', '', line).replace('House: ', '')  # (eliminate any [text in brackets])
            for line in data 
            if line.startswith('House:')
        ])
        for key in replacements:
            data = data.replace(key, replacements[key])
        episodes.append(data)

# Join all episodes into one large text string:
alltext = ' '.join(ep for ep in episodes)

# Build the list of words used:
tokenizer = nltk.tokenize.RegexpTokenizer(r"\w+|[^\w\s]+")
stream = tokenizer.tokenize(alltext)

# Build a list of word pairs used (AKA 2-grams):
stream2 = [(stream[i], stream[i+1]) for i in range(len(stream)-1)]

# A function that takes a pair of words and randomly chooses a word to follow them:
def nextpair(pair):
    return stream2[random.choice([i for i, j in enumerate(stream2) if (j == pair) & (i < len(stream2)-2)]) + 1]

# To clean up the generated text:
replacements = {
    ' .' : '.',
    ' ,' : ',',
    " ' " : "'",
    " ?" : "?",
    " !" : "!",
    " ’ " : "’",
    " ; " : "; ",
    " ‘ " : " ‘",
    "$ " : "$",
    " …" : "...",
    " - " : "-"
}
def postprocess(text):
    for key in replacements:
        text = text.replace(key, replacements[key])
    return text

# Generate text using 2-grams:
pair = random.choice([pair for pair in stream2 if pair[0][0].isupper()])
words = [pair[0], pair[1]]
while (words[-1] != '.') & (words[-1] != '!') & (words[-1] != '?') | (len(words) < 20):
    pair = nextpair(pair)
    words.append(pair[-1])

# Show the result:
print('\nHouse M.C. says:\n"' + postprocess(' '.join(words)) + '"')

