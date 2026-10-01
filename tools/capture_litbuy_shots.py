#!/usr/bin/env python3
"""Dated official LitBuy SPA screenshots. Uses system Chrome."""
from __future__ import annotations

from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "sites" / "litbuy-shared" / "media"
OUT.mkdir(parents=True, exist_ok=True)


def _dismiss(page) -> None:
    page.wait_for_timeout(2500)
    for sel in (
        'button:has-text("Login In")',
        'button:has-text("Log in")',
        '[aria-label="Close"]',
        "button.close",
        ".ant-modal-close",
        "img[alt='close']",
    ):
        try:
            loc = page.locator(sel).first
            if loc.count() and loc.is_visible():
                # Prefer the X on the coupon modal, not Login
                pass
        except Exception:
            pass
    # Click the modal X if present (top-right of coupon card)
    try:
        page.keyboard.press("Escape")
        page.wait_for_timeout(400)
    except Exception:
        pass
    # Overlay click
    try:
        page.evaluate(
            """() => {
              const xs = Array.from(document.querySelectorAll('button, span, i, div'))
                .filter(el => {
                  const t = (el.getAttribute('aria-label')||'') + (el.className||'');
                  return /close|modal-close|icon-close/i.test(t);
                });
              if (xs[0]) xs[0].click();
            }"""
        )
        page.wait_for_timeout(400)
    except Exception:
        pass


def main() -> None:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        ctx = browser.new_context(
            viewport={"width": 1440, "height": 1100},
            device_scale_factor=1,
            locale="en-US",
        )
        page = ctx.new_page()
        page.set_default_timeout(60000)

        page.goto("https://litbuy.com/", wait_until="domcontentloaded")
        page.wait_for_timeout(6000)
        _dismiss(page)
        # Click away from modal: press Escape again and click the X in the coupon dialog
        try:
            # coupon dialog close — often a small x in the card corner
            page.locator("text=Your exclusive newcomer gift").locator("xpath=ancestor::div[1]").wait_for(timeout=3000)
            page.mouse.click(1380, 40)
            page.keyboard.press("Escape")
            page.wait_for_timeout(800)
        except Exception:
            pass
        dest = OUT / "official-home-20261001.jpg"
        page.screenshot(path=str(dest), full_page=False, type="jpeg", quality=82)
        print("home", dest.stat().st_size, page.title()[:70])

        page.goto("https://litbuy.com/shipping-estimate", wait_until="domcontentloaded")
        page.wait_for_timeout(7000)
        _dismiss(page)
        dest = OUT / "estimator-20261001.jpg"
        page.screenshot(path=str(dest), full_page=False, type="jpeg", quality=82)
        print("est", dest.stat().st_size, page.title()[:70])

        page.goto("https://litbuy.com/help", wait_until="domcontentloaded")
        page.wait_for_timeout(6000)
        _dismiss(page)
        dest = OUT / "help-restricted-20261001.jpg"
        page.screenshot(path=str(dest), full_page=False, type="jpeg", quality=82)
        print("help", dest.stat().st_size, page.title()[:70])

        # Open Storage Period article
        try:
            page.get_by_text("Storage Period", exact=False).first.click()
            page.wait_for_timeout(4000)
            dest = OUT / "storage-period-20261001.jpg"
            page.screenshot(path=str(dest), full_page=False, type="jpeg", quality=82)
            print("storage", dest.stat().st_size, page.url, page.title()[:70])
        except Exception as e:
            print("storage click fail", e)

        # Prohibited items
        try:
            page.goto("https://litbuy.com/help", wait_until="domcontentloaded")
            page.wait_for_timeout(4000)
            page.get_by_text("Prohibited Items", exact=False).first.click()
            page.wait_for_timeout(4000)
            dest = OUT / "prohibited-20261001.jpg"
            page.screenshot(path=str(dest), full_page=False, type="jpeg", quality=82)
            print("prohibited", dest.stat().st_size, page.url, page.title()[:70])
        except Exception as e:
            print("prohibited click fail", e)

        browser.close()


if __name__ == "__main__":
    main()
