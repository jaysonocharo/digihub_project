import spacy
from app.models import Startup, Investor
from app.utils import send_notification


nlp = spacy.load("en_core_web_md")

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
        startup_text = " ".join([
            startup.tech_stack or "",
            startup.industry or "",
            startup.competitive_advantage or "",
            startup.pricing_strategy or "",
            startup.revenue_streams or ""
        ])
        doc_startup = nlp(startup_text.lower())

        for investor in investors:
            reasons = []

            if startup.industry and investor.industry_focus:
                if startup.industry.lower() != investor.industry_focus.lower():
                    continue
                else:
                    reasons.append(f"Shared industry: {startup.industry}")

            funding_ok = True
            if startup.funding_needed:
                if investor.check_size_min and startup.funding_needed < investor.check_size_min:
                    funding_ok = False
                elif investor.check_size_max and startup.funding_needed > investor.check_size_max:
                    funding_ok = False
                else:
                    reasons.append(f"Funding needed (${startup.funding_needed}) fits investor's range (${investor.check_size_min}–${investor.check_size_max})")

            if not funding_ok:
                continue

            if startup.stage and investor.stage_focus:
                if startup.stage.lower() not in investor.stage_focus.lower():
                    continue
                else:
                    reasons.append(f"Startup stage '{startup.stage}' aligns with investor's focus")

            investor_text = " ".join([
                investor.investment_thesis or "",
                investor.industry_focus or "",
                investor.engagement_style or "",
                investor.portfolio or ""
            ])
            doc_investor = nlp(investor_text.lower())

            similarity = doc_startup.similarity(doc_investor)
            score = round(similarity * 100, 2)
            tier = classify_score(score)

            # Notify both parties of match
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
