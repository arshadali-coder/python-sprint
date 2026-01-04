import json
def get_valid_marks(subject):
    while True:
        try:
            marks = int(input(f"How much marks did you receive in {subject}: "))
            if 0 <= marks <= 100:
                return marks
            else:
                print("Marks must be between 0 and 100.")
        except ValueError:
            print("Marks must be a number.")

def add_student():
    name = input("Enter the student's name: ")
    roll_no = int(input("Enter the student's roll number: "))
    branch = input("Enter the student's branch: ")

    try:
        with open("data.json", "r") as f:
            student_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        student_data = []

    # Roll number uniqueness check
    for student in student_data:
        if student["Roll Number"] == roll_no:
            print("Roll number already exists. Student not added.")
            return

    subjects = []
    fav_subject1 = input("Favourite Subject 1: ")
    fav_subject2 = input("Favourite Subject 2: ")
    fav_subject3 = input("Favourite Subject 3: ")

    subjects.extend([fav_subject1, fav_subject2, fav_subject3])

    marks = {}
    marks[fav_subject1] = get_valid_marks(fav_subject1)
    marks[fav_subject2] = get_valid_marks(fav_subject2)
    marks[fav_subject3] = get_valid_marks(fav_subject3)

    skills = input("Enter your technical skills in comma-separated format: ")
    skills_list = list(set(skill.strip() for skill in skills.split(",")))

    student_profile = {
        "Name": name,
        "Roll Number": roll_no,
        "Branch": branch,
        "Subjects": subjects,
        "Marks": marks,
        "Technical Skills": skills_list
    }

    student_data.append(student_profile)

    with open("data.json", "w") as f:
        json.dump(student_data, f, indent=4)

    print("Student profile has been saved to data.json")

def view_students():
    try:
        with open("data.json", "r") as f:
            student_data = json.load(f)

        for student in student_data:
            print(f"\nName: {student['Name']}")
            print(f"Roll No.: {student['Roll Number']}")
            print(f"Branch: {student['Branch']}")

            for i, subject in enumerate(student["Subjects"], start=1):
                print(f"Favourite Subject {i}: {subject}, Marks: {student['Marks'][subject]}")

            print(f"Technical Skills: {', '.join(student['Technical Skills'])}")

            highest_subject = max(student["Marks"], key=student["Marks"].get)
            print(f"Highest Marks Subject: {highest_subject}")

            total_marks = sum(student["Marks"].values())
            average_marks = total_marks / len(student["Marks"])

            print(f"Total Marks: {total_marks}")
            print(f"Average Marks: {average_marks}")

    except (FileNotFoundError, json.JSONDecodeError):
        print("No student data found.")

def rank_students():
    try:
        with open("data.json", "r") as f:
            students = json.load(f)

        ranked = sorted(
            students,
            key=lambda s: sum(s["Marks"].values()),
            reverse=True
        )

        print("\n--- Student Rankings ---")
        for i, student in enumerate(ranked, start=1):
            total = sum(student["Marks"].values())
            print(f"{i}. {student['Name']} (Roll {student['Roll Number']}) - Total: {total}")

    except (FileNotFoundError, json.JSONDecodeError):
        print("No data available.")


def subject_toppers():
    try:
        with open("data.json", "r") as f:
            students = json.load(f)

        subject_best = {}

        for student in students:
            for subject, marks in student["Marks"].items():
                if subject not in subject_best or marks > subject_best[subject][1]:
                    subject_best[subject] = (student["Name"], marks)

        print("\n--- Subject-wise Toppers ---")
        for subject, (name, marks) in subject_best.items():
            print(f"{subject}: {name} ({marks})")

    except (FileNotFoundError, json.JSONDecodeError):
        print("No data available.")


def most_common_skills():
    try:
        with open("data.json", "r") as f:
            students = json.load(f)

        skill_count = {}

        for student in students:
            for skill in student["Technical Skills"]:
                skill_count[skill] = skill_count.get(skill, 0) + 1

        print("\n--- Most Common Technical Skills ---")
        for skill, count in sorted(skill_count.items(), key=lambda x: x[1], reverse=True):
            print(f"{skill}: {count} student(s)")

    except (FileNotFoundError, json.JSONDecodeError):
        print("No data available.")