# SkinPort Skin Tracker
This project was created to assist my friend who wanted to track skin prices in Counter-Strike. A skin is an appearance for a gun in this game. He was interested in volume traded, prices, price history, etc,
and wanted a way to track it easier. This program takes a json file and uses a third-party skin trading website to pull price and sale history data.
Then, it outputs it to my google sheet for easy viewing. This is done through a google service account. There also exists a UI for adding/removing skins for the json file.

---

## Secrets Setup

1. Create file `servicecred.json` and populate the following data within it: 
    ```json
    {
        "type": "",
        "project_id": "",
        "private_key_id": "",
        "private_key": "",
        "client_email": "",
        "client_id": "",
        "auth_uri": "",
        "token_uri": "",
        "auth_provider_x509_cert_url": "",
        "client_x509_cert_url": "",
        "universe_domain": ""
    }
    ```
2. Create second file `skinport_secrets.json` and populate the following data within it:
    ```json
    {
        "client_id": "",
        "client_secret": ""
    }
    ```
3. Populate all `""` with the relevant secrets
