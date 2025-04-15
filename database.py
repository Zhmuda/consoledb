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
                return layer[key] if layer[key] is not None else self.NULL_VALUE
        return self.NULL_VALUE

    def _get_effective_state(self) -> dict:
        result = {}
        for layer in self.stack:
            for k, v in layer.items():
                if v is None:
                    result.pop(k, None)
                else:
                    result[k] = v
        return result

    def set_command(self, args: List[str]) -> None:
        if len(args) != 2:
            print("ERROR: SET requires 2 arguments.")
            return
        key, value = args
        self.stack[-1][key] = value

    def get_command(self, args: List[str]) -> None:
        if len(args) != 1:
            print("ERROR: GET requires 1 argument.")
            return
        key = args[0]
        print(self._get_value(key))

    def unset_command(self, args: List[str]) -> None:
        if len(args) != 1:
            print("ERROR: UNSET requires 1 argument.")
            return
        key = args[0]
        self.stack[-1][key] = None

    def counts_command(self, args: List[str]) -> None:
        if len(args) != 1:
            print("ERROR: COUNTS requires 1 argument.")
            return
        value = args[0]
        state = self._get_effective_state()
        count = sum(1 for v in state.values() if v == value)
        print(count)

    def find_command(self, args: List[str]) -> None:
        if len(args) != 1:
            print("ERROR: FIND requires 1 argument.")
            return
        value = args[0]
        state = self._get_effective_state()
        keys = [k for k, v in state.items() if v == value]
        print(" ".join(sorted(keys)) if keys else self.NULL_VALUE)

    def begin_command(self, args: List[str]) -> None:
        self.stack.append({})

    def rollback_command(self, args: List[str]) -> None:
        if len(self.stack) > 1:
            self.stack.pop()
        else:
            print("NO TRANSACTION")

    def commit_command(self, args: List[str]) -> None:
        if len(self.stack) <= 1:
            print("NO TRANSACTION")
            return

        current = self.stack.pop()
        for key, value in current.items():
            if value is None:
                self.stack[-1].pop(key, None)
            else:
                self.stack[-1][key] = value

    def run(self):
        while True:
            try:
                line = input("> ").strip()
                if not line:
                    continue
                if line == "END":
                    break
                parts = line.split()
                cmd = parts[0]
                args = parts[1:]
                if cmd in self.commands:
                    self.commands[cmd](args)
                else:
                    print(f"ERROR: Unknown command '{cmd}'")
            except EOFError:
                break
            except Exception as e:
                print(f"ERROR: {e}")


if __name__ == "__main__":
    db = Database()
    db.run()
