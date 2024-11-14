import rdflib
import io
from rdflib.namespace import Namespace
from rdflib import Graph, URIRef, Literal, BNode
from rdflib.plugins.sparql import prepareQuery
import re

ns = Namespace("http://example.org/kg/")
base_entity = ns['实体']
base_attribute = ns['属性']
base_relation = ns['关系']
is_belong_to = ns['类型']


def load_knowledge_from_xml(xml_str):
    graph = Graph()
    xml_file = io.StringIO(xml_str)
    graph.parse(xml_file, format='xml')
    return graph


def add_knowledge_entity(graph, entity):
    tmp_entity = ns[entity]
    graph.add((tmp_entity, is_belong_to, base_entity))


def add_knowledge_attribute(graph, entity, attribute_type, attribute_value):
    tmp_entity = ns[entity]
    tmp_attribute = ns[attribute_type]
    tmp_attribute_value = Literal(attribute_value)

    graph.add((tmp_attribute, is_belong_to, base_attribute))
    graph.add((tmp_entity, is_belong_to, base_entity))
    graph.add((tmp_entity, tmp_attribute, tmp_attribute_value))


def add_knowledge_relation(graph, entity1, relation, entity2):
    tmp_entity1 = ns[entity1]
    tmp_relation = ns[relation]
    tmp_entity2 = ns[entity2]

    graph.add((tmp_relation, is_belong_to, base_relation))
    graph.add((tmp_entity1, is_belong_to, base_entity))
    graph.add((tmp_entity2, is_belong_to, base_entity))
    graph.add((tmp_entity1, tmp_relation, tmp_entity2))


def remove_knowledge_relation(graph, entity1, relation, entity2):
    tmp_entity1 = ns[entity1]
    tmp_relation = ns[relation]
    tmp_entity2 = ns[entity2]

    graph.remove((tmp_relation, is_belong_to, base_relation))
    graph.remove((tmp_entity1, tmp_relation, tmp_entity2))


def remove_knowledge_attribute(graph, entity, attribute_type, attribute_value):
    tmp_entity = ns[entity]
    tmp_attribute = ns[attribute_type]
    tmp_attribute_value = Literal(attribute_value)

    graph.remove((tmp_attribute, is_belong_to, base_attribute))
    graph.remove((tmp_entity, tmp_attribute, tmp_attribute_value))


def remove_knowledge_entity(graph, entity):
    tmp_entity = ns[entity]
    graph.remove((tmp_entity, is_belong_to, base_entity))


def get_all_entity_knowledge(graph):
    query = prepareQuery('''
        PREFIX kg: <http://example.org/kg/>
        SELECT ?subject
        WHERE {
            ?subject kg:类型 kg:实体
        }
    ''', initNs={'kg': ns})

    results = []
    for r in graph.query(query):
        pattern = r"http://example.org/kg/(.*)'"
        match = re.search(pattern, str(r))
        results.append(match.group(1))
    return results


def get_all_attribute_knowledge(graph):
    query = prepareQuery('''
        PREFIX kg: <http://example.org/kg/>
        SELECT ?subject ?predicate ?object
        WHERE {
            ?predicate kg:类型 kg:属性 .
            ?subject kg:类型 kg:实体 .
            ?subject ?predicate ?object .
            FILTER (?object != kg:实体)
        }
    ''', initNs={'kg': ns})

    results = []
    for r in graph.query(query):
        pattern = r"(URIRef\('http://example.org/kg/(.*?)'\))|(Literal\('(.*?)'\))"
        matches = re.findall(pattern, str(r))
        tmp = [match[1] if match[1] else match[3] for match in matches]
        results.append({'实体': tmp[0], '属性': tmp[1], '属性值': tmp[2]})
    return results


def get_entity_attribute_knowledge(graph, entity):
    query = prepareQuery('''
        PREFIX kg: <http://example.org/kg/>
        SELECT ?subject ?predicate ?object
        WHERE {
            ?predicate kg:类型 kg:属性 .
            ?subject kg:类型 kg:实体 .
            ?subject ?predicate ?object .
            FILTER (?object != kg:实体 &&
            ?subject = kg:{{ entity }})
        }
    '''.replace('{{ entity }}', entity), initNs={'kg': ns})

    results = []
    for r in graph.query(query):
        pattern = r"(URIRef\('http://example.org/kg/(.*?)'\))|(Literal\('(.*?)'\))"
        matches = re.findall(pattern, str(r))
        tmp = [match[1] if match[1] else match[3] for match in matches]
        results.append({'实体': tmp[0], '属性': tmp[1], '属性值': tmp[2]})
    return results


def get_all_relation_knowledge(graph):
    query = prepareQuery('''
        PREFIX kg: <http://example.org/kg/>
        SELECT ?subject ?predicate ?object
        WHERE {
            ?predicate kg:类型 kg:关系 .
            ?subject ?predicate ?object .
        }
    ''', initNs={'kg': ns})

    results = []
    for r in graph.query(query):
        pattern = r"(URIRef\('http://example.org/kg/(.*?)'\))"
        matches = re.findall(pattern, str(r))
        tmp = [match[1] if match[1] else match[3] for match in matches]
        if len(tmp) == 3:
            results.append({'实体1': tmp[0], '关系': tmp[1], '实体2': tmp[2]})
    return results


def get_entity_relation_knowledge(graph, entity):
    query = prepareQuery('''
        PREFIX kg: <http://example.org/kg/>
        SELECT ?subject ?predicate ?object
        WHERE {
            ?predicate kg:类型 kg:关系 .
            ?subject ?predicate ?object .
            FILTER (?subject = kg:{{ entity }} ||
            ?object = kg:{{ entity }})
        }
    '''.replace('{{ entity }}', entity), initNs={'kg': ns})

    results = []
    for r in graph.query(query):
        pattern = r"(URIRef\('http://example.org/kg/(.*?)'\))"
        matches = re.findall(pattern, str(r))
        tmp = [match[1] if match[1] else match[3] for match in matches]
        if len(tmp) == 3:
            results.append({'实体1': tmp[0], '关系': tmp[1], '实体2': tmp[2]})
    return results


def get_knowledge_stats(rdf_xml):
    graph = load_knowledge_from_xml(rdf_xml)
    entitys = get_all_entity_knowledge(graph)
    attributes = get_all_attribute_knowledge(graph)
    relations = get_all_relation_knowledge(graph)
    graph.close()

    return len(entitys), len(attributes), len(relations)