"""Cuba: Ley 59/1987 Código Civil, updated edition of 8 Nov 2022 on the Gaceta Oficial site (born-digital PDF). Reads .cache only; adds the act to corpus.json."""
import hashlib, json, re
from pathlib import Path
import pymupdf
here = Path(__file__).parent
URL = 'https://www.gacetaoficial.gob.cu/sites/default/files/codigo_civil_actualizado_0.pdf'
pdf = here / '.cache' / 'civil.pdf'
txt = '\n'.join(p.get_text() for p in pymupdf.open(pdf)).replace('\xa0', ' ').replace('\t', ' ')
lines = []
for l in txt[txt.index('POR CUANTO: El Código civil'):].split('\n'):
    l = re.sub(r'\s+', ' ', l).strip()
    if not l:
        continue
    lines.append(l)

HEAD = re.compile(r'[A-ZÁÉÍÓÚÑ0-9 ,\.\-]{3,}')
ORD = ['PRIMERA', 'SEGUNDA', 'TERCERA', 'CUARTA', 'QUINTA', 'SEXTA', 'SÉPTIMA', 'OCTAVA', 'NOVENA', 'DÉCIMA']


def isheading(l):
    return bool(HEAD.fullmatch(l)) and bool(re.search(r'[A-ZÁÉÍÓÚÑ]', l))


def paragraphs(ls):
    out, cur = [], ''
    for l in ls:
        if not cur or isheading(l) or isheading(cur) or re.match(r'^(\d+\. |[a-zñ]\) |[ivx]+\) |(?:DEROGAD|MODIFICAD|ADICIONAD|SUSTITUID|SUPRIMID)[A-Z]* |(?:SECCIÓN|CAPÍTULO|TÍTULO|LIBRO) [A-ZÁÉÍÓÚ]+|POR CUANTO|POR TANTO|PUBLÍQUESE|DADA )', l):
            if cur:
                out.append(cur)
            cur = l
        elif cur.endswith('-') and re.match(r'^[a-zñáéíóú]', l):
            cur = cur[:-1] + l
        else:
            cur += ' ' + l
    if cur:
        out.append(cur)
    return out


units, key, label, kind, buf, pending, section = {}, 'preambulo', 'Preámbulo', 'preamble', [], [], None
tail = False   # after the last article


def flush():
    global buf
    if key:
        assert key not in units, key
        units[key] = {'label': label, 'kind': kind, 'text': '# ' + label + '\n' + '\n'.join(paragraphs(buf)) + '\n'}
    buf = []


last = 0
title_next = False
for l in lines:
    if l == 'LEY No. 59' and key == 'preambulo':
        flush(); key = None; continue
    if key is None and not tail and l in ('CÓDIGO CIVIL',):
        continue
    m = re.match(r'^ARTÍCULOS (\d+) a (\d+) \((Derogados)\)', l)
    if m and not tail and int(m.group(1)) > last:
        flush()
        key, label, kind = 'art-%03d-%03d' % (int(m.group(1)), int(m.group(2))), 'Artículos %s a %s' % (m.group(1), m.group(2)), 'art'
        last = int(m.group(2))
        buf = pending + ['(Derogados)']; pending = []
        continue
    m = re.match(r'^ARTÍCULO (\d+)(?:\.| )\s*(bis\.)?\s*(.*)', l)
    if m and not tail and (last < int(m.group(1)) <= last + 20 or (m.group(2) and int(m.group(1)) == last)):
        flush()
        n = int(m.group(1)); last = n
        bis = bool(m.group(2))
        key, label, kind = ('art-%03d-bis' if bis else 'art-%03d') % n, 'Artículo %d%s' % (n, ' bis' if bis else ''), 'art'
        rest = m.group(3).strip()
        if l.startswith('ARTÍCULO %d ' % n) and rest[:2] == '1.':
            pass
        buf = pending + ([rest] if rest else []); pending = []
        title_next = False
        continue
    if l == 'DISPOSICIONES ESPECIALES' and last == 547:
        flush(); key = None; tail = True; section = 'especiales'; continue
    if l == 'DISPOSICIONES TRANSITORIAS' and tail:
        flush(); key = None; section = 'transitorias'; continue
    if l == 'DISPOSICIONES FINALES' and tail:
        flush(); key = None; section = 'finales'; continue
    m = re.match(r'^(PRIMERA|SEGUNDA|TERCERA|CUARTA|QUINTA|SEXTA|SÉPTIMA|OCTAVA|NOVENA|DÉCIMA): ?(.*)', l)
    if m and section:
        flush(); i = ORD.index(m.group(1)) + 1
        pre = {'especiales': ('dis-especial', 'Disposición especial'), 'transitorias': ('dis-transitoria', 'Disposición transitoria'), 'finales': ('dis-final', 'Disposición final')}[section]
        key, label, kind = '%s-%02d' % (pre[0], i), '%s %s' % (pre[1], m.group(1).lower()), 'final'
        buf = [m.group(2)]; continue
    if not tail and key != 'preambulo' and (isheading(l) or title_next):
        pending.append(l); title_next = bool(re.match(r'^(LIBRO|T[ÍI]TULO|CAP[ÍI]TULO|SECCI[ÓO]N) ', l)) and not title_next; continue
    if pending and key:
        buf.extend(pending); pending = []
    buf.append(l)
