def stats(items):
    annotated = [item for item in items if item.get("label")]
    distribution = {}
    for item in annotated:
        label = item["label"]
        distribution[label] = distribution.get(label, 0) + 1
    total = len(items)
    return {
        "total_items": total,
        "annotated_items": len(annotated),
        "progress_percentage": round(len(annotated) / total * 100, 2) if total else 0.0,
        "label_distribution": distribution
    }
