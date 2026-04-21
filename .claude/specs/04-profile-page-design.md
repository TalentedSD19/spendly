# Spec: Profile Page Design

## Overview
Implement the `/profile` route and page so a logged-in user can view their account details (name, email, member-since date) and update their display name or password. The route stub already exists in `app.py` returning a plain string; this step replaces it with a fully rendered, session-guarded template styled to match Spendly's existing fintech aesthetic. It is the first "authenticated-only" page, establishing the pattern of session checks and login redirects that all future protected routes will follow.

## Depends on
- Step 01 — DB Setup (`users` table with `name`, `email`, `password_hash`, `created_at`)
- Step 02 — Registration (users must exist in the database)
- Step 03 — Login and Logout (session must be set; navbar must be session-aware)

## Routes
- `GET /profile` — render profile page with current user details — logged-in only
- `POST /profile` — handle name or password update form submission — logged-in only

## Database changes
No new tables or columns. A new helper `get_user_by_id(user_id)` must be added to `database/db.py` to fetch the full user row for display. A new helper `update_user(user_id, name, password_hash)` must be added to handle profile updates — `password_hash` may be `None` when only updating the name.

## Templates
- **Create:** `templates/profile.html`
  - Extends `base.html`
  - Displays a profile card: avatar placeholder (initials from name), name, email, member-since date
  - Two distinct form sections: "Update Name" and "Change Password"
  - Flash message block at the top for success/error feedback
  - Styled using existing CSS variables and card/form conventions from the codebase

## Files to change
- `app.py` — replace the `/profile` stub with a full `GET`/`POST` handler; import `get_user_by_id` and `update_user`; add a session guard (redirect to `/login` if `user_id` not in session)
- `database/db.py` — add `get_user_by_id(user_id)` and `update_user(user_id, name, password_hash)` helpers

## Files to create
- `templates/profile.html`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never string-format SQL
- Passwords hashed with `werkzeug.security.generate_password_hash` / verified with `check_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Session guard pattern: `if "user_id" not in session: return redirect(url_for("login"))`
- Password change must require the user to enter their current password first before accepting a new one
- Name update and password change are separate form `POST` actions distinguished by a hidden `action` field (`update_name` / `change_password`)
- After a successful update, use `flash()` and redirect back to `/profile` (PRG pattern) to prevent double-submit
- Update `session["user_name"]` in-place after a successful name change so the navbar reflects the new name immediately

## Definition of done
- [ ] Visiting `/profile` while logged out redirects to `/login`
- [ ] Visiting `/profile` while logged in renders the profile page without a 500 error
- [ ] The profile card shows the correct name, email, and member-since date for the logged-in user
- [ ] Submitting the "Update Name" form with a new valid name updates the database and shows a success flash
- [ ] The navbar reflects the updated name immediately after a name change (no re-login required)
- [ ] Submitting the "Update Name" form with a blank name shows a validation error
- [ ] Submitting the "Change Password" form with a correct current password and matching new passwords updates the hash in the database
- [ ] Submitting the "Change Password" form with an incorrect current password shows "Current password is incorrect"
- [ ] Submitting the "Change Password" form with mismatched new/confirm passwords shows a validation error
- [ ] After a password change, the user can log out and log back in with the new password
- [ ] App starts without errors after all changes
