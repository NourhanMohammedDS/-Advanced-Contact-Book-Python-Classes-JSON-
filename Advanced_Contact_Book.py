import json
import os

# Define the Contact class
class Contact:
    def __init__(self, name, phone, email, address=""):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address

    def to_dict(self):
        """Convert contact object to dictionary for JSON storage."""
        return {
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "address": self.address
        }

    @staticmethod
    def from_dict(data):
        """Create a Contact object from dictionary (e.g., loaded from JSON)."""
        return Contact(data["name"], data["phone"], data["email"], data.get("address", ""))


# Define the ContactBook class to manage contacts
class ContactBook:
    def __init__(self):
        self.contacts = []
        self.file_name = "contacts.json"
        self.load_contacts()  # Load from file at start

    def add_contact(self, contact):
        # Prevent duplicate names
        if any(c.name.lower() == contact.name.lower() for c in self.contacts):
            print("A contact with that name already exists.")
            return
        self.contacts.append(contact)
        print("Contact added successfully.")

    def view_contacts(self):
        if not self.contacts:
            print("No contacts to show.")
            return

        # Sort contacts by name before displaying
        sorted_contacts = sorted(self.contacts, key=lambda c: c.name.lower())
        for c in sorted_contacts:
            print(f"Name: {c.name}, Phone: {c.phone}, Email: {c.email}, Address: {c.address}")

    def search_contact(self, keyword):
        results = [
            c for c in self.contacts
            if keyword.lower() in c.name.lower() or keyword in c.phone
        ]
        if results:
            for c in results:
                print(f"Name: {c.name}, Phone: {c.phone}, Email: {c.email}, Address: {c.address}")
        else:
            print("No contact found with that keyword.")

    def delete_contact(self, name):
        for i, c in enumerate(self.contacts):
            if c.name.lower() == name.lower():
                del self.contacts[i]
                print("Contact deleted.")
                return
        print("Contact not found.")

    def update_contact(self, name):
        for c in self.contacts:
            if c.name.lower() == name.lower():
                print("Leave input blank to keep current value.")
                new_phone = input("New phone: ") or c.phone
                new_email = input("New email: ") or c.email
                new_address = input("New address: ") or c.address

                c.phone = new_phone
                c.email = new_email
                c.address = new_address
                print("Contact updated.")
                return
        print("Contact not found.")

    def save_contacts(self):
        # Save all contacts to a JSON file
        with open(self.file_name, "w") as f:
            json.dump([c.to_dict() for c in self.contacts], f, indent=4)
        print("Contacts saved to file.")

    def load_contacts(self):
        # Load contacts from JSON file if exists
        if os.path.exists(self.file_name):
            with open(self.file_name, "r") as f:
                try:
                    data = json.load(f)
                    self.contacts = [Contact.from_dict(c) for c in data]
                except json.JSONDecodeError:
                    print("Warning: Could not load contacts (file may be corrupted).")
        else:
            self.contacts = []


# Main function to run the app
def main():
    book = ContactBook()

    while True:
        print("\n===== Contact Book Menu =====")
        print("1. Add Contact")
        print("2. View All Contacts")
        print("3. Search Contact")
        print("4. Delete Contact")
        print("5. Update Contact")
        print("6. Save & Exit")

        choice = input("Choose an option (1-6): ")

        if choice == "1":
            name = input("Name: ")
            phone = input("Phone: ")
            email = input("Email: ")
            address = input("Address (optional): ")
            new_contact = Contact(name, phone, email, address)
            book.add_contact(new_contact)

        elif choice == "2":
            book.view_contacts()

        elif choice == "3":
            keyword = input("Enter name or phone to search: ")
            book.search_contact(keyword)

        elif choice == "4":
            name = input("Enter contact name to delete: ")
            book.delete_contact(name)

        elif choice == "5":
            name = input("Enter contact name to update: ")
            book.update_contact(name)

        elif choice == "6":
            book.save_contacts()
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please enter a number between 1 and 6.")

# Run the app
if __name__ == "__main__":
    main()
