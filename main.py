from ai_engine import enrich_lead, generate_email
import cloudscraper
import pandas as pd
import time
from tqdm import tqdm


# API SETUP
BASE_URL = "https://api.startupindia.gov.in/sih/api/noauth/search/profiles"
PROFILE_URL = "https://api.startupindia.gov.in/sih/api/common/replica/user/profile/{}"

scraper = cloudscraper.create_scraper()

payload = {
    "query": "",
    "roles": ["Startup"],
    "page": 0,
    "sort": {"orders": [{"field": "registeredOn", "direction": "DESC"}]},
    "dpiitRecogniseUser": True,
    "internationalUser": False
}

# FETCH
def fetch_profiles(page=0, size=9):
    payload["page"] = page
    res = scraper.post(BASE_URL, params={"size": size}, json=payload)
    try:
        return res.json()
    except:
        return None


def get_all_ids(max_pages=5):
    ids = []
    for page in range(max_pages):
        data = fetch_profiles(page)
        if not data or not data.get("content"):
            break
        ids.extend([x["id"] for x in data["content"]])
        time.sleep(1)
    return ids


def fetch_profile_details(ids):
    profiles = []
    for sid in ids:
        res = scraper.get(PROFILE_URL.format(sid))
        if res.status_code == 200:
            try:
                profiles.append(res.json())
            except:
                pass
        time.sleep(0.5)
    return profiles


# CLEAN + FILTER
def clean_profiles(all_profiles):
    cleaned = []

    for p in all_profiles:
        user = p.get("user", {})
        startup = user.get("startup", {})

        website = startup.get("website")

        # ✅ FILTER: ONLY REAL WEBSITES
        if not website or website.lower() in ["na", "n/a", "none", "", "only mobile app"]:
            continue

        cleaned.append({
            "name": user.get("name"),
            "idea": startup.get("ideaBrief"),
            "website": website
        })

    return pd.DataFrame(cleaned)


# MAIN

if __name__ == "__main__":

    print("Fetching IDs...")
    ids = get_all_ids(max_pages=5)

    print("Fetching profiles...")
    profiles = fetch_profile_details(ids)

    print("Cleaning + filtering...")
    df = clean_profiles(profiles)

    #  RAW CLEAN DATA
    df.to_csv("startup_raw.csv", index=False)

    print(f"Valid startups with website: {len(df)}")


    results = []

    for _, row in tqdm(df.iterrows(), total=len(df), desc="Generating Emails"):
        lead = row.to_dict()

        print(f"\nProcessing: {lead['name']}")

        enrich = enrich_lead(lead)
        lead.update(enrich)

        email_data = generate_email(lead)
        lead.update(email_data)

        results.append({
            "name": lead["name"],
            "idea": lead["idea"],
            "website": lead["website"],
            "generated_email": lead.get("generated_email", "")
        })

        time.sleep(2) 

    #  FINAL OUTPUT
    pd.DataFrame(results).to_csv("generated_outreach.csv", index=False)

    print("DONE ✅")