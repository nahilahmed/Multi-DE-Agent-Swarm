from agents.finder_agent import FinderAgent
from agents.transformer_agent import TransformerAgent
from agents.validator_agent import ValidatorAgent
from agents.loader_agent import LoaderAgent

class OrchestratorAgent:
    def __init__(self):
        self.finder = FinderAgent("./data/messy_sales.csv")
        self.transformer = TransformerAgent()
        self.validator = ValidatorAgent()
        self.loader = LoaderAgent()

    def execute(self):
        print("Orchestrator: Asking Finder Agent to read file...")
        raw_data = self.finder.read_file()
        
        print("Orchestrator: Asking Transformer Agent to clean data...")
        cleaned_data = self.transformer.clean_data(raw_data)

        print("Orchestrator: Transformer Agent responded with cleaned data:")
        print(cleaned_data)

        print("Orchestrator: Asking Validator Agent to validate data...")
        validation_result = self.validator.validate_data(cleaned_data)

        print("Orchestrator: Validator Agent response:")
        print(validation_result)

        if not validation_result["is_valid"]:
            print("Data Validation Failed. Stopping pipeline.")
        
        print("Orchestrator: Asking Loader Agent to load data into Postgres...")
        load_result = self.loader.load_data(cleaned_data)

        print("Orchestrator: Loader Agent response:")
        print(load_result)