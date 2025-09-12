class DataValidator:
    def __init__(self, rules_engine, error_handler, logger):
        self.rules_engine = rules_engine
        self.error_handler = error_handler
        self.logger = logger
    
    def validate(self, data):
        if not data:
            return False
        # Check if any item has negative values
        for item in data:
            if "value" in item and item["value"] < 0:
                return False
        return True


class MetricsCalculator:
    def __init__(self, formula_engine, cache_manager, precision_config):
        self.formula_engine = formula_engine
        self.cache_manager = cache_manager
        self.precision_config = precision_config
    
    def calculate_average(self, values):
        return sum(values) / len(values) if values else 0
    
    def calculate_trend(self, values):
        if len(values) < 2:
            return "stable"
        diff = values[-1] - values[0]
        if diff > 0:
            return "increasing"
        elif diff < 0:
            return "decreasing"
        return "stable"


class DataAggregator:
    def __init__(self, group_strategy, sort_manager, filter_chain):
        self.group_strategy = group_strategy
        self.sort_manager = sort_manager
        self.filter_chain = filter_chain
    
    def aggregate_by_category(self, data):
        result = {}
        for item in data:
            category = item.get("category", "uncategorized")
            if category not in result:
                result[category] = []
            result[category].append(item["value"])
        return result


class ReportFormatter:
    def __init__(self, template_engine, style_manager, localization_service):
        self.template_engine = template_engine
        self.style_manager = style_manager
        self.localization_service = localization_service
    
    def format_section(self, title, content):
        return f"=== {title} ===\n{content}\n"


class AnalyticsReportGenerator:
    def __init__(self, validator, calculator, aggregator, formatter):
        """This class is complex to instantiate due to all its dependencies"""
        self.validator = validator
        self.calculator = calculator
        self.aggregator = aggregator
        self.formatter = formatter
    
    def generate_summary(self, raw_data):
        """The method we want to test without dealing with complex instantiation"""
        # Validate data
        if not self.validator.validate(raw_data):
            return {"status": "error", "message": "Invalid data"}
        
        # Aggregate by category
        aggregated = self.aggregator.aggregate_by_category(raw_data)
        
        # Calculate metrics for each category
        summary = {}
        for category, values in aggregated.items():
            summary[category] = {
                "average": self.calculator.calculate_average(values),
                "trend": self.calculator.calculate_trend(values),
                "count": len(values)
            }
        
        # Format the result
        formatted = self.formatter.format_section("Analytics Summary", str(summary))
        
        return {
            "status": "success",
            "summary": summary,
            "formatted": formatted
        }


class ReportingService:
    def create_monthly_report(self, month_data):
        """This method creates all the complex dependencies and uses AnalyticsReportGenerator"""
        # Create all the sub-dependencies (imagine these are complex too)
        rules_engine = object()  # Complex rules engine
        error_handler = object()  # Error handling system
        logger = object()  # Logging system
        
        formula_engine = object()  # Mathematical formula processor
        cache_manager = object()  # Caching layer
        precision_config = object()  # Precision configuration
        
        group_strategy = object()  # Grouping strategies
        sort_manager = object()  # Sorting logic
        filter_chain = object()  # Filter pipeline
        
        template_engine = object()  # Template system
        style_manager = object()  # Styling configuration
        localization_service = object()  # i18n service
        
        # Create the main dependencies
        validator = DataValidator(rules_engine, error_handler, logger)
        calculator = MetricsCalculator(formula_engine, cache_manager, precision_config)
        aggregator = DataAggregator(group_strategy, sort_manager, filter_chain)
        formatter = ReportFormatter(template_engine, style_manager, localization_service)
        
        # Finally create the report generator
        generator = AnalyticsReportGenerator(validator, calculator, aggregator, formatter)
        
        # Generate the report
        return generator.generate_summary(month_data)