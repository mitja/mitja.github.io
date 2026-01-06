#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "flet[all]",
#     "claudette",
#     "httpx",
# ]
# ///

import flet as ft
from vat_info_fetcher import get_vat_categories_md

# =============================================================================
# UI Translations - packaged with the app for web deployment
# =============================================================================
TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "app_title": "EU VAT Calculator",
        "app_subtitle": "For all 27 EU member states",
        "country_label": "Country",
        "amount_label": "Amount (EUR)",
        "amount_hint": "e.g. 100.00",
        "direction_label": "Calculation direction:",
        "net_to_gross": "Net → Gross",
        "gross_to_net": "Gross → Net",
        "rate_label": "VAT Rate",
        "rate_standard": "standard",
        "rate_reduced": "reduced",
        "rate_zero": "zero-rated",
        "standard_rate_info": "Standard rate:",
        "btn_calculate": "Calculate",
        "btn_clear": "Clear",
        "result_title": "Result",
        "result_country": "Country:",
        "result_rate": "VAT Rate:",
        "net_amount": "Net amount:",
        "vat_amount": "VAT:",
        "gross_amount": "Gross amount:",
        "error": "Error",
        "categories_title": "Reduced Rate Categories",
        "language": "Language",
    },
    "de": {
        "app_title": "EU USt Rechner",
        "app_subtitle": "Für alle 27 EU-Mitgliedsstaaten",
        "country_label": "Land",
        "amount_label": "Betrag (EUR)",
        "amount_hint": "z.B. 100,00",
        "direction_label": "Berechnungsrichtung:",
        "net_to_gross": "Netto → Brutto",
        "gross_to_net": "Brutto → Netto",
        "rate_label": "Steuersatz",
        "rate_standard": "Regelsteuersatz",
        "rate_reduced": "ermäßigt",
        "rate_zero": "steuerfrei",
        "standard_rate_info": "Regelsteuersatz:",
        "btn_calculate": "Berechnen",
        "btn_clear": "Löschen",
        "result_title": "Ergebnis",
        "result_country": "Land:",
        "result_rate": "Steuersatz:",
        "net_amount": "Nettobetrag:",
        "vat_amount": "Umsatzsteuer:",
        "gross_amount": "Bruttobetrag:",
        "error": "Fehler",
        "categories_title": "Ermäßigte Steuersätze",
        "language": "Sprache",
    },
}

