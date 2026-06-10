"""WestLaw Next Playwright scraper — search and document retrieval.

Uses institutional access (university subscription) to automate searches
on WestLaw Next (1.next.westlaw.com) via headless Chromium.
"""

from __future__ import annotations

import asyncio
import logging
import os
import random
from typing import Any

logger = logging.getLogger(__name__)

# ── DOM Selector Constants (centralised for easy maintenance when Westlaw redesigns) ──
SEARCH_BOX_SELECTORS = (
    "#searchInputId, #co_search_headerSearch, "
    'input[name="SearchText"], textarea[id*="search"]'
)
DOC_CONTENT_SELECTORS = (
    "#co_document, [id*='documentContent'], "
    "[class*='document-body'], [class*='co_content']"
)
DOC_CONTENT_FALLBACK_SELECTORS = "article, .content, main"
RESULT_SELECTORS = (
    "#co_searchResults_citizenshipResults, "
    '[id*="cobalt_result_"], .co_searchResult, '
    "#coid_website_searchResults, #co_resultHeader"
)

# Singleton browser/context — reused across tool calls within one session
_browser = None
_context = None
_page = None
_logged_in = False
_lock = asyncio.Lock()  # Prevent concurrent access to the singleton _page


async def _ensure_browser():
    """Launch Playwright browser if not already running."""
    global _browser, _context, _page
    if _browser is not None and _page is not None:
        return _page

    from playwright.async_api import async_playwright

    pw = await async_playwright().start()
    _browser = await pw.chromium.launch(
        headless=True,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
        ],
    )
    _context = await _browser.new_context(
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        viewport={"width": 1920, "height": 1080},
        locale="en-US",
    )
    _page = await _context.new_page()
    return _page


async def _human_delay(min_s: float = 1.0, max_s: float = 3.0):
    """Random delay to mimic human behavior."""
    await asyncio.sleep(random.uniform(min_s, max_s))


# Playwright raises these (as a plain Error) when a navigation tears down the JS
# execution context mid-evaluate. Westlaw Classic redirects to its results URL
# while the page is still settling, so a single evaluate() can lose its context.
_NAV_DESTROYED_MARKERS = (
    "Execution context was destroyed",
    "context was destroyed",
    "Cannot find context",
    "frame got detached",
    "Target closed",
    "Target page, context or browser has been closed",
)


def _is_navigation_destroyed_error(exc: Exception) -> bool:
    """True if the exception is a transient navigation-destroyed-context error."""
    msg = str(exc)
    return any(marker in msg for marker in _NAV_DESTROYED_MARKERS)


async def _settle_page(page, timeout_ms: int = 15000) -> None:
    """Best-effort wait for an in-flight navigation to finish."""
    for state in ("domcontentloaded", "networkidle"):
        try:
            await page.wait_for_load_state(state, timeout=timeout_ms)
        except Exception:
            pass


async def _evaluate_with_retry(page, script: str, arg: Any = None, *, retries: int = 4):
    """Run ``page.evaluate`` retrying when a concurrent navigation destroys the
    JS execution context.

    This is the root-cause fix for the intermittent "Execution context was
    destroyed, most likely because of a navigation" failure that forced the
    Westlaw scraper to fall back to the free CourtListener source. Between
    attempts we let the page reach a stable load state so the navigation that
    killed the previous context has completed before we grab a new one.
    """
    last_exc: Exception | None = None
    for attempt in range(retries):
        try:
            if arg is None:
                return await page.evaluate(script)
            return await page.evaluate(script, arg)
        except Exception as exc:  # noqa: BLE001 — Playwright raises a plain Error
            if not _is_navigation_destroyed_error(exc):
                raise
            last_exc = exc
            logger.warning(
                "page.evaluate context destroyed (attempt %d/%d) — "
                "waiting for navigation to settle before retry",
                attempt + 1,
                retries,
            )
            await _settle_page(page)
            await _human_delay(0.5, 1.0)
    # Exhausted retries — surface the last navigation error to the caller.
    assert last_exc is not None
    raise last_exc


