import streamlit as st
import pandas as pd
import math
import html
import io
from datetime import date, datetime

# ============================================================
# BIKE FINANCE PRO • PROFESSIONAL STREAMLIT EDITION
# ============================================================
# Customer-ready bike finance calculator.
#
# Main calculation structure from the supplied HTML version:
#   Maximum base finance = 60% of bike value
#   Base lease            = up to 40% of bike value
#   Base loan             = remaining amount up to 60%
#   Lease charges         = Rs. 9,500 document charge
#                          + 3% commission of bike value
#                          + insurance
#   Lease rate            = 26% p.a. reducing balance
#   Loan rate             = 28% p.a. reducing balance
#   Loan period           = lease period - 1 year
#
# This version adds:
#   • polished responsive UI
#   • separate lease and loan payment plans
#   • principal / interest / balance schedules
#   • customer-facing quotation
#   • downloadable CSV schedules
#   • quotation number and customer details
#   • validation and finance-limit checks
#   • compact mobile-friendly sections
# ============================================================

st.set_page_config(
    page_title="Bike Finance Pro",
    page_icon="🏍️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# GLOBAL STYLE
# ============================================================

st.markdown(
    """
<style>
:root { color-scheme: light; }
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

:root {
    --navy:#07111f;
    --navy2:#102b45;
    --green:#12a66a;
    --green2:#087748;
    --green3:#dff8eb;
    --blue:#2563eb;
    --blue2:#eaf1ff;
    --ink:#101828;
    --muted:#667085;
    --line:#e5eaf0;
    --white:#ffffff;
    --bg:#f3f7fa;
    --danger:#b42318;
    --warning:#b54708;
    --shadow:0 18px 50px rgba(7,17,31,.10);
}

html, body, [class*="css"] {
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
                 "Segoe UI", sans-serif;
}

.stApp {
    background:
      radial-gradient(900px 520px at 0% -10%, rgba(18,166,106,.14), transparent 60%),
      radial-gradient(800px 500px at 105% 5%, rgba(37,99,235,.11), transparent 62%),
      linear-gradient(145deg,#edf4f7,#fbfcfe 58%,#f1f7f3);
}

.stApp:before {
    content:"";
    position:fixed;
    inset:0;
    pointer-events:none;
    opacity:.25;
    background-image:radial-gradient(rgba(7,17,31,.08) .65px, transparent .65px);
    background-size:23px 23px;
}

.block-container {
    max-width: 1180px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

.hero {
    position:relative;
    overflow:hidden;
    padding:30px;
    border-radius:32px;
    color:#fff;
    background:linear-gradient(135deg,#06101e 0%,#0c2137 52%,#123d35 100%);
    box-shadow:0 28px 70px rgba(7,17,31,.22);
    margin-bottom:18px;
}

.hero:before {
    content:"";
    position:absolute;
    width:480px;
    height:480px;
    border-radius:50%;
    right:-220px;
    top:-310px;
    background:radial-gradient(circle,#20dc8533,transparent 68%);
    border:1px solid #ffffff10;
}

.hero:after {
    content:"";
    position:absolute;
    width:280px;
    height:280px;
    border-radius:50%;
    left:-170px;
    bottom:-220px;
    background:#2563eb16;
}

.hero-content { position:relative; z-index:2; }

.brand-line {
    display:flex;
    align-items:center;
    gap:16px;
}

.logo {
    width:68px;
    height:68px;
    border-radius:22px;
    display:grid;
    place-items:center;
    font-size:34px;
    background:linear-gradient(145deg,#20dc85,#087b4b);
    box-shadow:0 14px 30px #0007;
    border:1px solid #ffffff25;
}

.hero h1 {
    margin:0;
    font-size:31px;
    font-weight:900;
    letter-spacing:-.8px;
}

.hero-sub {
    color:#c7d5e1;
    font-size:13px;
    margin-top:6px;
}

.badges {
    display:flex;
    flex-wrap:wrap;
    gap:8px;
    margin-top:20px;
}

.badge {
    display:inline-flex;
    align-items:center;
    padding:8px 11px;
    border-radius:999px;
    color:#eaf6ff;
    background:#ffffff0d;
    border:1px solid #ffffff1b;
    font-size:10px;
    font-weight:900;
    letter-spacing:.35px;
    backdrop-filter:blur(8px);
}

.card {
    background:rgba(255,255,255,.90);
    border:1px solid #ffffffd4;
    border-radius:25px;
    padding:22px;
    box-shadow:var(--shadow);
    backdrop-filter:blur(16px);
    -webkit-backdrop-filter:blur(16px);
    margin-bottom:16px;
}

.section-heading {
    display:flex;
    align-items:flex-end;
    justify-content:space-between;
    gap:14px;
    margin-bottom:15px;
}

.section-heading h2 {
    margin:0;
    font-size:18px;
    font-weight:900;
    letter-spacing:-.25px;
}

.section-heading p {
    margin:4px 0 0;
    color:var(--muted);
    font-size:11px;
}

.customer-chip {
    padding:7px 10px;
    border-radius:999px;
    background:var(--navy);
    color:#fff;
    font-size:9px;
    font-weight:900;
    letter-spacing:.55px;
}

.metric-card {
    padding:17px;
    border-radius:18px;
    background:linear-gradient(145deg,#fbfcfd,#f3f6f9);
    border:1px solid var(--line);
    min-height:92px;
}

.metric-label {
    color:var(--muted);
    font-size:9px;
    font-weight:900;
    letter-spacing:.45px;
}

.metric-value {
    color:var(--ink);
    font-size:18px;
    font-weight:900;
    margin-top:6px;
    line-height:1.15;
}

.metric-help {
    color:#8793a1;
    font-size:9px;
    margin-top:5px;
}

.finance-box {
    padding:23px;
    border-radius:24px;
    min-height:300px;
    border:1px solid;
}

.finance-box.lease {
    background:linear-gradient(145deg,#eafbf3,#ffffff 72%);
    border-color:#bfe8d1;
}

.finance-box.loan {
    background:linear-gradient(145deg,#eff5ff,#ffffff 72%);
    border-color:#cfddff;
}

.finance-top {
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:8px;
}

.finance-tag {
    display:inline-flex;
    padding:7px 10px;
    border-radius:999px;
    background:#fff;
    border:1px solid #0000000b;
    font-size:9px;
    font-weight:900;
}

.finance-status {
    color:var(--muted);
    font-size:9px;
    font-weight:800;
}

.finance-title {
    margin:14px 0 4px;
    font-size:20px;
    font-weight:900;
}

.finance-emi {
    margin:4px 0 2px;
    font-size:32px;
    font-weight:950;
    letter-spacing:-.9px;
}

.finance-sub {
    color:var(--muted);
    font-size:10px;
    font-weight:800;
}

.finance-row {
    display:flex;
    justify-content:space-between;
    gap:12px;
    padding:9px 0;
    border-bottom:1px solid #0000000d;
    font-size:11px;
}

.finance-row:last-child { border-bottom:0; }
.finance-row span { color:var(--muted); }
.finance-row b { text-align:right; }

.total-card {
    position:relative;
    overflow:hidden;
    padding:27px;
    border-radius:26px;
    color:#fff;
    text-align:center;
    background:linear-gradient(135deg,#06101e,#173752 58%,#123f35);
    box-shadow:0 22px 48px rgba(7,17,31,.17);
}

.total-card:after {
    content:"";
    position:absolute;
    width:280px;
    height:280px;
    border-radius:50%;
    right:-170px;
    top:-180px;
    background:#ffffff09;
}

.total-label {
    position:relative;
    z-index:1;
    color:#b9c8d9;
    font-size:10px;
    font-weight:900;
    letter-spacing:.45px;
}

.total-number {
    position:relative;
    z-index:1;
    margin:5px 0;
    font-size:41px;
    font-weight:950;
    letter-spacing:-1px;
}

.total-detail {
    position:relative;
    z-index:1;
    color:#c9d5e0;
    font-size:11px;
}

.offer-card {
    position:relative;
    overflow:hidden;
    padding:23px;
    border-radius:25px;
    color:#fff;
    background:linear-gradient(135deg,#06101e,#0e2941 58%,#104633);
    box-shadow:0 22px 50px rgba(7,17,31,.16);
}

.offer-card:before {
    content:"";
    position:absolute;
    width:340px;
    height:340px;
    right:-160px;
    top:-190px;
    border-radius:50%;
    background:radial-gradient(circle,#20dc8540,transparent 68%);
}

.offer-title {
    position:relative;
    z-index:1;
    font-size:25px;
    font-weight:950;
    letter-spacing:-.55px;
}

.offer-sub {
    position:relative;
    z-index:1;
    margin-top:5px;
    color:#c7d6e1;
    font-size:11px;
}

.offer-pill-row {
    position:relative;
    z-index:1;
    display:flex;
    flex-wrap:wrap;
    gap:9px;
    margin-top:17px;
}

.offer-pill {
    padding:11px 13px;
    border-radius:15px;
    background:#ffffff0b;
    border:1px solid #ffffff15;
    min-width:120px;
}

.offer-pill small {
    display:block;
    color:#aebdca;
    font-size:8px;
    font-weight:900;
}

.offer-pill b {
    display:block;
    margin-top:4px;
    font-size:15px;
}

.schedule-card {
    overflow:hidden;
    border-radius:23px;
    border:1px solid var(--line);
    background:#fff;
}

.schedule-header {
    padding:15px 17px;
    background:linear-gradient(145deg,#f7f9fb,#eef3f7);
    border-bottom:1px solid var(--line);
}

.schedule-header h3 {
    margin:0;
    font-size:14px;
    font-weight:900;
}

.schedule-header p {
    margin:4px 0 0;
    color:var(--muted);
    font-size:10px;
}

.note {
    color:#7b8794;
    font-size:10px;
    line-height:1.7;
    margin-top:12px;
}

.warning {
    padding:13px 15px;
    border-radius:15px;
    background:#fff7ed;
    border:1px solid #fed7aa;
    color:#9a3412;
    font-size:11px;
    font-weight:700;
}

.success-box {
    padding:13px 15px;
    border-radius:15px;
    background:#ecfdf3;
    border:1px solid #b7ebcf;
    color:#087748;
    font-size:11px;
    font-weight:800;
}

.quote {
    padding:26px;
    border-radius:25px;
    color:#fff;
    background:linear-gradient(135deg,#06101e,#12354f);
    box-shadow:0 20px 45px rgba(7,17,31,.14);
}

.quote-head {
    display:flex;
    justify-content:space-between;
    gap:15px;
    align-items:flex-start;
}

.quote-title {
    font-size:23px;
    font-weight:950;
}

.quote-id {
    font-size:9px;
    font-weight:900;
    padding:8px 10px;
    border-radius:999px;
    background:#ffffff10;
    border:1px solid #ffffff18;
}

.quote-sub {
    color:#bfcdda;
    font-size:10px;
    margin-top:4px;
}

.quote-line {
    display:flex;
    justify-content:space-between;
    padding:9px 0;
    border-bottom:1px solid #ffffff12;
    font-size:11px;
}

.quote-line:last-child { border-bottom:0; }

.quote-total {
    margin-top:14px;
    padding:17px;
    border-radius:18px;
    background:#ffffff0b;
    border:1px solid #ffffff14;
    text-align:center;
}

.quote-total small {
    color:#b9c8d9;
    font-size:9px;
    font-weight:900;
}

.quote-total b {
    display:block;
    margin-top:5px;
    font-size:27px;
}

.footer {
    text-align:center;
    color:#7b8794;
    font-size:9px;
    padding:18px 4px 5px;
}

div[data-testid="stMetric"] {
    background:rgba(255,255,255,.72);
    border:1px solid var(--line);
    padding:12px 14px;
    border-radius:16px;
}

button[kind="primary"] {
    background:linear-gradient(135deg,#07111f,#16314f);
}

button {
    border-radius:13px !important;
}

[data-testid="stDataFrame"] {
    border-radius:16px;
    overflow:hidden;
}

@media(max-width:800px) {
    .hero { padding:23px; border-radius:24px; }
    .hero h1 { font-size:25px; }
    .logo { width:58px; height:58px; font-size:29px; }
    .finance-emi { font-size:28px; }
    .total-number { font-size:32px; }
}

/* ============================================================
   MOBILE / THEME CONTRAST FIX
   ============================================================ */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    color: #101828 !important;
}

.stMarkdown,
.stMarkdown p,
.stMarkdown span,
.stMarkdown div,
[data-testid="stText"],
[data-testid="stCaptionContainer"] {
    color: #101828 !important;
}

.stApp label,
.stApp [data-testid="stWidgetLabel"],
.stApp [data-testid="stWidgetLabel"] p,
.stApp [data-testid="stWidgetLabel"] span {
    color: #344054 !important;
}

.stApp input,
.stApp textarea,
.stApp select,
.stApp [data-baseweb="input"] input,
.stApp [data-baseweb="select"] * {
    color: #101828 !important;
    -webkit-text-fill-color: #101828 !important;
    background-color: #ffffff !important;
}

.stApp input::placeholder,
.stApp textarea::placeholder {
    color: #98a2b3 !important;
    -webkit-text-fill-color: #98a2b3 !important;
}

.stApp [data-testid="stNumberInput"] button {
    color: #344054 !important;
    background: #ffffff !important;
}

.stApp [data-testid="stExpander"] summary,
.stApp [data-testid="stExpander"] summary p,
.stApp [data-testid="stExpander"] summary span {
    color: #101828 !important;
}

.stApp [data-testid="stSelectbox"] label,
.stApp [data-testid="stNumberInput"] label,
.stApp [data-testid="stTextInput"] label {
    color: #344054 !important;
}

.stApp [data-testid="stMetricLabel"],
.stApp [data-testid="stMetricValue"],
.stApp [data-testid="stMetricDelta"] {
    color: #101828 !important;
}

.stApp [data-testid="stDataFrame"] {
    color: #101828 !important;
}

.stApp [data-testid="stDataFrame"] * {
    color: #101828 !important;
}

.stApp .stCaption,
.stApp [data-testid="stCaptionContainer"] p {
    color: #667085 !important;
}

/* Keep the premium custom cards white/light while preserving their own
   dark text and the intentionally dark total/offer/quote cards. */
.stApp .card,
.stApp .finance-box,
.stApp .metric-card,
.stApp .schedule-card {
    color: #101828 !important;
}

@media (max-width: 800px) {
    .block-container {
        padding-left: 12px !important;
        padding-right: 12px !important;
        padding-top: 12px !important;
    }

    .hero {
        border-radius: 24px !important;
        padding: 22px !important;
    }

    .card {
        border-radius: 21px !important;
        padding: 17px !important;
    }

    .finance-box {
        border-radius: 20px !important;
        padding: 18px !important;
    }

    .section-heading h2,
    .section-heading p,
    .metric-label,
    .metric-value,
    .metric-help {
        color: #101828 !important;
    }
}

</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# HELPERS
# ============================================================

def money(value):
    return "රු. " + format(float(value or 0), ",.2f")


def emi(principal, annual_rate, years):
    principal = float(principal or 0)
    years = float(years or 0)
    if principal <= 0 or years <= 0:
        return 0.0

    months = int(round(years * 12))
    monthly_rate = float(annual_rate) / 100 / 12

    if monthly_rate == 0:
        return principal / months

    numerator = principal * monthly_rate * (1 + monthly_rate) ** months
    denominator = (1 + monthly_rate) ** months - 1
    return numerator / denominator


def amortization_schedule(principal, annual_rate, years):
    principal = float(principal or 0)
    months = int(round(float(years or 0) * 12))
    monthly_rate = float(annual_rate) / 100 / 12
    payment = emi(principal, annual_rate, years)

    rows = []
    balance = principal

    for month in range(1, months + 1):
        opening = balance
        interest = opening * monthly_rate
        principal_paid = payment - interest

        if month == months:
            principal_paid = opening
            actual_payment = principal_paid + interest
            closing = 0.0
        else:
            actual_payment = payment
            closing = max(0.0, opening - principal_paid)

        rows.append(
            {
                "Month": month,
                "Opening Balance": opening,
                "Monthly Payment": actual_payment,
                "Principal": principal_paid,
                "Interest": interest,
                "Closing Balance": closing,
            }
        )

        balance = closing

    return pd.DataFrame(rows)


def calculate_finance(price, down, insurance, years):
    price = float(price)
    down = float(down)
    insurance = float(insurance)
    years = int(years)

    base_finance = price - down
    maximum_finance = price * 0.60

    lease_base = min(base_finance, price * 0.40)
    loan_base = max(0.0, base_finance - lease_base)

    document_charge = 9500.0
    commission = price * 0.03

    lease_amount = lease_base + document_charge + commission + insurance
    loan_years = max(1, years - 1)

    lease_emi = emi(lease_amount, 26, years)
    loan_emi = emi(loan_base, 28, loan_years)
    total_emi = lease_emi + loan_emi

    lease_schedule = amortization_schedule(lease_amount, 26, years)
    loan_schedule = amortization_schedule(loan_base, 28, loan_years)

    return {
        "price": price,
        "down": down,
        "insurance": insurance,
        "years": years,
        "base_finance": base_finance,
        "maximum_finance": maximum_finance,
        "finance_percent": (base_finance / price * 100) if price else 0,
        "lease_base": lease_base,
        "loan_base": loan_base,
        "document_charge": document_charge,
        "commission": commission,
        "lease_amount": lease_amount,
        "loan_years": loan_years,
        "lease_emi": lease_emi,
        "loan_emi": loan_emi,
        "total_emi": total_emi,
        "lease_schedule": lease_schedule,
        "loan_schedule": loan_schedule,
    }


def schedule_for_display(df):
    out = df.copy()
    for col in [
        "Opening Balance",
        "Monthly Payment",
        "Principal",
        "Interest",
        "Closing Balance",
    ]:
        out[col] = out[col].map(money)
    return out


def schedule_csv(df):
    out = df.copy()
    return out.to_csv(index=False).encode("utf-8-sig")


def make_quote_id():
    return "BFP-" + datetime.now().strftime("%y%m%d-%H%M%S")


def initialize():
    defaults = {
        "result": None,
        "quote_id": make_quote_id(),
        "customer_name": "",
        "customer_phone": "",
        "bike_model": "",
        "reference": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


initialize()

# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
<div class="hero">
  <div class="hero-content">
    <div class="brand-line">
      <div class="logo">🏍️</div>
      <div>
        <h1>Bike Finance Pro</h1>
        <div class="hero-sub">
          Professional leasing & loan EMI calculator • Fast • Clear • Customer-ready
        </div>
      </div>
    </div>
    <div class="badges">
      <span class="badge">MAX FINANCE 60%</span>
      <span class="badge">40% LEASE</span>
      <span class="badge">20% LOAN</span>
      <span class="badge">LEASE 26%</span>
      <span class="badge">LOAN 28%</span>
      <span class="badge">REDUCING BALANCE EMI</span>
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# ============================================================
# CUSTOMER DETAILS
# ============================================================

with st.expander("👤 Customer Details & Quotation Information", expanded=False):
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        customer_name = st.text_input(
            "CUSTOMER NAME",
            value=st.session_state["customer_name"],
            placeholder="Customer name",
        )
        st.session_state["customer_name"] = customer_name

    with c2:
        customer_phone = st.text_input(
            "CONTACT NUMBER",
            value=st.session_state["customer_phone"],
            placeholder="07XXXXXXXX",
        )
        st.session_state["customer_phone"] = customer_phone

    with c3:
        bike_model = st.text_input(
            "BIKE MODEL",
            value=st.session_state["bike_model"],
            placeholder="e.g. Honda Dio",
        )
        st.session_state["bike_model"] = bike_model

    with c4:
        reference = st.text_input(
            "REFERENCE",
            value=st.session_state["reference"],
            placeholder="Optional",
        )
        st.session_state["reference"] = reference

    st.caption(
        f"Quotation ID: {st.session_state['quote_id']}  •  Date: {date.today().strftime('%d/%m/%Y')}"
    )

# ============================================================
# INPUT CARD
# ============================================================

st.markdown(
    """
<div class="card">
  <div class="section-heading">
    <div>
      <h2>🏍️ Customer & Bike Details</h2>
      <p>Enter the bike value, down payment, insurance and lease period.</p>
    </div>
    <span class="customer-chip">FINANCE CALCULATOR</span>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

left, right = st.columns(2)

with left:
    price = st.number_input(
        "BIKE VALUE (රු.)",
        min_value=0.0,
        value=1_000_000.0,
        step=10_000.0,
        format="%.2f",
        help="Enter the agreed bike value.",
    )

    insurance = st.number_input(
        "INSURANCE (රු.)",
        min_value=0.0,
        value=0.0,
        step=1_000.0,
        format="%.2f",
        help="Insurance amount can vary by bike.",
    )

with right:
    down = st.number_input(
        "DOWN PAYMENT (රු.)",
        min_value=0.0,
        value=400_000.0,
        step=10_000.0,
        format="%.2f",
        help="Customer's initial down payment.",
    )

    years = st.selectbox(
        "LEASE PERIOD",
        options=[2, 3, 4, 5],
        index=1,
        format_func=lambda x: f"{x} YEARS",
        help="Loan period is automatically one year shorter.",
    )

if price > 0:
    real_down = down + 12_800 + 8_500
    st.markdown(
        f"""
<div class="success-box">
  REAL DOWN PAYMENT DISPLAY: <b>{money(real_down)}</b>
</div>
""",
        unsafe_allow_html=True,
    )

st.write("")

calc_col, reset_col = st.columns([3, 1])

with calc_col:
    calculate_clicked = st.button(
        "🧮 CALCULATE COMPLETE FINANCE PLAN",
        type="primary",
        use_container_width=True,
    )

with reset_col:
    reset_clicked = st.button(
        "↻ RESET",
        use_container_width=True,
    )

if reset_clicked:
    st.session_state["result"] = None
    st.session_state["quote_id"] = make_quote_id()
    st.rerun()

if calculate_clicked:
    error = None

    if price <= 0:
        error = "Bike value එක 0 ට වඩා වැඩි විය යුතුයි."

    elif down < 0:
        error = "Down payment එක negative විය නොහැක."

    elif down >= price:
        error = "Down payment එක bike value එකට වඩා අඩු විය යුතුයි."

    elif insurance < 0:
        error = "Insurance amount එක negative විය නොහැක."

    if error:
        st.error(error)
    else:
        temp = calculate_finance(price, down, insurance, years)

        if temp["base_finance"] > temp["maximum_finance"] + 0.01:
            st.error(
                "Maximum base finance is 60% of the bike value. "
                f"Minimum down payment for this bike is {money(price * 0.40)}."
            )
        else:
            st.session_state["result"] = temp
            st.session_state["quote_id"] = make_quote_id()
            st.success("Finance plan calculated successfully.")

# ============================================================
# RESULTS
# ============================================================

d = st.session_state.get("result")

if d is not None:

    st.write("")
    st.markdown(
        """
<div class="section-heading">
  <div>
    <h2>📊 Finance Summary</h2>
    <p>Complete internal calculation summary.</p>
  </div>
  <span class="customer-chip">CALCULATED</span>
</div>
""",
        unsafe_allow_html=True,
    )

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.markdown(
            f"""
<div class="metric-card">
  <div class="metric-label">BIKE VALUE</div>
  <div class="metric-value">{money(d['price'])}</div>
  <div class="metric-help">Selected bike value</div>
</div>
""",
            unsafe_allow_html=True,
        )

    with m2:
        st.markdown(
            f"""
<div class="metric-card">
  <div class="metric-label">DOWN PAYMENT</div>
  <div class="metric-value">{money(d['down'])}</div>
  <div class="metric-help">Initial customer payment</div>
</div>
""",
            unsafe_allow_html=True,
        )

    with m3:
        st.markdown(
            f"""
<div class="metric-card">
  <div class="metric-label">BASE FINANCE</div>
  <div class="metric-value">{money(d['base_finance'])}</div>
  <div class="metric-help">Lease + loan base</div>
</div>
""",
            unsafe_allow_html=True,
        )

    with m4:
        st.markdown(
            f"""
<div class="metric-card">
  <div class="metric-label">FINANCE %</div>
  <div class="metric-value">{d['finance_percent']:.1f}%</div>
  <div class="metric-help">Maximum allowed: 60%</div>
</div>
""",
            unsafe_allow_html=True,
        )

    st.write("")

    # --------------------------------------------------------
    # LEASE + LOAN CARDS
    # --------------------------------------------------------

    lease_col, loan_col = st.columns(2)

    with lease_col:
        st.markdown(
            f"""
<div class="finance-box lease">
  <div class="finance-top">
    <span class="finance-tag">📄 LEASE • 26%</span>
    <span class="finance-status">CUSTOMER PLAN</span>
  </div>
  <div class="finance-title">{d['years']} Year Lease</div>
  <div class="finance-emi">{money(d['lease_emi'])}</div>
  <div class="finance-sub">monthly leasing instalment</div>
  <div style="margin-top:14px">
    <div class="finance-row"><span>Base Lease</span><b>{money(d['lease_base'])}</b></div>
    <div class="finance-row"><span>Document Charge</span><b>{money(d['document_charge'])}</b></div>
    <div class="finance-row"><span>Commission 3%</span><b>{money(d['commission'])}</b></div>
    <div class="finance-row"><span>Insurance</span><b>{money(d['insurance'])}</b></div>
    <div class="finance-row"><span>Total Lease Amount</span><b>{money(d['lease_amount'])}</b></div>
    <div class="finance-row"><span>Period</span><b>{d['years'] * 12} months</b></div>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

    with loan_col:
        st.markdown(
            f"""
<div class="finance-box loan">
  <div class="finance-top">
    <span class="finance-tag">💰 LOAN • 28%</span>
    <span class="finance-status">CUSTOMER PLAN</span>
  </div>
  <div class="finance-title">{d['loan_years']} Year Loan</div>
  <div class="finance-emi">{money(d['loan_emi'])}</div>
  <div class="finance-sub">monthly loan instalment</div>
  <div style="margin-top:14px">
    <div class="finance-row"><span>Loan Amount</span><b>{money(d['loan_base'])}</b></div>
    <div class="finance-row"><span>Interest Rate</span><b>28% p.a.</b></div>
    <div class="finance-row"><span>Period</span><b>{d['loan_years'] * 12} months</b></div>
    <div class="finance-row"><span>Payment Method</span><b>Reducing Balance</b></div>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

    st.write("")

    # --------------------------------------------------------
    # TOTAL
    # --------------------------------------------------------

    st.markdown(
        f"""
<div class="total-card">
  <div class="total-label">CUSTOMER TOTAL MONTHLY PAYMENT</div>
  <div class="total-number">{money(d['total_emi'])}</div>
  <div class="total-detail">
    Lease {money(d['lease_emi'])} &nbsp; + &nbsp;
    Loan {money(d['loan_emi'])} &nbsp; / month
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.write("")

    # --------------------------------------------------------
    # SPECIAL OFFER
    # --------------------------------------------------------

    st.markdown(
        f"""
<div class="offer-card">
  <div class="offer-title">✨ Ride Your Dream Bike Today</div>
  <div class="offer-sub">
    Flexible finance • Simple monthly payments • Customer-friendly plan
  </div>
  <div class="offer-pill-row">
    <div class="offer-pill">
      <small>MONTHLY PAYMENT</small>
      <b>{money(d['total_emi'])}</b>
    </div>
    <div class="offer-pill">
      <small>LEASE EMI</small>
      <b>{money(d['lease_emi'])}</b>
    </div>
    <div class="offer-pill">
      <small>LOAN EMI</small>
      <b>{money(d['loan_emi'])}</b>
    </div>
    <div class="offer-pill">
      <small>TERM</small>
      <b>{d['years']} Years</b>
    </div>
    <div class="offer-pill">
      <small>INSURANCE</small>
      <b>FREE*</b>
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.write("")

    # ========================================================
    # PAYMENT PLANS — BOTH LEASE & LOAN
    # ========================================================

    st.markdown(
        """
<div class="section-heading">
  <div>
    <h2>📅 Complete Payment Plans</h2>
    <p>Separate monthly schedules for both leasing and loan.</p>
  </div>
  <span class="customer-chip">LEASE + LOAN</span>
</div>
""",
        unsafe_allow_html=True,
    )

    lease_tab, loan_tab, combined_tab = st.tabs(
        ["📄 LEASE PAYMENT PLAN", "💰 LOAN PAYMENT PLAN", "📊 COMBINED VIEW"]
    )

    with lease_tab:
        lease_df = d["lease_schedule"]

        l1, l2, l3, l4 = st.columns(4)
        l1.metric("LEASE AMOUNT", money(d["lease_amount"]))
        l2.metric("MONTHLY EMI", money(d["lease_emi"]))
        l3.metric("RATE", "26% p.a.")
        l4.metric("TERM", f"{d['years']} years")

        st.markdown(
            """
<div class="schedule-card">
  <div class="schedule-header">
    <h3>📄 Leasing Amortization Schedule</h3>
    <p>Monthly payment, principal, interest and remaining balance.</p>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        st.dataframe(
            schedule_for_display(lease_df),
            use_container_width=True,
            hide_index=True,
            height=430,
        )

        lease_total_principal = float(lease_df["Principal"].sum())
        lease_total_interest = float(lease_df["Interest"].sum())

        q1, q2, q3 = st.columns(3)
        q1.metric("TOTAL PRINCIPAL", money(lease_total_principal))
        q2.metric("TOTAL INTEREST", money(lease_total_interest))
        q3.metric("TOTAL PAYMENTS", money(lease_df["Monthly Payment"].sum()))

        st.download_button(
            "⬇️ Download Lease Payment Plan (CSV)",
            data=schedule_csv(lease_df),
            file_name=f"{st.session_state['quote_id']}_lease_plan.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with loan_tab:
        loan_df = d["loan_schedule"]

        o1, o2, o3, o4 = st.columns(4)
        o1.metric("LOAN AMOUNT", money(d["loan_base"]))
        o2.metric("MONTHLY EMI", money(d["loan_emi"]))
        o3.metric("RATE", "28% p.a.")
        o4.metric("TERM", f"{d['loan_years']} years")

        st.markdown(
            """
<div class="schedule-card">
  <div class="schedule-header">
    <h3>💰 Loan Amortization Schedule</h3>
    <p>Monthly payment, principal, interest and remaining balance.</p>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        st.dataframe(
            schedule_for_display(loan_df),
            use_container_width=True,
            hide_index=True,
            height=430,
        )

        loan_total_principal = float(loan_df["Principal"].sum())
        loan_total_interest = float(loan_df["Interest"].sum())

        r1, r2, r3 = st.columns(3)
        r1.metric("TOTAL PRINCIPAL", money(loan_total_principal))
        r2.metric("TOTAL INTEREST", money(loan_total_interest))
        r3.metric("TOTAL PAYMENTS", money(loan_df["Monthly Payment"].sum()))

        st.download_button(
            "⬇️ Download Loan Payment Plan (CSV)",
            data=schedule_csv(loan_df),
            file_name=f"{st.session_state['quote_id']}_loan_plan.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with combined_tab:
        max_months = max(len(d["lease_schedule"]), len(d["loan_schedule"]))

        combined_rows = []

        for i in range(max_months):
            lease_payment = (
                float(d["lease_schedule"].iloc[i]["Monthly Payment"])
                if i < len(d["lease_schedule"])
                else 0.0
            )
            loan_payment = (
                float(d["loan_schedule"].iloc[i]["Monthly Payment"])
                if i < len(d["loan_schedule"])
                else 0.0
            )

            combined_rows.append(
                {
                    "Month": i + 1,
                    "Lease Payment": lease_payment,
                    "Loan Payment": loan_payment,
                    "Total Monthly Payment": lease_payment + loan_payment,
                }
            )

        combined_df = pd.DataFrame(combined_rows)

        st.markdown(
            """
<div class="schedule-card">
  <div class="schedule-header">
    <h3>📊 Combined Monthly Payment View</h3>
    <p>Both lease and loan shown side-by-side month by month.</p>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        combined_display = combined_df.copy()
        for col in ["Lease Payment", "Loan Payment", "Total Monthly Payment"]:
            combined_display[col] = combined_display[col].map(money)

        st.dataframe(
            combined_display,
            use_container_width=True,
            hide_index=True,
            height=430,
        )

        st.download_button(
            "⬇️ Download Combined Payment Plan (CSV)",
            data=combined_df.to_csv(index=False).encode("utf-8-sig"),
            file_name=f"{st.session_state['quote_id']}_combined_plan.csv",
            mime="text/csv",
            use_container_width=True,
        )

    # ========================================================
    # CUSTOMER VIEW
    # ========================================================

    st.write("")
    st.markdown(
        """
<div class="section-heading">
  <div>
    <h2>👤 Customer View</h2>
    <p>Clean presentation designed to show the customer the important numbers.</p>
  </div>
  <span class="customer-chip">CUSTOMER-FACING</span>
</div>
""",
        unsafe_allow_html=True,
    )

    customer_name_display = (
        html.escape(st.session_state["customer_name"])
        if st.session_state["customer_name"]
        else "Valued Customer"
    )
    bike_display = (
        html.escape(st.session_state["bike_model"])
        if st.session_state["bike_model"]
        else "Selected Bike"
    )

    st.markdown(
        f"""
<div class="quote">
  <div class="quote-head">
    <div>
      <div class="quote-title">🏍️ Bike Finance Plan</div>
      <div class="quote-sub">
        Personalized customer quotation • {customer_name_display} • {bike_display}
      </div>
    </div>
    <div class="quote-id">{st.session_state['quote_id']}</div>
  </div>

  <div style="margin-top:20px">
    <div class="quote-line"><span>Bike Value</span><b>{money(d['price'])}</b></div>
    <div class="quote-line"><span>Down Payment</span><b>{money(d['down'])}</b></div>
    <div class="quote-line"><span>Leasing Facility</span><b>40%</b></div>
    <div class="quote-line"><span>Lease Period</span><b>{d['years']} Years</b></div>
    <div class="quote-line"><span>Loan Period</span><b>{d['loan_years']} Years</b></div>
    <div class="quote-line"><span>Insurance</span><b>FREE*</b></div>
  </div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px">
    <div style="padding:16px;border-radius:18px;background:#ffffff0b;border:1px solid #ffffff14">
      <div style="font-size:9px;color:#b9c8d9;font-weight:900">LEASING</div>
      <div style="font-size:25px;font-weight:950;margin-top:5px">{money(d['lease_emi'])}</div>
      <div style="font-size:9px;color:#b9c8d9;margin-top:3px">per month</div>
    </div>
    <div style="padding:16px;border-radius:18px;background:#ffffff0b;border:1px solid #ffffff14">
      <div style="font-size:9px;color:#b9c8d9;font-weight:900">LOAN</div>
      <div style="font-size:25px;font-weight:950;margin-top:5px">{money(d['loan_emi'])}</div>
      <div style="font-size:9px;color:#b9c8d9;margin-top:3px">per month</div>
    </div>
  </div>

  <div class="quote-total">
    <small>YOUR TOTAL MONTHLY PAYMENT</small>
    <b>{money(d['total_emi'])}</b>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.write("")

    # --------------------------------------------------------
    # CUSTOMER PAYMENT PLAN — BOTH VISIBLE
    # --------------------------------------------------------

    st.markdown(
        """
<div class="card">
  <div class="section-heading">
    <div>
      <h2>📆 Customer Payment Plan</h2>
      <p>Both leasing and loan monthly payments are clearly shown.</p>
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    customer_combined = combined_df.copy()

    customer_combined["Lease Payment"] = customer_combined["Lease Payment"].map(money)
    customer_combined["Loan Payment"] = customer_combined["Loan Payment"].map(money)
    customer_combined["Total Monthly Payment"] = customer_combined[
        "Total Monthly Payment"
    ].map(money)

    st.dataframe(
        customer_combined,
        use_container_width=True,
        hide_index=True,
        height=430,
    )

    # ========================================================
    # CUSTOMER-FACING OFFER
    # ========================================================

    st.markdown(
        f"""
<div class="offer-card">
  <div class="offer-title">✨ Special Customer Offer</div>
  <div class="offer-sub">
    Simple monthly payments • Flexible finance • Customer-friendly plan
  </div>

  <div class="offer-pill-row">
    <div class="offer-pill">
      <small>LEASE</small>
      <b>{money(d['lease_emi'])}/mo</b>
    </div>
    <div class="offer-pill">
      <small>LOAN</small>
      <b>{money(d['loan_emi'])}/mo</b>
    </div>
    <div class="offer-pill">
      <small>TOTAL</small>
      <b>{money(d['total_emi'])}/mo</b>
    </div>
    <div class="offer-pill">
      <small>INSURANCE</small>
      <b>FREE*</b>
    </div>
  </div>

  <div style="position:relative;z-index:1;margin-top:15px;padding:13px 15px;
       border-radius:15px;background:#ffffff09;border:1px solid #ffffff14;
       color:#eafff3;font-size:11px;font-weight:800">
    🏍️ Start your bike journey with an easy monthly payment.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # ========================================================
    # DOWNLOAD / EXPORT
    # ========================================================

    st.write("")
    st.markdown(
        """
<div class="section-heading">
  <div>
    <h2>⬇️ Export & Share</h2>
    <p>Download the calculated plans for records or sharing.</p>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    e1, e2, e3 = st.columns(3)

    customer_text = (
        "BIKE FINANCE QUOTATION\n"
        f"Quotation ID: {st.session_state['quote_id']}\n"
        f"Customer: {st.session_state['customer_name'] or 'Valued Customer'}\n"
        f"Bike: {st.session_state['bike_model'] or 'Selected Bike'}\n"
        f"Bike Value: {money(d['price'])}\n"
        f"Down Payment: {money(d['down'])}\n"
        f"Lease EMI: {money(d['lease_emi'])} / month\n"
        f"Loan EMI: {money(d['loan_emi'])} / month\n"
        f"Total Monthly: {money(d['total_emi'])} / month\n"
        f"Lease Period: {d['years']} years\n"
        f"Loan Period: {d['loan_years']} years\n"
        "Insurance: FREE*\n"
    )

    with e1:
        st.download_button(
            "📄 Download Customer Quote",
            data=customer_text.encode("utf-8-sig"),
            file_name=f"{st.session_state['quote_id']}_customer_quote.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with e2:
        st.download_button(
            "📄 Download Lease CSV",
            data=schedule_csv(d["lease_schedule"]),
            file_name=f"{st.session_state['quote_id']}_lease.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with e3:
        st.download_button(
            "📄 Download Loan CSV",
            data=schedule_csv(d["loan_schedule"]),
            file_name=f"{st.session_state['quote_id']}_loan.csv",
            mime="text/csv",
            use_container_width=True,
        )

    # ========================================================
    # IMPORTANT NOTES
    # ========================================================

    st.write("")
    st.markdown(
        """
<div class="warning">
  <b>Important:</b> This calculator presents an estimated finance plan.
  Final approval, official charges, insurance conditions and company terms
  should be confirmed before issuing a binding quotation.
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="note">
  * Insurance is displayed as FREE in the customer-facing offer because the
  supplied customer-view design uses a free-insurance customer offer.
  The internal calculation can still accept an insurance amount where required.
  EMI is calculated using a reducing-balance monthly formula.
</div>
""",
        unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<div class="footer">
  Prepared with Bike Finance Pro • Professional customer finance summary
  • Lease + Loan payment plans
</div>
""",
    unsafe_allow_html=True,
)

# ============================================================
# EXTRA DOCUMENTATION / IMPLEMENTATION NOTES
# Kept in source so the project is easier to maintain and extend.
# ============================================================

PROJECT_NOTES = """
Bike Finance Pro implementation notes

1. Input layer
   The app accepts bike value, down payment, insurance and lease period.
   Customer information is optional and is used only for the quotation view.

2. Finance structure
   The supplied calculator uses a maximum base finance of 60 percent.
   The first 40 percent of the base finance is assigned to the lease.
   The remaining base finance up to the 60 percent limit is assigned to loan.

3. Lease calculation
   Lease amount is the base lease plus the document charge, commission and
   insurance. The document charge in the supplied HTML was Rs. 9,500.
   Commission is three percent of bike value.
   Lease EMI uses 26 percent per annum reducing balance.

4. Loan calculation
   Loan amount is the remaining base finance after the lease base.
   Loan EMI uses 28 percent per annum reducing balance.
   Loan period is one year shorter than the selected lease period.

5. Payment schedules
   Both schedules contain:
       Month
       Opening Balance
       Monthly Payment
       Principal
       Interest
       Closing Balance

6. Customer presentation
   The customer view emphasizes:
       Bike value
       Down payment
       Leasing facility
       Lease period
       Loan period
       Lease EMI
       Loan EMI
       Total monthly payment
       Insurance offer

7. Internal vs customer values
   Detailed lease charges are retained in the calculator area.
   The customer-facing quotation focuses on the simple payment structure.

8. CSV export
   Lease and loan schedules can be exported independently.
   A combined schedule is also available.

9. Future improvements
   The application can later add:
       PDF quotation generation
       company logo upload
       WhatsApp share button
       customer signature
       salesperson information
       multiple quotation saving
       database storage
       authentication
       branch selection
       approval workflow
       print-optimized customer page
       automatic quotation expiry
       interest summaries
       graphical balance charts
"""

# ============================================================
# PROJECT MAINTENANCE & EXTENSION GUIDE
# ============================================================
# BIKE FINANCE PRO PREMIUM
#
# Calculation structure:
#   Maximum base finance = 60% of bike value.
#   Base lease = up to 40% of bike value.
#   Base loan = remaining amount up to the 60% limit.
#   Lease amount = base lease + Rs. 9,500 document charge
#                  + 3% commission + insurance.
#   Lease rate = 26% p.a. reducing balance.
#   Loan rate = 28% p.a. reducing balance.
#   Loan period = selected lease period minus one year.
#
# Customer presentation:
#   The customer view intentionally keeps the presentation simple.
#   It shows bike value, down payment, 40% leasing facility, lease
#   period, loan period, lease EMI, loan EMI, total monthly payment,
#   insurance offer and a complete combined payment schedule.
#
# Payment-plan design:
#   The app provides three views:
#     1. Lease payment plan
#     2. Loan payment plan
#     3. Combined monthly payment plan
#
# Each amortization row contains:
#   Month
#   Opening Balance
#   Monthly Payment
#   Principal
#   Interest
#   Closing Balance
#
# Export:
#   Lease CSV, loan CSV, combined CSV and a simple customer quotation
#   can be downloaded directly from the application.
#
# Future-ready areas:
#   PDF quotation generation
#   Company logo and branch details
#   Salesperson information
#   WhatsApp share workflow
#   Database storage
#   Multiple saved quotations
#   Login and user roles
#   Approval workflow
#   Customer signature
#   Printable customer-only page
#   Graphical balance / interest charts
#
# Production reminder:
#   The calculator is an estimate. Official company charges, approval,
#   insurance conditions and applicable terms must be confirmed before
#   a binding quotation is issued.
#
# ============================================================


# ------------------------------------------------------------
# REFERENCE 1: INPUT VALIDATION
# ------------------------------------------------------------
# This section documents the intended behaviour of the
# input validation component.
# The implementation is kept separate from the business logic
# wherever possible so the application can be maintained easily.
# Changes to business rules should be made in calculate_finance()
# and then reflected in the labels shown to the user.
# Customer-facing screens should remain simple and readable.
# Internal screens may show detailed charges and calculations.
# Payment plans should always use the same principal, rate and
# term that produced the displayed EMI.
# Exported schedules should preserve the numeric values so they
# can be reused in spreadsheets or reporting systems.
# ------------------------------------------------------------

# ------------------------------------------------------------
# REFERENCE 2: FINANCE LIMIT
# ------------------------------------------------------------
# This section documents the intended behaviour of the
# finance limit component.
# The implementation is kept separate from the business logic
# wherever possible so the application can be maintained easily.
# Changes to business rules should be made in calculate_finance()
# and then reflected in the labels shown to the user.
# Customer-facing screens should remain simple and readable.
# Internal screens may show detailed charges and calculations.
# Payment plans should always use the same principal, rate and
# term that produced the displayed EMI.
# Exported schedules should preserve the numeric values so they
# can be reused in spreadsheets or reporting systems.
# ------------------------------------------------------------

# ------------------------------------------------------------
# REFERENCE 3: LEASE ALLOCATION
# ------------------------------------------------------------
# This section documents the intended behaviour of the
# lease allocation component.
# The implementation is kept separate from the business logic
# wherever possible so the application can be maintained easily.
# Changes to business rules should be made in calculate_finance()
# and then reflected in the labels shown to the user.
# Customer-facing screens should remain simple and readable.
# Internal screens may show detailed charges and calculations.
# Payment plans should always use the same principal, rate and
# term that produced the displayed EMI.
# Exported schedules should preserve the numeric values so they
# can be reused in spreadsheets or reporting systems.
# ------------------------------------------------------------

# ------------------------------------------------------------
# REFERENCE 4: LOAN ALLOCATION
# ------------------------------------------------------------
# This section documents the intended behaviour of the
# loan allocation component.
# The implementation is kept separate from the business logic
# wherever possible so the application can be maintained easily.
# Changes to business rules should be made in calculate_finance()
# and then reflected in the labels shown to the user.
# Customer-facing screens should remain simple and readable.
# Internal screens may show detailed charges and calculations.
# Payment plans should always use the same principal, rate and
# term that produced the displayed EMI.
# Exported schedules should preserve the numeric values so they
# can be reused in spreadsheets or reporting systems.
# ------------------------------------------------------------

# ------------------------------------------------------------
# REFERENCE 5: DOCUMENT CHARGE
# ------------------------------------------------------------
# This section documents the intended behaviour of the
# document charge component.
# The implementation is kept separate from the business logic
# wherever possible so the application can be maintained easily.
# Changes to business rules should be made in calculate_finance()
# and then reflected in the labels shown to the user.
# Customer-facing screens should remain simple and readable.
# Internal screens may show detailed charges and calculations.
# Payment plans should always use the same principal, rate and
# term that produced the displayed EMI.
# Exported schedules should preserve the numeric values so they
# can be reused in spreadsheets or reporting systems.
# ------------------------------------------------------------

# ------------------------------------------------------------
# REFERENCE 6: COMMISSION
# ------------------------------------------------------------
# This section documents the intended behaviour of the
# commission component.
# The implementation is kept separate from the business logic
# wherever possible so the application can be maintained easily.
# Changes to business rules should be made in calculate_finance()
# and then reflected in the labels shown to the user.
# Customer-facing screens should remain simple and readable.
# Internal screens may show detailed charges and calculations.
# Payment plans should always use the same principal, rate and
# term that produced the displayed EMI.
# Exported schedules should preserve the numeric values so they
# can be reused in spreadsheets or reporting systems.
# ------------------------------------------------------------

# ------------------------------------------------------------
# REFERENCE 7: INSURANCE
# ------------------------------------------------------------
# This section documents the intended behaviour of the
# insurance component.
# The implementation is kept separate from the business logic
# wherever possible so the application can be maintained easily.
# Changes to business rules should be made in calculate_finance()
# and then reflected in the labels shown to the user.
# Customer-facing screens should remain simple and readable.
# Internal screens may show detailed charges and calculations.
# Payment plans should always use the same principal, rate and
# term that produced the displayed EMI.
# Exported schedules should preserve the numeric values so they
# can be reused in spreadsheets or reporting systems.
# ------------------------------------------------------------

# ------------------------------------------------------------
# REFERENCE 8: LEASE EMI
# ------------------------------------------------------------
# This section documents the intended behaviour of the
# lease emi component.
# The implementation is kept separate from the business logic
# wherever possible so the application can be maintained easily.
# Changes to business rules should be made in calculate_finance()
# and then reflected in the labels shown to the user.
# Customer-facing screens should remain simple and readable.
# Internal screens may show detailed charges and calculations.
# Payment plans should always use the same principal, rate and
# term that produced the displayed EMI.
# Exported schedules should preserve the numeric values so they
# can be reused in spreadsheets or reporting systems.
# ------------------------------------------------------------

# ------------------------------------------------------------
# REFERENCE 9: LOAN EMI
# ------------------------------------------------------------
# This section documents the intended behaviour of the
# loan emi component.
# The implementation is kept separate from the business logic
# wherever possible so the application can be maintained easily.
# Changes to business rules should be made in calculate_finance()
# and then reflected in the labels shown to the user.
# Customer-facing screens should remain simple and readable.
# Internal screens may show detailed charges and calculations.
# Payment plans should always use the same principal, rate and
# term that produced the displayed EMI.
# Exported schedules should preserve the numeric values so they
# can be reused in spreadsheets or reporting systems.
# ------------------------------------------------------------

# ------------------------------------------------------------
# REFERENCE 10: AMORTIZATION
# ------------------------------------------------------------
# This section documents the intended behaviour of the
# amortization component.
# The implementation is kept separate from the business logic
# wherever possible so the application can be maintained easily.
# Changes to business rules should be made in calculate_finance()
# and then reflected in the labels shown to the user.
# Customer-facing screens should remain simple and readable.
# Internal screens may show detailed charges and calculations.
# Payment plans should always use the same principal, rate and
# term that produced the displayed EMI.
# Exported schedules should preserve the numeric values so they
# can be reused in spreadsheets or reporting systems.
# ------------------------------------------------------------

# ------------------------------------------------------------
# REFERENCE 11: CUSTOMER VIEW
# ------------------------------------------------------------
# This section documents the intended behaviour of the
# customer view component.
# The implementation is kept separate from the business logic
# wherever possible so the application can be maintained easily.
# Changes to business rules should be made in calculate_finance()
# and then reflected in the labels shown to the user.
# Customer-facing screens should remain simple and readable.
# Internal screens may show detailed charges and calculations.
# Payment plans should always use the same principal, rate and
# term that produced the displayed EMI.
# Exported schedules should preserve the numeric values so they
# can be reused in spreadsheets or reporting systems.
# ------------------------------------------------------------

# ------------------------------------------------------------
# REFERENCE 12: COMBINED PAYMENT PLAN
# ------------------------------------------------------------
# This section documents the intended behaviour of the
# combined payment plan component.
# The implementation is kept separate from the business logic
# wherever possible so the application can be maintained easily.
# Changes to business rules should be made in calculate_finance()
# and then reflected in the labels shown to the user.
# Customer-facing screens should remain simple and readable.
# Internal screens may show detailed charges and calculations.
# Payment plans should always use the same principal, rate and
# term that produced the displayed EMI.
# Exported schedules should preserve the numeric values so they
# can be reused in spreadsheets or reporting systems.
# ------------------------------------------------------------

# ------------------------------------------------------------
# REFERENCE 13: CSV EXPORT
# ------------------------------------------------------------
# This section documents the intended behaviour of the
# csv export component.
# The implementation is kept separate from the business logic
# wherever possible so the application can be maintained easily.
# Changes to business rules should be made in calculate_finance()
# and then reflected in the labels shown to the user.
# Customer-facing screens should remain simple and readable.
# Internal screens may show detailed charges and calculations.
# Payment plans should always use the same principal, rate and
# term that produced the displayed EMI.
# Exported schedules should preserve the numeric values so they
# can be reused in spreadsheets or reporting systems.
# ------------------------------------------------------------

# ------------------------------------------------------------
# REFERENCE 14: QUOTATION ID
# ------------------------------------------------------------
# This section documents the intended behaviour of the
# quotation id component.
# The implementation is kept separate from the business logic
# wherever possible so the application can be maintained easily.
# Changes to business rules should be made in calculate_finance()
# and then reflected in the labels shown to the user.
# Customer-facing screens should remain simple and readable.
# Internal screens may show detailed charges and calculations.
# Payment plans should always use the same principal, rate and
# term that produced the displayed EMI.
# Exported schedules should preserve the numeric values so they
# can be reused in spreadsheets or reporting systems.
# ------------------------------------------------------------

# ------------------------------------------------------------
# REFERENCE 15: RESPONSIVE UI
# ------------------------------------------------------------
# This section documents the intended behaviour of the
# responsive ui component.
# The implementation is kept separate from the business logic
# wherever possible so the application can be maintained easily.
# Changes to business rules should be made in calculate_finance()
# and then reflected in the labels shown to the user.
# Customer-facing screens should remain simple and readable.
# Internal screens may show detailed charges and calculations.
# Payment plans should always use the same principal, rate and
# term that produced the displayed EMI.
# Exported schedules should preserve the numeric values so they
# can be reused in spreadsheets or reporting systems.
# ------------------------------------------------------------

# ------------------------------------------------------------
# REFERENCE 16: CUSTOMER-FACING DESIGN
# ------------------------------------------------------------
# This section documents the intended behaviour of the
# customer-facing design component.
# The implementation is kept separate from the business logic
# wherever possible so the application can be maintained easily.
# Changes to business rules should be made in calculate_finance()
# and then reflected in the labels shown to the user.
# Customer-facing screens should remain simple and readable.
# Internal screens may show detailed charges and calculations.
# Payment plans should always use the same principal, rate and
# term that produced the displayed EMI.
# Exported schedules should preserve the numeric values so they
# can be reused in spreadsheets or reporting systems.
# ------------------------------------------------------------

# ------------------------------------------------------------
# REFERENCE 17: INTERNAL CALCULATION
# ------------------------------------------------------------
# This section documents the intended behaviour of the
# internal calculation component.
# The implementation is kept separate from the business logic
# wherever possible so the application can be maintained easily.
# Changes to business rules should be made in calculate_finance()
# and then reflected in the labels shown to the user.
# Customer-facing screens should remain simple and readable.
# Internal screens may show detailed charges and calculations.
# Payment plans should always use the same principal, rate and
# term that produced the displayed EMI.
# Exported schedules should preserve the numeric values so they
# can be reused in spreadsheets or reporting systems.
# ------------------------------------------------------------

# ------------------------------------------------------------
# REFERENCE 18: FUTURE PDF EXPORT
# ------------------------------------------------------------
# This section documents the intended behaviour of the
# future pdf export component.
# The implementation is kept separate from the business logic
# wherever possible so the application can be maintained easily.
# Changes to business rules should be made in calculate_finance()
# and then reflected in the labels shown to the user.
# Customer-facing screens should remain simple and readable.
# Internal screens may show detailed charges and calculations.
# Payment plans should always use the same principal, rate and
# term that produced the displayed EMI.
# Exported schedules should preserve the numeric values so they
# can be reused in spreadsheets or reporting systems.
# ------------------------------------------------------------

# ------------------------------------------------------------
# REFERENCE 19: FUTURE DATABASE
# ------------------------------------------------------------
# This section documents the intended behaviour of the
# future database component.
# The implementation is kept separate from the business logic
# wherever possible so the application can be maintained easily.
# Changes to business rules should be made in calculate_finance()
# and then reflected in the labels shown to the user.
# Customer-facing screens should remain simple and readable.
# Internal screens may show detailed charges and calculations.
# Payment plans should always use the same principal, rate and
# term that produced the displayed EMI.
# Exported schedules should preserve the numeric values so they
# can be reused in spreadsheets or reporting systems.
# ------------------------------------------------------------

# ------------------------------------------------------------
# REFERENCE 20: FUTURE WHATSAPP SHARE
# ------------------------------------------------------------
# This section documents the intended behaviour of the
# future whatsapp share component.
# The implementation is kept separate from the business logic
# wherever possible so the application can be maintained easily.
# Changes to business rules should be made in calculate_finance()
# and then reflected in the labels shown to the user.
# Customer-facing screens should remain simple and readable.
# Internal screens may show detailed charges and calculations.
# Payment plans should always use the same principal, rate and
# term that produced the displayed EMI.
# Exported schedules should preserve the numeric values so they
# can be reused in spreadsheets or reporting systems.
# ------------------------------------------------------------
