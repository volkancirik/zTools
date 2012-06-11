def not_in_dms_group(user):
    if user:
        return user.groups.filter(name='Dms').count() > 0
    return False