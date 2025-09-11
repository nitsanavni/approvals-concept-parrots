#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["approvaltests", "pickle"]
# ///

import pickle
import inspect
import json
from typing import List, Callable, Any
from pathlib import Path
from approvaltests import verify, Namer


def verify_parrot(fn: Callable, args: List[List]) -> None:
    fn_module = inspect.getmodule(fn)
    fn_file = inspect.getfile(fn) if fn_module else "unknown"
    fn_name = fn.__name__
    
    fn_file_path = Path(fn_file)
    fn_file_name = fn_file_path.stem if fn_file_path.name != "unknown" else "unknown"
    
    cache_data = {
        "function": f"{fn_file_name}.{fn_name}",
        "file": str(fn_file),
        "results": []
    }
    
    for arg_list in args:
        try:
            result = fn(*arg_list)
            cache_data["results"].append({
                "args": arg_list,
                "result": result
            })
        except Exception as e:
            cache_data["results"].append({
                "args": arg_list,
                "error": str(e)
            })
    
    # Save pickle file
    pickle_file = Path(f"{fn_file_name}-{fn_name}.pickle")
    with open(pickle_file, 'wb') as f:
        pickle.dump(cache_data, f, protocol=pickle.HIGHEST_PROTOCOL)
    
    # Create human-readable format for approval testing
    human_readable = f"Function: {cache_data['function']}\n"
    human_readable += f"File: {cache_data['file']}\n"
    human_readable += "-" * 50 + "\n"
    
    for entry in cache_data['results']:
        if 'error' in entry:
            human_readable += f"Args: {entry['args']} -> ERROR: {entry['error']}\n"
        else:
            human_readable += f"Args: {entry['args']} -> Result: {entry['result']}\n"
    
    class CustomNamer(Namer):
        def get_approved_filename(self, base=None):
            return f"{fn_file_name}-{fn_name}.approved.txt"
        
        def get_received_filename(self, base=None):
            return f"{fn_file_name}-{fn_name}.received.txt"
    
    verify(human_readable, namer=CustomNamer())