#
#
def filter_cond(line_dict):
    """Filter function
    Takes a dict with field names as argument
    Returns True if conditions are satisfied
    """
    cond_match = (
       int(line_dict["num_reviews"]) > 20
    ) 
    return True if cond_match else False

