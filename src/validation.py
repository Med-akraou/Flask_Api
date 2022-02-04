# valider le nom du task.
def validate_name(name: str) -> bool:
    return (name.replace(' ','').isalnum()  and len(name) >= 6)

# valider la description.
def validate_description(description: str) -> bool:
    return (len(description) > 0 and len(description) <= 200 and
     description.replace(' ','').isalnum() or description.isalpha())

# Valider completed
def validate_is_completed(completed: bool) -> bool:
    return completed!=None
