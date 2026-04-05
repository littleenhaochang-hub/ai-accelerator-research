# Automated Restaurant Booking Pipeline Design (Concept)
**Goal:** Create a robust, semi-automated pipeline for OpenClaw to book restaurants on platforms like `inline.app` or `OpenTable` while bypassing anti-bot measures (reCAPTCHA, OTP).

## The Challenge
Modern booking systems use:
1. **reCAPTCHA v3 / Cloudflare Turnstile:** Blocks headless browsers (like Selenium/Puppeteer) based on mouse movements and IP reputation.
2. **OTP (One-Time Password):** Sends an SMS to the user's phone to verify identity.
3. **Session Cookies/Tokens:** Requires a valid user session.

## Proposed Pipeline Architecture (The "Cookie-Injection" Method)

To allow OpenClaw to book on your behalf, we need to transition from a "bot" to an "authenticated agent."

### Phase 1: One-Time User Authentication (Setup)
1. **Manual Login:** The user (Enhao) logs into `inline.app` on their personal browser (Chrome/Safari).
2. **Cookie Extraction:** The user uses a browser extension (like EditThisCookie or an OpenClaw helper script) to export their valid `inline.app` session cookies and JWT tokens.
3. **Vault Storage:** These cookies are securely saved into OpenClaw's local workspace (e.g., `~/.openclaw/workspace/.secrets/inline_cookies.json`).

### Phase 2: The Agentic Booking Flow (Execution)
When Enhao says: *"Book Xiang Duck at 5 PM tomorrow for 4 people."*

1. **Target Identification:** OpenClaw translates the natural language request into the exact restaurant ID, branch ID, date, time, and party size.
2. **Headless Browser Launch (Stealth Mode):** 
   - OpenClaw launches Playwright or Selenium with stealth plugins (`undetected-chromedriver`).
   - OpenClaw **injects the saved cookies** from Phase 1 into the browser session.
3. **Bypassing the Login Wall:** Because the cookies are injected, the website believes OpenClaw *is* Enhao. The SMS OTP step is completely skipped.
4. **Availability Scan:** OpenClaw navigates directly to the booking URL and scans the DOM for the `17:00` button.
5. **Execution:** 
   - OpenClaw clicks the time slot.
   - Fills in any required checkboxes (e.g., "I agree to the cancellation policy").
   - Clicks "Confirm Booking."
6. **Confirmation:** OpenClaw screenshots the success page and sends the booking reference number back to the chat.

## Fallback Mechanism (The "Human-in-the-Loop" OTP)
If the session cookies expire and the site demands a new SMS OTP during Phase 2:
1. OpenClaw pauses the script.
2. OpenClaw sends a message to Telegram: *"Inline requires a new verification code. It was just sent to your phone. Reply to this message with the 6-digit code."*
3. Enhao replies: *"123456"*
4. OpenClaw reads the reply, inputs it into the browser, and completes the booking.
