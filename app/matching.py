import spacy
from app.models import Startup, Investor
from app.utils import send_notification

nlp = spacy.load("en_core_web_md")

# Industry synonym mapping
INDUSTRY_SYNONYMS = {
    "FinTech": ["financial technology", "payments", "digital finance", "mobile banking"],
    "EdTech": ["education", "e-learning", "learning", "education technology"],
    "AgriTech": ["agriculture", "farming", "agri-business"],
    "HealthTech": ["healthcare", "medical", "health", "telemedicine"],
    "LogisticsTech": ["logistics", "supply chain", "transport", "delivery"],
    "CleanTech": ["clean energy", "green tech", "sustainability"],
}

def expand_industry_keywords(industry):
    expanded = [industry.lower()]
    for key, synonyms in INDUSTRY_SYNONYMS.items():
        if industry.lower() == key.lower():
            expanded.extend([s.lower() for s in synonyms])
    return expanded

def classify_score(score):
    if score >= 90:
        return "Strong Match"
    elif score >= 70:
        return "Good Match"
    elif score >= 50:
        return "Weak Match"
    else:
        return "Unlikely Match"

def match_startups_to_investors():
    startups = Startup.query.all()
    investors = Investor.query.all()
    matches = []

    for startup in startups:
        expanded_startup_industry = " ".join(expand_industry_keywords(startup.industry or ""))
        startup_text = " ".join([
            startup.user.bio or "",
            startup.tech_stack or "",
            expanded_startup_industry,
            startup.competitive_advantage or "",
            startup.pricing_strategy or "",
            startup.revenue_streams or ""
        ])
        doc_startup = nlp(startup_text.lower())

        for investor in investors:
            reasons = []

            expanded_investor_focus = " ".join(expand_industry_keywords(investor.industry_focus or ""))

            funding_ok = True
            if startup.funding_needed:
                if investor.check_size_min and startup.funding_needed < investor.check_size_min:
                    funding_ok = False
                elif investor.check_size_max and startup.funding_needed > investor.check_size_max:
                    funding_ok = False
                else:
                    reasons.append(
                        f"Funding needed (Ksh. {startup.funding_needed:,.0f}) fits investor's range (Ksh. {investor.check_size_min:,.0f} – Ksh. {investor.check_size_max:,.0f})"
                    )


            if not funding_ok:
                continue

            if startup.stage and investor.stage_focus:
                if startup.stage.lower() not in investor.stage_focus.lower():
                    continue
                else:
                    reasons.append(f"Startup stage '{startup.stage}' aligns with investor's focus")

            investor_text = " ".join([
                investor.investment_thesis or "",
                expanded_investor_focus,
                investor.engagement_style or "",
                investor.portfolio or ""
            ])
            doc_investor = nlp(investor_text.lower())

            similarity = doc_startup.similarity(doc_investor)
            score = round(similarity * 100, 2)
            tier = classify_score(score)

            send_notification(startup.user_id, f"You've been matched with investor: {investor.firm_name}!", category='match')
            send_notification(investor.user_id, f"New startup match: {startup.company_name}", category='match')

            matches.append({
                'startup': startup,
                'investor': investor,
                'startup_name': startup.company_name,
                'investor_name': investor.firm_name,
                'score': score,
                'tier': tier,
                'reasons': reasons or ["General similarity based on descriptions."]
            })

    matches.sort(key=lambda m: m['score'], reverse=True)
    return matches

