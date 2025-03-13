class SessionLayer:
    def __init__(self):
        self.session_active = False

    def start_session(self):
        """Starts a communication session."""
        self.session_active = True
        print("[Session Layer] Session Started.")

    def end_session(self):
        """Ends the communication session."""
        self.session_active = False
        print("[Session Layer] Session Ended.")

    def encapsulate(self, data):
        """Adds session state information."""
        return f"SESSION_START|{data}|SESSION_END"

    def decapsulate(self, data):
        """Removes session state information."""
        if data.startswith("SESSION_START|") and data.endswith("|SESSION_END"):
            print("[Session Layer] Session Active. Processing Data.")
            return data[len("SESSION_START|"):-len("|SESSION_END")]
        return None
