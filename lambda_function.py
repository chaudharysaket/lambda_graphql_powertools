import requests
from aws_lambda_powertools import Logger, Tracer, Metrics
from aws_lambda_powertools.metrics import MetricUnit

logger = Logger(service="countries_service")
tracer = Tracer(service="countries_service")
metrics = Metrics(namespace="CountriesAPI", service="countries_service")

query = """
{
  country(code: "US") {
    name
    capital
    currency
    languages {
      name
    }
  }
}
"""

@metrics.log_metrics(capture_cold_start_metric=True)
@tracer.capture_lambda_handler
@logger.inject_lambda_context
def lambda_handler(event, context):
    logger.info("Handling request to fetch country data")
    
    url = "https://countries.trevorblades.com/"
    try:
        response = requests.post(url, json={"query": query})
        response.raise_for_status()
        
        data = response.json()
        logger.info("Successfully fetched country data", extra={"response": data})
        
        metrics.add_metric(name="SuccessfulGraphQLRequest", unit=MetricUnit.Count, value=1)
        
        return {
            "statusCode": 200,
            "body": data
        }
    except requests.RequestException as e:
        logger.error("Failed to fetch country data", exc_info=e)
        
        metrics.add_metric(name="FailedGraphQLRequest", unit=MetricUnit.Count, value=1)
        
        return {
            "statusCode": 500,
            "body": {"error": str(e)}
        }
