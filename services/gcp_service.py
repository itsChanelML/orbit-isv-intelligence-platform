import json
import os
from datetime import datetime, timezone
from google.oauth2 import service_account
from googleapiclient.discovery import build
from config import Config

GCP_STATE_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'gcp_state.json')

# GCP APIs we care about surfacing to ISVs
RELEVANT_APIS = {
    'aiplatform.googleapis.com': 'Vertex AI',
    'bigquery.googleapis.com': 'BigQuery',
    'run.googleapis.com': 'Cloud Run',
    'container.googleapis.com': 'Google Kubernetes Engine',
    'storage.googleapis.com': 'Cloud Storage',
    'cloudfunctions.googleapis.com': 'Cloud Functions',
    'pubsub.googleapis.com': 'Pub/Sub',
    'dataflow.googleapis.com': 'Dataflow',
    'notebooks.googleapis.com': 'Vertex AI Workbench',
    'ml.googleapis.com': 'Cloud ML Engine',
    'speech.googleapis.com': 'Speech-to-Text',
    'vision.googleapis.com': 'Vision AI',
    'language.googleapis.com': 'Natural Language AI',
    'translate.googleapis.com': 'Cloud Translation',
    'videointelligence.googleapis.com': 'Video Intelligence',
    'automl.googleapis.com': 'AutoML',
    'documentai.googleapis.com': 'Document AI',
    'discoveryengine.googleapis.com': 'Vertex AI Search',
}


def _load_state():
    try:
        with open(GCP_STATE_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save_state(state):
    os.makedirs(os.path.dirname(GCP_STATE_FILE), exist_ok=True)
    with open(GCP_STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)


def get_gcp_credentials():
    """Load GCP service account credentials."""
    key_path = Config.GCP_SERVICE_ACCOUNT_KEY
    if not key_path or not os.path.exists(key_path):
        return None
    try:
        return service_account.Credentials.from_service_account_file(
            key_path,
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
    except Exception:
        return None


def get_enabled_services(project_id=None):
    """
    Call GCP Service Usage API to get all enabled services.
    Returns list of enabled service names.
    """
    creds = get_gcp_credentials()
    if not creds:
        return None, "GCP credentials not configured"

    project = project_id or Config.GCP_PROJECT_ID
    if not project:
        return None, "GCP project ID not configured"

    try:
        service = build('serviceusage', 'v1', credentials=creds)
        enabled = []
        page_token = None

        while True:
            request = service.services().list(
                parent=f'projects/{project}',
                filter='state:ENABLED',
                pageToken=page_token
            )
            response = request.execute()

            for svc in response.get('services', []):
                name = svc.get('name', '').split('/')[-1]
                enabled.append(name)

            page_token = response.get('nextPageToken')
            if not page_token:
                break

        return enabled, None

    except Exception as e:
        return None, str(e)


def check_for_new_services(session_id=None):
    """
    Compare current enabled GCP services against last known state.
    Returns list of new services detected since last check.
    """
    services, error = get_enabled_services()
    if error or not services:
        return [], error

    state = _load_state()
    known = set(state.get('known_services', []))
    current = set(services)

    # Find newly enabled services
    new_services = current - known

    # Filter to only relevant/interesting APIs
    new_relevant = []
    for svc in new_services:
        if svc in RELEVANT_APIS:
            new_relevant.append({
                'api': svc,
                'name': RELEVANT_APIS[svc],
                'detected_at': datetime.now(timezone.utc).isoformat()
            })

    # Update state
    state['known_services'] = list(current)
    state['last_checked'] = datetime.now(timezone.utc).isoformat()
    state['new_detections'] = state.get('new_detections', []) + new_relevant
    _save_state(state)

    return new_relevant, None


def get_current_stack_from_gcp():
    """
    Get the current GCP tech stack as a clean list of service names.
    Used to populate the tech stack sidebar.
    """
    services, error = get_enabled_services()
    if error or not services:
        return [], error

    stack = []
    for svc in services:
        if svc in RELEVANT_APIS:
            stack.append(RELEVANT_APIS[svc])

    return sorted(stack), None


def get_connection_status():
    """Check if GCP is connected and return status info."""
    creds = get_gcp_credentials()
    if not creds:
        return {
            'connected': False,
            'message': 'No service account key configured'
        }

    project = Config.GCP_PROJECT_ID
    if not project:
        return {
            'connected': False,
            'message': 'No GCP project ID configured'
        }

    state = _load_state()
    last_checked = state.get('last_checked', 'Never')
    known_count = len(state.get('known_services', []))

    return {
        'connected': True,
        'project_id': project,
        'last_checked': last_checked,
        'services_count': known_count,
        'message': f'Connected to {project}'
    }


def get_pending_alerts():
    """
    Get new service detections that haven't been shown to the user yet.
    Returns list of alerts and clears them from state.
    """
    state = _load_state()
    alerts = state.get('new_detections', [])
    if alerts:
        state['new_detections'] = []
        _save_state(state)
    return alerts