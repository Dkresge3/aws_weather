





def getClothes(testdata):
    # %pip install "pyqt5<5.16"
    # %pip install "pyqtwebengine<5.16"
    # %pip install "jupyter-server~=1.16"
    # %pip install nest-asyncio==1.5.5
    # %pip install sagemaker-data-insights==0.4.0
    # %pip install "ipython>=7.31.1,<8.0.0"
    # %pip install spyder==5.3.3
    # %pip install "pyqtwebengine<5.16"

    # %pip install --upgrade pip


    # %pip install --no-build-isolation --force-reinstall \
    #     "boto3>=1.28.57" \
    #     "awscli>=1.29.57" \
    #     "botocore>=1.31.57"

    # %pip install --quiet \
    #     langchain==0.0.309 \
    #     "transformers>=4.24,<5" \
    #     sqlalchemy -U \
    #     "faiss-cpu>=1.7,<2" \
    #     "pypdf>=3.8,<4" \
    #     pinecone-client \
    #     apache-beam \
    #     datasets \
    #     tiktoken \
    #     "ipywidgets>=7,<8" \
    #     matplotlib

    # %pip install --quiet \
    #     duckduckgo-search  \
    #     yfinance  \
    #     pandas_datareader  \
    #     langchain_experimental \
    #     pysqlite3 \
    #     google-search-results

    # %pip install --quiet beautifulsoup4


    import json
    import os
    import sys

    import boto3
    import botocore

    module_path = ".."
    sys.path.append(os.path.abspath(module_path))
    from utils import bedrock, print_ww


    # ---- ⚠️ Un-comment and edit the below lines as needed for your AWS setup ⚠️ ----

    # os.environ["AWS_DEFAULT_REGION"] = "<REGION_NAME>"  # E.g. "us-east-1"
    # os.environ["AWS_PROFILE"] = "<YOUR_PROFILE>"
    # os.environ["BEDROCK_ASSUME_ROLE"] = "<YOUR_ROLE_ARN>"  # E.g. "arn:aws:..."


    boto3_bedrock = bedrock.get_bedrock_client(
        assumed_role=os.environ.get("BEDROCK_ASSUME_ROLE", None),
        region=os.environ.get("AWS_DEFAULT_REGION", None),
        runtime=False
    )


    bedrock_runtime = bedrock.get_bedrock_client(
        assumed_role=os.environ.get("BEDROCK_ASSUME_ROLE", None),
        region=os.environ.get("AWS_DEFAULT_REGION", None),
        runtime=True
    )



    prompt_data = """Human: """
    prompt_data += format(testdata)
    prompt_data += """ what should my child wear to school.Respoind only as a summary, in bullet points """
    prompt_data += """ Include Location, like city and state, as well at tempatrure in Celcuisand farignhieght"
    Assistant:
    """

    body = json.dumps({"prompt": prompt_data, "max_tokens_to_sample": 500})
    modelId = "anthropic.claude-instant-v1"  # change this to use a different version from the model provider
    accept = "application/json"
    contentType = "application/json"

    try:

        response = bedrock_runtime.invoke_model(
            body=body, modelId=modelId, accept=accept, contentType=contentType
        )
        response_body = json.loads(response.get("body").read())

        print(response_body.get("completion"))

    except botocore.exceptions.ClientError as error:

        if error.response['Error']['Code'] == 'AccessDeniedException':
               print(f"\x1b[41m{error.response['Error']['Message']}\
                    \nTo troubeshoot this issue please refer to the following resources.\
                     \nhttps://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_access-denied.html\
                     \nhttps://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html\x1b[0m\n")

        else:
            raise error
