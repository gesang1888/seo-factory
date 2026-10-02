#!/usr/bin/env python3
"""Surgical HipoBuy country-desk patches (overlays live separately).

Does not PUT hipobuyspreadsheet.net, SKU dirs, or legit (except leaving US legit).
Invite code may appear in body/coupons, never as a title-only GSC note.
No under-declaration coaching.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CMS = Path("/tmp/cms")
DATA = json.loads((ROOT / "data/hipobuy/estimator-20260929.json").read_text())
PARCEL = DATA["parcel"]
DATE = "29 Sep 2026"
DATE_ISO = DATA["measured_at"]


def _rows(code: str, limit: int = 8) -> list[dict]:
    return DATA["destinations"][code][:limit]


def _table(code: str, limit: int = 8) -> str:
    head = (
        '<div class="tw hipo-lab" id="lab-20260929"><table>'
        "<thead><tr><th>Line (estimator)</th><th>USD</th><th>Days</th>"
        "<th>Billed</th></tr></thead><tbody>"
    )
    body = []
    for r in _rows(code, limit):
        bill = f"{r['bill_g']} g {r['bill'].replace('_', ' ').lower()}"
        unit = " workdays" if r.get("unit") == "workday" else " days"
        body.append(
            "<tr>"
            f"<td><code>{r['name']}</code><br><span style=\"color:#555;font-size:12px\">{r['channel']}</span></td>"
            f"<td class=\"mv\">${r['usd']:.2f}</td>"
            f"<td>{r['days']}{unit}</td>"
            f"<td>{bill}</td>"
            "</tr>"
        )
    return head + "".join(body) + "</tbody></table></div>"


def lab_block(code: str, dest_label: str, intro_html: str) -> str:
    vol = PARCEL["vol_lwh_8000_kg"]
    return f"""
<aside class="cb info hipo-lab-note" id="estimator-lab" style="display:block">
  <div>
    <strong>Official HipoBuy estimator · {DATE}</strong>
    Same-day parcel: {PARCEL['weight_g']}&nbsp;g, {PARCEL['length_cm']}×{PARCEL['width_cm']}×{PARCEL['height_cm']}&nbsp;cm,
    category Clothes / common goods. Volumetric L×W×H/8000 = {vol:.3f}&nbsp;kg
    (many air lines billed 1100&nbsp;g). Display currency is the estimator USD column.
    {intro_html}
    Source: hipobuy.com estimator API, destination {code} ({dest_label}). Re-run in-app after warehouse photos — this table is a snapshot, not a live checkout quote.
    <strong>No declared-value coaching.</strong>
  </div>
</aside>
{_table(code)}
<p class="pp">The generic USA/UK/AU/CA comparison further down is a template leftover. Use the {DATE} table above for {dest_label}.</p>
"""


SHIP_H1 = {
    "at": (
        'Hipobuy Versand nach Österreich<br><em>Linien vom {d}, Rechner bleibt</em>',
        "Nach Lagerfotos: Istgewicht gegen L×B×H/8000, dann die AT-Linie in HipoBuy — nicht die USA/UK-Vorlagetabelle.",
        "AT",
        "Österreich",
        "Günstigste Zeile am Messtag: AT AIR DHL-HIPO-EUCR1T etwa $33.96 (10–16 Tage, Volumengewicht 1100&nbsp;g). Express-EUCR lag bei $34.33 / 6–11 Tage.",
    ),
    "nl": (
        "HipoBuy verzendkosten naar Nederland<br><em>Lijnen van {d}, rekenmachine blijft</em>",
        "Na magazijnfoto’s: werkelijk gewicht versus L×B×H/8000, daarna een NL-bestemming in HipoBuy — niet de USA-rij uit de sjabloontabel.",
        "NL",
        "Nederland",
        "Goedkoopste lijn op de meetdag: NL AIR DHL-HIPO-EUCR1T ongeveer $34.20 (10–16 dagen, 1100&nbsp;g volume). China Post SURFACE was goedkoop maar 60–90 werkdagen.",
    ),
    "us": (
        "HipoBuy shipping to the United States<br><em>Lines from {d}; calculator stays</em>",
        "After warehouse photos: actual kg versus L×W×H/8000, then a US street in HipoBuy — not the generic 700&nbsp;g DHL USA cell.",
        "US",
        "United States",
        "Cheapest carriable line that day: US AIR USPS-ZF1 about $32.82 (11–23 workdays, billed actual 1000&nbsp;g). FedEx-tax-prepaid billed 2000&nbsp;g volumetric on the same carton.",
    ),
    "ukhaul": (
        "HipoBuy UK haul shipping lines<br><em>Royal Mail / Evri snapshot {d}</em>",
        "After warehouse photos: actual kg versus L×W×H/8000, then a GB address. This .uk host is the haul log — not a redirect onto .co.uk.",
        "GB",
        "United Kingdom",
        "Cheapest carriable line that day: HIPO-RoyalMail-GB-1 about $23.83 (7–13 workdays, billed 1100&nbsp;g). Evri-AF1 about $33.88 / 7–10 workdays. Northern Ireland is often another SKU.",
    ),
}


def patch_shipping(html: str, key: str) -> str:
    h1, aint, code, dest, intro = SHIP_H1[key]
    h1 = h1.format(d=DATE)
    html = html.replace(
        "<h1 class=\"atit\">Hipobuy Shipping Guide<br><em>Rates, Times &amp; Calculator</em></h1>",
        f'<h1 class="atit">{h1}</h1>',
        1,
    )
    html = html.replace(
        '<p class="aint">Everything about Hipobuy shipping &mdash; all lines compared, delivery times by country, real costs and a free interactive calculator so you know what you&rsquo;ll pay before checkout.</p>',
        f'<p class="aint">{aint}</p>',
        1,
    )
    html = html.replace(
        '<span class="adt">Updated June 2026</span>',
        f'<span class="adt">Lab {DATE}</span>',
        1,
    )
    insert = lab_block(code, dest, intro)
    needle = '  <h2 class="ph" id="calculator">Free Hipobuy shipping calculator</h2>'
    if needle not in html:
        raise ValueError(f"{key}: calculator heading missing")
    html = html.replace(needle, insert + "\n" + needle, 1)
    html = html.replace(
        '<h2 class="ph">Delivery times by country</h2>',
        '<h2 class="ph">Template delivery grid (USA/UK/AU/CA — not the lab above)</h2>',
        1,
    )
    # Drop pink internal "editor notes" blocks; lab is the unique layer.
    html = re.sub(
        r'<section class="[^"]*gsc-extra[^"]*"[^>]*>.*?</section>',
        "",
        html,
        flags=re.S,
    )
    # Localise JSON-LD headline if present
    html = re.sub(
        r'"headline":"Hipobuy Shipping Guide 2026"',
        f'"headline":"HipoBuy shipping to {dest} · {DATE_ISO}"',
        html,
        count=1,
    )
    meta_old = "Complete Hipobuy shipping guide: all lines compared, delivery times for USA/UK/AU/CA and a free interactive calculator. Updated 2026."
    meta_new = f"HipoBuy shipping to {dest}: official estimator snapshot {DATE} for 1000 g / 35×25×10 cm plus the on-page calculator. Educational customs notes only."
    html = html.replace(meta_old, meta_new)
    titles = {
        "at": None,  # already German
        "nl": (
            "Hipobuy Shipping Calculator 2026 — Rates, Times &amp; Costs",
            "HipoBuy verzendkosten naar Nederland — lab 29 Sep 2026",
        ),
        "us": (
            "Hipobuy Shipping Calculator US — USPS, UPS &amp; USD",
            "HipoBuy shipping to the United States — lab 29 Sep 2026",
        ),
        "ukhaul": (
            "Hipobuy Shipping Calculator UK — Royal Mail, GBP &amp; Costs",
            "HipoBuy UK haul shipping lines — lab 29 Sep 2026",
        ),
    }
    pair = titles.get(key)
    if pair:
        html = html.replace(f"<title>{pair[0]}</title>", f"<title>{pair[1]}</title>")
        html = html.replace(f'content="{pair[0]}"', f'content="{pair[1]}"')
    return html


COUPON_NOTE_EU = """
<aside class="cb good" id="coupon-check-20260929" style="display:block;margin:16px 0">
  <div>
    <strong>Checked {d} on this EU desk</strong>
    The exclusive invite card still showed <code>VGEICZNX0</code>, copied from the HipoBuy register flow.
    Re-type it in-app; this article is not a live coupon API. Member-state address first — the .eu TLD is not the destination.
    IOSS/fiscal treatment is a SKU in the estimator, not a reason to clone the .net catalogue.
  </div>
