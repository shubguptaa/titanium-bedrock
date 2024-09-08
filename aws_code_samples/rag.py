import boto3
import os
from IPython.display import Markdown, display
import logging
import boto3


from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
    
logging.basicConfig(level=logging.INFO,format="%(levelname)s: %(message)s")

region = os.environ.get("AWS_REGION")
bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    region_name=region,
)
claude3 = 'claude3'
llama2 = 'llama2'
llama3='llama3'
mistral='mistral'
titan='titan'
models_dict = {
    claude3 : 'anthropic.claude-3-sonnet-20240229-v1:0',
    llama2: 'meta.llama2-13b-chat-v1',
    llama3: 'meta.llama3-8b-instruct-v1:0',
    mistral: 'mistral.mistral-7b-instruct-v0:2',
    titan : 'amazon.titan-text-premier-v1:0'
}
max_tokens_val = 200
temperature_val = 0.1


dict_add_params = {
    llama3: {}, #"max_gen_len":max_tokens_val, "temperature":temperature_val} , 
    claude3: {"top_k": 200, },# "temperature": temperature_val, "max_tokens": max_tokens_val},
    mistral: {}, #{"max_tokens":max_tokens_val, "temperature": temperature_val} , 
    titan:  {"topK": 200, },# "maxTokenCount": max_tokens_val}
}
inference_config={
    "temperature": temperature_val,
    "maxTokens": max_tokens_val,
    "topP": 0.9
}

def generate_conversation(bedrock_client,model_id,system_text,input_text):
    """
    Sends a message to a model.
    Args:
        bedrock_client: The Boto3 Bedrock runtime client.
        model_id (str): The model ID to use.
        system_text (JSON) : The system prompt.
        input text : The input message.

    Returns:
        response (JSON): The conversation that the model generated.

    """

    logger.info("Generating message with model %s", model_id)

    # Message to send.
    message = {
        "role": "user",
        "content": [{"text": input_text}]
    }
    messages = [message]
    system_prompts = [{"text" : system_text}]

    if model_id in [models_dict.get(mistral), models_dict.get(titan)]:
        system_prompts = [] # not supported

    # Inference parameters to use.
 

    #Base inference parameters to use.
    #inference_config = {"temperature": temperature}


    # Send the message.
    response = bedrock_client.converse(
        modelId=model_id,
        messages=messages,
        system=system_prompts,
        inferenceConfig=inference_config,
        additionalModelRequestFields=get_additional_model_fields(model_id)
    )

    return response

def get_additional_model_fields(modelId):

    return dict_add_params.get(modelId)
    #{"top_k": top_k, "max_tokens": max_tokens}}
    
def get_converse_output(response_obj):
    ret_messages=[]
    output_message = response['output']['message']
    role_out = output_message['role']

    for content in output_message['content']:
        ret_messages.append(content['text'])
        
    return ret_messages, role_out