async def _solve_captcha(page) -> str:
    """Solve CAPTCHA image using ddddocr OCR."""
    try:
        import ddddocr
    except ImportError:
        logger.warning("ddddocr not installed — cannot solve CAPTCHA")
        return ""

    ocr = ddddocr.DdddOcr(show_ad=False)

    # Find CAPTCHA image (src contains /captcha/)
    captcha_img = page.locator('img[src*="captcha"]')
    if await captcha_img.count() == 0:
        # Fallback: find small images likely to be CAPTCHAs
        all_imgs = await page.query_selector_all("img")
        for img in all_imgs:
            width = await img.evaluate("el => el.width")
            height = await img.evaluate("el => el.height")
            if 50 < width < 300 and 20 < height < 100:
                img_bytes = await img.screenshot()
                result = ocr.classification(img_bytes)
                logger.info("CAPTCHA OCR (fallback): %s", result)
                return result
        return ""

    img_bytes = await captcha_img.first.screenshot()
    result = ocr.classification(img_bytes)
    logger.info("CAPTCHA OCR: %s", result)
    return result


async def _handle_institution_sso(page) -> bool:
    """Handle university SSO login (institution IDM with CAPTCHA).

    Returns True if SSO login was attempted and succeeded.
    Set INSTITUTION_SSO_DOMAIN env var to your institution's SSO domain
    (e.g. "idm.example.edu") to enable.
    """
    sso_domain = os.getenv("INSTITUTION_SSO_DOMAIN", "")
    if not sso_domain:
        return False
    current_url = page.url
    if sso_domain not in current_url:
        return False

    username = os.getenv("WESTLAW_USERNAME", "")
    password = os.getenv("WESTLAW_PASSWORD", "")
    if not username or not password:
        logger.warning("Institution SSO detected but no credentials set")
        return False

    max_captcha_retries = 8
    for attempt in range(max_captcha_retries):
        logger.info("Institution SSO login attempt %d/%d", attempt + 1, max_captcha_retries)

        if sso_domain not in page.url:
            logger.info("No longer on institution SSO page — redirected to: %s", page.url[:100])
            return True

        # Fill username (use input[name=] to avoid matching <label> with same ID)
        user_input = page.locator('input[name="username"]')
        if await user_input.count() > 0:
            await user_input.first.fill(username)
            await _human_delay(0.3, 0.5)

        # Fill password
        pwd_input = page.locator('input[name="password"]')
        if await pwd_input.count() > 0:
            await pwd_input.first.fill(password)
            await _human_delay(0.3, 0.5)

        # Solve CAPTCHA
        captcha_input = page.locator('#checkNum, input[name="captcha_value"]')
        if await captcha_input.count() > 0:
            try:
                captcha_text = await _solve_captcha(page)
            except Exception as e:
                logger.warning("CAPTCHA OCR exception on attempt %d: %s", attempt + 1, e)
                captcha_text = ""

            if not captcha_text:
                logger.warning("Could not solve CAPTCHA on attempt %d", attempt + 1)
                await page.reload(wait_until="domcontentloaded")
                await _human_delay(1, 2)
                continue
            await captcha_input.first.fill(captcha_text)
            await _human_delay(0.3, 0.5)

        # Submit
        submit = page.locator(
            'input[type="submit"], button:has-text("登入"), button:has-text("Login")'
        )
        if await submit.count() > 0:
            await submit.first.click()
            logger.info("Submitted SSO form, waiting for redirect chain...")

            # Wait for the redirect chain to complete (SSO → OpenAthens → TR → WestLaw)
            # The chain goes through openathens.net and signon.thomsonreuters.com
            for _ in range(6):
                await asyncio.sleep(2)
                try:
                    await page.wait_for_load_state("domcontentloaded", timeout=5000)
                except Exception:
                    pass
                new_url = page.url
                if sso_domain not in new_url:
                    logger.info("SSO login successful! Redirected to: %s", new_url[:100])
                    return True

            # Still on institution SSO — check for error messages (wrong CAPTCHA)
            error_el = page.locator('.error, .alert-danger, [class*="error"], .errorMessage')
            if await error_el.count() > 0:
                error_text = await error_el.first.text_content() or ""
                if error_text.strip():
                    logger.warning("SSO login error: %s", error_text.strip()[:100])

            logger.info("Still on SSO page, retrying with new CAPTCHA...")
            await _human_delay(1, 2)

    logger.error("Failed to pass institution SSO after %d attempts", max_captcha_retries)
    return False


