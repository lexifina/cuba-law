"""Cuba: Constitution of 2019 from Gaceta Oficial No. 5 Extraordinaria (born-digital PDF). Reads .cache only."""
import hashlib, json, re
from pathlib import Path
import pymupdf
here = Path(__file__).parent
URL = 'https://www.gacetaoficial.gob.cu/sites/default/files/goc-2019-ex5.pdf'
pdf = here / '.cache' / 'goc-2019-ex5.pdf'
txt = '\n'.join(p.get_text() for p in pymupdf.open(pdf))
txt = txt.replace('\xa0', ' ').replace('\t', ' ')
start = txt.index('CONSTITUCIÓN DE LA REPÚBLICA\nPREÁMBULO')
lines = []
for l in txt[start:].split('\n'):
    l = re.sub(r'\s+', ' ', l).strip()
    if not l or re.fullmatch(r'\d+|Gaceta Oficial|10 de abril de 2019|CONSTITUCIÓN|CONSTITUCIÓN DE LA REPÚBLICA|______', l):
        continue
    lines.append(l)

def paragraphs(ls):
    out, cur, was_head = [], '', False
    for l in ls:
        head = l.isupper() or re.fullmatch(r'(TÍTULO|CAPÍTULO|SECCIÓN) [A-ZÚ ]+', l)
        if not cur or head or was_head or re.match(r'^([a-zñ]|\d+)\) ', l) or (re.search(r'[.;:]$', cur) and re.match(r'^[A-ZÁÉÍÓÚ“«]', l)):
            if cur: out.append(cur)
            cur = l
        else:
            cur += ' ' + l
        was_head = bool(head)
    if cur: out.append(cur)
    return out

units, order = {}, []
key, label, kind, buf = 'preambulo', 'Preámbulo', 'preamble', []
ORD = ['PRIMERA', 'SEGUNDA', 'TERCERA', 'CUARTA', 'QUINTA', 'SEXTA', 'SÉPTIMA', 'OCTAVA', 'NOVENA', 'DÉCIMA', 'DECIMOPRIMERA', 'DECIMOSEGUNDA', 'DECIMOTERCERA']
section = None
def flush():
    global buf
    if key:
        ps = paragraphs(buf)
        units[key] = {'label': label, 'kind': kind, 'text': '# ' + label + '\n' + '\n'.join(ps) + '\n'}
    buf = []
pending = []
for l in lines:
    if l == 'PREÁMBULO':
        continue
    m = re.match(r'^ARTÍCULO (\d+)\. ?(.*)', l)
    if m:
        flush()
        n = int(m.group(1)); key, label, kind = 'art-%03d' % n, 'Artículo %d' % n, 'art'
        buf = pending + ([m.group(2)] if m.group(2) else []); pending = []
        continue
    if l in ('DISPOSICIONES ESPECIALES', 'DISPOSICIONES TRANSITORIAS', 'DISPOSICIONES FINALES'):
        flush(); key = None; section = l.split()[1].lower(); continue
    m = re.match(r'^(PRIMERA|SEGUNDA|TERCERA|CUARTA|QUINTA|SEXTA|SÉPTIMA|OCTAVA|NOVENA|DÉCIMA|DECIMOPRIMERA|DECIMOSEGUNDA|DECIMOTERCERA): ?(.*)', l)
    if m and section:
        flush(); i = ORD.index(m.group(1)) + 1
        pre = {'especiales': ('dis-especial', 'Disposición especial'), 'transitorias': ('dis-transitoria', 'Disposición transitoria'), 'finales': ('dis-final', 'Disposición final')}[section]
        key, label, kind = '%s-%02d' % (pre[0], i), '%s %s' % (pre[1], m.group(1).lower()), 'transitional' if section != 'finales' else 'final'
        buf = [m.group(2)]; continue
    # headings between articles (TÍTULO/CAPÍTULO/SECCIÓN and their names) go in front of the next article
    if (l.isupper() or re.match(r'^(TÍTULO|CAPÍTULO|SECCIÓN) ', l)) and key and (key.startswith('art-') or (key == 'preambulo' and l.startswith(('TÍTULO', 'CAPÍTULO', 'FUNDAMENTOS', 'PRINCIPIOS')))) and not l.startswith('ARTÍCULO'):
        pending.append(l) if l else None
        continue
    if pending and key and key.startswith('art-'):
        # a lowercase continuation after a heading: heading belongs to the next article, text to the current
        pass
    buf.append(l)
flush()
arts = [k for k in units if k.startswith('art-')]
assert len(arts) == 229, len(arts)
corpus = {
 'country': {'code': 'CU', 'name': 'Cuba', 'slug': 'cuba', 'lang': 'es', 'tz': 'America/Havana', 'future_branch': 'future',
   'publisher': {'name': 'Gaceta Oficial de la República de Cuba (Ministerio de Justicia)', 'email': 'goc@gacetaoficial.gob.cu.invalid'},
   'default_in_force_rule': {'text': 'Final provision Segunda: the Constitution enters into force, once proclaimed, from its publication in the Gaceta Oficial; it was proclaimed on 10 April 2019 (Gaceta Oficial No. 5 Extraordinaria, 10 April 2019).', 'source': URL},
   'licence_note': 'Official text of the Constitution of the Republic of Cuba, proclaimed 10 April 2019, from Gaceta Oficial de la República de Cuba No. 5 Extraordinaria (gacetaoficial.gob.cu). The site states no licence; official legal text reproduced for reference with attribution to the publisher.'},
 'sources': [{'name': 'Gaceta Oficial de la República de Cuba: No. 5 Extraordinaria, 10 April 2019', 'url': URL, 'retrieved': '2026-10-29', 'requests': 3,
   'licence': 'no licence stated', 'notes': 'Born-digital PDF (Adobe InDesign), text layer used as is.'}],
 'laws': {}, 'applies': [],
 'acts': [{'slug': 'constitucion', 'short': 'Constitución', 'title': 'Constitución de la República de Cuba (2019)', 'url': URL, 'first_law': None, 'earlier_laws': [],
   'versions': [{'from': '2019-04-10', 'source_url': URL, 'sha256': hashlib.sha256(pdf.read_bytes()).hexdigest(), 'units': units, 'credits': {},
     'note': 'Oldest version available: the Constitution as proclaimed and published on 10 April 2019. The Gaceta Oficial does not publish consolidated texts.'}]}],
 'decisions': ['Spanish is built: the official text is Spanish; no official English text was used.',
   'One version dated 2019-04-10, the proclamation date, which the final provision makes the in-force date.',
   'TÍTULO, CAPÍTULO and SECCIÓN headings are kept at the start of the article that follows them; line wraps in the PDF are joined into paragraphs.'],
 'ai_use': ['Claude Code wrote the parser; it did not write or alter any legal text. 0 model calls at data-build time.']}
(here / 'corpus.json').write_text(json.dumps(corpus, ensure_ascii=False, indent=1) + chr(10), encoding='utf8', newline=chr(10))
print(len(units), 'units')
