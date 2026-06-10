from dataclasses import dataclass
@dataclass
class Books:
    name:str
    price:float
    author:str

book = Books("The hounds of baskervills", 225, "Arthur Conan Doyle")
print(book)