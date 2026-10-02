"""Dated CNY→local display conversion + catalogue chrome i18n for country desks.

X-Rates historical 1 Oct 2026 (units of local currency per 1 CNY).
This is a display conversion of the China warehouse card, not checkout.
"""
from __future__ import annotations

import json
from html import escape
from typing import Callable

FX_DATE = "1 Oct 2026"

# Inverse of X-Rates 2026-10-01 tables:
#   1 EUR = 7.522213 CNY  → 0.132940
#   1 USD = 6.706143 CNY  → 0.149117
#   1 CAD = 4.706361 CNY  → 0.212478
#   GBP via USD (1 USD = 0.758400 GBP)
#   AUD via USD (1 USD = 1.446817 AUD)
CNY_TO = {
    "EUR": 0.132940,
    "USD": 0.149117,
    "CAD": 0.212478,
    "GBP": 0.113091,
    "AUD": 0.215745,
    "PLN": 0.537200,
}

EXTRA_CSS_FX = """
.sg-card .pr-src{font-size:11px;font-weight:500;color:#94a3b8}
.sg-fx{color:#64748b;font-size:13px;line-height:1.55;margin:4px 0 10px;max-width:760px}
"""

CHIP_ALL = {
    "en": "All",
    "de": "Alle",
    "es": "Todo",
    "fr": "Tout",
    "it": "Tutti",
    "nl": "Alles",
}
CHIP_FALLBACK = {
    "bag": {
        "en": "Bags",
        "de": "Taschen",
        "es": "Bolsos",
        "fr": "Sacs",
        "it": "Borse",
        "nl": "Tassen",
    },
    "watch": {
        "en": "Watches",
        "de": "Uhren",
        "es": "Relojes",
        "fr": "Montres",
        "it": "Orologi",
        "nl": "Horloges",
    },
}

