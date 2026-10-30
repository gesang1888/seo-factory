<?php

namespace App\Services;

/**
 * Dest-unique #local briefing keyed by HTTP_HOST.
 * Generated — do not hand-edit fingerprints.
 */
class DestLocal
{
    public static function key(?string $host = null): ?string
    {
        $host = $host ?? ($GLOBALS['domain_host'] ?? '');
        $map = ['cssbuy.at' => 'at', 'cssbuy.es' => 'es', 'cssbuy.fr' => 'fr', 'cssbuy.it' => 'it', 'cssbuy.nl' => 'nl'];
        return $map[$host] ?? null;
    }

    public static function html(): string
    {
        $key = self::key();
        if (!$key) {
            return '';
        }
        $path = BASE_PATH . '/resources/views/partials/dest-local-' . $key . '.php';
        if (!is_file($path)) {
            return '';
        }
        ob_start();
        include $path;
        $inner = ob_get_clean();
        if ($inner === '') {
            return '';
        }
        return '<section class="lite-section dest-local-wrap"><div class="container">'
            . $inner
            . '</div></section>';
    }

    public static function css(): string
    {
        return '.skip{position:absolute;left:-999px;top:8px;background:#fff;padding:8px 12px;z-index:20;border-radius:8px}
.skip:focus{left:12px}
.legal-note{font-size:13px;color:#64748b;line-height:1.65;margin:8px 0 0;max-width:640px}
.local-steps{margin:12px 0 0;padding:0;list-style:none;display:grid;gap:12px}
.local-steps li{border:1px solid #e5e7eb;border-radius:12px;padding:14px 16px;background:#fff}
.local-steps strong{display:block;margin:0 0 6px;font-size:15px}
.local-steps span{display:block;color:#334155;line-height:1.7;font-size:15px}
.local-src{font-size:14px;color:#334155;line-height:1.7;margin:14px 0 0}
.local-src a{color:inherit}
#local{scroll-margin-top:96px}

.dest-local-wrap{background:#e8f8ee;border-top:1px solid #b7e7c8;border-bottom:1px solid #b7e7c8}
.sg-sec{margin:0;padding:8px 0 12px}
.sg-sec h2{font-size:clamp(22px,3vw,30px);font-weight:700;letter-spacing:-.4px;margin:0 0 8px;color:#1a1a1a}
.sg-sec .ssub{color:#555;margin:0 0 12px;font-size:15px;line-height:1.65}
.sg-sec a{color:#009E44}
.local-steps li{border-color:#b7e7c8}
';
    }

    public static function cta(): string
    {
        $key = self::key();
        $map = ['at' => 'AT-Check', 'es' => 'Check ES', 'fr' => 'Check FR', 'it' => 'Check IT', 'nl' => 'Check NL'];
        return $map[$key] ?? '';
    }

    public static function skipLabel(): string
    {
        $key = self::key();
        $map = ['at' => 'Zum Inhalt', 'es' => 'Saltar al contenido', 'fr' => 'Aller au contenu', 'it' => 'Vai al contenuto', 'nl' => 'Naar de inhoud'];
        $lang = $GLOBALS['locale'] ?? 'en';
        if ($key && isset($map[$key])) {
            return $map[$key];
        }
        $fallback = ['de' => 'Zum Inhalt', 'es' => 'Saltar al contenido', 'fr' => 'Aller au contenu', 'it' => 'Vai al contenuto', 'nl' => 'Naar de inhoud'];
        return $fallback[$lang] ?? 'Skip to content';
    }

    public static function faqs(): array
    {
        $key = self::key();
        $all = json_decode('{"at": [{"q": "Welches Land im CSSBuy-Schätzer für cssbuy.at?", "a": "Schätzer-Land ist AT mit vierstelliger PLZ, nicht die TLD .at, nicht DE, nicht „EU“. Der Schätzer braucht einen Ländercode, nicht diesen Hostnamen. Wer Abgaben nach Österreich zahlt, steht auf der gebuchten SKU. Österreichische Post kann bei Collect extra kassieren. Quelle dieses Desks: BMF Zoll (bmf.gv.at), nicht ein Discord-Screenshot. Schätzer-Ziel ist AT mit vierstelliger Postleitzahl, nicht DE. Keine Unterdeklaration."}, {"q": "Wer zahlt Einfuhr auf diese Adresse?", "a": "Wer Abgaben nach Österreich zahlt, steht auf der gebuchten SKU. Österreichische Post kann bei Collect extra kassieren. Quelle dieses Desks: BMF Zoll (bmf.gv.at), nicht ein Discord-Screenshot. Schätzer-Ziel ist AT mit vierstelliger Postleitzahl, nicht DE. Keine Unterdeklaration. IOSS und Einfuhr-USt ändern sich. BMF Zoll und die SKU-Bedingungen am Versandtag lesen. Dieser Desk erfindet keinen Betrag für eine AT-Adresse und kopiert keine Schwelle aus Deutschland."}, {"q": "Wie lange lagert CSSBuy?", "a": "Lager: 90 freie Tage ab In Warehouse (offizielle CSSBuy-FAQ), danach ¥15/Bestellung/Monat. Am Versandmorgen in Help prüfen. Diese Zahl kommt aus der offiziellen Warehouse-FAQ, nicht aus einem Discord-Screenshot."}, {"q": "Ist das die offizielle CSSBuy-Kasse?", "a": "Nein. cssbuy.at ist ein Infodesk für Österreich. Bestellung, Zahlung und Reklamation nur auf cssbuy.com. Schwester-Länderhosts bleiben eigene Dateien — kein 301."}], "es": [{"q": "¿Qué país pongo en el estimador de CSSBuy en cssbuy.es?", "a": "El país del estimador es ES, no este TLD, no EU. El formulario oficial pide un país, no este hostname. Quién paga aranceles al entrar en España lo dice la SKU. Correos puede añadir una tasa de despacho en Collect. Fuente: Agencia Tributaria, no un recuento de líneas de otro agente. Destino del estimador: España. Sin infradeclaración."}, {"q": "¿Quién paga aranceles a esta dirección?", "a": "Quién paga aranceles al entrar en España lo dice la SKU. Correos puede añadir una tasa de despacho en Collect. Fuente: Agencia Tributaria, no un recuento de líneas de otro agente. Destino del estimador: España. Sin infradeclaración. IVA, IOSS y umbrales cambian. Lee la AEAT y la SKU el día del envío. Este desk no inventa un valor declarado ni copia un snapshot de un recuento de líneas de otro agente."}, {"q": "¿Cuánto tiempo guarda CSSBuy el paquete?", "a": "Almacén: 90 días gratis desde In Warehouse (FAQ oficial CSSBuy), luego ¥15/pedido/mes. Confirma Help el día del envío. La cifra sale de la FAQ oficial de almacén, no de un recuento de líneas ajeno."}, {"q": "¿Esta página cobra el flete?", "a": "No. cssbuy.es es un desk informativo para España. Pedidos y pagos solo en cssbuy.com. Los hosts hermanos siguen en archivos separados — sin 301."}], "fr": [{"q": "Quel pays dans l’estimateur CSSBuy sur cssbuy.fr ?", "a": "Le pays de l’estimateur est FR, pas ce TLD, pas BE, pas EU. Le formulaire officiel veut un code pays, pas ce nom d’hôte. Qui paie les droits vers la France est sur la SKU. Colissimo peut ajouter des frais de dédouanement en Collect. Source : douane.gouv.fr. Destination FR, pas un code postal belge. Pas de sous-déclaration."}, {"q": "Qui paie les droits vers cette adresse ?", "a": "Qui paie les droits vers la France est sur la SKU. Colissimo peut ajouter des frais de dédouanement en Collect. Source : douane.gouv.fr. Destination FR, pas un code postal belge. Pas de sous-déclaration. TVA, IOSS et seuils bougent. Lis douane.gouv.fr et la SKU le jour de l’envoi. Ce desk n’invente pas une valeur déclarée et ne copie pas un dossier Belgique."}, {"q": "Combien de temps CSSBuy stocke-t-il ?", "a": "Entrepôt : 90 jours gratuits dès In Warehouse (FAQ officielle CSSBuy), puis ¥15/commande/mois. Vérifier Help le matin de l’envoi. Le chiffre vient de la FAQ entrepôt officielle, pas d’un dossier Belgique."}, {"q": "Cette page encaisse-t-elle le fret ?", "a": "Non. cssbuy.fr est un desk d’information pour France. Commandes et paiements uniquement sur cssbuy.com. Les hôtes sœurs restent des fichiers séparés — pas de 301."}], "it": [{"q": "Quale paese nell’estimator CSSBuy su cssbuy.it?", "a": "Il paese dell’estimator è IT, non questo TLD, non EU. Il modulo ufficiale vuole un codice paese, non questo hostname. Chi paga dazi verso l’Italia lo dice la SKU. Poste Italiane può aggiungere un fee di sdoganamento. Fonte: ADM (adm.gov.it). Destinazione IT, non Correos. Niente sottofatturazione."}, {"q": "Chi paga i dazi verso questo indirizzo?", "a": "Chi paga dazi verso l’Italia lo dice la SKU. Poste Italiane può aggiungere un fee di sdoganamento. Fonte: ADM (adm.gov.it). Destinazione IT, non Correos. Niente sottofatturazione. IVA, IOSS e soglie cambiano. Leggi ADM e la SKU il giorno della spedizione. Questo desk non inventa un valore dichiarato per un CAP italiano."}, {"q": "Quanto tiene CSSBuy in magazzino?", "a": "Magazzino: 90 giorni gratis da In Warehouse (FAQ ufficiale CSSBuy), poi ¥15/ordine/mese. Conferma Help il giorno della spedizione. Il numero viene dalla FAQ magazzino ufficiale."}, {"q": "Questa pagina incassa il nolo?", "a": "No. cssbuy.it è un desk informativo per Italia. Ordini e pagamenti solo su cssbuy.com. Gli host fratelli restano file separati — niente 301."}], "nl": [{"q": "Welk land in de CSSBuy-estimator op cssbuy.nl?", "a": "Estimator-land is NL, niet deze TLD, niet EU. Het officiële formulier wil een landcode, niet deze hostname. Wie invoer naar Nederland betaalt, staat op de SKU. DHL kan bij Collect een inklaringsfee innen. Bron: Belastingdienst Douane. Bestemming NL met Nederlandse postcode, geen Duits afhaalautomaat-nummer. Geen onderwaardering."}, {"q": "Wie betaalt invoer naar dit adres?", "a": "Wie invoer naar Nederland betaalt, staat op de SKU. DHL kan bij Collect een inklaringsfee innen. Bron: Belastingdienst Douane. Bestemming NL met Nederlandse postcode, geen Duits afhaalautomaat-nummer. Geen onderwaardering. BTW, IOSS en drempels wijzigen. Lees de Douane en de SKU op de verzenddag. Deze desk verzint geen aangegeven waarde en kopieert geen Duitse Zoll-drempel."}, {"q": "Hoe lang slaat CSSBuy op?", "a": "Magazijn: 90 gratis dagen vanaf In Warehouse (officiële CSSBuy-FAQ), daarna ¥15/order/maand. Check Help op de verzenddag. Het getal komt uit de officiële warehouse-FAQ."}, {"q": "Is dit de kassa?", "a": "Nee. cssbuy.nl is een infodesk voor Nederland. Bestellen en betalen alleen op cssbuy.com. Zushosts blijven aparte bestanden — geen 301."}]}', true);
        if (!$key || !is_array($all) || empty($all[$key])) {
            return [];
        }
        return $all[$key];
    }
}
