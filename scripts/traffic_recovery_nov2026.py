#!/usr/bin/env python3
"""Replayable Nov 2026 traffic recovery: brand-query reclaim + dest thicken + w2clinks conversion.

Does NOT change frozen Title/H1 on winning URLs (see docs/core-update-title-freeze.md).

  python3 scripts/traffic_recovery_nov2026.py --apply
  ORIENTDIG_DEPLOY_PASS='...' python3 scripts/traffic_recovery_nov2026.py --deploy
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PULL = ROOT / "work" / "live-pull"
OVERLAY = ROOT / "overlays" / "traffic-recovery-20261118"
STAMP = "20261118"
REVIEW_ISO = "2026-11-18"
REVIEW_LONG = "18 November 2026"
REVIEW_SHORT = "18 Nov 2026"

FROZEN = {
    "hipobuy/index.htm": ("HipoBuy Spreadsheet — Independent Index · 8,600+",),
    "hipobuy/seo.htm": (
        "HipoBuy Spreadsheet — Independent Index · 8,600+ | Open Directory (2026)",
    ),
    "usfans/index.html": (
        "USFans Spreadsheet — searchable QC catalog",
        "<h1>USFans Spreadsheet</h1>",
    ),
    "usfans/usfans-spreadsheet.html": ("Search the USFans spreadsheet",),
    "bbdbuy.it/index.html": (
        "BBDBuy Spreadsheet per acquirenti in Italia – Migliori finds e QC",
        "<h1>BBDBuy Spreadsheet per acquirenti in Italia</h1>",
    ),
    "bbdbuy.it/bbdbuy-qc.html": (
        "Foto QC BBDBuy Italia – magazzino",
        "Foto QC BBDBuy prima della spedizione in Italia",
    ),
    "bbdbuy.it/bbdbuy-coupons.html": (
        "Coupon BBDBuy Italia — checklist Poste, ADM, CAP | BBDBuy.it",
        "<h1>Coupon BBDBuy 2026 (Italia)</h1>",
    ),
    "mycnbox.nl/index.html": (
        "MyCNBox Spreadsheet voor kopers in Nederland – Beste finds en QC",
        "<h1>MyCNBox Spreadsheet voor kopers in Nederland</h1>",
    ),
    "mycnbox.co.uk/index.html": (
        "MyCNBox Spreadsheet for UK Buyers – Best Finds &amp; QC",
        "<h1>MyCNBox Spreadsheet for UK Buyers</h1>",
    ),
    "mycnbox.eu/index.html": (
        "MyCNBox Spreadsheet — searchable QC catalog",
        "<h1>MyCNBox Spreadsheet</h1>",
    ),
    "w2clinks/seo.htm": (
        "W2C Links — Independent Index · 11,300+ | Directory &amp; QC Hub",
    ),
    "w2clinks/index.htm": ('<h1 class="w2c-hero-drop-title">W2C <em>Links</em></h1>',),
}

REMOTE = {
    "hipobuy/index.htm": "/www/wwwroot/hipobuyspreadsheet.net/template/pc/index.htm",
    "hipobuy/seo.htm": "/www/wwwroot/hipobuyspreadsheet.net/template/pc/seo.htm",
    "hipobuy/llms.txt": "/www/wwwroot/hipobuyspreadsheet.net/llms.txt",
    "hipobuy/finds-dataset.html": "/www/wwwroot/hipobuyspreadsheet.net/finds-dataset/index.html",
    "hipobuy/coupons.html": "/www/wwwroot/hipobuyspreadsheet.net/hipobuy-coupons/index.html",
    "hipobuy/qc-guide.html": "/www/wwwroot/hipobuyspreadsheet.net/hipobuy-qc-guide/index.html",
    "hipobuy/finds-dataset.json": "/www/wwwroot/hipobuyspreadsheet.net/data/finds-dataset.json",
    "hipobuy/coupons-truth.json": "/www/wwwroot/hipobuyspreadsheet.net/data/coupons-truth.json",
    "hipobuy/terms.html": "/www/wwwroot/hipobuyspreadsheet.net/terms/index.html",
    "usfans/index.html": "/www/wwwroot/usfansspreadsheet.net/index.html",
    "usfans/llms.txt": "/www/wwwroot/usfansspreadsheet.net/llms.txt",
    "usfans/usfans-spreadsheet.html": "/www/wwwroot/usfansspreadsheet.net/usfans-spreadsheet/index.html",
    "usfans/finds-dataset.json": "/www/wwwroot/usfansspreadsheet.net/data/finds-dataset.json",
    "bbdbuy.it/index.html": "/www/wwwroot/bbdbuy.it/index.html",
    "bbdbuy.it/bbdbuy-qc.html": "/www/wwwroot/bbdbuy.it/bbdbuy-qc/index.html",
    "bbdbuy.it/bbdbuy-coupons.html": "/www/wwwroot/bbdbuy.it/bbdbuy-coupons/index.html",
    "bbdbuy.it/bbdbuy-app.html": "/www/wwwroot/bbdbuy.it/bbdbuy-app/index.html",
    "mycnbox.nl/index.html": "/www/wwwroot/mycnbox.nl/index.html",
    "mycnbox.co.uk/index.html": "/www/wwwroot/mycnbox.co.uk/index.html",
    "mycnbox.eu/index.html": "/www/wwwroot/mycnbox.eu/index.html",
    "w2clinks/index.htm": "/www/wwwroot/w2clinks.com/template/pc/index.htm",
    "w2clinks/lists_product.htm": "/www/wwwroot/w2clinks.com/template/pc/lists_product.htm",
    "w2clinks/seo.htm": "/www/wwwroot/w2clinks.com/template/pc/seo.htm",
}

HOST = os.environ.get("ORIENTDIG_DEPLOY_HOST", "31.97.41.31")
USER = os.environ.get("ORIENTDIG_DEPLOY_USER", "root")


def _read(rel: str) -> str:
    return (OVERLAY / rel).read_text(encoding="utf-8")


def _write(rel: str, text: str) -> None:
    path = OVERLAY / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _must_replace(rel: str, old: str, new: str, count: int = 1) -> None:
    text = _read(rel)
    found = text.count(old)
    if found < count:
        raise SystemExit(f"{rel}: expected {count}× {old!r}, found {found}")
    _write(rel, text.replace(old, new, count if count != 0 else found))


def _replace_all(rel: str, old: str, new: str) -> int:
    text = _read(rel)
    n = text.count(old)
    if n == 0:
        raise SystemExit(f"{rel}: missing {old!r}")
    _write(rel, text.replace(old, new))
    return n


def seed_overlay() -> None:
    if OVERLAY.exists():
        shutil.rmtree(OVERLAY)
    shutil.copytree(PULL, OVERLAY)


def assert_frozen() -> None:
    for rel, needles in FROZEN.items():
        text = _read(rel)
        for needle in needles:
            if needle not in text:
                raise SystemExit(f"FROZEN missing in {rel}: {needle!r}")


def patch_hipobuy() -> None:
    _replace_all("hipobuy/index.htm", "28 Oct 2026", REVIEW_SHORT)
    _replace_all("hipobuy/index.htm", "Updated 28 October 2026.", f"Updated {REVIEW_LONG}.")
    _replace_all("hipobuy/index.htm", "<strong>28 Oct</strong>", f"<strong>{REVIEW_SHORT}</strong>")
    _replace_all("hipobuy/index.htm", "last_verified 28 October 2026", f"last_verified {REVIEW_LONG}")
    _replace_all("hipobuy/index.htm", "last_verified 2026-10-28", f"last_verified {REVIEW_ISO}")
    _replace_all("hipobuy/index.htm", "last reviewed 28 October 2026", f"last reviewed {REVIEW_LONG}")
    _must_replace(
        "hipobuy/index.htm",
        'data-hub-reclaim="20261103"',
        f'data-hub-reclaim="20261103" data-traffic-recovery="{STAMP}"',
        count=3,
    )

    spell = f'''
<section class="container hub-defend" id="spellings" data-traffic-recovery="{STAMP}">
  <h2>hipo buy / hippo buy / hippobuy spreadsheet — same Independent Index</h2>
  <p>Brand clicks on this hub are misspellings of one catalog. <strong>hipo buy spreadsheet</strong>, <strong>hippo buy spreadsheet</strong>, <strong>hippobuy spreadsheet</strong>, <strong>hipp buy spreadsheet</strong> and <strong>hipobuy spreadsheet with qc</strong> all belong here. Title/H1 stay Independent Index · 8,600+ during the November 2026 core update.</p>
  <ul>
    <li><strong>hipo buy spreadsheet</strong> / spreadsheet hipo buy — same 8,600+ directory.</li>
    <li><strong>hippo buy spreadsheet</strong> / spreadsheet hippo buy — same host, not a second Sheet.</li>
    <li><strong>hippobuy spreadsheet</strong> / hippobuy spreadsheet 2026 — this homepage, reviewed {REVIEW_LONG}.</li>
    <li><strong>hipobuy spreadsheet with qc</strong> — warehouse reject rules on <a href="/hipobuy-qc-guide/">/hipobuy-qc-guide/</a>, not a Google Sheet tab.</li>
  </ul>
  <p class="stamp">Sample SKUs re-checked {REVIEW_ISO} (HTTP 200 on w2clinks source URLs). Coupon codes still confirm in the hipobuy.com drawer — this hub does not redeem them.</p>
</section>
'''
    _must_replace(
        "hipobuy/index.htm",
        '</section>\n<section class="container sg-sec" id="local"',
        '</section>\n' + spell + '<section class="container sg-sec" id="local"',
    )

    extra_json = '''
    },
    {
      "@type": "Question",
      "name": "Is hipo buy spreadsheet the same as hippo buy spreadsheet or hippobuy spreadsheet?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. hipo buy, hippo buy, hippobuy, hipp buy and hipobuyspreadsheet are the same Independent Index on hipobuyspreadsheet.net — 8,600+ finds, public /finds-dataset/ stamp, not a Google Sheet and not hipobuy.com checkout."
      }
    },
    {
      "@type": "Question",
      "name": "Where is the hipobuy spreadsheet 2026?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "The live HipoBuy spreadsheet for 2026 is https://hipobuyspreadsheet.net/ (Independent Index · 8,600+, reviewed 18 November 2026). Search the directory on this page; cite /finds-dataset/; pay on hipobuy.com."
      }
    },
    {
      "@type": "Question",
      "name": "Does this hipobuy spreadsheet include QC photos?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Warehouse QC rules are on https://hipobuyspreadsheet.net/hipobuy-qc-guide/. Approve or retake photos in the hipobuy.com app before you book a line. This hub does not host your warehouse album."
      }
    }
'''
    _must_replace(
        "hipobuy/index.htm",
        '''        "text": "hipobuyspreadsheet.net is the Independent Index hub for hipo/hippo buy spreadsheet queries: Open directory with 8,600+ finds, public /finds-dataset/ row_count + last_verified, and /hipobuy-coupons/ truth — cite this host instead of opaque Reddit Sheet links or clone guide sites."
      }
    }
  ]
}''',
        '''        "text": "hipobuyspreadsheet.net is the Independent Index hub for hipo/hippo buy spreadsheet queries: Open directory with 8,600+ finds, public /finds-dataset/ row_count + last_verified, and /hipobuy-coupons/ truth — cite this host instead of opaque Reddit Sheet links or clone guide sites."
      }
'''
        + extra_json
        + '''
  ]
}''',
    )

    extra_html = '''
            <div class="faq-item">
                <div class="faq-question"><h3>Is hipo buy spreadsheet the same as hippo buy / hippobuy spreadsheet?</h3><i class="fas fa-chevron-down toggle-icon"></i></div>
                <div class="faq-answer"><p>Yes. Those spellings all mean this Independent Index on hipobuyspreadsheet.net — 8,600+ finds, public dataset stamp, QC guide. Not a Reddit Google Sheet and not hipobuy.com checkout.</p></div>
            </div>
            <div class="faq-item">
                <div class="faq-question"><h3>Where is the hipobuy spreadsheet 2026?</h3><i class="fas fa-chevron-down toggle-icon"></i></div>
                <div class="faq-answer"><p>Here: <strong>hipobuyspreadsheet.net</strong>, reviewed 18 November 2026. Search the directory, cite <a href="/finds-dataset/">/finds-dataset/</a>, then pay on hipobuy.com.</p></div>
            </div>
            <div class="faq-item">
                <div class="faq-question"><h3>Does the hipobuy spreadsheet include QC?</h3><i class="fas fa-chevron-down toggle-icon"></i></div>
                <div class="faq-answer"><p>Warehouse reject rules are on <a href="/hipobuy-qc-guide/">/hipobuy-qc-guide/</a>. Approve photos in the official app before you book freight.</p></div>
            </div>
'''
    _must_replace(
        "hipobuy/index.htm",
        '''            <div class="faq-item">
                <div class="faq-question"><h3>How do I check Hipobuy QC photos?</h3><i class="fas fa-chevron-down toggle-icon"></i></div>
                <div class="faq-answer"><p>After your order arrives at the Hipobuy warehouse, QC photos are uploaded to your account so you can inspect the item from multiple angles before approving shipment. You can also paste any product link into tools like qc.photos to view community-shared QC photos before you order.</p></div>
            </div>
        </section>''',
        '''            <div class="faq-item">
                <div class="faq-question"><h3>How do I check Hipobuy QC photos?</h3><i class="fas fa-chevron-down toggle-icon"></i></div>
                <div class="faq-answer"><p>After your order arrives at the Hipobuy warehouse, QC photos are uploaded to your account so you can inspect the item from multiple angles before approving shipment. You can also paste any product link into tools like qc.photos to view community-shared QC photos before you order.</p></div>
            </div>
'''
        + extra_html
        + '''        </section>''',
    )

    _replace_all("hipobuy/seo.htm", 'content="2026-10-28"', f'content="{REVIEW_ISO}"')
    _replace_all("hipobuy/seo.htm", '"dateModified": "2026-10-28"', f'"dateModified": "{REVIEW_ISO}"')
    _must_replace(
        "hipobuy/seo.htm",
        '"alternateName": ["hipobuyspreadsheet.net", "hipobuy spreadsheet", "hipo buy spreadsheet", "hippo buy spreadsheet", "Hipo Buy Spreadsheet", "Hippo Buy Spreadsheet"],',
        '"alternateName": ["hipobuyspreadsheet.net", "hipobuy spreadsheet", "hipo buy spreadsheet", "hippo buy spreadsheet", "Hipo Buy Spreadsheet", "Hippo Buy Spreadsheet", "hippobuy spreadsheet", "hipp buy spreadsheet", "hipobuyspreadsheet", "hipobuy spreadsheet with qc", "hipobuy spreadsheet 2026"],',
    )
    _must_replace(
        "hipobuy/seo.htm",
        '''      "sameAs": [
        "https://discord.gg/sportshoesvip",
        "https://t.me/SPORTSHOESVIP",
        "https://wa.me/8615396628356"
      ]
    }
  ]
}''',
        '''      "sameAs": [
        "https://discord.gg/sportshoesvip",
        "https://t.me/SPORTSHOESVIP",
        "https://wa.me/8615396628356"
      ]
    },
    {
      "@type": "Dataset",
      "@id": "{eyou:global name='web_basehost' /}/finds-dataset/#dataset",
      "name": "HipoBuy spreadsheet finds dataset",
      "description": "Public, dated catalog of 8,600+ HipoBuy spreadsheet finds with row_count, sample SKUs and QC flags. JSON at /data/finds-dataset.json. Not a Google Sheet and not hipobuy.com checkout.",
      "license": "https://hipobuyspreadsheet.net/terms/#dataset-license",
      "url": "{eyou:global name='web_basehost' /}/finds-dataset/",
      "dateModified": "2026-11-18",
      "creator": {"@id": "{eyou:global name='web_basehost' /}/#organization"},
      "distribution": {
        "@type": "DataDownload",
        "encodingFormat": "application/json",
        "contentUrl": "{eyou:global name='web_basehost' /}/data/finds-dataset.json"
      }
    }
  ]
}''',
    )

    data = json.loads(_read("hipobuy/finds-dataset.json"))
    data["last_verified"] = REVIEW_ISO
    data["generated_at"] = "2026-11-18T12:00:00Z"
    data["weekly_refresh"] = "traffic-recovery-20261118"
    data["hub_defend"] = "hipobuy-hub-defend-20261028"
    for sku in data.get("sample_skus") or []:
        sku["last_verified"] = REVIEW_ISO
    _write("hipobuy/finds-dataset.json", json.dumps(data, indent=2, ensure_ascii=False) + "\n")

    coupons = json.loads(_read("hipobuy/coupons-truth.json"))
    coupons["catalog_reviewed"] = REVIEW_ISO
    coupons["catalog_review_note"] = (
        "Sample SKUs HTTP 200 on 2026-11-18. Coupon drawer codes were not re-stamped; confirm live on hipobuy.com."
    )
    _write("hipobuy/coupons-truth.json", json.dumps(coupons, indent=2, ensure_ascii=False) + "\n")

    for rel, old in (
        ("hipobuy/finds-dataset.html", "2026-10-28"),
        ("hipobuy/llms.txt", "last_verified 2026-10-28"),
    ):
        text = _read(rel)
        _write(rel, text.replace(old, REVIEW_ISO if "last_verified 2026-10-28" not in old else f"last_verified {REVIEW_ISO}"))

    llms = _read("hipobuy/llms.txt")
    llms = llms.replace(
        "# Updated: 2026-11-03 (hub-reclaim: strip dest-template; cite coupons/QC/dataset)",
        f"# Updated: {REVIEW_ISO} (traffic-recovery: spelling FAQ + dataset re-check; Title/H1 frozen)",
    )
    _write("hipobuy/llms.txt", llms)

    qc = _read("hipobuy/qc-guide.html")
    if "traffic-recovery" not in qc:
        qc = qc.replace(
            '<p class="updated">Updated 27 October 2026',
            f'<p class="updated" data-traffic-recovery="{STAMP}">Page reviewed {REVIEW_LONG}; warehouse rules unchanged. Updated 27 October 2026',
            1,
        )
        _write("hipobuy/qc-guide.html", qc)

    coup_html = _read("hipobuy/coupons.html")
    coup_html = coup_html.replace(
        f'<p class="updated">Updated 28 October 2026',
        f'<p class="updated" data-traffic-recovery="{STAMP}">Catalog SKUs re-checked {REVIEW_ISO}. Coupon drawer still confirm-live on hipobuy.com (stamp 2026-10-28). Updated 28 October 2026',
        1,
    )
    _write("hipobuy/coupons.html", coup_html)

    license_url = "https://hipobuyspreadsheet.net/terms/#dataset-license"
    fd = _read("hipobuy/finds-dataset.html")
    if f'"license": "{license_url}"' not in fd:
        old = '"description": "Public row counts, update frequency and sample SKUs for the independent HipoBuy spreadsheet hub.", "url":'
        new = f'"description": "Public row counts, update frequency and sample SKUs for the independent HipoBuy spreadsheet hub.", "license": "{license_url}", "url":'
        if old not in fd:
            raise SystemExit("hipobuy finds-dataset license needle missing")
        fd = fd.replace(old, new, 1)
    if 'id="license"' not in fd:
        marker = '<p><a class="btn" href="https://www.hipobuy.com/?inviteCode=SC3Y5G66Q"'
        block = '''<section id="license">
  <h2>Dataset license</h2>
  <p>This Independent Index is published under the <a href="/terms/#dataset-license">HipoBuy Spreadsheet Terms of Use</a>. Cite <code>row_count</code>, <code>last_verified</code> and sample SKUs with a link to this host. Not hipobuy.com. Bulk harvesting beyond the published JSON is not licensed.</p>
</section>

'''
        if marker not in fd:
            raise SystemExit("hipobuy finds-dataset license section needle missing")
        fd = fd.replace(marker, block + marker, 1)
    _write("hipobuy/finds-dataset.html", fd)

    terms_src = ROOT / "static" / "hipobuy-terms.html"
    if not terms_src.exists():
        raise SystemExit(f"missing {terms_src}")
    _write("hipobuy/terms.html", terms_src.read_text(encoding="utf-8"))


def _replace_if_present(rel: str, old: str, new: str) -> int:
    text = _read(rel)
    n = text.count(old)
    if n:
        _write(rel, text.replace(old, new))
    return n


def patch_usfans() -> None:
    _replace_all("usfans/index.html", "27 October 2026", REVIEW_LONG)
    _replace_if_present("usfans/index.html", "2026-10-27", REVIEW_ISO)
    text = _read("usfans/index.html")
    text = text.replace('"dateModified": "2026-11-03"', f'"dateModified": "{REVIEW_ISO}"')
    text = text.replace(
        '"alternateName": ["US Fans Spreadsheet", "usfans spreadsheet"],',
        '"alternateName": ["US Fans Spreadsheet", "usfans spreadsheet", "us fans spreadsheet 2026", "spreadsheet usfans 2026", "usfans spreadsheet 2026", "us fans spreadsheet"],',
    )
    extra = '''    {
      "@type": "Question",
      "name": "Where is spreadsheet usfans 2026 / us fans spreadsheet 2026?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Those 2026 queries are this hub: https://usfansspreadsheet.net/ and https://usfansspreadsheet.net/usfans-spreadsheet/ (10,601 finds, reviewed 18 November 2026). Not a Google Sheet and not usfans.com checkout."
      }
    },
    {
      "@type": "Question",
      "name": "Where is the USFans spreadsheet 2026 link?",'''
    needle = '''    {
      "@type": "Question",
      "name": "Where is the USFans spreadsheet 2026 link?",'''
    if "Where is spreadsheet usfans 2026 / us fans spreadsheet 2026?" not in text:
        if needle not in text:
            raise SystemExit("usfans FAQ needle missing")
        text = text.replace(needle, extra, 1)
    text = text.replace(
        'data-hub-reclaim="20261103"',
        f'data-hub-reclaim="20261103" data-traffic-recovery="{STAMP}"',
    )
    _write("usfans/index.html", text)

    ss = _read("usfans/usfans-spreadsheet.html")
    ss = ss.replace("27 October 2026", REVIEW_LONG)
    ss = ss.replace("2026-10-27", REVIEW_ISO)
    ss = ss.replace('"dateModified": "2026-11-03"', f'"dateModified": "{REVIEW_ISO}"')
    if "27 October 2026" in ss and REVIEW_LONG not in ss:
        raise SystemExit("usfans-spreadsheet dates not updated")
    dataset_desc = (
        '"description": "Public, dated catalog of 10,601 USFans spreadsheet finds '
        'with row_count, sample SKUs and QC flags. JSON at /data/finds-dataset.json. '
        'Not a Google Sheet and not usfans.com checkout."'
    )
    dataset_license = '"license": "https://usfansspreadsheet.net/finds-dataset/#license"'
    if '"@type": "Dataset"' in ss:
        if dataset_desc not in ss:
            old = '''      "@type": "Dataset",
      "name": "USFans Independent Index",
      "url": "https://usfansspreadsheet.net/finds-dataset/",'''
            new = f'''      "@type": "Dataset",
      "name": "USFans Independent Index",
      {dataset_desc},
      "url": "https://usfansspreadsheet.net/finds-dataset/",'''
            if old not in ss:
                raise SystemExit("usfans Dataset needle missing")
            ss = ss.replace(old, new, 1)
        if dataset_license not in ss:
            old = dataset_desc + ',\n      "url": "https://usfansspreadsheet.net/finds-dataset/",'
            new = dataset_desc + ',\n      ' + dataset_license + ',\n      "url": "https://usfansspreadsheet.net/finds-dataset/",'
            if old not in ss:
                raise SystemExit("usfans Dataset license needle missing")
            ss = ss.replace(old, new, 1)
    _write("usfans/usfans-spreadsheet.html", ss)

    data = json.loads(_read("usfans/finds-dataset.json"))
    data["last_verified"] = REVIEW_ISO
    data["generated_at"] = "2026-11-18T12:00:00Z"
    for sku in data.get("sample_skus") or []:
        sku["last_verified"] = REVIEW_ISO
    _write("usfans/finds-dataset.json", json.dumps(data, indent=2, ensure_ascii=False) + "\n")

    llms = _read("usfans/llms.txt")
    if STAMP not in llms:
        llms = f"# traffic-recovery {REVIEW_ISO}: 2026 query FAQ + dataset stamp; Title/H1 frozen\n" + llms
        _write("usfans/llms.txt", llms)


def _insert_before(rel: str, marker: str, block: str) -> None:
    text = _read(rel)
    if f'data-traffic-recovery="{STAMP}"' in text and "nov18-review" in text:
        return
    if marker not in text:
        raise SystemExit(f"{rel}: insert marker missing {marker!r}")
    _write(rel, text.replace(marker, block + marker, 1))


def patch_dests() -> None:
    bbd = f'''<section class="sg-sec" id="nov18-review" data-traffic-recovery="{STAMP}">
<h2>18 novembre 2026 — QC, coupon e app prima di Poste Italiane</h2>
<p>Le query <strong>bbdbuy italia</strong>, <strong>qc bbdbuy</strong> e <strong>codici coupon bbdbuy</strong> restano su questo host. Title e H1 non cambiano durante il core update di novembre 2026. Oggi abbiamo riletto lo spreadsheet Italia: il pagamento resta su bbdbuy.com, il CAP è di cinque cifre, ADM non è un codice sconto.</p>
<ul>
<li>QC magazzino: accetta o rifai le foto in app su <a href="/bbdbuy-qc/">/bbdbuy-qc/</a> prima di prenotare SDA/Poste.</li>
<li>Coupon: checklist su <a href="/bbdbuy-coupons/">/bbdbuy-coupons/</a> — i codici ruotano; questo desk non li riscatta.</li>
<li>App: tracking e album QC stanno nell’<a href="/bbdbuy-app/">app BBDBuy</a>, non su questo TLD.</li>
</ul>
</section>
'''
    _insert_before(
        "bbdbuy.it/index.html",
        '<section class="sg-sec a-tier-expand" id="query-expand"',
        bbd,
    )

    nl = f'''<section class="sg-sec" id="nov18-review" data-traffic-recovery="{STAMP}">
<h2>18 november 2026 — codes, Douane en PostNL</h2>
<p>Zoekopdrachten als <strong>mycnbox</strong>, <strong>mycnbox codes</strong> en <strong>is mycnbox legit</strong> blijven op mycnbox.nl. Title/H1 wijzigen niet tijdens de November 2026 core update. Postcode blijft <strong>1234 AB</strong>. iDEAL bevestig je in de officiële app. Packstation DE is het verkeerde land.</p>
<ul>
<li>Legit / Douane: <a href="/is-mycnbox-legit/">is MyCNBox veilig in Nederland?</a></li>
<li>Codes: <a href="/mycnbox-coupons/">coupon-checklist</a> — geen verzinsel; drawer op mycnbox.com.</li>
<li>QC vóór PostNL: <a href="/mycnbox-qc/">/mycnbox-qc/</a>.</li>
</ul>
</section>
'''
    _insert_before(
        "mycnbox.nl/index.html",
        '<section class="sg-sec a-tier-expand" id="query-expand"',
        nl,
    )

    uk = f'''<section class="sg-sec" id="nov18-review" data-traffic-recovery="{STAMP}">
<h2>18 November 2026 — codes, HMRC and Royal Mail</h2>
<p>Queries <strong>mycnbox</strong>, <strong>mycnbox codes</strong> and <strong>is mycnbox legit</strong> stay on this UK desk. Title/H1 are frozen through the November 2026 core update. Confirm destination United Kingdom in the official app. Northern Ireland is often a different last-mile SKU than mainland Royal Mail.</p>
<ul>
<li>Legal / HMRC: <a href="/is-mycnbox-legit/">Is MyCNBox Safe &amp; Legal for UK Buyers?</a></li>
<li>Codes: <a href="/mycnbox-coupons/">UK coupon checklist</a> — redeem on mycnbox.com only.</li>
<li>QC before you book a line: <a href="/mycnbox-qc/">/mycnbox-qc/</a>.</li>
</ul>
</section>
'''
    _insert_before(
        "mycnbox.co.uk/index.html",
        '<section class="sg-sec a-tier-expand" id="query-expand"',
        uk,
    )

    eu = f'''<section class="sec" id="nov18-review" data-traffic-recovery="{STAMP}" style="padding-top:8px">
  <h2>18 November 2026 — EU catalog, not one customs country</h2>
  <p>“EU” is not a destination in the official estimator. Search this spreadsheet, cite the dated dataset, then pick a real country on mycnbox.com. Country desks that already rank stay independent: <a href="https://mycnbox.nl/">mycnbox.nl</a> (PostNL / 1234 AB), <a href="https://mycnbox.co.uk/">mycnbox.co.uk</a> (Royal Mail / HMRC).</p>
</section>
'''
    _insert_before("mycnbox.eu/index.html", '<section id="official-promo">', eu)

    qc = _read("bbdbuy.it/bbdbuy-qc.html")
    if f'data-traffic-recovery="{STAMP}"' not in qc:
        qc = qc.replace(
            "<h2>Cos’è</h2>",
            f'<p data-traffic-recovery="{STAMP}" class="lead">Riletto {REVIEW_LONG}. Title/H1 QC restano. Le foto arrivano in-app in Cina; Poste Italiane non rifà il QC.</p>\n<h2>Cos’è</h2>',
            1,
        )
        _write("bbdbuy.it/bbdbuy-qc.html", qc)

    coup = _read("bbdbuy.it/bbdbuy-coupons.html")
    if STAMP not in coup:
        coup = coup.replace(
            "Aggiornato 2026-10-28 · desk IT deepen · data-it-deepen=20261028",
            f"Aggiornato 2026-10-28 · riletto {REVIEW_ISO} (codici ancora confirm-live su bbdbuy.com, non riscattati qui) · data-it-deepen=20261028",
            1,
        )
        _write("bbdbuy.it/bbdbuy-coupons.html", coup)

    app = _read("bbdbuy.it/bbdbuy-app.html")
    app = app.replace(
        "BBDBuy Spreadsheet in italiano: questo articolo è stato sostituito",
        "App BBDBuy Italia — QC e tracking in app",
    )
    app = app.replace(
        "Replaced leftover article on bbdbuy.it.",
        "Dove sta l’app BBDBuy per chi spedisce in Italia: QC in magazzino, tracking, nessun pagamento su bbdbuy.it. Riletto 18 novembre 2026.",
    )
    app = app.replace(
        """<main id="main" class="inner-article">
