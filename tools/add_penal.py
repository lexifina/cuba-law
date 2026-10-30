"""Cuba: Ley 151/2022 Código Penal from Gaceta Oficial No. 93 Ordinaria (born-digital PDF). Reads .cache only; adds the act to corpus.json."""
import hashlib, json, re
from pathlib import Path
import pymupdf
here = Path(__file__).parent
URL = 'https://www.gacetaoficial.gob.cu/sites/default/files/goc-2022-o93_0.pdf'
pdf = here / '.cache' / 'goc-2022-o93.pdf'
txt = '\n'.join(p.get_text() for p in pymupdf.open(pdf)).replace('\xa0', ' ').replace('\t', ' ')
lines = []
for l in txt[txt.index('POR CUANTO: La Constitución'):].split('\n'):
    l = re.sub(r'\s+', ' ', l).strip()
    if not l or re.fullmatch(r'\d{4}|GACETA OFICIAL|1ro\. de septiembre de 2022', l):
        continue
    lines.append(l)

HEAD = re.compile(r'[A-ZÁÉÍÓÚÑ0-9 ,\.\-]{3,}')
ORD = ['PRIMERA', 'SEGUNDA', 'TERCERA', 'CUARTA', 'QUINTA', 'SEXTA', 'SÉPTIMA', 'OCTAVA', 'NOVENA', 'DÉCIMA']


def isheading(l):
    return bool(HEAD.fullmatch(l))


def paragraphs(ls):
    out, cur = [], ''
    for l in ls:
        if not cur or isheading(l) or isheading(cur) or re.match(r'^(\d+\. |[a-zñ]\) |[ivx]+\) |POR CUANTO|POR TANTO|PUBLÍQUESE|DADA )', l):
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


expect = 1
for l in lines:
    if l == 'LEY No. 151' and key == 'preambulo':
        flush(); key = None; continue
    if key is None and not tail and l in ('CÓDIGO PENAL',):
        continue
    m = re.match(r'^Artículo (\d+)\.(.*)', l)
    if m and not tail and int(m.group(1)) == expect:
        flush()
        n = expect; expect += 1
        key, label, kind = 'art-%03d' % n, 'Artículo %d' % n, 'art'
        rest = m.group(2).strip()
        buf = pending + ([rest] if rest else []); pending = []
        continue
    if l == 'DISPOSICIONES ESPECIALES' and expect == 435:
        flush(); key = None; tail = True; section = 'especiales'; continue
    if l == 'DISPOSICIONES FINALES' and tail:
        flush(); key = None; section = 'finales'; continue
    if l == 'ANEXO' and tail:
        flush(); key, label, kind, section = 'anexo', 'Anexo. Definiciones de términos y expresiones', 'annex', None; continue
    m = re.match(r'^(PRIMERA|SEGUNDA|TERCERA|CUARTA|QUINTA|SEXTA|SÉPTIMA|OCTAVA|NOVENA|DÉCIMA): ?(.*)', l)
    if m and section:
        flush(); i = ORD.index(m.group(1)) + 1
        pre = {'especiales': ('dis-especial', 'Disposición especial'), 'finales': ('dis-final', 'Disposición final')}[section]
        key, label, kind = '%s-%02d' % (pre[0], i), '%s %s' % (pre[1], m.group(1).lower()), 'final'
        buf = [m.group(2)]; continue
    if not tail and isheading(l) and key != 'preambulo':
        pending.append(l); continue
    if pending and key:
        buf.extend(pending); pending = []
    buf.append(l)
flush()
assert expect == 435, expect
# trim the signature block off the last final provision
t = units['dis-final-02']['text']
c = t.find('Juan Esteban Lazo')
if c > 0:
    units['dis-final-02']['text'] = t[:c].rstrip('\n') + '\n'
sha = hashlib.sha256(pdf.read_bytes()).hexdigest()
corpus = json.loads((here / 'corpus.json').read_text(encoding='utf-8'))
corpus['laws']['ley-151-2022'] = {'label': 'Ley No. 151/2022', 'title': 'Código Penal', 'kind': 'law', 'enacted': '2022-05-15', 'published': '2022-09-01',
                                  'url': URL, 'temporary_until': None, 'restores': None, 'note': None}
corpus['acts'] = [a for a in corpus['acts'] if a['slug'] != 'codigo-penal']
corpus['acts'].append({'slug': 'codigo-penal', 'short': 'Código Penal', 'title': 'Código Penal (Ley No. 151/2022)', 'url': URL, 'first_law': 'ley-151-2022', 'earlier_laws': [],
                       'versions': [{'from': '2022-12-01', 'source_url': URL, 'sha256': sha, 'units': units, 'credits': {},
                                     'note': 'The Código Penal as approved on 15 May 2022 and published in Gaceta Oficial No. 93 Ordinaria on 1 September 2022. The Gaceta Oficial does not publish consolidated texts.'}]})
corpus['sources'] = [s for s in corpus['sources'] if 'No. 93' not in s['name']] + [{
    'name': 'Gaceta Oficial de la República de Cuba: No. 93 Ordinaria, 1 September 2022 (Ley 151/2022, Código Penal)', 'url': URL, 'retrieved': '2026-10-30',
    'licence': 'no licence stated', 'notes': 'Born-digital PDF, text layer used as is.'}]
corpus['decisions'] = [d for d in corpus['decisions'] if 'Código Penal' not in d] + [
    'Código Penal (Ley 151/2022): one version dated 2022-12-01. Final provision Segunda makes the Law enter into force ninety days after publication in the Gaceta Oficial (1 September 2022); the first day after those ninety days is 1 December 2022, the date Cuban press gave. Credited to Ley 151/2022 as the act as enacted.',
    'Código Penal: Libro, Título, Capítulo and Sección headings are kept at the start of the article that follows them; the Anexo (definitions) is its own file; the enacting formula, signatures and page headers are left out.']
(here / 'corpus.json').write_text(json.dumps(corpus, ensure_ascii=False, indent=1) + '\n', encoding='utf-8', newline='\n')
print(len(units), 'units')
