#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["approvaltests", "pickle"]
# ///

import pickle
import inspect
from typing import List, Callable, Any
from pathlib import Path
from approvaltests import verify, verify_binary, Namer, Options


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
    
    # Use approvaltests to verify pickle data
    pickled_data = pickle.dumps(cache_data, protocol=pickle.HIGHEST_PROTOCOL)
    
    class PickleNamer(Namer):
        def get_approved_filename(self, base=None):
            return f"{fn_file_name}-{fn_name}.approved.pickle"
        
        def get_received_filename(self, base=None):
            return f"{fn_file_name}-{fn_name}.received.pickle"
    
    # Create human-readable format for approval testing
    human_readable = f"Function: {cache_data['function']}\n"
    human_readable += f"File: {cache_data['file']}\n"
    human_readable += "-" * 50 + "\n"
    
    for entry in cache_data['results']:
        if 'error' in entry:
            human_readable += f"Args: {entry['args']} -> ERROR: {entry['error']}\n"
        else:
            human_readable += f"Args: {entry['args']} -> Result: {entry['result']}\n"
    
    class TextNamer(Namer):
        def get_approved_filename(self, base=None):
            return f"{fn_file_name}-{fn_name}.approved.txt"
        
        def get_received_filename(self, base=None):
            return f"{fn_file_name}-{fn_name}.received.txt"
    
    # Collect any approval exceptions to raise at the end
    exceptions = []
    
    # Verify binary pickle data
    try:
        pickle_options = Options().with_namer(PickleNamer())
        verify_binary(pickled_data, ".pickle", options=pickle_options)
    except Exception as e:
        exceptions.append(e)
    
    # Verify human-readable text
    try:
        text_options = Options().with_namer(TextNamer())
        verify(human_readable, options=text_options)
    except Exception as e:
        exceptions.append(e)
    
    # If any verifications failed, raise the first exception
    if exceptions:
        raise exceptions[0]