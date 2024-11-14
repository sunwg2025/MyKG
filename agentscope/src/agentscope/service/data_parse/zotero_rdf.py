# -*- coding: utf-8 -*-
""" Parse Data From RDF File"""
from typing import Optional
from typing import Any
import os

from ...service.service_response import ServiceResponse
from ...service.service_status import ServiceExecStatus

try:
    import rdflib
    from rdflib import Namespace
except ImportError:
    rdflib = None

BIB = Namespace("http://purl.org/net/biblio#")
DC = Namespace("http://purl.org/dc/elements/1.1/")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
Z = Namespace("http://www.zotero.org/namespaces/export#")
DCTERMS = Namespace("http://purl.org/dc/terms/")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
LINK = Namespace("http://purl.org/rss/1.0/modules/link/")
PRISM = Namespace("http://prismstandard.org/namespaces/1.2/basic/")


def parse_zotero_rdf(
    file: str,
    **kwargs: Any,
) -> ServiceResponse:
    # Check if the rdf file is exists
    if not os.path.exists(file):
        return ServiceResponse(
            status=ServiceExecStatus.ERROR,
            content="FileExistsError: The file isn't exists.",
        )

    # Check if input path is file
    if not os.path.isfile(file):
        return ServiceResponse(
            status=ServiceExecStatus.ERROR,
            content="FileTypeError: The path isn't a file.",
        )

    g = rdflib.Graph()
    g.parse(file)

    results = []
    for article in g.subjects(RDF.type, BIB.Article):
        title = ""
        itemType = ""
        authors = []
        abstract = ""
        dateS = ""
        uri = ""

        for pred, obj in g.predicate_objects(article):
            if pred == DC.title:
                title = str(obj)
            if pred == Z.itemType:
                itemType = str(obj)
            if pred == DC.date:
                dateS = str(obj)
            if pred == BIB.authors:
                for sub_pred, sub_obj in g.predicate_objects(obj):
                    if sub_pred == RDF.type:
                        continue
                    surname = ""
                    givenName = ""
                    for leaf_pred, leaf_obj in g.predicate_objects(sub_obj):
                        if leaf_pred == FOAF.surname:
                            surname = leaf_obj
                        if leaf_pred == FOAF.givenName:
                            givenName = leaf_obj
                    authors.append(str(surname) + " " + str(givenName))
            if pred == DCTERMS.abstract:
                abstract = str(obj)
            if pred == DC.identifier:
                for sub_pred, sub_obj in g.predicate_objects(obj):
                    if sub_pred == RDF.value:
                        uri = str(sub_obj)

        results.append({'title': title, 'itemType': itemType, 'date': dateS, 'authors': authors,
                        'uri': uri, 'abstract': abstract})

    return ServiceResponse(
        status=ServiceExecStatus.SUCCESS,
        content=results,
    )




