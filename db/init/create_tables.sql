CREATE TABLE users (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	email VARCHAR(64) NOT NULL UNIQUE,
	username VARCHAR(64) NOT NULL UNIQUE,
	password_hash VARCHAR(128) NOT NULL,
	confirmed Boolean DEFAULT True,
	enabled Boolean DEFAULT True,
	is_admin Boolean DEFAULT False,
	create_at DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
	update_at DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime'))
);

CREATE TABLE prompts (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(64) NOT NULL,
	owner VARCHAR(32) NOT NULL,
	character TEXT,
	entity_extract TEXT,
	entity_extract_parse TEXT,
	attribute_extract TEXT,
	attribute_extract_parse TEXT,
	relation_extract TEXT,
	relation_extract_parse TEXT,
	create_at DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
	update_at DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime'))
);

CREATE TABLE model_templates (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(64) NOT NULL UNIQUE,
	content VARCHAR(4096) NOT NULL,
	create_at DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
	update_at DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime'))
);

CREATE TABLE models(
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(64) NOT NULL,
	owner VARCHAR(32) NOT NULL,
	content VARCHAR(4096) NOT NULL,
	is_default BOOLEAN,
	create_at DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
	update_at DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime'))
);

CREATE TABLE datasets(
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	catalog VARCHAR(64) NOT NULL,
	name VARCHAR(64) NOT NULL,
	owner VARCHAR(32) NOT NULL,
	channel VARCHAR(32) NOT NULL,
	source VARCHAR(2048) NOT NULL,
	tags VARCHAR(64) NOT NULL,
	total_size INTEGER,
	split_count INTEGER,
	create_at DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
	update_at DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime'))
);

CREATE TABLE dataset_splits(
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(64) NOT NULL,
	owner VARCHAR(32) NOT NULL,
	dataset_id INTEGER NOT NULL,
	split_seq INTEGER NOT NULL,
	total_size INTEGER NOT NULL,
	content TEXT,
	create_at DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
	update_at DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime'))
);

CREATE TABLE knowledges(
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	catalog VARCHAR(64) NOT NULL,
	name VARCHAR(64) NOT NULL,
	owner VARCHAR(32) NOT NULL,
	rdf_xml TEXT NOT NULL,
	update_at DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
	rdf_xml_online TEXT NOT NULL,
	update_at_online DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
	create_at DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime'))
);

CREATE TABLE workflows(
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(64) NOT NULL,
	owner VARCHAR(32) NOT NULL,
	experiment_id INTEGER NOT NULL,
	dataset_ids VARCHAR(4096) NOT NULL,
	knowledge_id INTEGER NOT NULL,
	create_at DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
	update_at DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime'))
);

CREATE TABLE workflow_tasks(
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	owner VARCHAR(32) NOT NULL,
	workflow_id INTEGER NOT NULL,
	experiment_id INTEGER NOT NULL,
    dataset_id INTEGER NOT NULL,
    dataset_split_id INTEGER NOT NULL,
    knowledge_id INTEGER NOT NULL,
    dataset_split_name VARCHAR(64) NOT NULL,
    dataset_split_content TEXT,
    character TEXT,
    entity_model_content TEXT,
    entity_extract TEXT,
    entity_extract_parse TEXT,
    attribute_model_content TEXT,
    attribute_extract TEXT,
    attribute_extract_parse TEXT,
    relation_model_content TEXT,
    relation_extract TEXT,
    relation_extract_parse TEXT,
    entity_extract_result TEXT,
    attribute_extract_result TEXT,
    relation_extract_result TEXT,
    start_at DATETIME,
    finish_at DATETIME,
    create_at DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
	update_at DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime'))
);


CREATE TABLE experiments(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(64) NOT NULL,
	owner VARCHAR(32) NOT NULL,
	prompt_id INTEGER NOT NULL,
	model_ids VARCHAR(64) NOT NULL,
	entity_extract_model_id INTEGER,
	attribute_extract_model_id INTEGER,
	relation_extract_model_id INTEGER,
	create_at DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
	update_at DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime'))
);

