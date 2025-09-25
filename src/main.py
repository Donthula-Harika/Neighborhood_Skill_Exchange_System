# src/main.py

from services.user_service import UserService
from services.skill_service import SkillService
from services.exchange_service import ExchangeService
from services.feedback_service import FeedbackService

user_service = UserService()
skill_service = SkillService()
exchange_service = ExchangeService()
feedback_service = FeedbackService()

current_user = None

def clear_screen():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    """Wait for user to press Enter before continuing."""
    input("\nPress Enter to continue...")

# ------------------ MENU FLOWS ------------------ #

def register_flow():
    print("\n--- Register ---")
    name = input("Name: ").strip()
    email = input("Email: ").strip()
    password = input("Password: ").strip()
    try:
        user = user_service.register_user(name, email, password)
        if user:
            print(f"User {name} registered successfully!")
        else:
            print("Registration failed. Email may already exist.")
    except Exception as e:
        print("Registration error:", e)

def login_flow():
    global current_user
    print("\n--- Login ---")
    email = input("Email: ").strip()
    password = input("Password: ").strip()
    try:
        user = user_service.login_user(email, password)
        if user:
            current_user = user
            print(f"Welcome, {current_user['name']}!")
        else:
            print("Invalid email or password.")
    except Exception as e:
        print("Login error:", e)

def add_skill_flow():
    if not current_user:
        print("You must login first.")
        return
    print("\n--- Add Skill ---")
    skill_name = input("Skill Name: ").strip()
    skill_type = input("Type (Offer/Request): ").strip()
    category = input("Category: ").strip()
    try:
        skill = skill_service.add_skill(current_user['user_id'], skill_name, skill_type, category)
        if skill:
            print(f"Skill '{skill_name}' ({skill_type}) added successfully! ID: {skill.get('skill_id')}")
        else:
            print("Failed to add skill.")
    except Exception as e:
        print("Error adding skill:", e)

def view_skills_flow():
    if not current_user:
        print("You must login first.")
        return
    print("\n--- Your Skills ---")
    skills = skill_service.view_skills(current_user['user_id'])
    if not skills:
        print("No skills found for this user.")
        return
    for s in skills:
        print(f"{s.get('skill_name')} ({s.get('skill_type')}) - Category: {s.get('category')}")

def request_exchange_flow():
    if not current_user:
        print("You must login first.")
        return
    users = user_service.list_all_users()
    users = [u for u in users if u['user_id'] != current_user['user_id']]

    if not users:
        print("No other users available to exchange with.")
        return

    print("\nAvailable Users:")
    for i, user in enumerate(users, start=1):
        print(f"{i}. {user['name']} ({user['email']})")

    try:
        choice = int(input("Select a user to exchange with (number): ")) - 1
        if choice < 0 or choice >= len(users):
            print("Invalid selection.")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    responder = users[choice]

    # Responder's skills
    skills = skill_service.view_skills(responder['user_id'])
    if not isinstance(skills, list):
        print("Error fetching skills for the responder.")
        return
    skills = [s for s in skills if s.get('skill_type') == 'Offer']

    if not skills:
        print(f"{responder['name']} has no offered skills.")
        return

    print("\nAvailable Skills from this user:")
    for i, skill in enumerate(skills, start=1):
        print(f"{i}. {skill.get('skill_name')} ({skill.get('category')})")

    try:
        skill_choice = int(input("Select the skill to request (number): ")) - 1
        if skill_choice < 0 or skill_choice >= len(skills):
            print("Invalid selection.")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    skill_requested = skills[skill_choice]['skill_name']

    # Your own skills to offer
    my_skills = skill_service.view_skills(current_user['user_id'])
    if not isinstance(my_skills, list):
        print("Error fetching your skills.")
        return
    my_skills = [s for s in my_skills if s.get('skill_type') == 'Offer']

    if not my_skills:
        print("You have no skills to offer for exchange.")
        return

    print("\nYour Offered Skills:")
    for i, skill in enumerate(my_skills, start=1):
        print(f"{i}. {skill.get('skill_name')} ({skill.get('category')})")

    try:
        skill_offer_choice = int(input("Select your skill to offer (number): ")) - 1
        if skill_offer_choice < 0 or skill_offer_choice >= len(my_skills):
            print("Invalid selection.")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    skill_offered = my_skills[skill_offer_choice]['skill_name']

    scheduled_time = input("Enter scheduled time (YYYY-MM-DD HH:MM) or leave blank: ").strip()
    if scheduled_time == "":
        scheduled_time = None

    try:
        exchange = exchange_service.request_exchange(
            current_user['user_id'],
            responder['user_id'],
            skill_offered,
            skill_requested,
            scheduled_time
        )
        if isinstance(exchange, dict):
            print(f"\nExchange request created successfully! ID: {exchange.get('exchange_id')}")
        else:
            print("Failed to create exchange:", exchange)
    except Exception as e:
        print("Error creating exchange:", e)



