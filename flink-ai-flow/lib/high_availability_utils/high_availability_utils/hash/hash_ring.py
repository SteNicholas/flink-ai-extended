# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import hashlib


class HashRing(object):

    def __init__(self, nodes=None, replicas=3):
        """
        Manages a hash ring.

        `nodes` is a list of objects that have a proper __str__ representation.
        `replicas` indicates how many virtual points should be used pr. node,
        replicas are required to improve the distribution.
        """
        self.replicas = replicas
        self.ring = dict()
        self._sorted_keys = []
        if nodes:
            for node in nodes:
                self.add_node(node)

    def add_node(self, node):
        """
        Adds a `node` to the hash ring (including a number of replicas).

        :param node: A node added to the hash ring.
        """
        for i in range(0, self.replicas):
            key = self._gen_key('%s:%s' % (node, i))
            self.ring[key] = node
            self._sorted_keys.append(key)
        self._sorted_keys.sort()

    def remove_node(self, node):
        """
        Removes `node` from the hash ring and its replicas.

        :param node: A node removed from the hash ring.
        """
        for i in range(0, self.replicas):
            key = self._gen_key('%s:%s' % (node, i))
            del self.ring[key]
            self._sorted_keys.remove(key)

    def get_node(self, string_key):
        """
        Given a string key a corresponding node in the hash ring is returned.
        If the hash ring is empty, `None` is returned.

        :param string_key: A given string key corresponding to the node of the hash ring.
        """
        return self.get_node_pos(string_key)[0]

    def get_node_pos(self, string_key):
        """
        Given a string key a corresponding node in the hash ring is returned
        along with it's position in the ring.
        If the hash ring is empty, (`None`, `None`) is returned.

        :param string_key: A given string key corresponding to the node of the hash ring.
        """
        if not self.ring:
            return None, None
        key = self._gen_key(string_key)
        nodes = self._sorted_keys
        for i in range(0, len(nodes)):
            node = nodes[i]
            if key <= node:
                return self.ring[node], i
        return self.ring[nodes[0]], 0

    def get_nodes(self, string_key):
        """
        Given a string key it returns the nodes as a generator that can hold the key.
        The generator is never ending and iterates through the ring
        starting at the correct position.

        :param string_key: A given string key corresponding to the node of the hash ring.
        """
        if not self.ring:
            yield None, None
        node, pos = self.get_node_pos(string_key)
        for key in self._sorted_keys[pos:]:
            yield self.ring[key]
        while True:
            for key in self._sorted_keys:
                yield self.ring[key]

    @staticmethod
    def _gen_key(key):
        """
        Given a string key it returns a long value,
        this long value represents a place on the hash ring.
        md5 is currently used because it mixes well.

        :param key: A given string key to represent a place on the hash ring.
        """
        return hashlib.md5(key.encode(encoding='UTF-8')).hexdigest()
