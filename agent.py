from termcolor import colored
from prompts import agent_system_prompt_template
from models.openaiModel import OpenAIModel
from models.ollamaModel import OllamaModel
from tools.basicCalculator import basic_calculator
from tools.reverser import reverse_string
from toolbox import ToolBox


class Agent:
    def __init__(self, tools, model_service, model_name, stop=None):
        """
        Initializes the agent with a list of tools and a model.

        Parameters:
        tools (list): List of tool functions.
        model_service (class): The model service class with a generate_text method.
        model_name (str): The name of the model to use.
        """
        self.tools = tools
        self.model_service = model_service
        self.model_name = model_name
        self.stop = stop
        
    def prepare_tools(self):
        """
        Stores the tools in the toolbox and returns their descriptions.

        Returns:
        str: Descriptions of the tools stored in the toolbox.
        """
        toolbox = ToolBox() #Storing tools and getting their tool descriptions
        toolbox.store(self.tools)
        tool_descriptions = toolbox.tools()
        return tool_descriptions
    
    #Using the LLM
    def think(self, prompt):
        """
        Runs the generate_text method on the model using the system prompt template and tool descriptions.

        Parameters:
        prompt (str): The user query to generate a response for.

        Returns:
        dict: The response from the model as a dictionary.
        """
        tool_descriptions = self.prepare_tools()
        agent_system_prompt = agent_system_prompt_template.format(tool_descriptions=tool_descriptions)

        # Create an instance of the model service with the system prompt
        
        #Need to return a stop token if using OllamaClass
        if self.model_service == OllamaModel:
            model_instance = self.model_service(
                model=self.model_name,
                system_prompt=agent_system_prompt,
                temperature=0,
                stop=self.stop
            )
        
        #No need to return a stop token if using OpenAI
        else:
            model_instance = self.model_service(
                model=self.model_name,
                system_prompt=agent_system_prompt,
                temperature=0
            )

        # Generate and return the response dictionary
        agent_response_dict = model_instance.generate_text(prompt)
        return agent_response_dict
    
    #Execute the functions that we may have selected from toolbox
    def work(self, prompt):
        """
        Parses the dictionary returned from think and executes the appropriate tool.

        Parameters:
        prompt (str): The user query to generate a response for.

        Returns:
        The response from executing the appropriate tool or the tool_input if no matching tool is found.
        """
        agent_response_dict = self.think(prompt)
        tool_choice = agent_response_dict.get("tool_choice")
        tool_input = agent_response_dict.get("tool_input")

        for tool in self.tools:
            
            #If we are choosing to use a took
            if tool.__name__ == tool_choice:
                
                #execute the tool
                response = tool(tool_input)

                print(colored(response, 'cyan'))
                return
                # return tool(tool_input)

        print(colored(tool_input, 'cyan'))
        
        return


# Example usage
if __name__ == "__main__":

    tools = [basic_calculator, reverse_string]


    #Eunning with OpenAI
    model_service = OpenAIModel
    model_name = 'gpt-3.5-turbo'
    stop = None

    # # Uncomment below to run with Ollama
    # model_service = OllamaModel
    # model_name = 'llama3:instruct'
    # stop = "<|eot_id|>"

    agent = Agent(tools=tools, model_service=model_service, model_name=model_name, stop=stop)

    while True:
        prompt = input("Ask me anything: ")
        if prompt.lower() == "exit":
            break
    
        agent.work(prompt)