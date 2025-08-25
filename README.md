# Authentication System Challenge – Backend/API

This project is a solution to the Authentication System Challenge, where the objective is to design and implement a secure authentication backend with JWT (JSON Web Token) integration and conditional response mechanisms.
The system ensures that only authenticated users with valid credentials can access protected routes and secret information.

Objectives:

->User registration, login, and protected routes
->JWT authentication with access & refresh token validation
->Systematic discovery process to access hidden/secret keys
->Protected API endpoints requiring valid JWTs
->Bonus: Secure cookie management for session handling alongside JWTs

Frontend Client interacts with API endpoints:

JWT Layer validates issued tokens.
Protected Routes only return secret data if JWT is valid.
PostgreSQL stores user credentials securely.

Visual Documentation:

->User registers → POST /register
->Logs in → receives JWT access & refresh tokens
->Calls protected endpoint → must include Authorization: Bearer <token>
->If valid, secret/hidden data is returned

Screenshot of Register route -> https://1drv.ms/i/c/9e20c83bc241a9d6/EXc_gyboaX5FnMnuYA7eO00BkEZo2ubRYjmlnvGpyEJ1Ag?e=ufPGWD

Screenshot of Login Route -> https://1drv.ms/i/c/9e20c83bc241a9d6/Eer_cx-PPp1CjVZrCNU2qtoBbdsg2MJbWxULT64-x5x7bQ?e=b08KeI

Screenshot of Secret Route -> https://1drv.ms/i/c/9e20c83bc241a9d6/EX-hkuXpKPRMm9Rcg0xSItUB6Lj1fvrLil0qaZqgDLmyvg?e=a5HS8q


Demonstration Video:

👉 Demo Video (2-3 mins) : https://youtu.be/5DNvPmPmy7Y

⚙️ Installation & Setup
1. Clone the repository
git clone https://github.com/yourusername/auth-system-challenge.git
cd auth-system-challenge

2. Create & activate a virtual environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

3. Install dependencies
pip install -r requirements.txt

4. Setup environment variables

Create .env file:

SECRET_KEY=your-django-secret
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=postgresql://user:password@localhost:5432/auth_db

5. Run migrations
python manage.py migrate

6. Start the server
python manage.py runserver

->Secret Key Discovery (Protected)

->The secret key can only be revealed by accessing the /secret/ endpoint with a valid JWT token.

Example:

GET /secret/
Authorization: Bearer <valid_access_token>
->If the token is valid → response:

{
  "message": "Congrats 🎉 You discovered the hidden key!",
  "secret_key": "secretkey@authchallenge"
}


->If the token is invalid/expired → response:
{
  "detail": "Authentication credentials were not provided."
}

</details>
Technology Stack :

Backend Framework: Django + Django REST Framework
Authentication: JWT via rest_framework_simplejwt
Database: PostgreSQL

Security:
JWT-based Auth
Token Blacklisting (logout)
Secure cookie handling (bonus)
Deployment: Render / Docker-ready

->In addition to Authorization headers, JWT tokens can be stored in HttpOnly secure cookies for improved session handling and protection against XSS.