def respond_exchange_flow():
    if not current_user:
        print("You must login first.")
        return

    exchanges = exchange_service.get_exchanges_for_user(current_user['user_id'])
    if isinstance(exchanges, str):
        print("Error fetching exchanges:", exchanges)
        return

    pending = [ex for ex in exchanges if ex.get('status') == 'Pending' and ex.get('responder_id') == current_user['user_id']]
    if not pending:
        print("No pending exchanges to respond to.")
        return

    print("\nPending Exchanges:")
    for i, ex in enumerate(pending, start=1):
        print(f"{i}. Exchange ID:{ex.get('exchange_id')}")
        print(f"   Requested Skill: {ex.get('skill_requested')}")
        print(f"   Offered Skill (from requester): {ex.get('skill_offered')}\n")

    try:
        choice = int(input("Select exchange to respond (number): ")) - 1
        if choice < 0 or choice >= len(pending):
            print("Invalid selection.")
            return
    except ValueError:
        print("Invalid input.")
        return

    exchange = pending[choice]

    # Responder chooses their skill
    my_skills = skill_service.view_skills(current_user['user_id'])
    my_skills = [s for s in my_skills if s.get('skill_type') == 'Offer']

    if not my_skills:
        print("You have no skills to offer. Cannot accept this request.")
        return

    print("\nYour Offered Skills (choose one):")
    for i, s in enumerate(my_skills, 1):
        print(f"{i}. {s.get('skill_name')} ({s.get('category')})")

    try:
        skill_choice = int(input("Select your skill to offer (number): ")) - 1
        if skill_choice < 0 or skill_choice >= len(my_skills):
            print("Invalid selection.")
            return
    except ValueError:
        print("Invalid input.")
        return

    skill_offered_by_responder = my_skills[skill_choice]['skill_name']

    # Update exchange
    try:
        # Update offered skill
        exchange_service.exchange_dao.table.update(
            {"skill_offered": skill_offered_by_responder, "status": "Accepted"}
        ).eq("exchange_id", exchange['exchange_id']).execute()

        print(f"\nExchange accepted! You offered '{skill_offered_by_responder}'.")
    except Exception as e:
        print("Error updating exchange:", e)


def complete_exchange_flow():
    if not current_user:
        print("You must login first.")
        return
    exchanges = exchange_service.get_exchanges_for_user(current_user['user_id'])
    if isinstance(exchanges, str):
        print("Error fetching exchanges:", exchanges)
        return

    accepted = [ex for ex in exchanges if ex.get('status') == 'Accepted']

    if not accepted:
        print("No accepted exchanges to complete.")
        return

    print("\nAccepted Exchanges:")
    for i, ex in enumerate(accepted, start=1):
        print(f"{i}. ID:{ex.get('exchange_id')} - {ex.get('skill_requested')}")

    try:
        choice = int(input("Select exchange to complete (number): ")) - 1
        if choice < 0 or choice >= len(accepted):
            print("Invalid selection.")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    completed = exchange_service.complete_exchange(accepted[choice]['exchange_id'])
    if isinstance(completed, dict):
        print(f"Exchange marked as {completed.get('status')}.")
    else:
        print(completed)

def add_feedback_flow():
    if not current_user:
        print("You must login first.")
        return
    exchanges = exchange_service.get_exchanges_for_user(current_user['user_id'])
    if isinstance(exchanges, str):
        print("Error fetching exchanges:", exchanges)
        return

    completed = [ex for ex in exchanges if ex.get('status') == 'Completed']

    if not completed:
        print("No completed exchanges to give feedback.")
        return

    print("\nCompleted Exchanges:")
    for i, ex in enumerate(completed, start=1):
        print(f"{i}. ID:{ex.get('exchange_id')} - {ex.get('skill_requested')}")

    try:
        choice = int(input("Select exchange to give feedback (number): ")) - 1
        if choice < 0 or choice >= len(completed):
            print("Invalid selection.")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    try:
        rating = int(input("Rating (1-5): "))
        if rating < 1 or rating > 5:
            print("Rating must be between 1 and 5.")
            return
    except ValueError:
        print("Invalid rating. Enter a number between 1 and 5.")
        return

    comments = input("Comments: ").strip()

    try:
        feedback = feedback_service.add_feedback(
            current_user['user_id'], 
            completed[choice]['exchange_id'], 
            rating, 
            comments, 
            user_service=user_service
        )
        if feedback:
            print("Feedback added successfully!")
        else:
            print("Failed to add feedback.")
    except Exception as e:
        print("Error adding feedback:", e)