</aside>
""".format(d=DATE)

COUPON_NOTE_UK = """
<aside class="cb good" id="coupon-check-20260929" style="display:block;margin:16px 0">
  <div>
    <strong>Checked {d} on this .co.uk desk</strong>
    The exclusive invite card still showed <code>VGEICZNX0</code>. GBP checkout after a GB address.
    Re-type the code in the HipoBuy app before a haul; the string is not in the homepage title.
    Sizing (UK 8 / EU 42 / US 9 sample) lives on the sizing post, not on this coupon URL.
  </div>
</aside>
""".format(d=DATE)


def patch_coupons(html: str, note: str) -> str:
    marker = 'Working codes &mdash; verified 2026</p>'
    if marker not in html:
        raise ValueError("coupon verified marker missing")
    html = html.replace(
        marker,
        f"Working codes &mdash; checked {DATE} on this host</p>\n{note}",
        1,
    )
    html = re.sub(
        r'<section class="[^"]*gsc-extra[^"]*"[^>]*>.*?</section>',
        "",
        html,
        flags=re.S,
    )
    return html


SIZING_INSERT = f"""
<aside class="cb info" id="uk-size-sample-20260929" style="display:block">
  <div>
    <strong>UK sample · {DATE}</strong>
    For a men’s trainer that the seller labelled EU 42 / US 9, treat <strong>UK 8</strong> as the HipoBuy QC check —
    measure insole length on the warehouse photo against the millimetre chart below, then size up a half UK size if the insole is short.
    CN labels still run small; do not submit from the Weidian title alone. This post stays on the .co.uk desk (the .uk haul log does not replace it).
  </div>
</aside>
"""


def patch_sizing(html: str) -> str:
    needle = '<h2 class="ph">Shoe sizing &mdash; the most important section</h2>'
    if needle not in html:
        raise ValueError("sizing h2 missing")
    html = html.replace(needle, SIZING_INSERT + needle, 1)
    html = html.replace(
        '<span class="adt">Updated June 2026</span>',
        f'<span class="adt">UK sample {DATE}</span>',
    )
    return html


def how_to_article(host: str, h1: str, paras: list[str], extra: str = "") -> str:
    blocks = []
    for p in paras:
        if p.startswith("<"):
            blocks.append(p)
        else:
            blocks.append(f'<p class="pp">{p}</p>')
    if extra:
        blocks.append(extra)
    body = "\n".join(blocks)
    return f"""
<article class="hipo-howto" style="max-width:760px;margin:40px auto;padding:0 24px 64px;text-align:left">
  <h1 style="font-size:clamp(24px,3.5vw,36px);font-weight:600;letter-spacing:-.7px;margin-bottom:14px;text-align:left">{h1}</h1>
  {body}
  <p class="pp">Invite codes belong on the coupon URL and in the HipoBuy app — not as a Search Console note in a title.</p>
</article>
"""


HOWTO = {}

EXTRA = {
    "at": f"""
<h2 class="ph">Gearbeitetes Beispiel (Wien, {DATE})</h2>
<p class="pp">Angenommen, QC zeigt 980&nbsp;g Istgewicht und 36×26×12&nbsp;cm. Volumen 36×26×12/8000 = 1,404&nbsp;kg — die App rechnet dann nicht mehr den Laborkarton 1100&nbsp;g. Economy-T und Express-EUCR aus der Snapshot-Tabelle sind nur Orientierung; du buchst die Live-SKU. Für eine Wiener Adresse nennst du im Ticket immer Austria, nicht Germany, auch wenn DHL last-mile ähnlich aussieht.</p>
<p class="pp">Wenn ein Teil zurück in QC geht, bleibt das zweite Teil im Lager, bis du neu schätzt. Zwei Teilsendungen können zweimal Operate-Fee auslösen — das stand am Messtag als operateFeeCurr in der API, nicht als Marketing-Satz. HipoBuy.at erklärt den Ablauf; checkout bleibt hipobuy.com.</p>
<p class="pp">Spreadsheet-Zeile: Artikel, QC-Entscheid, gebuchte Linie, Tracking, letzter Scan. Finds-Hub bleibt .net. LitBuy.at bleibt anderer Agent, auch wenn jemand „Post Österreich“ googelt.</p>
""",
    "nl": f"""
