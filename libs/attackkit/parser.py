class AttackParser:
    """Parse ATT&CK JSON data (stub)."""

    def __init__(self, path: str | None = None):
        self.path = path
        self.data = {}
        if path:
            self.load(path)

    def load(self, path: str) -> None:
        """Load data from given JSON path."""
        self.path = path
        try:
            import json
            with open(path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = {}

    def get_techniques(self) -> list:
        """Return list of technique IDs."""
        if not self.data:
            return []
        return [obj.get('id') for obj in self.data.get('objects', []) if obj.get('type') == 'attack-pattern']
