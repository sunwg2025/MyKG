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
	content VARCHAR(4096) NOT NULL,
	tags VARCHAR(64) NOT NULL,
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
    knowledge_id INTEGER NOT NULL,
    dataset_content TEXT,
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
