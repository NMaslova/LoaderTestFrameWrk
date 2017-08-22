from objects.enums import KeyWords


# checks if data retrieve is required
def database_check_required(prop_d):
    if KeyWords.dbCheck.value in prop_d:
        return True
    return False
