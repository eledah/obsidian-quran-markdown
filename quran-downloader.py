import json
from urllib.request import urlopen
import pyarabic.araby as araby

# editions http://api.alquran.cloud/v1/edition/type/translation
ar_edition = '/quran-uthmani'
fa_edition = '/fa.makarem'

# Verbose logging flag
verbose = True

def log(message):
    if verbose:
        print(message)

# consts
ENTER = '\n'
NEWLINE = ENTER + '<br>'

STYLE_BEFORE_AYAH = '<span class="ayah">'
STYLE_AFTER_AYAH = '</span>'

STYLE_BEFORE_TRANSLATION = '<span class="ayah_translation">'
STYLE_AFTER_TRANSLATION = '</span>'

output_dir = "obsidian-quran-markdown/quran/fa/"

# extracting the surah list
name = "سوره"

try:
    log("Opening surah list file for writing.")
    with open(output_dir + name + ".md", "w", encoding='utf-8') as surahFile:
        surahName = ['N/A']
        surah_url = 'http://api.alquran.cloud/v1/meta'
        log(f"Fetching surah list from {surah_url}.")
        surahurl = urlopen(surah_url)
        surahjson = json.loads(surahurl.read())
        log("Writing surah names to the file.")
        for i in range(1, 115):
            surahName.append(araby.strip_diacritics(surahjson['data']['surahs']['references'][i - 1]['name']))
            surahFile.write(str(i) + "- [[" + araby.strip_diacritics(surahjson['data']['surahs']['references'][i - 1]['name']) + "]] " + ENTER)
        surahName.append('N/A')
    log("Surah list file written successfully.")
except Exception as e:
    log(f"Error extracting surah list: {e}")

for surah in range(1, 115):
    log(f"Creating md files for surah #{surah}.")
    try:
        ar_url = 'http://api.alquran.cloud/v1/surah/' + str(surah) + ar_edition
        log(f"Fetching Arabic text for surah #{surah} from {ar_url}.")
        ar_url = urlopen(ar_url)
        ar_json = json.loads(ar_url.read())
        
        fa_url = 'http://api.alquran.cloud/v1/surah/' + str(surah) + fa_edition
        log(f"Fetching translation for surah #{surah} from {fa_url}.")
        fa_url = urlopen(fa_url)
        fa_json = json.loads(fa_url.read())
        
        if ar_json['status'] == 'OK':
            name = araby.strip_diacritics(ar_json['data']['name'])
            numberOfAyahs = ar_json['data']['numberOfAyahs']
            
            log(f"Opening file {name}.md for writing surah content.")
            with open(output_dir + name + ".md", "w", encoding='utf-8') as surahFile:
                nextSurah = surahName[surah + 1]
                prevSurah = surahName[surah - 1]

                log("Writing frontmatter to the file.")
                surahFile.write('---' + ENTER)
                surahFile.write('cssclass: quran-surah' + ENTER) 
                surahFile.write('---' + NEWLINE + ENTER) 

                log("Writing navigation links to the file.")
                surahFile.write(ENTER + "▶ [[" + prevSurah + "]] | [[" + nextSurah + "]] ◀"  + ENTER + NEWLINE + ENTER + ENTER)
                
                log(f"Writing ayahs for surah #{surah}.")
                for ayah in range(0, numberOfAyahs):
                    surahFile.write("##### " + str(ayah + 1) + ENTER + ENTER)
                    if ar_json['data']['ayahs'][ayah]['sajda']:
                        surahFile.write(STYLE_BEFORE_AYAH
                                        + ar_json['data']['ayahs'][ayah]['text']
                                        + " **سجده** "
                                        + STYLE_AFTER_AYAH
                                        + ENTER
                                        + STYLE_BEFORE_TRANSLATION
                                        + fa_json['data']['ayahs'][ayah]['text'].replace('"', '\'')
                                        + STYLE_AFTER_TRANSLATION + ENTER + ENTER
                                        )
                    else:
                        surahFile.write(STYLE_BEFORE_AYAH
                                        + ar_json['data']['ayahs'][ayah]['text']
                                        + STYLE_AFTER_AYAH
                                        + NEWLINE
                                        + STYLE_BEFORE_TRANSLATION
                                        + fa_json['data']['ayahs'][ayah]['text'].replace('"', '\'')
                                        + STYLE_AFTER_TRANSLATION + ENTER + ENTER
                                        )
            log(f"File {name}.md written successfully.")
    except Exception as e:
        log(f"Error creating file for surah {surah}: {e}")
