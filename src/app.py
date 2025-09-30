# src/app.py
import streamlit as st
from services.user_service import UserService
from services.skill_service import SkillService
from services.exchange_service import ExchangeService
from services.feedback_service import FeedbackService

# Services
user_service = UserService()
skill_service = SkillService()
exchange_service = ExchangeService()
feedback_service = FeedbackService()

# Initialize session state
if "current_user" not in st.session_state:
    st.session_state.current_user = None

# ---------------- UI FLOWS ---------------- #

def register_ui():
    st.subheader("Register")
    name = st.text_input("Name", key="reg_name")
    email = st.text_input("Email", key="reg_email")
    password = st.text_input("Password", type="password", key="reg_pass")
    if st.button("Register"):
        try:
            user = user_service.register_user(name, email, password)
            if user:
                st.success(f"User {name} registered successfully!")
            else:
                st.error("Registration failed. Email may already exist.")
        except Exception as e:
            st.error(f"Registration error: {e}")

# def login_ui():
#     st.subheader("Login")
#     email = st.text_input("Email", key="login_email")
#     password = st.text_input("Password", type="password", key="login_pass")
#     if st.button("Login"):
#         user = user_service.login_user(email, password)
#         if user:
#             st.session_state.current_user = user
#             st.success(f"Welcome, {user['name']}!")
#             st.experimental_rerun()  # Immediately update UI
#         else:
#             st.error("Invalid email or password.")

# def logout_ui():
#     if st.button("Logout"):
#         st.session_state.current_user = None
#         st.success("Logged out successfully!")
#         st.experimental_rerun()  # Immediately update UI



def login_ui():
    st.subheader("Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_pass")
    if st.button("Login"):
        user = user_service.login_user(email, password)
        if user:
            st.session_state.current_user = user
            st.success(f"Welcome, {user['name']}!")
            st.session_state.login_trigger = not st.session_state.get("login_trigger", False)  # Force rerun
        else:
            st.error("Invalid email or password.")

def logout_ui():
    if st.button("Logout"):
        st.session_state.current_user = None
        st.success("Logged out successfully!")
        st.session_state.login_trigger = not st.session_state.get("login_trigger", False)  # Force rerun


def add_skill_ui():
    st.subheader("Add Skill")
    skill_name = st.text_input("Skill Name", key="skill_name")
    skill_type = st.selectbox("Type", ["Offer", "Request"], key="skill_type")
    category = st.text_input("Category", key="skill_cat")
    if st.button("Add Skill", key="add_skill_btn"):
        try:
            skill = skill_service.add_skill(
                st.session_state.current_user['user_id'], skill_name, skill_type, category
            )
            st.success(f"Skill '{skill_name}' ({skill_type}) added!")
        except Exception as e:
            st.error(f"Error: {e}")

def view_skills_ui():
    st.subheader("Your Skills")
    skills = skill_service.view_skills(st.session_state.current_user['user_id'])
    if skills:
        for s in skills:
            st.write(f"{s['skill_name']} ({s['skill_type']}) - Category: {s['category']}")
    else:
        st.info("No skills found.")

def request_exchange_ui():
    st.subheader("Request Exchange")
    users = user_service.list_all_users()
    users = [u for u in users if u['user_id'] != st.session_state.current_user['user_id']]
    if not users:
        st.info("No users to exchange with.")
        return

    user_names = [f"{u['name']} ({u['email']})" for u in users]
    idx = st.selectbox("Select user to exchange with", range(len(users)), format_func=lambda i: user_names[i], key="req_user")
    responder = users[idx]

    # Skills offered by responder
    skills = skill_service.view_skills(responder['user_id'])
    offered_skills = [s for s in skills if s['skill_type'] == "Offer"]
    if not offered_skills:
        st.info(f"{responder['name']} has no offered skills.")
        return
    skill_idx = st.selectbox("Select skill to request", range(len(offered_skills)), format_func=lambda i: offered_skills[i]['skill_name'], key="req_skill")
    skill_requested = offered_skills[skill_idx]['skill_name']

    # Your skills to offer
    my_skills = [s for s in skill_service.view_skills(st.session_state.current_user['user_id']) if s['skill_type']=="Offer"]
    if not my_skills:
        st.info("You have no skills to offer.")
        return
    my_idx = st.selectbox("Select your skill to offer", range(len(my_skills)), format_func=lambda i: my_skills[i]['skill_name'], key="req_my_skill")
    skill_offered = my_skills[my_idx]['skill_name']

    scheduled_time = st.text_input("Scheduled time (YYYY-MM-DD HH:MM, optional)", key="req_time")
    if st.button("Send Exchange Request", key="req_btn"):
        scheduled = scheduled_time if scheduled_time.strip() else None
        try:
            exchange = exchange_service.request_exchange(
                st.session_state.current_user['user_id'], responder['user_id'],
                skill_offered, skill_requested, scheduled
            )
            st.success(f"Exchange request created! ID: {exchange.get('exchange_id')}")
        except Exception as e:
            st.error(f"Error creating exchange: {e}")

