
def compare_names(claimant_name, lost_item_owners):
    """
    Compare claimant's name with owners' names of lost items.
    Return a list of matching lost item IDs.
    """
    matching_items = []
    for item_id, owner_name in lost_item_owners.items():
        # Check if claimant_name and owner_name are not None
        if claimant_name and owner_name:
            # Compare claimant's name with owner's name
            if claimant_name.lower() == owner_name.lower():
                matching_items.append(item_id)
    return matching_items