import json
import sys
from utility import *

def main():
    try:
        with open("data.json", "r") as f:
            student_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        student_data = []

    choice = input(f"""
1. Add Student
2. View All Student Data - {len(student_data)} Student(s)
3. Analytics
4. Exit
Choose between the options : """)

    if choice.strip() == "1":
        add_student()
        main()
    elif choice.strip() == "2":
        view_students()
        main()
    elif choice.strip() == "3":
        rank_students()
        subject_toppers()
        most_common_skills()
        main()
    elif choice.strip() == "4":
        sys.exit()


if __name__ == "__main__":
    main()