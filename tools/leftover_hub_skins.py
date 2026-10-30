#!/usr/bin/env python3
"""Skin leftover Georgia / #local hub shells with the same CMS chrome as the 48 dests.

Does not overwrite unique PHP/CMS (wemimi.net, hubbuy.net, hipobuyspreadsheet.net,
fashionrepsspreadsheet.com, CSSBuy PHP AT/ES/FR/IT/NL, HipoBuy gold dests).
Does not skin twins that already 301 into a dest or unique hub.
Ranked inner HTML is wrapped, not replaced with a 5KB overlay.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

import dest_inner_chrome as inner
import hub_skin_desks as skin
from hub_skin_desks import AGENTS, HOSTS, _facts, build_home, theme_css

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sites"
DATE = "2 Oct 2026"
CMS_CSS = OUT / "shared" / "desk-cms.css"


def A(**kw):
    return kw


def H(**kw):
    return kw


EXTRA_AGENTS = {
    "BaseTao": A(
        primary="#e11d48",
        soft="#fff1f2",
        nav="#1f2937",
        logo="/assets/images/basetao-logo.png",
        official="https://www.basetao.com/",
        estimator="https://www.basetao.com/best-taobao-agent-service/how_make/cost.html",
        register="https://www.basetao.com/",
        storage="Official BaseTao FAQ: 120 days free storage; confirm that live article the morning you ship",
        codes=[],
        css=["/assets/css/desk-cms.css", "/assets/css/basetao-theme.css"],
    ),
    "BoonBuy": A(
        primary="#2563eb",
        soft="#eff6ff",
        nav="#1e3a8a",
        logo="/assets/images/boonbuy-logo.png",
        official="https://boonbuy.com/",
        estimator="https://boonbuy.com/shipping-estimate",
        register="https://boonbuy.com/",
        storage="Official BoonBuy Help is an SPA; confirm that live copy the morning you ship",
        codes=[],
        css=["/assets/css/desk-cms.css", "/assets/css/boonbuy-theme.css"],
    ),
    "CNShopper": A(
        primary="#dc2626",
        soft="#fef2f2",
        nav="#7f1d1d",
        logo="/assets/images/cnshopper-logo.svg",
        official="https://www.cnshopper.com/en",
        estimator="https://www.cnshopper.com/en/estimate",
        register="https://www.cnshopper.com/en",
        storage="Official CNShopper Help is the live site; confirm that copy the morning you ship",
        codes=[],
        css=["/assets/css/desk-cms.css", "/assets/css/cnshopper-theme.css"],
    ),
    "FishGoo": A(
        primary="#0d9488",
        soft="#f0fdfa",
        nav="#134e4a",
        logo="/assets/images/fishgoo-logo.svg",
        official="https://www.fishgoo.com/",
        estimator="https://www.fishgoo.com/estimation",
        register="https://www.fishgoo.com/",
        storage="Official FishGoo app storage notice; confirm that live copy the morning you ship",
        codes=[],
        css=["/assets/css/desk-cms.css", "/assets/css/fishgoo-theme.css"],
    ),
    "HipoBuy": A(
        primary="#15803d",
        soft="#f0fdf4",
        nav="#14532d",
        logo="/assets/images/hipobuy-wordmark.png",
        official="https://hipobuy.com/",
        estimator="https://hipobuy.com/estimation",
        register="https://hipobuy.com/",
        storage="Official HipoBuy Help is an SPA; confirm that live copy the morning you ship",
        codes=[],
        css=["/assets/css/desk-cms.css", "/assets/css/hipobuy-theme.css"],
    ),
    "HubBuy": A(
        primary="#1d4ed8",
        soft="#eff6ff",
        nav="#1e3a8a",
        logo="/assets/images/hubbuy-logo.svg",
        official="https://www.hubbuyer.com/",
        estimator="https://www.hubbuyer.com/shipping",
        register="https://www.hubbuyer.com/",
        storage="Official HubBuyer FAQ: free the first month, then the membership plan; confirm that live article the morning you ship",
        codes=[],
        css=["/assets/css/desk-cms.css", "/assets/css/hubbuy-theme.css"],
    ),
    "Kakobuy": A(
        primary="#0284c7",
        soft="#e0f2fe",
        nav="#0c4a6e",
        logo="/assets/images/kakobuy-logo.png",
        official="https://www.kakobuy.com/",
        estimator="https://www.kakobuy.com/tools/estimate",
        register="https://www.kakobuy.com/",
        storage="Official Kakobuy Help is the live site; confirm storage there the morning you ship",
        codes=[],
        css=["/assets/css/desk-cms.css", "/assets/css/kakobuy-theme.css"],
    ),
    "OSSBuy": A(
        primary="#ea580c",
        soft="#fff7ed",
        nav="#9a3412",
        logo="/assets/images/ossbuy-logo.png",
        official="https://www.ossbuy.com/",
        estimator="https://www.ossbuy.com/freight-estimate",
        register="https://www.ossbuy.com/",
        storage="Official OSSBuy Help; confirm that live copy the morning you ship",
        codes=[],
        css=["/assets/css/desk-cms.css", "/assets/css/ossbuy-theme.css"],
    ),
    "WeMimi": A(
        primary="#7c3aed",
        soft="#f5f3ff",
        nav="#4c1d95",
        logo="/assets/images/wemimi-logo.svg",
        official="https://www.wemimi.com/",
        estimator="https://www.wemimi.com/",
        register="https://www.wemimi.com/",
        storage="Official WeMimi app storage notice; confirm that live copy the morning you ship",
        codes=[],
        css=["/assets/css/desk-cms.css", "/assets/css/wemimi-theme.css"],
    ),
    "GoatedBuy": A(
        primary="#111827",
        soft="#f3f4f6",
        nav="#030712",
        logo="/assets/images/goatedbuy-logo.png",
        official="https://goatedbuy.com/",
        estimator="https://goatedbuy.com/#/pages/estimation/shipping",
        register="https://goatedbuy.com/",
        storage="Official GoatedBuy Help is an SPA; confirm that live copy the morning you ship",
        codes=[],
        css=["/assets/css/desk-cms.css", "/assets/css/goatedbuy-theme.css"],
    ),
    "PikoBuy": A(
        primary="#db2777",
        soft="#fdf2f8",
        nav="#9d174d",
        logo="/assets/images/pikobuy-logo.png",
        official="https://www.pikobuy.com/",
        estimator="https://www.pikobuy.com/",
        register="https://www.pikobuy.com/",
        storage="Official PikoBuy Help is in the live app; confirm that copy the morning you ship",
        codes=[],
        css=["/assets/css/desk-cms.css", "/assets/css/pikobuy-theme.css"],
    ),
    "LoLoBuy": A(
        primary="#f97316",
        soft="#fff7ed",
        nav="#9a3412",
        logo="/assets/images/lolobuy-logo.png",
        official="https://www.lolobuy.com/",
        estimator="https://www.lolobuy.com/estimation",
        register="https://www.lolobuy.com/",
        storage="Official LoLoBuy Help is an SPA; confirm that live copy the morning you ship",
        codes=[],
        css=["/assets/css/desk-cms.css", "/assets/css/lolobuy-theme.css"],
    ),
    "EastMallBuy": A(
        primary="#0ea5e9",
        soft="#f0f9ff",
        nav="#075985",
        logo="/assets/images/eastmallbuy-logo.png",
        official="https://eastmallbuy.com/web/#/home",
        estimator="https://eastmallbuy.com/web/#/estimate",
        register="https://eastmallbuy.com/web/#/home",
        storage="Official EastMallBuy Help Center; confirm that live copy the morning you ship",
        codes=[],
        css=["/assets/css/desk-cms.css", "/assets/css/eastmallbuy-theme.css"],
    ),
    "FSBuy": A(
        primary="#4f46e5",
        soft="#eef2ff",
        nav="#312e81",
        logo="/assets/images/fsbuy-logo.png",
        official="https://fsbuy.com/",
        estimator="https://fsbuy.com/#/estimation",
        register="https://fsbuy.com/",
        storage="Official FSBuy homepage storage notice; confirm that live copy the morning you ship",
        codes=[],
        css=["/assets/css/desk-cms.css", "/assets/css/fsbuy-theme.css"],
    ),
    "GTbuy": A(
        primary="#16a34a",
        soft="#f0fdf4",
        nav="#14532d",
        logo="/assets/images/gtbuy-logo.png",
        official="https://www.gtbuy.com/",
        estimator="https://www.gtbuy.com/estimation",
        register="https://www.gtbuy.com/",
        storage="Official GTbuy Help; confirm that live copy the morning you ship",
        codes=[],
        css=["/assets/css/desk-cms.css", "/assets/css/gtbuy-theme.css"],
    ),
    "iTaoBuy": A(
        primary="#0891b2",
        soft="#ecfeff",
        nav="#155e75",
        logo="/assets/images/itaobuy-logo.png",
        official="https://www.itaobuy.com/",
        estimator="https://www.itaobuy.com/freight-estimate",
        register="https://www.itaobuy.com/",
        storage="Official iTaoBuy Help; confirm that live copy the morning you ship",
        codes=[],
        css=["/assets/css/desk-cms.css", "/assets/css/itaobuy-theme.css"],
    ),
    "PinguBuy": A(
        primary="#2563eb",
        soft="#eff6ff",
        nav="#1e3a8a",
        logo="/assets/images/pingubuy-logo.png",
        official="https://www.pingubuy.com/",
        estimator="https://www.pingubuy.com/estimates",
        register="https://www.pingubuy.com/",
        storage="Official PinguBuy Help Center; confirm that live copy the morning you ship",
        codes=[],
        css=["/assets/css/desk-cms.css", "/assets/css/pingubuy-theme.css"],
    ),
    "SpanBuy": A(
        primary="#FF6B00",
        soft="#FFF4EB",
        nav="#E05E00",
        logo="/assets/images/official-logo.png",
        official="https://www.spanbuy.com/en",
        estimator="https://www.spanbuy.com/en/estimate",
        register="https://www.spanbuy.com/en",
        storage="Official SpanBuy Help; confirm that live copy the morning you ship",
        codes=[],
        css=["/assets/css/desk-cms.css", "/assets/css/spanbuy-theme.css"],
    ),
}

LEFTOVER = {
    "mycnbox.eu": H(
        agent="MyCNBox", dest=None, loc="en", lang="en", ccy="EUR",
        dest_label="a country in the estimator",
        title="MyCNBox.eu — not a customs territory; pick a member-state",
        h1="MyCNBox.eu is not a customs territory — pick a real country",
        keep=[("/mycnbox-refund-guide/", "Refund guide"), ("/mycnbox-shipping-guide/", "Shipping"), ("/how-to-use-mycnbox/", "How to use"), ("/mycnbox-spreadsheet/", "Spreadsheet")],
    ),
    "mycnboxhaul.com": H(
        agent="MyCNBox", dest=None, loc="en", lang="en", ccy="USD",
        dest_label="a country in the estimator",
        title="MyCNBox haul SOP — not a customs territory",
        h1="This haul hostname is not a customs territory",
        keep=[("/spreadsheet-finds/", "Spreadsheet finds"), ("/shipping-calculator/", "Shipping"), ("/help/", "Help"), ("/reviews/", "Reviews")],
    ),
    "fansbuy.eu": H(
        agent="FansBuy", dest=None, loc="en", lang="en", ccy="EUR",
        dest_label="a country in the estimator",
        title="FansBuy.eu — not a customs territory; pick a member-state",
        h1="FansBuy.eu is not a customs territory — pick a real country",
        keep=[("/fansbuy-shipping-guide/", "Shipping"), ("/fansbuy-spreadsheet/", "Spreadsheet"), ("/how-to-use-fansbuy/", "How to use"), ("/is-fansbuy-legit/", "Legit?")],
    ),
    "fansbuysheets.net": H(
        agent="FansBuy", dest=None, loc="en", lang="en", ccy="USD",
        dest_label="a country in the estimator",
        title="FansBuy sheets hub — not a customs territory",
        h1="This .net hostname is not a customs territory",
        keep=[("/fansbuy-coupons/", "Coupons"), ("/fansbuy-shipping-guide/", "Shipping"), ("/fansbuy-invite-code/", "Invite article"), ("/fansbuy-spreadsheet/", "Spreadsheet")],
    ),
    "lovegobuyspreadsheet.eu": H(
        agent="LoveGoBuy", dest=None, loc="en", lang="en", ccy="EUR",
        dest_label="a country in the estimator",
        title="LoveGoBuy EU spreadsheet hub — pick a country in the estimator",
        h1="This .eu hostname is not a customs territory",
        keep=[("/lovegobuy-europe/", "Europe notes"), ("/lovegobuy-spreadsheet/", "Spreadsheet"), ("/lovegobuy-shipping-eu/", "Shipping"), ("/is-lovegobuy-legit/", "Is it legit?")],
    ),
    "lovegobuyguide.com": H(
        agent="LoveGoBuy", dest=None, loc="en", lang="en", ccy="USD",
        dest_label="a country in the estimator",
        title="LoveGoBuy global desk — pick a country in the estimator",
        h1="This hostname is not a customs territory",
        keep=[("/lovegobuy-spreadsheet/", "Spreadsheet"), ("/is-lovegobuy-legit/", "Is it legit?"), ("/how-to-use-lovegobuy/", "How to use"), ("/lovegobuy-shipping/", "Shipping")],
    ),
    "ootdbuyspreadsheet.net": H(
        agent="OOTDBuy", dest=None, loc="en", lang="en", ccy="USD",
        dest_label="a country in the estimator",
        title="OOTDBuy .net hub — not a customs territory",
        h1="This .net hostname is not a customs territory — pick a real country",
        keep=[("/ootdbuy-coupon-2026.html", "Coupon pack"), ("/categories/", "Categories"), ("/how-to-buy-from-china-2026.html", "How to buy"), ("/best-ootdbuy-spreadsheet-2026.html", "Spreadsheet 2026")],
    ),
    "ootdbuyspreadsheet.org": H(
        agent="OOTDBuy", dest=None, loc="en", lang="en", ccy="USD",
        dest_label="a country in the estimator",
        title="OOTDBuy .org hub — not a customs territory",
        h1="This .org hostname is not a customs territory — pick a real country",
        keep=[("/is-ootdbuy-legit/", "Legit?"), ("/ootdbuy-spreadsheet/", "Spreadsheet"), ("/ootdbuy-shipping-guide/", "Shipping"), ("/ootdbuy-coupons/", "Coupons")],
    ),
    "cssbuyspreadsheet.eu": H(
        agent="CSSBuy", dest=None, loc="en", lang="en", ccy="EUR",
        dest_label="a country in the estimator",
        title="CSSBuy.eu spreadsheet hub — not a customs territory",
        h1="This .eu hostname is not a customs territory — pick a real country",
        keep=[("/spreadsheet/", "Spreadsheet"), ("/faq/", "FAQ"), ("/guides/", "Guides"), ("/guides/shipping/", "Shipping")],
    ),
    "basetaospreadsheet.com": H(
        agent="BaseTao", dest=None, loc="en", lang="en", ccy="USD",
        dest_label="a country in the estimator",
        title="BaseTao .com hub — not a customs territory",
        h1="This .com hostname is not a customs territory — pick a real country",
        keep=[("/basetao-referral-code/", "Referral"), ("/basetao-shipping-calculator/", "Shipping calculator"), ("/basetao-calculator/", "Haul calculator"), ("/basetao-review/", "Review")],
    ),
    "boonspreadsheet.com": H(
        agent="BoonBuy", dest=None, loc="en", lang="en", ccy="USD",
        dest_label="a country in the estimator",
        title="BoonBuy .com hub — not a customs territory",
        h1="This .com hostname is not a customs territory — pick a real country",
        keep=[("/boonbuy-coupons/", "Coupons"), ("/is-boonbuy-legit/", "Legit?"), ("/boonbuy-shipping-guide/", "Shipping"), ("/boonbuy-spreadsheet-2026/", "Spreadsheet 2026")],
    ),
    "cnshopper.net": H(
        agent="CNShopper", dest=None, loc="en", lang="en", ccy="USD",
        dest_label="a country in the estimator",
        title="CNShopper.net hub — not a customs territory",
        h1="This .net hostname is not a customs territory — pick a real country",
        keep=[("/cnshopper-spreadsheet-2026.html", "Spreadsheet 2026"), ("/cnshopper-coupon-tracker-2026.html", "Coupons"), ("/is-cnshopper-legit.html", "Legit?"), ("/cnshopper-shipping-lines-2026.html", "Shipping")],
    ),
    "cnshopperspreadsheet.net": H(
        agent="CNShopper", dest=None, loc="en", lang="en", ccy="USD",
        dest_label="a country in the estimator",
        title="CNShopper spreadsheet hub — not a customs territory",
        h1="This spreadsheet hostname is not a customs territory",
        keep=[("/cnshopperspread-user-reports-2026.html", "User reports"), ("/cnshopperspread-coupon-tracker-2026.html", "Coupons"), ("/cnshopperspread-shipping-lines-2026.html", "Shipping"), ("/shoes/", "Shoes")],
    ),
    "fishgoospreadsheet.net": H(
        agent="FishGoo", dest=None, loc="en", lang="en", ccy="USD",
        dest_label="a country in the estimator",
        title="FishGoo .net hub — not a customs territory",
        h1="This .net hostname is not a customs territory — pick a real country",
        keep=[("/fishgoo-spreadsheet.html", "Spreadsheet"), ("/fishgoo-rimowa-spreadsheet/", "Rimowa"), ("/shipping-guide.html", "Shipping"), ("/comparisons.html", "Comparisons")],
    ),
    "hipobuyreview.com": H(
        agent="HipoBuy", dest=None, loc="en", lang="en", ccy="USD",
        dest_label="a country in the estimator",
        title="HipoBuy review hub — not a customs territory",
        h1="This .com hostname is not a customs territory — pick a real country",
        keep=[("/hipobuy-coupons/", "Coupons"), ("/is-hipobuy-legit/", "Legit?"), ("/hipobuy-shipping-guide/", "Shipping"), ("/hipobuy-spreadsheet/", "Spreadsheet")],
    ),
    "kakobuydocs.com": H(
        agent="Kakobuy", dest=None, loc="en", lang="en", ccy="USD",
        dest_label="a country in the estimator",
        title="KakobuyDocs hub — not a customs territory",
        h1="This hostname is not a customs territory — pick a real country",
        keep=[("/kakobuy-shoes-spreadsheet/", "Shoes spreadsheet"), ("/kakobuy-spreadsheet/", "Spreadsheet"), ("/how-to-use-kakobuy/", "How to use"), ("/is-kakobuy-legit/", "Legit?")],
    ),
    "ossbuyspreadsheets.org": H(
        agent="OSSBuy", dest=None, loc="en", lang="en", ccy="USD",
        dest_label="a country in the estimator",
        title="OSSBuy .org hub — not a customs territory",
        h1="This .org hostname is not a customs territory — pick a real country",
        keep=[("/ossbuy-coupons/", "Coupons"), ("/ossbuy-shipping-guide/", "Shipping"), ("/is-ossbuy-legit/", "Legit?"), ("/ossbuy-spreadsheet/", "Spreadsheet")],
    ),
    "wemimispreadsheet.com": H(
        agent="WeMimi", dest=None, loc="en", lang="en", ccy="USD",
        dest_label="a country in the estimator",
        title="WeMimi spreadsheet.com hub — not a customs territory",
        h1="This .com hostname is not a customs territory — pick a real country",
        keep=[("/shoes381/", "Shoes"), ("/wemimispread-coupon-tracker-2026.html", "Coupons"), ("/wemimispread-user-reports-2026.html", "Reports"), ("/wemimispread-shipping-lines-2026.html", "Shipping")],
    ),
    "hubbuyspreadsheet.net": H(
        agent="HubBuy", dest=None, loc="en", lang="en", ccy="USD",
        dest_label="a country in the estimator",
        title="HubBuy spreadsheet.net hub — not a customs territory",
        h1="This .net hostname is not a customs territory — pick a real country",
        keep=[("/hubbuy-guide/", "Beginner guide"), ("/hubbuy-spreadsheet/", "Spreadsheet"), ("/comparisons/", "Comparisons"), ("/hubbuy-coupons/", "Coupons")],
    ),
    "goatedspreadsheet.com": H(
        agent="GoatedBuy", dest=None, loc="en", lang="en", ccy="USD",
        dest_label="a country in the estimator",
        title="GoatedBuy .com hub — not a customs territory",
        h1="This .com hostname is not a customs territory — pick a real country",
        keep=[("/goatedbuy-coupons/", "Coupons"), ("/is-goatedbuy-legit/", "Legit?"), ("/goatedbuy-spreadsheet/", "Spreadsheet"), ("/goatedbuy-shipping-guide/", "Shipping")],
    ),
    "pikospreadsheets.net": H(
        agent="PikoBuy", dest=None, loc="en", lang="en", ccy="USD",
        dest_label="a country in the estimator",
        title="PikoBuy .net hub — not a customs territory",
        h1="This .net hostname is not a customs territory — pick a real country",
        keep=[("/pikobuy-shipping-guide/", "Shipping"), ("/is-pikobuy-legit/", "Legit?"), ("/pikobuy-coupons/", "Coupons"), ("/pikobuy-spreadsheet/", "Spreadsheet")],
    ),
    "bestlolobuyspreadsheet.com": H(
        agent="LoLoBuy", dest=None, loc="en", lang="en", ccy="USD",
        dest_label="a country in the estimator",
        title="LoLoBuy QC hub — not a customs territory",
        h1="This .com hostname is not a customs territory — pick a real country",
        keep=[("/guides/coupons/", "Coupons"), ("/guides/shipping/", "Shipping"), ("/guides/is-lolobuy-legit/", "Legit?"), ("/spreadsheet/", "Spreadsheet")],
    ),
    "lolospreadsheet.com": H(
        agent="LoLoBuy", dest=None, loc="en", lang="en", ccy="USD",
        dest_label="a country in the estimator",
        title="LoLoBuy SOP hub — not a customs territory",
        h1="This .com hostname is not a customs territory — pick a real country",
        keep=[("/guides/", "Guides"), ("/guides/is-lolobuy-legit/", "Legit?"), ("/spreadsheet/", "Spreadsheet"), ("/brand/prada/", "Prada")],
    ),
    "eastmallspreadsheet.com": H(
        agent="EastMallBuy", dest=None, loc="en", lang="en", ccy="USD",
        dest_label="a country in the estimator",
        title="EastMallBuy .com hub — not a customs territory",
        h1="This .com hostname is not a customs territory — pick a real country",
        keep=[("/eastmallbuy-coupons/", "Coupons"), ("/eastmallbuy-shipping-guide/", "Shipping"), ("/is-eastmallbuy-legit/", "Legit?"), ("/eastmallbuy-spreadsheet/", "Spreadsheet")],
    ),
    "fsbuyspreadsheets.com": H(
        agent="FSBuy", dest=None, loc="en", lang="en", ccy="USD",
        dest_label="a country in the estimator",
        title="FSBuy .com hub — not a customs territory",
        h1="This .com hostname is not a customs territory — pick a real country",
        keep=[("/fsbuy-coupons/", "Coupons"), ("/fsbuy-shipping-guide/", "Shipping"), ("/is-fsbuy-legit/", "Legit?"), ("/fsbuy-spreadsheet/", "Spreadsheet")],
    ),
    "gtspreadsheet.com": H(
        agent="GTbuy", dest=None, loc="en", lang="en", ccy="USD",
        dest_label="a country in the estimator",
        title="GTbuy .com hub — not a customs territory",
        h1="This .com hostname is not a customs territory — pick a real country",
        keep=[("/gtbuy-coupons/", "Coupons"), ("/gtbuy-shipping-guide/", "Shipping"), ("/is-gtbuy-legit/", "Legit?"), ("/gtbuy-spreadsheet/", "Spreadsheet")],
    ),
    "itaobuyspreadsheet.net": H(
        agent="iTaoBuy", dest=None, loc="en", lang="en", ccy="USD",
        dest_label="a country in the estimator",
        title="iTaoBuy .net hub — not a customs territory",
        h1="This .net hostname is not a customs territory — pick a real country",
        keep=[("/itaobuy-shipping-lines-2026.html", "Shipping lines"), ("/itaobuy-coupon-tracker-2026.html", "Coupons"), ("/itaobuy-real-shipping-bills-2026.html", "Real bills"), ("/itaobuy-user-reports-2026.html", "Reports")],
    ),
    "pingubuyspreadsheet.net": H(
        agent="PinguBuy", dest=None, loc="en", lang="en", ccy="USD",
        dest_label="a country in the estimator",
        title="PinguBuy .net hub — not a customs territory",
        h1="This .net hostname is not a customs territory — pick a real country",
        keep=[("/pingubuy-coupons/", "Coupons"), ("/pingubuy-shipping-guide/", "Shipping"), ("/is-pingubuy-legit/", "Legit?"), ("/pingubuy-spreadsheet/", "Spreadsheet")],
    ),
    "spanbuyspreadsheets.com": H(
        agent="SpanBuy", dest=None, loc="en", lang="en", ccy="USD",
        dest_label="a country in the estimator",
        title="SpanBuy .com hub — not a customs territory",
        h1="This .com hostname is not a customs territory — pick a real country",
        keep=[("/spanbuy-coupons/", "Coupons"), ("/spanbuy-shipping-guide/", "Shipping"), ("/is-spanbuy-legit/", "Legit?"), ("/spanbuy-spreadsheet/", "Spreadsheet")],
    ),
}

# Unique CMS hubs already live — leftover dest generate/PUT must not smash them.
SKIP_UNIQUE = frozenset({
    "boonspreadsheet.com",
    "basetaospreadsheet.com",
    "cnshopper.net",
    "cnshopperspreadsheet.net",
    "fishgoospreadsheet.net",
    "goatedspreadsheet.com",
    "pikospreadsheets.net",
    "lolospreadsheet.com",
    "eastmallspreadsheet.com",
    "fsbuyspreadsheets.com",
    "gtspreadsheet.com",
    "itaobuyspreadsheet.net",
    "pingubuyspreadsheet.net",
    "spanbuyspreadsheets.com",
})

# Origin path that already has a usable logo file, copied onto leftover hosts.
LOGO_SRC = {
    "MyCNBox": ("mycnbox.de", "assets/images/mycnbox-logo.png"),
    "FansBuy": ("fansbuy.co.uk", "assets/images/fansbuy-wordmark.png"),
    "LoveGoBuy": ("lovegobuy.nl", "assets/images/lovegobuy-logo.png"),
    "OOTDBuy": ("ootdbuy.nl", "assets/images/ootdbuy-logo.png"),
    "CSSBuy": ("cssbuyspreadsheet.ca", "assets/images/cssbuy-logo.png"),
    "HipoBuy": ("hipobuyreview.com", "assets/images/hipobuy-wordmark.png"),
    "Kakobuy": ("lovegobuy.nl", "assets/images/kakobuy-logo.png"),
    "BoonBuy": ("boonspreadsheet.com", "assets/images/official-logo.png"),
    "BaseTao": ("basetaospreadsheet.com", "assets/images/official-logo.png"),
    "OSSBuy": ("ossbuyspreadsheets.org", "assets/images/official-logo.png"),
    "GoatedBuy": ("goatedspreadsheet.com", "assets/images/official-logo.png"),
    "PikoBuy": ("pikospreadsheets.net", "assets/images/official-logo.png"),
    "LoLoBuy": ("bestlolobuyspreadsheet.com", "assets/images/official-logo.png"),
    "EastMallBuy": ("eastmallspreadsheet.com", "assets/images/official-logo.png"),
    "FSBuy": ("fsbuyspreadsheets.com", "assets/images/official-logo.png"),
    "GTbuy": ("gtspreadsheet.com", "assets/images/official-logo.png"),
    "iTaoBuy": ("itaobuyspreadsheet.net", "assets/images/official-logo.png"),
    "PinguBuy": ("pingubuyspreadsheet.net", "assets/images/official-logo.png"),
    "SpanBuy": ("spanbuyspreadsheets.com", "assets/images/official-logo.png"),
}


def register() -> None:
    AGENTS.update(EXTRA_AGENTS)
    HOSTS.update(LEFTOVER)


def generate() -> None:
    register()
    if not CMS_CSS.is_file():
        raise SystemExit("missing desk-cms.css")
    for host, d in LEFTOVER.items():
        if host in SKIP_UNIQUE:
            print("SKIP unique CMS", host)
            continue
        html = build_home(host)
        if "Georgia" in html:
            raise SystemExit(f"{host}: Georgia leak")
        if "#00C853" in html and d["agent"] != "HipoBuy":
            raise SystemExit(f"{host}: HipoBuy green leak")
        for e in skin.validate_desk(html, _facts(host), page="home"):
            raise SystemExit(f"{host}: {e}")
        if "not a customs territory" not in html:
            raise SystemExit(f"{host}: missing hub customs line")
        if len(html) < 18000:
            raise SystemExit(f"{host}: too small {len(html)}")
        dest = OUT / host / "overlay"
        dest.mkdir(parents=True, exist_ok=True)
        (dest / "index.html").write_text(html, encoding="utf-8")
        themed = OUT / "shared" / "themes" / f"{d['agent'].lower()}-theme.css"
        themed.parent.mkdir(parents=True, exist_ok=True)
        if not themed.is_file():
            themed.write_text(theme_css(d["agent"]), encoding="utf-8")
        print("OK", host, len(html), d["agent"])


def inventory_host(client, host: str) -> dict:
    remote = f"/www/wwwroot/{host}"
    script = rf"""