async def _handle_onepass_login(page) -> bool:
    """Handle Thomson Reuters OnePass login.

    Returns True if OnePass login was attempted.
    """
    username_input = page.locator('input[id="Username"], input[name="Username"]')
    if await username_input.count() == 0:
        return False

    username = os.getenv("WESTLAW_USERNAME", "")
    password = os.getenv("WESTLAW_PASSWORD", "")
    if not username or not password:
        return False

    logger.info("Filling OnePass credentials")
    await username_input.first.fill(username)
    await _human_delay(0.5, 1.0)

    pwd_input = page.locator('input[id="Password"], input[name="Password"]')
    if await pwd_input.count() > 0:
        await pwd_input.first.fill(password)
        await _human_delay(0.5, 1.0)

    submit = page.locator(
        '#SignIn, button[id="SignIn"], button[type="submit"], input[type="submit"]'
    )
    if await submit.count() > 0:
        await submit.first.click()
        logger.info("Submitted OnePass login, waiting for redirect...")
        try:
            await page.wait_for_url("**/next.westlaw.com/**", timeout=20000)
        except Exception:
            await page.wait_for_load_state("domcontentloaded", timeout=15000)
        await _human_delay(3, 5)

    return True


async def _handle_client_id_login(page) -> bool:
    """Handle Westlaw Client ID form login.

    Returns True if Client ID login was attempted.
    """
    # WestLaw Classic Client ID form (#co_clientIDTextbox or generic ClientID input)
    client_id_input = page.locator(
        '#co_clientIDTextbox, input[name="clientIdTextbox"], '
        'input[name="ClientID"], input[id*="clientId"], input[id*="ClientId"]'
    )
    if await client_id_input.count() == 0:
        return False

    logger.info("Client ID form detected, filling and submitting...")

    # Dismiss cookie consent banner if present (OneTrust)
    try:
        cookie_btn = page.locator("#onetrust-accept-btn-handler")
        if await cookie_btn.count() > 0 and await cookie_btn.first.is_visible():
            await cookie_btn.first.click()
            await _human_delay(0.5, 1.0)
    except Exception:
        pass

    # Fill Client ID if empty (pre-filled after SSO, but use env var as fallback)
    try:
        current_val = await client_id_input.first.input_value()
        if not current_val.strip():
            client_id = os.getenv("WESTLAW_CLIENT_ID", "")
            if client_id:
                await client_id_input.first.fill(client_id)
                await _human_delay(0.3, 0.5)
                logger.info("Filled Client ID from env var")
    except Exception:
        pass

    # Client ID is usually pre-filled; just click Continue
    continue_btn = page.locator(
        '#co_clientIDContinueButton, button:has-text("Continue"), '
        'input[value="Continue"], button[type="submit"], input[type="submit"]'
    )
    if await continue_btn.count() > 0:
        await continue_btn.first.click()
        await _human_delay(2, 3)
        try:
            await page.wait_for_load_state("domcontentloaded", timeout=15000)
        except Exception:
            pass

    return True


async def _check_session_health() -> bool:
    """Check if the current Westlaw session is still valid."""
    if _page is None:
        return False
    try:
        current_url = _page.url
        # SSO expired: redirected back to login page
        sso_domain = os.getenv("INSTITUTION_SSO_DOMAIN", "")
        if (sso_domain and sso_domain in current_url) or "signon.thomsonreuters.com" in current_url:
            logger.warning("WESTLAW_SESSION expired — redirected to SSO: %s", current_url[:100])
            return False
        if "westlaw" in current_url.lower():
            return True
        return False
    except Exception:
        return False