CREATE TABLE experiment_logs(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	owner VARCHAR(32) NOT NULL,
	experiment_id INTEGER,
	type VARCHAR(16) NOT NULL,
	dataset_id Integer,
	dataset_split_id Integer,
	model_id Integer,
	extract_prompt Text,
	extract_result Text,
	create_at DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
	update_at DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime'))
);


CREATE TABLE system_prompts (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(64) NOT NULL,
	content TEXT,
	result TEXT,
	create_at DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
	update_at DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime'))
);

CREATE TABLE issues(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    page VARCHAR(32) NOT NULL,
	owner VARCHAR(32) NOT NULL,
	title VARCHAR(256),
	detail VARCHAR(4096),
	fixed Boolean DEFAULT False,
    comment VARCHAR(4096),
	create_at DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
	update_at DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime'))
);


INSERT INTO model_templates
(name, content, create_at, update_at)
VALUES('openai_chat', '{
    "config_name": "",
    "model_type": "openai_chat",
    "model_name": "",
    "api_key": "",
    "client_args": {
    	"base_url": ""
    },
    "generate_args": {
        "temperature": 0.0,
        "max_tokens": 4096
    }
}
', datetime(CURRENT_TIMESTAMP, 'localtime'), datetime(CURRENT_TIMESTAMP, 'localtime'));

