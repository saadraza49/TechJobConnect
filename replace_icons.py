import os
import re

html_dir = r"d:\Programming\techjobconnect\static"

emoji_map = {
    "🏠": "home",
    "📋": "list_alt",
    "👥": "group",
    "📊": "bar_chart",
    "💬": "chat",
    "⚙️": "settings",
    "🔔": "notifications",
    "🔍": "search",
    "🏢": "apartment",
    "❤️": "favorite",
    "✏️": "edit",
    "👤": "person",
    "📄": "description",
    "💼": "work",
    "⚡": "bolt",
    "🎨": "palette",
    "🚀": "rocket_launch",
    "🐙": "code_blocks",
    "🌍": "public",
    "⏰": "schedule",
    "✨": "auto_awesome",
    "←": "arrow_back"
}

css_link = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" />'

for file in os.listdir(html_dir):
    if file.endswith(".html"):
        filepath = os.path.join(html_dir, file)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Add Material Symbols Outlined link if not present
        if "Material+Symbols+Outlined" not in content:
            content = content.replace("<head>", f"<head>\n  {css_link}")
            
        # Replace <span>emoji</span> blocks first to avoid wrapping them twice
        for emoji, icon in emoji_map.items():
            content = content.replace(f"<span>{emoji}</span>", f'<span class="material-symbols-outlined">{icon}</span>')
            
            # Now replace raw emojis that aren't wrapped in spans (except checkmark, which is text usually)
            # Actually, to be safe, we wrap them in spans.
            # But wait, we used `✓` directly in text. Let's just wrap the rest.
            content = content.replace(f"{emoji}", f'<span class="material-symbols-outlined" style="font-size: 1.25em; vertical-align: middle;">{icon}</span>')

        # Fix up "✓" manually:
        content = content.replace("✓", f'<span class="material-symbols-outlined" style="font-size: 1.2em; vertical-align: middle;">check</span>')

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

print("Icons replaced successfully!")
