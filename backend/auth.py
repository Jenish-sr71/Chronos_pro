import hashlib
import hmac
import json
import os

import streamlit as st

from .constants import ACCOUNTS_FILE

# Default used only for local dev when nothing else is configured, so the
# app doesn't crash the first time you run it. Anything deployed publicly
# should override this — see _signup_key() below.
_FALLBACK_DEV_KEY = "changeme"


def _signup_key():
    """Resolves the current invite key, checked in this order:

    1. Streamlit secrets — st.secrets["SIGNUP_KEY"]. This is the intended
       path for Streamlit Community Cloud: set it in the app's Secrets
       panel, and it never touches the git repo, so a public GitHub repo
       doesn't leak it.
    2. CHRONOS_SIGNUP_KEY environment variable — useful for local runs or
       other hosts that pass config via env vars instead of Streamlit
       secrets.
    3. A hardcoded fallback — only ever used if neither of the above is
       set, so the signup form still works out of the box on a laptop.
       Never rely on this in a real deployment.
    """
    try:
        secret_key = st.secrets.get("SIGNUP_KEY")
        if secret_key:
            return str(secret_key)
    except Exception:
        pass

    env_key = os.environ.get("CHRONOS_SIGNUP_KEY")
    if env_key:
        return env_key

    return _FALLBACK_DEV_KEY


def _using_fallback_key():
    return _signup_key() == _FALLBACK_DEV_KEY


def _hash(password):
    return hashlib.sha256(password.encode()).hexdigest()


def _static_users():
    """Admin-provisioned accounts set in Streamlit Cloud's Secrets panel.
    These always survive a container restart — unlike self-signup accounts
    below, which live in a local file."""
    try:
        return dict(st.secrets.get("USERS", {}))
    except Exception:
        return {}


def _load_accounts():
    """Self-signed-up accounts: {username: password_hash}.

    NOTE — Streamlit Community Cloud's local filesystem does not survive
    a container restart (the app sleeping from inactivity, a redeploy, a
    crash). Accounts created here can be lost when that happens; accounts
    added via Streamlit secrets (USERS) cannot. If that risk matters to
    you, ask me to wire this up to a real external datastore instead.
    """
    if not os.path.exists(ACCOUNTS_FILE):
        return {}
    try:
        with open(ACCOUNTS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def _save_accounts(accounts):
    os.makedirs(os.path.dirname(ACCOUNTS_FILE), exist_ok=True)
    with open(ACCOUNTS_FILE, "w") as f:
        json.dump(accounts, f, indent=2)


def _all_usernames():
    return set(_static_users()) | set(_load_accounts())


def _check_password(username, password):
    static = _static_users()
    if username in static:
        return hmac.compare_digest(str(static[username]), password)
    accounts = _load_accounts()
    if username in accounts:
        return hmac.compare_digest(accounts[username], _hash(password))
    return False


def _create_account(username, password):
    accounts = _load_accounts()
    accounts[username] = _hash(password)
    _save_accounts(accounts)


def require_login():
    if st.session_state.get("chronos_user"):
        return

    st.markdown("## ⏳ Chronos")
    tab_login, tab_signup = st.tabs(["Sign in", "Create account"])

    with tab_login:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Sign in", key="login_btn"):
            if _check_password(username, password):
                st.session_state.chronos_user = username
                st.rerun()
            else:
                st.error("Wrong username or password.")

    with tab_signup:
        st.caption("Ask whoever runs this app for the access key.")
        if _using_fallback_key():
            st.warning(
                "No SIGNUP_KEY is configured in secrets or the environment — "
                "using the local dev default. Set one before deploying "
                "publicly (see backend/auth.py).",
                icon="⚠️",
            )
        new_user = st.text_input("Choose a username", key="signup_user")
        new_pass = st.text_input("Choose a password", type="password", key="signup_pass")
        key = st.text_input("Access key", type="password", key="signup_key")
        if st.button("Create account", key="signup_btn"):
            if not hmac.compare_digest(key, _signup_key()):
                st.error("Wrong access key.")
            elif not new_user or not new_pass:
                st.error("Username and password can't be empty.")
            elif new_user in _all_usernames():
                st.error("That username is already taken.")
            else:
                _create_account(new_user, new_pass)
                st.session_state.chronos_user = new_user
                st.success("Account created!")
                st.rerun()

    st.stop()


def current_user():
    return st.session_state.get("chronos_user", "default")


def render_account_footer():
    with st.sidebar:
        st.caption(f"Signed in as **{current_user()}**")
        if st.button("Log out", key="logout_btn"):
            del st.session_state["chronos_user"]
            st.rerun()
