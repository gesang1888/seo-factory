"""Trust / legal pages for each Lovegobuy domain."""

from __future__ import annotations

TRUST_SLUGS = (
    "about",
    "contact",
    "privacy-policy",
    "terms",
    "affiliate-disclosure",
    "partner-disclosure",
)

TRUST_PAGES: dict[str, dict[str, dict]] = {
    "about": {
        "en": {
            "title": "About Lovegobuy Spreadsheet Guide",
            "description": "About this independent Lovegobuy spreadsheet resource hub with W2CLinks browsing and WhatsApp help.",
            "h1": "About Lovegobuy Spreadsheet Guide",
            "intro": "This site is an independent resource for Lovegobuy spreadsheet searchers. We explain how to browse finds on W2CLinks and register on Lovegobuy with referral support.",
            "sections": [
                (
                    "What we do",
                    "We publish country-specific guides for shipping, QC, coupons and spreadsheet browsing. "
                    "Product actions open W2CLinks in a new tab; orders are placed on Lovegobuy.",
                ),
                (
                    "What we are not",
                    "This is not the official Lovegobuy website and not a local product store. "
                    "We do not host checkout or warehouse tools.",
                ),
            ],
        },
        "nl": {
            "title": "Over Lovegobuy Spreadsheet Guide",
            "description": "Over deze onafhankelijke Lovegobuy spreadsheet resource met W2CLinks en WhatsApp.",
            "h1": "Over Lovegobuy Spreadsheet Guide",
            "intro": "Onafhankelijke gids voor Lovegobuy spreadsheet-zoekers in Nederland en Europa.",
            "sections": [
                ("Wat we doen", "Guides voor verzending, QC, coupons en W2CLinks spreadsheet browsing."),
                ("Wat we niet zijn", "Geen officiële Lovegobuy-site en geen lokale winkel."),
            ],
        },
        "de": {
            "title": "Über Lovegobuy Spreadsheet Guide",
            "description": "Unabhängige Lovegobuy Spreadsheet-Ressource mit W2CLinks und WhatsApp.",
            "h1": "Über Lovegobuy Spreadsheet Guide",
            "intro": "Unabhängiger Guide für Lovegobuy Spreadsheet-Nutzer.",
            "sections": [
                ("Was wir tun", "Guides zu Versand, QC, Gutscheinen und W2CLinks Spreadsheet."),
                ("Was wir nicht sind", "Keine offizielle Lovegobuy-Website."),
            ],
        },
        "it": {
            "title": "Informazioni su Lovegobuy Spreadsheet Guide",
            "description": "Risorsa indipendente Lovegobuy spreadsheet con W2CLinks e WhatsApp.",
            "h1": "Informazioni su Lovegobuy Spreadsheet Guide",
            "intro": "Guida indipendente per chi cerca lovegobuy spreadsheet.",
            "sections": [
                ("Cosa facciamo", "Guide su spedizione, QC, coupon e spreadsheet W2CLinks."),
                ("Cosa non siamo", "Non siamo il sito ufficiale Lovegobuy."),
            ],
        },
        "fr": {
            "title": "À propos du guide Lovegobuy Spreadsheet",
            "description": "Ressource indépendante Lovegobuy spreadsheet avec W2CLinks et WhatsApp.",
            "h1": "À propos du guide Lovegobuy Spreadsheet",
            "intro": "Guide indépendant pour les recherches lovegobuy spreadsheet en France.",
            "sections": [
                ("Notre rôle", "Guides livraison, QC, coupons et tableur W2CLinks."),
                ("Ce que nous ne sommes pas", "Pas le site officiel Lovegobuy."),
            ],
        },
    },
    "contact": {
        "en": {
            "title": "Contact — Lovegobuy Spreadsheet Guide",
            "description": "Contact this independent Lovegobuy spreadsheet resource via WhatsApp.",
            "h1": "Contact",
            "intro": "Use WhatsApp for spreadsheet browsing help. Order issues go to Lovegobuy support.",
            "sections": [
                ("WhatsApp", "Message us on WhatsApp for guide questions about W2CLinks and Lovegobuy workflow."),
                ("Lovegobuy orders", "For parcel, payment or QC issues contact Lovegobuy Help Center via lovegobuy.com."),
            ],
        },
        "nl": {"title": "Contact", "description": "Contact via WhatsApp.", "h1": "Contact", "intro": "WhatsApp voor gidsvragen.", "sections": [("WhatsApp", "Stuur een bericht voor spreadsheet hulp.")]},
        "de": {"title": "Kontakt", "description": "Kontakt per WhatsApp.", "h1": "Kontakt", "intro": "WhatsApp für Guide-Fragen.", "sections": [("WhatsApp", "Schreiben Sie uns bei Spreadsheet-Fragen.")]},
        "it": {"title": "Contatti", "description": "Contatto WhatsApp.", "h1": "Contatti", "intro": "WhatsApp per domande sulla guida.", "sections": [("WhatsApp", "Scrivici per aiuto sul spreadsheet.")]},
        "fr": {"title": "Contact", "description": "Contact WhatsApp.", "h1": "Contact", "intro": "WhatsApp pour questions sur le guide.", "sections": [("WhatsApp", "Écrivez-nous pour l'aide tableur.")]},
    },
    "privacy-policy": {
        "en": {
            "title": "Privacy Policy",
            "description": "Privacy policy for Lovegobuy Spreadsheet Guide static resource sites.",
            "h1": "Privacy Policy",
            "intro": "We do not run accounts or checkout on this guide site.",
            "sections": [
                ("Analytics", "Hosting logs may record IP and user agent for security."),
                ("Third parties", "Outbound links to W2CLinks and Lovegobuy have their own policies."),
            ],
        },
        "nl": {"title": "Privacybeleid", "description": "Privacybeleid.", "h1": "Privacybeleid", "intro": "Geen accounts op deze gids.", "sections": []},
        "de": {"title": "Datenschutz", "description": "Datenschutz.", "h1": "Datenschutz", "intro": "Keine Konten auf diesem Guide.", "sections": []},
        "it": {"title": "Privacy", "description": "Privacy.", "h1": "Privacy", "intro": "Nessun account su questa guida.", "sections": []},
        "fr": {"title": "Confidentialité", "description": "Politique de confidentialité.", "h1": "Confidentialité", "intro": "Pas de comptes sur ce guide.", "sections": []},
    },
    "terms": {
        "en": {
            "title": "Terms of Use",
            "description": "Terms for using Lovegobuy Spreadsheet Guide resource pages.",
            "h1": "Terms of Use",
            "intro": "By using this site you agree these pages are informational only.",
            "sections": [
                ("No guarantees", "Shipping times, coupons and product availability can change on Lovegobuy."),
                ("Affiliate links", "Some Lovegobuy register links may include referral parameters."),
            ],
        },
        "nl": {"title": "Gebruiksvoorwaarden", "description": "Voorwaarden.", "h1": "Gebruiksvoorwaarden", "intro": "Alleen informatief.", "sections": []},
        "de": {"title": "Nutzungsbedingungen", "description": "Bedingungen.", "h1": "Nutzungsbedingungen", "intro": "Nur informational.", "sections": []},
        "it": {"title": "Termini", "description": "Termini.", "h1": "Termini", "intro": "Solo informativo.", "sections": []},
        "fr": {"title": "Conditions", "description": "Conditions.", "h1": "Conditions", "intro": "Informatif uniquement.", "sections": []},
    },
    "affiliate-disclosure": {
        "en": {
            "title": "Affiliate Disclosure",
            "description": "Affiliate and referral disclosure for Lovegobuy Spreadsheet Guide.",
            "h1": "Affiliate Disclosure",
            "intro": "We may earn referral benefits when you register on Lovegobuy through our links.",
            "sections": [
                ("W2CLinks", "Spreadsheet browsing opens W2CLinks — our primary product-find hub."),
                ("Lovegobuy register", "Register links may include ref= invitation codes."),
            ],
        },
        "nl": {"title": "Affiliate disclosure", "description": "Affiliate.", "h1": "Affiliate disclosure", "intro": "Referral links mogelijk.", "sections": []},
        "de": {"title": "Affiliate Offenlegung", "description": "Affiliate.", "h1": "Affiliate Offenlegung", "intro": "Referral-Links möglich.", "sections": []},
        "it": {"title": "Affiliate disclosure", "description": "Affiliate.", "h1": "Affiliate disclosure", "intro": "Link referral possibili.", "sections": []},
        "fr": {"title": "Divulgation affiliate", "description": "Affiliation.", "h1": "Divulgation affiliate", "intro": "Liens de parrainage possibles.", "sections": []},
    },
    "partner-disclosure": {
        "en": {
            "title": "Partner Disclosure",
            "description": "Relationship disclosure for Lovegobuy Spreadsheet Guide.",
            "h1": "Partner Disclosure",
            "intro": "This is an independent guide site, not an official Lovegobuy property.",
            "sections": [
                ("Independence", "We are not authorized to speak for Lovegobuy customer service."),
                ("Trademarks", "Lovegobuy trademarks belong to their respective owners."),
            ],
        },
        "nl": {"title": "Partner disclosure", "description": "Partner.", "h1": "Partner disclosure", "intro": "Onafhankelijke gids.", "sections": []},
        "de": {"title": "Partner Offenlegung", "description": "Partner.", "h1": "Partner Offenlegung", "intro": "Unabhängiger Guide.", "sections": []},
        "it": {"title": "Partner disclosure", "description": "Partner.", "h1": "Partner disclosure", "intro": "Guida indipendente.", "sections": []},
        "fr": {"title": "Divulgation partenaire", "description": "Partenaire.", "h1": "Divulgation partenaire", "intro": "Guide indépendant.", "sections": []},
    },
}


def get_trust_page(slug: str, lang: str) -> dict | None:
    block = TRUST_PAGES.get(slug)
    if not block:
        return None
    ui = lang if lang in ("nl", "fr", "es", "fi") else "en"
    data = block.get(ui) or block.get("en")
    if not data:
        return None
    return {
        "slug": slug,
        "cta": "Open Lovegobuy Spreadsheet",
        "cta_href": "https://w2clinks.com/spreadsheet/",
        **data,
        "faq": [
            {
                "question": "Where does the spreadsheet open?",
                "answer": "All spreadsheet CTAs open W2CLinks in a new tab.",
            },
            {
                "question": "How can I contact support?",
                "answer": "Use WhatsApp at +44 7856 544534 for guide questions.",
            },
        ],
    }
