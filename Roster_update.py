roster = [
    {"name": "Amara Singh", "grade": 91, "attendance": 0.95},
    {"name": "Liam Chen", "grade": 68, "attendance": 0.72},
    {"name": "Priya Nair", "grade": 84, "attendance": 0.88},
]

def average_grade(roster):
    if not roster:
        return None
    return sum(s["grade"] for s in roster) / len(roster)


def classify_students(roster):
    need_help = []
    on_track = []

    if not roster:
        print("No students in roster.")
        return need_help, on_track, None, None

    for student in roster:
        if student["grade"] < 70 or student["attendance"] < 0.8:
            need_help.append(student)
        else:
            on_track.append(student)

    print("Students who need help:")
    for student in need_help:
        print(f"- {student['name']} (grade: {student['grade']}, attendance: {student['attendance']:.0%})")
    need_help_average = average_grade(need_help)
    if need_help_average is None:
        print("Average grade: N/A")
    else:
        print(f"Average grade: {need_help_average:.1f}")

    print("Students on track:")
    for student in on_track:
        print(f"- {student['name']} (grade: {student['grade']}, attendance: {student['attendance']:.0%})")
    on_track_average = average_grade(on_track)
    if on_track_average is None:
        print("Average grade: N/A")
    else:
        print(f"Average grade: {on_track_average:.1f}")

    return need_help, on_track, need_help_average, on_track_average


need_help, on_track, need_help_average, on_track_average = classify_students(roster)


""" Output:
Students who need help:
- Liam Chen (grade: 68, attendance: 72%)
Average grade: 68.0
Students on track:
- Amara Singh (grade: 91, attendance: 95%)
- Priya Nair (grade: 84, attendance: 88%)
Average grade: 87.5
"""