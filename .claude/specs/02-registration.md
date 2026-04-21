# Spec: Registration

## Overview
Implement user registration so new visitors can create a Spendly account. The existing `GET /register` route already renders the form; this step wires up `POST /register` to validate the submission, hash the password, insert the user into the database, and redirect to the login page on success. It also establishes Flask's `secret_key` and flash-message infrastructure that every subsequent authenticated feature depends on.

## Depends on
- Step 01 — DB Setup (users table, `get_db()` must be in place)

## Routes
- `GET /register` — render registration form — public *(already exists, no change needed)*
- `POST /register` — process registration form, create user, redirect to `/login` — public

## Database changes
No new tables or columns. The existing `users` table (`id`, `name`, `email`, `password_hash`, `created_at`) covers all required fields.

A new helper function `create_user(name, email, password_hash)` must be added to `database/db.py`.

## Templates
- **Modify:** `templates/register.html`
  - Ensure `<form>` has `method="POST"` and `action="/register"`
  - Fields: `name` (text), `email` (email), `password` (password), `confirm_password` (password)
  - Display flashed error/success messages above the form
  - All form inputs must have matching `name` attributes

## Files to change
- `app.py` — add `secret_key`, import `request`/`redirect`/`url_for`/`flash`/`session`, implement `POST /register` logic
- `database/db.py` — add `create_user()` helper
- `templates/register.html` — add POST form attributes, input names, flash message block

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never string-format SQL
- Passwords hashed with `werkzeug.security.generate_password_hash` before any DB write
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- `secret_key` must be set on the Flask `app` object before any flash/session usage; use a hard-coded dev string for now (e.g. `"dev-secret-change-me"`)
- Validate server-side: all fields required, password === confirm_password, email not already registered
- On duplicate email (UNIQUE constraint violation), catch the `sqlite3.IntegrityError` and flash a user-friendly error — do not let a 500 bubble up
- On success, flash a success message and `redirect(url_for("login"))`
- Do not log the user in automatically — that is Step 3 (Login)

## Definition of done
- [ ] Submitting the form with valid data creates a new row in `users` with a hashed password
- [ ] Submitting with mismatched passwords shows an error message on the page without creating a user
- [ ] Submitting with an already-registered email shows an error message without a 500 error
- [ ] Submitting with any blank field shows an error message
- [ ] Successful registration redirects to `/login`
- [ ] A flash success message is visible on the login page after redirect
- [ ] The demo user's email (`demo@spendly.com`) cannot be re-registered
- [ ] App starts without errors after changes to `app.py`
