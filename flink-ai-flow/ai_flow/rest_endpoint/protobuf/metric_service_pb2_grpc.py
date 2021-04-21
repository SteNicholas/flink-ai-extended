#
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
#
# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import message_pb2 as message__pb2
from . import metric_service_pb2 as metric__service__pb2


class MetricServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.registerMetricMeta = channel.unary_unary(
                '/service.MetricService/registerMetricMeta',
                request_serializer=metric__service__pb2.MetricMetaRequest.SerializeToString,
                response_deserializer=metric__service__pb2.MetricMetaResponse.FromString,
                )
        self.registerMetricSummary = channel.unary_unary(
                '/service.MetricService/registerMetricSummary',
                request_serializer=metric__service__pb2.MetricSummaryRequest.SerializeToString,
                response_deserializer=metric__service__pb2.MetricSummaryResponse.FromString,
                )
        self.updateMetricMeta = channel.unary_unary(
                '/service.MetricService/updateMetricMeta',
                request_serializer=metric__service__pb2.MetricMetaRequest.SerializeToString,
                response_deserializer=metric__service__pb2.MetricMetaResponse.FromString,
                )
        self.getMetricMeta = channel.unary_unary(
                '/service.MetricService/getMetricMeta',
                request_serializer=metric__service__pb2.GetMetricMetaRequest.SerializeToString,
                response_deserializer=metric__service__pb2.MetricMetaResponse.FromString,
                )
        self.updateMetricSummary = channel.unary_unary(
                '/service.MetricService/updateMetricSummary',
                request_serializer=metric__service__pb2.MetricSummaryRequest.SerializeToString,
                response_deserializer=metric__service__pb2.MetricSummaryResponse.FromString,
                )
        self.getDatasetMetricMeta = channel.unary_unary(
                '/service.MetricService/getDatasetMetricMeta',
                request_serializer=metric__service__pb2.GetDataSetMetricMetaRequest.SerializeToString,
                response_deserializer=metric__service__pb2.ListMetricMetaResponse.FromString,
                )
        self.getModelMetricMeta = channel.unary_unary(
                '/service.MetricService/getModelMetricMeta',
                request_serializer=metric__service__pb2.GetModelMetricMetaRequest.SerializeToString,
                response_deserializer=metric__service__pb2.ListMetricMetaResponse.FromString,
                )
        self.getMetricSummary = channel.unary_unary(
                '/service.MetricService/getMetricSummary',
                request_serializer=metric__service__pb2.GetMetricSummaryRequest.SerializeToString,
                response_deserializer=metric__service__pb2.ListMetricSummaryResponse.FromString,
                )
        self.deleteMetricMeta = channel.unary_unary(
                '/service.MetricService/deleteMetricMeta',
                request_serializer=metric__service__pb2.UuidRequest.SerializeToString,
                response_deserializer=message__pb2.Response.FromString,
                )
        self.deleteMetricSummary = channel.unary_unary(
                '/service.MetricService/deleteMetricSummary',
                request_serializer=metric__service__pb2.UuidRequest.SerializeToString,
                response_deserializer=message__pb2.Response.FromString,
                )


class MetricServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def registerMetricMeta(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def registerMetricSummary(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def updateMetricMeta(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getMetricMeta(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def updateMetricSummary(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getDatasetMetricMeta(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getModelMetricMeta(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getMetricSummary(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def deleteMetricMeta(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def deleteMetricSummary(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MetricServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'registerMetricMeta': grpc.unary_unary_rpc_method_handler(
                    servicer.registerMetricMeta,
                    request_deserializer=metric__service__pb2.MetricMetaRequest.FromString,
                    response_serializer=metric__service__pb2.MetricMetaResponse.SerializeToString,
            ),
            'registerMetricSummary': grpc.unary_unary_rpc_method_handler(
                    servicer.registerMetricSummary,
                    request_deserializer=metric__service__pb2.MetricSummaryRequest.FromString,
                    response_serializer=metric__service__pb2.MetricSummaryResponse.SerializeToString,
            ),
            'updateMetricMeta': grpc.unary_unary_rpc_method_handler(
                    servicer.updateMetricMeta,
                    request_deserializer=metric__service__pb2.MetricMetaRequest.FromString,
                    response_serializer=metric__service__pb2.MetricMetaResponse.SerializeToString,
            ),
            'getMetricMeta': grpc.unary_unary_rpc_method_handler(
                    servicer.getMetricMeta,
                    request_deserializer=metric__service__pb2.GetMetricMetaRequest.FromString,
                    response_serializer=metric__service__pb2.MetricMetaResponse.SerializeToString,
            ),
            'updateMetricSummary': grpc.unary_unary_rpc_method_handler(
                    servicer.updateMetricSummary,
                    request_deserializer=metric__service__pb2.MetricSummaryRequest.FromString,
                    response_serializer=metric__service__pb2.MetricSummaryResponse.SerializeToString,
            ),
            'getDatasetMetricMeta': grpc.unary_unary_rpc_method_handler(
                    servicer.getDatasetMetricMeta,
                    request_deserializer=metric__service__pb2.GetDataSetMetricMetaRequest.FromString,
                    response_serializer=metric__service__pb2.ListMetricMetaResponse.SerializeToString,
            ),
            'getModelMetricMeta': grpc.unary_unary_rpc_method_handler(
                    servicer.getModelMetricMeta,
                    request_deserializer=metric__service__pb2.GetModelMetricMetaRequest.FromString,
                    response_serializer=metric__service__pb2.ListMetricMetaResponse.SerializeToString,
            ),
            'getMetricSummary': grpc.unary_unary_rpc_method_handler(
                    servicer.getMetricSummary,
                    request_deserializer=metric__service__pb2.GetMetricSummaryRequest.FromString,
                    response_serializer=metric__service__pb2.ListMetricSummaryResponse.SerializeToString,
            ),
            'deleteMetricMeta': grpc.unary_unary_rpc_method_handler(
                    servicer.deleteMetricMeta,
                    request_deserializer=metric__service__pb2.UuidRequest.FromString,
                    response_serializer=message__pb2.Response.SerializeToString,
            ),
            'deleteMetricSummary': grpc.unary_unary_rpc_method_handler(
                    servicer.deleteMetricSummary,
                    request_deserializer=metric__service__pb2.UuidRequest.FromString,
                    response_serializer=message__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'service.MetricService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class MetricService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def registerMetricMeta(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service.MetricService/registerMetricMeta',
            metric__service__pb2.MetricMetaRequest.SerializeToString,
            metric__service__pb2.MetricMetaResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def registerMetricSummary(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service.MetricService/registerMetricSummary',
            metric__service__pb2.MetricSummaryRequest.SerializeToString,
            metric__service__pb2.MetricSummaryResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def updateMetricMeta(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service.MetricService/updateMetricMeta',
            metric__service__pb2.MetricMetaRequest.SerializeToString,
            metric__service__pb2.MetricMetaResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getMetricMeta(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service.MetricService/getMetricMeta',
            metric__service__pb2.GetMetricMetaRequest.SerializeToString,
            metric__service__pb2.MetricMetaResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def updateMetricSummary(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service.MetricService/updateMetricSummary',
            metric__service__pb2.MetricSummaryRequest.SerializeToString,
            metric__service__pb2.MetricSummaryResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getDatasetMetricMeta(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service.MetricService/getDatasetMetricMeta',
            metric__service__pb2.GetDataSetMetricMetaRequest.SerializeToString,
            metric__service__pb2.ListMetricMetaResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getModelMetricMeta(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service.MetricService/getModelMetricMeta',
            metric__service__pb2.GetModelMetricMetaRequest.SerializeToString,
            metric__service__pb2.ListMetricMetaResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getMetricSummary(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service.MetricService/getMetricSummary',
            metric__service__pb2.GetMetricSummaryRequest.SerializeToString,
            metric__service__pb2.ListMetricSummaryResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def deleteMetricMeta(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service.MetricService/deleteMetricMeta',
            metric__service__pb2.UuidRequest.SerializeToString,
            message__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def deleteMetricSummary(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service.MetricService/deleteMetricSummary',
            metric__service__pb2.UuidRequest.SerializeToString,
            message__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
