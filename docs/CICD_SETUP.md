# GitHub Actions CI/CD Setup Guide

This guide will help you set up the GitHub Actions workflow for automated deployment to Google Cloud Run.

## Prerequisites

- Google Cloud Project with billing enabled
- GitHub repository with your code
- Cloud Run services already created (backend and frontend)
- Cloud SQL instance created

## 1. Set Up Workload Identity Federation (Recommended)

Workload Identity Federation allows GitHub Actions to authenticate to GCP without storing service account keys.

### Create Workload Identity Pool

```bash
# Set your project ID
export PROJECT_ID="project-0df8a33a-f160-4525-a6a"

# Enable required APIs
gcloud services enable iamcredentials.googleapis.com --project="${PROJECT_ID}"

# Create workload identity pool
gcloud iam workload-identity-pools create "github-actions" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --display-name="GitHub Actions Pool"

# Create workload identity provider
# IMPORTANT: Replace YOUR_GITHUB_USERNAME with your actual GitHub username
export GITHUB_USERNAME="YOUR_GITHUB_USERNAME"

gcloud iam workload-identity-pools providers create-oidc "github-provider" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --workload-identity-pool="github-actions" \
  --display-name="GitHub Provider" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository,attribute.repository_owner=assertion.repository_owner" \
  --attribute-condition="assertion.repository_owner == '${GITHUB_USERNAME}'" \
  --issuer-uri="https://token.actions.githubusercontent.com"
```

### Create Service Account for GitHub Actions

```bash
# Create service account
gcloud iam service-accounts create github-actions-sa \
  --display-name="GitHub Actions Service Account" \
  --project="${PROJECT_ID}"

# Grant necessary roles
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:github-actions-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:github-actions-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.writer"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:github-actions-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/cloudsql.client"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:github-actions-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"

# Allow GitHub to impersonate the service account
# Replace YOUR_GITHUB_ORG/YOUR_REPO with your actual GitHub org/username and repo
export REPO="YOUR_GITHUB_USERNAME/YOUR_REPO_NAME"

gcloud iam service-accounts add-iam-policy-binding \
  "github-actions-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
  --project="${PROJECT_ID}" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/$(gcloud projects describe ${PROJECT_ID} --format='value(projectNumber)')/locations/global/workloadIdentityPools/github-actions/attribute.repository/${REPO}"
```

### Get Workload Identity Provider Name

```bash
gcloud iam workload-identity-pools providers describe "github-provider" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --workload-identity-pool="github-actions" \
  --format="value(name)"
```

Save the output - you'll need it for GitHub secrets.

## 2. Configure GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions → New repository secret

Add the following secrets:

### Required Secrets:

1. **GCP_PROJECT_ID**

   - Value: `project-0df8a33a-f160-4525-a6a`

2. **GCP_REGION**

   - Value: `northamerica-northeast1`

3. **GCP_WORKLOAD_IDENTITY_PROVIDER**

   - Value: The output from the command above (should look like: `projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/github-actions/providers/github-provider`)

4. **GCP_SERVICE_ACCOUNT_EMAIL**

   - Value: `github-actions-sa@project-0df8a33a-f160-4525-a6a.iam.gserviceaccount.com`

5. **BACKEND_CORS_ORIGINS**

   - Value: `https://public-square-frontend-940756986344.northamerica-northeast1.run.app`

6. **SECRET_KEY**

   - Value: Your JWT secret key (from cloudrun.env)
   - Example: Generate with: `openssl rand -hex 32`

7. **DATABASE_URL** (if not using Secret Manager)
   - Only needed if you're not using `--set-secrets`
   - Format: `postgresql+asyncpg://user:password@/dbname?host=/cloudsql/CONNECTION_NAME`

## 3. Create Secret Manager Secrets

The workflow uses Secret Manager for the DATABASE_URL:

```bash
# If you haven't already created the DATABASE_URL secret:
echo -n "postgresql+asyncpg://YOUR_DB_USER:YOUR_DB_PASSWORD@/YOUR_DB_NAME?host=/cloudsql/project-0df8a33a-f160-4525-a6a:northamerica-northeast1:public-square-sql" | \
  gcloud secrets create DATABASE_URL \
  --data-file=- \
  --project="${PROJECT_ID}"

# Grant the service accounts access
gcloud secrets add-iam-policy-binding DATABASE_URL \
  --member="serviceAccount:cloud-run-backend-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor" \
  --project="${PROJECT_ID}"

gcloud secrets add-iam-policy-binding DATABASE_URL \
  --member="serviceAccount:github-actions-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor" \
  --project="${PROJECT_ID}"
```

## 4. Frontend Dockerfile

You need to create a Dockerfile for your frontend. Create `frontend/Dockerfile`:

```dockerfile
FROM node:20-alpine AS base

WORKDIR /app

# Copy package files
COPY frontend/app/package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY frontend/app/ ./

# Build the app
RUN npm run build

# Production image
FROM nginx:alpine

# Copy built app to nginx
COPY --from=base /app/dist /usr/share/nginx/html

# Copy nginx config (optional)
# COPY frontend/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

## 5. Test Locally

Before pushing, test the Docker builds locally:

```bash
# Test backend build
cd backend
docker build -t test-backend .

# Test frontend build (once Dockerfile is created)
cd ../frontend
docker build -t test-frontend -f Dockerfile ..
```

## 6. Workflow Overview

The workflow will:

1. ✅ Run backend tests with pytest
2. ✅ Build and push backend Docker image to Artifact Registry
3. ✅ Build and push frontend Docker image to Artifact Registry
4. ✅ Deploy backend to Cloud Run with environment variables
5. ✅ Update/create database migration Cloud Run Job
6. ✅ Run database migrations
7. ✅ Deploy frontend to Cloud Run

## 7. Troubleshooting

### Common Issues:

**Issue: "Permission denied" errors**

- Solution: Check that all IAM roles are granted correctly
- Verify the service account has the necessary permissions

**Issue: "Workload Identity Pool not found"**

- Solution: Make sure you created the pool in the correct project
- Verify the provider name in GitHub secrets is correct

**Issue: "Secret not found"**

- Solution: Create the secret in Secret Manager
- Grant access to the service account

**Issue: Docker build fails**

- Solution: Test builds locally first
- Check Dockerfile paths and context

**Issue: Frontend deployment fails**

- Solution: Create the frontend Dockerfile first
- Or comment out the frontend deployment steps until ready

## 8. Next Steps

1. Replace `YOUR_GITHUB_USERNAME/YOUR_REPO_NAME` in the setup commands
2. Run all the setup commands above
3. Add all secrets to GitHub
4. Create the frontend Dockerfile
5. Push to main branch to trigger the workflow
6. Monitor the workflow in GitHub Actions tab

## Notes

- The workflow triggers on every push to the `main` branch
- Failed deployments won't affect the currently running services
- Always test changes in a development environment first
- Consider adding a staging environment for testing before production
