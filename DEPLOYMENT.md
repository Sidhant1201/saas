# Vercel Deployment Guide

## Prerequisites
All environment variables are already set in Vercel:
- `CLERK_JWKS_URL`
- `CLERK_SECRET_KEY`
- `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`
- `GEMINI_API_KEY`

## Deploy to Vercel

### Option 1: Using Vercel CLI
```bash
vercel --prod
```

### Option 2: Using Git Integration
1. Push your code to GitHub
2. Import the repository in Vercel dashboard
3. Vercel will automatically detect Next.js and deploy

## How it Works

### Development
- Next.js runs on `http://localhost:3000`
- FastAPI runs on `http://127.0.0.1:8000`
- Next.js proxies `/api` requests to FastAPI

### Production (Vercel)
- Next.js and FastAPI are deployed together
- Vercel handles routing via `vercel.json`
- All `/api/*` requests go to the Python backend
- Environment variables are automatically injected

## Testing Locally Before Deploy
```bash
# Terminal 1: Start FastAPI
cd api
uvicorn index:app --reload --port 8000

# Terminal 2: Start Next.js
npm run dev
```

## Post-Deployment
1. Visit your Vercel URL
2. Sign in with Clerk
3. Test the consultation form
4. Verify streaming works correctly
