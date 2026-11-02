Security Policy

Supported Versions

Security updates are provided only for the current development baseline and the most recent stable release.

Version / branch

Supported

main

✅ Yes

Latest production-stable-* tag

✅ Yes

Latest stable web release/tag

✅ Yes, when applicable

Older production-stable-* tags

❌ No

deploy-* candidate tags

❌ No

Feature branches (feat/*, fix/*, perf/*)

❌ No

Evaluation / experiment branches (eval/*)

❌ No

At present, the project uses dated deployment and stable tags rather than semantic version numbers.

Only the most recent stable version should be considered supported for security fixes. Older releases are retained for reproducibility and rollback purposes, but they do not receive security updates.

When formal versioned releases are introduced, this table will be updated to list the supported release series explicitly.

Reporting a Vulnerability

Please do not disclose suspected security vulnerabilities in a public issue, discussion, pull request, or other public channel.

Report vulnerabilities privately to the repository maintainer using GitHub's private vulnerability reporting feature, if enabled for this repository.

If private vulnerability reporting is not available, contact the maintainer privately through an appropriate contact method listed on the repository or maintainer profile.

Please include, where possible:

a description of the vulnerability;

affected component or version;

steps to reproduce;

expected impact;

proof-of-concept details, if safe to provide;

any suggested mitigation.

Do not include real credentials, API keys, private intelligence data, or other sensitive information in a report.

Scope

Security reports are particularly useful for issues involving:

unauthorized modification of intelligence data;

bypass of read-only protections;

unsafe API or web endpoints;

authentication or authorization failures;

exposure of private configuration, credentials, or API keys;

path traversal or unintended file access;

command or code execution;

unsafe ingestion of externally supplied content;

dependency vulnerabilities with a demonstrated impact on this project;

leakage of local or user-specific state;

vulnerabilities in deployment, supervisor, or operational tooling.

Problems involving data quality, clustering accuracy, entity resolution, geolocation accuracy, or intelligence-analysis correctness should generally be reported as normal software defects rather than security vulnerabilities unless they create a concrete security impact.

Response Process

After receiving a valid security report, the maintainer will aim to:

confirm receipt of the report;

reproduce and assess the issue;

determine affected supported versions;

prepare and test a fix;

release the fix to the currently supported version;

disclose the issue publicly when it is safe and appropriate to do so.

No specific response or remediation timeline is guaranteed.

Operational Security

This project may integrate external data sources, APIs, local databases, model files, and optional credentials.

Users should:

keep API keys and credentials outside the repository;

avoid committing .env files, tokens, secrets, or private data;

restrict production-local web interfaces to trusted networks or localhost unless appropriate authentication and authorization are added;

keep dependencies and the host operating system updated;

use the latest supported stable version;

review configuration before enabling collectors or integrations that communicate with third-party services.

Historical Releases

Historical tags, evaluation snapshots, deployment candidates, and rollback artifacts may remain available for reproducibility.

Their presence in the repository does not mean they are actively maintained or supported for security updates.
