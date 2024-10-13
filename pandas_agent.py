import pandas as pd
import ast
import inspect

class PandasAgent:
    def __init__(self, dataframe):
        self.df = dataframe

    def execute(self, code_line):
        # Create a local namespace with the DataFrame
        local_vars = {'df': self.df}
        
        try:
            # Parse the code line into an AST
            parsed = ast.parse(code_line, mode='eval')
            
            # Compile the AST
            compiled_code = compile(parsed, '<string>', 'eval')
            
            # Execute the compiled code
            result = eval(compiled_code, globals(), local_vars)
            
            # Update the internal DataFrame if the result is a DataFrame
            if isinstance(result, pd.DataFrame):
                self.df = result
            
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    def get_dataframe(self):
        return self.df

    def describe_dataframe(self):
        return self.df.describe()

    def get_column_names(self):
        return self.df.columns.tolist()

    def get_available_methods(self):
        return [method for method in dir(pd.DataFrame) if not method.startswith('_')]