async def _ensure_logged_in():
    """Navigate to Westlaw and handle login (institution SSO / OnePass / Client ID)."""
    global _logged_in

    if _logged_in:
        if not await _check_session_health():
            logger.info("WESTLAW_SESSION re-login required")
            _logged_in = False
    if _logged_in:
        return

    page = await _ensure_browser()

    # Use institution proxy URL if set, otherwise direct Westlaw URL
    # Priority: WESTLAW_BASE_URL > OPENATHENS_WAYFLESS_URL > direct westlaw.com
    base_url = os.getenv("WESTLAW_BASE_URL", "") or os.getenv("OPENATHENS_WAYFLESS_URL", "")
    if not base_url:
        base_url = "https://1.next.westlaw.com/Search/Home.html?transitionType=Default&contextData=(sc.Default)"

    logger.info("WESTLAW_NAV base_url=%s", base_url)
    await page.goto(base_url, wait_until="domcontentloaded", timeout=30000)
    await _human_delay(2, 4)
    logger.info("WESTLAW_NAV after_goto url=%s", page.url)
    # Log page title to understand what page we landed on
    try:
        title = await page.title()
        logger.info("WESTLAW_NAV page_title=%s", title)
    except Exception:
        pass

    try:
        # Step 0: Handle intermediate redirect pages (OpenAthens, ExLibris Primo, etc.)
        intermediate_domains = ("openathens.net", "exlibrisgroup.com", "primo.exlibrisgroup")
        if any(d in page.url for d in intermediate_domains):
            domain_name = next((d for d in intermediate_domains if d in page.url), "unknown")
            logger.info("On intermediate page (%s), waiting for redirect to SSO...", domain_name)
            for _ in range(15):
                await asyncio.sleep(2)
                current = page.url
                # Stop once we leave all intermediate domains and reach SSO or Westlaw
                if not any(d in current for d in intermediate_domains):
                    break
            logger.info("WESTLAW_NAV after_intermediate url=%s", page.url)

        # Step 1: Handle institution SSO (with CAPTCHA)
        sso_domain = os.getenv("INSTITUTION_SSO_DOMAIN", "")
        if sso_domain and sso_domain not in page.url and "westlaw" not in page.url.lower():
            logger.info("Waiting for redirect chain to reach SSO or Westlaw...")
            for _ in range(10):
                await asyncio.sleep(2)
                if sso_domain in page.url or "westlaw" in page.url.lower():
                    break
            logger.info("WESTLAW_NAV redirect_settled url=%s", page.url)

        sso_ok = await _handle_institution_sso(page)
        if sso_ok:
            # SSO redirected us — wait for the full chain to settle
            # (OpenAthens → Thomson Reuters → WestLaw Classic)
            for _ in range(10):
                await asyncio.sleep(2)
                try:
                    await page.wait_for_load_state("domcontentloaded", timeout=5000)
                except Exception:
                    pass
                # Stop waiting once we hit westlaw.com or a Client ID page
                if "westlaw.com" in page.url or "next.westlaw" in page.url:
                    break
            await _human_delay(1, 2)

        # Step 2: Handle OnePass login (if redirected to signon.thomsonreuters.com)
        if "signon.thomsonreuters.com" in page.url:
            await _handle_onepass_login(page)

        # Step 3: Handle Client ID form (shown after SSO on WestLaw Classic)
        # Wait for the Client ID form or search box to appear in the DOM
        try:
            await page.wait_for_selector(
                "#co_clientIDTextbox, #searchInputId, #co_search_headerSearch",
                timeout=10000,
            )
            await _human_delay(0.5, 1.0)
        except Exception:
            logger.debug("Neither Client ID form nor search box found within timeout")

        if await _handle_client_id_login(page):
            await _human_delay(2, 3)
            try:
                await page.wait_for_load_state("domcontentloaded", timeout=15000)
            except Exception:
                pass

        # Verify we actually reached WestLaw
        current = page.url
        if "westlaw" in current.lower() or "next.westlaw" in current:
            _logged_in = True
            logger.info("WESTLAW_NAV session_ready url=%s", current)
            # Debug: capture page content to understand what page we're on
            try:
                title = await page.title()
                body_text = await page.evaluate("() => document.body?.innerText?.substring(0, 500) || ''")
                logger.info("WESTLAW_DEBUG page_title=%s body_preview=%s", title, body_text[:300])
            except Exception as dbg_e:
                logger.warning("WESTLAW_DEBUG could not capture page: %s", dbg_e)
        elif sso_domain and sso_domain in current:
            logger.error("WESTLAW_NAV login_failed url=%s", current)
        else:
            # Might be on some intermediate page but worth trying
            _logged_in = True
            logger.warning("WESTLAW_NAV login_uncertain url=%s", current)

    except Exception as e:
        logger.warning("Login flow error (may already be logged in): %s", e)
        # If we're somehow on WestLaw, mark as logged in
        if "westlaw" in page.url.lower():
            _logged_in = True


