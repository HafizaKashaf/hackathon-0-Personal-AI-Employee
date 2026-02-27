"""
Orchestrator

Main process that triggers the AI assistant (Qwen/Claude Code) to process 
items in the Needs_Action folder. This is the "brain" coordinator for the
Personal AI Employee system.

For Bronze Tier: Simple file-based triggering
For Silver/Gold Tier: Integrate with Ralph Wiggum loop
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime
import logging


class Orchestrator:
    """
    Orchestrates AI processing of action items.
    
    The orchestrator:
    1. Checks for items in Needs_Action folder
    2. Triggers AI (Qwen/Claude Code) to process them
    3. Updates the Dashboard
    4. Logs all activities
    
    Note: This system works with any AI assistant:
    - Qwen (this implementation)
    - Claude Code (alternative)
    - Any other LLM with CLI access
    """
    
    def __init__(self, vault_path: str):
        """
        Initialize the orchestrator.
        
        Args:
            vault_path: Path to the Obsidian vault root
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.done = self.vault_path / 'Done'
        self.plans = self.vault_path / 'Plans'
        self.logs = self.vault_path / 'Logs'
        self.dashboard = self.vault_path / 'Dashboard.md'
        self.handbook = self.vault_path / 'Company_Handbook.md'
        
        # Ensure directories exist
        self.needs_action.mkdir(parents=True, exist_ok=True)
        self.done.mkdir(parents=True, exist_ok=True)
        self.plans.mkdir(parents=True, exist_ok=True)
        self.logs.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self._setup_logging()
        
    def _setup_logging(self):
        """Configure logging."""
        log_file = self.logs / f'orchestrator_{datetime.now().strftime("%Y-%m-%d")}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('Orchestrator')
    
    def get_pending_items(self) -> list:
        """
        Get all .md files in Needs_Action that need processing.
        
        Returns:
            List of Path objects for pending action files
        """
        pending = []
        for f in self.needs_action.iterdir():
            if f.is_file() and f.suffix == '.md':
                pending.append(f)
        return sorted(pending, key=lambda x: x.stat().st_mtime)
    
    def count_items(self) -> dict:
        """
        Count items in various folders.
        
        Returns:
            Dictionary with counts
        """
        return {
            'needs_action': len(list(self.needs_action.glob('*.md'))),
            'done_today': len([f for f in self.done.iterdir() 
                              if f.is_file() and self._is_today(f)]),
            'plans': len(list(self.plans.iterdir())),
        }
    
    def _is_today(self, file_path: Path) -> bool:
        """Check if file was modified today."""
        today = datetime.now().date()
        mtime = datetime.fromtimestamp(file_path.stat().st_mtime).date()
        return mtime == today
    
    def update_dashboard(self, counts: dict):
        """
        Update the Dashboard.md with current stats.
        
        Args:
            counts: Dictionary with item counts
        """
        if not self.dashboard.exists():
            self.logger.warning('Dashboard.md not found!')
            return
        
        content = self.dashboard.read_text(encoding='utf-8')
        
        # Update timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Update stats in dashboard
        lines = content.split('\n')
        new_lines = []
        in_stats = False
        
        for line in lines:
            if '| Pending Actions |' in line:
                new_lines.append(f'| Pending Actions | {counts["needs_action"]} |')
            elif '| In Progress |' in line:
                new_lines.append(f'| In Progress | {counts["plans"]} |')
            elif '| Completed Today |' in line:
                new_lines.append(f'| Completed Today | {counts["done_today"]} |')
            elif '*No recent activity*' in line and counts['needs_action'] > 0:
                new_lines.append(f'- {timestamp}: {counts["needs_action"]} item(s) pending')
            else:
                new_lines.append(line)
        
        # Add last processed timestamp
        new_content = '\n'.join(new_lines)
        if '*Last processed:' in new_content:
            new_content = new_content.split('*Last processed:')[0] + f'*Last processed: {timestamp}'
        
        self.dashboard.write_text(new_content, encoding='utf-8')
        self.logger.info('Dashboard updated')
    
    def trigger_ai(self, prompt: str, ai_type: str = 'qwen') -> bool:
        """
        Trigger AI assistant to process items.
        
        Args:
            prompt: The prompt to give the AI
            ai_type: 'qwen' or 'claude'
            
        Returns:
            True if successful, False otherwise
        """
        self.logger.info(f'Triggering AI ({ai_type})...')
        
        if ai_type == 'claude':
            cmd = ['claude', '--cwd', str(self.vault_path), prompt]
        else:
            # For Qwen: Create a prompt file that user can reference
            # Qwen integration happens through the chat interface
            prompt_file = self.vault_path / 'Updates' / 'ai_prompt.txt'
            prompt_file.parent.mkdir(parents=True, exist_ok=True)
            prompt_file.write_text(prompt, encoding='utf-8')
            self.logger.info(f'Prompt written to: {prompt_file}')
            self.logger.info('To process with Qwen, share the vault context and ask me to process files')
            return True
        
        try:
            self.logger.info(f'Running: {" ".join(cmd)}')
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=300
            )
            
            if result.returncode == 0:
                self.logger.info(f'AI completed successfully')
                if result.stdout:
                    self.logger.info(f'Output: {result.stdout[:500]}...')
            else:
                self.logger.error(f'AI exit code: {result.returncode}')
                if result.stderr:
                    self.logger.error(f'Error: {result.stderr}')
            
            return result.returncode == 0
        except FileNotFoundError:
            self.logger.error(f'{ai_type.upper()} not found')
            if ai_type == 'claude':
                self.logger.info('Install: npm install -g @anthropic/claude-code')
            return False
        except subprocess.TimeoutExpired:
            self.logger.error('AI timed out after 5 minutes')
            return False
        except Exception as e:
            self.logger.error(f'Error triggering AI: {e}')
            return False
    
    def log_action(self, action_type: str, details: str):
        """
        Log an action to the logs folder.
        
        Args:
            action_type: Type of action (process, move, create, etc.)
            details: Details of the action
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action_type,
            'details': details
        }
        
        log_file = self.logs / f'{datetime.now().strftime("%Y-%m-%d")}.jsonl'
        
        with open(log_file, 'a') as f:
            import json
            f.write(json.dumps(log_entry) + '\n')
    
    def run_once(self, ai_type: str = 'qwen'):
        """
        Run a single processing cycle.
        
        Check for pending items and trigger AI if found.
        
        Args:
            ai_type: 'qwen' or 'claude'
        """
        pending = self.get_pending_items()
        counts = self.count_items()
        
        self.logger.info(f'Found {len(pending)} pending item(s)')
        self.update_dashboard(counts)
        
        if pending:
            # Build prompt for AI
            files = ', '.join([f.name for f in pending])
            prompt = f"""Process the following files in /Needs_Action: {files}

