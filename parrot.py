import pickle
import inspect
from typing import List, Callable, Any, Optional, Dict
from pathlib import Path
from approvaltests import verify, verify_binary, Namer, Options
from unittest.mock import patch

# Global registry for missing args hooks
_missing_args_hooks: List[Callable[[str, str, Any, Dict], None]] = []


def register_missing_args_hook(hook: Callable[[str, str, Any, Dict], None]) -> None:
    """Register a hook to be called when parrot encounters uncached arguments.
    
    Hook signature: (function_name: str, file_path: str, args: Any, cache_data: Dict) -> None
    """
    _missing_args_hooks.append(hook)


def clear_missing_args_hooks() -> None:
    """Clear all registered missing args hooks."""
    _missing_args_hooks.clear()


def verify_parrot(fn: Callable[..., Any], args: List[List[Any]]) -> None:
    fn_module = inspect.getmodule(fn)
    fn_file = inspect.getfile(fn) if fn_module else "unknown"
    fn_name = fn.__name__

    fn_file_path = Path(fn_file)
    fn_file_name = fn_file_path.stem if fn_file_path.name != "unknown" else "unknown"

    cache_data: dict[str, Any] = {
        "function": f"{fn_file_name}.{fn_name}",
        "file": str(Path(fn_file).relative_to(Path.cwd())),
        "results": [],
    }

    for arg_list in args:
        try:
            result = fn(*arg_list)
            cache_data["results"].append({"args": arg_list, "result": result})
        except Exception as e:
            cache_data["results"].append({"args": arg_list, "error": str(e)})

    # Use approvaltests to verify pickle data
    pickled_data = pickle.dumps(cache_data, protocol=pickle.HIGHEST_PROTOCOL)

    class PickleNamer(Namer):
        def get_approved_filename(self, base: Optional[str] = None) -> str:
            return str(Path.cwd() / f"{fn_file_name}-{fn_name}.approved.pickle")

        def get_received_filename(self, base: Optional[str] = None) -> str:
            return str(Path.cwd() / f"{fn_file_name}-{fn_name}.received.pickle")

    # Create human-readable format for approval testing
    human_readable = f"Function: {cache_data['function']}\n"
    human_readable += f"File: {cache_data['file']}\n"
    human_readable += "-" * 50 + "\n"

    for entry in cache_data["results"]:
        if "error" in entry:
            human_readable += f"Args: {entry['args']} -> ERROR: {entry.get('error')}\n"
        else:
            human_readable += (
                f"Args: {entry['args']} -> Result: {entry.get('result')}\n"
            )

    class TextNamer(Namer):
        def get_approved_filename(self, base: Optional[str] = None) -> str:
            return str(Path.cwd() / f"{fn_file_name}-{fn_name}.approved.txt")

        def get_received_filename(self, base: Optional[str] = None) -> str:
            return str(Path.cwd() / f"{fn_file_name}-{fn_name}.received.txt")

    # Collect any approval exceptions to raise at the end
    exceptions: list[Exception] = []

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


def parrot(fn: Callable[..., Any]) -> Any:
    fn_module = inspect.getmodule(fn)
    fn_file = inspect.getfile(fn) if fn_module else "unknown"
    fn_name = fn.__name__

    fn_file_path = Path(fn_file)
    fn_file_name = fn_file_path.stem if fn_file_path.name != "unknown" else "unknown"

    # Load the pickle file
    pickle_file = Path.cwd() / f"{fn_file_name}-{fn_name}.approved.pickle"

    if not pickle_file.exists():
        # Call hooks for missing cache file
        for hook in _missing_args_hooks:
            hook(fn_name, str(fn_file_path), None, {"results": []})
        raise FileNotFoundError(f"No approved pickle file found: {pickle_file}")

    with open(pickle_file, "rb") as f:
        cache_data = pickle.load(f)

    # Build lookup map from args to results
    results_map: dict[tuple[Any, ...], Any] = {}
    for entry in cache_data["results"]:
        # Convert args list to tuple for hashable key
        args_key = tuple(entry["args"])
        if "error" in entry:
            results_map[args_key] = Exception(entry["error"])
        else:
            results_map[args_key] = entry["result"]

    # Get the fully qualified name for patching
    fn_module_name = fn_module.__name__ if fn_module else "__main__"
    patch_target = f"{fn_module_name}.{fn_name}"

    def mock_fn(*call_args: Any) -> Any:
        args_key = tuple(call_args)
        if args_key not in results_map:
            # Call any registered hooks with available info
            for hook in _missing_args_hooks:
                hook(fn_name, str(pickle_file.parent / fn_file_path.name), call_args, cache_data)
            raise ValueError(f"No cached result for args: {call_args}")
        result = results_map[args_key]
        if isinstance(result, Exception):
            raise result
        return result

    # Return the patch context manager
    return patch(patch_target, side_effect=mock_fn)