# EU member states with their standard and reduced VAT rates (2025)
EU_VAT_RATES: dict[str, dict] = {
    "AT": {"name": "Austria", "name_de": "Österreich", "standard": 20, "reduced": [10, 13], "zero": True},
    "BE": {"name": "Belgium", "name_de": "Belgien", "standard": 21, "reduced": [6, 12], "zero": True},
    "BG": {"name": "Bulgaria", "name_de": "Bulgarien", "standard": 20, "reduced": [9], "zero": True},
    "HR": {"name": "Croatia", "name_de": "Kroatien", "standard": 25, "reduced": [5, 13], "zero": True},
    "CY": {"name": "Cyprus", "name_de": "Zypern", "standard": 19, "reduced": [5, 9], "zero": True},
    "CZ": {"name": "Czech Republic", "name_de": "Tschechien", "standard": 21, "reduced": [12], "zero": True},
    "DK": {"name": "Denmark", "name_de": "Dänemark", "standard": 25, "reduced": [], "zero": True},
    "EE": {"name": "Estonia", "name_de": "Estland", "standard": 22, "reduced": [9], "zero": True},
    "FI": {"name": "Finland", "name_de": "Finnland", "standard": 25.5, "reduced": [10, 14], "zero": True},
    "FR": {"name": "France", "name_de": "Frankreich", "standard": 20, "reduced": [5.5, 10], "zero": True},
    "DE": {"name": "Germany", "name_de": "Deutschland", "standard": 19, "reduced": [7], "zero": True},
    "GR": {"name": "Greece", "name_de": "Griechenland", "standard": 24, "reduced": [6, 13], "zero": True},
    "HU": {"name": "Hungary", "name_de": "Ungarn", "standard": 27, "reduced": [5, 18], "zero": True},
    "IE": {"name": "Ireland", "name_de": "Irland", "standard": 23, "reduced": [9, 13.5], "zero": True},
    "IT": {"name": "Italy", "name_de": "Italien", "standard": 22, "reduced": [4, 5, 10], "zero": True},
    "LV": {"name": "Latvia", "name_de": "Lettland", "standard": 21, "reduced": [5, 12], "zero": True},
    "LT": {"name": "Lithuania", "name_de": "Litauen", "standard": 21, "reduced": [5, 9], "zero": True},
    "LU": {"name": "Luxembourg", "name_de": "Luxemburg", "standard": 17, "reduced": [3, 8], "zero": True},
    "MT": {"name": "Malta", "name_de": "Malta", "standard": 18, "reduced": [5, 7], "zero": True},
    "NL": {"name": "Netherlands", "name_de": "Niederlande", "standard": 21, "reduced": [9], "zero": True},
    "PL": {"name": "Poland", "name_de": "Polen", "standard": 23, "reduced": [5, 8], "zero": True},
    "PT": {"name": "Portugal", "name_de": "Portugal", "standard": 23, "reduced": [6, 13], "zero": True},
    "RO": {"name": "Romania", "name_de": "Rumänien", "standard": 19, "reduced": [5, 9], "zero": True},
    "SK": {"name": "Slovakia", "name_de": "Slowakei", "standard": 23, "reduced": [5, 10], "zero": True},
    "SI": {"name": "Slovenia", "name_de": "Slowenien", "standard": 22, "reduced": [5, 9.5], "zero": True},
    "ES": {"name": "Spain", "name_de": "Spanien", "standard": 21, "reduced": [4, 10], "zero": True},
    "SE": {"name": "Sweden", "name_de": "Schweden", "standard": 25, "reduced": [6, 12], "zero": True},
}


