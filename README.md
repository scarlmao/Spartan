# 🛡️ spartan

An advanced OSINT Discord bot designed for intelligence gathering across multiple queries such as emails, usernames, IPs, domains, and legal records.

## ✨ Features

* **Email Intelligence:** Scan breach databases and social presence.
* **User Recon:** Track usernames across 35+ social media platforms.
* **Network OSINT:** Detailed IP, WhoisXML, and site lookups.
* **Security Tools:** VirusTotal hash analysis for malware intelligence.
* **Legal & Geo:** Search court records via CourtListener and geolocate images using AI.
* **Discord Lookup:** ID-based user tracking and scammer database checks.

## 🛠️ Installation

### Prerequisites

* Python 3.8+
* A Discord Bot Token (via [Discord Developer Portal](https://discord.com/developers/applications))
* API Keys for: Hunter.io, VirusTotal, WhoisXML, CourtListener, and Picarta.

### Steps

1. **Clone the repository:**
```bash
git clone https://github.com/scarlmao/spartan.git
cd spartan

```


2. **Install dependencies:**
```bash
pip install -r requirements.txt

```


3. **Configuration:**
* Open `config.json` in the root directory.
* Place your api keys inside of it:


```json
{
  "token": "YOUR_DISCORD_BOT_TOKEN", https://discord.com/developers/home
  "hunter_api": "YOUR_KEY", https://hunter.io/
  "virustotal_api": "YOUR_KEY", https://www.virustotal.com/gui/
  "whoisxml_api": "YOUR_KEY", https://www.whoisxmlapi.com/
  "courtlistener_api": "YOUR_KEY", https://www.courtlistener.com/
  "picarta_api": "YOUR_KEY" https://picarta.ai/
}

```


4. **Launch the bot:**
```bash
python main.py

```



## 🚀 Commands

| Command | Description |
| --- | --- |
| `!email <email>` | Scans for breaches and social media accounts linked to an email. |
| `!user <username>` | Checks for the existence of a username across 35+ sites. |
| `!geo` | Localizes an attached image using AI (Picarta integration). |
| `!dlookup <id>` | Performs a Discord ID lookup for scammer status and data leaks. |
| `!vt <hash>` | Queries VirusTotal for file analysis and malicious reports. |
| `!court <name>` | Searches for legal case history and court records. |

## 🤝 Contributing

Contributions help make Spartan better!

1. Fork the Project.
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the Branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

Small contributions are more imporant then large contributions !

## 📜 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.
(AI was used for debugging this project)
---
