import pandas as pd
import json
import os
import re
import glob
from unidecode import unidecode

# =====================================================
# FOLDERS
# =====================================================
INPUT_DIR = "input"
OUTPUT_KW_DIR = "output_kw"
OUTPUT_OCULUS_DIR = "output_oculus"

# =====================================================
# COMMON HELPERS
# =====================================================
def extract_value(x, key):
    try:
        data = json.loads(x)
        if isinstance(data, list) and len(data) > 0:
            return data[0].get(key, "")
        if isinstance(data, dict):
            return data.get(key, "")
    except:
        pass
    return ""


def normalize_text(text):
    if not isinstance(text, str):
        return ""

    text = (
        text.replace("â€™", "'")
            .replace("â€œ", '"')
            .replace("â€�", '"')
            .replace("â€˜", "'")
            .replace("â€“", "-")
            .replace("â€”", "-")
            .replace("Â°", "°")
            .replace("Â", "")
    )

    text = unidecode(text)
    text = re.sub(r"[^A-Za-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def get_amazon_domain(marketplace):
    marketplace_map = {
        "US": "amazon.com",
        "IN": "amazon.in",
        "UK": "amazon.co.uk",
        "DE": "amazon.de",
        "FR": "amazon.fr",
        "IT": "amazon.it",
        "ES": "amazon.es",
        "CA": "amazon.ca",
        "AU": "amazon.com.au",
        "SA": "amazon.sa",
        "EG": "amazon.eg",
        "MX": "amazon.com.mx",
        "AE": "amazon.ae",
        "TR": "amazon.com.tr",
        "PL": "amazon.pl",
        "NL": "amazon.nl",
        "BE": "amazon.com.be",
        "BR": "amazon.com.br",
        "SE": "amazon.se",
        "IE": "amazon.ie" 
    }

    marketplace = str(marketplace).strip().upper()
    if marketplace not in marketplace_map:
        raise ValueError(f"Unsupported marketplace: {marketplace}")

    return marketplace_map[marketplace]


# =====================================================
# KW BATCH LOGIC
# =====================================================
def safe_extract_title(x):
    if not isinstance(x, str):
        return ""

    x = x.strip()
    if x.startswith("[") and "asinProductTitle" in x:
        return extract_value(x, "asinProductTitle")
    return x


def process_kw_file(source_file, marketplace):
    try:
        df = pd.read_csv(source_file, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(source_file, encoding="latin1")

    if "asin_title" in df.columns:
        df["asin_title"] = (
            df["asin_title"]
            .astype(str)
            .apply(safe_extract_title)
            .apply(normalize_text)
        )

    if "asin_image_url" in df.columns:
        df["asin_image_url"] = (
            df["asin_image_url"]
            .astype(str)
            .apply(lambda x: extract_value(x, "asinImageUrl"))
        )

    df = df.replace(r'^\s*$', pd.NA, regex=True)

    # ✅ FIX: Drop ONLY mandatory fields
    df = df.dropna(subset=["asins", "asin_title"])

    df = df.drop_duplicates(subset=["asins"], keep="first")

    domain = get_amazon_domain(marketplace)

    final_df = pd.DataFrame({
        "asin": df["asins"],
        "marketplaceId": marketplace,
        "asinTitle": df["asin_title"],
        "asin_image_url": df.get("asin_image_url", "NA"),
        "contextHelperUrls": df["asins"].apply(
            lambda asin: f"https://www.{domain}/dp/{asin}"
        )
    })

    os.makedirs(os.path.join(OUTPUT_KW_DIR, marketplace), exist_ok=True)

    base_name = os.path.basename(source_file).replace(".csv", "")
    output_file = os.path.join(
        OUTPUT_KW_DIR, marketplace, f"final_asker_{base_name}.csv"
    )

    final_df.to_csv(output_file, index=False, encoding="utf-8")

    # ✅ ONLY OUTPUT (as requested)
    print(f"✅ KW Created: {output_file}")


# =====================================================
# OCULUS BATCH LOGIC
# =====================================================
def process_oculus_file(source_file, marketplace):
    df = pd.read_csv(source_file, encoding="utf-8")

    df = df.replace(r'^\s*$', pd.NA, regex=True)

    # ✅ FIX: Drop ONLY mandatory fields
    df = df.dropna(subset=["target_asin", "title"])

    df = df.drop_duplicates(subset=["target_asin"], keep="first")

    domain = get_amazon_domain(marketplace)

    final_df = pd.DataFrame({
        "asin": df["target_asin"],
        "id": "NA",
        "asinImageUrl": df.get("image_url", "NA"),
        "contextHelperUrls": df["target_asin"].apply(
            lambda asin: f"https://www.{domain}/dp/{asin}"
        ),
        "asinProductTitle": df["title"],
        "asinProductDescription": "NA",
        "imageText": "NA",
        "asinFeatureBullets": "NA",
        "asinBrand": "NA",
        "marketplace": marketplace
    })

    os.makedirs(os.path.join(OUTPUT_OCULUS_DIR, marketplace), exist_ok=True)

    base_name = os.path.basename(source_file).replace(".csv", "")
    output_file = os.path.join(
        OUTPUT_OCULUS_DIR, marketplace, f"final_oculus_{base_name}.csv"
    )

    final_df.to_csv(output_file, index=False, encoding="utf-8")

    # ✅ ONLY OUTPUT
    print(f"✅ Oculus Created: {output_file}")


# =====================================================
# MASTER RUNNER
# =====================================================
def run_automation():
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_KW_DIR, exist_ok=True)
    os.makedirs(OUTPUT_OCULUS_DIR, exist_ok=True)

    files = glob.glob(os.path.join(INPUT_DIR, "*.csv"))
    if not files:
        raise FileNotFoundError("❌ No CSV files found in input folder")

    file_map = {str(i + 1): f for i, f in enumerate(files)}

    print("\nFiles found in input folder:")
    for idx, f in file_map.items():
        print(f"{idx}. {os.path.basename(f)}")

    used_files = set()

    # -----------------------------
    # KW BATCH
    # -----------------------------
    kw_selection = input(
        "\nEnter file numbers for KW batch (comma-separated, or press Enter to skip): "
    ).strip()

    if kw_selection:
        for idx in kw_selection.split(","):
            idx = idx.strip()
            if idx not in file_map or idx in used_files:
                raise ValueError(f"❌ Invalid or duplicate selection: {idx}")

            marketplace = input(
                f"Select marketplace for {os.path.basename(file_map[idx])}: "
            ).strip().upper()

            process_kw_file(file_map[idx], marketplace)
            used_files.add(idx)

    # -----------------------------
    # OCULUS BATCH
    # -----------------------------
    oculus_selection = input(
        "\nEnter file numbers for Oculus batch (comma-separated, or press Enter to skip): "
    ).strip()

    if oculus_selection:
        for idx in oculus_selection.split(","):
            idx = idx.strip()
            if idx not in file_map or idx in used_files:
                raise ValueError(f"❌ Invalid or duplicate selection: {idx}")

            marketplace = input(
                f"Select marketplace for {os.path.basename(file_map[idx])}: "
            ).strip().upper()

            process_oculus_file(file_map[idx], marketplace)
            used_files.add(idx)

    print("\n🎉 All selected files processed successfully")


# =====================================================
if __name__ == "__main__":
    run_automation()

