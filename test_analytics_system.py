#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pytest", "approvaltests"]
# ///

from parrot import verify_parrot, parrot
from analytics_system import (
    AnalyticsReportGenerator, 
    DataValidator, 
    MetricsCalculator,
    DataAggregator,
    ReportFormatter,
    ReportingService
)
from unittest.mock import patch, MagicMock
from approvaltests import verify, Options
from approvaltests.inline.inline_options import InlineOptions


def test_generate_summary_with_verify_parrot():
    """
    First, we record the AnalyticsReportGenerator.generate_summary behavior.
    We create simplified versions of dependencies just for recording.
    """
    
    # Create minimal dependencies for testing
    # These are simplified versions that work for our test cases
    validator = DataValidator(None, None, None)
    calculator = MetricsCalculator(None, None, None)
    aggregator = DataAggregator(None, None, None)
    formatter = ReportFormatter(None, None, None)
    
    # Create the generator with our simplified dependencies
    generator = AnalyticsReportGenerator(validator, calculator, aggregator, formatter)
    
    # Test data sets - each inner list is the arguments for one call
    test_data_sets = [
        # Valid data with multiple categories
        [[
            {"category": "sales", "value": 100},
            {"category": "sales", "value": 150},
            {"category": "costs", "value": 50},
            {"category": "costs", "value": 60},
        ]],
        # Single category data
        [[
            {"category": "revenue", "value": 200},
            {"category": "revenue", "value": 250},
            {"category": "revenue", "value": 300},
        ]],
        # Empty data (invalid)
        [[]],
        # Data with negative values (invalid)
        [[
            {"category": "profit", "value": 100},
            {"category": "profit", "value": -50},
        ]],
        # Data without categories
        [[
            {"value": 75},
            {"value": 85},
        ]],
    ]
    
    # Record the behavior
    verify_parrot(generator.generate_summary, test_data_sets)


def test_reporting_service_with_stubbed_init():
    """
    Test ReportingService which creates AnalyticsReportGenerator internally.
    We stub the __init__ to avoid complex instantiation and use parrot for generate_summary.
    """
    
    # Create a dummy generator to get the generate_summary method
    dummy_generator = AnalyticsReportGenerator(None, None, None, None)
    
    # Stub all the complex class __init__ methods to avoid their real initialization
    with patch.object(DataValidator, '__init__', return_value=None):
        with patch.object(MetricsCalculator, '__init__', return_value=None):
            with patch.object(DataAggregator, '__init__', return_value=None):
                with patch.object(ReportFormatter, '__init__', return_value=None):
                    with patch.object(AnalyticsReportGenerator, '__init__', return_value=None):
                        # Use parrot for the class method by patching it directly
                        with parrot(AnalyticsReportGenerator.generate_summary):
                            # Now test ReportingService
                            service = ReportingService()
                            
                            # Test with valid data
                            month_data = [
                                {"category": "sales", "value": 100},
                                {"category": "sales", "value": 150},
                                {"category": "costs", "value": 50},
                                {"category": "costs", "value": 60},
                            ]
                            
                            result = service.create_monthly_report(month_data)
                            assert result["status"] == "success"
                            assert "sales" in result["summary"]
                            assert "costs" in result["summary"]


def test_reporting_service_with_approval():
    """
    Multi-category report:
    Status: success
    Categories: ['sales', 'costs']
    
    Single category report:
    Status: success
    Categories: ['revenue']
    
    Empty data report:
    Status: error
    Message: Invalid data
    """
    
    # Stub all __init__ methods
    with patch.object(DataValidator, '__init__', return_value=None):
        with patch.object(MetricsCalculator, '__init__', return_value=None):
            with patch.object(DataAggregator, '__init__', return_value=None):
                with patch.object(ReportFormatter, '__init__', return_value=None):
                    with patch.object(AnalyticsReportGenerator, '__init__', return_value=None):
                        with parrot(AnalyticsReportGenerator.generate_summary):
                            service = ReportingService()
                            
                            # Test various scenarios
                            test_cases = [
                                {
                                    "name": "Multi-category report",
                                    "data": [
                                        {"category": "sales", "value": 100},
                                        {"category": "sales", "value": 150},
                                        {"category": "costs", "value": 50},
                                        {"category": "costs", "value": 60},
                                    ]
                                },
                                {
                                    "name": "Single category report",
                                    "data": [
                                        {"category": "revenue", "value": 200},
                                        {"category": "revenue", "value": 250},
                                        {"category": "revenue", "value": 300},
                                    ]
                                },
                                {
                                    "name": "Empty data report",
                                    "data": []
                                },
                            ]
                            
                            results = []
                            for test_case in test_cases:
                                result = service.create_monthly_report(test_case["data"])
                                results.append(f"{test_case['name']}:\nStatus: {result['status']}")
                                if result["status"] == "success":
                                    results.append(f"Categories: {list(result['summary'].keys())}")
                                else:
                                    results.append(f"Message: {result.get('message', 'N/A')}")
                                results.append("")  # Empty line for readability
                            
                            verify("\n".join(results), options=Options().inline(InlineOptions.automatic()))


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])