UI = {
    "en": {
        "ph": "Search sneakers, hoodie…",
        "ssub": "The catalogue on this homepage comes from /api/products/. Local-language words often return zero — type the English key (sneakers, hoodie).",
        "fx": "Prices in {ccy} are a display conversion of the China warehouse card (X-Rates mid-market, {date}, 1 CNY = {rate} {ccy}). Not a checkout price.",
        "count": "{n} on this page",
        "open": "Open",
        "empty": "No cards for that English key. Try sneakers or hoodie.",
        "err": "Catalogue API not reachable on this host yet.",
        "foot": "Independent information desk on {host}. Not the official {brand} site. Sister country hosts stay separate files — no 301.",
        "on_host": "On this host",
        "official": "Official",
        "contact": "Contact",
        "freight": "Freight estimate",
        "register": "Register",
        "indep": "independent desk",
        "choose_lang": "Choose language or region",
        "menu": "Menu",
        "desks": "Independent desks",
        "en_group": "English",
        "local_group": "Local editions",
        "register_on": "Register on {brand} →",
        "privacy": "Privacy",
        "cookies": "Cookies",
    },
    "de": {
        "ph": "Sneakers, Hoodie suchen…",
        "ssub": "Der Katalog auf dieser Startseite kommt von /api/products/. Deutsche Wörter liefern oft null Treffer — englische Keys nutzen (sneakers, hoodie).",
        "fx": "Preise in {ccy} sind eine Anzeigeumrechnung der China-Lagerkarte (X-Rates, {date}, 1 CNY = {rate} {ccy}). Kein Kassenpreis.",
        "count": "{n} auf dieser Seite",
        "open": "Öffnen",
        "empty": "Keine Karten für diesen englischen Suchbegriff. Probier sneakers oder hoodie.",
        "err": "Katalog-API auf diesem Host noch nicht erreichbar.",
        "foot": "Unabhängiger Infodesk auf {host}. Nicht die offizielle {brand}-Seite. Schwester-Länderhosts bleiben eigene Dateien — kein 301.",
        "on_host": "Auf diesem Host",
        "official": "Offiziell",
        "contact": "Kontakt",
        "freight": "Fracht-Schätzer",
        "register": "Registrieren",
        "indep": "unabhängiger Desk",
        "choose_lang": "Sprache oder Region wählen",
        "menu": "Menü",
        "desks": "Unabhängige Desks",
        "en_group": "Englisch",
        "local_group": "Lokale Ausgaben",
        "register_on": "Auf {brand} registrieren →",
        "privacy": "Datenschutz",
        "cookies": "Cookies",
    },
    "es": {
        "ph": "Buscar sneakers, hoodie…",
        "ssub": "El catálogo de esta portada sale de /api/products/. Palabras en español suelen devolver cero — usa la clave inglesa (sneakers, hoodie).",
        "fx": "Los precios en {ccy} son una conversión de visualización de la ficha de almacén en China (X-Rates, {date}, 1 CNY = {rate} {ccy}). No es el precio de caja.",
        "count": "{n} en esta página",
        "open": "Abrir",
        "empty": "No hay fichas para esa clave inglesa. Prueba sneakers o hoodie.",
        "err": "La API del catálogo aún no responde en este host.",
        "foot": "Escritorio de información independiente en {host}. No es el sitio oficial de {brand}. Los hosts hermanos siguen en archivos separados — sin 301.",
        "on_host": "En este host",
        "official": "Oficial",
        "contact": "Contacto",
        "freight": "Estimador de envío",
        "register": "Registrarse",
        "indep": "escritorio independiente",
        "choose_lang": "Elegir idioma o región",
        "menu": "Menú",
        "desks": "Escritorios independientes",
        "en_group": "Inglés",
        "local_group": "Ediciones locales",
        "register_on": "Registrarse en {brand} →",
        "privacy": "Privacidad",
        "cookies": "Cookies",
    },
    "fr": {
        "ph": "Rechercher sneakers, hoodie…",
        "ssub": "Le catalogue de cette accueil vient de /api/products/. Les mots français renvoient souvent zéro — tapez la clé anglaise (sneakers, hoodie).",
        "fx": "Les prix en {ccy} sont une conversion d’affichage de la fiche entrepôt Chine (X-Rates, {date}, 1 CNY = {rate} {ccy}). Ce n’est pas un prix de caisse.",
        "count": "{n} sur cette page",
        "open": "Ouvrir",
        "empty": "Aucune fiche pour cette clé anglaise. Essayez sneakers ou hoodie.",
        "err": "L’API catalogue n’est pas encore joignable sur cet hôte.",
        "foot": "Desk d’information indépendant sur {host}. Pas le site officiel {brand}. Les hôtes sœurs restent des fichiers séparés — pas de 301.",
        "on_host": "Sur cet hôte",
        "official": "Officiel",
        "contact": "Contact",
        "freight": "Estimateur de fret",
        "register": "S’inscrire",
        "indep": "desk indépendant",
        "choose_lang": "Choisir la langue ou la région",
        "menu": "Menu",
        "desks": "Desks indépendants",
        "en_group": "Anglais",
        "local_group": "Éditions locales",
        "register_on": "S’inscrire sur {brand} →",
        "privacy": "Confidentialité",
        "cookies": "Cookies",
    },
    "it": {
        "ph": "Cerca sneakers, hoodie…",
        "ssub": "Il catalogo di questa home arriva da /api/products/. Le parole italiane spesso danno zero — usa la chiave inglese (sneakers, hoodie).",
        "fx": "I prezzi in {ccy} sono una conversione di visualizzazione della scheda magazzino Cina (X-Rates, {date}, 1 CNY = {rate} {ccy}). Non è il prezzo di cassa.",
        "count": "{n} in questa pagina",
        "open": "Apri",
        "empty": "Nessuna scheda per questa chiave inglese. Prova sneakers o hoodie.",
        "err": "API del catalogo non ancora raggiungibile su questo host.",
        "foot": "Desk informativo indipendente su {host}. Non è il sito ufficiale {brand}. Gli host fratelli restano file separati — niente 301.",
        "on_host": "Su questo host",
        "official": "Ufficiale",
        "contact": "Contatto",
        "freight": "Stima spedizione",
        "register": "Registrati",
        "indep": "desk indipendente",
        "choose_lang": "Scegli lingua o regione",
        "menu": "Menu",
        "desks": "Desk indipendenti",
        "en_group": "Inglese",
        "local_group": "Edizioni locali",
        "register_on": "Registrati su {brand} →",
        "privacy": "Privacy",
        "cookies": "Cookie",
    },
    "nl": {
        "ph": "Zoek sneakers, hoodie…",
        "ssub": "De catalogus op deze homepage komt van /api/products/. Nederlandse woorden geven vaak nul — gebruik de Engelse key (sneakers, hoodie).",
        "fx": "Prijzen in {ccy} zijn een weergaveconversie van de China-voorraadkaart (X-Rates, {date}, 1 CNY = {rate} {ccy}). Geen kassaprijs.",
        "count": "{n} op deze pagina",
        "open": "Openen",
        "empty": "Geen kaarten voor die Engelse zoekterm. Probeer sneakers of hoodie.",
        "err": "Catalogus-API is op deze host nog niet bereikbaar.",
        "foot": "Onafhankelijke infodesk op {host}. Niet de officiële {brand}-site. Zushosts blijven aparte bestanden — geen 301.",
        "on_host": "Op deze host",
        "official": "Officieel",
        "contact": "Contact",
        "freight": "Vracht-schatter",
        "register": "Registreren",
        "indep": "onafhankelijke desk",
        "choose_lang": "Kies taal of regio",
        "menu": "Menu",
        "desks": "Onafhankelijke desks",
        "en_group": "Engels",
        "local_group": "Lokale edities",
        "register_on": "Registreren op {brand} →",
        "privacy": "Privacy",
        "cookies": "Cookies",
    },
}

