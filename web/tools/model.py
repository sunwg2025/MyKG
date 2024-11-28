import agentscope
from agentscope.message import Msg
from agentscope.agents import KnowledgeAgent, DialogAgent
from agentscope.parsers import MarkdownJsonDictParser
from web.database.system_prompt import System_Prompt
import re


def check_model_config(content):
    try:
        model_configs = eval(content)
        config_name = model_configs['config_name']
        agentscope.init(model_configs=model_configs, disable_saving=True, save_code=False)
        dialogAgent = DialogAgent(name='assistant',
                                  model_config_name=config_name,
                                  sys_prompt='You are a helpful ai assistant')
        msg = Msg(name='MyKG', content='Hi!', role='user')
        x = dialogAgent(msg)
        return True
    except Exception as e:
        raise e
    finally:
        agentscope.manager.ModelManager.flush(self=agentscope.manager.ModelManager.get_instance())


def call_knowledge_agent_base(model_configs, sys_prompt, extract_parse, dataset_content):
    agentscope.init(model_configs=model_configs, disable_saving=True, save_code=False)
    config_name = model_configs['config_name']
    knowledgeAgent = KnowledgeAgent(name="assistant", model_config_name=config_name, sys_prompt=sys_prompt)
    ontology_extract_parser = MarkdownJsonDictParser(content_hint=eval(extract_parse))
    knowledgeAgent.set_parser(ontology_extract_parser)
    msg = Msg(name="user", content=dataset_content, role="user")
    agent_result = knowledgeAgent(msg).content
    return agent_result['分析结果']


def is_alnum_chinese(s):
    pattern = re.compile(r'^[\w\u4e00-\u9fa5]+$')
    return bool(pattern.match(s))


def extract_entity_knowledge(dataset_content, model_content, character, extract_prompt, extract_parse):
    model_configs = eval(model_content)
    sys_prompt = character + ' ' + extract_prompt
    for i in range(5):
        try:
            agent_result = call_knowledge_agent_base(model_configs, sys_prompt, extract_parse, dataset_content)
            return agent_result
        except Exception as e:
            raise e
    raise ValueError('实体解析结果错误！')


def extract_attribute_knowledge(dataset_content, entity_content, model_content, character, extract_prompt,
                               extract_parse):
    model_configs = eval(model_content)
    sys_prompt = character + ' ' + extract_prompt.replace('{{ entity }}', entity_content)
    extract_result = []
    agent_result = ''
    entity_list = eval(entity_content)
    for i in range(5):
        try:
            agent_result = call_knowledge_agent_base(model_configs, sys_prompt, extract_parse, dataset_content)
            for res in agent_result:
                if len(res) == 3:
                    if res[0] in entity_list and is_alnum_chinese(res[0]):
                        extract_result.append(res)
            return extract_result
        except Exception as e:
            raise e


def extract_relation_knowledge(dataset_content, entity_content, model_content, character, extract_prompt,
                               extract_parse):
    model_configs = eval(model_content)
    sys_prompt = character + ' ' + extract_prompt.replace('{{ entity }}', entity_content)
    extract_result = []
    agent_result = ''
    entity_list = eval(entity_content)
    for i in range(5):
        try:
            agent_result = call_knowledge_agent_base(model_configs, sys_prompt, extract_parse, dataset_content)
            for res in agent_result:
                if len(res) == 3:
                    if res[0] in entity_list and res[2] in entity_list and is_alnum_chinese(res[1]):
                        extract_result.append(res)
            return extract_result
        except Exception as e:
            raise e


def call_system_prompt_base(content, model, sys_prompt_content, sys_prompt_result):
    try:
        model_configs = eval(model)
        config_name = model_configs['config_name']
        agentscope.init(model_configs=model_configs)
        knowledegAgent = KnowledgeAgent(name='assistant',
                                        model_config_name=config_name,
                                        sys_prompt=sys_prompt_content)
        result_parser = MarkdownJsonDictParser(content_hint=eval(sys_prompt_result))
        knowledegAgent.set_parser(result_parser)
        msg = Msg(name="user", content=content, role="user")
        agent_result = knowledegAgent(msg).content
        return agent_result['分析结果']
    except Exception as e:
        raise e


def analyze_content_tags(content, model):
    sys_prompt = System_Prompt.get_system_prompt_by_name('Tags_Analyze')
    return call_system_prompt_base(content, model, sys_prompt.content, sys_prompt.result)


def analyze_content_summary(content, model):
    sys_prompt = System_Prompt.get_system_prompt_by_name('Summary_Analyze')
    return call_system_prompt_base(content, model, sys_prompt.content, sys_prompt.result)



def analyze_content_entities(content, model):
    sys_prompt = System_Prompt.get_system_prompt_by_name('Entities_Analyze')
    return call_system_prompt_base(content, model, sys_prompt.content, sys_prompt.result)


def analyze_knowledges_choose(knowledge_input, content, model):
    sys_prompt = System_Prompt.get_system_prompt_by_name('Knowledges_Choose')
    sys_prompt_content = sys_prompt.content.replace('{{ knowledge_input }}', knowledge_input)
    return call_system_prompt_base(content, model, sys_prompt_content, sys_prompt.result)


def generate_knowledges_answer(knowledge_input, content, model):
    sys_prompt = System_Prompt.get_system_prompt_by_name('Knowledges_Answer')
    sys_prompt_content = sys_prompt.content.replace('{{ knowledge_input }}', knowledge_input)
    return call_system_prompt_base(content, model, sys_prompt_content, sys_prompt.result)