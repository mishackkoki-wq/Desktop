# Chimera LMS – Full-Stack Learning Management System

Modern role-based LMS built for the system design document (Learners, Lecturers, Administrators).

## Stack

| Layer     | Technology                                      |
|-----------|-------------------------------------------------|
| Frontend  | HTML5 + CSS3 + Vanilla JS (no frameworks)       |
| Backend   | Node.js HTTP server + EmailJS for SMTP email    |
| Auth      | JWT (HS256)                                     |
| Storage   | JSON file (`backend/data.json`)                 |

## Project Structure

```
chimera-lms/
├── index.html          # Login + app shell
├── Css/styles.css      # Dark/light theme, responsive
├── Javascript/app.js   # Frontend logic + API client
├── README.md
└── backend/
    ├── server.js       # JavaScript REST API
    ├── package.json    # Node run scripts
    └── data.json       # Auto-created on first run
```

## Quick Start

### Start the LMS
```bash
cd backend
npm start
```
The LMS and API run together at **http://127.0.0.1:5000**. Open that address to
register a learner account or sign in. When opening this folder in VS Code, the
workspace task starts the backend automatically; approve the task prompt if VS
Code asks for permission. If it does not start, choose **Terminal → Run Task →
Start Chimera LMS API**.

The server listens on all network interfaces by default, so devices that can
reach the host can open the LMS using the host machine's network address and
port 5000. Set `HOST=127.0.0.1` to restrict access to the host machine.

Sign in using the username (or email) and password for an account. Choose the
matching account type on the sign-in form; the selected role is checked against
the account.

### Seeded Sign-in Accounts
Accounts in `backend/data.json` marked as demo can sign in with the password
`demo`. After the first successful sign-in, the server saves that password as a
scrypt hash and removes the demo flag. Registered accounts with saved password
hashes continue to use their own passwords. Choose the matching account type on
the sign-in form.

The seeded staff accounts are:

| Account type | Email | Initial password |
|--------------|-------|------------------|
| Facilitator | `s.chen@faculty.edu` | `demo` |
| Admin | `m.rivera@admin.edu` | `demo` |

### Learner application and decision emails
After creating a profile, the applicant is signed in and can continue to
registration page 2. They select a course, upload an ID document and
qualification as PDF files (maximum 5 MB each), and submit the application.
The course selection is recorded as pending; the learner is enrolled after an
administrator approves the application. Applicants can sign back in to see the
review status, but cannot enter the learner portal before approval.

Administrators review submitted applications under **Admissions & enrolment**,
download the two PDFs, then approve or decline. The decision email is sent
before the application status is changed; if mail delivery fails, the decision
is not applied and the administrator can try again after fixing the mail setup.

Copy `backend/.env.example` to `backend/.env` and configure `APP_BASE_URL`,
`SMTP_HOST`, `SMTP_PORT`, `SMTP_SECURE`, and `SMTP_FROM`. Set `SMTP_USER` and
`SMTP_PASS` when your SMTP server requires authentication. The approval email
contains the learner portal link; the decline email informs the applicant.
The approval link opens the sign-in form directly.
Never commit real SMTP credentials.

## API Endpoints

| Method | Path                    | Description                  | Auth      |
|--------|-------------------------|------------------------------|-----------|
| GET    | /api/health             | Health check                 | Public    |
| POST   | /api/auth/login         | Login → JWT                  | Public    |
| POST   | /api/auth/register      | Create learner account       | Public    |
| POST   | /api/auth/complete-application | Submit course and PDF documents | Learner |
| GET    | /api/applications       | List applications awaiting review | Admin |
| POST   | /api/applications/decision | Approve or decline and email applicant | Admin |
| GET    | /api/me                 | Current user                 | Bearer    |
| GET    | /api/courses            | List courses                 | Bearer    |
| GET    | /api/assignments        | List assignments             | Bearer    |
| POST   | /api/assignments        | Create assessment            | Lecturer  |
| POST   | /api/submissions        | Submit assignment            | Learner   |
| POST   | /api/submissions/grade  | Grade submission             | Lecturer  |
| GET    | /api/materials          | List materials for accessible courses | Learner / Lecturer / Admin |
| POST   | /api/materials          | Upload a file to a course topic | Lecturer |
| GET    | /api/users              | User list                    | Admin     |
| GET    | /api/audit              | Audit log                    | Admin     |
| GET    | /api/stats              | Role-based stats             | Bearer    |

## Features

- Role-based dashboards (Learner / Lecturer / Admin / Guest)
- JWT authentication
- Assignment submission with file upload UI
- Create assessments
- Grade submissions
- Upload learning files to course topics and track topic completion on the learner's My Courses page
- Admin user management + audit log
- Dark / Light theme toggle (persisted)
- Fully offline-capable fallback if backend is down
- Responsive layout

## Security Notes (Demo)

- Registered passwords are hashed with Node.js scrypt; built-in demo accounts use the shared `demo` password
- Set a private `JWT_SECRET` environment variable before deployment
- For production: use PostgreSQL, proper password hashing (bcrypt/argon2), HTTPS, rate limiting

## Requirements

- Node.js 18 or newer
