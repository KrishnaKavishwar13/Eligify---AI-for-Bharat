# Eligify Frontend - Deployment Guide

## 🚀 Deployment Options

### Option 1: Vercel (Recommended)

Vercel is the easiest way to deploy Next.js apps.

#### Steps:

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

2. **Connect to Vercel**
- Go to [vercel.com](https://vercel.com)
- Click "Import Project"
- Select your GitHub repository
- Vercel auto-detects Next.js

3. **Configure Environment Variables**
Add these in Vercel dashboard:
```
NEXT_PUBLIC_API_URL=https://your-api-gateway.com/api
NEXT_PUBLIC_USE_MOCK_API=false
NEXT_PUBLIC_COGNITO_USER_POOL_ID=your-pool-id
NEXT_PUBLIC_COGNITO_CLIENT_ID=your-client-id
NEXT_PUBLIC_COGNITO_REGION=us-east-1
```

4. **Deploy**
- Click "Deploy"
- Wait 2-3 minutes
- Your app is live! 🎉

#### Custom Domain (Optional)
- Go to Project Settings → Domains
- Add your custom domain
- Update DNS records as instructed

---

### Option 2: AWS Amplify

Perfect for AWS-native deployments.

#### Steps:

1. **Install Amplify CLI**
```bash
npm install -g @aws-amplify/cli
amplify configure
```

2. **Initialize Amplify**
```bash
cd frontend
amplify init
```

3. **Add Hosting**
```bash
amplify add hosting
# Select: Hosting with Amplify Console
```

4. **Configure Build Settings**
Create `amplify.yml`:
```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - npm ci
    build:
      commands:
        - npm run build
  artifacts:
    baseDirectory: .next
    files:
      - '**/*'
  cache:
    paths:
      - node_modules/**/*
```

5. **Deploy**
```bash
amplify publish
```

---

### Option 3: Self-Hosted (Docker)

For custom infrastructure.

#### Create Dockerfile:

```dockerfile
FROM node:18-alpine AS base

# Install dependencies
FROM base AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

# Build app
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Production image
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000

CMD ["node", "server.js"]
```

#### Build and Run:

```bash
# Build image
docker build -t eligify-frontend .

# Run container
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=https://your-api.com/api \
  -e NEXT_PUBLIC_USE_MOCK_API=false \
  eligify-frontend
```

---

## 🔧 Pre-Deployment Checklist

### Code Quality
- [ ] Run `npm run lint` - No errors
- [ ] Run `npm run build` - Builds successfully
- [ ] Test all pages manually
- [ ] Check responsive design
- [ ] Verify all forms work
- [ ] Test error scenarios

### Environment Variables
- [ ] Set `NEXT_PUBLIC_API_URL` to production API
- [ ] Set `NEXT_PUBLIC_USE_MOCK_API=false`
- [ ] Configure Cognito credentials
- [ ] Verify all env vars are prefixed with `NEXT_PUBLIC_`

### Performance
- [ ] Enable Next.js Image Optimization
- [ ] Configure CDN for static assets
- [ ] Enable compression
- [ ] Set up caching headers

### Security
- [ ] Use HTTPS only
- [ ] Set secure headers
- [ ] Configure CORS properly
- [ ] Enable rate limiting
- [ ] Review exposed environment variables

### Monitoring
- [ ] Set up error tracking (Sentry)
- [ ] Configure analytics (Google Analytics)
- [ ] Enable performance monitoring
- [ ] Set up uptime monitoring

---

## 📊 Build Optimization

### Reduce Bundle Size

1. **Analyze Bundle**
```bash
npm install -D @next/bundle-analyzer
```

Add to `next.config.js`:
```js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});

module.exports = withBundleAnalyzer({
  // ... existing config
});
```

Run analysis:
```bash
ANALYZE=true npm run build
```

2. **Dynamic Imports**
Already implemented for modals:
```tsx
const Modal = dynamic(() => import('./Modal'), { ssr: false });
```

3. **Tree Shaking**
Ensure imports are specific:
```tsx
// Good
import { useState } from 'react';

// Bad
import * as React from 'react';
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          
      - name: Install dependencies
        run: npm ci
        working-directory: ./frontend
        
      - name: Run linter
        run: npm run lint
        working-directory: ./frontend
        
      - name: Build
        run: npm run build
        working-directory: ./frontend
        env:
          NEXT_PUBLIC_API_URL: ${{ secrets.API_URL }}
          NEXT_PUBLIC_COGNITO_USER_POOL_ID: ${{ secrets.COGNITO_POOL_ID }}
          NEXT_PUBLIC_COGNITO_CLIENT_ID: ${{ secrets.COGNITO_CLIENT_ID }}
          
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
          working-directory: ./frontend
```

---

## 🌍 Environment-Specific Configs

### Development
```env
NEXT_PUBLIC_API_URL=http://localhost:4000/api
NEXT_PUBLIC_USE_MOCK_API=true
```

### Staging
```env
NEXT_PUBLIC_API_URL=https://staging-api.eligify.com/api
NEXT_PUBLIC_USE_MOCK_API=false
NEXT_PUBLIC_COGNITO_USER_POOL_ID=staging-pool-id
```

### Production
```env
NEXT_PUBLIC_API_URL=https://api.eligify.com/api
NEXT_PUBLIC_USE_MOCK_API=false
NEXT_PUBLIC_COGNITO_USER_POOL_ID=prod-pool-id
```

---

## 📈 Post-Deployment

### Monitoring Checklist
- [ ] Check error rates in logs
- [ ] Monitor API response times
- [ ] Track user sign-ups
- [ ] Monitor page load times
- [ ] Check mobile performance
- [ ] Review user feedback

### Performance Targets
- First Contentful Paint: < 1.5s
- Time to Interactive: < 3.5s
- Largest Contentful Paint: < 2.5s
- Cumulative Layout Shift: < 0.1

---

## 🐛 Troubleshooting

### Build Fails
```bash
# Clear cache
rm -rf .next node_modules
npm install
npm run build
```

### Environment Variables Not Working
- Ensure they start with `NEXT_PUBLIC_`
- Restart dev server after changes
- Check Vercel dashboard for typos

### API Calls Failing
- Verify CORS is configured on backend
- Check API URL is correct
- Ensure auth tokens are being sent
- Review network tab in DevTools

### Slow Performance
- Enable Next.js Image Optimization
- Use CDN for static assets
- Enable compression
- Implement code splitting

---

## 📞 Support

For deployment issues:
1. Check Next.js deployment docs
2. Review Vercel/Amplify logs
3. Check browser console for errors
4. Review network requests

---

Ready to deploy! 🚀
