

from langchain_community.llms import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

model_id = "/Users/liushihao/Downloads/model/microsoft/Phi-3-mini-128k-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id,trust_remote_code=True)
pipe = pipeline(
    "text-generation", model=model, tokenizer=tokenizer, max_new_tokens=10
)
hf = HuggingFacePipeline(pipeline=pipe)
"""
The model 'Phi3ForCausalLM' is not supported for text-generation. 
Supported models are ['BartForCausalLM', 'BertLMHeadModel', 'BertGenerationDecoder', 'BigBirdForCausalLM', 
'BigBirdPegasusForCausalLM', 'BioGptForCausalLM', 'BlenderbotForCausalLM', 'BlenderbotSmallForCausalLM', 
'BloomForCausalLM', 'CamembertForCausalLM', 'LlamaForCausalLM', 'CodeGenForCausalLM', 'CohereForCausalLM', 
'CpmAntForCausalLM', 'CTRLLMHeadModel', 'Data2VecTextForCausalLM', 'DbrxForCausalLM', 'ElectraForCausalLM', 
'ErnieForCausalLM', 'FalconForCausalLM', 'FuyuForCausalLM', 'GemmaForCausalLM', 'GitForCausalLM', 'GPT2LMHeadModel', 
'GPT2LMHeadModel', 'GPTBigCodeForCausalLM', 'GPTNeoForCausalLM', 'GPTNeoXForCausalLM', 'GPTNeoXJapaneseForCausalLM', 
'GPTJForCausalLM', 'JambaForCausalLM', 'LlamaForCausalLM', 'MambaForCausalLM', 'MarianForCausalLM', 'MBartForCausalLM', 
'MegaForCausalLM', 'MegatronBertForCausalLM', 'MistralForCausalLM', 'MixtralForCausalLM', 'MptForCausalLM', 'MusicgenForCausalLM', 
'MusicgenMelodyForCausalLM', 'MvpForCausalLM', 'OlmoForCausalLM', 'OpenLlamaForCausalLM', 'OpenAIGPTLMHeadModel', 'OPTForCausalLM', 
'PegasusForCausalLM', 'PersimmonForCausalLM', 'PhiForCausalLM', 'PLBartForCausalLM', 'ProphetNetForCausalLM', 'QDQBertLMHeadModel', 
'Qwen2ForCausalLM', 'Qwen2MoeForCausalLM', 'RecurrentGemmaForCausalLM', 'ReformerModelWithLMHead', 'RemBertForCausalLM', 
'RobertaForCausalLM', 'RobertaPreLayerNormForCausalLM', 'RoCBertForCausalLM', 'RoFormerForCausalLM', 'RwkvForCausalLM', 
'Speech2Text2ForCausalLM', 'StableLmForCausalLM', 'Starcoder2ForCausalLM', 'TransfoXLLMHeadModel', 'TrOCRForCausalLM', 
'WhisperForCausalLM', 'XGLMForCausalLM', 'XLMWithLMHeadModel', 'XLMProphetNetForCausalLM', 'XLMRobertaForCausalLM', 
'XLMRobertaXLForCausalLM', 'XLNetLMHeadModel', 'XmodForCausalLM'].

"""