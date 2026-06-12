import numpy as np

A = np.arange(20)
B = np.array([i for i in A if i %2 ==0])
C = np.array([i*i for i in A])
names = [" Alice ", " Bob ", " Charlie "]

clean_names = [name.strip() for name in names]
events = [
    {"id": 1, "name": "Python Meetup"},
    {"id": 2, "name": "AI Summit"},
]
for i in events:
    print(i["name"], i["id"])

names = [event["name"] for event in events]

print(A)
print(B)
print(C)
print(clean_names)
print(names)