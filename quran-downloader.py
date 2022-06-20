import json
from urllib.request import urlopen
import pyarabic.araby as araby

# consts
ENTER = '\r\n'
NEWLINE = ENTER + '<br>'

STYLE_BEFORE_TRANSLATION = '<span class="ayah hovertext" data-hover=\"'
STYLE_AFTER_TRANSLATION = '\">'
STYLE_FINAL = '</span>'

# editions http://api.alquran.cloud/v1/edition/type/translation
ar_edition = '/quran-uthmani'
fa_edition = '/fa.khorramshahi'

# extracting the surah list
name = "سوره"
surahFile = open(name + ".md", "w", encoding='utf-8')

surahName = ['N/A']
surah_url = 'http://api.alquran.cloud/v1/meta'
surahurl = urlopen(surah_url)
surahjson = json.loads(surahurl.read())
for i in range(1, 115):
    surahName.append(araby.strip_diacritics(surahjson['data']['surahs']['references'][i - 1]['name']))
    surahFile.write(str(i)
                    + "- [["
                    + araby.strip_diacritics(surahjson['data']['surahs']['references'][i - 1]['name'])
                    + "]] "
                    + ENTER)
surahName.append('N/A')

for surah in range(1, 115):
    print('Creating md files for surah #' + str(surah))

    ar_url = 'http://api.alquran.cloud/v1/surah/' + str(surah) + ar_edition
    ar_url = urlopen(ar_url)
    ar_json = json.loads(ar_url.read())

    fa_url = 'http://api.alquran.cloud/v1/surah/' + str(surah) + fa_edition
    fa_url = urlopen(fa_url)
    fa_json = json.loads(fa_url.read())

    if ar_json['status'] == 'OK':
        name = araby.strip_diacritics(ar_json['data']['name'])
        revelationType = ar_json['data']['revelationType']
        numberOfAyahs = ar_json['data']['numberOfAyahs']

        surahFile = open(name + ".md", "w", encoding='utf-8')

        nextSurah = surahName[surah + 1]
        prevSurah = surahName[surah - 1]

        surahFile.write("# " + name + ENTER)
        surahFile.write("#" + revelationType + ENTER + NEWLINE)

        surahFile.write("▶ [[" + prevSurah + "]] | [[" + nextSurah + "]] ◀" + ENTER + NEWLINE + ENTER + NEWLINE)

        for ayah in range(0, numberOfAyahs):
            surahFile.write("##### " + str(ayah + 1) + ENTER)
            if ar_json['data']['ayahs'][ayah]['sajda']:
                surahFile.write(STYLE_BEFORE_TRANSLATION
                                + fa_json['data']['ayahs'][ayah]['text'].replace('"', '\'')
                                + STYLE_AFTER_TRANSLATION
                                + ar_json['data']['ayahs'][ayah]['text']
                                + " **سجده** "
                                + STYLE_FINAL
                                + ENTER
                                )
            else:
                surahFile.write(STYLE_BEFORE_TRANSLATION
                                + fa_json['data']['ayahs'][ayah]['text'].replace('"', '\'')
                                + STYLE_AFTER_TRANSLATION
                                + ar_json['data']['ayahs'][ayah]['text']
                                + STYLE_FINAL
                                + ENTER)