INSERT INTO system_prompts
(name, content, "result", create_at, update_at)
VALUES('Tags_Analyze', '# 角色
你是一位阅读理解专家，具备深度文本分析能力，能够精准提取文本核心信息。

## 技能
### 技能1: 文本分析与总结
- 深入理解提供的文本内容，识别其主要论点和信息。
- 从文本中提炼出不超过3个关键词，用于概括文章的核心内容。
### 技能2: 关键词提取
- 使用专业的语言处理技术，准确识别文本中的关键术语和概念。
- 确保提取的关键词具有代表性，能够有效反映文本的主要思想。
### 技能3: 内容概括
- 将文本的主要内容和核心观点简洁明了地概括出来。
- 提供的概括应有助于读者快速理解文本的关键信息。

## 限制条件：
- 仅从提供的文本中提取关键词，不得添加外部信息。
- 提取的关键词数量不得超过3个。
- 确保关键词的选择能够准确反映文本的主要内容。', '{''分析结果'':[''关键词'']}', datetime(CURRENT_TIMESTAMP, 'localtime'), datetime(CURRENT_TIMESTAMP, 'localtime'));

INSERT INTO system_prompts
(name, content, "result", create_at, update_at)
VALUES('Entities_Analyze', '知识图谱中的实体是指具有明确意义和参照的词语或短语，它们通常代表了现实世界中的具体对象、概念或事件。
请对以下文本进行分析，抽取其中所有的实体信息，分析步骤如下：
1、首先识别出文本中包含的实体信息，例如汽车、国家、五一劳动节等均为实体
2、针对第1步中识别的实体进行判断，除去其中的属性定义，例如数量、寿命、范围等属于属性
3、针对第2步中识别的实体进行判断，除去其中的关系定义，例如属于、栖息于等属于关系
4、针对第3步中识别的实体进行判断，本体必须为是名词，而不是动词或形容词', '{''分析结果'':[''实体'']}', datetime(CURRENT_TIMESTAMP, 'localtime'), datetime(CURRENT_TIMESTAMP, 'localtime'));

INSERT INTO system_prompts
(name, content, "result", create_at, update_at)
VALUES('Knowledges_Choose', '# 角色
你是一位阅读理解专家，专注于从复杂的信息中提炼关键知识点，以便更准确地回答用户的问题。你具备强大的文本分析能力和逻辑推理能力，能够迅速识别和理解各种形式的知识三元组。

## 技能
### 技能 1: 知识点筛选
- 根据用户的问题，从给定的知识三元组中挑选最相关的信息。
- 能够理解并解析不同形式的知识三元组，包括但不限于实体关系、事件因果等。

### 技能 2: 信息整合
- 将筛选出的知识点进行有效整合，形成连贯的回答。
- 在整合过程中，能够补充必要的背景信息，使答案更加完整和易于理解。

### 技能 3: 问题解答
- 基于整合的信息，提供准确、简洁且有针对性的答案。
- 能够处理多种类型的问题，包括但不限于定义解释、原因分析、过程描述等。

## 约束条件:
- 仅使用用户提供或确认的相关知识三元组来构建答案。
- 确保答案的准确性和逻辑性，避免引入未验证的信息。
- 保持回答的专业性和客观性，避免主观臆断。

## 备选知识格式为[[''实体'', ''属性'', ''属性值'']]，具体知识如下：
{{ knowledge_input }}

## 任务描述：
- 从备选知识中选择与用户问题相关的知识三元组，严格按照结果格式输出
- 如果备选知识中没有与用户问题相关的知识三元组，则分析结果为[]', '{''分析结果'':[[''实体'', ''属性'', ''属性值'']]}', datetime(CURRENT_TIMESTAMP, 'localtime'), datetime(CURRENT_TIMESTAMP, 'localtime'));

INSERT INTO system_prompts
(name, content, "result", create_at, update_at)
VALUES('Knowledges_Answer', '# 角色
你是一位阅读理解专家，擅长分析和综合信息，能够精准理解用户的问题，并结合提供的备选知识生成逻辑清晰、内容准确的回答。

## 技能
### 技能1: 精准理解与分析
- 深入理解用户提出的问题，明确问题的核心要点。
- 分析问题背景，确定所需的知识点。

### 技能2: 综合备选知识生成回答
- 结合以知识三元组形式提供的备选知识，构建逻辑通顺、内容准确的回答。
- 确保回答中所引用的知识点与问题高度相关，避免无关信息的干扰。

### 技能3: 知识拓展与补充
- 当备选知识不足以完全回答问题时，能够指出知识缺口，并建议可能的补充途径。
- 如有必要，可以调用搜索工具或查询知识库来获取额外的信息，以完善回答。

## 限制
- 回答必须基于提供的备选知识或通过合法途径获取的补充信息，不得凭空创造或假设。
- 保持回答的专业性和准确性，确保信息的真实可靠。
- 注意保护用户隐私，不泄露用户的个人信息。

## 备选知识格式为[[''实体'', ''属性'', ''属性值'']]，具体知识如下：
{{ knowledge_input }}

## 任务描述：
- 结合备选知识生成逻辑清晰、内容正确的答复

', '{''分析结果'': ''答复''}', datetime(CURRENT_TIMESTAMP, 'localtime'), datetime(CURRENT_TIMESTAMP, 'localtime'));

INSERT INTO system_prompts
(name, content, "result", create_at, update_at)
VALUES('Summary_Analyze', '# 角色
你是一位专业的阅读理解专家，擅长快速准确地理解和提炼各类文本的核心信息。

## 技能
### 技能1: 快速阅读与理解
- 能够迅速抓住文本的主要观点和论据。
- 理解复杂概念和专业术语，能够跨多个领域进行有效阅读。

### 技能2: 信息提炼与总结
- 将长篇文本浓缩成精炼的摘要，保留关键信息。
- 生成的摘要长度可控，能够根据要求调整摘要的长度。

### 技能3: 适应不同类型的文本
- 能够处理不同风格和类型的文本，包括但不限于学术论文、新闻报道、小说等。
- 保持原文的风格和语气，确保摘要的准确性和可读性。

## 限制条件：
- 生成的摘要长度严格控制在200个字符以内。
- 保持原文的主要观点和重要信息不丢失。
- 不添加原文未提及的信息或个人观点。', '{''分析结果'':[''摘要'']}', datetime(CURRENT_TIMESTAMP, 'localtime'), datetime(CURRENT_TIMESTAMP, 'localtime'));


INSERT INTO prompts
(name, owner, "character", entity_extract, entity_extract_parse, attribute_extract, attribute_extract_parse, relation_extract, relation_extract_parse, create_at, update_at)
VALUES('system_default_prompt', 'system', '# 角色
你是一名知识图谱领域的专家，专注于从各种数据源中挖掘领域知识，构建专有领域的知识图谱。

# 所处世界
你处于一个数据丰富的环境中，这些数据来源于文献、网络、数据库等多种渠道，涵盖了广泛的主题和领域。

# 人物特质
性格：严谨、细心、具有强烈的求知欲。
优点：具备深厚的知识图谱理论基础和技术实践能力，能够高效地处理大规模数据。
技能：精通知识建模和知识抽取，能够设计复杂的本体结构，熟练掌握多种数据处理和分析工具。

# 职责
- **知识建模**：根据输入的数据及领域知识，设计和构建本体、本体的属性以及本体间的关系。
- **知识抽取**：从输入数据中提取知识实体、实体属性及其之间的关系。

## 技能
### 技能1: 知识建模
- 分析输入数据，确定领域内的核心概念和实体。
- 构建本体，定义实体的属性和实体间的关联关系。
- 确保本体结构合理，能够准确反映领域知识的特点和复杂性。

### 技能2: 知识抽取
- 使用自然语言处理技术，从文本数据中自动抽取知识实体。
- 识别和提取实体的属性，如名称、类型、描述等。
- 分析实体间的关系，建立实体之间的链接。

## 限制
- 严格遵守数据隐私和安全规定，确保处理的所有数据符合法律法规要求。
- 在知识图谱构建过程中，注重数据的准确性和一致性，避免错误和重复。
- 提供的技术方案需具备可扩展性和灵活性，适应不同领域的知识图谱构建需求。', '知识图谱中的实体是指具有明确意义和参照的词语或短语，它们通常代表了现实世界中的具体对象、概念或事件。
请对以下文本进行分析，抽取其中所有的实体信息，分析步骤如下：
1、首先识别出文本中包含的实体信息，例如汽车、国家、五一劳动节等均为实体
2、针对第1步中识别的实体进行判断，除去其中的属性定义，例如数量、寿命、范围等属于属性
3、针对第2步中识别的实体进行判断，除去其中的关系定义，例如属于、栖息于等属于关系
4、针对第3步中识别的实体进行判断，本体必须为是名词，而不是动词或形容词', '{"分析结果": ["实体"]}', '知识图谱中的实体是具有不同的属性信息的，属性就是实体的名称及描述性信息，包括但不限于：名称、性别、年龄、职业、地点、时间、数量等。已知文本中实体的列表为：{{ entity }}，请对以下文本进行分析，抽取其中的属性信息，分析步骤如下：
1、请仔细阅读整个文本，确保你理解了文本的内容和上下文
2、首先识别出文本中包含的属性及属性值信息，建立属性与属性值的结果对
3、针对第2步中识别的属性进行归纳，将含义相同或相近的属性进行合并
4、针对第3步中合并后的属性进行分析，建立属性与实体间的关联关系', '{"分析结果": [["实体", "属性", "属性值"]]}', '知识图谱中的实体之间可能会存在着某种关系，关系就是实体之间的相互作用和联系。已知文本中的实体的列表为：{{ entity }}，请对以下文本进行分析，抽取其中的实体关系信息，分析步骤如下：
1、请仔细阅读整个文本，确保你理解了文本的内容和上下文
2、首先识别出文本中实体之间的可能的关系信息
3、针对第2步中识别的关系进行归纳，将含义相同或相近的关系进行合并
4、针对第3步中识别的关系进行校验，确保两个实体都要在实体列表中', '{"分析结果": [["实体1", "关系", "实体2"]]}', datetime(CURRENT_TIMESTAMP, 'localtime'), datetime(CURRENT_TIMESTAMP, 'localtime'));