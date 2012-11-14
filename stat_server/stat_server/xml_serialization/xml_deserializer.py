from __future__ import unicode_literals
import collections
import xml.parsers.expat

class XmlDeserializer(object):

    # spec: class, str -> instance_of_class
    def deserialize(self, dest_type, string_source):
        intermediate_result = XmlDeserializationHelper().deserialize(string_source)
        return dest_type.create(intermediate_result)

class XmlDeserializationHelper(object):

    # spec: str -> {str: Inner}, where Inner = {str: Inner}\[{str: Inner}]
    def deserialize(self, string_source):
        parse_stack = collections.deque()
        parse_stack.append({})
        parser = xml.parsers.expat.ParserCreate()
        parser.StartElementHandler = lambda name, attrs: self._process_start_element(name, attrs, parse_stack)
        parser.EndElementHandler = lambda name: self._process_end_element(parse_stack)
        parser.CharacterDataHandler = lambda data: self._process_char_data(data, parse_stack)
        parser.Parse(string_source)
        return parse_stack.pop()

    # spec: str, {str: str}, deque -> None
    def _process_start_element(self, name, attrs, parse_stack):
        current = parse_stack[len(parse_stack)-1]
        new ={}
        if name in current:
            # if name exists in current dict, then we have list of objects
            value = current[name]
            if not isinstance(value, list):
                value = [value]
                current[name] = value
            value.append(new)
        else:
            current[name] = new
            # add attributes
        for attr_key in attrs:
            new[attr_key] = attrs[attr_key]
        parse_stack.append(new)

    # spec: deque -> None
    def _process_end_element(self, parse_stack):
        parse_stack.pop()

        # spec: str, deque -> None
    def _process_char_data(self, data, parse_stack):
        current = parse_stack[len(parse_stack)-1]
        current[''] = data

__author__ = 'andrey.ushakov'
