class Student:
    def __init__(self, name, marks):
        self.name = name
        self._marks = marks  # private convention (_marks)

    @property
    def marks(self):
        print("Getting marks...")
        return self._marks

    @marks.setter
    def marks(self, value):
        print("Setting marks...")
        if 0 <= value <= 100:
            self._marks = value
        else:
            print("Invalid marks!")

    @marks.deleter
    def marks(self):
        print("Deleting marks...")
        del self._marks
    

s = Student("Alice", 90)

print(s.marks)     # calls getter
s.marks = 95       # calls setter
del s.marks        # calls deleter