def view_feedback_flow():
    if not current_user:
        print("You must login first.")
        return
    feedbacks = feedback_service.get_feedback_for_user(current_user['user_id'])
    if not feedbacks:
        print("No feedback found.")
        return
    print("\nYour Feedback (received):")
    for f in feedbacks:
        print(f"From user {f.get('user_id')} - Rating: {f.get('rating')}, Comments: {f.get('comments')}")


def browse_and_request_flow():
    if not current_user:
        print("You must login first.")
        return

    # 1️⃣ Show categories
    categories = skill_service.list_categories()
    if not categories:
        print("No categories available.")
        return

    print("\n--- Skill Categories ---")
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")

    try:
        choice = int(input("Select a category (number): ")) - 1
        if choice < 0 or choice >= len(categories):
            print("Invalid selection.")
            return
    except ValueError:
        print("Invalid input.")
        return

    selected_category = categories[choice]

    # Show skills in category (anonymous)
    skills = skill_service.get_skills_by_category(selected_category)
    skill_list = [s for s in skills if s.get('user_id') != current_user['user_id'] and s.get('skill_type') == 'Offer']

    if not skill_list:
        print(f"No skills available in '{selected_category}'.")
        return

    print(f"\nSkills in '{selected_category}':")
    for i, s in enumerate(skill_list, 1):
        print(f"{i}. {s.get('skill_name')}")

    # Ask to request a skill
    request = input("\nDo you want to request a skill? (yes/no): ").strip().lower()
    if request != "yes":
        return

    try:
        skill_choice = int(input("Select a skill to request (number): ")) - 1
        if skill_choice < 0 or skill_choice >= len(skill_list):
            print("Invalid selection.")
            return
    except ValueError:
        print("Invalid input.")
        return

    skill_requested = skill_list[skill_choice]['skill_name']
    responder_id = skill_list[skill_choice]['user_id']

    #Show your own skills to offer
    my_skills = skill_service.view_skills(current_user['user_id'])
    my_skills = [s for s in my_skills if s.get('skill_type') == 'Offer']

    if not my_skills:
        print("You have no skills to offer for exchange.")
        return

    print("\nYour Offered Skills:")
    for i, s in enumerate(my_skills, 1):
        print(f"{i}. {s.get('skill_name')}")

    try:
        offer_choice = int(input("Select your skill to offer (number): ")) - 1
        if offer_choice < 0 or offer_choice >= len(my_skills):
            print("Invalid selection.")
            return
    except ValueError:
        print("Invalid input.")
        return

    skill_offered = my_skills[offer_choice]['skill_name']

    scheduled_time = input("Enter scheduled time (YYYY-MM-DD HH:MM) or leave blank: ").strip()
    if scheduled_time == "":
        scheduled_time = None

    #  Create exchange request
    try:
        exchange = exchange_service.request_exchange(
            current_user['user_id'],
            responder_id,
            skill_offered,
            skill_requested,
            scheduled_time
        )
        if isinstance(exchange, dict):
            print(f"\nExchange request created! ID: {exchange.get('exchange_id')}")
        else:
            print("Failed to create exchange:", exchange)
    except Exception as e:
        print("Error creating exchange:", e)


# ------------------ MAIN MENU ------------------ #

while True:
    clear_screen()
    if not current_user:
        print("=== Neighborhood Skill-Exchange ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            register_flow(); pause()
        elif choice == "2":
            login_flow(); pause()
        elif choice == "3":
            break
    else:
        print(f"=== Welcome, {current_user['name']} ===")
        print("1. Add Skill")
        print("2. View My Skills")
        print("3. Request Exchange")
        print("4. Respond to Exchange")
        print("5. Complete Exchange")
        print("6. Add Feedback")
        print("7. View Feedback")
        print("8. Logout")
        print("9. Browse & Request Skills by Category")

        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_skill_flow(); pause()
        elif choice == "2":
            view_skills_flow(); pause()
        elif choice == "3":
            request_exchange_flow(); pause()
        elif choice == "4":
            respond_exchange_flow(); pause()
        elif choice == "5":
            complete_exchange_flow(); pause()
        elif choice == "6":
            add_feedback_flow(); pause()
        elif choice == "7":
            view_feedback_flow(); pause()
        elif choice == "8":
            current_user = None  # no pause here
        elif choice == "9":
            browse_and_request_flow(); pause()


