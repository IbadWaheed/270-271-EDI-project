import json
import os
from _270_271  import *
from _270_271._271Parser import _271Parser
from _270_271._271Parser import *

def main(file_path):
   
    if not os.path.exists(file_path):
        print(f"File '{file_path}' not found.")
        return
    
    
    parser = _271Parser()
    
    try:
       
        parsed_data = parser.parse_271_file(file_path)
        
        
        base_file_name = os.path.splitext(file_path)[0]  
        json_file_path = f"{base_file_name}_output.json" 
        
      
        parsed_data_json = [obj_to_dict(data) for data in parsed_data]
        
       
        with open(json_file_path, 'w') as json_file:
            json.dump(parsed_data_json, json_file, indent=4, cls=DateTimeEncoder)
        
        print(f"Parsed data successfully written to {json_file_path}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

def obj_to_dict(obj):
    
    if hasattr(obj, 'to_dict'):
        return obj.to_dict()
    elif hasattr(obj, '__dict__'):
        return {key: obj_to_dict(value) for key, value in obj.__dict__.items()}
    elif isinstance(obj, list):
        return [obj_to_dict(item) for item in obj]
    else:
        return obj

if __name__ == "__main__":
   
    input_file = 'SAMPLE_271_WITHOUT_PHI.271'
    main(input_file)