def respond_exchange_ui():
    st.subheader("Respond to Exchanges")
    exchanges = exchange_service.get_exchanges_for_user(st.session_state.current_user['user_id'])
    pending = [ex for ex in exchanges if ex['status']=="Pending" and ex['responder_id']==st.session_state.current_user['user_id']]
    if not pending:
        st.info("No pending exchanges.")
        return

    ex_idx = st.selectbox("Select exchange to respond", range(len(pending)), format_func=lambda i: f"ID {pending[i]['exchange_id']}: {pending[i]['skill_requested']}", key="resp_ex")
    exchange = pending[ex_idx]

    # Your offered skills
    my_skills = [s for s in skill_service.view_skills(st.session_state.current_user['user_id']) if s['skill_type']=="Offer"]
    if not my_skills:
        st.info("No skills to offer.")
        return
    skill_idx = st.selectbox("Select skill to offer", range(len(my_skills)), format_func=lambda i: my_skills[i]['skill_name'], key="resp_skill")
    skill_offered = my_skills[skill_idx]['skill_name']

    if st.button("Accept Exchange", key="accept_btn"):
        try:
            exchange_service.exchange_dao.table.update(
                {"skill_offered": skill_offered, "status": "Accepted"}
            ).eq("exchange_id", exchange['exchange_id']).execute()
            st.success(f"Exchange accepted with skill '{skill_offered}'!")
        except Exception as e:
            st.error(f"Error: {e}")

def complete_exchange_ui():
    st.subheader("Complete Exchanges")
    exchanges = exchange_service.get_exchanges_for_user(st.session_state.current_user['user_id'])
    accepted = [ex for ex in exchanges if ex['status']=="Accepted"]
    if not accepted:
        st.info("No accepted exchanges.")
        return
    ex_idx = st.selectbox("Select exchange to complete", range(len(accepted)), format_func=lambda i: f"ID {accepted[i]['exchange_id']}", key="comp_ex")
    exchange = accepted[ex_idx]
    if st.button("Mark Completed", key="comp_btn"):
        exchange_service.complete_exchange(exchange['exchange_id'])
        st.success("Exchange marked as Completed!")

def add_feedback_ui():
    st.subheader("Add Feedback")
    exchanges = exchange_service.get_exchanges_for_user(st.session_state.current_user['user_id'])
    completed = [ex for ex in exchanges if ex['status']=="Completed"]
    if not completed:
        st.info("No completed exchanges.")
        return
    ex_idx = st.selectbox("Select exchange to give feedback", range(len(completed)), format_func=lambda i: f"ID {completed[i]['exchange_id']}", key="fb_ex")
    exchange = completed[ex_idx]

    rating = st.slider("Rating", 1, 5, key="fb_rating")
    comments = st.text_area("Comments", key="fb_comments")
    if st.button("Submit Feedback", key="fb_btn"):
        feedback_service.add_feedback(st.session_state.current_user['user_id'], exchange['exchange_id'], rating, comments, user_service=user_service)
        st.success("Feedback submitted!")

def view_feedback_ui():
    st.subheader("View Feedback")
    feedbacks = feedback_service.get_feedback_for_user(st.session_state.current_user['user_id'])
    if not feedbacks:
        st.info("No feedback received.")
        return
    for f in feedbacks:
        st.write(f"From user {f['user_id']}: Rating {f['rating']}, Comments: {f['comments']}")

# ------------------ MAIN APP ---------------- #

def main():
    # At the very top of main()
    if "login_trigger" not in st.session_state:
        st.session_state.login_trigger = False  # just to toggle rerun

    if st.session_state.current_user is None:
        tab = st.selectbox("Select Tab", ["Register", "Login"])
        if tab=="Register":
            register_ui()
        elif tab=="Login":
            login_ui()
    else:
        tabs = ["Add Skill", "View Skills", "Request Exchange", "Respond Exchange", "Complete Exchange", "Add Feedback", "View Feedback", "Logout"]
        choice = st.selectbox("Select Tab", tabs, key="main_tabs")
        if choice=="Add Skill":
            add_skill_ui()
        elif choice=="View Skills":
            view_skills_ui()
        elif choice=="Request Exchange":
            request_exchange_ui()
        elif choice=="Respond Exchange":
            respond_exchange_ui()
        elif choice=="Complete Exchange":
            complete_exchange_ui()
        elif choice=="Add Feedback":
            add_feedback_ui()
        elif choice=="View Feedback":
            view_feedback_ui()
        elif choice=="Logout":
            logout_ui()

if __name__ == "__main__":
    st.set_page_config(page_title="Neighborhood Skill Exchange")
    main()
