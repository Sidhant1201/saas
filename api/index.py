import os
from fastapi import FastAPI, Depends  # type: ignore
from fastapi.responses import StreamingResponse  # type: ignore
from fastapi_clerk_auth import ClerkConfig, ClerkHTTPBearer, HTTPAuthorizationCredentials  # type: ignore
from google import genai

app = FastAPI()

clerk_config = ClerkConfig(jwks_url=os.getenv("CLERK_JWKS_URL"))
clerk_guard = ClerkHTTPBearer(clerk_config)

@app.get("/api")
def idea(creds: HTTPAuthorizationCredentials = Depends(clerk_guard)):
    user_id = creds.decoded["sub"]  # User ID from JWT - available for future use
    # We now know which user is making the request! 
    # You could use user_id to:
    # - Track usage per user
    # - Store generated ideas in a database
    # - Apply user-specific limits or customization
    async def event_stream():
        client = genai.Client()  # keep client alive for stream lifetime
        try:
            stream = client.models.generate_content_stream(
                model="gemini-3-flash-preview",
                contents=["Reply with a new business idea for AI Agents, formatted with headings, sub-headings and bullet points"],
            )

            for chunk in stream:
                if chunk.text:
                    # IMPORTANT:
                    # - Do NOT split lines
                    # - Preserve raw text
                    # - SSE framing only
                    yield f"data: {chunk.text}\n\n"

        except Exception as e:
            # Send error to client instead of crashing stream
            yield f"data: ERROR: {str(e)}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )