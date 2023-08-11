from pymongo import MongoClient
from datetime import datetime
from hashlib import sha256

client = MongoClient("mongodb://localhost:27017/")
db = client["todo_app"]
users_collection = db["users"]
tasks_collection = db["tasks"]

def add_task(task_text, due_date, priority):
    task = {
        "text": task_text,
        "due_date": due_date,
        "priority": priority,
        "completed": False
    }
    tasks_collection.insert_one(task)

def register_user(username, password):
    password_hash = sha256(password.encode()).hexdigest()
    user = {"username": username, "password": password_hash}
    users_collection.insert_one(user)


def login(username, password):
    password_hash = sha256(password.encode()).hexdigest()
    return users_collection.find_one({"username": username, "password": password_hash})    

def get_tasks(filter_query=None):
    if filter_query is None:
        return tasks_collection.find()
    else:
        return tasks_collection.find(filter_query)
    
def mark_task_as_completed(task_id):
    tasks_collection.update_one({"_id": task_id}, {"$set": {"completed": True}})

def delete_task(task_id):
    tasks_collection.delete_one({"_id": task_id})

if __name__ == "__main__":
    while True:
        print("Todo List App")
        print("1. Register")
        print("2. Login")
        print("3. Add Task")
        print("4. List Tasks")
        print("5. Delete Task")
        print("6. Mark Task as Completed")
        print("7. List Completed Tasks")
        print("8. Exit")
        
        choice = input("Select an option: ")
        
        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            register_user(username, password)
            print("User registered successfully.")
        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            user = login(username, password)
            if user:
                print("Login successful.")
                user_id = user["_id"]
            else:
                print("Invalid credentials.")
                continue
        elif choice == "3":
            task_text = input("Enter task text: ")
            due_date = input("Enter due date (YYYY-MM-DD): ")
            priority = input("Enter priority (High/Medium/Low): ")
            add_task(task_text, datetime.strptime(due_date, "%Y-%m-%d"), priority)
            print("Task added successfully.")
        elif choice == "4":
            tasks = get_tasks()
            for task in tasks:
                status = "Completed" if task["completed"] else "Not Completed"
                print(f"{task['_id']}: {task['text']} (Due: {task['due_date']} | Priority: {task['priority']}) - {status}")
        elif choice == "5":
            task_id = input("Enter task ID to mark as completed: ")
            mark_task_as_completed(task_id)
            print("Task marked as completed.")
        elif choice == "6":
            task_id = input("Enter task ID to delete: ")
            delete_task(task_id)
            print("Task deleted.")       
        elif choice == "7":
            completed_tasks = get_tasks({"completed": True})
            for task in completed_tasks:
                print(f"{task['_id']}: {task['text']} (Due: {task['due_date']} | Priority: {task['priority']})")
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")