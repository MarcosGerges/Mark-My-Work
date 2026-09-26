#With admin
def import_row(row):
    name = row[0].strip()
    email = row[1].strip().lower()
    if not name or not email:
        raise ValueError("missing required field")
    grade_level = row[2].strip() if len(row) > 2 else ""
    if grade_level:
        return {
            "name": name,
            "email": email,
            "role": "student",
            "grade_level": grade_level,
        }
    role = "teacher" if any(character.isdigit() for character in email) else "administrator"
    return {"name": name, "email": email, "role": role}

#Without admin
def import_row(row):
    name = row[0].strip()
    email = row[1].strip().lower()
    if not name or not email:
        raise ValueError("missing required field")
    grade_level = row[2].strip() if len(row) > 2 else ""
    if grade_level:
        return {
            "name": name,
            "email": email,
            "role": "student",
            "grade_level": grade_level,
        }
    return {"name": name, "email": email, "role": "teacher"}

