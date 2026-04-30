# 🚀 Admission AI - Postman API Flow Guide

This document outlines the logical sequence of API calls needed to test the application from start to finish.

---

## 1. Initial Setup (Development Only)
If you want to quickly test with pre-filled data, use the seed endpoint.
- **GET** `/api/dev/seed`
  - *Result*: Creates a demo institute and a super_admin user (`demo@example.com` / `admin123`).

---

## 2. Authentication Flow
Every request (except Login/Register) requires an `Authorization: Bearer <TOKEN>` header.

### A. Registration
- **POST** `/api/auth/register`
  - *Payload*: `{"full_name": "...", "email": "...", "password": "...", "institute_name": "..."}`
### B. Login
- **POST** `/api/auth/login`
  - *Payload*: `{"email": "...", "password": "..."}`
  - *Action*: Copy the `access_token` for subsequent requests.

---

## 3. Onboarding Flow
After logging in, an institute needs to complete onboarding.

- **GET** `/api/onboarding/status`
  - Checks current progress.
- **POST** `/api/onboarding/step`
  - *Payload*: `{"step": 1, "data": {...}}`
  - Updates the onboarding state.

---

## 4. Knowledge & Personas
Set up the "brain" of your AI agent.

- **POST** `/api/knowledge/upload`
  - *Multipart/Form*: Upload PDF/Text files.
- **POST** `/api/knowledge/persona`
  - *Payload*: `{"agent_name": "Sarah", "tone_style": "Professional", ...}`

---

## 5. Leads & Campaigns
The core logic for managing admissions.

### A. Managing Leads
- **GET** `/api/leads/` - List all leads.
- **POST** `/api/leads/import` - Bulk import leads via JSON/CSV.

### B. Launching Campaigns
- **POST** `/api/leads/campaigns`
  - *Payload*: `{"name": "Summer Intake", "calling_days": ["Mon", "Wed"], "time_start": "09:00", ...}`

---

## 6. Live Interactions
View ongoing calls and conversations.

- **GET** `/api/calls/logs` - List all call attempts.
- **GET** `/api/conversations/{lead_id}` - Get full chat/call transcript for a lead.

---

## 🛠️ Postman Tips
1. **Environment Variables**: Create an environment in Postman and add a variable `base_url` set to `http://localhost:8000`.
2. **Auth Header**: In your Postman Collection, go to the **Auth** tab, select **Bearer Token**, and use `{{access_token}}`.
3. **Tests Script**: In your Login request's "Tests" tab, add:
   ```javascript
   pm.environment.set("access_token", pm.response.json().access_token);
   ```
