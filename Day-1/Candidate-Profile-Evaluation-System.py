import sys

# Taking The Inputs From User To Evaluate
name = input("Enter Your Full Name : ")
if name.strip() == "":
    print("Invalid Input: Name cannot be empty.")
    sys.exit()
age = int(input("Enter Your Age in Years : "))
if age <= 0 or age > 60:
    print("Invalid Input: Age must be between 1 and 60.")
    sys.exit()
city = input("Enter the city you currently live in : ")
if city.strip() == "":
    print("Invalid Input: City cannot be empty.")
    sys.exit()
skill = input("What is your Primary Skill That You are proud Of : ")
if skill.strip() == "":
    print("Invalid Input: Skill cannot be empty.")
    sys.exit()
skill_level = input("What is the level of your Skill (Beginner/Intermediate/Advanced) : ")
if skill_level.lower() not in ["beginner", "intermediate", "advanced"]:
    print("Invalid Input: Skill level must be Beginner, Intermediate, or Advanced.")
    sys.exit()
# Evaluation Logic

#The Career Stage Logic
if(age<19):
    career = "Student"
elif(age<25):
    career = "Early Professional"
else:
    career= "Experienced Professional"

#The Readiness Tag Logic
if(skill_level.lower() == "beginner"):
    tag = "Foundation Stage"
    recommendation = " Focus on core fundamentals and consistency"
elif(skill_level.lower() == "intermediate"):
    tag = "Intern / Junior Ready"
    recommendation = "Start building real-world projects"
elif(skill_level.lower() == "advanced"):
    tag = "Production Ready"
    recommendation = "Contribute to production-grade systems"
# Final Profile Card
print(f"""
    =======================================
            CANDIDATE PROFILE CARD
    =======================================
    Name        : {name.title()}
    Age         : {age}
    City        : {city.title()}
    Primary Skill   : {skill.title()}
    Skill Level     : {skill_level.title()}

    Career Stage    : {career}
    Readiness Tag   : {tag}
    Recommendation  : {recommendation}
    =======================================
""")