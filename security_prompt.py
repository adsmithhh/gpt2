"""
SecurityPrompt class for representing and working with security prompt data.
"""
import json
from typing import List, Optional


class SecurityPrompt:
    """Represents a security prompt with input text and label classification."""
    
    def __init__(self, input_text: str, label: str):
        """
        Initialize a SecurityPrompt instance.
        
        Args:
            input_text (str): The prompt input text
            label (str): The security label/classification (e.g., 'injection', 'phishing', 'payload')
        """
        self.input = input_text
        self.label = label
    
    def __repr__(self) -> str:
        """
        Return a string representation of the SecurityPrompt.
        
        Returns:
            str: A readable representation showing the prompt type and truncated input
        """
        # Truncate input text if it's too long for readability
        truncated_input = self.input[:50] + "..." if len(self.input) > 50 else self.input
        return f"SecurityPrompt(label='{self.label}', input='{truncated_input}')"
    
    def __str__(self) -> str:
        """Return a user-friendly string representation."""
        return f"[{self.label.upper()}] {self.input}"
    
    def __eq__(self, other) -> bool:
        """Check equality based on input and label."""
        if not isinstance(other, SecurityPrompt):
            return False
        return self.input == other.input and self.label == other.label
    
    def to_dict(self) -> dict:
        """Convert the SecurityPrompt to a dictionary."""
        return {"input": self.input, "label": self.label}
    
    @classmethod
    def from_dict(cls, data: dict) -> 'SecurityPrompt':
        """
        Create a SecurityPrompt from a dictionary.
        
        Args:
            data (dict): Dictionary with 'input' and 'label' keys
            
        Returns:
            SecurityPrompt: New instance created from the dictionary
        """
        return cls(data["input"], data["label"])
    
    @classmethod
    def load_from_jsonl(cls, file_path: str) -> List['SecurityPrompt']:
        """
        Load security prompts from a JSONL file.
        
        Args:
            file_path (str): Path to the JSONL file
            
        Returns:
            List[SecurityPrompt]: List of SecurityPrompt instances
        """
        prompts = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:  # Skip empty lines
                        continue
                    try:
                        data = json.loads(line)
                        if 'input' in data and 'label' in data:
                            prompts.append(cls.from_dict(data))
                        else:
                            print(f"Warning: Line {line_num} missing 'input' or 'label' field")
                    except json.JSONDecodeError as e:
                        print(f"Warning: Invalid JSON on line {line_num}: {e}")
        except FileNotFoundError:
            print(f"Error: File {file_path} not found")
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
        
        return prompts
    
    def is_security_threat(self) -> bool:
        """
        Check if this prompt represents a security threat.
        
        Returns:
            bool: True if the prompt is classified as a security threat
        """
        threat_labels = {'injection', 'phishing', 'payload', 'jailbreak', 'override'}
        return self.label.lower() in threat_labels