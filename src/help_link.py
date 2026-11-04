"""
Where Help goes. Home > Help (Help menu) opens the BarBell Operator Guide in
the person's web browser.

The address lives in ONE place, HELP_URL below - change it here (or per
machine with Settings.help_url in settings.json) and nothing else needs to
know. Keeping it out of the window code, and out of any installer script, means
a packaged install can point at a different guide, or a local copy, without a
rebuild.

Only http/https addresses are ever opened: the override is a setting on disk,
and Help must never be a way to launch a file or another program.
"""

HELP_URL = "https://claude.ai/artifact/H5yXBB29Aq899C8i6eVfBu"


def resolve_help_url(override: str = "") -> str:
    """The address Help should open: the settings override if it is a usable
    http(s) address, otherwise the built-in HELP_URL."""
    candidate = (override or "").strip()
    if candidate.lower().startswith(("https://", "http://")) and " " not in candidate:
        return candidate
    return HELP_URL
