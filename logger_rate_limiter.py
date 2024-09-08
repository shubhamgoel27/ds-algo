class Logger:
    """
    A rate-limiting logger that allows messages to be printed only once every 10 seconds.

    This logger keeps track of messages and their timestamps to prevent the same message
    from being printed too frequently.
    """

    def __init__(self):
        # Dictionary to store messages and their last printed timestamp
        self.messages = {}

    def shouldPrintMessage(self, timestamp: int, message: str) -> bool:
        """
        Determines whether a message should be printed based on its timestamp.

        Args:
            timestamp (int): The current timestamp in seconds.
            message (str): The message to be logged.

        Returns:
            bool: True if the message should be printed, False otherwise.
        """
        if message in self.messages:
            if timestamp < self.messages[message] + 10:
                return False  # Message was printed less than 10 seconds ago
        
        # Update the timestamp for this message
        self.messages[message] = timestamp
        return True  # Message can be printed


# Test cases
def run_tests():
    logger = Logger()
    
    # Test case 1: First occurrence of a message
    assert logger.shouldPrintMessage(1, "Hello") == True
    
    # Test case 2: Same message within 10 seconds
    assert logger.shouldPrintMessage(2, "Hello") == False
    
    # Test case 3: Same message after 10 seconds
    assert logger.shouldPrintMessage(11, "Hello") == True
    
    # Test case 4: Different messages
    assert logger.shouldPrintMessage(3, "World") == True
    assert logger.shouldPrintMessage(8, "Hello") == False
    assert logger.shouldPrintMessage(10, "World") == False
    
    print("All test cases passed!")

# Run the tests
run_tests()

# Your Logger object will be instantiated and called as such:
# obj = Logger()
# param_1 = obj.shouldPrintMessage(timestamp, message)