flush()
assert last == 547, last
t = units['dis-final-03']['text']
c = t.find('Flavio Bravo')
if c > 0:
    units['dis-final-03']['text'] = t[:c].rstrip(chr(10)) + chr(10)
sha = hashlib.sha256(pdf.read_bytes()).hexdigest()
corpus = json.loads((here / 'corpus.json').read_text(encoding='utf-8'))
corpus['laws']['ley-59-1987'] = {'label': 'Ley No. 59/1987', 'title': 'Código Civil', 'kind': 'law', 'enacted': '1987-07-16', 'published': '1987-10-15',
                                 'url': URL, 'temporary_until': None, 'restores': None, 'note': None}
corpus['acts'] = [a for a in corpus['acts'] if a['slug'] != 'codigo-civil']
corpus['acts'].append({'slug': 'codigo-civil', 'short': 'Código Civil', 'title': 'Código Civil (Ley No. 59/1987), versión actualizada', 'url': URL, 'first_law': None, 'earlier_laws': ['ley-59-1987'],
                       'versions': [{'from': '2022-11-08', 'source_url': URL, 'sha256': sha, 'units': units, 'credits': {},
                                     'note': 'Oldest version available: the updated edition of the Código Civil that the Gaceta Oficial site publishes, current to 8 November 2022 (it incorporates the Constitution of 2019, the Código de las Familias and the later decree-laws listed on its first page).'}]})
corpus['sources'] = [s for s in corpus['sources'] if 'Código Civil' not in s['name']] + [{
    'name': 'Gaceta Oficial de la República de Cuba: Ley No. 59 Código Civil, versión actualizada al 8 de noviembre de 2022', 'url': URL, 'retrieved': '2026-10-30',
    'licence': 'no licence stated', 'notes': 'Born-digital PDF, text layer used as is.'}]
corpus['decisions'] = [d for d in corpus['decisions'] if 'Código Civil' not in d] + [
    'Código Civil: the Gaceta Oficial site publishes only an updated edition, current to 8 November 2022; it is recorded as one version dated 2022-11-08, the oldest version available, with the 1987 law as an earlier law. Earlier consolidated texts are not online. Notes in the edition on derogated or modified provisions are kept.',
    'Código Civil: Libro, Título, Capítulo and Sección headings are kept at the start of the article that follows them; Artículos 542 a 544 (repealed) are one file; page headers are left out.']
(here / 'corpus.json').write_text(json.dumps(corpus, ensure_ascii=False, indent=1) + chr(10), encoding='utf-8', newline=chr(10))
print(len(units), 'units')
