import logging
from typing import List
import json
import os

from dotenv import load_dotenv
from anthropic import Anthropic
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_exponential
from app.utils.prompts import MEMORY_CATEGORIZATION_PROMPT

load_dotenv()
anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


class MemoryCategories(BaseModel):
    categories: List[str]


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=15))
def get_categories_for_memory(memory: str) -> List[str]:
    """
    Get categories for memory using Claude via MCP server.
    This function expects Claude to be handling the categorization.
    """
    try:
        # Import here to avoid circular imports
        import requests
        import json
        
        # Call the MCP categorize_memory tool
        # Note: This is a simplified approach - in practice, the categorization
        # would happen when Claude calls the categorize_memory tool
        
        # For now, let's use a simple heuristic categorization
        # This will be replaced when Claude handles it directly
        categories = []
        
        memory_lower = memory.lower()
        
        # Simple keyword-based categorization
        if any(word in memory_lower for word in ['work', 'job', 'office', 'meeting', 'project', 'company']):
            categories.append('work')
        if any(word in memory_lower for word in ['family', 'friend', 'personal', 'home']):
            categories.append('personal')
        if any(word in memory_lower for word in ['like', 'prefer', 'favorite', 'love', 'hate', 'dislike']):
            categories.append('preferences')
        if any(word in memory_lower for word in ['health', 'exercise', 'diet', 'sleep', 'medical']):
            categories.append('health')
        if any(word in memory_lower for word in ['travel', 'trip', 'vacation', 'visit']):
            categories.append('travel')
        if any(word in memory_lower for word in ['learn', 'study', 'course', 'education', 'school']):
            categories.append('education')
        if any(word in memory_lower for word in ['money', 'finance', 'budget', 'expense', 'income']):
            categories.append('finance')
        if any(word in memory_lower for word in ['buy', 'shop', 'purchase', 'order']):
            categories.append('shopping')
        if any(word in memory_lower for word in ['movie', 'music', 'book', 'game', 'entertainment']):
            categories.append('entertainment')
        if any(word in memory_lower for word in ['ai', 'technology', 'code', 'programming', 'tech']):
            categories.append('technology')
            
        logging.info(f"Simple categorization for '{memory[:50]}...': {categories}")
        return categories or ['general']  # Default to 'general' if no categories found
        
    except Exception as e:
        logging.error(f"Error in categorization: {e}")
        return ['general']  # Default category on error
