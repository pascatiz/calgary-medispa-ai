#!/usr/bin/env python3
"""
Calgary MediSpa AI - Marketing Content Pipeline
Generates a 7-day social media content calendar.
"""

import click
from datetime import datetime, timedelta
from pathlib import Path


CONTENT_CALENDAR = [
    {
        "day": 1, "theme": "Botox Education", "service": "Botox / Neuromodulators",
        "platforms": ["Instagram", "Facebook"],
        "caption": "Did you know? Botox is one of the most studied cosmetic treatments. At Calgary MediSpa, every treatment is performed by our physician-led team for safe, natural-looking results. Book your complimentary consultation today.",
        "cta": "Book your free consultation — link in bio.",
        "image_idea": "Close-up of smooth forehead skin, soft lighting, clean white aesthetic",
        "hashtags": "#Calgary #Botox #CalgaryMediSpa #PhysicianLed #AntiAging",
    },
    {
        "day": 2, "theme": "Filler Results Trust", "service": "Dermal Fillers",
        "platforms": ["Instagram", "TikTok"],
        "caption": "Natural lip enhancement is an art. Our injectors specialize in subtle, balanced results that enhance YOUR features — not change them. Physician oversight on every treatment.",
        "cta": "See our gallery. DM us to book.",
        "image_idea": "Side-by-side lip before/after, bright clinical lighting",
        "hashtags": "#LipFiller #CalgaryFillers #NaturalResults #MediSpa",
    },
    {
        "day": 3, "theme": "Weight Loss Program", "service": "Medical Weight Loss",
        "platforms": ["Facebook", "Instagram"],
        "caption": "Struggling with weight loss? Our physician-supervised program uses the latest evidence-based treatments. No fad diets. Just real medical support.",
        "cta": "Book a weight loss consultation — call or book online.",
        "image_idea": "Active lifestyle image, energetic and positive tone",
        "hashtags": "#WeightLoss #MedicalWeightLoss #Calgary #HealthyLiving",
    },
    {
        "day": 4, "theme": "Skin Care Science", "service": "Skin Care / Facials",
        "platforms": ["Instagram", "Pinterest"],
        "caption": "Great skin is a long game. Our medical-grade skin care treatments are designed for lasting results. Ask us about personalized skin care plans starting at your first consultation.",
        "cta": "Book a skin care assessment. Link in bio.",
        "image_idea": "Glowing, hydrated skin with serums, soft cream tones",
        "hashtags": "#SkinCare #MedicalFacial #CalgaryGlow #GlowingSkin",
    },
    {
        "day": 5, "theme": "Physician-Led Trust", "service": "Brand / About Us",
        "platforms": ["Instagram", "Facebook", "LinkedIn"],
        "caption": "Why choose Calgary MediSpa? Every treatment plan is designed and overseen by our medical team. We believe aesthetic medicine should be safe, ethical, and evidence-based.",
        "cta": "Learn about our team. Link in bio.",
        "image_idea": "Physician in clinic, professional and approachable, white coat",
        "hashtags": "#PhysicianLed #MedicalAesthetics #CalgaryMediSpa #SafeAesthetics",
    },
    {
        "day": 6, "theme": "FAQ / Myth Busting", "service": "Education / All Services",
        "platforms": ["Instagram Stories", "TikTok", "Facebook"],
        "caption": "MYTH: Botox makes you look frozen. FACT: Done correctly, Botox results look completely natural. The key is a skilled injector who understands facial balance. Questions? Ask us anything.",
        "cta": "Drop your questions in the comments.",
        "image_idea": "MYTH vs FACT carousel, bold clean typography",
        "hashtags": "#BotoxMyths #CalgaryBotox #AestheticsFacts #MediSpaEducation",
    },
    {
        "day": 7, "theme": "Weekend Promo", "service": "Promotional",
        "platforms": ["Instagram", "Facebook", "Email"],
        "caption": "This week only: Book any treatment and receive a complimentary skin analysis with our aesthetician. Limited spots available. Calgary MediSpa — where medicine meets beauty.",
        "cta": "Call us or book online. Offer expires Sunday.",
        "image_idea": "Bold promo graphic with clinic colors, clear offer text",
        "hashtags": "#CalgaryMediSpaPromo #CalgaryDeal #AestheticsOffer",
    },
]


def generate_calendar(start_date=None):
    if start_date is None:
        start_date = datetime.now()
    elif isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines_out = [
        "# 7-Day Social Media Content Calendar",
        f"**Clinic:** Calgary MediSpa",
        f"**Generated:** {generated_at}",
        f"**Week Starting:** {start_date.strftime('%B %d, %Y')}",
        "", "---", "", "## Overview", "",
        "| Day | Date | Theme | Service | Platforms |",
        "|---|---|---|---|---|",
    ]
    for post in CONTENT_CALENDAR:
        post_date = start_date + timedelta(days=post["day"] - 1)
        platforms = ", ".join(post["platforms"])
        lines_out.append(f"| Day {post['day']} | {post_date.strftime('%b %d')} | {post['theme']} | {post['service']} | {platforms} |")
    lines_out.extend(["", "---", ""])
    for post in CONTENT_CALENDAR:
        post_date = start_date + timedelta(days=post["day"] - 1)
        platforms = ", ".join(post["platforms"])
        lines_out.extend([
            f"## Day {post['day']} -- {post_date.strftime('%A, %B %d')}",
            f"**Theme:** {post['theme']}",
            f"**Service:** {post['service']}",
            f"**Platforms:** {platforms}",
            "", "### Caption",
            f"> {post['caption']}",
            "", f"**CTA:** {post['cta']}",
            "", f"**Image Idea:** {post['image_idea']}",
            "", f"**Hashtags:** {post['hashtags']}",
            "", "---", "",
        ])
    lines_out.extend([
        "## Usage Notes",
        "- Customize captions to match current promotions",
        "- Always add your clinic location tag (Calgary, AB)",
        "- Schedule posts using Buffer, Hootsuite, or Later",
        "- Respond to all comments within 24 hours",
        "- Comply with provincial advertising guidelines for medical treatments",
        "", "*Generated by Calgary MediSpa AI Marketing Pipeline*",
    ])
    return "\n".join(lines_out)


def run(safe_save):
    click.echo("\n  MARKETING CONTENT PIPELINE")
    click.echo("  Generate a 7-day social media content calendar.\n")
    start_date_str = input("  Start date (YYYY-MM-DD) or Enter for today: ").strip()
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d") if start_date_str else datetime.now()
    except ValueError:
        click.echo("  Invalid date format. Using today.")
        start_date = datetime.now()
    click.echo(f"  Generating calendar from {start_date.strftime('%B %d, %Y')}...")
    calendar = generate_calendar(start_date)
    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = Path("outputs") / f"Content_Calendar_{date_str}.md"
    saved = safe_save(filepath, calendar)
    if saved:
        click.echo(f"\n  Content calendar saved: {filepath}")
        click.echo("  7 posts ready. Customize captions before publishing.")


if __name__ == "__main__":
    def _save(path, content):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        print(f"Saved: {path}")
        return True
    run(_save)
