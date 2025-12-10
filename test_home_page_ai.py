"""Quick test to verify AI buttons are on home page."""
from app import app

with app.test_client() as client:
    resp = client.get('/')
    content = resp.get_data(as_text=True)
    
    # Check for AI feature buttons
    checks = {
        "Ask Alumni button": "Ask Now" in content,
        "Resume Scorer button": "Score Resume" in content,
        "Find Mentors button": "Find Mentors" in content,
        "AI Features section": "AI-Powered Features" in content,
    }
    
    print("=" * 60)
    print("HOME PAGE AI FEATURES TEST")
    print("=" * 60)
    for check, result in checks.items():
        status = "✓" if result else "✗"
        print(f"{status} {check}")
    
    print("\n" + "=" * 60)
    if all(checks.values()):
        print("✓ All AI feature buttons are visible on home page!")
    else:
        print("✗ Some buttons are missing")
    print("=" * 60)
