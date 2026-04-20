# Admission AI - Backend API Testing Guide

This document provides a single, end-to-end example with exact payloads and URLs you can use to test the backend in Postman.

> [!IMPORTANT]
> The backend routes use `/api` as the base structure. Additionally, grouped routes like `/call/trigger` or `/conversations/active` are located inside the `communication` router, so their full path requires the `/communication` prefix. See the correct URLs below.

## 1. Developer Database Seeding
**URL**: `POST http://localhost:8000/api/dev/seed`  
**Description**: Populates the database with initial fake data if needed.
**Payload** (JSON):
```json
{}
```

## 2. Register User
**URL**: `POST http://localhost:8000/api/auth/register`
**Payload** (JSON):
```json
{
  "fullName": "Rohan Mehta",
  "email": "rohan.mehta.ai01@gmail.com",
  "password": "SecurePass123",
  "instituteName": "NextGen Academy"
}
```

## 3. Login
**URL**: `POST http://localhost:8000/api/auth/login`
**Payload** (JSON):
```json
{
  "email": "rohan.mehta.ai01@gmail.com",
  "password": "SecurePass123"
}
```
*Note: Copy the `access_token` returned in the response. Use it as a Bearer Token for all subsequent requests.*

## 4. Onboarding Setup
**URL**: `POST http://localhost:8000/api/onboarding/setup`
**Auth**: Bearer Token
**Payload** (JSON):
```json
{
  "fullName": "Rohan Mehta",
  "email": "rohan.mehta.ai01@gmail.com",
  "instituteName": "NextGen Academy"
}
```

## 5. Knowledge Base Upload
**URL**: `POST http://localhost:8000/api/knowledge-base/upload`
**Auth**: Bearer Token
**Payload** (Form-Data):
- Key: `file`, Type: File, Value: `[attach a test pdf/doc]`

## 6. Save Persona
**URL**: `POST http://localhost:8000/api/knowledge-base/persona`
**Auth**: Bearer Token
**Payload** (JSON):
```json
{
  "agent_name": "Aisha",
  "designation": "Senior Admission Advisor",
  "tone_style": "professional",
  "voice_gender": "female",
  "voice_speed": 1.1,
  "persona_description": "Confident and helpful counselor guiding students"
}
```

## 7. Save Script
**URL**: `POST http://localhost:8000/api/knowledge-base/script`
**Auth**: Bearer Token
**Payload** (JSON):
```json
{
  "sections": [
    {
      "id": "intro_1",
      "title": "Introduction",
      "content": "Hello, this is Riya from Future Tech Institute. Am I speaking with {{name}}?",
      "isActive": true
    },
    {
      "id": "interest_check",
      "title": "Interest Check",
      "content": "I noticed you showed interest in {{course}}. Are you still looking for admission?",
      "isActive": true
    }
  ]
}
```

## 8. Leads Upload (CSV)
**URL**: `POST http://localhost:8000/api/leads/upload-csv`
**Auth**: Bearer Token
**Payload** (Form-Data):
- Key: `file`, Type: File, Value: `[attach leads.csv file]`

## 9. Campaign Launch
**URL**: `POST http://localhost:8000/api/leads/campaign/launch`
**Auth**: Bearer Token
**Payload** (JSON):
```json
{
  "callingDays": ["Mon", "Wed", "Fri"],
  "timeStart": "10:00",
  "timeEnd": "17:00",
  "maxAttempts": 2,
  "fallbackName": "Support Team",
  "fallbackPhone": "+918888888888"
}
```

## 10. Trigger Call
> [!NOTE] 
> This route evaluates under the `communication` prefix.
**URL**: `POST http://localhost:8000/api/communication/call/trigger`
**Auth**: Bearer Token
**Payload** (JSON):
```json
{
  "leadId": 1
}
```

## 11. View Active Conversations
**URL**: `GET http://localhost:8000/api/communication/conversations/active`
**Auth**: Bearer Token
**Payload**: `None`

## 12. View Conversation Thread
**URL**: `GET http://localhost:8000/api/communication/conversations/1/thread`
**Auth**: Bearer Token
**Payload**: `None`

## 13. Reply manually in Conversation
**URL**: `POST http://localhost:8000/api/communication/conversations/1/reply`
**Auth**: Bearer Token
**Payload** (JSON):
```json
{
  "content": "Sure, I will guide you step by step."
}
```

## 14. Update Booking Status
> [!NOTE] 
> The path uses a parameter for the booking ID (`/bookings/{booking_id}/status`)
**URL**: `POST http://localhost:8000/api/bookings/1/status`
**Auth**: Bearer Token
**Payload** (JSON):
```json
{
  "status": "confirmed",
  "agentAssignedId": 301
}
```

## 15. Save Settings
**URL**: `POST http://localhost:8000/api/settings/save`
**Auth**: Bearer Token
**Payload** (JSON):
```json
{
  "whatsappEnabled": true,
  "callEnabled": true
}
```
