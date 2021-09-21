import json
import logging


class CSSAdapter:
    def __init__(self, element):
        self.element = element

    def css(self, key):
        return self.element.css(key)

    def xpath(self, key):
        return self.element.xpath(key)

    def css_json_first(self, key, default=None):
        jsons = self.css_json(key)
        if len(jsons):
            return jsons[0]

        return default

    def css_json(self, key):
        result = []
        elem = self.element.css(key)
        if len(elem):
            for e in elem:
                text = e.get().strip()
                try:
                    result.append(json.loads(text))
                except:
                    pass

        return result

    def css_exists(self, key):
        return len(self.element.css(key)) > 0

    def css_extract(self, key):
        return [i.strip() for i in self.element.css(key).extract()]

    def css_extract_join(self, key, join='/', default=None):
        list = self.css_extract(key)
        if len(list):
            return join.join(list)

        return default

    def css_extract_first(self, key, default=None):
        element = self.element.css(key)
        if len(element):
            return element.extract_first().strip()
        return default

    def css_get(self, key):
        try:
            return self.element.css(key).get().strip()
        except AttributeError:
            return self.element.css(key).get()

    def xpath_exists(self, key):
        return len(self.element.xpath(key)) > 0

    def xpath_extract(self, key):
        return [i.strip() for i in self.element.xpath(key).extract()]

    def xpath_extract_first(self, key, default=None):
        element = self.element.xpath(key)
        if len(element):
            return element.extract_first().strip()
        return default

    def xpath_get(self, key):
        try:
            return self.element.xpath(key).get().strip()
        except AttributeError:
            return self.element.xpath(key).get()
