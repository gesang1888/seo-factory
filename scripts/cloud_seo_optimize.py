#!/usr/bin/env python3
"""Run Cursor Cloud Agent to optimize SEO content in seo-factory.

Prerequisites:
  pip install cursor-sdk
  export CURSOR_API_KEY='cursor_...'   # https://cursor.com/dashboard/integrations
  export SEO_FACTORY_REPO_URL='https://github.com/YOU/seo-factory'  # or --repo

The repo must be pushed to GitHub (or GitLab/Azure DevOps connected to Cursor)
before cloud agents can clone it.

Examples:
  # Preview prompt only
  python3 scripts/cloud_seo_optimize.py --task p1 --brand lovegobuy --dry-run

  # Optimize Lovegobuy P1 pages and open a PR
  python3 scripts/cloud_seo_optimize.py --task p1 --brand lovegobuy --create-pr

  # Single slug on NL domain
  python3 scripts/cloud_seo_optimize.py --brand lovegobuy \\
    --slugs best-lovegobuy-spreadsheet --domain lovegobuyspreadsheet.nl --create-pr

  # Resume a cloud agent
  python3 scripts/cloud_seo_optimize.py --resume bc-abc123 --follow-up "Also update FAQ"
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]

BRANDS: dict[str, dict[str, str]] = {
    "lovegobuy": {
        "pages": "scripts/pages_lovegobuy.py",
        "deep": "scripts/deep_content_lovegobuy.py",
        "keywords": "scripts/keyword_articles_lovegobuy.py",
        "build": "python3 build_lovegobuy_site.py",
        "cluster": "sites/lovegobuy-cluster/cluster-config.json",
        "register": "https://www.lovegobuy.com/?invite_code=W5RJX3",
        "spreadsheet": "https://w2clinks.com/spreadsheet/",
    },
    "kakobuy": {
        "pages": "scripts/pages_kakobuy.py",
        "deep": "scripts/deep_content_kakobuy.py",
        "keywords": "scripts/keyword_articles_kakobuy.py",
        "build": "python3 build_kakobuy_site.py",
        "cluster": "sites/kakobuy-cluster/cluster-config.json",
        "register": "https://ikako.vip/r/yze69",
        "spreadsheet": "https://w2clinks.com/spreadsheet/",
    },
}


def _load_p1_urls(brand: str) -> list[str]:
    cfg_path = ROOT / BRANDS[brand]["cluster"]
    data = json.loads(cfg_path.read_text(encoding="utf-8"))
    return list(data.get("gsc_p1_urls") or [])


def _slug_from_url(url: str) -> str:
    path = url.rstrip("/").split("/", 3)
    if len(path) < 4 or not path[3]:
        return ""
    return path[3].strip("/").split("/")[0]


def build_prompt(
    *,
    brand: str,
    task: str,
    slugs: list[str] | None = None,
    domain: str | None = None,
    custom: str | None = None,
) -> str:
    if brand not in BRANDS:
        raise SystemExit(f"Unknown brand {brand!r}. Choose: {', '.join(BRANDS)}")

    meta = BRANDS[brand]
    pages = meta["pages"]
    deep = meta["deep"]
    keywords = meta["keywords"]
    build_cmd = meta["build"]
    cluster = meta["cluster"]

    scope = ""
    if task == "p1":
        urls = _load_p1_urls(brand)
        slug_list = sorted({_slug_from_url(u) for u in urls if _slug_from_url(u)})
        home_urls = [u for u in urls if _slug_from_url(u) == ""]
        scope = dedent(
            f"""
            Optimize P1 URLs from `{cluster}` → `gsc_p1_urls` ({len(urls)} URLs).

            Priority slugs (unique): {", ".join(slug_list) or "(home only)"}
            Home URLs: {", ".join(home_urls) or "none"}

            Work slug-by-slug. For each slug, improve the matching locale block in `{pages}`
            (and `{deep}` / `{keywords}` when relevant).
            """
        ).strip()
    elif task == "slugs":
        if not slugs:
            raise SystemExit("--slugs is required when --task slugs")
        dom = f" (domain hint: {domain})" if domain else ""
        scope = (
            f"Optimize these page slugs only: {', '.join(slugs)}{dom}. "
            f"Edit `{pages}` and related modules."
        )
    elif task == "custom":
        if not custom:
            raise SystemExit("--prompt is required when --task custom")
        scope = custom.strip()
    else:
        raise SystemExit(f"Unknown task {task!r}")

    return dedent(
        f"""
        You are an SEO content engineer working in the `seo-factory` repository.

        ## Goal
        {scope}

        ## Brand: {brand}
        - Register CTA: {meta["register"]}
        - Spreadsheet: {meta["spreadsheet"]}
        - Do not invent coupon amounts; match the live agent site policy.

        ## Files you may edit
        - `{pages}` — title, description, h1, intro, sections, FAQ per locale
        - `{deep}` — long-form SEO sections merged into pages
        - `{keywords}` — country/keyword guide HTML blocks
        - `sites/<domain>/keyword-plan.md` — only if keyword targeting needs a note

        ## Rules
        1. Minimize diff scope — only touch pages in scope.
        2. Keep existing URL slugs and hreflang structure unchanged.
        3. Natural keyword placement: title, meta description (~150–160 chars), H1, first paragraph, one H2.
        4. Add internal links between related slugs (spreadsheet, shipping, coupon, legit, how-to).
        5. External links: register URL and W2CLinks spreadsheet with target="_blank" rel="noopener".
        6. Do not edit `dist/` — it is generated output.
        7. After edits, run: `{build_cmd}` and fix any build errors.
        8. Summarize changes as a bullet list: slug → fields updated (title/description/h1/sections/faq).

        ## Do not
        - Commit secrets or deploy passwords
        - Force-push main
        - Change nginx/deploy scripts unless explicitly asked
        """
    ).strip()


def _repo_url(explicit: str | None) -> str:
    url = (explicit or os.environ.get("SEO_FACTORY_REPO_URL") or "").strip()
    if not url:
        raise SystemExit(
            "Missing repo URL. Pass --repo or set SEO_FACTORY_REPO_URL "
            "(e.g. https://github.com/you/seo-factory)."
        )
    return url


def run_cloud(
    *,
    prompt: str,
    repo_url: str,
    ref: str,
    create_pr: bool,
    model: str,
    api_key: str,
    stream: bool,
) -> int:
    try:
        from cursor_sdk import Agent, AgentOptions, CloudAgentOptions, CloudRepository, CursorAgentError
    except ImportError:
        print("Install the SDK: pip install cursor-sdk", file=sys.stderr)
        return 1

    print(f"Cloud repo: {repo_url} @ {ref}")
    print(f"Create PR: {create_pr}")
    print("--- prompt preview (first 800 chars) ---")
    print(prompt[:800] + ("..." if len(prompt) > 800 else ""))
    print("---")

    try:
        with Agent.create(
            model=model,
            api_key=api_key,
            cloud=CloudAgentOptions(
                repos=[CloudRepository(url=repo_url, starting_ref=ref)],
                auto_create_pr=create_pr,
                skip_reviewer_request=True,
            ),
        ) as agent:
            print(f"Agent id: {agent.agent_id}")
            run = agent.send(prompt)
            print(f"Run id: {run.id}")

            if stream:
                for message in run.messages():
                    if message.type == "assistant":
                        for block in message.message.content:
                            if block.type == "text" and block.text:
                                sys.stdout.write(block.text)
                                sys.stdout.flush()
            result = run.wait()
    except CursorAgentError as err:
        print(f"Startup failed: {err.message} (retryable={err.is_retryable})", file=sys.stderr)
        return 1

    if result.status == "error":
        print(f"Run failed: {result.id}", file=sys.stderr)
        return 2

    print(f"\nFinished: status={result.status} agent={agent.agent_id} run={result.id}")
    if create_pr:
        print("Check GitHub for the auto-created PR.")
    return 0


def run_resume(
    *,
    agent_id: str,
    follow_up: str,
    api_key: str,
    stream: bool,
) -> int:
    try:
        from cursor_sdk import Agent, AgentOptions, CursorAgentError
    except ImportError:
        print("Install the SDK: pip install cursor-sdk", file=sys.stderr)
        return 1

    try:
        with Agent.resume(agent_id, AgentOptions(api_key=api_key)) as agent:
            run = agent.send(follow_up)
            print(f"Run id: {run.id}")
            if stream:
                for message in run.messages():
                    if message.type == "assistant":
                        for block in message.message.content:
                            if block.type == "text" and block.text:
                                sys.stdout.write(block.text)
                                sys.stdout.flush()
            result = run.wait()
    except CursorAgentError as err:
        print(f"Resume failed: {err.message}", file=sys.stderr)
        return 1

    if result.status == "error":
        print(f"Run failed: {result.id}", file=sys.stderr)
        return 2
    print(f"Finished: status={result.status}")
    return 0


def list_repos(api_key: str) -> int:
    try:
        from cursor_sdk import Cursor
    except ImportError:
        print("Install the SDK: pip install cursor-sdk", file=sys.stderr)
        return 1

    repos = Cursor.repositories.list(api_key=api_key)
    if not repos:
        print("No repositories connected. Link GitHub in Cursor Settings → Integrations.")
        return 0
    for item in repos:
        url = getattr(item, "url", None) or item.get("url") if isinstance(item, dict) else str(item)
        print(url)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Cursor Cloud SEO content optimizer for seo-factory")
    parser.add_argument("--brand", choices=sorted(BRANDS), default="lovegobuy")
    parser.add_argument(
        "--task",
        choices=("p1", "slugs", "custom"),
        default="p1",
        help="p1 = cluster-config gsc_p1_urls; slugs = explicit list; custom = --prompt",
    )
    parser.add_argument("--slugs", help="Comma-separated slugs (with --task slugs)")
    parser.add_argument("--domain", help="Optional domain hint for locale (e.g. lovegobuyspreadsheet.nl)")
    parser.add_argument("--prompt", help="Custom instructions (with --task custom)")
    parser.add_argument("--repo", help="Git repo URL (default: SEO_FACTORY_REPO_URL)")
    parser.add_argument("--ref", default="main", help="Starting git ref for cloud clone")
    parser.add_argument("--create-pr", action="store_true", help="Open PR when cloud run completes")
    parser.add_argument("--model", default="composer-2.5")
    parser.add_argument("--dry-run", action="store_true", help="Print prompt and exit")
    parser.add_argument("--no-stream", action="store_true", help="Do not stream assistant text")
    parser.add_argument("--list-repos", action="store_true", help="List Cursor-connected repos and exit")
    parser.add_argument("--resume", metavar="AGENT_ID", help="Resume cloud agent (bc-...)")
    parser.add_argument("--follow-up", help="Message when using --resume")
    args = parser.parse_args()

    api_key = os.environ.get("CURSOR_API_KEY", "").strip()
    if not api_key and not args.dry_run:
        print("Set CURSOR_API_KEY (https://cursor.com/dashboard/integrations)", file=sys.stderr)
        return 1

    if args.list_repos:
        return list_repos(api_key)

    if args.resume:
        if not args.follow_up:
            print("--follow-up is required with --resume", file=sys.stderr)
            return 1
        return run_resume(
            agent_id=args.resume,
            follow_up=args.follow_up,
            api_key=api_key,
            stream=not args.no_stream,
        )

    slugs = [s.strip() for s in (args.slugs or "").split(",") if s.strip()] or None
    prompt = build_prompt(
        brand=args.brand,
        task=args.task,
        slugs=slugs,
        domain=args.domain,
        custom=args.prompt,
    )

    if args.dry_run:
        print(prompt)
        return 0

    return run_cloud(
        prompt=prompt,
        repo_url=_repo_url(args.repo),
        ref=args.ref,
        create_pr=args.create_pr,
        model=args.model,
        api_key=api_key,
        stream=not args.no_stream,
    )


if __name__ == "__main__":
    raise SystemExit(main())
