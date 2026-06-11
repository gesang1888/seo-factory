"""Country-specific Kakobuy shipping reference tables (estimates, not quotes)."""

from __future__ import annotations

from html import escape as esc

from scripts.hub_icons import flag_img, region_label

# Estimated ranges — always verify live lines in Kakobuy before paying.
SHIPPING_TABLES: dict[str, dict] = {
    "US": {
        "currency": "USD",
        "note": (
            "US delivery costs depend on actual weighed parcel size, chosen line, fuel surcharges "
            "and customs clearance. Treat these as planning ranges only."
        ),
        "rows": [
            ("Economy line", "0.5–1.0 kg", "$18–$32", "12–22 days"),
            ("Standard line", "1.0–2.0 kg", "$28–$48", "10–18 days"),
            ("Express line", "1.0–2.5 kg", "$45–$78", "7–14 days"),
            ("Shoes parcel", "1.5–2.5 kg", "$35–$62", "10–20 days"),
            ("Hoodie + tee combo", "1.2–2.0 kg", "$30–$52", "10–18 days"),
        ],
        "customs": (
            "US buyers should budget for possible customs review. De minimis rules can change; "
            "keep product value, shipping cost and item category documented for your parcel."
        ),
    },
    "ES": {
        "currency": "EUR",
        "note": (
            "Envíos a España varían según peso real, volumen, línea elegida y gestión aduanera. "
            "Confirma siempre la tarifa final en Kakobuy antes de pagar."
        ),
        "rows": [
            ("Línea económica", "0.5–1.0 kg", "€16–€28", "14–25 días"),
            ("Línea estándar", "1.0–2.0 kg", "€24–€42", "12–20 días"),
            ("Línea express", "1.0–2.5 kg", "€38–€65", "8–16 días"),
            ("Paquete zapatillas", "1.5–2.5 kg", "€30–€55", "12–22 días"),
            ("Sudadera + camiseta", "1.2–2.0 kg", "€26–€46", "12–20 días"),
        ],
        "customs": (
            "España puede aplicar IVA y tramites de importación según valor declarado y transportista. "
            "Reserva margen extra si el paquete supera umbrales habituales de revisión."
        ),
    },
    "FR": {
        "currency": "EUR",
        "note": (
            "Les tarifs vers la France dépendent du poids réel, du volume, de la ligne choisie "
            "et du dédouanement. Vérifiez toujours le montant final dans Kakobuy."
        ),
        "rows": [
            ("Ligne économique", "0.5–1.0 kg", "€16–€29", "14–26 jours"),
            ("Ligne standard", "1.0–2.0 kg", "€25–€44", "12–21 jours"),
            ("Ligne express", "1.0–2.5 kg", "€39–€68", "8–17 jours"),
            ("Colis sneakers", "1.5–2.5 kg", "€31–€56", "12–23 jours"),
            ("Hoodie + t-shirt", "1.2–2.0 kg", "€27–€48", "12–21 jours"),
        ],
        "customs": (
            "En France, TVA et frais d'importation peuvent s'appliquer selon la valeur déclarée "
            "et le transporteur. Gardez une marge pour les contrôles douaniers."
        ),
    },
    "AT": {
        "currency": "EUR",
        "note": (
            "Versand nach Österreich hängt vom tatsächlichen Gewicht, Volumen, der Linie "
            "und der Zollabfertigung ab. Finalen Preis immer in Kakobuy prüfen."
        ),
        "rows": [
            ("Economy-Linie", "0.5–1.0 kg", "€16–€28", "14–25 Tage"),
            ("Standard-Linie", "1.0–2.0 kg", "€24–€43", "12–21 Tage"),
            ("Express-Linie", "1.0–2.5 kg", "€38–€66", "8–16 Tage"),
            ("Schuh-Paket", "1.5–2.5 kg", "€30–€54", "12–22 Tage"),
            ("Hoodie + Shirt", "1.2–2.0 kg", "€26–€47", "12–20 Tage"),
        ],
        "customs": (
            "Für Österreich können Einfuhrumsatzsteuer und Zollprüfungen anfallen. "
            "Deklarierter Warenwert, Versandkosten und Inhalt sollten nachvollziehbar sein."
        ),
    },
    "UK": {
        "currency": "GBP",
        "note": "UK estimates for planning — confirm live Kakobuy lines before checkout.",
        "rows": [
            ("Economy", "0.5–1.0 kg", "£14–£24", "12–22 days"),
            ("Standard", "1.0–2.0 kg", "£22–£38", "10–18 days"),
            ("Express", "1.0–2.5 kg", "£36–£58", "7–14 days"),
        ],
        "customs": "Budget for HMRC handling and possible VAT depending on declared value.",
    },
    "DE": {
        "currency": "EUR",
        "note": "Deutschland — Schätzwerte zur Planung; Live-Preis in Kakobuy prüfen.",
        "rows": [
            ("Economy", "0.5–1.0 kg", "€15–€27", "14–24 Tage"),
            ("Standard", "1.0–2.0 kg", "€23–€41", "12–20 Tage"),
            ("Express", "1.0–2.5 kg", "€37–€64", "8–16 Tage"),
        ],
        "customs": "Zoll und Einfuhrumsatzsteuer je nach Wert und Spediteur einplanen.",
    },
}


def shipping_section_html(region: str, lang: str) -> str:
    data = SHIPPING_TABLES.get(region) or SHIPPING_TABLES.get("US")
    if not data:
        return ""
    label = region_label(region)
    flag = flag_img(region, 28)
    rows_html = ""
    for line, weight, cost, eta in data["rows"]:
        rows_html += (
            f"<tr><td>{esc(line)}</td><td>{esc(weight)}</td>"
            f"<td>{esc(cost)}</td><td>{esc(eta)}</td></tr>"
        )
    title = {
        "es": f"Tarifas de envío estimadas — {label}",
        "fr": f"Tarifs de livraison estimés — {label}",
        "de": f"Geschätzte Versandkosten — {label}",
    }.get(lang, f"Estimated shipping rates — {label}")
    customs_label = {
        "es": "Notas aduaneras",
        "fr": "Notes douanières",
        "de": "Zollhinweise",
    }.get(lang, "Customs notes")
    return f"""<div class="card od-shipping-rates">
  <h2><img class="od-flag-inline" src="{esc(flag)}" alt="" width="28" height="21" loading="lazy"> {esc(title)}</h2>
  <p class="od-muted">{esc(data['note'])}</p>
  <div class="table-wrap">
    <table class="od-table">
      <thead><tr><th>Line</th><th>Weight</th><th>Est. cost ({esc(data['currency'])})</th><th>ETA</th></tr></thead>
      <tbody>{rows_html}</tbody>
    </table>
  </div>
  <p><strong>{esc(customs_label)}:</strong> {esc(data['customs'])}</p>
</div>"""
