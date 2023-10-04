import os
import sys

def main_menu():
    print("1. Run Consumer for Email")
    print("2. Run Consumer for SMS")
    print("3. Generate Data")
    print("4. Run Producer")
    print("5. Exit")

def run_script(script_name):
    script_path = os.path.join(os.path.dirname(__file__), "scripts", script_name)
    os.system(f"python {script_path}")

if __name__ == "__main__":
    while True:
        main_menu()
        choice = input("Select an option: ")

        if choice == "1":
            run_script("consumer_email.py")
        elif choice == "2":
            run_script("consumer_sms.py")
        elif choice == "3":
            run_script("generate_data.py")
        elif choice == "4":
            run_script("producer.py")
        elif choice == "5":
            sys.exit()
        else:
            print("Invalid option. Please select again.")
