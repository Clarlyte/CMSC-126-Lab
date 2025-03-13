class ApplicationLayer:
    def encapsulate(self, message):
        """Prepares the user message for transmission."""
        data = f"MSG|{message}|END"
        print(f"[Application Layer] Encapsulated Data: {data}")
        return data

    def decapsulate(self, data):
        """Extracts the user message from the formatted data."""
        parts = data.split("|")
        if parts[0] == "MSG" and parts[-1] == "END":
            print(f"[Application Layer] Decapsulated Message: {parts[1]}")
            return parts[1]
        return None
