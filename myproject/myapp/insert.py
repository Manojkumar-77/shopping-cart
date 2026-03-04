from myapp.models import Student

# Create a new student
Student.objects.create(name="Alice", age=20)

print("Student added successfully!")