# lost_items_backend/utils.py

def compare_names(claimant_name, lost_item_owners):
    """
    Compare claimant's name with names of lost item owners.
    Return a list of matching lost item IDs.
    """
    matching_items = []
    for item_id, item_owner in lost_item_owners.items():
        # Check if claimant_name and item_owner are not None
        if claimant_name and item_owner:
            # Implement your comparison logic here
            # For simplicity, let's assume a basic string matching approach
            if claimant_name.lower() == item_owner.lower():
                matching_items.append(item_id)
    return matching_items
