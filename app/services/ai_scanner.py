"""
CryptoShield Guardian AI Scanner
FBI-grade scam intelligence engine powered by OpenAI
"""
import os
import json
import logging
from typing import Dict, Any
from openai import AsyncOpenAI

logger = logging.getLogger(__name__)

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4o-mini"

async def analyze_text(text: str) -> Dict[str, Any]:
    """
    Analyze text for scam patterns using OpenAI GPT-4
    
    Args:
        text: The text to analyze
        
    Returns:
        Dict containing scam analysis results matching frontend format
    """
    print("=" * 80)
    print("ANALYZE TEXT ENGINE INPUT:", text[:200])
    print("OPENAI KEY EXISTS:", "OPENAI_API_KEY" in os.environ)
    print("=" * 80)
    
    if not os.getenv("OPENAI_API_KEY"):
        logger.error("OPENAI_API_KEY not found in environment")
        return {
            "error": "OPENAI_API_KEY not configured",
            "danger_score": 0,
            "risk_level": "UNKNOWN",
            "scam_probability": 0.0,
            "archetype": "Unknown",
            "emotional_tone": {
                "anger": 0.0,
                "gaslighting": 0.0,
                "seduction": 0.0,
                "threatening": 0.0,
                "calm_manipulation": 0.0
            },
            "manipulation_timeline": [],
            "summary": "OpenAI API key not configured",
            "recommended_actions": ["Configure OPENAI_API_KEY in environment variables"]
        }
    
    prompt = f"""You are CryptoShield Guardian AI, an FBI-grade scam intelligence engine.
Analyze the following communication for fraud, manipulation, threats, coercion, or scam behavior.

Return ONLY valid JSON with this exact structure (no markdown, no code blocks, just raw JSON):

{{
  "danger_score": <0-100>,
  "risk_level": "LOW" | "MEDIUM" | "HIGH" | "CRITICAL",
  "scam_probability": <0-1>,
  "archetype": "<scammer type>",
  "emotional_tone": {{
      "anger": <0-1>,
      "gaslighting": <0-1>,
      "seduction": <0-1>,
      "threatening": <0-1>,
      "calm_manipulation": <0-1>
  }},
  "manipulation_timeline": [
      {{
          "timestamp": <integer milliseconds>,
          "label": "<emotion/manipulation type>",
          "intensity": <0-1>
      }}
  ],
  "summary": "<short summary>",
  "recommended_actions": [
      "<action 1>",
      "<action 2>"
  ]
}}

Text to analyze:
{text}"""

    try:
        logger.info(f"Calling OpenAI API with model {MODEL}")
        
        response = await client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            timeout=30.0
        )
        
        content = response.choices[0].message.content
        logger.info(f"OpenAI response received: {len(content)} characters")
        
        content = content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        result = json.loads(content)
        
        logger.info(f"Successfully parsed AI response: danger_score={result.get('danger_score')}, risk_level={result.get('risk_level')}")
        
        return result
        
    except json.JSONDecodeError as e:
        error_msg = f"Failed to parse OpenAI response as JSON: {str(e)}"
        logger.error(error_msg)
        logger.error(f"Raw content: {content[:500]}")
        return {
            "error": error_msg,
            "raw_response": content[:500],
            "danger_score": 0,
            "risk_level": "UNKNOWN",
            "scam_probability": 0.0,
            "archetype": "Unknown",
            "emotional_tone": {
                "anger": 0.0,
                "gaslighting": 0.0,
                "seduction": 0.0,
                "threatening": 0.0,
                "calm_manipulation": 0.0
            },
            "manipulation_timeline": [],
            "summary": "Failed to parse AI response",
            "recommended_actions": ["Review error logs"]
        }
        
    except Exception as e:
        error_msg = f"OpenAI API error: {str(e)}"
        logger.error(error_msg)
        logger.exception("Full exception details:")
        return {
            "error": error_msg,
            "danger_score": 0,
            "risk_level": "UNKNOWN",
            "scam_probability": 0.0,
            "archetype": "Unknown",
            "emotional_tone": {
                "anger": 0.0,
                "gaslighting": 0.0,
                "seduction": 0.0,
                "threatening": 0.0,
                "calm_manipulation": 0.0
            },
            "manipulation_timeline": [],
            "summary": f"Analysis failed: {str(e)}",
            "recommended_actions": ["Check OpenAI API key and quota"]
        }