CAT_CHIP_ROWS = [
    ("all", ""),
    ("sneakers", "sneakers"),
    ("hoodie", "hoodie"),
    ("t-shirt", "t-shirt"),
    ("jacket", "jacket"),
    ("bag", "bag"),
    ("watch", "watch"),
]


def ui_copy(lang: str) -> dict:
    return UI.get(lang, UI["en"])


def currency_for(key: str, d: dict) -> str:
    if d.get("ccy"):
        return d["ccy"]
    dest = (d.get("dest") or "").upper()
    if dest in {"AT", "IT", "ES", "FR", "NL", "DE"} or key == "eu":
        return "EUR"
    if dest in {"GB", "UK"}:
        return "GBP"
    if dest == "CA":
        return "CAD"
    if dest == "AU":
        return "AUD"
    if dest == "PL":
        return "PLN"
    return "USD"


def chip_label(lang: str, slug: str, cat_labels: dict) -> str:
    if slug == "all":
        return CHIP_ALL.get(lang, CHIP_ALL["en"])
    labels = cat_labels.get(lang) or cat_labels.get("en") or {}
    if slug == "bag":
        return labels.get("bags") or CHIP_FALLBACK["bag"].get(lang, "Bags")
    if slug == "watch":
        return labels.get("watches") or CHIP_FALLBACK["watch"].get(lang, "Watches")
    return labels.get(slug, slug.replace("-", " ").title())


