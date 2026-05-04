
#!/bin/bash

gcloud run deploy orbit-isv-platform --source . --region us-central1 --allow-unauthenticated --memory 1Gi --timeout 300 --set-env-vars="NVIDIA_API_KEY=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,SECRET_KEY=orbit-secret-2025-nx9k,ISV_ACCESS_CODE=ORBIT-ISV-2025,ADMIN_ACCESS_CODE=ORBIT-ADMIN-2025,SENDGRID_API_KEY=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,ADMIN_EMAIL=chanel@mentormecollective.org,SENDGRID_FROM_EMAIL=chanel@mentormecollective.org,IPINFO_TOKEN=d772a2411991a6,GCP_PROJECT_ID=orbit-isv-intelligence,DEBUG=False"

