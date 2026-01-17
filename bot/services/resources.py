RESOURCES = [
    "OWASP Top 10 + ASVS: https://owasp.org",
    "PortSwigger Web Security Academy: https://portswigger.net/web-security",
    "Hacking APIs: https://github.com/hapi-dev/awesome-api-security",
    "Red Team Ops primer: https://redteam.guide",
    "Blue Team playbooks: https://www.sans.org/white-papers/",
]

LAB_GUIDE = [
    "Use isolated VMs (VirtualBox/VMware) with Kali + Ubuntu.",
    "Deliberate targets: OWASP Juice Shop, DVWA, Metasploitable2.",
    "Never test on production or unauthorized networks.",
    "Capture traffic with Burp/ZAP; document every step.",
]

CTF_TIPS = [
    "Read challenge scope carefully; no real-world collateral.",
    "Automate carefully; avoid DoS. Keep notes and payloads.",
    "Practice common categories: web, crypto, pwn, forensics.",
    "Use checklists for recon, exploitation, and cleanup.",
]

DISCLOSURE_TEMPLATE = """\
Responsible Disclosure Template:
- Summary: Briefly describe the issue and impact.
- Scope: Affected systems/URLs.
- Steps to Reproduce: Numbered steps with minimal PoC.
- Expected vs Actual: Clarify the vulnerability.
- Fix Suggestion: Safe remediation ideas.
- Contact: How to reach you for follow-up.
Always obtain authorization and follow local laws."""

GLOSSARY = [
    "XSS: Injecting script into a trusted site to run in another user's browser.",
    "CSRF: Forging a user's request by abusing their session.",
    "SSRF: Forcing a server to make requests it shouldn't.",
    "RCE: Remote Code Execution vulnerability.",
    "LFI/RFI: Local/Remote File Inclusion to read/execute unintended files.",
]

ATTACKS = [
    "Phishing: social engineering to steal credentials—defend with MFA and FIDO keys.",
    "Credential stuffing: reused passwords; defend with rate limits and breach checks.",
    "SQLi: unsanitized input; defend with parameterized queries and least privilege.",
    "Command injection: untrusted shell input; defend with allowlists and escaping.",
    "Privilege escalation: misconfigurations and weak boundaries; defend with hardening + audits.",
]

TOOLS = [
    "Nmap: network scanning; use only in authorized scopes.",
    "Burp Suite / ZAP: web proxy for testing apps.",
    "Metasploit: exploit framework; best used in labs/CTFs.",
    "Responder/Impacket: protocol testing; lab-focused only.",
    "Wireshark/tcpdump: packet analysis for incident response.",
]
