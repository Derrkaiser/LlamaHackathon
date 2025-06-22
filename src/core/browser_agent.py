#!/usr/bin/env python3
"""
Browser Automation Agent - Executes browser actions synchronized with avatar presentation
"""

import asyncio
import time
import re
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from playwright.async_api import async_playwright, Browser, Page
import logging

@dataclass
class BrowserAction:
    """Represents a browser action with timing and parameters"""
    action_type: str
    selector: Optional[str] = None
    text: Optional[str] = None
    url: Optional[str] = None
    wait_time: float = 2.0
    description: str = ""

class BrowserAgent:
    """Browser automation agent for synchronized demos"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.is_running = False
        self.current_action = None
        self.action_history = []
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    async def initialize(self):
        """Initialize browser and page"""
        
        try:
            self.playwright = await async_playwright().start()
            
            # Launch browser in visible mode for demo
            self.browser = await self.playwright.chromium.launch(
                headless=False,  # Visible for demo
                args=[
                    '--start-maximized',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor'
                ]
            )
            
            # Create new page
            self.page = await self.browser.new_page()
            
            # Set viewport
            await self.page.set_viewport_size({"width": 1920, "height": 1080})
            
            # Navigate to base URL
            await self.page.goto(self.base_url)
            
            self.is_running = True
            self.logger.info(f"🌐 Browser agent initialized for: {self.base_url}")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize browser agent: {e}")
            raise
    
    async def execute_action(self, action_description: str) -> bool:
        """Execute a browser action based on description"""
        
        if not self.is_running or not self.page:
            self.logger.error("Browser agent not initialized")
            return False
        
        try:
            self.current_action = action_description
            self.logger.info(f"🤖 Executing: {action_description}")
            
            # Parse action description
            action = self._parse_action(action_description)
            
            if not action:
                self.logger.warning(f"⚠️ Could not parse action: {action_description}")
                return False
            
            # Execute the action
            success = await self._execute_parsed_action(action)
            
            if success:
                self.action_history.append({
                    "description": action_description,
                    "action": action,
                    "timestamp": time.time(),
                    "success": True
                })
                self.logger.info(f"✅ Action completed: {action_description}")
            else:
                self.logger.error(f"❌ Action failed: {action_description}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"❌ Action execution error: {e}")
            return False
    
    def _parse_action(self, description: str) -> Optional[BrowserAction]:
        """Parse action description into structured action"""
        
        description_lower = description.lower()
        
        # Click actions
        if any(word in description_lower for word in ['click', 'press', 'tap']):
            selector = self._extract_selector(description)
            return BrowserAction(
                action_type="click",
                selector=selector,
                description=description
            )
        
        # Type actions
        elif any(word in description_lower for word in ['type', 'enter', 'input', 'fill']):
            selector = self._extract_selector(description)
            text = self._extract_text(description)
            return BrowserAction(
                action_type="type",
                selector=selector,
                text=text,
                description=description
            )
        
        # Navigate actions
        elif any(word in description_lower for word in ['navigate', 'go to', 'visit', 'open']):
            url = self._extract_url(description)
            return BrowserAction(
                action_type="navigate",
                url=url,
                description=description
            )
        
        # Wait actions
        elif any(word in description_lower for word in ['wait', 'pause', 'delay']):
            wait_time = self._extract_wait_time(description)
            return BrowserAction(
                action_type="wait",
                wait_time=wait_time,
                description=description
            )
        
        # Scroll actions
        elif any(word in description_lower for word in ['scroll', 'scroll down', 'scroll up']):
            direction = "down" if "down" in description_lower else "up"
            return BrowserAction(
                action_type="scroll",
                text=direction,
                description=description
            )
        
        return None
    
    def _extract_selector(self, description: str) -> str:
        """Extract CSS selector from description"""
        
        # Common patterns
        patterns = [
            r'button.*?["\']([^"\']+)["\']',  # button with text
            r'link.*?["\']([^"\']+)["\']',    # link with text
            r'field.*?["\']([^"\']+)["\']',   # field with text
            r'["\']([^"\']+)["\']',           # anything in quotes
            r'#([a-zA-Z0-9_-]+)',             # ID selector
            r'\.([a-zA-Z0-9_-]+)',            # class selector
        ]
        
        for pattern in patterns:
            match = re.search(pattern, description, re.IGNORECASE)
            if match:
                return match.group(1)
        
        # Fallback selectors based on common elements
        if 'login' in description.lower():
            return 'input[type="email"], input[name="email"], input[name="username"]'
        elif 'password' in description.lower():
            return 'input[type="password"]'
        elif 'submit' in description.lower():
            return 'button[type="submit"], input[type="submit"]'
        elif 'menu' in description.lower():
            return 'nav, .menu, .navigation'
        elif 'dashboard' in description.lower():
            return '.dashboard, #dashboard, [data-testid="dashboard"]'
        
        return 'button, a, input'  # Generic fallback
    
    def _extract_text(self, description: str) -> str:
        """Extract text to type from description"""
        
        # Look for text in quotes
        match = re.search(r'["\']([^"\']+)["\']', description)
        if match:
            return match.group(1)
        
        # Common test data
        if 'email' in description.lower() or 'username' in description.lower():
            return 'demo@example.com'
        elif 'password' in description.lower():
            return 'demo123'
        elif 'name' in description.lower():
            return 'Demo User'
        
        return 'demo'
    
    def _extract_url(self, description: str) -> str:
        """Extract URL from description"""
        
        # Look for URL patterns
        url_pattern = r'https?://[^\s]+'
        match = re.search(url_pattern, description)
        if match:
            return match.group(0)
        
        # Look for path patterns
        path_pattern = r'/([a-zA-Z0-9/_-]+)'
        match = re.search(path_pattern, description)
        if match:
            return self.base_url + match.group(0)
        
        # Common paths
        if 'dashboard' in description.lower():
            return self.base_url + '/dashboard'
        elif 'login' in description.lower():
            return self.base_url + '/login'
        elif 'home' in description.lower():
            return self.base_url + '/'
        
        return self.base_url
    
    def _extract_wait_time(self, description: str) -> float:
        """Extract wait time from description"""
        
        # Look for time patterns
        time_patterns = [
            r'(\d+)\s*seconds?',
            r'(\d+)\s*s',
            r'(\d+)\s*minutes?',
            r'(\d+)\s*m'
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, description, re.IGNORECASE)
            if match:
                value = int(match.group(1))
                if 'minute' in pattern or 'm' in pattern:
                    return value * 60
                return value
        
        return 2.0  # Default wait time
    
    async def _execute_parsed_action(self, action: BrowserAction) -> bool:
        """Execute a parsed browser action"""
        
        try:
            if action.action_type == "click":
                return await self._click_action(action)
            elif action.action_type == "type":
                return await self._type_action(action)
            elif action.action_type == "navigate":
                return await self._navigate_action(action)
            elif action.action_type == "wait":
                return await self._wait_action(action)
            elif action.action_type == "scroll":
                return await self._scroll_action(action)
            else:
                self.logger.warning(f"⚠️ Unknown action type: {action.action_type}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Action execution error: {e}")
            return False
    
    async def _click_action(self, action: BrowserAction) -> bool:
        """Execute click action"""
        
        try:
            if action.selector:
                # Try to find and click the element
                element = await self.page.query_selector(action.selector)
                if element:
                    await element.click()
                    await self.page.wait_for_timeout(1000)  # Wait for click to register
                    return True
                else:
                    # Try clicking by text content
                    await self.page.click(f"text={action.selector}")
                    await self.page.wait_for_timeout(1000)
                    return True
            else:
                # Generic click on first clickable element
                await self.page.click('button, a, [role="button"]')
                await self.page.wait_for_timeout(1000)
                return True
                
        except Exception as e:
            self.logger.error(f"❌ Click action failed: {e}")
            return False
    
    async def _type_action(self, action: BrowserAction) -> bool:
        """Execute type action"""
        
        try:
            if action.selector and action.text:
                # Clear and type
                await self.page.fill(action.selector, "")
                await self.page.type(action.selector, action.text)
                await self.page.wait_for_timeout(500)
                return True
            else:
                self.logger.warning("⚠️ Type action missing selector or text")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Type action failed: {e}")
            return False
    
    async def _navigate_action(self, action: BrowserAction) -> bool:
        """Execute navigate action"""
        
        try:
            if action.url:
                await self.page.goto(action.url)
                await self.page.wait_for_load_state("networkidle")
                return True
            else:
                self.logger.warning("⚠️ Navigate action missing URL")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Navigate action failed: {e}")
            return False
    
    async def _wait_action(self, action: BrowserAction) -> bool:
        """Execute wait action"""
        
        try:
            await self.page.wait_for_timeout(int(action.wait_time * 1000))
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Wait action failed: {e}")
            return False
    
    async def _scroll_action(self, action: BrowserAction) -> bool:
        """Execute scroll action"""
        
        try:
            if action.text == "down":
                await self.page.evaluate("window.scrollBy(0, 500)")
            else:
                await self.page.evaluate("window.scrollBy(0, -500)")
            
            await self.page.wait_for_timeout(1000)
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Scroll action failed: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        
        return {
            "is_running": self.is_running,
            "current_action": self.current_action,
            "action_history": self.action_history,
            "base_url": self.base_url
        }
    
    async def cleanup(self):
        """Clean up browser resources"""
        
        try:
            if self.page:
                await self.page.close()
            if self.browser:
                await self.browser.close()
            if hasattr(self, 'playwright'):
                await self.playwright.stop()
            
            self.is_running = False
            self.logger.info("🧹 Browser agent cleaned up")
            
        except Exception as e:
            self.logger.error(f"❌ Cleanup error: {e}")

# Example usage
if __name__ == "__main__":
    async def test_browser_agent():
        agent = BrowserAgent("https://example.com")
        await agent.initialize()
        
        # Test actions
        actions = [
            "Click on the login button",
            "Enter email 'demo@example.com'",
            "Enter password 'demo123'",
            "Click submit",
            "Wait 3 seconds",
            "Navigate to dashboard"
        ]
        
        for action in actions:
            success = await agent.execute_action(action)
            print(f"Action: {action} - {'✅' if success else '❌'}")
            await asyncio.sleep(2)
        
        await agent.cleanup()
    
    # Run test
    asyncio.run(test_browser_agent()) 