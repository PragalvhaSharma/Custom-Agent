class ToolBox:
    def __init__(self):
        self.tools_dict = {}
        
    #Takes in a list of functions and then returns a dictionary with the function names as keys and their docstrings as values
    def store(self, functions_list):
        """
        Stores the literal name and docstring of each function in the list.

        Parameters:
        functions_list (list): List of function objects to store.

        Returns:
        dict: Dictionary with function names as keys and their docstrings as values.
        """
        for func in functions_list: #Iterating through functions
            self.tools_dict[func.__name__] = func.__doc__ #Function as key and docstring as value then return that in a dictionary
        return self.tools_dict
    
    #Simply reutnrs the dictionary made above as a string (To insert back into the prompt as a list of tools)
    def tools(self):
        """
        Returns the dictionary created in store as a text string.

        Returns:
        str: Dictionary of stored functions and their docstrings as a text string.
        """
        tools_str = ""
        for name, doc in self.tools_dict.items():
            tools_str += f"{name}: \"{doc}\"\n"
        return tools_str.strip()