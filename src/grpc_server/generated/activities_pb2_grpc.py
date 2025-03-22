# flake8: noqa
# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import warnings

import grpc_server.generated.activities_pb2 as activities__pb2
import grpc
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2

GRPC_GENERATED_VERSION = "1.70.0"
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower

    _version_not_supported = first_version_is_lower(
        GRPC_VERSION, GRPC_GENERATED_VERSION
    )
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f"The grpc package installed is at version {GRPC_VERSION},"
        + f" but the generated code in activities_pb2_grpc.py depends on"
        + f" grpcio>={GRPC_GENERATED_VERSION}."
        + f" Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}"
        + f" or downgrade your generated code using grpcio-tools<={GRPC_VERSION}."
    )


class ActivitiesServiceStub(object):
    """Сервис для управления активностями пользователя.
    Предоставляет метод для получения стрима активностей пользователя.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetActivities = channel.unary_stream(
            "/activities.ActivitiesService/GetActivities",
            request_serializer=activities__pb2.UsersList.SerializeToString,
            response_deserializer=activities__pb2.Activity.FromString,
            _registered_method=True,
        )
        self.ReceiveActivityUpdates = channel.unary_stream(
            "/activities.ActivitiesService/ReceiveActivityUpdates",
            request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            response_deserializer=activities__pb2.Activity.FromString,
            _registered_method=True,
        )


class ActivitiesServiceServicer(object):
    """Сервис для управления активностями пользователя.
    Предоставляет метод для получения стрима активностей пользователя.
    """

    def GetActivities(self, request, context):
        """
        Метод GetActivities принимает список пользователей и возвращает поток
        активностей каждого пользователя из списка.
        Метод ReceiveActivityUpdates принимает пустое сообщение и возвращает поток
        активностей.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def ReceiveActivityUpdates(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_ActivitiesServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "GetActivities": grpc.unary_stream_rpc_method_handler(
            servicer.GetActivities,
            request_deserializer=activities__pb2.UsersList.FromString,
            response_serializer=activities__pb2.Activity.SerializeToString,
        ),
        "ReceiveActivityUpdates": grpc.unary_stream_rpc_method_handler(
            servicer.ReceiveActivityUpdates,
            request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            response_serializer=activities__pb2.Activity.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "activities.ActivitiesService", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers(
        "activities.ActivitiesService", rpc_method_handlers
    )


# This class is part of an EXPERIMENTAL API.
class ActivitiesService(object):
    """Сервис для управления активностями пользователя.
    Предоставляет метод для получения стрима активностей пользователя.
    """

    @staticmethod
    def GetActivities(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_stream(
            request,
            target,
            "/activities.ActivitiesService/GetActivities",
            activities__pb2.UsersList.SerializeToString,
            activities__pb2.Activity.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True,
        )

    @staticmethod
    def ReceiveActivityUpdates(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_stream(
            request,
            target,
            "/activities.ActivitiesService/ReceiveActivityUpdates",
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            activities__pb2.Activity.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True,
        )
