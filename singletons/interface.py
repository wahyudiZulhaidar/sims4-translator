# -*- coding: utf-8 -*-

import os
import sys
import glob
import xml.etree.ElementTree as ElementTree
from collections import namedtuple
from typing import List, Optional

from singletons.config import config

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS # type: ignore
else:
    base_path = os.path.abspath(".")


class Lang(namedtuple('Lang', 'code name items authors version')):

    def get(self, k: str, v: str) -> str:
        if k in self.items and v in self.items[k]:
            value = self.items[k][v]
            return value.strip() if value is not None else v.strip()
        return v.strip()


class Interface:

    def __init__(self) -> None:
        self.__languages = {}
        self.__current: Optional[Lang] = None
        self.__load()

    def __load(self) -> None:
        interface_folder_path = os.path.join(base_path, 'prefs', 'interface')
        files = glob.glob(os.path.join(interface_folder_path, '*.xml'))

        for f in files:
            with open(f, 'r', encoding='utf-8') as fp:
                content = fp.read()

            try:
                parser = ElementTree.XMLParser(encoding='utf-8')
                root = ElementTree.fromstring(content, parser=parser)
            except ElementTree.ParseError:
                continue

            code = root.get('language')
            name = root.get('name')
            authors = root.get('authors')
            version = root.get('version')

            if code and name:
                lang_items = {}

                for context in root.findall('context'):
                    key = context.get('name')
                    if key:
                        context_items = {}

                        for s in context.findall('string'):
                            source = s.find('source')
                            translation = s.find('translation')
                            if source is not None and translation is not None:
                                context_items[source.text] = translation.text

                        lang_items[key] = context_items

                self.__languages[code] = Lang(code, name, lang_items, authors, version)

        self.__languages = dict(sorted(self.__languages.items()))

        self.reload()

    def reload(self) -> None:
        lang_code = str(config.value('interface', 'language'))
        self.__current = self.__languages.get(lang_code, None)

    def text(self, k: str, v: str) -> str:
        return self.__current.get(k, v) if isinstance(self.__current, Lang) else v

    @property
    def authors(self) -> Optional[str]:
        return self.__current.authors if isinstance(self.__current, Lang) else None

    @property
    def version(self) -> Optional[str]:
        return self.__current.version if isinstance(self.__current, Lang) else None

    @property
    def languages(self) -> List[Lang]:
        return list(self.__languages.values())

    @property
    def current_index(self) -> int:
        keys = list(self.__languages.keys())
        interface_value = str(config.value('interface', 'language'))
        if interface_value in keys:
            return keys.index(interface_value)
        return 0


interface = Interface()