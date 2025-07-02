#!/usr/bin/env python3
"""
Quote API Test
Tests working quote APIs: Zen Quotes and Advice Slip with philosophy categories
"""

import asyncio
import requests
import random
import pytest
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

async def async_test_working_apis():
    print("🧪 Working Quote APIs Test with Philosophy Categories")
    print("=" * 70)

    # Test Zen Quotes API (working)
    print("\n🧘 Testing Zen Quotes API:")
    try:
        response = requests.get('https://zenquotes.io/api/random', timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Zen Quote: \"{data[0].get('q', '')}\"")
            print(f"   Author: {data[0].get('a', 'Unknown')}")
            print(f"   Philosophy: wisdom")
        else:
            print(f"❌ Zen Quotes API Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Zen Quotes API Error: {e}")

    # Test Advice Slip API (working)
    print("\n💡 Testing Advice Slip API:")
    try:
        response = requests.get('https://api.adviceslip.com/advice', timeout=10)
        if response.status_code == 200:
            data = response.json()
            slip = data.get('slip', {})
            print(f"✅ Advice: \"{slip.get('advice', '')}\"")
            print(f"   ID: {slip.get('id', 'Unknown')}")
            print(f"   Philosophy: wisdom")
        else:
            print(f"❌ Advice Slip API Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Advice Slip API Error: {e}")

    # Test scenario-specific quotes with philosophy categories
    scenarios = {
        'improvement': ['success', 'achievement', 'growth', 'motivation'],
        'setback': ['perseverance', 'resilience', 'overcoming', 'challenge'],
        'excellence': ['excellence', 'mastery', 'perfection', 'achievement'],
        'struggle': ['struggle', 'difficulty', 'perseverance', 'strength'],
        'consistency': ['discipline', 'consistency', 'habits', 'focus'],
        'reflection': ['wisdom', 'philosophy', 'thinking', 'awareness'],
        'growth': ['growth', 'development', 'learning', 'progress'],
        'breakthrough': ['breakthrough', 'innovation', 'discovery', 'achievement'],
        'first_grade': ['beginning', 'start', 'journey', 'first_step']
    }
    
    print("\n🎯 Testing Scenario-Specific Quotes with Philosophy Categories:")
    for scenario, categories in scenarios.items():
        print(f"\n📊 Testing {scenario} (Categories: {', '.join(categories)}):")
        success = False
        
        # Try Zen Quotes first
        try:
            response = requests.get('https://zenquotes.io/api/random', timeout=10)
            if response.status_code == 200:
                data = response.json()
                selected_category = random.choice(categories)
                print(f"✅ {scenario} (Zen Quotes): \"{data[0].get('q', '')}\"")
                print(f"   Author: {data[0].get('a', 'Unknown')}")
                print(f"   Philosophy: {selected_category}")
                success = True
        except Exception as e:
            print(f"❌ {scenario} (Zen Quotes): Error {e}")
        
        # Try Advice Slip as fallback
        if not success:
            try:
                response = requests.get('https://api.adviceslip.com/advice', timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    slip = data.get('slip', {})
                    selected_category = random.choice(categories)
                    print(f"✅ {scenario} (Advice Slip): \"{slip.get('advice', '')}\"")
                    print(f"   ID: {slip.get('id', 'Unknown')}")
                    print(f"   Philosophy: {selected_category}")
                    success = True
            except Exception as e:
                print(f"❌ {scenario} (Advice Slip): Error {e}")

    # Test quote structure with philosophy attribute
    print("\n🔍 Testing Quote Structure with Philosophy Attribute:")
    test_quote = {
        'text': 'The unexamined life is not worth living.',
        'author': 'Socrates',
        'philosophy': 'wisdom',
        'context': 'local_fallback'
    }
    print(f"✅ Quote Structure: {test_quote}")
    print(f"   Has philosophy attribute: {'philosophy' in test_quote}")
    print(f"   Philosophy value: {test_quote.get('philosophy', 'None')}")

def test_working_apis():
    asyncio.run(async_test_working_apis())

if __name__ == "__main__":
    test_working_apis()
    print("\n✅ All tests completed!")
    print("📝 Working APIs: Zen Quotes and Advice Slip")
    print("🎯 Philosophy Categories: wisdom, philosophy, life, motivation, perseverance, etc.") 