def not_in_rts_group(user):
    if user:
        return user.groups.filter(name='Rts').count() > 0
    return False