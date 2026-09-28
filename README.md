# Naike LinkedIn Operations Skill

A reusable Codex skill for planning, preparing, validating, publishing, and learning from Naike Group Co., Ltd. LinkedIn company-page posts.

## What It Covers

- A varied weekly editorial mix spanning real company moments, factory and quality proof, buyer education, product customization, compliance, and company culture.
- Fresh English B2B copy with a clear buyer benefit, readable spacing, light emoji, relevant keywords, hashtags, and configured contact details.
- Generated 3-4 image creative-drinkware carousels by default; real-media selection for authentic company, factory, employee, QC, certificate, and shipment themes; image-quality and content-credential rules.
- Chrome-based LinkedIn company-page publishing, post verification, one-retry failure handling, dated packages and logs, and low-reach amplification materials.
- A package validator and a Git hook that pushes committed skill improvements to the configured GitHub repository.

## Install

Copy this directory to your Codex skills folder as `naike-linkedin-post`, or use the skill directly from the repository checkout. Codex discovers the skill through `SKILL.md`.

## Run

Invoke `$naike-linkedin-post` when preparing or publishing a Naike LinkedIn post. Publishing uses the signed-in Chrome session and the company-page admin composer. Follow the workflow's action-time checks for public posts and comments.

Validate a package with:

```powershell
python .\scripts\validate_package.py --package .\outputs\linkedin_post_YYYY-MM-DD_package.md --images .\image1.png .\image2.png .\image3.png
```

## Profile

Brand, products, contacts, copy rules, and image constraints are in [`references/naike-requirements.md`](references/naike-requirements.md). Edit that profile when the user changes these facts, then record the update in [`CHANGELOG.md`](CHANGELOG.md).

## Automatic GitHub Updates

The installed skill checkout is the source of truth. After reviewing a skill improvement, commit it; the configured Git `post-commit` hook pushes that commit to `origin` automatically. Confirm the push result before reporting the remote as updated.

The public repository must contain reusable skill instructions and generic tooling only. Do not commit dated post packages, publish logs, screenshots, private images, browser data, credentials, or customer lead data.