def catalog_block(
    key: str,
    d: dict,
    *,
    register_url: str,
    loc_fn: Callable[[str], str],
    cat_labels: dict,
) -> str:
    lang = loc_fn(key)
    u = ui_copy(lang)
    ccy = currency_for(key, d)
    rate = CNY_TO[ccy]
    chips = "".join(
        f'<button type="button" data-q="{escape(q)}" class="{"on" if slug == "all" else ""}">{escape(chip_label(lang, slug, cat_labels))}</button>'
        for slug, q in CAT_CHIP_ROWS
    )
    fx_note = u["fx"].format(ccy=ccy, date=FX_DATE, rate=f"{rate:.6f}")
    fx_ccy_js = json.dumps(ccy)
    fx_rate_js = json.dumps(rate)
    fx_locale_js = json.dumps(d["lang"])
    open_js = json.dumps(u["open"], ensure_ascii=False)
    count_js = json.dumps(u["count"], ensure_ascii=False)
    empty_js = json.dumps(u["empty"], ensure_ascii=False)
    err_js = json.dumps(u["err"], ensure_ascii=False)
    reg_js = json.dumps(register_url)
    return f"""
<section class="sg-mw" id="catalog">
  <p class="ssub">{escape(u["ssub"])}</p>
  <p class="sg-fx">{escape(fx_note)}</p>
  <div class="sg-chips">{chips}</div>
  <div class="sg-fbar">
    <input id="sg-q" type="search" placeholder="{escape(u["ph"])}">
    <span id="sg-count"></span>
  </div>
  <div class="sg-grid" id="sg-grid"></div>
</section>
<script>
(function(){{
  var PAPI='/api/products/';
  var q='';
  var W2C_IMG='https://w2clinks.com';
  var FX_CCY={fx_ccy_js};
  var FX_RATE={fx_rate_js};
  var FX_LOCALE={fx_locale_js};
  var OPEN_LAB={open_js};
  var COUNT_TPL={count_js};
  var EMPTY_MSG={empty_js};
  var ERR_MSG={err_js};
  var REG={reg_js};
  function absImg(u){{
    if(!u) return '';
    u=String(u);
    if(/^https?:\\/\\//i.test(u)) return u;
    if(u.indexOf('//')===0) return 'https:'+u;
    if(u.charAt(0)==='/') return W2C_IMG+u;
    return W2C_IMG+'/'+u.replace(/^\\/+/, '');
  }}
  function fmtMoney(it){{
    var src=String(it.currency||'CNY').toUpperCase();
    var n=parseFloat(String(it.price||'').replace(/,/g,'.'));
    if(!isFinite(n)) return {{local:'', srcCcy:src, src:(it.currency||'')+' '+(it.price||'')}};
    var localN=n;
    if(src==='CNY' && FX_CCY!=='CNY') localN=n*FX_RATE;
    else if(src!==FX_CCY && src!=='CNY') localN=n;
    var local='';
    try {{ local=new Intl.NumberFormat(FX_LOCALE,{{style:'currency',currency:FX_CCY}}).format(localN); }}
    catch(e){{ local=FX_CCY+' '+localN.toFixed(2); }}
    var srcLab=src+' '+String(it.price);
    return {{local:local, srcCcy:src, src:srcLab}};
  }}
  function render(data){{
    var items=data.items||data.products||[];
    var g=document.getElementById('sg-grid');
    var c=document.getElementById('sg-count');
    if(c) c.textContent=COUNT_TPL.replace('{{n}}', String(items.length));
    g.innerHTML='';
    items.forEach(function(it){{
      var el=document.createElement('article');
      el.className='sg-card';
      var img=document.createElement('img');
      img.src=absImg(it.image||''); img.alt=it.title||''; img.loading='lazy';
      img.referrerPolicy='no-referrer'; img.decoding='async';
      var b=document.createElement('div'); b.className='b';
      var t=document.createElement('div'); t.className='t'; t.textContent=it.title||'';
      var m=fmtMoney(it);
      var p=document.createElement('div'); p.className='pr'; p.textContent=m.local||m.src;
      b.appendChild(t); b.appendChild(p);
      if(m.srcCcy==='CNY' && FX_CCY!=='CNY' && m.local){{
        var s=document.createElement('div'); s.className='pr-src'; s.textContent=m.src;
        b.appendChild(s);
      }}
      var a=document.createElement('a'); a.className='buy'; a.target='_blank'; a.rel='noopener sponsored';
      a.href=it.href||it.target||REG; a.textContent=OPEN_LAB;
      el.appendChild(img); el.appendChild(b); el.appendChild(a);
      g.appendChild(el);
    }});
    if(!items.length){{
      var empty=document.createElement('p'); empty.textContent=EMPTY_MSG; g.appendChild(empty);
    }}
  }}
  function load(){{
    var u=new URL(PAPI, location.origin);
    if(q) u.searchParams.set('q', q);
    u.searchParams.set('limit','24');
    u.searchParams.set('page','1');
    fetch(u, {{headers:{{'Accept':'application/json'}}}}).then(function(r){{return r.json();}}).then(render).catch(function(){{
      var g=document.getElementById('sg-grid');
      g.innerHTML='';
      var err=document.createElement('p'); err.textContent=ERR_MSG; g.appendChild(err);
    }});
  }}
  function applyQ(next){{
    q=next||'';
    var inp=document.getElementById('sg-q');
    if(inp) inp.value=q;
    document.querySelectorAll('.sg-chips button').forEach(function(x){{
      x.classList.toggle('on', (x.getAttribute('data-q')||'')===q);
    }});
    load();
  }}
  document.querySelectorAll('.sg-chips button').forEach(function(b){{
    b.addEventListener('click', function(){{ applyQ(b.getAttribute('data-q')||''); }});
  }});
  document.querySelectorAll('a.sg-cat[data-q]').forEach(function(a){{
    a.addEventListener('click', function(ev){{
      ev.preventDefault();
      applyQ(a.getAttribute('data-q')||'');
      var cat=document.getElementById('catalog');
      if(cat) cat.scrollIntoView({{behavior:'smooth',block:'start'}});
    }});
  }});
  var inp=document.getElementById('sg-q');
  var t=null;
  inp.addEventListener('input', function(){{
    clearTimeout(t); t=setTimeout(function(){{ q=inp.value.trim(); load(); }}, 250);
  }});
  load();
}})();
</script>
"""