python3 - <<'PY'
import os, json
root={remote!r}
files=[]
for dirpath, dirnames, names in os.walk(root):
    dirnames[:] = [x for x in dirnames if x not in {{".git","node_modules","vendor","runtime","data","upload","uploads","assets","static"}}]
    rel_dir = os.path.relpath(dirpath, root)
    depth = 0 if rel_dir == "." else rel_dir.count(os.sep) + 1
    if depth > 4:
        dirnames[:] = []
        continue
    for fn in names:
        if not fn.endswith(".html"):
            continue
        if fn in {{"404.html","403.html"}}:
            continue
        p = os.path.join(dirpath, fn)
        rel = os.path.relpath(p, root)
        if rel in {{"index.html","404/index.html"}}:
            continue
        try:
            sz = os.path.getsize(p)
        except OSError:
            continue
        if sz < 2000 or sz > 400000:
            continue
        files.append({{"rel": rel.replace("\\\\","/"), "bytes": sz}})
print(json.dumps({{"host": os.path.basename(root), "count": len(files), "files": files}}))
PY
"""
    out = skin._run(client, script, timeout=120)
    return json.loads(out)


def put_homes() -> None:
    generate()
    client = skin._connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/leftover-hub-skins-{stamp}"
    print(skin._run(client, f"mkdir -p '{bak}'"))
    sftp = client.open_sftp()
    for host, d in LEFTOVER.items():
        if host in SKIP_UNIQUE:
            print("SKIP unique CMS PUT", host)
            continue
        remote_root = f"/www/wwwroot/{host}"
        ag = AGENTS[d["agent"]]
        logo_rel = ag["logo"].lstrip("/")
        theme_name = Path(ag["css"][-1]).name
        skin._run(
            client,
            f"mkdir -p '{remote_root}/assets/css' '{remote_root}/assets/images' '{bak}/{host}' "
            f"&& cp -a '{remote_root}/index.html' '{bak}/{host}/index.html'",
        )
        local = OUT / host / "overlay" / "index.html"
        sftp.put(str(local), f"{remote_root}/index.html")
        sftp.put(str(CMS_CSS), f"{remote_root}/assets/css/desk-cms.css")
        theme_local = OUT / "shared" / "themes" / f"{d['agent'].lower()}-theme.css"
        if not theme_local.is_file():
            theme_local.write_text(theme_css(d["agent"]), encoding="utf-8")
        sftp.put(str(theme_local), f"{remote_root}/assets/css/{theme_name}")
        dest_logo = f"{remote_root}/{logo_rel}"
        src = LOGO_SRC.get(d["agent"])
        copied = False
        if src and not dest_logo.endswith(".svg"):
            src_host, src_rel = src
            check = skin._run(client, f"test -f '/www/wwwroot/{src_host}/{src_rel}' && echo yes || echo no")
            if check.strip() == "yes":
                skin._run(client, f"cp -a '/www/wwwroot/{src_host}/{src_rel}' '{dest_logo}'")
                copied = True
        if not copied:
            svg = (
                "<svg xmlns='http://www.w3.org/2000/svg' width='220' height='40'>"
                f"<rect width='220' height='40' rx='8' fill='{ag['primary']}'/>"
                f"<text x='16' y='26' fill='#fff' font-family='Inter,Arial,sans-serif' "
                f"font-size='18' font-weight='700'>{d['agent']}</text></svg>"
            )
            local_svg = OUT / "shared" / "themes" / (Path(logo_rel).stem + ".svg")
            local_svg.write_text(svg, encoding="utf-8")
            target = dest_logo if dest_logo.endswith(".svg") else dest_logo.rsplit(".", 1)[0] + ".svg"
            sftp.put(str(local_svg), target)
        skin._run(
            client,
            f"chown -R www:www '{remote_root}/index.html' '{remote_root}/assets/css' '{remote_root}/assets/images' 2>/dev/null || true",
        )
        print("PUT home", host, local.stat().st_size)
    sftp.close()
    print("backup", bak)
    client.close()


def put_inners() -> None:
    register()
    client = skin._connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/leftover-inner-chrome-{stamp}"
    print(skin._run(client, f"mkdir -p '{bak}'"))
    rows = []
    for host in LEFTOVER:
        if host in SKIP_UNIQUE:
            print("SKIP unique CMS inner", host)
            continue
        row = inventory_host(client, host)
        rows.append(row)
        print("INV", host, row["count"])
    inv_path = Path("/tmp/leftover-inners.json")
    inv_path.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    snips = inner.build_snips()
    leftover_snips = {h: snips[h] for h in LEFTOVER if h in snips and h not in SKIP_UNIQUE}
    snip_path = Path("/tmp/leftover-inner-chrome-snips.json")
    snip_path.write_text(json.dumps(leftover_snips), encoding="utf-8")
    sftp = client.open_sftp()
    sftp.put(str(inv_path), "/tmp/leftover-inners.json")
    sftp.put(str(snip_path), "/tmp/inner-chrome-snips.json")
    sftp.put(str(_TOOLS / "dest_inner_chrome.py"), "/tmp/dest_inner_chrome.py")
    sftp.close()
    # worker expects /tmp/dest-inners.json
    cmd = (
        f"cp /tmp/leftover-inners.json /tmp/dest-inners.json && "
        f"INNER_BAK='{bak}' python3 /tmp/dest_inner_chrome.py worker"
    )
    print(skin._run(client, cmd, timeout=300))
    client.close()


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "generate"
    if cmd == "put":
        put_homes()
    elif cmd == "inners":
        put_inners()
    elif cmd == "all":
        put_homes()
        put_inners()
    else:
        generate()
