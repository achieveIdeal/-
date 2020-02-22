
def distinct_field(queryset, field):
    parents_id_not_null = []

    for comment in queryset:

        parents_id_not_null.append(eval('comment.'+str(field)))

    currents = list(set(parents_id_not_null))

    commentsEnd = []
    for comment in queryset:
        if eval('comment.'+str(field)) in currents and comment.id not in parents_id_not_null:
            commentsEnd.append(comment)
            currents.remove(comment.parents_id)
        if eval('comment.'+str(field)) is None and comment.id not in parents_id_not_null and comment not in commentsEnd:
            commentsEnd.append(comment)
    return commentsEnd