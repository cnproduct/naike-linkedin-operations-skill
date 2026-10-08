#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REQUIRED_SNIPPETS = [
    "Keywords:",
]

BANNED_TERMS = [
    "leverage",
    "utilize",
    "streamline",
    "robust",
    "seamless",
    "unlock",
    "game-changer",
    "deep dive",
    "in today's fast-paced world",
]


def extract_post(markdown: str) -> str:
    marker = "## LinkedIn Post"
    if marker not in markdown:
        raise ValueError('package missing "## LinkedIn Post" section')
    text = markdown.split(marker, 1)[1]
    for stop in ["## Copy Check", "## Image", "## Images", "## Assets", "## Publish"]:
        if stop in text:
            text = text.split(stop, 1)[0]
    return text.strip()


def count_english_chars(text: str) -> int:
    # Match the project convention: Python len() on the final post text.
    return len(text)


def validate(package: Path, images: list[Path], user_supplied_image_count: bool = False) -> dict:
    if not package.exists():
        raise ValueError(f"package does not exist: {package}")
    markdown = package.read_text(encoding="utf-8")
    post = extract_post(markdown)
    char_count = count_english_chars(post)
    errors = []

    if post.upper().startswith("DO YOU WANT") and "do you want" in markdown.lower():
        # The hook is allowed occasionally, but the newer Naike guidance no longer requires it.
        pass
    if not (300 <= char_count <= 1200):
        errors.append(f"post must be 300-1200 characters; got {char_count}")
    if char_count < 650 and not post.upper().startswith("DO YOU WANT"):
        errors.append(f"non-sourcing-hook posts should usually be 650+ characters; got {char_count}")
    lowered = post.lower()
    if re.search(r"https?://|www\.|[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|\+?\d[\d ()-]{7,}\d", post, re.IGNORECASE):
        errors.append("post body must not include external URLs or contact details")
    for term in BANNED_TERMS:
        if term in lowered:
            errors.append(f"banned AI-style filler term found: {term}")
    if any(mark in post for mark in ["—", "–", "--"]):
        errors.append("post must not contain em dash, en dash, or double dash")
    for snippet in REQUIRED_SNIPPETS:
        if snippet not in post:
            errors.append(f"missing required snippet: {snippet}")

    hashtags = re.findall(r"(?<!\\w)#[-A-Za-z0-9_]+", post)
    if not (5 <= len(hashtags) <= 8):
        errors.append(f"post must include 5-8 hashtags; got {len(hashtags)}")

    allowed_image_count = 1 <= len(images) <= 4 if user_supplied_image_count else 3 <= len(images) <= 4
    if not allowed_image_count:
        expected = "1-4 user-supplied images" if user_supplied_image_count else "3-4 images"
        errors.append(f"must attach {expected}; got {len(images)}")
    for image in images:
        if not image.exists():
            errors.append(f"image does not exist: {image}")
        elif image.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
            errors.append(f"unsupported image extension: {image}")

    return {
        "ok": not errors,
        "errors": errors,
        "package": str(package),
        "post_character_count": char_count,
        "hashtags": hashtags,
        "image_count": len(images),
        "images": [str(image) for image in images],
        "post_preview": post[:180],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", required=True, type=Path)
    parser.add_argument("--images", nargs="+", required=True, type=Path)
    parser.add_argument(
        "--user-supplied-image-count",
        action="store_true",
        help="Allow 1-4 images when the user explicitly supplies the image set or count.",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        result = validate(args.package, args.images, args.user_supplied_image_count)
    except Exception as exc:
        result = {"ok": False, "errors": [str(exc)]}

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("OK" if result["ok"] else "FAILED")
        for error in result.get("errors", []):
            print(f"- {error}")
        print(json.dumps({k: v for k, v in result.items() if k != "errors"}, ensure_ascii=False, indent=2))

    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
