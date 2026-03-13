# Korean Kubestronaut Tracker

Track Korean Kubstronauts and celebrate new ones for [CNCK (Cloud Native Community Korea)](https://community.cncf.io/cloud-native-community-korea/).

## What is a Kubestronaut?

A [**Kubestronaut**](https://www.cncf.io/training/kubestronaut/) is someone who has earned all five CNCF Kubernetes certifications:

- [**CKA**](https://training.linuxfoundation.org/certification/certified-kubernetes-administrator-cka/) — Certified Kubernetes Administrator
- [**CKAD**](https://training.linuxfoundation.org/certification/certified-kubernetes-application-developer-ckad/) — Certified Kubernetes Application Developer
- [**CKS**](https://training.linuxfoundation.org/certification/certified-kubernetes-security-specialist/) — Certified Kubernetes Security Specialist
- [**KCNA**](https://training.linuxfoundation.org/certification/kubernetes-cloud-native-associate/) — Kubernetes and Cloud Native Associate
- [**KCSA**](https://training.linuxfoundation.org/certification/kubernetes-and-cloud-native-security-associate-kcsa/) — Kubernetes and Cloud Native Security Associate

A **Golden Kubestronaut** has achieved all five certifications *and* renewed them, demonstrating ongoing commitment to the Kubernetes ecosystem.

## How It Works

1. Fetches the Korean Kubestronaut list from the [CNCF website](https://www.cncf.io/training/kubestronaut/?_sft_lf-country=kr) via their AJAX API
2. Saves the current list as `data/this-week-kr-kubestronaut.json` (previous week's data is rotated to `last-week-kr-kubestronaut.json`)
3. Computes the diff to find new members and saves them to `data/new-kubestronaut.json`

## Project Structure

```
kr-kubestronaut-tracker/
├── fetch.py                  # Main script — fetch, compare, and save
├── pyproject.toml            # Project metadata and dependencies
├── uv.lock                   # Locked dependency versions
├── data/
│   ├── this-week-kr-kubestronaut.json   # Current week's full list
│   ├── last-week-kr-kubestronaut.json   # Previous week's full list
│   └── new-kubestronaut.json            # Newly added Kubstronauts
└── README.md
```

## Usage

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

### Run

```bash
uv run python fetch.py
```

Example output:

```
Fetching Korean Kubstronauts from CNCF...
  Page 1: 10 people
  Page 2: 10 people
  ...
  Page 13: 0 people (done)

Total: 119 kubstronauts fetched

Saved: data/this-week-kr-kubestronaut.json

📋 New Kubstronauts (compared to last week): 2
  1. Hong Gildong (ExampleCorp)
  2. Kim Cheolsu (CloudInc)

Saved: data/new-kubestronaut.json
```

## Data Format

Each JSON file follows this schema:

```json
{
  "fetched_at": "2026-03-13T22:52:22.688334+09:00",
  "total": 119,
  "kubstronauts": [
    {
      "name": "Seoyul Yoon",
      "company": "SK AX",
      "golden": false,
      "linkedin": "https://www.linkedin.com/in/yoon-seoyul/",
      "github": "https://github.com/Seo-yul"
    }
  ]
}
```

| Field      | Type          | Description                                  |
|------------|---------------|----------------------------------------------|
| `name`     | string        | Full name                                    |
| `company`  | string        | Company or organization                      |
| `golden`   | boolean       | Whether the person is a Golden Kubestronaut  |
| `linkedin` | string / null | LinkedIn profile URL                         |
| `github`   | string / null | GitHub profile URL                           |

## Weekly Workflow

Run every **Tuesday (KST)**:

1. Run `uv run python fetch.py`
2. Check `data/new-kubestronaut.json` for newly added members
3. Celebrate new Kubstronauts in the CNCK community!
