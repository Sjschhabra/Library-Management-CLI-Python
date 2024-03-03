import os
import json
from tabulate import tabulate  
import sys
import shutil

def center_text(text):
    # Get the width of the terminal window
    terminal_width = shutil.get_terminal_size().columns
    # Calculate the amount of space to add before the text
    padding = (terminal_width - len(text)) // 2
    # Print the text with the calculated padding
    print(" " * padding + text)


# Example usage
project_directory = os.path.dirname(os.path.abspath(__file__))  # Determine the project directory # Assumes this script is in the project directory

#Our library class
class Library:
    def __init__(self, library_name):
        library_name = library_name.title()
        self.library_name = library_name
        self.library_file = os.path.join(project_directory, f"{library_name}.json")  # JSON file for this library
        self.load_from_file()  # Load existing data from the library file

    def load_from_file(self):
        try:
            with open(self.library_file, 'r') as file:
                self.books = json.load(file)  #this assigns the variable called books the data from the file of that library
        except FileNotFoundError:     #this is useless, but present
            self.books = {}
            print(f"Library file for {self.library_name} not found. Creating a new library.")

    def save_to_file(self):
        sorted_books = dict(sorted(self.books.items(), key=lambda x: x[0]))
        with open(self.library_file, 'w') as file:       #self.library_file = os.path.join(project_directory, f"{library_name}.json")
            json.dump(sorted_books, file)  #just updating the existing json file with updated and resorted file


    def _books(self):
        if self.books:
            # Sort the books alphabetically by title
            sorted_books = sorted(self.books.items(), key=lambda x: x[0])
            table = []
            for idx, (book, quantity) in enumerate(sorted_books, start=1):
                formatted_book = formatted_quantity = ""
                if idx == 1:  # The first row
                    formatted_book = "\033[1;93m" + book + "\033[0m"
                    formatted_quantity = "\033[1;93m" + str(quantity) + "\033[0m"
                else:
                    formatted_book = "\033[1;93m" + book + "\033[0m"
                    formatted_quantity = "\033[1;93m" + str(quantity) + "\033[0m"
                table.append([idx, formatted_book, formatted_quantity])
            print(f"\n\033[1;31m>Books in the {self.library_name} library:\033[0m")
            table_str = tabulate(table, headers=["\033[0m#", "\033[1mBook Name\033[0m", "\033[1mQuantity\033[0m"], tablefmt="pretty")
            print(table_str)

            total_books = sum(self.books.values())
            print(f"Total number of books in the {self.library_name} library: {total_books}")
        else:
            print(f"\n0 books in the {self.library_name} library.")


    def add_book_from_user_input(self):
        while True:
            book_name = input(f"\033[1mEnter the name of the book to add to {self.library_name} library (or b: back, m: modify book): \033[0m")
            if book_name == 'b':
                return  # Go back to library selection
            elif book_name == 'm':
                self.edit_book()
            else:
                book_name = book_name.title()               
                if book_name in self.books:
                    ans=input("Book already exists, want to add/subs some peices? (y: yes, e: exit) 😍\n")
                    if ans=='y':
                        try:
                            quantity = int(input("\033[1mEnter quantity to add/subs: \033[0m"))
                            self.books[book_name] += quantity
                        except ValueError:
                            print("Invalid input. Please enter a valid serial number.")
                    else:
                        break
                    self.save_to_file()    
                else:
                    quantity = int(input("\033[1mEnter its quantity: \033[0m"))
                    if quantity<=0:
                        print("You must input some quantity!")
                        break
                    self.books[book_name] = quantity
                    print("It's a new book, and now added 😍\n")
                    self.save_to_file()   
            self._books()  # Print the updated books table
            self.load_from_file()  #this will again read the new file so that after modifications or adding a new file, updated serial numbered file is in use.
            
    def edit_book(self):
        
        book_to_edit = input("\n\033[1m>>Enter the serial number of the book you want to modify: \033[0m")
        try:
            book_to_edit = int(book_to_edit)
            if 1 <= book_to_edit <= len(self.books):
                book_to_edit = list(self.books.keys())[book_to_edit - 1]
                print(f"Book: {book_to_edit}")
                print(f"Current Quantity: {self.books[book_to_edit]}")
                edit_choice = input("\033[1m>>>What do you want to do (n:name change, q:quantity change, u:add/subs quantity, r:remove book)? \033[0m").lower()
                if edit_choice == 'n':
                    new_name = input("\033[1mEnter the new name: \033[0m")
                    new_name = new_name.title()
                    self.books[new_name] = self.books.pop(book_to_edit)
                elif edit_choice == 'q':
                    new_quantity = int(input("\033[1mEnter the new quantity (0: delete the book): \033[0m"))
                    if new_quantity==0:
                        del self.books[book_to_edit]
                        print("Book deleted")
                    elif new_quantity<0:
                        print("Invalid choice")
                        return
                    else:
                        self.books[book_to_edit] = new_quantity
                elif edit_choice == 'r':
                    del self.books[book_to_edit]
                elif edit_choice=='u':
                    quantity = int(input("\033[1mEnter quantity to add/subs : \033[0m"))
                    self.books[book_to_edit] += quantity
                else:
                    print("Invalid choice.")
                self.save_to_file()                
            else:
                print("Invalid serial number. Please enter a valid number.")      
        except ValueError:
            print("Invalid input. Please enter a valid serial number.")
        
        


# Function to create a new library instance
def create_library():
    library_name = input("Enter a name for the new library: ")
    new_library = Library(library_name)
    with open(new_library.library_file, 'w') as file:
        json.dump(new_library.books, file)

# Function to create a new library instance or select an existing one
def create_or_select_library():
    while True:
        print("\n\033[1;31mAvailable Libraries:\033[0m")
        library_files = [f for f in os.listdir(project_directory) if f.endswith('.json')]
        library_names = [os.path.splitext(library_file)[0] for library_file in library_files]
        library_names.sort()  # Sort library names alphabetically
        available_libraries = [{"#": idx, "\033[1mLibraries Available\033[0m": "\033[1;93m" + name + "\033[0m"} for idx, name in enumerate(library_names, start=1)]
        table_str = tabulate(available_libraries, headers="keys", tablefmt="pretty")
        print(table_str)
        choice = input("Enter a serial no. to open that library (or n:new library creation, e:exit the program) : ")
        if choice.lower() == 'n':
            create_library()
        elif choice.lower()=="e":
                print("\033[1;95m")
                center_text("--Program Exited Safely--\033[0m\n\n\n\n")
                sys.exit(0)
        else:
            try:
                choice = int(choice)
                if 1 <= choice <= len(library_names):
                    library_name = library_names[choice - 1]
                    return Library(library_name)
                else:
                    print("Invalid library number. Please select an existing library or create a new one.")
            except ValueError:
                print("Invalid input. Please enter a valid number or 'new'.")


# Main program
while True:
    current_library = create_or_select_library()
    
    current_library.load_from_file()  # Load existing data
    current_library._books()
    current_library.add_book_from_user_input()
    current_library.save_to_file()
    