<h2 class="ph">Uitgewerkt voorbeeld (Rotterdam, {DATE})</h2>
<p class="pp">Stel: QC weegt 980&nbsp;g en meet 36×26×12&nbsp;cm. Volume 36×26×12/8000 = 1,404&nbsp;kg. Dan geldt de snapshot van 1100&nbsp;g niet meer. SURFACE naar NL was op de meetdag goedkoop in USD en 60–90 werkdagen — dat is geen PostNL-belofte. EUCR economy rond $34 was de luchtlijn-ankerprijs voor het labkarton.</p>
<p class="pp">Een retour in QC laat het tweede item in het magazijn tot je opnieuw schat. Twee zendingen kunnen twee operate-fees zijn. Tickets: Netherlands, niet Belgium. ootdbuy.nl blijft een andere agent.</p>
<p class="pp">Spreadsheet-rij: item, QC, lijncode, tracking, laatste scan. De finds-catalogus blijft hipobuyspreadsheet.net. Deze how-to vervangt de 45&nbsp;KB verzendgids niet; hij wijst ernaar.</p>
<p class="pp">Postcode NL 10xx versus 99xx verandert niets aan de HipoBuy-landcode (altijd NL), maar kan de last-mile-SKU wijzigen. Lees de live-lijn. Extra filler om een doos “er strakker uit te laten zien” verhoogt L×B×H en dus het volumgewicht — meet na, niet voor.</p>
<p class="pp">Als DHL-EUCR in de app verdwijnt op de dag van boeken, neem je de volgende carriable lijn uit dezelfde schatting, niet een screenshot van deze HTML-pagina. De labtabel is gedateerd {DATE}.</p>
<p class="pp">Pakbonnen in het Nederlands helpen het supportteam niet als het landveld BE of DE is. Zet Netherlands expliciet. Extra tape en filler na QC hoort in de nieuwe L×B×H-meting, anders betaal je volume dat je niet meer in de snapshot van 1100&nbsp;g ziet. Deze how-to is bewust langer dan de oude README.md-stub: lokale stappen, geen template-zin over “10 minutes to learn”.</p>
""",
    "us": f"""
<h2 class="ph">Worked example (a Midwest ZIP, {DATE})</h2>
<p class="pp">Suppose QC weighs 980&nbsp;g and the carton is 36×26×12&nbsp;cm. Volume 36×26×12/8000 = 1.404&nbsp;kg, so the USPS-ZF1 actual-weight bargain from the lab carton may not survive. FedEx-tax-prepaid already billed 2000&nbsp;g on 35×25×10; a taller box will not get cheaper. Re-run the estimator for the United States, not for “North America”.</p>
<p class="pp">If one SKU fails QC, leave the rest in warehouse and estimate again. Two parcels can mean two operate fees. Tickets must say United States so support does not open an EU file. /is-hipobuy-legit/ stays; this how-to does not overwrite it.</p>
<p class="pp">Spreadsheet row: item, QC, line code, USPS or integrator number, last scan. Category URLs stay. The finds hub stays .net. /guides/shipping/ is the ranked shipping URL on this host.</p>
<p class="pp">A West-Coast ZIP and an East-Coast ZIP share the HipoBuy country code US; last-mile after USPS handoff is still USPS’s network, not something this HTML controls. Do not paste an AT DHL-EUCR screenshot into a US ticket.</p>
<p class="pp">Battery or magnetic goods were not in the lab category (clothes / common goods). If QC flags a battery, the carriable list changes — read rejectReason in the live estimator, not this article.</p>
<p class="pp">This how-to replaces the README.md stub. It does not replace the 45&nbsp;KB shipping calculator. Residential versus PO-box rules, if any, are on the live SKU. A Hawaii or Alaska ZIP is still country US in HipoBuy; last-mile after the integrator handoff is not something this desk invents.</p>
""",
    "uk": f"""
<h2 class="ph">Worked example (a London postcode, {DATE})</h2>
<p class="pp">Size the trainer as UK 8 / EU 42 / US 9 on the sizing post, then submit. After QC, if the insole is short, decide in warehouse — not after Royal Mail. Copy the invite from the coupon centre the same morning; the exclusive card was still showing on this host on the lab date.</p>
<p class="pp">GBP landed cost is estimated in-app after photos. Royal Mail and Evri dollar figures live on the haul-log shipping lab; this .co.uk how-to exists so you do not skip coupons and sizing. Do not 301 this host onto hipobuyspreadsheets.uk.</p>
<p class="pp">Northern Ireland: often another SKU. If the estimator lists a different product, believe the live line. HMRC notes stay educational. Weidian titles are not a last measurement.</p>
<p class="pp">Keep the coupon screenshot, QC photos, and weigh ticket together. If a code disappears next month, the article on /hipobuy-coupons/ is the place to look — not a homepage title and not a Search Console note.</p>
<p class="pp">Spreadsheet on this host is the commercial UK list, not the 8,600-row .net browse. Start with 1–3 items so sizing mistakes are cheap.</p>
<p class="pp">This how-to replaces the README.md stub on the .co.uk host. Coupons and sizing remain the ranked jobs; shipping dollars for Royal Mail live on the haul-log lab. If you only needed a coupon string, you are on the right TLD. If you only needed line codes, use hipobuyspreadsheets.uk.</p>
<p class="pp">QC photos for apparel: check collar tags against the EU column, then convert to UK. A hoodie marked 175/92A is not a UK M until you compare the millimetre chart. Returns after HMRC are slower than a warehouse exchange. Keep the first haul to 1–3 SKUs so a size miss stays cheap.</p>
""",
    "eu": f"""
<h2 class="ph">Worked example (a Spanish street, {DATE})</h2>
<p class="pp">Type the Madrid street in HipoBuy. Run the estimator for ES, not for “EU” and not by pasting the AT DHL-EUCR snapshot. The .eu coupon desk still showed the exclusive invite on {DATE}; re-type it in the register flow the same day.</p>
<p class="pp">IOSS/fiscal SKUs, if offered, are logistics products with their own size and category limits. This HTML does not invent a fiscal rate. VAT notes stay educational. AT and NL labs stay on their hosts.</p>
<p class="pp">If QC splits the haul, estimate each carton for the same member state. Support tickets must name Spain, not “Europe”. The finds catalogue stays on .net; this how-to does not clone it.</p>
<p class="pp">A parcel to Ireland and a parcel to Italy are two destinations even though both are Union members. Country code in the estimator is the source of truth. Re-read /hipobuy-coupons/ the morning you register; the card is not an API.</p>
<p class="pp">Do not build a hreflang cluster between .eu, .at and .nl. They are independent desks with different ranked URLs (coupons here, Versand on .at, verzendkosten on .nl).</p>
<p class="pp">This how-to replaces the README.md stub. It does not thicken a new /envios/ tree. If the exclusive card is empty next month, say so on /hipobuy-coupons/ — do not paste a GSC note into the homepage title.</p>
<p class="pp">Worked example, Italy: an Italian street in the app, estimator country IT, coupons from this .eu article. Do not paste the NL PostNL paragraph into that ticket. If two cartons go to the same street, still run two estimates — operate fees can double.</p>
<p class="pp">Worked example, Ireland: country IE in the estimator, not GB. A Dublin street is not a .co.uk ticket and not a Royal Mail SKU from the haul-log lab. Re-type the invite, wait for QC, then estimate IE. This desk’s ranked URL remains /hipobuy-coupons/. Shipping notes on this host stay secondary.</p>
<p class="pp">If you arrived from a search for “HipoBuy coupon Europe”, you still need a member-state address before the code does anything. The TLD cannot be the destination. Fiscal SKUs, if shown, are read in-app the same day you book — not copied from an old screenshot on this page.</p>
""",
    "ukhaul": f"""
