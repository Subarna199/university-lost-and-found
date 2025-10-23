# Project Plan — University Lost & Found (Flask Web App)

**Program Developed By Shrestha**

## 1. Problem Description
Universities often handle lost items (phones, keys, IDs, laptops) using informal channels: notice boards, emails, or social media. This leads to slow matching, misplaced items, and difficulty tracking returned items.

### Aspects solvable with a program
- Centralized reporting of lost and found items.
- Search and match functionality to connect finders with owners.
- Status tracking (Unclaimed, Claimed, Returned).
- Administrative tracking and simple analytics (counts, recent reports).

## 2. Process Change
**Before:** Manual, fragmented communication; physical logs or ad-hoc messages.  
**After:** Single web interface where users report and search items; campus staff manage claims. Faster matches, audit trail of reports.

## 3. Requirements on the Program
- Functional:
  - Submit "lost" and "found" reports with item name, date, location, description, contact info.
  - Search reports by keyword, location, or date.
  - Admin view to mark items as returned/claimed.
- Non-functional:
  - Easy to use (simple forms and clear messages).
  - Lightweight: runs on a single host without heavy dependencies.
  - Data persistence: local JSON storage for prototype; easily replaceable with a DB later.

## 4. Change in Operating Model
- Centralized digital logs reduce phone/email-based coordination.
- Staff can use the admin view to reconcile items during daily operations.
- Students use the same familiar web interface anywhere on campus.

## 5. Use Situations
- Student reports a lost student ID after class.
- Staff finds a set of keys on campus and adds a found report.
- Campus Lost & Found office searches for items during office hours to reunite items.

**Deployment options**
- Prototype: Local host (no server required for testing).
- Production: Small VPS or university internal server; HTTPS recommended.

## 6. Software Architecture
**MVC-inspired** (Model: JSON data store, View: Flask + HTML templates, Controller: Flask routes)
- app.py contains routes (controllers), reads/writes `data/lost_found.json` (model), and renders templates (views).
- Reason: Clear separation, easy to replace storage or front-end later.

## 7. Ensuring Correct Functioning
- Input validation on the server side (prevent empty fields).
- Unit tests (not included in prototype) should cover add/search/mark workflows.
- Regular backups of the JSON file; implement file-locking if concurrent writes are expected.

## 8. Usability Considerations
- Minimal fields required to report: item name, where, when, contact.
- Search with free text and filters (location).
- Confirmation messages and clear status labels.

## 9. How the Program Should be Used
1. Run the Flask app locally or on a small server.
2. Users visit the index page to report or search for items.
3. Staff use the Admin page to mark items as returned.
4. Data stored in `data/lost_found.json` for later analysis or migration to a DB.

## 10. Future Extensions
- User authentication (student/staff accounts).
- Email notifications when matches are found.
- Photo uploads for item verification.
- Migrate to PostgreSQL or another RDBMS for concurrency and scale.

---
