# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# 'License'); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
import unittest

from high_availability_utils.hash.hash_ring import HashRing


class TestHashRing(unittest.TestCase):

    def test_hash_ring(self):
        hash_ring = HashRing(['192.168.1.1', '192.168.1.2', '192.168.1.3'])
        self.assertEqual('192.168.1.1', hash_ring.get_node('dag_1'))
        self.assertEqual('192.168.1.3', hash_ring.get_node('dag_2'))
        self.assertEqual('192.168.1.3', hash_ring.get_node('dag_3'))
        self.assertEqual('192.168.1.2', hash_ring.get_node('dag_4'))
        self.assertEqual('192.168.1.1', hash_ring.get_node('dag_5'))
        self.assertEqual('192.168.1.1', hash_ring.get_node('dag_6'))
        self.assertEqual('192.168.1.1', hash_ring.get_node('dag_7'))
        self.assertEqual('192.168.1.3', hash_ring.get_node('dag_8'))

        hash_ring.add_node('192.168.1.4')
        self.assertEqual('192.168.1.1', hash_ring.get_node('dag_1'))
        self.assertEqual('192.168.1.3', hash_ring.get_node('dag_2'))
        self.assertEqual('192.168.1.4', hash_ring.get_node('dag_3'))
        self.assertEqual('192.168.1.2', hash_ring.get_node('dag_4'))
        self.assertEqual('192.168.1.1', hash_ring.get_node('dag_5'))
        self.assertEqual('192.168.1.1', hash_ring.get_node('dag_6'))
        self.assertEqual('192.168.1.1', hash_ring.get_node('dag_7'))
        self.assertEqual('192.168.1.4', hash_ring.get_node('dag_8'))

        hash_ring.remove_node('192.168.1.4')
        self.assertEqual('192.168.1.1', hash_ring.get_node('dag_1'))
        self.assertEqual('192.168.1.3', hash_ring.get_node('dag_2'))
        self.assertEqual('192.168.1.3', hash_ring.get_node('dag_3'))
        self.assertEqual('192.168.1.2', hash_ring.get_node('dag_4'))
        self.assertEqual('192.168.1.1', hash_ring.get_node('dag_5'))
        self.assertEqual('192.168.1.1', hash_ring.get_node('dag_6'))
        self.assertEqual('192.168.1.1', hash_ring.get_node('dag_7'))
        self.assertEqual('192.168.1.3', hash_ring.get_node('dag_8'))
