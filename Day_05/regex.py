import re

pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

email = "shivam@example.com"
print(bool(re.match(pattern, email)))

# Phone Number (Indian):-
pattern = r"^[6-9]\d{9}$"

# Using re.compile():--
email_pattern = re.compile(r"...email regex...")
if email_pattern.match(email):
    pass


# For Groups:--
text = "Name: Shivam, Age: 22"

pattern = r"Name:\s(\w+),\sAge:\s(\d+)"
match = re.search(pattern, text)

print(match.group(1))  # Shivam
print(match.group(2))  # 22

# Replacing Text (re.sub()):---

text = "My number is 9876543210"
pattern = r"\d{10}"

masked = re.sub(pattern, "**********", text)
print(masked)

