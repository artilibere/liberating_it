#!/usr/bin/env python3
"""Targeted tests for the static site build helpers."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from build import (  # noqa: E402
    apply_structure_counts,
    build_home_faq,
    build_howto_jsonld,
    build_principles_faq,
    bundle_css,
    bundle_js,
    clean_orphan_og_images,
    build_display_icons,
    ensure_icon_thumbs,
    ensure_favicon,
    ensure_og_png,
    fase_label_it,
    format_meta_description,
    format_page_title,
    hub_meta_description,
    hub_page_title,
    italian_typography,
    italian_typography_ctx,
    load_tracking_config,
    make_env,
    render,
    HUBS_COMPLESSITA,
    HUBS_DIFFICOLTA,
    HUBS_DURATA,
    HUBS_FASE,
    LEGAL_PAGES,
    PER_BISOGNO,
    build_faq_jsonld,
    build_item_list_jsonld,
    build_organization_jsonld,
    build_share_links,
    md_block_to_html,
    md_inline,
    parse_legal_page,
    merge_jsonld,
    minify_css,
    minify_html,
    normalize_structure_count_text,
    OG_IMAGE_HEIGHT,
    OG_IMAGE_REL,
    OG_IMAGE_WIDTH,
    FAVICON_APPLE,
    FAVICON_ICO,
    FAVICON_PNG,
    parse_duration_iso,
    parse_editorial_page,
    parse_faq,
    parse_frontmatter,
    structure_og_image_url,
    structure_reading_minutes,
    format_reading_time_label,
    truncate_text,
    write_llms_txt,
    write_sitemap,
)


class ItalianTypographyTests(unittest.TestCase):
    def test_difficolta_and_common_accents(self) -> None:
        self.assertEqual(italian_typography("Difficolta' intermedia"), "Difficoltà intermedia")
        self.assertEqual(italian_typography("piu' facile"), "più facile")
        self.assertEqual(italian_typography("Cos'e' TRIZ?"), "Cos'è TRIZ?")
        self.assertEqual(italian_typography("gia' rodati"), "già rodati")

    def test_preserves_correct_apostrophes(self) -> None:
        self.assertEqual(italian_typography("l'agenda"), "l'agenda")
        self.assertEqual(italian_typography("un po' di tempo"), "un po' di tempo")
        self.assertEqual(italian_typography("regole d'oro"), "regole d'oro")

    def test_e_accent_without_breaking_elisions(self) -> None:
        self.assertEqual(italian_typography("non e' vuoto"), "non è vuoto")
        self.assertEqual(italian_typography("c'e' tempo"), "c'è tempo")

    def test_html_text_nodes(self) -> None:
        ctx = {
            "page_type": "catalog",
            "page_title": "Le strutture | Liberating.it",
            "meta_description": "Filtra per difficolta', durata e fase.",
            "canonical": "https://liberating.it/structures/",
            "active_nav": "structures",
            "has_path_nav": False,
            "breadcrumbs": [{"name": "Home", "url": "/"}, {"name": "Le strutture", "url": None}],
            "structures": [],
            "fase_filters": [],
            "jsonld": None,
        }
        fixed = italian_typography_ctx(ctx)
        self.assertIn("difficoltà", fixed["meta_description"])
        self.assertNotIn("difficolta'", fixed["meta_description"])


class RenderTypographyTests(unittest.TestCase):
    def test_catalog_page_has_difficolta_accent(self) -> None:
        import tempfile

        src_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            env = make_env(src_root / "templates", root)
            out_path = root / "structures" / "index.html"
            render(
                env,
                "catalog.html",
                out_path,
                root,
                page_type="catalog",
                page_title="Le strutture | Liberating.it",
                meta_description="Catalogo: filtra per difficolta', durata e fase.",
                canonical="https://liberating.it/structures/",
                active_nav="structures",
                has_path_nav=False,
                breadcrumbs=[{"name": "Home", "url": "/"}, {"name": "Le strutture", "url": None}],
                structures=[],
                fase_filters=[],
                jsonld=None,
            )
            html = out_path.read_text(encoding="utf-8")
        self.assertIn("Difficoltà", html)
        self.assertNotRegex(html, r"Difficolta'|difficolta'")
        self.assertIn('rel="alternate"', html)
        self.assertIn("llms.txt", html)


class ParseFaqTests(unittest.TestCase):
    def test_leading_hashes_without_newline(self) -> None:
        text = "### Cos'e' 1-2-4-All?\nRisposta breve."
        items = parse_faq(text)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["question"], "Cos'e' 1-2-4-All?")
        self.assertNotIn("###", items[0]["question"])

    def test_multiple_questions(self) -> None:
        text = "### Prima?\nUno.\n\n### Seconda?\nDue."
        items = parse_faq(text)
        self.assertEqual(len(items), 2)


class DurationTests(unittest.TestCase):
    def test_minutes(self) -> None:
        self.assertEqual(parse_duration_iso("15 minuti"), "PT15M")
        self.assertEqual(parse_duration_iso("1 min"), "PT1M")

    def test_hours_and_minutes(self) -> None:
        self.assertEqual(parse_duration_iso("2 h 30 min"), "PT2H30M")

    def test_variable_returns_none(self) -> None:
        self.assertIsNone(parse_duration_iso("variabile"))


class JsonLdTests(unittest.TestCase):
    def test_merge_graph(self) -> None:
        raw = merge_jsonld({"@type": "FAQPage"}, {"@type": "HowTo"})
        data = json.loads(raw or "{}")
        self.assertIn("@graph", data)
        self.assertEqual(len(data["@graph"]), 2)

    def test_howto_perform_time_iso(self) -> None:
        structure = {
            "h1": "1-2-4-All",
            "url": "https://liberating.it/structures/1-2-4-all/",
            "durata": "15 minuti",
            "brief_plain": "Definizione breve.",
            "steps": [{"action": "Rifletti da solo", "time": "1 min"}],
            "prep_items": ["Timer"],
        }
        howto = build_howto_jsonld(structure)
        assert howto is not None
        self.assertEqual(howto["totalTime"], "PT15M")
        self.assertEqual(howto["step"][0]["performTime"], "PT1M")


class EditorialTests(unittest.TestCase):
    def test_principles_page_has_ten_sections(self) -> None:
        path = Path(__file__).resolve().parents[2] / "content" / "v1" / "pagine" / "10-principi-fondamentali-liberating-structures.md"
        if not path.exists():
            self.skipTest("principles markdown not found")
        editorial = parse_editorial_page(path)
        self.assertEqual(len(editorial["sections"]), 10)
        self.assertIn("Inclusione reale", editorial["sections"][0]["title"])
        self.assertIn("<a href=", editorial["sections"][0]["body"])


class FrontmatterTests(unittest.TestCase):
    def test_parse_frontmatter(self) -> None:
        raw = "---\ntitle: Test\n---\n# Body\n"
        meta, body = parse_frontmatter(raw)
        self.assertEqual(meta["title"], "Test")
        self.assertIn("# Body", body)


class FormatPageTitleTests(unittest.TestCase):
    def test_short_title_unchanged(self) -> None:
        self.assertEqual(
            format_page_title("1-2-4-All: far parlare tutti"),
            "1-2-4-All: far parlare tutti | Liberating.it",
        )

    def test_long_title_truncated_to_sixty(self) -> None:
        title = format_page_title(
            "Open Space Technology (OST): workshop auto-organizzati"
        )
        self.assertLessEqual(len(title), 60)
        self.assertTrue(title.endswith("| Liberating.it"))

    def test_empty_title_fallback(self) -> None:
        self.assertEqual(format_page_title(""), "Liberating.it")


class FormatMetaDescriptionTests(unittest.TestCase):
    def test_short_description_unchanged(self) -> None:
        text = "Breve meta description."
        self.assertEqual(format_meta_description(text), text)

    def test_long_description_truncated(self) -> None:
        text = "A" * 200
        result = format_meta_description(text)
        from html import escape

        self.assertLessEqual(len(escape(result)), 155)
        self.assertTrue(result.endswith("…"))

    def test_apostrophe_respects_escaped_length(self) -> None:
        text = "15% Solutions chiede a ognuno: cosa puoi fare subito con le risorse e l'autonomia che hai gia' oggi, senza aspettare il resto del team."
        from html import escape

        result = format_meta_description(text)
        self.assertLessEqual(len(escape(result)), 155)


class HubSeoTests(unittest.TestCase):
    def test_intermedia_hub_page_title(self) -> None:
        hub = HUBS_DIFFICOLTA["intermedia"]
        title = hub_page_title(hub)
        self.assertIn("Liberating Structures intermedie", title)
        self.assertLessEqual(len(title), 60)

    def test_intermedia_hub_faq_jsonld(self) -> None:
        faq_ld = build_faq_jsonld(HUBS_DIFFICOLTA["intermedia"]["faq"])
        self.assertIsNotNone(faq_ld)
        assert faq_ld is not None
        self.assertEqual(faq_ld["@type"], "FAQPage")
        self.assertEqual(len(faq_ld["mainEntity"]), 4)


class AllHubsHaveFaqTests(unittest.TestCase):
    def test_every_taxonomy_hub_has_faq(self) -> None:
        for collection in (HUBS_COMPLESSITA, HUBS_DIFFICOLTA, HUBS_DURATA, HUBS_FASE, PER_BISOGNO):
            for slug, hub in collection.items():
                faq = hub.get("faq") or []
                self.assertGreaterEqual(len(faq), 2, msg=f"{slug} missing FAQ")


class LegalPageTests(unittest.TestCase):
    def test_md_block_to_html_renders_lists(self) -> None:
        html = md_block_to_html("- Primo\n- Secondo")
        self.assertIn("<ul>", html)
        self.assertIn("<li>Primo</li>", html)

    def test_md_inline_mailto_links(self) -> None:
        html = md_inline("Scrivi a [ciao@carlogandolfo.it](mailto:ciao@carlogandolfo.it)")
        self.assertIn('href="mailto:ciao@carlogandolfo.it"', html)
        self.assertIn("ciao@carlogandolfo.it</a>", html)

    def test_legal_pages_contact_details(self) -> None:
        root = Path(__file__).resolve().parents[2] / "content/v1/pagine"
        for slug in LEGAL_PAGES:
            path = root / f"{slug}.md"
            if not path.exists():
                self.skipTest(f"{slug}.md not found")
            text = path.read_text(encoding="utf-8")
            self.assertIn("Carlo Gandolfo", text)
            self.assertIn("ciao@carlogandolfo.it", text)
            self.assertNotIn("info@liberating.it", text)

    def test_parse_privacy_policy_sections(self) -> None:
        path = Path(__file__).resolve().parents[2] / "content/v1/pagine/privacy-policy.md"
        if not path.exists():
            self.skipTest("privacy-policy.md not found")
        legal = parse_legal_page(path)
        self.assertEqual(legal["h1"], "Privacy Policy")
        self.assertGreaterEqual(len(legal["sections"]), 5)
        self.assertIn("<h3>", legal["sections"][2]["html"])

    def test_sitemap_includes_legal_pages(self) -> None:
        import tempfile

        content_root = Path(__file__).resolve().parents[2] / "content/v2"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_sitemap([], root, content_root=content_root)
            text = (root / "sitemap.xml").read_text(encoding="utf-8")
        for slug in LEGAL_PAGES:
            self.assertIn(f"{slug}/", text)


class SpeedTests(unittest.TestCase):
    def test_minify_html_collapses_tag_whitespace(self) -> None:
        raw = "<div>\n  <p>Test</p>\n</div>"
        self.assertEqual(minify_html(raw), "<div><p>Test</p></div>")

    def test_bundle_css_writes_manifest(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            css_dir = root / "assets" / "css"
            js_dir = root / "assets" / "js"
            css_dir.mkdir(parents=True)
            js_dir.mkdir(parents=True)
            for name in ("tokens.css", "base.css", "components.css"):
                (css_dir / name).write_text(f"body{{margin:0 /* {name} */}}", encoding="utf-8")
            (js_dir / "nav.js").write_text("(function () { return 1; })();\n", encoding="utf-8")
            manifest, css_inline = bundle_css(root)
            bundle_js(root)
            self.assertTrue(css_inline)
            self.assertTrue((css_dir / Path(manifest["css"]).name).exists())
            self.assertTrue((root / "assets" / "build-manifest.json").exists())
            built = json.loads((root / "assets" / "build-manifest.json").read_text())
            self.assertIn("js", built)
            self.assertIn("nav", built["js"])

    def test_apply_structure_counts(self) -> None:
        editorial = {
            "lead": "Dietro a tutte le 35 strutture.",
            "sections": [{"title": "A", "body": "35 schede nel catalogo."}],
            "leggi_anche": [{"name": "Cat", "url": "/structures/", "reason": "tutte le 35 schede"}],
            "faq": [{"question": "Quante?", "answer": "Sono 35 formati pratici."}],
        }
        apply_structure_counts(editorial, 41)
        self.assertIn("41 strutture", editorial["lead"])
        self.assertIn("41 schede", editorial["sections"][0]["body"])
        self.assertIn("41 schede", editorial["leggi_anche"][0]["reason"])
        self.assertIn("41 formati", editorial["faq"][0]["answer"])

    def test_normalize_structure_count_text_variants(self) -> None:
        text = (
            "35 Liberating Structures, 35 formati, tutte le 35, "
            "sui 35 strumenti pratici."
        )
        result = normalize_structure_count_text(text, 41)
        self.assertIn("41 Liberating Structures", result)
        self.assertIn("41 formati", result)
        self.assertIn("tutte le 41", result)
        self.assertIn("sui 41 strumenti", result)

    def test_home_faq_uses_structure_count(self) -> None:
        faq = build_home_faq(41)
        self.assertIn("41 schede", faq[2]["answer"])
        faq39 = build_home_faq(39)
        self.assertIn("39 schede", faq39[2]["answer"])

    def test_principles_faq_mentions_counts(self) -> None:
        faq = build_principles_faq(41)
        self.assertIn("33 formati ufficiali", faq[0]["answer"])
        self.assertIn("41 schede", faq[0]["answer"])

    def test_minify_css_strips_comments_and_whitespace(self) -> None:
        raw = "/* note */\n.foo { color: red; }\n"
        self.assertEqual(minify_css(raw), ".foo{color:red;}")

    def test_build_display_icons_uses_ls_menu_fallback(self) -> None:
        import shutil
        import tempfile

        from generate_adaptation_icons import LS_MENU_ICON_REL, ensure_ls_menu_icon

        src_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(src_root / "assets/images/structures", root / "assets/images/structures")
            ensure_ls_menu_icon(root)
            icons_full = {"1-2-4-all": "assets/images/structures/1-2-4-all.png"}
            display_icons, default_icon, default_full = build_display_icons(root, icons_full)
        self.assertEqual(default_full, LS_MENU_ICON_REL)
        self.assertIn("ls-menu", default_icon)
        self.assertEqual(display_icons["1-2-4-all"], "assets/images/structures/thumbs/1-2-4-all.png")
        self.assertNotIn("missing", display_icons)

    def test_monochrome_structure_icon_uses_black_on_white(self) -> None:
        from icon_mono import MONO_BLACK, MONO_WHITE, monochrome_structure_icon
        from PIL import Image

        sample = Image.new("RGB", (40, 40), MONO_WHITE)
        sample.paste((255, 0, 0), (10, 10, 30, 30))
        mono = monochrome_structure_icon(sample)
        self.assertEqual(mono.getpixel((0, 0)), MONO_WHITE)
        self.assertEqual(mono.getpixel((20, 20)), MONO_BLACK)

    def test_ensure_icon_thumbs_smaller_than_source(self) -> None:
        import shutil
        import tempfile

        src_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(src_root / "assets/images/structures", root / "assets/images/structures")
            manifest = json.loads((root / "assets/images/structures/manifest.json").read_text())
            thumbs = ensure_icon_thumbs(root, manifest)
            self.assertIn("1-2-4-all", thumbs)
            thumb = root / thumbs["1-2-4-all"]
            full = root / manifest["1-2-4-all"]
            self.assertTrue(thumb.exists())
            self.assertLess(thumb.stat().st_size, full.stat().st_size)


class SeoGeoTests(unittest.TestCase):
    def test_hub_meta_description_prefers_dedicated_field(self) -> None:
        hub = {
            "intro": "Breve intro visiva.",
            "meta_description": "Meta SEO piu' lunga con keyword Liberating Structures.",
        }
        self.assertEqual(hub_meta_description(hub), hub["meta_description"])

    def test_hub_meta_description_falls_back_to_intro(self) -> None:
        hub = {"intro": "Solo intro."}
        self.assertEqual(hub_meta_description(hub), "Solo intro.")

    def test_llms_txt_includes_high_traffic_structures(self) -> None:
        import tempfile

        structures = [
            {
                "slug": "drawing-together",
                "title": "Drawing Together",
                "brief_plain": "Definizione di prova per llms.txt.",
            },
            {
                "slug": "1-2-4-all",
                "title": "1-2-4-All",
                "brief_plain": "Altra definizione.",
            },
        ]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_llms_txt(structures, root)
            text = (root / "llms.txt").read_text(encoding="utf-8")
        self.assertIn("drawing-together", text)
        self.assertIn("Schede con più traffico", text)
        self.assertIn("difficolta/intermedia", text)
        self.assertIn("Hub per difficoltà", text)
        self.assertIn("Cos'è una Liberating Structure?", text)
        self.assertIn("Percorso per iniziare subito", text)

    def test_item_list_jsonld_lists_structures(self) -> None:
        items = [
            {"slug": "triz", "title": "TRIZ"},
            {"slug": "ecocycle-planning", "title": "Ecocycle Planning"},
        ]
        data = build_item_list_jsonld("Strutture intermedie", items, "https://liberating.it/difficolta/intermedia/")
        assert data is not None
        self.assertEqual(data["@type"], "ItemList")
        self.assertEqual(data["numberOfItems"], 2)
        self.assertEqual(data["itemListElement"][0]["url"], "https://liberating.it/structures/triz/")

    def test_intermedia_hub_meta_mentions_primary_keywords(self) -> None:
        hub = HUBS_DIFFICOLTA["intermedia"]
        meta = hub_meta_description(hub)
        self.assertIn("Liberating Structures", meta)
        self.assertIn("TRIZ", meta)
        self.assertLessEqual(len(format_meta_description(meta)), 155)

    def test_sitemap_includes_lastmod(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_sitemap(
                [{"slug": "1-2-4-all", "source_lastmod": "2024-06-01"}],
                root,
            )
            text = (root / "sitemap.xml").read_text(encoding="utf-8")
        self.assertIn("<lastmod>", text)
        self.assertIn("2024-06-01", text)


class ReviewFixTests(unittest.TestCase):
    def test_clean_orphan_og_images_removes_stale_files(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            og_dir = root / "assets/images/og"
            og_dir.mkdir(parents=True)
            (og_dir / "1-2-4-all.png").write_bytes(b"png")
            (og_dir / "removed-slug.png").write_bytes(b"png")
            structures = [{"slug": "1-2-4-all"}]
            clean_orphan_og_images(structures, root)
            self.assertTrue((og_dir / "1-2-4-all.png").exists())
            self.assertFalse((og_dir / "removed-slug.png").exists())


class TruncateTests(unittest.TestCase):
    def test_truncate_text_at_word_boundary(self) -> None:
        text = "Una frase lunga che deve essere tagliata prima della fine della parola successiva."
        result = truncate_text(text, 50)
        self.assertTrue(result.endswith("..."))
        self.assertLess(len(result), 53)
        self.assertNotIn(" parola", result)

    def test_truncate_text_short_unchanged(self) -> None:
        self.assertEqual(truncate_text("Breve", 50), "Breve")


class DeiTests(unittest.TestCase):
    def test_fase_label_it_uses_italian_labels(self) -> None:
        self.assertEqual(fase_label_it("Ideate", "ideate"), "Ideare")
        self.assertEqual(fase_label_it("Empathize", "empathize"), "Empatizzare")

    def test_principles_faq_covers_quiet_participants(self) -> None:
        faq = build_principles_faq(41)
        questions = [item["question"] for item in faq]
        self.assertTrue(any("silenzio" in q.lower() for q in questions))

    def test_llms_txt_includes_inclusion_structures(self) -> None:
        import tempfile

        structures = [
            {
                "slug": "heard-seen-respected-hsr",
                "title": "HSR",
                "brief_plain": "Ascolto empatico nel gruppo.",
            },
        ]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_llms_txt(structures, root)
            text = (root / "llms.txt").read_text(encoding="utf-8")
        self.assertIn("inclusione e partecipazione", text)
        self.assertIn("heard-seen-respected-hsr", text)


class SocialTests(unittest.TestCase):
    def test_structure_reading_minutes(self) -> None:
        structure = {
            "brief_plain": " ".join(["parola"] * 400),
            "steps": [{"action": "passo"}],
        }
        self.assertEqual(structure_reading_minutes(structure), 2)
        self.assertEqual(format_reading_time_label(1), "1 minuto")
        self.assertEqual(format_reading_time_label(3), "3 minuti")

    def test_build_share_links_match_wordpress_networks(self) -> None:
        links = build_share_links(
            "https://liberating.it/structures/1-2-4-all/",
            "1-2-4-All",
        )
        self.assertIn("linkedin.com/shareArticle", links["linkedin"])
        self.assertIn("facebook.com/sharer.php", links["facebook"])
        self.assertIn("x.com/intent/post", links["x"])

    def test_organization_jsonld_includes_same_as(self) -> None:
        org = build_organization_jsonld()
        self.assertIn("sameAs", org)
        self.assertIn("linkedin.com/in/carlogandolfo", org["sameAs"][0])

    def test_structure_page_includes_social_meta_and_share(self) -> None:
        import shutil
        import tempfile

        src_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(src_root / "templates", root / "templates")
            env = make_env(root / "templates", root)
            out = root / "structures" / "demo" / "index.html"
            render(
                env,
                "structure.html",
                out,
                root,
                page_type="structure",
                page_title="Demo | Liberating.it",
                meta_description="Test",
                canonical="https://liberating.it/structures/demo/",
                llms_url="https://liberating.it/llms.txt",
                og_type="article",
                og_image="https://liberating.it/assets/images/og/demo.png",
                og_image_width=1200,
                og_image_height=630,
                og_image_type="image/png",
                og_image_alt="Demo",
                has_path_nav=False,
                jsonld=None,
                reading_time_label="3 minuti",
                share=build_share_links(
                    "https://liberating.it/structures/demo/",
                    "Demo struttura",
                ),
                structure={
                    "slug": "demo",
                    "h1": "Demo struttura",
                    "brief": "",
                    "difficolta_slug": "facile",
                    "complessita_slug": "iniziare-subito",
                    "durata_slug": "breve",
                    "fase_slug": "discover",
                },
            )
            html = out.read_text(encoding="utf-8")
            self.assertIn('name="twitter:label1" content="Tempo di lettura stimato"', html)
            self.assertIn('name="twitter:data1" content="3 minuti"', html)
            self.assertIn("linkedin.com/shareArticle", html)
            self.assertIn("ls-share__copy", html)
            self.assertIn('aria-live="polite"', html)
            self.assertIn("Condividi su LinkedIn", html)

    def test_ensure_og_png_creates_1200x630(self) -> None:
        import shutil
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            assets = root / "assets" / "images"
            assets.mkdir(parents=True)
            shutil.copy(
                Path(__file__).resolve().parents[1] / "assets/images/og.svg",
                assets / "og.svg",
            )
            ensure_og_png(root)
            png = root / OG_IMAGE_REL
            self.assertTrue(png.exists())
            from PIL import Image

            with Image.open(png) as img:
                self.assertEqual(img.size, (OG_IMAGE_WIDTH, OG_IMAGE_HEIGHT))

    def test_ensure_favicon_from_ls_menu_icon(self) -> None:
        import tempfile

        from generate_adaptation_icons import ensure_ls_menu_icon

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ensure_ls_menu_icon(root)
            ensure_favicon(root)
            self.assertTrue((root / FAVICON_ICO).exists())
            self.assertTrue((root / FAVICON_PNG).exists())
            self.assertTrue((root / FAVICON_APPLE).exists())
            from PIL import Image

            with Image.open(root / FAVICON_PNG) as img:
                self.assertEqual(img.size, (32, 32))
            with Image.open(root / FAVICON_APPLE) as img:
                self.assertEqual(img.size, (180, 180))

    def test_structure_og_image_composites_icon(self) -> None:
        import shutil
        import tempfile

        src_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(src_root / "assets/images", root / "assets/images")
            ensure_og_png(root)
            structure = {
                "slug": "1-2-4-all",
                "icon": "assets/images/structures/1-2-4-all.png",
            }
            url = structure_og_image_url(structure, root)
            self.assertIn("/assets/images/og/1-2-4-all.png", url)
            self.assertTrue((root / "assets/images/og/1-2-4-all.png").exists())

    def test_structure_og_title_fallback_without_icon(self) -> None:
        import shutil
        import tempfile

        src_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(src_root / "assets/images", root / "assets/images")
            ensure_og_png(root)
            structure = {
                "slug": "triz",
                "title": "TRIZ: superare i compromessi",
            }
            url = structure_og_image_url(structure, root)
            self.assertIn("/assets/images/og/triz.png", url)
            self.assertTrue((root / "assets/images/og/triz.png").exists())

    def test_adaptation_icons_in_manifest(self) -> None:
        from generate_adaptation_icons import ADAPTATIONS, LS_MENU_ICON_REL, ensure_adaptation_icons

        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ensure_adaptation_icons(root)
            manifest = json.loads((root / "assets/images/structures/manifest.json").read_text())
            for slug in ADAPTATIONS:
                self.assertIn(slug, manifest)
                self.assertTrue((root / manifest[slug]).exists())
            self.assertTrue((root / LS_MENU_ICON_REL).exists())


class TrackingTests(unittest.TestCase):
    def test_load_tracking_config_gtm_only(self) -> None:
        cfg = load_tracking_config()
        self.assertTrue(cfg["enabled"])
        self.assertEqual(cfg["gtm_id"], "GTM-KN9M84W")
        self.assertTrue(cfg["consent_default_denied"])

    def test_load_tracking_config_invalid_json_disables_tracking(self) -> None:
        import json
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("{not valid json")
            bad_path = Path(f.name)
        try:
            cfg = load_tracking_config(bad_path)
            self.assertFalse(cfg["enabled"])
            self.assertEqual(cfg["gtm_id"], "")
        finally:
            bad_path.unlink(missing_ok=True)

    def test_consent_mode_default_denied_before_gtm(self) -> None:
        import shutil
        import tempfile

        src_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(src_root / "templates", root / "templates")
            env = make_env(root / "templates", root)
            out = root / "privacy-policy" / "index.html"
            render(
                env,
                "legal.html",
                out,
                root,
                page_type="legal",
                page_title="Privacy Policy | Liberating.it",
                meta_description="Test",
                canonical="https://liberating.it/privacy-policy/",
                llms_url="https://liberating.it/llms.txt",
                og_type="website",
                og_image="https://liberating.it/assets/images/og/default.png",
                og_image_width=1200,
                og_image_height=630,
                og_image_type="image/png",
                og_image_alt="Liberating.it",
                has_path_nav=False,
                jsonld=None,
                legal={"title": "Privacy Policy", "sections": []},
            )
            html = out.read_text(encoding="utf-8")
            charset_pos = html.find('charset="utf-8"')
            consent_pos = html.find("gtag('consent','default'")
            gtm_pos = html.find("googletagmanager.com/gtm.js")
            self.assertGreater(charset_pos, -1)
            self.assertGreater(consent_pos, charset_pos)
            self.assertGreater(gtm_pos, consent_pos)
            self.assertIn("'analytics_storage':'denied'", html)
            self.assertIn("ls-cookie-consent", html)
            self.assertIn("consent.js", html)
            self.assertIn("aria-modal=\"false\"", html)
            self.assertIn("data-action=\"cookie-preferences\"", html)

    def test_tracking_snippets_in_rendered_html(self) -> None:
        import shutil
        import tempfile

        src_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(src_root / "templates", root / "templates")
            env = make_env(root / "templates", root)
            out = root / "privacy-policy" / "index.html"
            render(
                env,
                "legal.html",
                out,
                root,
                page_type="legal",
                page_title="Privacy Policy | Liberating.it",
                meta_description="Test",
                canonical="https://liberating.it/privacy-policy/",
                llms_url="https://liberating.it/llms.txt",
                og_type="website",
                og_image="https://liberating.it/assets/images/og/default.png",
                og_image_width=1200,
                og_image_height=630,
                og_image_type="image/png",
                og_image_alt="Liberating.it",
                has_path_nav=False,
                jsonld=None,
                legal={"title": "Privacy Policy", "sections": []},
            )
            html = out.read_text(encoding="utf-8")
            self.assertIn("GTM-KN9M84W", html)
            self.assertIn("googletagmanager.com/gtm.js", html)
            self.assertNotIn("gtag/js", html)
            self.assertNotIn("GT-M34QZZ2", html)
            self.assertIn("googletagmanager.com/ns.html?id=GTM-KN9M84W", html)


if __name__ == "__main__":
    unittest.main()
