from app.services import stats

def test_stats():
    result = stats([
        {"label":"positive"},
        {"label":"negative"},
        {"label":"positive"},
        {"label":None}
    ])
    assert result["annotated_items"] == 3
    assert result["progress_percentage"] == 75.0
    assert result["label_distribution"]["positive"] == 2
