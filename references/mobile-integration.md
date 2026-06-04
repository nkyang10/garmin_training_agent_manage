# Mobile App Garmin Integration Patterns

## Architecture Options

### 1. iOS App → Python Backend → Garmin API (Preferred)

Reuses the existing `garminconnect` Python library. Backend runs on home PC or cloud server.

```
iOS (SwiftUI) ──→ FastAPI Backend ──→ Garmin Connect API
                    (garminconnect)
```

**Pros:** Reuses all existing workout logic, target types, m/s conversion, SafeGarmin wrapper.
**Cons:** Requires a running backend server.

### 2. iOS Direct via OAuth2 PKCE

Implement Garmin's official OAuth2 PKCE flow natively in Swift. No backend needed.

```
iOS (Swift) ──→ Garmin OAuth2 PKCE ──→ Garmin API (direct REST)
```

**Key endpoints:**
- `GET https://connect.garmin.com/oauth2Confirm` — authorization
- `POST https://diauth.garmin.com/di-oauth2-service/oauth/token` — token exchange & refresh

**Reference:** https://github.com/alexanderhodes/garmin-auth-app (Expo app with complete OAuth2 + auto-refresh)

**Pros:** Self-contained app, no server dependency.
**Cons:** Must reimplement all workout JSON construction in Swift; Garmin's reverse-engineered API quirks (targetTypeId=6 for pace, step-level targetValueOne/Two) must be replicated.

### 3. iOS App → Cloud LLM Backend → Garmin

NL query flows through cloud LLM then Garmin API:

```
iOS ──→ Claude Sonnet 4 ──→ Python Garmin client ──→ Garmin Connect
         (NL → workout JSON)    (push & schedule)
```

### 4. Bookmarklet (No Backend, No OAuth — Cross-Platform)

The simplest integration: iOS app generates workout JSON via LLM → user copies → bookmarks a JS snippet on Garmin Connect → pastes JSON into a bookmarklet popup → submits using the **existing browser session cookies**.

```
iOS App (generates workout JSON via LLM)
    │  user copies JSON
    ▼
Safari/Chrome on connect.garmin.com (already logged in)
    │  taps bookmarklet
    ▼
Bookmarklet popup → paste JSON → enter date → submit
    │
    ▼
fetch POST /workout-service/workout → POST /workout-service/schedule/{id}
(uses existing session cookies — no auth needed)
```

**Setup (once):** Add bookmarklet to Safari/Chrome browser.
Full JS bookmarklet code: <pre>javascript:(function(){let t=document.createElement('textarea'),b=document.createElement('button');t.style.cssText='width:100%;height:100px;font-size:16px;border:1px solid #ccc';b.textContent='Submit';b.style.cssText='font-size:16px;padding:8px 16px;margin-top:6px;background:#007AFF;color:#fff;border:none;border-radius:6px';let d=document.createElement('div');d.style.cssText='position:fixed;top:25%;left:10%;width:80%;background:#fff;border:2px solid #007AFF;padding:16px;z-index:9999;border-radius:12px;box-shadow:0 8px 30px rgba(0,0,0,0.3);font-family:system-ui';d.append(t,b);let c=document.createElement('button');c.textContent='✕';c.style.cssText='float:right;font-size:22px;background:none;border:none;cursor:pointer';c.onclick=()=>document.body.removeChild(d);d.prepend(c);b.onclick=()=>{try{let w=JSON.parse(t.value);fetch('/workout-service/workout',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(w)}).then(r=>r.json()).then(w2=>{let dt=prompt('Date? (YYYY-MM-DD)');if(dt)return fetch('/workout-service/schedule/'+w2.workoutId,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({date:dt})})}).then(r=>{if(r&&r.ok)alert('✅ Done!');else if(r)alert('✅ Scheduled!')}).catch(e=>alert('❌ '+e))}catch(e){alert('❌ Invalid JSON')}};document.body.append(d);t.focus()})()</pre>

**Add bookmarklet on iOS:** Share icon → Add Bookmark → Edit URL → paste the `javascript:` code. Chrome iOS uses the same steps (Share icon at bottom center).

**Pros:** Zero auth code, zero backend, every browser/platform works, 10-minute setup.
**Cons:** Requires browser on desktop or iOS (not native in-app UX), user needs to copy-paste JSON.

**Platform support:**

| Browser | Bookmarklet works? | Chrome Extension? |
|---------|-------------------|-------------------|
| Safari iOS/Desktop | ✅ | N/A |
| Chrome iOS | ✅ (bookmarklet, not extension) | ❌ (iOS Chrome doesn't support extensions) |
| Chrome Desktop | ✅ | ✅ (separate build) |
| Firefox Desktop | ✅ | N/A |

## Garmin API: Two-Step Workflow (No Single Request)

There is NO endpoint that creates and schedules a workout in one call. Always two requests:

| Step | Method | Endpoint | Purpose |
|------|--------|----------|---------|
| 1 | POST | `/workout-service/workout` | Create workout template → returns `workoutId` |
| 2 | POST | `/workout-service/schedule/{workoutId}` | Schedule on calendar date (body: `{"date": "2026-05-30"}`) |

**Pattern:** The iOS app sends one request to your backend; your backend makes both Garmin calls internally.

## Auth Token Flow

`python-garminconnect` uses Garth (SSO-based) and saves tokens to `~/.garminconnect/garmin_tokens.json`. Tokens auto-refresh for ~1 year. On mobile, either:
- **Backend handles all auth** — user credentials stored only on your server
- **Official OAuth2 PKCE** — user authenticates from the iOS app, tokens stored on device
- **Bookmarklet** — uses existing browser session cookies; no token management needed

## LLM Cost Architecture

For cloud LLM integration, use a two-tier approach:
1. **Tier 1 (On-device):** Free classifier (Core ML / Apple Foundation Models / MLX) filters non-training queries
2. **Tier 2 (Cloud):** Claude Sonnet 4 with prompt caching (~$0.0003/query after 90% caching discount) generates workout JSON

90% of chit-chat never reaches the cloud.
