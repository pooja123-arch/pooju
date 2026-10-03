try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None
from ..config import get_settings
SYSTEM="""You are PocketSmart AI, a practical personal budgeting assistant. Give concise, non-judgmental guidance based only on supplied budget data. Use Indian rupees (₹). Do not claim to be a financial adviser. Do not invent transactions or income."""
def _client():
    key=get_settings().gemini_api_key
    if not key or genai is None:
        return None
    return genai.Client(api_key=key)
def generate_recommendations(c):
    client=_client()
    if not client:return "local",local_recs(c)
    try:
        r=client.models.generate_content(model=get_settings().gemini_model,contents=f"Analyze this budget and return exactly 5 practical recommendations, one per line.\n{c}",config=types.GenerateContentConfig(system_instruction=SYSTEM,temperature=.3))
        lines=[x.strip(" -•\t") for x in (r.text or "").splitlines() if x.strip()]
        if lines:return "gemini",lines[:5]
    except Exception:pass
    return "local",local_recs(c)
def chat(message,c):
    client=_client()
    if not client:return local_chat(message,c),"local"
    try:
        r=client.models.generate_content(model=get_settings().gemini_model,contents=f"Budget data: {c}\nUser question: {message}\nAnswer simply in 3-6 sentences.",config=types.GenerateContentConfig(system_instruction=SYSTEM,temperature=.3))
        if r.text:return r.text.strip(),"gemini"
    except Exception:pass
    return local_chat(message,c),"local"
def local_recs(c):
    income,total,goal,available,cats=c["income"],c["total_expenses"],c["savings_goal"],c["available_after_expenses"],c["category_totals"];o=[]
    if income<=0:o.append("Set your monthly income first so PocketSmart can calculate a meaningful budget.")
    if total>income and income>0:o.append("Your recorded expenses are above income; pause non-essential spending and review the largest category first.")
    elif income>0:o.append(f"Try keeping recorded monthly spending below ₹{income*.7:,.0f} so your savings target has more room.")
    if cats:o.append(f"Review your {next(iter(cats))} spending because it is currently your largest recorded category.")
    if goal and available<goal:o.append(f"Your current gap to the savings goal is about ₹{goal-max(available,0):,.2f}; consider a weekly spending limit to close it.")
    o.append("Track expenses as soon as you spend so the dashboard stays accurate.")
    return o[:5]
def local_chat(message,c):
    m=message.lower()
    if "save" in m or "saving" in m:return f"You currently have ₹{max(c['available_after_expenses'],0):,.2f} left after recorded expenses, against a savings goal of ₹{c['savings_goal']:,.2f}. Consider setting a weekly discretionary limit."
    if "spend" in m or "expense" in m:return f"Your recorded spending is ₹{c['total_expenses']:,.2f}. The largest category is {next(iter(c['category_totals']),'not available')}. Review that category first."
    return f"You have ₹{c['available_after_expenses']:,.2f} after recorded expenses. Your current budget status is {c['budget_status']}."
