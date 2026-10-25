"""HTML building blocks for the Streamlit page. All styling lives in styles.css."""

from pathlib import Path

import streamlit as st

STYLESHEET_PATH = Path(__file__).with_name("styles.css")
APP_NAME = "Multilingual Video Translation"

# (icon, title, description, icon colour) for the "AI Pipeline" info card
FEATURES = [
    ("🎙️", "Speech-to-Text", "OpenAI Whisper — 99+ languages, near-perfect accuracy", "purple"),
    ("🌍", "Multilingual Translation", "Google Translate — context-aware, cultural nuances preserved", "cyan"),
    ("🔊", "Neural Text-to-Speech", "gTTS — natural voices, atempo-synced to original duration", "pink"),
    ("⏱️", "Audio-Video Sync", "FFmpeg time-stretch — translated audio matches original timing", "purple"),
]


def render_html(markup):
    """Render raw HTML on the page."""
    st.markdown(markup, unsafe_allow_html=True)


def load_styles():
    render_html(f"<style>{STYLESHEET_PATH.read_text(encoding='utf-8')}</style>")


def render_navbar():
    render_html(f"""
<div class="navbar">
    <div class="navbar-logo">{APP_NAME}</div>
    <div class="navbar-links">
        <span class="navbar-link active">Translate</span>
        <span class="navbar-link">How it Works</span>
        <div class="navbar-button">Try Now</div>
    </div>
</div>
""")


def render_hero():
    render_html("""
<div class="hero">
    <h1>Translate Any Video<br>Into Any Language</h1>
    <p>High-precision AI speech translation with perfectly synced audio —<br>
       powered by Whisper, Google Translate &amp; gTTS.</p>
</div>
""")


def render_progress_tracker(steps, completed_count):
    """Show one icon per step: finished steps get a tick, the next step is highlighted."""
    parts = []
    for index, step in enumerate(steps):
        if index < completed_count:
            status, icon = "done", "✓"
        elif index == completed_count:
            status, icon = "active", step.icon
        else:
            status, icon = "", step.icon

        parts.append(
            f'<div class="progress-step">'
            f'<div class="progress-icon {status}">{icon}</div>'
            f'<span class="progress-label {status}">{step.label}</span>'
            f'</div>'
        )
        if index < len(steps) - 1:
            connector_status = "done" if index < completed_count - 1 else ""
            parts.append(f'<div class="progress-connector {connector_status}"></div>')

    render_html(f'<div class="progress-tracker">{"".join(parts)}</div>')


def render_step_card(step, number, total, done):
    """Show the header card for one pipeline step (e.g. "02 / 06 · Extract Audio")."""
    card_status = "done" if done else ""
    icon_colour = "cyan" if number % 2 == 0 else ""
    render_html(f"""
<div class="step-card {card_status}">
    <span class="step-card-number">{number:02d} / {total:02d}</span>
    <div class="step-card-header">
        <div class="step-card-icon {icon_colour}">{step.icon}</div>
        <div>
            <div class="step-card-title">{step.title}</div>
            <div class="step-card-subtitle">{step.subtitle}</div>
        </div>
    </div>
</div>
""")


def render_success_badge(message):
    render_html(f'<div class="success-badge">✓ &nbsp; {message}</div>')


def render_info_panel(language_names):
    """Show the right-hand column: the pipeline's features and the supported languages."""
    features = "".join(
        f'<div class="feature">'
        f'<div class="feature-icon {colour}">{icon}</div>'
        f'<div><div class="feature-title">{title}</div>'
        f'<div class="feature-description">{description}</div></div>'
        f'</div>'
        for icon, title, description, colour in FEATURES
    )
    languages = "".join(f'<span class="language-chip">{name}</span>' for name in language_names)

    render_html(f"""
<div class="info-panel">
    <div class="info-card">
        <div class="info-card-heading">AI Pipeline</div>
        <div class="feature-list">{features}</div>
    </div>
    <div class="info-card highlight">
        <div class="info-card-heading">Supported Languages</div>
        <div class="language-list">{languages}</div>
    </div>
</div>
""")


def render_footer():
    render_html(f"""
<div class="page-footer">
    <div class="page-footer-title">{APP_NAME} AI</div>
    <p>© 2024 {APP_NAME} AI · High-precision translation technology</p>
</div>
""")
