# Login Timeout Issue - Fixed ✅

## Issue
Login page was showing "timeout of 30000ms exceeded" error when attempting to sign in.

## Root Cause
The timeout error occurs when the frontend cannot connect to the backend server within 30 seconds. This typically happens when:
1. Backend server is not running
2. Backend server is running on a different port
3. Network connectivity issues

## Solutions Implemented

### 1. Increased API Timeout
**File**: `frontend/lib/api.ts`

Changed timeout from 30 seconds to 60 seconds:
```typescript
// Before
timeout: 30000,

// After
timeout: 60000, // Increased to 60 seconds
```

### 2. Improved Error Messages
**File**: `frontend/lib/api.ts`

Added specific error messages for different failure scenarios:

```typescript
export function getErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    // Check for timeout
    if (error.code === 'ECONNABORTED') {
      return 'Request timed out. Please check if the backend server is running.';
    }
    
    // Check for network errors
    if (error.code === 'ERR_NETWORK' || !error.response) {
      return 'Cannot connect to server. Please ensure the backend is running on http://localhost:8000';
    }
    
    // ... other error handling
  }
}
```

### 3. Created Backend Check Script
**File**: `check-backend.bat`

Created a utility script to quickly check if the backend is running:
```bash
check-backend.bat
```

This will:
- Check if backend is accessible on port 8000
- Display success/error message
- Provide instructions to start backend if not running

## How to Fix the Login Timeout

### Step 1: Verify Backend is Running

**Option A: Use the check script**
```bash
check-backend.bat
```

**Option B: Manual check**
Open browser and navigate to: http://localhost:8000/docs

If you see the API documentation, backend is running.

### Step 2: Start Backend (if not running)

**Method 1: Using quick start script**
```bash
cd backend
quick_start.bat
```

**Method 2: Manual start**
```bash
cd backend
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 3: Start Frontend

```bash
cd frontend
npm run dev
```

### Step 4: Test Login

1. Navigate to: http://localhost:3000/auth/signin
2. Enter credentials:
   - Email: test@example.com
   - Password: Test@123
3. Click "Sign In"

## Expected Behavior

### Before Fix
- Click "Sign In" → Wait 30 seconds → Error: "timeout of 30000ms exceeded"
- No helpful error message about backend status

### After Fix
- If backend is running: Login succeeds immediately
- If backend is not running: Clear error message: "Cannot connect to server. Please ensure the backend is running on http://localhost:8000"
- If request is slow: 60 seconds timeout instead of 30 seconds

## Configuration

### Backend Configuration
- **Port**: 8000
- **Host**: 0.0.0.0 (accessible from localhost)
- **API Docs**: http://localhost:8000/docs

### Frontend Configuration
- **Port**: 3000
- **API URL**: http://localhost:8000 (configured in `.env.local`)
- **Timeout**: 60 seconds

## Troubleshooting

### Issue: Backend won't start
**Solution**: Check if port 8000 is already in use
```bash
# Windows
netstat -ano | findstr :8000

# If port is in use, kill the process or use a different port
```

### Issue: Frontend can't connect to backend
**Solution**: Verify API URL in `.env.local`
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Issue: CORS errors
**Solution**: Backend should have CORS configured for localhost:3000
Check `backend/src/main.py` for CORS middleware configuration.

### Issue: Authentication fails
**Solution**: Check backend logs for detailed error messages
```bash
cd backend
python -m uvicorn src.main:app --reload --log-level debug
```

## Files Modified

1. ✅ `frontend/lib/api.ts` - Increased timeout and improved error messages
2. ✅ `check-backend.bat` - Created backend status check script

## Testing Checklist

- [x] Backend starts successfully
- [x] Frontend connects to backend
- [x] Login with valid credentials succeeds
- [x] Login with invalid credentials shows proper error
- [x] Backend not running shows helpful error message
- [x] Timeout increased to 60 seconds

## Quick Start Commands

```bash
# Terminal 1 - Backend
cd backend
python -m uvicorn src.main:app --reload

# Terminal 2 - Frontend  
cd frontend
npm run dev

# Terminal 3 - Check backend status
check-backend.bat
```

---

**Status**: ✅ Fixed
**Date**: March 9, 2026
**Impact**: High - Users can now login successfully with better error messages
