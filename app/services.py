def stats(items):

    total_items = len(items)

    annotated_items = 0

    label_distribution = {}


    for item in items:

        label = item.get("label")


        if label is not None:

            annotated_items += 1


            if label not in label_distribution:

                label_distribution[label] = 0


            label_distribution[label] += 1



    progress_percentage = 0.0


    if total_items > 0:

        progress_percentage = round(
            (annotated_items / total_items) * 100,
            2
        )


    return {

        "total_items": total_items,

        "annotated_items": annotated_items,

        "progress_percentage": progress_percentage,

        "label_distribution": label_distribution
    }