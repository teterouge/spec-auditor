# Acceptance Criteria Patterns

A library of good and bad AC examples organized by feature type. Use this reference when rewriting untestable ACs in Pass 2, or when you need to understand what "testable" looks like for a specific feature category.

---

## Table of Contents
1. [CRUD Features](#crud-features)
2. [Search & Filtering](#search--filtering)
3. [Authentication & Authorization](#authentication--authorization)
4. [Notifications & Alerts](#notifications--alerts)
5. [Real-Time Features](#real-time-features)
6. [Forms & Validation](#forms--validation)
7. [File Upload & Processing](#file-upload--processing)
8. [Payments & Billing](#payments--billing)
9. [Onboarding Flows](#onboarding-flows)
10. [Dashboard & Analytics](#dashboard--analytics)

---

## CRUD Features

### Creating a record

❌ **Bad:** "Users can create a new project with all required information"
- "All required information" is undefined
- No error state for missing fields

✅ **Good:** "When a user submits the Create Project form with a valid name (1–100 characters, no special characters except hyphens and underscores) and at least one team member selected, a new project record is created and the user is redirected to the project detail page within 2 seconds."

---

❌ **Bad:** "Show an error if the form is incomplete"
- Which fields are required?
- What does the error look like?
- When does it appear (on submit? on blur?)?

✅ **Good:** "If the user submits the form with the Name field empty, display an inline error message 'Project name is required' directly below the Name field. The form does not submit. All other fields retain their entered values."

---

### Editing a record

❌ **Bad:** "Users can edit their profile information"
- Which fields are editable?
- What validation applies?
- What happens on save?

✅ **Good:** "Authenticated users can edit their display name (1–50 characters), bio (0–500 characters), and profile photo. Changes are saved on clicking 'Save changes'. A success toast 'Profile updated' appears for 3 seconds. Unsaved changes prompt a 'Leave without saving?' confirmation dialog when navigating away."

---

### Deleting a record

❌ **Bad:** "Users can delete their account"
- Is there a confirmation step?
- What gets deleted? What's retained?
- Is it reversible?

✅ **Good:** "Users can delete their account from Settings > Account > Delete Account. Clicking 'Delete Account' opens a modal requiring the user to type their email address to confirm. On confirmation, the account is soft-deleted (data retained for 30 days per the retention policy), the user is logged out, and a confirmation email is sent to the registered email address. The action cannot be undone through the UI."

---

## Search & Filtering

❌ **Bad:** "Search results are relevant and load quickly"
- "Relevant" is subjective
- "Quickly" has no threshold

✅ **Good:** "Search returns results matching the query string against [fields: title, description, tags]. Results are ranked by [relevance algorithm/field]. First result page (20 items) renders within 500ms for queries returning ≤1000 matches, measured from keypress to visible results. Queries returning 0 results display the empty state with the exact query text and a 'Clear search' link."

---

❌ **Bad:** "Users can filter by multiple criteria"
- Which criteria?
- Are filters additive (AND) or alternative (OR)?
- What happens when no results match?

✅ **Good:** "Users can filter the project list by Status (Active, Archived, Draft — multi-select, OR logic within field), Owner (single-select from team member list), and Created Date (date range picker). Applied filters display as removable chips above the list. Filters are applied immediately on selection. When no results match the applied filters, display the empty state: 'No projects match your filters' with a 'Clear filters' button."

---

## Authentication & Authorization

❌ **Bad:** "Only admins can access the settings page"
- What happens when a non-admin tries?
- What constitutes an admin?

✅ **Good:** "The /settings route is accessible only to users with the 'organization_admin' role. Users without this role who navigate to /settings directly are redirected to /dashboard with a toast notification: 'You don't have permission to access Settings.' The Settings link in the navigation is not rendered for non-admin users."

---

❌ **Bad:** "Users stay logged in for a reasonable amount of time"
- "Reasonable" is undefined

✅ **Good:** "Sessions expire after 30 days of inactivity. Active sessions (any API request made within 30 days) are extended automatically. Users are shown a 'Session expiring in 5 minutes' modal when a session will expire during an active browser session, with options to extend or log out. Expired sessions redirect to /login with the message 'Your session has expired. Please log in again.'"

---

## Notifications & Alerts

❌ **Bad:** "Users receive notifications for important events"
- Which events?
- What does the notification look like?
- How is it delivered?

✅ **Good:** "Users receive an in-app notification (bell icon, red badge) when: (1) they are @mentioned in a comment, (2) a task assigned to them changes status, (3) a project they own is approaching its deadline (7 days before). Each notification includes the actor name, event type, and a link to the relevant resource. Notifications are marked as read when clicked. The unread count resets to 0 when the user opens the notification panel."

---

❌ **Bad:** "Email notifications should not be spammy"
- "Spammy" is subjective
- No definition of frequency, batching, or opt-out

✅ **Good:** "Email notifications are batched and sent at most once per hour per user when there are unread in-app notifications. If a user has 0 unread notifications, no email is sent. All notification emails include an unsubscribe link that disables email notifications for that notification type. The email subject line format is: '[Product Name] [N] new notification(s) — [first notification summary]'."

---

## Real-Time Features

❌ **Bad:** "The page updates in real-time when other users make changes"
- How quickly?
- What if the connection drops?
- What does the update look like to the user?

✅ **Good:** "When another user edits a shared document, changes are reflected in all connected clients within 2 seconds. If the WebSocket connection is lost, the UI displays a 'Reconnecting...' banner. On reconnection, the client fetches a diff since last sync and applies it without requiring a page reload. Conflicts (two users editing the same field simultaneously) are resolved by last-write-wins, with a brief highlight animation on the updated field."

---

## Forms & Validation

❌ **Bad:** "The form validates user input correctly"
- Which fields?
- What validation rules?
- When does validation trigger?

✅ **Good:**
```
Name field:
- Required
- 2–100 characters
- Validation triggers: on blur and on submit
- Error message: "Name must be between 2 and 100 characters"

Email field:
- Required
- Must match RFC 5322 format (standard email regex)
- Must not be already registered in the system
- Validation triggers: on blur and on submit
- Error messages:
  - Invalid format: "Please enter a valid email address"
  - Already registered: "An account with this email already exists. Log in instead?"

Password field:
- Required
- Minimum 8 characters, at least 1 uppercase, 1 number, 1 special character
- Validation triggers: on submit only
- Error message: "Password must be at least 8 characters and include an uppercase letter, number, and special character"
```

---

## File Upload & Processing

❌ **Bad:** "Users can upload files to their account"
- What file types?
- What size limits?
- What happens during processing?

✅ **Good:** "Users can upload files up to 50MB in the following formats: PDF, DOCX, XLSX, PNG, JPG, MP4. Files are uploaded via drag-and-drop or file picker. During upload, a progress bar shows percentage complete. On completion, the file appears in the file list within 5 seconds. If upload fails (network error, size exceeded, unsupported format), the specific error is shown: 'File too large (max 50MB)', 'Unsupported file type', or 'Upload failed — please try again'. Files are virus-scanned before being available for download; during scanning the file shows status 'Processing...'."

---

## Payments & Billing

❌ **Bad:** "Users can upgrade their plan"
- From which plan?
- What's the proration logic?
- What confirmation do they receive?

✅ **Good:** "Users on the Free plan can upgrade to Pro ($29/month) from Settings > Billing > Upgrade. The upgrade page shows: current plan, new plan features, monthly cost, and a Stripe payment form. On successful payment: (1) plan is upgraded immediately, (2) user receives a confirmation email with receipt within 5 minutes, (3) the billing page reflects the new plan. If payment fails, the Stripe error message is displayed inline: 'Your card was declined. Please check your card details or use a different card.' The plan does not change on failure."

---

## Onboarding Flows

❌ **Bad:** "The onboarding flow guides users through setup"
- How many steps?
- What's required vs. skippable?
- What's the exit condition?

✅ **Good:** "New users complete a 3-step onboarding flow after email verification: (1) Profile setup — display name and avatar (required), (2) Team setup — create or join a team (required), (3) First project — create a project or explore with a template (skippable). Progress is shown as a step indicator. Users can navigate back to previous steps. Completing or skipping step 3 redirects to the dashboard. Closing the browser mid-onboarding and returning resumes at the last incomplete step. Users who have completed onboarding are never shown the onboarding flow again."

---

## Dashboard & Analytics

❌ **Bad:** "The dashboard shows key metrics"
- Which metrics?
- For what time period?
- Updated how often?

✅ **Good:** "The dashboard displays the following metrics for the selected date range (default: last 30 days, selectable: last 7 days, last 30 days, last 90 days, custom range): (1) Total active users — unique users with ≥1 session in period, (2) New signups — accounts created in period, (3) Conversion rate — signups who completed onboarding / total signups, expressed as %. All metrics are calculated as of midnight UTC the previous day. The date the data was last refreshed is displayed below each metric. Metrics load within 3 seconds. If data is unavailable, display '--' with a tooltip: 'Data unavailable for this period'."
