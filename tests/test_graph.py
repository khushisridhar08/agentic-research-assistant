from types import SimpleNamespace

from graph import route_after_review, MAX_REVISIONS


def test_approved_analysis_goes_to_brief():
    state = {
        "review": SimpleNamespace(approved=True),
        "revision_count": 0,
    }

    result = route_after_review(state)

    assert result == "brief"


def test_rejected_analysis_goes_to_revision():
    state = {
        "review": SimpleNamespace(approved=False),
        "revision_count": 0,
    }

    result = route_after_review(state)

    assert result == "revise"


def test_rejected_analysis_stops_at_revision_limit():
    state = {
        "review": SimpleNamespace(approved=False),
        "revision_count": MAX_REVISIONS,
    }

    result = route_after_review(state)

    assert result == "brief"


def test_approved_analysis_skips_further_revisions():
    state = {
        "review": SimpleNamespace(approved=True),
        "revision_count": 1,
    }

    result = route_after_review(state)

    assert result == "brief"