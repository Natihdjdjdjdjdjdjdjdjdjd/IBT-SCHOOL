# let us create our student list in our school
students=[
    {"id": 10, "name": "Natoli"},
    {"id": 11, "name": "Natan"},
    {"id": 12, "name": "Bona"}
]
# let define our function to find student by id and name
def find_by_id(students,student_id):
    left = 0
    right = len(students) - 1

    while left <= right:
        mid = (left + right) // 2
        if students[mid]["id"] == student_id:
            return students[mid]
        elif students[mid]["id"] < student_id:
            left = mid + 1
        else:
            right = mid - 1

    return None
# letr define our function to find student by name only
def find_by_name(students, student_name):
    for student in students:
        if student["name"] == student_name:
            return student
    return None

print(find_by_id(students, 11))  
print(find_by_name(students, "Natoli")) 