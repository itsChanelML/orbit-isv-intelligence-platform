#!/bin/bash
gcloud run deploy orbit-isv-platform \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --timeout 300 \
  --set-env-vars="SECRET_KEY=orbit-secret-2025-nx9k,ISV_ACCESS_CODE=ORBIT-ISV-2025,ADMIN_ACCESS_CODE=ORBIT-ADMIN-2025,ADMIN_EMAIL=chanel@mentormecollective.org,SENDGRID_FROM_EMAIL=chanel@mentormecollective.org,GCP_PROJECT_ID=orbit-isv-intelligence,DEBUG=False"
