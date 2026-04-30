# Backend Implementation Guide

This document outlines the API contracts, JSON payload structures, and conditional logic required by the backend developer to integrate with the newly built React frontend UI.

## 1. UI Routes & Required Endpoints

### 1.1 Onboarding (`/onboarding`)
- **GET** `/api/onboarding/status`: Fetch current onboarding progress.
- **POST** `/api/onboarding/setup`: Submit initial configuration (institute name, logo, context).

### 1.2 Knowledge Base (`/knowledge-base`)
- **POST** `/api/knowledge-base/upload`: Handle PDF/DOCX multi-part file uploads.
- **POST** `/api/knowledge-base/report/save`: Save the edited text of the AI analysis report.
- **GET** `/api/knowledge-base/persona`: Fetch AI Persona settings.
- **POST** `/api/knowledge-base/persona/save`: Save Persona settings.
- **GET** `/api/knowledge-base/script`: Fetch the 5-part AI Script structure.
- **POST** `/api/knowledge-base/script/save`: Save the 5-part AI script flow.
- **POST** `/api/knowledge-base/script/preview`: Generate an audio preview URL given the current script text.

### 1.3 Leads (`/leads`)
- **POST** `/api/leads/upload-csv`: Extract and upload bulk CSV leads.
- **GET** `/api/leads/preview`: Fetch table data for the frontend preview.
- **POST** `/api/leads/campaign/launch`: Save agent config and initiate the automated calling sequence.

### 1.4 Calls (`/calls`)
- **GET** `/api/calls/logs`: Fetch paginated call histories, filterable by search term and sentiment.
- **GET** `/api/calls/details/{callId}`: Fetch specific call transcript, sentiment analysis, and handoff timeline.
- **POST** `/api/calls/trigger`: Manually trigger an outbound call to a specific lead.

### 1.5 Conversations (`/conversations`)
- **GET** `/api/conversations/active`: Fetch active threads across WhatsApp and Voice.
- **GET** `/api/conversations/thread/{threadId}`: Fetch specific conversation history/transcripts.
- **POST** `/api/conversations/reply`: Submit a human override message.
- **POST** `/api/conversations/pause-ai`: Toggle the AI intervention state for a specific thread.

### 1.6 Bookings (`/bookings`)
- **GET** `/api/bookings`: Fetch calendar and list views of scheduled appointments.
- **POST** `/api/bookings/{bookingId}/update`: Update a booking status (e.g., Confirmed) or assigned human agent.

### 1.7 Settings (`/settings`)
- **GET** `/api/settings`: Fetch all global settings (profile, team, routing, notifications, billing).
- **POST** `/api/settings/save`: Push configuration updates to the backend.

---

## 2. Expected JSON Data Structures & Payloads

### 2.1 AI Tone & Persona Payload (`/knowledge-base/ai-tone-persona`)
**Expected POST Payload (Saving Persona):**
```json
{
  "agentName": "Admission Assistant",
  "designation": "Admissions Counselor",
  "toneStyle": "Friendly", // Enum: Formal, Friendly, Persuasive
  "voiceGender": "Female", // Enum: Female, Male
  "voiceSpeed": 1.0,       // Float (0.5 to 2.0)
  "personaDescription": "You are a helpful and enthusiastic admissions counselor representing the university..."
}
```

### 2.2 Pitch Script Structure (`/knowledge-base/pitch-script`)
**Expected GET Response / POST Payload:**
```json
{
  "sections": [
    {
      "id": 1,
      "title": "Section 1: The Opening (Identity & Relevance)",
      "script": "Hi, this is {AgentName} from {UniversityName}...",
      "instruction": "Keep this brief and upbeat"
    }
    // ... Additional sections 2-5
  ]
}
```

### 2.3 Leads Table Schema (`/leads`)
**Expected GET Response:**
```json
{
  "leads": [
    {
      "id": 1,
      "name": "Alice Smith",
      "phone": "+1 555-0101",
      "course": "Computer Science",
      "status": "Pending"
    }
  ],
  "totalRows": 5
}
```

### 2.4 Leads Campaign Configuration Payload (`/leads` Launch Agent)
**Expected POST Payload (Save & Launch Agent):**
```json
{
  "callingConfig": {
    "callingDays": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    "timeStart": "09:00",
    "timeEnd": "17:00",
    "maxAttempts": 3
  },
  "humanFallback": {
    "fallbackName": "John Doe",
    "fallbackPhone": "+1 234 567 8900"
  }
}
```

### 2.5 Calls History Log & Transcript (`/calls`)
**Expected GET Response for a Call Details Fetch:**
```json
{
  "id": 1,
  "name": "Alice Smith",
  "sentiment": "Positive", // Enum: Positive, Neutral, Negative
  "duration": "4m 12s",
  "summary": "Student is highly interested in the CS program...",
  "handoffLog": "11:25 AM - Transferred to John Doe", // Or null
  "transcript": [
    { "speaker": "AI", "text": "Hi Alice, how can I help?" },
    { "speaker": "Human", "text": "Tell me about the CS program." }
  ]
}
```

### 2.6 Conversations Thread (`/conversations`)
**Expected GET Response for Thread details:**
```json
{
  "id": 2,
  "channel": "Voice", // Enum: WhatsApp, Voice
  "activeState": "Needs Human",
  "messages": [
    { "id": 201, "speaker": "AI", "text": "Hello Bob!", "isAudio": false },
    { "id": 202, "speaker": "User", "text": "I need help.", "isAudio": true, "duration": "0:15" }
  ]
}
```

### 2.7 Settings Global Config (`/settings`)
**Expected POST Payload for Schedule Config (`/api/settings/save`):**
```json
{
  "timezone": "America/New_York",
  "businessHours": {
    "start": "09:00",
    "end": "17:30"
  },
  "notifications": {
    "dailySummary": true,
    "leadAlerts": false,
    "handoffAlerts": true,
    "healthAlerts": true
  }
}
```

---

## 3. Conditional Gating Backend Logic

The backend must enforce validation prior to persisting states to guarantee AI agent safety:

1. **AI Knowledge Base Analysis Rules:** 
   - *Requirement:* A user cannot "Save Knowledge" without valid grounding data.
   - *Backend Enforcement:* Check that at least **1 valid PDF/DOCX file** exists and has been fully processed into vector context prior to flagging the Knowledge Base status as 'ready'. Reject saves with empty `reportText`.

2. **Leads Agent Launch Rules:**
   - *Requirement:* The user **cannot** initiate calling sequences without both a target audience and valid routing hours.
   - *Backend Enforcement:* Validate at least 1 valid CSV record exists, `callingDays` array isn't empty, `timeStart` < `timeEnd`, and `fallbackPhone` is in E.164.

3. **Conversation Intervention & Handoffs:**
   - *Requirement:* When a human posts a reply (`/api/conversations/reply`), the AI must stop auto-responding to that thread immediately.
   - *Backend Enforcement:* Hook into the WhatsApp API / Twilio webhooks to set an `aiPaused: true` flag in the database upon the first human execution to prevent cross-talking.

4. **Booking Assignments:**
   - *Requirement:* Ensures a booking isn't dropped blindly.
   - *Backend Enforcement:* Ensure updates to `/api/bookings/{id}/update` pointing to a human assignment correlate to a valid Administrator/Agent ID documented in the `/settings` user map.