async def search(
    query: str,
    content_type: str | None = None,
    jurisdiction: str | None = None,
    limit: int = 20,
) -> dict[str, Any]:
    """Search WestLaw via Playwright.

    Args:
        query: Search query (supports Westlaw search syntax).
        content_type: Filter — 'cases', 'statutes', 'regulations', 'secondary'.
            Note: NOT currently used by the Playwright scraper (query-only search).
        jurisdiction: Jurisdiction filter (e.g., 'US-FED').
            Note: NOT currently used by the Playwright scraper (query-only search).
        limit: Max results to return.

    Returns:
        Dict with 'results' list and 'meta' info.
    """
    async with _lock:
        await _ensure_logged_in()
        page = _page
        assert page is not None

        return await _search_impl(page, query, limit)


async def _search_impl(page, query: str, limit: int) -> dict[str, Any]:
    """Internal search implementation (called under _lock)."""
    try:
        # Navigate to search page if not already there
        if "Search" not in page.url and "search" not in page.url:
            await page.goto(
                "https://1.next.westlaw.com/Search/Home.html",
                wait_until="domcontentloaded",
                timeout=15000,
            )
            await _human_delay(1, 2)

        # Wait for search box to appear (it may take a moment after Client ID form)
        try:
            await page.wait_for_selector(SEARCH_BOX_SELECTORS, timeout=10000)
        except Exception:
            # Search box not found — might still be on Client ID page, try handling
            logger.debug("Search box not found, checking for Client ID form...")
            if await _handle_client_id_login(page):
                await _human_delay(2, 3)
                try:
                    await page.wait_for_load_state("domcontentloaded", timeout=10000)
                    await page.wait_for_selector(SEARCH_BOX_SELECTORS, timeout=10000)
                except Exception:
                    pass

        # Find and fill search box
        search_box = page.locator(SEARCH_BOX_SELECTORS)
        if await search_box.count() == 0:
            # Debug: capture full page state to diagnose why search box is missing
            try:
                title = await page.title()
                body_text = await page.evaluate(
                    "() => document.body?.innerText?.substring(0, 800) || ''"
                )
                all_inputs = await page.evaluate(
                    "() => [...document.querySelectorAll('input,textarea')].map("
                    "el => ({tag: el.tagName, id: el.id, name: el.name, type: el.type})"
                    ").slice(0, 10)"
                )
                logger.warning(
                    "WESTLAW_SEARCH_FAIL url=%s title=%s inputs=%s body=%s",
                    page.url, title, all_inputs, body_text[:500],
                )
            except Exception as dbg_e:
                logger.warning(
                    "WESTLAW_SEARCH_FAIL url=%s debug_error=%s", page.url, dbg_e
                )
            return {"error": "Cannot find search input on Westlaw page", "results": []}

        await search_box.first.clear()
        await _human_delay(0.3, 0.6)
        await search_box.first.fill(query)
        await _human_delay(0.5, 1.0)

        # Submit search
        await page.keyboard.press("Enter")
        logger.info("Search submitted, waiting for results...")

        # Wait for network activity to settle (AJAX search results)
        try:
            await page.wait_for_load_state("networkidle", timeout=60000)
        except Exception:
            logger.debug("networkidle timeout — results may still be loading")

        # Additional explicit wait for result elements to appear
        result_appeared = False
        try:
            await page.wait_for_selector(RESULT_SELECTORS, timeout=30000)
            result_appeared = True
            await _human_delay(0.5, 1.0)
        except Exception:
            logger.debug("Result container selector timed out")

        # If results haven't appeared, try waiting for loading spinner to disappear
        if not result_appeared:
            try:
                await page.wait_for_function(
                    "() => !document.body.innerText.includes('Loading, please wait')",
                    timeout=30000,
                )
                await _human_delay(1, 2)
            except Exception:
                logger.debug("Loading text still present after timeout")

        # Let any in-flight results-page navigation finish before we read the DOM,
        # then extract via a navigation-resilient evaluate (retries if Westlaw
        # redirects mid-evaluate instead of failing over to CourtListener).
        await _settle_page(page)
        results = await _evaluate_with_retry(
            page,
            """(maxResults) => {
            const results = [];

            // Strategy 1: Find all document links (most reliable)
            // WestLaw Classic wraps each result with a link to /Document/
            const docLinks = document.querySelectorAll(
                'a[href*="/Document/"], a[href*="/Link/Document/"]'
            );

            const seenTitles = new Set();
            const seenDocIds = new Set();
            for (const link of docLinks) {
                if (results.length >= maxResults) break;

                const title = link.textContent.trim();
                // Skip non-title links (icons, "Show synopsis", etc.)
                if (!title || title.length < 5 || title.length > 300) continue;
                if (/^(Show|Hide|View|More|Less|\\d+$)/.test(title)) continue;
                // Skip snippet-like text (starts with "...")
                if (title.startsWith('...') && title.length < 200) continue;
                if (seenTitles.has(title)) continue;

                // Deduplicate by Document ID in the URL
                const href = link.href || '';
                const docIdMatch = href.match(/Document\\/([A-Za-z0-9]+)/);
                const docId = docIdMatch ? docIdMatch[1] : '';
                if (docId && seenDocIds.has(docId)) continue;
                if (docId) seenDocIds.add(docId);
                seenTitles.add(title);

                // Walk up to find the result container and extract metadata
                let container = link.parentElement;
                let citation = '';
                let snippet = '';

                // Look for citation/court info near the title
                for (let i = 0; i < 5 && container; i++) {
                    // Check siblings and children for metadata
                    const metaEls = container.querySelectorAll(
                        '[class*="cite"], [class*="court"], [class*="meta"], ' +
                        '[class*="Cite"], [class*="Court"]'
                    );
                    if (metaEls.length > 0) {
                        citation = [...metaEls].map(el => el.textContent.trim())
                            .filter(t => t.length > 3)
                            .join(' | ')
                            .substring(0, 200);
                    }

                    // Check for snippet/synopsis text
                    const snippetEls = container.querySelectorAll(
                        '[class*="snippet"], [class*="synopsis"], [class*="headnote"], ' +
                        '[class*="Snippet"], [class*="Synopsis"]'
                    );
                    if (snippetEls.length > 0) {
                        snippet = [...snippetEls].map(el => el.textContent.trim())
                            .filter(t => t.length > 10)
                            .join(' ')
                            .substring(0, 500);
                    }

                    // If we found metadata, stop walking up
                    if (citation || snippet) break;
                    container = container.parentElement;
                }

                // Fallback: extract text near the title link
                if (!citation && !snippet) {
                    const parent = link.closest('div, li, tr, section') || link.parentElement;
                    if (parent) {
                        const fullText = parent.textContent.trim();
                        // Remove the title from the full text to get metadata
                        const remaining = fullText.replace(title, '').trim();
                        if (remaining.length > 10) {
                            // Try to split into citation (court/date) and snippet
                            const parts = remaining.split(/\\n+/).filter(p => p.trim().length > 5);
                            if (parts.length > 0) citation = parts[0].trim().substring(0, 200);
                            if (parts.length > 1) snippet = parts.slice(1).join(' ').trim().substring(0, 500);
                        }
                    }
                }

                results.push({ title, citation, snippet, url: href });
            }

            // Strategy 2: If no Document links found, try extracting from page text
            if (results.length === 0) {
                // Look for any meaningful links with case-like titles
                const allLinks = document.querySelectorAll('a[href]');
                for (const link of allLinks) {
                    if (results.length >= maxResults) break;
                    const text = link.textContent.trim();
                    // Case titles typically contain "v." or "Inc." or similar patterns
                    if (text.length > 10 && text.length < 300 &&
                        (text.includes(' v. ') || text.includes(' v ') ||
                         text.includes('§') || text.includes('U.S.C.'))) {
                        if (!seenTitles.has(text)) {
                            seenTitles.add(text);
                            results.push({
                                title: text, citation: '', snippet: '',
                                url: link.href || '',
                            });
                        }
                    }
                }
            }

            return results;
        }""",
            limit,
        )

        logger.info("Extracted %d results from page", len(results))

        return {
            "query": query,
            "source": "westlaw_classic",
            "result_count": len(results),
            "results": results,
        }

    except Exception as e:
        logger.exception("Westlaw search failed: %s", e)
        return {"error": str(e), "results": []}


