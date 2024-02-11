import time

class RateLimiter:
    def __init__(self, max_requests, window_time):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the instance variables that will be used by other methods in this class.
        
        
        :param self: Represent the instance of the class
        :param max_requests: Set the maximum number of requests that can be made within a given time window
        :param window_time: Determine the time window to check for requests
        :return: The object itself, not a value
        :doc-author: Trelent
        """
        self.requests = {}
        self.max_requests = max_requests
        self.window_time = window_time

    def is_allowed(self, client_id):
        """
        The is_allowed function takes in a client_id and returns True if the client is allowed to make another request,
        and False otherwise. The function keeps track of how many requests each client has made within a window of time.
        If the number of requests exceeds max_requests within that window, then the function will return False for that 
        client until enough time has passed.
        
        :param self: Represent the instance of the class
        :param client_id: Identify the client making the request
        :return: True if the client_id exists in the self
        :doc-author: Trelent
        """
        current_time = time.time()
        request_info = self.requests.get(client_id)

        if request_info is None:
            self.requests[client_id] = [current_time, 1]
            return True

        last_request_time, request_count = request_info

        if current_time - last_request_time > self.window_time:
            self.requests[client_id] = [current_time, 1]
            return True

        if request_count < self.max_requests:
            self.requests[client_id][1] += 1
            return True

        return False