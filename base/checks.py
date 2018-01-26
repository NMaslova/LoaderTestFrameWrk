from globals import *


# checks if data retrieve is required
def database_check_required(prop_d):
    if DB_CHECK in prop_d:
        return True
    return False
