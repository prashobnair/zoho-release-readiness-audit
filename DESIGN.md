# Release review and rollback

## Change classification

Add/change/remove is determined by stable kind/name identity. A removed component always needs explicit review. Changes to workflow, validation, function or webhook carry a behavior-review finding even if dependencies are intact. Missing dependencies are listed by component and reference. The tool does not select an application order or automatically block a deploy; `ready_for_release` means only that these narrow findings are absent.

## Release checklist

1. Confirm the source sandbox, target production organization, admin permissions and documented change window.
2. Export and verify current target configuration, dependencies, custom fields, layouts, validation/workflow rules, Deluge functions and webhook mappings. The real extraction format must be mapped separately.
3. Diff manifests; investigate all removals, behavior changes and missing references. Review API/HTTP payload-to-field mappings, data types and role permissions manually.
4. Run sandbox tests on good/bad records, workflow triggers, retries, notifications and external integrations. Record expected outputs and test evidence.
5. Approve a migration sequence, backup and *tested* rollback/deactivation plan; name owners for go/no-go and monitoring. Do not treat a rollback as simply deleting changed fields.
6. Deploy through the platform's supported path, verify post-release behavior, and log deviations. This repository performs none of these steps.

## Tests and known gaps

Six tests cover the bad fixture, no-op pass, unknown dependency, duplicate key, deterministic fingerprint and new workflow review. It cannot parse actual Zoho exports or Deluge, detect semantic changes under the same metadata, validate API payloads, order dependencies, or prove rollback. No production deployment is authorized or implemented.
