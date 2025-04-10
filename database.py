from typing import List

class Database:
    NULL_VALUE = "NULL"

    def __init__(self):
        self.stack = [{}]
        self.commands = {
            "SET": self.set_command,
            "GET": self.get_command,
            "UNSET": self.unset_command,
            "COUNTS": self.counts_command,
            "FIND": self.find_command,
            "BEGIN": self.begin_command,
            "ROLLBACK": self.rollback_command,
            "COMMIT": self.commit_command,
        }

    def _get_value(self, key: str) -> str:
        for layer in reversed(self.stack):
            if key in layer:
                value = layer[key]
                return value if value is not None else self.NULL_VALUE

        return self.NULL_VALUE

    def set_command(self, args: List[str]) -> None:
        key, value = args
        self.stack[-1][key] = value

    def get_command(self, args: List[str]) -> None:
        key = args[0]
        print(self._get_value(key))

    def unset_command(self, args: List[str]) -> None:
        key = args[0]
        self.stack[-1][key] = None

    def counts_command(self, args: List[str]) -> None:
        value = args[0]
        all_keys = set()
        for layer in self.stack:
            all_keys.update(layer.keys())

        count = sum(1 for key in all_keys if self._get_value(key) == value)
        print(count)

    def find_command(self, args: List[str]) -> None:
        value = args[0]
        all_keys = set()
        for layer in self.stack:
            all_keys.update(layer.keys())

        keys = [key for key in all_keys if self._get_value(key) == value]
        print(" ".join(sorted(keys)) if keys else self.NULL_VALUE)

    def begin_command(self, args: List[str]) -> None:
        self.stack.append({})

    def rollback_command(self, args: List[str]) -> None:
        if len(self.stack) > 1:
            self.stack.pop()

    def commit_command(self, args: List[str]) -> None:
        if len(self.stack) > 1:
            current = self.stack.pop()

            for key, value in current.items():
                if value is None:
                    if key in self.stack[-1]:
                        del self.stack[-1][key]
                else:
                    self.stack[-1][key] = value

    def run(self):
        while True:
            try:
                line = input("> ").strip()
                if line == "END":
                    break
                parts = line.split()
                cmd = parts[0]
                args = parts[1:]
                if cmd in self.commands:
                    self.commands[cmd](args)
            except EOFError:
                break


if __name__ == "__main__":
    db = Database()
    db.run()