async def get_document(doc_url: str, include_full_text: bool = True) -> dict[str, Any]:
    """Retrieve a specific document from WestLaw.

    Args:
        doc_url: Full Westlaw document URL.
        include_full_text: Whether to extract full document text.

    Returns:
        Dict with document title, text, metadata.
    """
    async with _lock:
        await _ensure_logged_in()
        page = _page
        assert page is not None

        try:
            # 1. Navigate with networkidle (wait for AJAX content to load)
            await page.goto(doc_url, wait_until="networkidle", timeout=30000)
            await _human_delay(2, 3)

            # 2. Handle Client ID form (search() has this but old get_document didn't)
            await _handle_client_id_login(page)

            # 3. Wait for document content selector to appear
            try:
                await page.wait_for_selector(
                    DOC_CONTENT_SELECTORS, state="attached", timeout=15000
                )
                await _human_delay(1, 2)
            except Exception:
                logger.warning("WESTLAW_DOC content selector not found within 15s")

            # 4. Extract document title
            title_el = page.locator("h1, h2, [class*='documentTitle'], [class*='docTitle']")
            title = await title_el.first.text_content() if await title_el.count() > 0 else ""

            # 5. Extract metadata (court, date, citation)
            meta_parts = []
            meta_els = page.locator(
                "[class*='court'], [class*='date'], [class*='citation'], [class*='docket']"
            )
            for i in range(min(await meta_els.count(), 5)):
                text = await meta_els.nth(i).text_content()
                if text and text.strip():
                    meta_parts.append(text.strip())

            # 6. Extract full text — specific selectors first, fallback second
            full_text = ""
            if include_full_text:
                specific_el = page.locator(DOC_CONTENT_SELECTORS)
                if await specific_el.count() > 0:
                    full_text = (await specific_el.first.text_content() or "").strip()[:10000]

                # If specific selector got too little, try fallback selectors
                if len(full_text) < 100:
                    fallback_el = page.locator(DOC_CONTENT_FALLBACK_SELECTORS)
                    if await fallback_el.count() > 0:
                        fb = (await fallback_el.first.text_content() or "").strip()
                        if len(fb) > len(full_text):
                            full_text = fb[:10000]

            # 7. Empty content detection + debug logging
            if not full_text or len(full_text.strip()) < 100 or "Client ID" in full_text[:200]:
                page_title = ""
                try:
                    page_title = await page.title()
                except Exception:
                    pass
                logger.warning(
                    "WESTLAW_DOC_EMPTY url=%s page_title=%s text_len=%d preview=%s",
                    page.url[:100], page_title, len(full_text), full_text[:200],
                )
                return {
                    "title": title.strip() if title else "",
                    "metadata": " | ".join(meta_parts),
                    "url": doc_url,
                    "full_text": full_text,
                    "source": "westlaw_classic",
                    "_warning": "Document content may be incomplete.",
                }

            return {
                "title": title.strip() if title else "",
                "metadata": " | ".join(meta_parts),
                "url": doc_url,
                "full_text": full_text,
                "source": "westlaw_classic",
            }

        except Exception as e:
            logger.exception("Westlaw document retrieval failed: %s", e)
            return {"error": str(e), "title": "", "full_text": ""}


async def close():
    """Gracefully close the browser."""
    global _browser, _context, _page, _logged_in
    async with _lock:
        if _browser:
            await _browser.close()
        _browser = _context = _page = None
        _logged_in = False