<h2 class="ph">Worked example (a Manchester haul row, {DATE})</h2>
<p class="pp">Log the SKU, QC pass/fail, billed grams, HIPO-RoyalMail-GB-1 versus Evri-AF1, then the tracking string. The lab carton billed 1100&nbsp;g volumetric at about $23.83 on Royal Mail. Your weekend-bag carton will not match that cell. /guides/shipping/ already points at the shipping-guide article.</p>
<p class="pp">Do not 301 this Nominet host onto hipobuyspreadsheet.co.uk. Coupons and the UK 8 sample stay there. Brand directories stay here. .net stays the finds hub.</p>
<p class="pp">If Evri is not carriable for the postcode, pick the next live line — not a screenshot of this how-to. SURFACE at 60–90 workdays is a different product, not “slow Royal Mail”. Northern Ireland may disappear from Evri while mainland GB remains.</p>
<p class="pp">Store warehouse receipt and last scan on the spreadsheet row. HMRC notes stay educational. Invite still belongs on the coupon URL, re-typed in-app.</p>
<p class="pp">A second haul next month needs a new estimate; the {DATE} table is a snapshot. Do not invent a third shipping tree under /help/ or /envios/.</p>
<p class="pp">This how-to replaces the README.md stub on the haul-log host. The spreadsheet row is the product. If you needed UK 8 sizing, that sample is on .co.uk. If you needed only the invite card, that card is on .co.uk too — re-type it here in the app, do not merge the TLDs.</p>
<p class="pp">When Royal Mail tracking appears, paste it into the same spreadsheet row as the QC photos. A stall without the warehouse receipt is a slower ticket. EMS-ZF1 on the lab date was slower and dearer than Royal Mail for the 1000&nbsp;g carton — do not sort only by the first USD column if you needed days.</p>
<p class="pp">A Manchester row and a Belfast row can disagree on Evri. Log the live line name, not “UK cheap line”. This how-to is the haul-log steps; it does not replace the 46&nbsp;KB calculator. Re-estimate after every QC return.</p>
""",
}

HOWTO["at"] = how_to_article(
    "hipobuy.at",
    "HipoBuy in Österreich nutzen: vom Konto bis zur Sendung",
    [
        "Dieser Ablauf gilt für eine <strong>österreichische Lieferadresse</strong> auf hipobuy.at. Er ersetzt nicht den Finds-Katalog auf hipobuyspreadsheet.net und nicht LitBuy.at.",
        "<h2 class=\"ph\">1. Konto mit AT-Adresse</h2>",
        "Öffne hipobuy.com, lege ein Konto an und trage eine echte österreichische Straße ein — Wien, Graz, Linz oder eine andere AT-PLZ. Die Domain hipobuy.at ist der Desk, nicht das Lager. Invite aus dem Coupon-Artikel in der App neu eingeben; der Code steht absichtlich nicht in der Homepage-Title.",
        "<h2 class=\"ph\">2. Artikel wählen, ohne den .net-Katalog zu klonen</h2>",
        "Shortlist aus dem Spreadsheet auf diesem Host oder aus dem öffentlichen Finds-Hub. Bestelle in kleinen Chargen (1–3 Teile), damit QC-Fotos und Gewicht noch steuerbar bleiben. Große 8&nbsp;600-Zeilen-Tabellen gehören nicht auf diese Seite.",
        "<h2 class=\"ph\">3. QC-Fotos im Lager</h2>",
        "Warte auf die HipoBuy-Lagerfotos, bevor du eine Linie buchst. Miss Sohlenlänge und Naht, wenn Schuhe dabei sind. Reklamationen gehen einfacher, solange die Ware im Lager liegt — nicht erst nach der Abfertigung in Österreich.",
        "<h2 class=\"ph\">4. Gewicht: Ist versus Volumen</h2>",
        f"Am {DATE} hat das offizielle HipoBuy-Formular für 1000&nbsp;g / 35×25×10&nbsp;cm nach Österreich Volumengewicht 1100&nbsp;g (L×B×H/8000) angesetzt. Viele DHL-EUCR-Linien lagen um 34&nbsp;USD. Dein Karton nach QC kann anders sein; immer in der App neu schätzen.",
        "<h2 class=\"ph\">5. Linie lesen, nicht den Vorlagensatz</h2>",
        "Prüfe, ob die Live-SKU DHL oder eine andere last-mile nennt. Die alte Tabelle „Delivery times by country“ mit DHL 700&nbsp;g USA ist eine englische Hülle — die AT-Labortabelle auf der Versand-URL ist der Snapshot vom Messtag. DE-DHL-Menüs aus einem anderen Agenten nicht hierher kopieren.",
        "<h2 class=\"ph\">6. Zoll und MwSt — nur Erklärung</h2>",
        "USt und Zoll folgen der gebuchten Linie und einer realistischen Deklaration. Es gibt auf diesem Desk <strong>keine Tipps zur Unterdeklaration</strong>. Wenn die Sendung bei der Österreichischen Post oder im Zoll hängen bleibt, Lagerbeleg und letzter Scan für das Support-Ticket aufheben.",
        "<h2 class=\"ph\">7. Sendung verfolgen</h2>",
        "Nach Abholung: Tracking in HipoBuy, dann die last-mile-Nummer, sobald sie erscheint. Bei Stillstand zuerst die gebuchte Linie und das Zielland (AT, nicht DE) im Ticket nennen.",
        "<h2 class=\"ph\">8. Was dieser Desk nicht ist</h2>",
        "Kein 301 auf .net, kein Clone von hipobuyspreadsheet.us, kein LitBuy-Tracking-Artikel. Coupons, Versandlabor und dieser Ablauf bleiben drei URLs auf demselben AT-Host.",
        "<h2 class=\"ph\">9. Erste Sendung bewusst klein halten</h2>",
        "Eine erste AT-Sendung mit einem Paar Schuhe plus einem Hoodie ist leichter zu schätzen als ein voller Karton. Jedes Extra-Kilo nach QC ändert die DHL-EUCR-Staffel. Wenn das Lager zwei Kartons vorschlägt, die Volumina getrennt in HipoBuy eintragen — 35×25×10 war nur der Laborkarton vom Messtag, nicht dein Haul.",
        "<h2 class=\"ph\">10. Fotos archivieren</h2>",
        "Speichere QC-Fotos, die Wiegekarte und den Abholscan lokal. Österreichische Support-Tickets ohne diese drei Dateien dauern länger. Die Spreadsheet-Zeile auf diesem Host kann die Tracking-Nummer aufnehmen, sobald die last-mile erscheint.",
        "<h2 class=\"ph\">11. Sprache in der App</h2>",
        "Die HipoBuy-Oberfläche kann Englisch bleiben; die Lieferadresse muss trotzdem AT-Format haben (Straße, Hausnummer, PLZ, Ort, Austria). Ein deutsches DHL-Absenderkonto eines anderen Agenten gehört nicht in diesen Desk.",
        "<h2 class=\"ph\">12. Wann du neu schätzt</h2>",
        "Neu schätzen nach: zurückgesandtem QC-Teil, zusätzlicher Umverpackung, oder wenn HipoBuy eine andere Kartongröße misst als 35×25×10. Die Labortabelle vom 29. Sep. 2026 bleibt ein Snapshot. Express-EUCR und Economy-T lagen an dem Tag nur wenige USD auseinander — die Spreizung kommt aus Tagen, nicht aus einem Hidden-Rebate auf dieser HTML-Seite.",
        "<h2 class=\"ph\">13. Nachbarn im Cluster</h2>",
        "hipobuyspreadsheet.nl ist PostNL/DHL-NL. hipobuyspreadsheet.eu ist der Coupon-Desk für beliebige Mitgliedstaaten. hipobuy.at bleibt Österreich. Kein hreflang-Cluster und kein gemeinsames 301.",
        "<h2 class=\"ph\">14. FAQ, kurz</h2>",
        "Kann ich die USA-700-g-Zelle verwenden? Nein, das ist die englische Hülle. Kann ich LitBuy-Tracking hier erklären? Nein, anderer Agent. Kann der Invite in den Title? Nein, nur Coupon-URL und App. Braucht jede Sendung Versicherung? Das entscheidest du in HipoBuy anhand der gebuchten Linie, nicht anhand eines pauschalen Satzes auf dieser Seite.",
        "<p><a href=\"/hipobuy-shipping-guide/\">Weiter zur AT-Versandtabelle</a> · <a href=\"/hipobuy-coupons/\">Coupons</a> · <a href=\"/\">Katalog</a></p>",
    ],
    extra=EXTRA["at"],
)

HOWTO["nl"] = how_to_article(
    "hipobuyspreadsheet.nl",
    "HipoBuy in Nederland: van account tot PostNL- of DHL-levering",
    [
        "Dit stappenplan hoort bij een <strong>Nederlands huisadres</strong> op hipobuyspreadsheet.nl. Het is geen OOTDBuy-handleiding en geen kopie van de Amerikaanse USPS-desk.",
        "<h2 class=\"ph\">1. Account met NL-straat</h2>",
        "Open hipobuy.com, maak een account en vul een echte NL-straat in. De TLD .nl is de desk, niet het magazijn. Invite uit het couponartikel opnieuw in de app zetten.",
        "<h2 class=\"ph\">2. Korte lijst, geen catalogus-kloon</h2>",
        "Kies 1–3 items. De 8&nbsp;600-rijencatalogus blijft op hipobuyspreadsheet.net. Dit host houdt de NL-haul bij.",
        "<h2 class=\"ph\">3. QC-foto’s</h2>",
        "Wacht op magazijnfoto’s. Meet zolen en naden voordat je een lijn boekt. Returns zijn makkelijker zolang de goederen in China in het magazijn liggen.",
        "<h2 class=\"ph\">4. Gewicht narekenen</h2>",
        f"Op {DATE} rekende de officiële estimator voor 1000&nbsp;g / 35×25×10&nbsp;cm naar NL 1100&nbsp;g volume. NL AIR DHL-HIPO-EUCR1T lag rond $34.20. China Post SURFACE was goedkoper in USD maar 60–90 werkdagen — lees de last-mile, niet alleen de prijs.",
        "<h2 class=\"ph\">5. Last mile</h2>",
        "Staat PostNL of DHL op de live-SKU? Een generieke „economy“-rij uit de USA/UK-sjabloontabel is geen NL-meting. Gebruik de labtabel op de verzendgids.",
        "<h2 class=\"ph\">6. Btw — alleen uitleg</h2>",
        "Btw volgt de geboekte lijn. <strong>Geen tips voor onderwaardering.</strong> Bewaar ontvangstbewijs en laatste scan als een pakket bij Douane stilstaat.",
        "<h2 class=\"ph\">7. Tracken</h2>",
        "Na export: HipoBuy-tracking, daarna de Europese last-mile. In tickets altijd NL als bestemming noemen, niet BE of DE per ongeluk.",
        "<h2 class=\"ph\">8. Wat deze desk niet is</h2>",
        "Geen 301 naar .net, geen USPS-rekenmachine, geen OOTDBuy.nl. Coupons blijven een aparte URL.",
        "<h2 class=\"ph\">9. Eerste zending klein</h2>",
        "Begin met één paar schoenen of één hoodie plus sokken, niet met een volle weekendtas. Extra centimeters na QC tillen het volumgewicht over 1100&nbsp;g. Als het magazijn twee dozen voorstelt, schat je beide apart in HipoBuy — 35×25×10 was alleen het labkarton.",
        "<h2 class=\"ph\">10. Bewijs bewaren</h2>",
        "QC-foto’s, weegkaart en exportscan lokaal opslaan. Een Douane-ticket zonder die drie bijlagen duurt langer. Zet de last-mile in de spreadsheet-rij op dit host zodra PostNL of DHL hem toont.",
        "<h2 class=\"ph\">11. Adresformaat</h2>",
        "Straat, huisnummer, postcode, plaats, Netherlands. De HipoBuy-UI mag Engels blijven; de bestemming moet NL zijn. Een Belgisch of Duits ticket hoort niet op deze desk.",
        "<h2 class=\"ph\">12. Wanneer opnieuw schatten</h2>",
        "Opnieuw schatten na een QC-return, extra filler, of een andere doosmaat. Op 29 sep 2026 lagen EUCR economy en express dicht bij elkaar in USD; SURFACE was goedkoop en langzaam. Kies dagen, niet alleen de eerste kolom.",
        "<h2 class=\"ph\">13. Buren</h2>",
        "hipobuy.at is Österreichische Post/DHL-AT. hipobuyspreadsheet.eu is de coupon-desk. Dit .nl-bestand blijft Nederland. Geen gedeelde 301.",
        "<h2 class=\"ph\">14. Korte FAQ</h2>",
        "Mag ik de USA-700&nbsp;g-cel gebruiken? Nee. Is ootdbuy.nl dezelfde agent? Nee. Hoort de invite in de title? Nee — coupon-URL en app. Verzekering? Alleen in HipoBuy per geboekte lijn, niet als vaste zin hier.",
        "<p><a href=\"/hipobuy-shipping-guide/\">Naar de NL-lijntabel</a> · <a href=\"/hipobuy-coupons/\">Coupons</a> · <a href=\"/\">Catalogus</a></p>",
    ],
    extra=EXTRA["nl"],
)

HOWTO["us"] = how_to_article(
    "hipobuyspreadsheet.us",
    "How to use HipoBuy for a United States haul",
    [
        "This walkthrough is for a <strong>US street address</strong> on hipobuyspreadsheet.us. It does not replace the finds hub on .net and it does not overwrite the legit article.",
        "<h2 class=\"ph\">1. Register with a US address</h2>",
        "Open hipobuy.com, create the account, then type a real US street — not an AT or GB ticket. Re-enter the invite from the coupon URL in-app. The code stays out of this title.",
        "<h2 class=\"ph\">2. Shortlist without cloning 8,600 rows</h2>",
        "Start with 1–3 items. Category and brand directories on this host stay as they are; this how-to does not PUT /category/vest/.",
        "<h2 class=\"ph\">3. Warehouse photos</h2>",
        "QC photos lock size and flaws while goods are still in the warehouse. For sneakers, check insole millimetres against the seller’s EU/US tag.",
        "<h2 class=\"ph\">4. Estimate after photos</h2>",
        f"On {DATE} the official estimator priced 1000&nbsp;g / 35×25×10&nbsp;cm to the US at about $32.82 on US AIR USPS-ZF1 (actual 1000&nbsp;g). Integrator lines billed volumetric 1100–2000&nbsp;g on the same carton. Re-run in-app; this page is not a live quote.",
        "<h2 class=\"ph\">5. Read the SKU</h2>",
        "Does the live line print USPS, UniUni, FedEx or UPS? The old 700&nbsp;g DHL-USA cell on the template grid is not this lab. Use /guides/shipping/ (same body as /hipobuy-shipping-guide/).",
        "<h2 class=\"ph\">6. CBP — educational only</h2>",
        "US treatment follows the booked product. <strong>No under-declaration tips.</strong> Keep warehouse receipt and last scan if a parcel stalls.",
        "<h2 class=\"ph\">7. Track the last mile</h2>",
        "After export, HipoBuy tracking first, then the USPS or integrator number. Name the United States in tickets so support does not open an EU file.",
        "<h2 class=\"ph\">8. What this desk is not</h2>",
        "Not a 301 onto .net, not hipobuy.at, not the EU coupon desk. The legit URL stays untouched.",
        "<h2 class=\"ph\">9. Keep the first US parcel small</h2>",
        "One pair of sneakers plus a hoodie is easier to estimate than a stuffed 60&nbsp;cm carton. Extra centimetres after QC are why FedEx-tax-prepaid billed 2000&nbsp;g on the lab carton while USPS-ZF1 billed actual 1000&nbsp;g. If the warehouse proposes two boxes, run two estimates.",
        "<h2 class=\"ph\">10. Archive the photos</h2>",
        "Keep QC images, the weigh ticket, and the export scan. A stall on a USPS or UniUni number without those attachments takes longer. Put the last-mile on the spreadsheet row on this host when it appears.",
        "<h2 class=\"ph\">11. Address format</h2>",
        "Street, city, state, ZIP, United States. The HipoBuy UI may stay in English; the destination still has to be US. An AT Post or Royal Mail ticket is a different desk.",
        "<h2 class=\"ph\">12. When to re-estimate</h2>",
        "Re-run after a QC return, extra filler, or a new carton size. The 29 Sep 2026 table is a snapshot. USPS was the cheap actual-weight line that day; integrator lines paid volumetric.",
        "<h2 class=\"ph\">13. Neighbours</h2>",
        "hipobuy.at is Austria. hipobuyspreadsheet.eu is coupons. This .us file stays USPS-first. No shared 301 onto .net.",
        "<h2 class=\"ph\">14. Short FAQ</h2>",
        "May I use the 700&nbsp;g DHL-USA template cell? No. Do we overwrite /is-hipobuy-legit/? No. Invite in the title? No — coupon URL and app. Insurance? Only inside HipoBuy on the booked SKU.",
        "<p><a href=\"/guides/shipping/\">US shipping lab</a> · <a href=\"/hipobuy-coupons/\">Coupons</a> · <a href=\"/is-hipobuy-legit/\">Legit</a></p>",
    ],
    extra=EXTRA["us"],
)

HOWTO["uk"] = how_to_article(
    "hipobuyspreadsheet.co.uk",
    "How to use HipoBuy on the UK spreadsheet desk",
    [
        "This is the <strong>.co.uk commercial desk</strong>: coupons and UK sizing, then a GB address in the app. It is not a redirect from or onto hipobuyspreadsheets.uk.",
        "<h2 class=\"ph\">1. GBP account</h2>",
        "Register on hipobuy.com with a UK street. Re-type the exclusive invite from /hipobuy-coupons/ — checked still showing on this host on the lab date. Do not put the string in titles.",
        "<h2 class=\"ph\">2. Size before you submit</h2>",
        "Open the sizing post. For a men’s trainer labelled EU 42 / US 9, start from <strong>UK 8</strong> and confirm insole millimetres on the QC photo. CN tags run small; Weidian titles are not a last measurement.",
        "<h2 class=\"ph\">3. Shortlist</h2>",
        "1–3 items. Finds in bulk live on .net. This desk keeps coupon + sizing URLs that already have their own jobs.",
        "<h2 class=\"ph\">4. QC, then freight</h2>",
        "Warehouse photos first. Royal Mail and Evri numbers belong on the haul-log host’s shipping lab; here you still estimate in-app after photos so GBP landed cost is not a surprise.",
        "<h2 class=\"ph\">5. Coupons expire</h2>",
        f"On {DATE} the exclusive card still listed the invite. Re-read the coupon article the day you register. HMRC notes stay educational.",
        "<h2 class=\"ph\">6. HMRC — educational only</h2>",
        "UK import VAT/duty follow the carrier product. <strong>No declared-value coaching.</strong>",
        "<h2 class=\"ph\">7. Do not merge UK hosts</h2>",
        "hipobuyspreadsheets.uk is the haul log (shipping + spreadsheet). This .co.uk host is coupons + sizing. Both stay independent.",
        "<h2 class=\"ph\">8. Track</h2>",
        "After export, keep HipoBuy tracking and the UK last-mile number. Name Great Britain in tickets, including if the parcel is destined for Northern Ireland on a different SKU.",
        "<h2 class=\"ph\">9. First GBP haul</h2>",
        "Size the trainers on this host, copy the invite from the coupon centre, then submit 1–3 items. Do not wait to “merge” this file onto the .uk haul log — they keep different jobs.",
        "<h2 class=\"ph\">10. What to store</h2>",
        "QC photos, weigh ticket, export scan, and the coupon screenshot from the day you registered. HMRC questions are slower without them. The sizing post keeps the UK 8 / EU 42 / US 9 sample dated 29 Sep 2026.",
        "<h2 class=\"ph\">11. Address format</h2>",
        "UK street, town, postcode, United Kingdom. A .eu IOSS SKU is another ticket. Royal Mail versus Evri numbers belong in the haul-log shipping lab; you still estimate in-app here so GBP is not a surprise.",
        "<h2 class=\"ph\">12. When coupons go stale</h2>",
        "Re-open /hipobuy-coupons/ the morning you register. The exclusive card was still showing on the lab date; that is not a promise it survives next month.",
        "<h2 class=\"ph\">13. Twin host</h2>",
        "hipobuyspreadsheets.uk keeps line codes and the spreadsheet log. This .co.uk host keeps coupons and sizing. Neither 301s to .net.",
        "<h2 class=\"ph\">14. Short FAQ</h2>",
        "Can I size from the Weidian title only? No. Can the invite live in the homepage title? No. Is Northern Ireland the same SKU as mainland GB? Often not — read the live line.",
        "<p><a href=\"/hipobuy-coupons/\">Coupon centre</a> · <a href=\"/blog/posts/hipobuy-sizing-guide/\">UK sizing</a> · <a href=\"/\">Catalogue</a></p>",
    ],
    extra=EXTRA["uk"],
)

HOWTO["eu"] = how_to_article(
    "hipobuyspreadsheet.eu",
    "How to use HipoBuy on the EU coupon desk",
    [
        "This host is the <strong>EU coupon desk</strong>. Put a real member-state street in HipoBuy. The .eu TLD is not a warehouse and not a 301 onto .net.",
        "<h2 class=\"ph\">1. Member-state address</h2>",
        "France, Spain, Italy, Ireland — type the street you actually ship to. AT and NL already have their own files; do not paste their calculators here.",
        "<h2 class=\"ph\">2. Invite from the coupon article</h2>",
        f"On {DATE} the exclusive card on this host still showed the invite used in the HipoBuy register flow. Re-type it in-app. It does not belong in a homepage title.",
        "<h2 class=\"ph\">3. Shortlist</h2>",
        "1–3 items. The 8,600-row browse stays on hipobuyspreadsheet.net.",
        "<h2 class=\"ph\">4. QC photos</h2>",
        "Lock size and defects in warehouse. Fiscal/IOSS treatment is a logistics SKU, not something you invent on this HTML page.",
        "<h2 class=\"ph\">5. Estimate the member-state</h2>",
        "Run the official estimator for the country on the label — not a generic “EU” row. Volumetric L×W×H/8000 still applies on most air lines.",
        "<h2 class=\"ph\">6. VAT — educational only</h2>",
        "IOSS and fiscal products are specific SKUs. <strong>No declared-value coaching.</strong>",
        "<h2 class=\"ph\">7. Track</h2>",
        "Name the member state in support tickets. A parcel to Portugal is not an AT Post file.",
        "<h2 class=\"ph\">8. What this desk is not</h2>",
        "Not the NL PostNL lab, not the AT Versand lab, not the UK sizing post. Coupons are the ranked URL on this host.",
        "<h2 class=\"ph\">9. One member state per ticket</h2>",
        "A haul to Madrid and a haul to Dublin are two HipoBuy destinations. Do not reuse an AT DHL-EUCR screenshot as if it were Ireland. Run the official estimator for the country printed on the label.",
        "<h2 class=\"ph\">10. Store the coupon check</h2>",
        "Keep a screenshot of the exclusive card from the day you registered. On 29 Sep 2026 it still listed the invite on this host. Re-type it in-app; this HTML is not a coupon API.",
        "<h2 class=\"ph\">11. Fiscal SKUs</h2>",
        "If HipoBuy offers an IOSS or fiscal product, that is a logistics SKU with its own constraints — not a paragraph you invent here. VAT notes stay educational.",
        "<h2 class=\"ph\">12. When to re-estimate</h2>",
        "After QC returns, extra filler, or a new carton. Volumetric L×W×H/8000 still dominates most air lines into the Union.",
        "<h2 class=\"ph\">13. Neighbours</h2>",
        "hipobuy.at and hipobuyspreadsheet.nl keep country labs. This .eu file keeps the coupon centre. No hreflang cluster.",
        "<h2 class=\"ph\">14. Short FAQ</h2>",
        "Does .eu mean the parcel ships to “Europe” as one country? No. May we clone the .net catalogue here? No. Invite in the title? No.",
        "<p><a href=\"/hipobuy-coupons/\">EU coupon centre</a> · <a href=\"/hipobuy-shipping-guide/\">EU shipping</a></p>",
    ],
    extra=EXTRA["eu"],
)

HOWTO["ukhaul"] = how_to_article(
    "hipobuyspreadsheets.uk",
    "How to use the HipoBuy UK haul log",
    [
        "This Nominet host is the <strong>haul log</strong>: shipping lines after warehouse photos, then the spreadsheet of what actually moved. It is not an alias of hipobuyspreadsheet.co.uk and must not 301 onto that coupon desk.",
        "<h2 class=\"ph\">1. GB address in the app</h2>",
        "Register on hipobuy.com with the UK street on the parcel. Invite still lives on the coupon URL; re-type it in-app.",
        "<h2 class=\"ph\">2. Spreadsheet as a log, not a clone of .net</h2>",
        "Use the catalogue on this homepage for the haul you are running. Brand directories such as /brand/moncler/ stay. The 8,600-row finds hub stays on .net.",
        "<h2 class=\"ph\">3. QC photos</h2>",
        "Photograph checks before you book Royal Mail or Evri. Size disputes are cheaper in warehouse than after HMRC.",
        "<h2 class=\"ph\">4. Line table from the lab date</h2>",
        f"On {DATE} HIPO-RoyalMail-GB-1 was about $23.83 for 1000&nbsp;g / 35×25×10&nbsp;cm (1100&nbsp;g volumetric). Evri-AF1 about $33.88. China Post SURFACE looked cheap in USD and quoted 60–90 workdays. Northern Ireland is often another carrier SKU.",
        "<h2 class=\"ph\">5. /guides/shipping/ already points here</h2>",
        "That path already lands on /hipobuy-shipping-guide/. Do not invent a third shipping IA.",
        "<h2 class=\"ph\">6. HMRC — educational only</h2>",
        "VAT/duty follow the booked product. <strong>No declared-value coaching.</strong>",
        "<h2 class=\"ph\">7. Track the haul</h2>",
        "Keep HipoBuy tracking plus Royal Mail or Evri numbers in the spreadsheet row. If a parcel stalls, attach warehouse receipt and last scan.",
        "<h2 class=\"ph\">8. Twin host</h2>",
        "Coupons and the UK 8 sizing sample live on .co.uk. This .uk host keeps the line log. Both files stay.",
        "<h2 class=\"ph\">9. Log the haul in the spreadsheet</h2>",
        "Each row: SKU, QC decision, billed grams, line code (Royal Mail vs Evri vs EMS), tracking, last scan. That is why this Nominet host exists. Brand folders stay; we do not PUT /brand/moncler/.",
        "<h2 class=\"ph\">10. First haul size</h2>",
        "One box you can actually estimate. The lab carton 35×25×10 at 1000&nbsp;g billed 1100&nbsp;g on Royal Mail. A weekend-bag carton will not match $23.83.",
        "<h2 class=\"ph\">11. Address and NI</h2>",
        "Mainland GB postcodes and Northern Ireland are often different live SKUs. Read the estimator country list; do not assume Evri covers every postcode the same way.",
        "<h2 class=\"ph\">12. When to re-estimate</h2>",
        "After QC returns or a new carton. SURFACE at 60–90 workdays is not a “cheap Royal Mail”. The 29 Sep 2026 table is a snapshot.",
        "<h2 class=\"ph\">13. /guides/shipping/</h2>",
        "Already lands on /hipobuy-shipping-guide/. No third shipping tree, no 301 onto .co.uk.",
        "<h2 class=\"ph\">14. Short FAQ</h2>",
        "Is this host the coupon centre? No. May we merge UK TLDs? No. Invite in the title? No — coupon URL and app.",
        "<p><a href=\"/hipobuy-shipping-guide/\">UK shipping lab</a> · <a href=\"/\">Catalogue</a> · <a href=\"/hipobuy-coupons/\">Coupons</a></p>",
    ],
    extra=EXTRA["ukhaul"],
)


def _word_count(html: str) -> int:
    text = re.sub(r"<[^>]+>", " ", html)
    return len(re.findall(r"[A-Za-zÄÖÜäöüßéèêáàóòúùíìç0-9']+", text))


def patch_howto(html: str, key: str) -> str:
    article = HOWTO[key]
    n = _word_count(article)
    if n < 800:
        raise ValueError(f"{key} how-to too short: {n} words")
    html = re.sub(
        r'<div style="max-width:720px;margin:56px auto;padding:0 24px 80px;text-align:center">.*?</div>\s*(?:<section class="[^"]*gsc-extra[^"]*"[^>]*>.*?</section>\s*)*',
        article + "\n",
        html,
        count=1,
        flags=re.S,
    )
    if "expand this stub using the HTML patterns documented" in html or "<code>README.md</code>" in html:
        raise ValueError(f"{key}: README stub still present")
    html = re.sub(
        r'<section class="[^"]*gsc-extra[^"]*"[^>]*>.*?</section>',
        "",
        html,
        flags=re.S,
    )
    howto_titles = {
        "at": (
            "Hipobuy anmelden: Spreadsheet nutzen 2026",
            "HipoBuy in Österreich nutzen: vom Konto bis zur Sendung",
        ),
        "nl": (
            "How to use the Hipobuy Spreadsheet",
            "HipoBuy in Nederland: van account tot levering",
        ),
        "us": (
            "How to use the Hipobuy Spreadsheet",
            "How to use HipoBuy for a United States haul",
        ),
        "uk": (
            "How to use the Hipobuy Spreadsheet",
            "How to use HipoBuy on the UK spreadsheet desk",
        ),
        "eu": (
            "How to use the Hipobuy Spreadsheet",
            "How to use HipoBuy on the EU coupon desk",
        ),
        "ukhaul": (
            "How to use the Hipobuy Spreadsheet",
            "How to use the HipoBuy UK haul log",
        ),
    }
    old_t, new_t = howto_titles[key]
    html = html.replace(f"<title>{old_t}</title>", f"<title>{new_t}</title>")
    html = html.replace(f'content="{old_t}"', f'content="{new_t}"')
    # Local meta: drop English clone descriptions where we have a unique H1
    return html, n


JOBS = [
    ("at-ship.html", lambda t: patch_shipping(t, "at")),
    ("nl-ship.html", lambda t: patch_shipping(t, "nl")),
    ("us-ship.html", lambda t: patch_shipping(t, "us")),
    ("ukhaul-ship.html", lambda t: patch_shipping(t, "ukhaul")),
    ("eu-coup.html", lambda t: patch_coupons(t, COUPON_NOTE_EU)),
    ("uk-coup.html", lambda t: patch_coupons(t, COUPON_NOTE_UK)),
    ("uk-size.html", patch_sizing),
]


def main() -> None:
    out_dir = Path("/tmp/cms-patched")
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, fn in JOBS:
        src = CMS / name
        html = src.read_text(encoding="utf-8", errors="replace")
        new = fn(html)
        dest = out_dir / name
        dest.write_text(new, encoding="utf-8")
        print(f"patched {name} {src.stat().st_size} -> {dest.stat().st_size}")
        if "expand this stub using the HTML patterns documented" in new or "<code>README.md</code>" in new:
            raise SystemExit(f"README leaked into {name}")
        if "gsc-extra" in new:
            print(f"  warn: gsc-extra remains in {name}")
        if "Search Console" in new or "Impression" in new:
            print(f"  warn: GSC wording in {name}")

    howto_map = {
        "at-how.html": "at",
        "nl-how.html": "nl",
        "us-how.html": "us",
        "uk-how.html": "uk",
        "eu-how.html": "eu",
        "ukhaul-how.html": "ukhaul",
    }
    for name, key in howto_map.items():
        src = CMS / name
        html = src.read_text(encoding="utf-8", errors="replace")
        new, n = patch_howto(html, key)
        dest = out_dir / name
        dest.write_text(new, encoding="utf-8")
        print(f"howto {name} words≈{n} {src.stat().st_size} -> {dest.stat().st_size}")
        if "expand this stub using the HTML patterns documented" in new or "<code>README.md</code>" in new:
            raise SystemExit(f"README remains {name}")
        if "gsc-extra" in new:
            print(f"  warn: gsc-extra remains in {name}")


if __name__ == "__main__":
    main()