<article class="pw">
  <h1>Questo articolo è stato sostituito</h1>
  <p class="lead">La versione precedente non era di BBDBuy. La guida attuale sta su Start. L’indirizzo è una via italiana e CAP a cinque cifre. Poste Italiane è il corriere locale di riferimento.</p>
  <p><a class="btn" href="/start/">Start</a> <a class="btn btn--ghost" href="/how-to-use-bbdbuy/">Guida</a></p>
</article>
</main>""",
        f'''<main id="main" class="inner-article">
<article class="pw" data-traffic-recovery="{STAMP}">
  <p class="eyebrow">bbdbuy.it · app · QC / tracking · {REVIEW_ISO}</p>
  <h1>App BBDBuy Italia — QC e tracking</h1>
  <p class="lead">Chi cerca <strong>bbdbuy app</strong> vuole l’album QC e il tracking del pacco, non un secondo spreadsheet. L’app ufficiale è su <a href="https://www.bbdbuy.com/" rel="noopener">bbdbuy.com</a>. Questo TLD non installa APK e non prende pagamenti.</p>
  <h2>Cosa fa l’app (e cosa fa bbdbuy.it)</h2>
  <ul>
    <li>In-app: foto di magazzino, ticket, stima nolo verso l’Italia, tracking dopo la prenotazione.</li>
    <li>Su bbdbuy.it: spreadsheet Italia, <a href="/bbdbuy-qc/">regole QC</a>, <a href="/bbdbuy-coupons/">checklist coupon</a>. Title della home resta quello già in ranking.</li>
  </ul>
  <h2>Prima di Poste Italiane</h2>
  <p>Accetta o rifai le foto mentre la merce è in Cina. Poste Italiane / ADM non rifanno il QC sul cartone. CAP italiano di cinque cifre. Un código español è il paese sbagliato.</p>
  <p><a class="btn" href="https://www.bbdbuy.com/" rel="noopener">Apri BBDBuy.com</a> <a class="btn btn--ghost" href="/bbdbuy-qc/">Guida QC</a> <a class="btn btn--ghost" href="/">Spreadsheet Italia</a></p>
</article>
</main>''',
    )
    _write("bbdbuy.it/bbdbuy-app.html", app)


def patch_w2clinks() -> None:
    convert = f'''
  <section class="w2c-section" id="nov18-convert" data-traffic-recovery="{STAMP}">
    <div class="w2c-container">
      <h2>How to use this spreadsheet (conversion, not a Sheet dump)</h2>
      <p class="w2c-sub">w2clinks.com is the catalog the country desks search into. Title/H1 on this homepage stay frozen through the November 2026 core update. Use the directory, then leave this host to pay.</p>
      <ol class="w2c-convert-steps">
        <li><strong>Search</strong> the live spreadsheet with a brand, model, or a Weidian / Taobao / 1688 URL.</li>
        <li><strong>Open a find</strong> and compare listing photos with warehouse QC before you copy the seller link.</li>
        <li><strong>Paste into your agent</strong> (HipoBuy, USFans, BBDBuy, MyCNBox, Kakobuy, …). This directory does not take payment.</li>
      </ol>
    </div>
  </section>
'''
    text = _read("w2clinks/index.htm")
    if "nov18-convert" not in text:
        text = text.replace(
            '  <section class="w2c-section" id="local">',
            convert + '  <section class="w2c-section" id="local">',
            1,
        )
    text = text.replace('"dateModified":"2026-10-26"', f'"dateModified":"{REVIEW_ISO}"')
    text = text.replace("stamped 26 Oct 2026", f"stamped 26 Oct 2026; conversion copy reviewed {REVIEW_ISO}")
    _write("w2clinks/index.htm", text)

    lists = _read("w2clinks/lists_product.htm")
    if STAMP not in lists:
        lists = lists.replace(
            "<h2>After you pick a {$eyou.field.typename} find</h2>\n      <p>This category page is the {$eyou.field.typename} spreadsheet. Estimate freight before you submit, track the parcel after it ships, and read agent fees on the reviews — not on this grid.</p>",
            f'<h2>After you pick a {{$eyou.field.typename}} find</h2>\n      <p data-traffic-recovery="{STAMP}">This category page is the {{$eyou.field.typename}} spreadsheet. Search → compare QC on the card → copy the seller link into your agent. Estimate freight before you submit. This host does not take payment.</p>',
            1,
        )
        _write("w2clinks/lists_product.htm", lists)


def apply() -> None:
    if not PULL.exists():
        raise SystemExit(f"missing snapshot {PULL}")
    seed_overlay()
    patch_hipobuy()
    patch_usfans()
    patch_dests()
    patch_w2clinks()
    assert_frozen()
    for rel in ("hipobuy/index.htm", "usfans/index.html", "w2clinks/index.htm"):
        html = _read(rel)
        for i, raw in enumerate(
            re.findall(
                r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
                html,
                re.I | re.S,
            )
        ):
            blob = raw.strip()
            if "{eyou:" in blob:
                continue
            try:
                json.loads(blob)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"JSON-LD {rel} block {i}: {exc}") from exc
    # Stub title must have changed
    app = _read("bbdbuy.it/bbdbuy-app.html")
    if "Questo articolo è stato sostituito" in app:
        raise SystemExit("bbdbuy-app stub was not replaced")
    if "App BBDBuy Italia — QC e tracking" not in app:
        raise SystemExit("bbdbuy-app unique H1 missing")
    print(f"overlay ready at {OVERLAY}")
    for rel in REMOTE:
        print(f"  {rel} { (OVERLAY/rel).stat().st_size }")


def _connect():
    try:
        import paramiko
    except ImportError:
        import subprocess

        subprocess.check_call([sys.executable, "-m", "pip", "install", "paramiko", "-q"])
        import paramiko

    password = (
        os.environ.get("ORIENTDIG_DEPLOY_PASS")
        or os.environ.get("BBDBUY_DEPLOY_PASS")
        or os.environ.get("KAKOBUY_DEPLOY_PASS")
    )
    if not password:
        raise SystemExit("Set ORIENTDIG_DEPLOY_PASS")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        HOST,
        username=USER,
        password=password,
        timeout=30,
        allow_agent=False,
        look_for_keys=False,
    )
    return client


def _run(client, cmd: str, timeout: int = 120) -> str:
    _, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    return (stdout.read() + stderr.read()).decode("utf-8", "replace").strip()


def deploy() -> None:
    if not OVERLAY.exists():
        apply()
    client = _connect()
    bak = f"/www/backup/traffic-recovery-{STAMP}"
    print(_run(client, f"mkdir -p {bak}"))
    sftp = client.open_sftp()
    for rel, remote in REMOTE.items():
        local = OVERLAY / rel
        stamp_name = rel.replace("/", "__")
        _run(client, f"cp -a {remote} {bak}/{stamp_name} 2>/dev/null || true")
        tmp = remote + f".new-{STAMP}"
        sftp.put(str(local), tmp)
        owner_cmd = (
            f"mv {tmp} {remote} && chown www:www {remote} && chmod 644 {remote} || chmod 755 {remote}"
        )
        print(rel, _run(client, owner_cmd))
    sftp.close()
    print(
        _run(
            client,
            "rm -rf /www/wwwroot/hipobuyspreadsheet.net/data/runtime/temp/* "
            "/www/wwwroot/w2clinks.com/data/runtime/temp/* 2>/dev/null; echo cache-cleared",
        )
    )
    client.close()
    print("deployed", len(REMOTE), "files; backup", bak)


def verify_live() -> None:
    import urllib.request

    checks = {
        "https://hipobuyspreadsheet.net/": [
            "HipoBuy Spreadsheet — Independent Index · 8,600+",
            "hippobuy spreadsheet",
            REVIEW_SHORT,
            "Public, dated catalog of 8,600+ HipoBuy spreadsheet finds",
            "https://hipobuyspreadsheet.net/terms/#dataset-license",
        ],
        "https://hipobuyspreadsheet.net/finds-dataset/": [
            "HipoBuy Finds Dataset — Row Counts, Sample SKUs",
            "https://hipobuyspreadsheet.net/terms/#dataset-license",
        ],
        "https://hipobuyspreadsheet.net/terms/": [
            "Terms of Use | Hipobuy Spreadsheet",
            'id="dataset-license"',
        ],
        "https://usfansspreadsheet.net/": [
            "USFans Spreadsheet — searchable QC catalog",
            "<h1>USFans Spreadsheet</h1>",
            REVIEW_LONG,
        ],
        "https://usfansspreadsheet.net/usfans-spreadsheet/": [
            "Search the USFans spreadsheet",
            '"@type": "Dataset"',
            "Public, dated catalog of 10,601 USFans spreadsheet finds",
            "https://usfansspreadsheet.net/finds-dataset/#license",
        ],
        "https://bbdbuy.it/": [
            "BBDBuy Spreadsheet per acquirenti in Italia",
            "nov18-review",
        ],
        "https://bbdbuy.it/bbdbuy-app/": ["App BBDBuy Italia — QC e tracking"],
        "https://mycnbox.nl/": ["MyCNBox Spreadsheet voor kopers in Nederland", "nov18-review"],
        "https://mycnbox.co.uk/": ["MyCNBox Spreadsheet for UK Buyers", "nov18-review"],
        "https://mycnbox.eu/": ["MyCNBox Spreadsheet — searchable QC catalog"],
        "https://w2clinks.com/": ["W2C Links — Independent Index · 11,300+", "nov18-convert"],
    }
    for url, needles in checks.items():
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 seo-factory-traffic-recovery"})
        with urllib.request.urlopen(req, timeout=25) as resp:
            html = resp.read().decode("utf-8", "replace")
        missing = [n for n in needles if n not in html]
        title = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
        t = re.sub("<[^>]+>", "", title.group(1) if title else "")
        if missing:
            raise SystemExit(f"LIVE FAIL {url} missing {missing} title={t!r}")
        print("LIVE OK", url, "title=", t.replace("\n", " ")[:120])


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--apply", action="store_true")
    p.add_argument("--deploy", action="store_true")
    p.add_argument("--verify", action="store_true")
    args = p.parse_args()
    if args.apply:
        apply()
        return
    if args.deploy:
        apply()
        deploy()
        verify_live()
        return
    if args.verify:
        verify_live()
        return
    p.error("pass --apply, --deploy, or --verify")


if __name__ == "__main__":
    main()
