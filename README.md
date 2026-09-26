# Zoho Release Readiness Audit

An offline comparison of **fictional** CRM configuration manifests before and after a proposed release. It lists added, removed and changed components, flags broken dependencies and prompts review of workflow, validation, function and webhook changes. It prints a target-manifest fingerprint for evidence. It does not fetch Zoho metadata, run Deluge, deploy config or claim a release is safe.

## Contract use-case

A [Zoho CRM migration consultant contract posting](https://www.linkedin.com/posts/hari-prasad-palana-8b9a53291_zohocrm-zohodeveloper-deluge-activity-7458417036126359552-oIc4) called for reviewing sandbox fields, layouts, workflows, validation dependencies, Deluge functions, API mappings, testing and rollback. The [Zoho CRM Upwork board](https://www.upwork.com/freelance-jobs/zoho-crm/) also samples troubleshooting requests. The LinkedIn posting was dated May 8, 2026 and is not asserted to be open now. This repo illustrates a change-review slice, not work for either poster.

## Run

Python 3.10+ and standard library only. From the repository root:

```sh
python3 cli.py examples.json
python3 cli.py examples.json --strict  # exit code 2 on review findings
python3 -m unittest discover -p 'test_*.py' -v
```

No Zoho trial, API key, Docker, browser or paid plan is needed. The fictional bad fixture removes `Deal.External_Ref`, disables its validation and changes a function version while layout/function still depend on the removed field. Output includes `removal_review`, `behavior_regression_review`, `missing_dependency`, `ready_for_release: false` and `deployment_actions: 0`. Comparing a manifest to itself passes these *narrow* checks. `DESIGN.md` describes review and rollback.

## Manifest contract

Each list has components with unique `(kind, name)`, where kind is `field`, `layout`, `workflow`, `validation`, `function` or `webhook`. `depends_on` is a list of strings like `field:Deal.External_Ref`. The diff compares JSON component values, flags behavioral types and checks references against the target manifest. A SHA-256 of the target list is produced for repeatability, not authenticity or approval. This is a **fictional intermediate model**, not a Zoho CRM sandbox export schema or API payload.

## Boundary

A clean report does not prove production readiness: it misses runtime behavior, permissions, test coverage, ordering, hidden vendor dependencies, performance and deployment history. Before touching a tenant, inspect current Zoho docs and metadata, verify the correct sandbox/production organization, run regression tests and secure a human-reviewed sequence, backup and rollback. Never put client configuration or secrets in this repo.
