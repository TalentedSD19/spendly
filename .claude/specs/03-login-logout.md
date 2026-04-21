# Spec: Login and Logout

## Overview
Implement session-based login and logout so registered users can authenticate with their email and password and maintain a logged-in state across requests. The `GET /login` route already renders the form; this step wires up `POST /login` to verify credentials against the database, store the user's `id` and `name` in Flask's session on success, and redirect to a dashboard stub. `GET /logout` clears the session and redirects to the landing page. It also updates the navbar to show contextual links (sign-in/register vs. username/logout) depending on session state.

## Depends on
- Step 01 — DB Setup (`users` table, `get_db()` must be in place)
- Step 02 — Registration (users must exist in the database to log in)

## Routes
- `GET /login` — render login form — public *(already exists, needs POST added)*
- `POST /login` — validate credentials, set session, redirect to `/dashboard` — public
- `GET /logout` — clear session, redirect to `/` — logged-in *(stub already exists)*

## Database changes
No new tables or columns. A new helper `get_user_by_email(email)` must be added to `database/db.py` to look up a user row by email for credential verification.

## Templates
- **Modify:** `templates/login.html`
  - Add flash message block (success/error) above the form
  - Form already has `method="POST" action="/login"` and correct field names — confirm and keep
- **Modify:** `templates/base.html`
  - Navbar `nav-links` div: when `session.user_id` is set, show the user's name and a "Sign out" link (`/logout`); otherwise show the existing "Sign in" and "Get started" links

## Files to change
- `app.py` — implement `POST /login` logic and `GET /logout`; add `session` to Flask imports; add a minimal `GET /dashboard` stub so the post-login redirect resolves
- `database/db.py` — add `get_user_by_email(email)` helper
- `templates/login.html` — add flash message display block
- `templates/base.html` — make navbar session-aware

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never string-format SQL
- Passwords verified with `werkzeug.security.check_password_hash` — never compare plaintext
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Store only `user_id` (int) and `user_name` (str) in `session` — never the password hash
- On failed login, re-render `login.html` with a generic error ("Invalid email or password") — do not reveal which field was wrong
- `GET /logout` must use `session.clear()` and then `redirect(url_for('landing'))`
- The dashboard stub can return a plain string for now — it will be fully implemented in a later step
- `app.secret_key` is already set in `app.py`; do not change it

## Definition of done
- [ ] Submitting valid credentials sets `session['user_id']` and `session['user_name']` and redirects to `/dashboard`
- [ ] Submitting an unknown email shows "Invalid email or password" without a 500 error
- [ ] Submitting a correct email with a wrong password shows "Invalid email or password"
- [ ] Submitting with blank fields shows an error message
- [ ] Visiting `/logout` clears the session and redirects to `/`
- [ ] After logout, visiting `/dashboard` does not show the previous user's session data
- [ ] The navbar shows "Sign out" and the user's name when logged in
- [ ] The navbar shows "Sign in" and "Get started" when logged out
- [ ] The demo user (`demo@spendly.com` / `demo123`) can log in successfully
- [ ] App starts without errors after all changes