For each file:
1. Read and understand what action is needed
2. Check Company_Handbook.md for rules
3. Create a Plan.md if multiple steps are needed
4. Execute simple actions or create approval requests for sensitive ones
5. Move completed items to /Done

Reference the Company Handbook for decision-making rules."""
            
            self.trigger_ai(prompt, ai_type)
            self.log_action('trigger_ai', f'Processing {len(pending)} files with {ai_type}')
        else:
            self.logger.info('No pending items to process')
        
        return len(pending)
    
    def run_continuous(self, check_interval: int = 60, ai_type: str = 'qwen'):
        """
        Run continuously, checking for items periodically.
        
        Args:
            check_interval: Seconds between checks
            ai_type: 'qwen' or 'claude'
        """
        import time
        
        self.logger.info(f'Starting continuous mode with {ai_type} (interval: {check_interval}s)')
        
        try:
            while True:
                self.run_once(ai_type)
                time.sleep(check_interval)
        except KeyboardInterrupt:
            self.logger.info('Orchestrator stopped by user')


if __name__ == '__main__':
    # Get vault path from command line or use default
    if len(sys.argv) > 1:
        vault_path = sys.argv[1]
    else:
        # Default: parent directory (the vault root)
        vault_path = str(Path(__file__).parent.parent)
        print(f"Using default vault path: {vault_path}")
    
    # Get AI type (qwen or claude)
    ai_type = sys.argv[2] if len(sys.argv) > 2 else 'qwen'
    
    orchestrator = Orchestrator(vault_path)
    
    # Run mode based on arguments
    if len(sys.argv) > 3 and sys.argv[3] == '--continuous':
        interval = int(sys.argv[4]) if len(sys.argv) > 4 else 60
        orchestrator.run_continuous(interval, ai_type)
    else:
        # Run once
        orchestrator.run_once(ai_type)
