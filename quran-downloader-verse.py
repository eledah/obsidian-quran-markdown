import json
from urllib.request import urlopen
import pyarabic.araby as araby
import os

# editions http://api.alquran.cloud/v1/edition/type/translation
ar_edition = '/quran-uthmani'
id_edition = '/id.indonesian'

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

output_dir = "quran-verse/"

# Create the main output directory
os.makedirs(output_dir, exist_ok=True)

# Fetch Surah metadata
surah_meta_url = 'http://api.alquran.cloud/v1/meta'
log(f"Fetching Surah metadata from {surah_meta_url}")
surah_meta_json = json.loads(urlopen(surah_meta_url).read())
surah_names = {surah['number']: surah['englishName'] for surah in surah_meta_json['data']['surahs']['references']}

for surah in range(1, 115):
    log(f"Processing Surah #{surah}")
    try:
        ar_url = f'http://api.alquran.cloud/v1/surah/{surah}{ar_edition}'
        log(f"Fetching Arabic text for Surah #{surah} from {ar_url}")
        ar_json = json.loads(urlopen(ar_url).read())
        
        id_url = f'http://api.alquran.cloud/v1/surah/{surah}{id_edition}'
        log(f"Fetching Indonesian translation for Surah #{surah} from {id_url}")
        id_json = json.loads(urlopen(id_url).read())
        
        if ar_json['status'] == 'OK':
            surah_name = str(surah).zfill(3)
            number_of_ayahs = ar_json['data']['numberOfAyahs']
            
            # Create a folder for each Surah with English name
            surah_dir = os.path.join(output_dir, f"{surah_name} - {surah_names[surah]}")
            os.makedirs(surah_dir, exist_ok=True)
            
            # Create main Surah file
            with open(os.path.join(surah_dir, f"{surah_name}.md"), "w", encoding='utf-8') as surah_file:
                log(f"Writing main file for Surah #{surah}")
                surah_file.write('---\n')
                surah_file.write('cssclass: quran-surah\n')
                surah_file.write(f'---\n\n')
                
                for ayah in range(1, number_of_ayahs + 1):
                    surah_file.write(f"![[{surah_name}-{str(ayah).zfill(3)}]]\n\n")
            
            # Create individual verse files
            for ayah in range(number_of_ayahs):
                verse_file = os.path.join(surah_dir, f"{surah_name}-{str(ayah + 1).zfill(3)}.md")
                with open(verse_file, "w", encoding='utf-8') as verse_file:
                    log(f"Writing verse file for Surah #{surah}, Ayah #{ayah + 1}")
                    verse_file.write(f"##### {ayah + 1}\n\n")
                    verse_file.write(f"{STYLE_BEFORE_AYAH}{ar_json['data']['ayahs'][ayah]['text']}{STYLE_AFTER_AYAH}\n\n")
                    verse_file.write(f"{STYLE_BEFORE_TRANSLATION}{id_json['data']['ayahs'][ayah]['text']}{STYLE_AFTER_TRANSLATION}\n")
            
            log(f"Completed processing Surah #{surah}")
    except Exception as e:
        log(f"Error processing Surah {surah}: {e}")

log("Quran download and processing complete")
