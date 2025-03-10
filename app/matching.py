from app.models import Startup, Investor

def match_startups_to_investors():
    matches = []
    startups = Startup.query.all()
    investors = Investor.query.all()

    for startup in startups:
        for investor in investors:
            if (
                startup.industry == investor.industry_focus and
                investor.investment_range_min <= startup.funding_needed <= investor.investment_range_max
            ):
                matches.append((startup, investor))
    
    return matches
