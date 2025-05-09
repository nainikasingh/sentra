
Sentra is an open-source, AI-augmented internal network auditing tool designed to autonomously discover network hosts, identify vulnerabilities, and generate audit-ready reports. 

# Use script.sh to create environment

```
sentra/
├── cli.py
├── config
│   └── settings.py
├── core
│   ├── analyze.py
│   ├── engine
│   │   ├── __init__.py
│   │   ├── nmap_engine.py
│   │   └── scanner_engine.py
│   ├── __init__.py
│   ├── report.py
│   └── scan.py
├── __main__.py
└── plugins
    └── __init__.py
```

# Run cli.py

> Discover self IP address

> Identify CIDR & network range

> Automatically starts searching for live hosts

> Run Nmap scan against live hosts to find active/hidden ports
