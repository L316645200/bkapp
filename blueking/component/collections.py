# -*- coding: utf-8 -*-
"""Collections for component client"""
from blueking.component.apis.get_usage_disk import CollectionsGetDfusage
from .apis.bk_login import CollectionsBkLogin
from .apis.bk_paas import CollectionsBkPaas
from .apis.cc import CollectionsCC
from .apis.cmsi import CollectionsCMSI
from .apis.gse import CollectionsGSE
from .apis.job import CollectionsJOB
from .apis.sops import CollectionsSOPS


# Available components
AVAILABLE_COLLECTIONS = {
    'bk_login': CollectionsBkLogin,
    'bk_paas': CollectionsBkPaas,
    'cc': CollectionsCC,
    'cmsi': CollectionsCMSI,
    'gse': CollectionsGSE,
    'job': CollectionsJOB,
    'sops': CollectionsSOPS,
    'self_server': CollectionsGetDfusage,
}