def main(page: ft.Page):
    # Current language state
    current_lang = "en"

    def t(key: str) -> str:
        """Get translation for current language."""
        return TRANSLATIONS[current_lang].get(key, key)

    def get_country_name(code: str) -> str:
        """Get country name in current language."""
        info = EU_VAT_RATES[code]
        return info["name_de"] if current_lang == "de" else info["name"]

    def get_rate_options(country_code: str) -> list[ft.dropdown.Option]:
        """Generate dropdown options for the selected country's VAT rates."""
        rates = EU_VAT_RATES[country_code]
        options = [
            ft.dropdown.Option(
                str(rates["standard"]),
                f"{rates['standard']}% ({t('rate_standard')})"
            )
        ]
        for rate in rates["reduced"]:
            options.append(ft.dropdown.Option(str(rate), f"{rate}% ({t('rate_reduced')})"))
        if rates["zero"]:
            options.append(ft.dropdown.Option("0", f"0% ({t('rate_zero')})"))
        return options

    def get_country_options() -> list[ft.dropdown.Option]:
        """Generate country dropdown options in current language."""
        return [
            ft.dropdown.Option(code, f"{get_country_name(code)} ({code})")
            for code, _ in sorted(EU_VAT_RATES.items(), key=lambda x: get_country_name(x[0]))
        ]

    def open_url(e):
        """Open URL in browser."""
        if e.data:
            import webbrowser
            webbrowser.open(e.data)

    # Page setup
    page.title = t("app_title")
    page.window.width = 530
    page.window.height = 730
    page.padding = 25
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO

    # Result texts
    netto_result = ft.Text("—", size=18)
    ust_result = ft.Text("—", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700)
    brutto_result = ft.Text("—", size=18)
    country_info = ft.Text("", size=12, color=ft.Colors.GREY_600)

    # VAT categories info panel (Markdown)
    vat_info_md = ft.Markdown(
        get_vat_categories_md("DE", current_lang),
        selectable=True,
        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
        on_tap_link=open_url,
    )

    # UI elements that need translation updates
    app_title = ft.Text(t("app_title"), size=24, weight=ft.FontWeight.BOLD)
    app_subtitle = ft.Text(t("app_subtitle"), size=14, color=ft.Colors.GREY_600)
    result_title = ft.Text(t("result_title"), size=18, weight=ft.FontWeight.BOLD)
    categories_title = ft.Text(t("categories_title"), size=16, weight=ft.FontWeight.BOLD)

    result_country_label = ft.Text("", size=12, color=ft.Colors.GREY_600)
    result_rate_label = ft.Text("", size=12, color=ft.Colors.GREY_600)
    net_label = ft.Text(t("net_amount"), width=120)
    vat_label = ft.Text(t("vat_amount"), width=120)
    gross_label = ft.Text(t("gross_amount"), width=120)

    def berechnen(e):
        try:
            betrag = float(betrag_input.value.replace(",", "."))
            steuersatz = float(steuersatz_dropdown.value) / 100
            country_code = country_dropdown.value
            country_name = get_country_name(country_code)

            if berechnung_art.value == "netto_zu_brutto":
                netto = betrag
                ust = netto * steuersatz
                brutto = netto + ust
            else:  # brutto_zu_netto
                brutto = betrag
                netto = brutto / (1 + steuersatz)
                ust = brutto - netto

            netto_result.value = f"{netto:.2f} EUR"
            ust_result.value = f"{ust:.2f} EUR"
            brutto_result.value = f"{brutto:.2f} EUR"
            result_country_label.value = f"{t('result_country')} {country_name}"
            result_rate_label.value = f"{t('result_rate')} {steuersatz_dropdown.value}%"

        except ValueError:
            netto_result.value = t("error")
            ust_result.value = "—"
            brutto_result.value = "—"
            result_country_label.value = ""
            result_rate_label.value = ""

        page.update()

    def clear(e):
        betrag_input.value = ""
        netto_result.value = "—"
        ust_result.value = "—"
        brutto_result.value = "—"
        result_country_label.value = ""
        result_rate_label.value = ""
        page.update()

    # Full width for inputs (window width minus padding)
    input_width = 480

    # Amount input
    betrag_input = ft.TextField(
        label=t("amount_label"),
        hint_text=t("amount_hint"),
        keyboard_type=ft.KeyboardType.NUMBER,
        on_submit=berechnen,
        width=input_width,
    )

    # Calculation direction dropdown
    berechnung_art = ft.Dropdown(
        label=t("direction_label").rstrip(":"),
        value="netto_zu_brutto",
        options=[
            ft.dropdown.Option("netto_zu_brutto", t("net_to_gross")),
            ft.dropdown.Option("brutto_zu_netto", t("gross_to_net")),
        ],
        width=input_width,
    )

    # Tax rate dropdown
    steuersatz_dropdown = ft.Dropdown(
        label=t("rate_label"),
        value="19",
        options=get_rate_options("DE"),
        width=input_width,
    )

    # Country dropdown
    country_dropdown = ft.Dropdown(
        label=t("country_label"),
        value="DE",
        options=get_country_options(),
        width=input_width,
    )

    # Buttons
    btn_calculate = ft.Button(t("btn_calculate"), icon=ft.Icons.CALCULATE, on_click=berechnen)
    btn_clear = ft.Button(
        t("btn_clear"),
        icon=ft.Icons.CLEAR,
        on_click=clear,
        style=ft.ButtonStyle(bgcolor=ft.Colors.TRANSPARENT),
    )

    # Language selector
    lang_dropdown = ft.Dropdown(
        label=t("language"),
        value=current_lang,
        options=[
            ft.dropdown.Option("en", "English"),
            ft.dropdown.Option("de", "Deutsch"),
        ],
        width=150,
    )

    def update_rates(e):
        """Update tax rate options and info panel when country changes."""
        country_code = e.data if hasattr(e, 'data') else e.control.value
        rates = EU_VAT_RATES[country_code]
        steuersatz_dropdown.options = get_rate_options(country_code)
        steuersatz_dropdown.value = str(rates["standard"])
        country_info.value = f"{t('standard_rate_info')} {rates['standard']}%"
        # Update VAT categories info
        vat_info_md.value = get_vat_categories_md(country_code, current_lang)
        page.update()

    def change_language(e):
        """Switch UI language."""
        nonlocal current_lang
        current_lang = e.data if hasattr(e, 'data') else e.control.value

        # Update page title
        page.title = t("app_title")

        # Update all translatable texts
        app_title.value = t("app_title")
        app_subtitle.value = t("app_subtitle")
        result_title.value = t("result_title")
        categories_title.value = t("categories_title")
        net_label.value = t("net_amount")
        vat_label.value = t("vat_amount")
        gross_label.value = t("gross_amount")

        # Update input labels
        betrag_input.label = t("amount_label")
        betrag_input.hint_text = t("amount_hint")
        steuersatz_dropdown.label = t("rate_label")
        country_dropdown.label = t("country_label")
        lang_dropdown.label = t("language")

        # Update calculation direction dropdown
        berechnung_art.label = t("direction_label").rstrip(":")
        berechnung_art.options = [
            ft.dropdown.Option("netto_zu_brutto", t("net_to_gross")),
            ft.dropdown.Option("brutto_zu_netto", t("gross_to_net")),
        ]

        # Update buttons
        btn_calculate.text = t("btn_calculate")
        btn_clear.text = t("btn_clear")

        # Update country dropdown options
        country_dropdown.options = get_country_options()

        # Update rate dropdown options
        steuersatz_dropdown.options = get_rate_options(country_dropdown.value)

        # Update VAT info
        rates = EU_VAT_RATES[country_dropdown.value]
        country_info.value = f"{t('standard_rate_info')} {rates['standard']}%"
        vat_info_md.value = get_vat_categories_md(country_dropdown.value, current_lang)

        page.update()

    # Result rows with right-aligned numbers
    result_net_row = ft.Row(
        [net_label, ft.Container(expand=True), netto_result],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
    result_vat_row = ft.Row(
        [vat_label, ft.Container(expand=True), ust_result],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
    result_gross_row = ft.Row(
        [gross_label, ft.Container(expand=True), brutto_result],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    # Results card - title with country/rate info on the right
    results_header = ft.Row(
        [
            result_title,
            ft.Container(expand=True),
            ft.Column([result_country_label, result_rate_label], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.END),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )
    results_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    results_header,
                    ft.Divider(),
                    result_net_row,
                    result_vat_row,
                    result_gross_row,
                ],
                spacing=12,
            ),
            padding=25,
        ),
    )

    # Categories panel
    categories_panel = ft.Column(
        [
            categories_title,
            ft.Container(
                content=vat_info_md,
                padding=15,
                bgcolor=ft.Colors.GREY_100,
                border_radius=8,
            ),
        ],
    )

    # Header with language selector only
    header = ft.Row(
        [
            ft.Column([app_title, app_subtitle], spacing=5),
            ft.Container(expand=True),
            lang_dropdown,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Single column layout (full width)
    main_content = ft.Column(
        [
            # Inputs section - explicit widths
            country_dropdown,
            country_info,
            ft.Container(height=10),
            betrag_input,
            ft.Container(height=10),
            berechnung_art,
            ft.Container(height=10),
            steuersatz_dropdown,
            ft.Container(height=15),
            ft.Row([btn_calculate, btn_clear], spacing=10),
            # Results section
            ft.Container(height=20),
            results_card,
            # Categories section
            ft.Container(height=20),
            categories_panel,
        ],
    )

    # Layout
    page.add(
        header,
        ft.Divider(height=20),
        main_content,
    )

    # Set event handlers - Flet 0.80+ uses on_select for Dropdown
    country_dropdown.on_select = update_rates
    lang_dropdown.on_select = change_language


if __name__ == "__main__":
    ft.run(main, view=ft.AppView.WEB_BROWSER)
