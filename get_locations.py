import requests
import pandas as pd
from datetime import datetime

# Variables
refresh_token = "your_refresh_token"  # <-- replace with your refresh token
refresh_url = "https://manage-api-v1.cloudi-fi.net/auth/refresh"
locations_url = "https://manage-api-v1.cloudi-fi.net/locations"

# Full list of fields to exclude
excluded_fields = {
    'admin', 'parent', 'bandwidthIn', 'bandwidthOut', 'lastAccessAt', 'firstSeenAt',
    'createdAt', 'updatedAt', 'deletedAt', 'config', 'createdByMember', 'updatedByMember',
    'externalActivations', 'groups', 'teams', 'coordinates', 'addressCountry', 'postOfficeBoxNumber',
    'alias', 'lang', 'template', 'aup', 'redirect', 'timezone', 'country', '@id', '@type',
    'data_fields_bounds_east', 'data_fields_bounds_west', 'data_fields_bounds_north', 'data_fields_bounds_south',
    'metadata_fields_bounds_source_input', 'metadata_fields_bounds_source_process', 'metadata_fields_bounds_createdAt',
    'metadata_fields_timezone_source_input', 'metadata_fields_timezone_source_process', 'metadata_fields_timezone_createdAt',
    'metadata_fields_coordinates_source_input', 'metadata_fields_coordinates_source_process', 'metadata_fields_coordinates_createdAt',
    'metadata_processes_geocoding_input', 'metadata_processes_geocoding_output', 'metadata_processes_geocoding_checksum',
    'metadata_processes_geocoding_lastRunAt', 'features_captivePortal_enabled', 'features_captivePortal_firstAccess',
    'features_captivePortal_lastAccess', 'features_iot_enabled', 'features_iot_firstAccess', 'features_iot_lastAccess',
    'data_fields_aps', 'metadata_fields_aps_source_input', 'metadata_fields_aps_source_process', 'metadata_fields_aps_createdAt',
    'metadata_fields_postalCode_source_input', 'metadata_fields_postalCode_source_process', 'metadata_fields_postalCode_createdAt',
    'metadata_fields_streetAddress_source_input', 'metadata_fields_streetAddress_source_process', 'metadata_fields_streetAddress_createdAt',
    'metadata_fields_addressLocality_source_input', 'metadata_fields_addressLocality_source_process', 'metadata_fields_addressLocality_createdAt',
    'metadata_processes_vendor', 'metadata_processes_access_point_input', 'metadata_processes_access_point_output',
    'metadata_processes_access_point_checksum', 'metadata_processes_access_point_lastRunAt', 'metadata_processes_reverse_geocoding_input',
    'metadata_processes_reverse_geocoding_output', 'metadata_processes_reverse_geocoding_checksum', 'metadata_processes_reverse_geocoding_lastRunAt',
    'metadata_fields_region_source_input', 'metadata_fields_region_source_process', 'metadata_fields_region_createdAt',
    'metadata_processes_machine_learning_input', 'metadata_processes_machine_learning_output', 'metadata_processes_machine_learning_checksum',
    'metadata_processes_machine_learning_lastRunAt', 'data', 'metadata', 'identifiers', 'syncStatus', 'features'
}

# Step 1: Refresh the token
refresh_payload = {"refresh_token": refresh_token}
refresh_headers = {"Content-Type": "application/json"}

response = requests.post(refresh_url, json=refresh_payload, headers=refresh_headers)
response.raise_for_status()

bearer_token = response.json()["token"]

# Step 2: Get locations
locations_headers = {"Authorization": f"Bearer {bearer_token}"}

locations_response = requests.get(locations_url, headers=locations_headers)
locations_response.raise_for_status()

locations_data = locations_response.json()

# Step 3: Extract 'hydra:member'
locations_list = locations_data.get("hydra:member", [])

# Step 4: Prepare final records
final_records = []
summary_records = []

for location in locations_list:
    # Remove excluded fields
    cleaned_location = {k: v for k, v in location.items() if k not in excluded_fields}

    identifiers = location.get("identifiers", [])

    # Add only key and alias for each identifier
    for idx, identifier in enumerate(identifiers, start=1):
        cleaned_location[f"identifier_{idx}_key"] = identifier.get("key")
        cleaned_location[f"identifier_{idx}_alias"] = identifier.get("alias")

    final_records.append(cleaned_location)

    # Prepare summary info
    summary_records.append({
        "Location ID": location.get("id"),
        "Location Name": location.get("name"),
        "Nombre d'APs": len(identifiers)
    })

# Step 5: Create DataFrames
df_locations = pd.DataFrame(final_records)
df_summary = pd.DataFrame(summary_records)

# Step 6: Save both sheets into one Excel
today_fr = datetime.now().strftime("%d-%m-%Y")  # French date format
output_file = f"locations_with_identifiers_{today_fr}.xlsx"

with pd.ExcelWriter(output_file) as writer:
    df_locations.to_excel(writer, sheet_name=f"Locations{today_fr}", index=False)
    df_summary.to_excel(writer, sheet_name=f"Nbre_APs_{today_fr}", index=False)

print(f"✅ Exported {len(df_locations)} locations to {output_file} with two sheets (locations + nombre de APs).")