import datetime
import sys

name = input("Full Name: ")
if not name.strip():
    print("Error: Name must not be empty.")
    sys.exit()

try:
    age = int(input("Age: "))
    if not (10 <= age <= 60):
        print("Error: Age must be between 10 and 60.")
        sys.exit()
except ValueError:
    print("Error: Please enter a valid number for age.")
    sys.exit()

city = input("City: ")

skill = input("Primary Skill: ")

skill_level = input("Skill Level (Beginner/Intermediate/Advanced): ").strip().capitalize()
if skill_level not in ["Beginner", "Intermediate", "Advanced"]:
    print("Error: Skill level must be exactly Beginner, Intermediate, or Advanced.")
    sys.exit()

if age < 18:
    career_stage = "Student"
elif 18 <= age <= 25:
    career_stage = "Early Professional"
else:
    career_stage = "Experienced Professional"

if skill_level == "Beginner":
    readiness = "Foundation Stage"
    recommendation = "Focus on core fundamentals and consistency"
elif skill_level == "Intermediate":
    readiness = "Intern / Junior Ready"
    recommendation = "Start building real-world projects"
else:
    readiness = "Production Ready"
    recommendation = "Contribute to production-grade systems"

print("\n" + "="*45)

print("="*45)
print(f"{'Name':<15} : {name.title()}")
print(f"{'Age':<15} : {age}")
print(f"{'City':<15} : {city.title()}")
print(f"{'Primary Skill':<15} : {skill}")
print(f"{'Skill Level':<15} : {skill_level}")
print("-" * 45)
print(f"{'Career Stage':<15} : {career_stage}")
print(f"{'Readiness Tag':<15} : {readiness}")
print(f"{'Recommendation':<15} : {recommendation}")
print("="*45)