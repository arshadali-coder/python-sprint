# Student Marks Calculator

student_name = input("Enter student name: ")
num_subjects = int(input("Enter number of subjects: "))

total_marks = 0

for i in range(1, num_subjects + 1):
    marks = float(input(f"Enter marks for subject {i}: "))
    total_marks += marks

average_marks = total_marks / num_subjects

print("\n📄 Student Result Summary")
print("-------------------------")
print(f"Name           : {student_name}")
print(f"Total Marks    : {total_marks}")
print(f"Average Marks  : {average_marks:.2f}")