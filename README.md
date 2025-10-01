# Neighborhood Skill Exchange System

A **Python Streamlit web application** that enables neighbors to **offer, request, and exchange skills** within their community. Users can track exchanges, provide feedback, and manage their skill sets in a seamless, intuitive interface.

---

## 🌟 Features

### User Management
- **Sign Up / Login / Logout** functionality.
- Passwords securely hashed using bcrypt.
- Reputation system: users earn points based on feedback.

### Skill Management
- Add skills as **Offer** or **Request**.
- Categorize skills for easier browsing.
- View all your skills.

### Exchange System
- Request exchanges with other users.
- Accept or reject incoming exchange requests.
- Complete exchanges and mark them as done.
- Schedule exchange with optional date/time.

### Feedback System
- Submit feedback on completed exchanges.
- Track ratings and comments for each user.
- Calculate average ratings for each user.

### Browse Skills
- Browse skills by category.
- Request skills from other users while offering your own.

---

## 💻 Tech Stack
- **Backend & Services:** Python, Supabase (as database)
- **Frontend/UI:** Streamlit
- **Authentication & Security:** bcrypt for password hashing
- **Environment Management:** dotenv for environment variables

---

## 📁 Project Structure

```
src/
 ├─ dao/ # Data access objects (User, Skill, Exchange, Feedback)
 ├─ services/ # Business logic for each module
 ├─ config.py # Supabase client configuration
 ├─ app.py # Streamlit app (UI)
 └─ main.py # CLI version of the app
```
---

## ⚡ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/neighborhood-skill-exchange.git
cd neighborhood-skill-exchange

#Create a virtual environment:


python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

#Install dependencies:


pip install -r requirements.txt

#Setup environment variables:


cp .env.example .env
# Fill in your SUPABASE_URL and SUPABASE_KEY

#Run the Streamlit app:


streamlit run src/app.py

```
---
📌 Usage

- Register / Login as a user.


- Add skills you want to offer or request.


- Browse other users’ skills and request exchanges.


- Respond to incoming exchanges and complete them.


- Provide feedback after completing an exchange.


- Track your reputation points based on received feedback.


---
🛠 Future Improvements
- Add real-time notifications for exchange requests.


- Implement chat system between users for easier coordination.


- Improve UI/UX with better design and animations.


- Mobile-friendly responsive design.

---

👤 Author
Harika Donthula
 GitHub: https://github.com/Donthula-Harika

📄 License
This project is licensed under the MIT License.
