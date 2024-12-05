## Test New Relic instrumentation of Lambda
Test if Lambda with `aws_lambda_powertools` and graphql is working with New Relic Lambda layer instrumentation
## Steps to deploy .zip lambda
Steps are mentioned in the [aws docs](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html) 

1. Create package folder
```
mkdir package
```
2. Install libraries
```
pip install --target ./package aws-lambda-powertools
pip install --target ./package aws_xray_sdk
pip install --target ./package requests
```
3. Create zip
```
cd package                                          
zip -r ../my_deployment_package.zip .
```
```
cd ..                                               
zip my_deployment_package.zip lambda_function.py
```
4. Use `newrelic-lambda-cli` to instrument the Lambda
```
newrelic-lambda layers install \
    --function <LambdaFunction> \
    --nr-account-id <NewRelicAccountId> \
    --aws-region <Region>
```
