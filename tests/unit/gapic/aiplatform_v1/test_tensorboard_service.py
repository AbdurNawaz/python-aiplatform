# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os

# try/except added for compatibility with python < 3.8
try:
    from unittest import mock
    from unittest.mock import AsyncMock  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    import mock

import grpc
from grpc.experimental import aio
from collections.abc import Iterable
from google.protobuf import json_format
import json
import math
import pytest
from google.api_core import api_core_version
from proto.marshal.rules.dates import DurationRule, TimestampRule
from proto.marshal.rules import wrappers
from requests import Response
from requests import Request, PreparedRequest
from requests.sessions import Session
from google.protobuf import json_format

from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import future
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import operation
from google.api_core import operation_async  # type: ignore
from google.api_core import operations_v1
from google.api_core import path_template
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.aiplatform_v1.services.tensorboard_service import (
    TensorboardServiceAsyncClient,
)
from google.cloud.aiplatform_v1.services.tensorboard_service import (
    TensorboardServiceClient,
)
from google.cloud.aiplatform_v1.services.tensorboard_service import pagers
from google.cloud.aiplatform_v1.services.tensorboard_service import transports
from google.cloud.aiplatform_v1.types import encryption_spec
from google.cloud.aiplatform_v1.types import operation as gca_operation
from google.cloud.aiplatform_v1.types import tensorboard
from google.cloud.aiplatform_v1.types import tensorboard as gca_tensorboard
from google.cloud.aiplatform_v1.types import tensorboard_data
from google.cloud.aiplatform_v1.types import tensorboard_experiment
from google.cloud.aiplatform_v1.types import (
    tensorboard_experiment as gca_tensorboard_experiment,
)
from google.cloud.aiplatform_v1.types import tensorboard_run
from google.cloud.aiplatform_v1.types import tensorboard_run as gca_tensorboard_run
from google.cloud.aiplatform_v1.types import tensorboard_service
from google.cloud.aiplatform_v1.types import tensorboard_time_series
from google.cloud.aiplatform_v1.types import (
    tensorboard_time_series as gca_tensorboard_time_series,
)
from google.cloud.location import locations_pb2
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import options_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.oauth2 import service_account
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
import google.auth


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


# If default endpoint template is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint template so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint_template(client):
    return (
        "test.{UNIVERSE_DOMAIN}"
        if ("localhost" in client._DEFAULT_ENDPOINT_TEMPLATE)
        else client._DEFAULT_ENDPOINT_TEMPLATE
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert TensorboardServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        TensorboardServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        TensorboardServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        TensorboardServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        TensorboardServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        TensorboardServiceClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


def test__read_environment_variables():
    assert TensorboardServiceClient._read_environment_variables() == (
        False,
        "auto",
        None,
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        assert TensorboardServiceClient._read_environment_variables() == (
            True,
            "auto",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        assert TensorboardServiceClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            TensorboardServiceClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        assert TensorboardServiceClient._read_environment_variables() == (
            False,
            "never",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        assert TensorboardServiceClient._read_environment_variables() == (
            False,
            "always",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"}):
        assert TensorboardServiceClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            TensorboardServiceClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_CLOUD_UNIVERSE_DOMAIN": "foo.com"}):
        assert TensorboardServiceClient._read_environment_variables() == (
            False,
            "auto",
            "foo.com",
        )


def test__get_client_cert_source():
    mock_provided_cert_source = mock.Mock()
    mock_default_cert_source = mock.Mock()

    assert TensorboardServiceClient._get_client_cert_source(None, False) is None
    assert (
        TensorboardServiceClient._get_client_cert_source(
            mock_provided_cert_source, False
        )
        is None
    )
    assert (
        TensorboardServiceClient._get_client_cert_source(
            mock_provided_cert_source, True
        )
        == mock_provided_cert_source
    )

    with mock.patch(
        "google.auth.transport.mtls.has_default_client_cert_source", return_value=True
    ):
        with mock.patch(
            "google.auth.transport.mtls.default_client_cert_source",
            return_value=mock_default_cert_source,
        ):
            assert (
                TensorboardServiceClient._get_client_cert_source(None, True)
                is mock_default_cert_source
            )
            assert (
                TensorboardServiceClient._get_client_cert_source(
                    mock_provided_cert_source, "true"
                )
                is mock_provided_cert_source
            )


@mock.patch.object(
    TensorboardServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(TensorboardServiceClient),
)
@mock.patch.object(
    TensorboardServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(TensorboardServiceAsyncClient),
)
def test__get_api_endpoint():
    api_override = "foo.com"
    mock_client_cert_source = mock.Mock()
    default_universe = TensorboardServiceClient._DEFAULT_UNIVERSE
    default_endpoint = TensorboardServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = TensorboardServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    assert (
        TensorboardServiceClient._get_api_endpoint(
            api_override, mock_client_cert_source, default_universe, "always"
        )
        == api_override
    )
    assert (
        TensorboardServiceClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "auto"
        )
        == TensorboardServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        TensorboardServiceClient._get_api_endpoint(None, None, default_universe, "auto")
        == default_endpoint
    )
    assert (
        TensorboardServiceClient._get_api_endpoint(
            None, None, default_universe, "always"
        )
        == TensorboardServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        TensorboardServiceClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "always"
        )
        == TensorboardServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        TensorboardServiceClient._get_api_endpoint(None, None, mock_universe, "never")
        == mock_endpoint
    )
    assert (
        TensorboardServiceClient._get_api_endpoint(
            None, None, default_universe, "never"
        )
        == default_endpoint
    )

    with pytest.raises(MutualTLSChannelError) as excinfo:
        TensorboardServiceClient._get_api_endpoint(
            None, mock_client_cert_source, mock_universe, "auto"
        )
    assert (
        str(excinfo.value)
        == "mTLS is not supported in any universe other than googleapis.com."
    )


def test__get_universe_domain():
    client_universe_domain = "foo.com"
    universe_domain_env = "bar.com"

    assert (
        TensorboardServiceClient._get_universe_domain(
            client_universe_domain, universe_domain_env
        )
        == client_universe_domain
    )
    assert (
        TensorboardServiceClient._get_universe_domain(None, universe_domain_env)
        == universe_domain_env
    )
    assert (
        TensorboardServiceClient._get_universe_domain(None, None)
        == TensorboardServiceClient._DEFAULT_UNIVERSE
    )

    with pytest.raises(ValueError) as excinfo:
        TensorboardServiceClient._get_universe_domain("", None)
    assert str(excinfo.value) == "Universe Domain cannot be an empty string."


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (TensorboardServiceClient, transports.TensorboardServiceGrpcTransport, "grpc"),
        (TensorboardServiceClient, transports.TensorboardServiceRestTransport, "rest"),
    ],
)
def test__validate_universe_domain(client_class, transport_class, transport_name):
    client = client_class(
        transport=transport_class(credentials=ga_credentials.AnonymousCredentials())
    )
    assert client._validate_universe_domain() == True

    # Test the case when universe is already validated.
    assert client._validate_universe_domain() == True

    if transport_name == "grpc":
        # Test the case where credentials are provided by the
        # `local_channel_credentials`. The default universes in both match.
        channel = grpc.secure_channel(
            "http://localhost/", grpc.local_channel_credentials()
        )
        client = client_class(transport=transport_class(channel=channel))
        assert client._validate_universe_domain() == True

        # Test the case where credentials do not exist: e.g. a transport is provided
        # with no credentials. Validation should still succeed because there is no
        # mismatch with non-existent credentials.
        channel = grpc.secure_channel(
            "http://localhost/", grpc.local_channel_credentials()
        )
        transport = transport_class(channel=channel)
        transport._credentials = None
        client = client_class(transport=transport)
        assert client._validate_universe_domain() == True

    # TODO: This is needed to cater for older versions of google-auth
    # Make this test unconditional once the minimum supported version of
    # google-auth becomes 2.23.0 or higher.
    google_auth_major, google_auth_minor = [
        int(part) for part in google.auth.__version__.split(".")[0:2]
    ]
    if google_auth_major > 2 or (google_auth_major == 2 and google_auth_minor >= 23):
        credentials = ga_credentials.AnonymousCredentials()
        credentials._universe_domain = "foo.com"
        # Test the case when there is a universe mismatch from the credentials.
        client = client_class(transport=transport_class(credentials=credentials))
        with pytest.raises(ValueError) as excinfo:
            client._validate_universe_domain()
        assert (
            str(excinfo.value)
            == "The configured universe domain (googleapis.com) does not match the universe domain found in the credentials (foo.com). If you haven't configured the universe domain explicitly, `googleapis.com` is the default."
        )

        # Test the case when there is a universe mismatch from the client.
        #
        # TODO: Make this test unconditional once the minimum supported version of
        # google-api-core becomes 2.15.0 or higher.
        api_core_major, api_core_minor = [
            int(part) for part in api_core_version.__version__.split(".")[0:2]
        ]
        if api_core_major > 2 or (api_core_major == 2 and api_core_minor >= 15):
            client = client_class(
                client_options={"universe_domain": "bar.com"},
                transport=transport_class(
                    credentials=ga_credentials.AnonymousCredentials(),
                ),
            )
            with pytest.raises(ValueError) as excinfo:
                client._validate_universe_domain()
            assert (
                str(excinfo.value)
                == "The configured universe domain (bar.com) does not match the universe domain found in the credentials (googleapis.com). If you haven't configured the universe domain explicitly, `googleapis.com` is the default."
            )

    # Test that ValueError is raised if universe_domain is provided via client options and credentials is None
    with pytest.raises(ValueError):
        client._compare_universes("foo.bar", None)


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (TensorboardServiceClient, "grpc"),
        (TensorboardServiceAsyncClient, "grpc_asyncio"),
        (TensorboardServiceClient, "rest"),
    ],
)
def test_tensorboard_service_client_from_service_account_info(
    client_class, transport_name
):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "aiplatform.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://aiplatform.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.TensorboardServiceGrpcTransport, "grpc"),
        (transports.TensorboardServiceGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.TensorboardServiceRestTransport, "rest"),
    ],
)
def test_tensorboard_service_client_service_account_always_use_jwt(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (TensorboardServiceClient, "grpc"),
        (TensorboardServiceAsyncClient, "grpc_asyncio"),
        (TensorboardServiceClient, "rest"),
    ],
)
def test_tensorboard_service_client_from_service_account_file(
    client_class, transport_name
):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "aiplatform.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://aiplatform.googleapis.com"
        )


def test_tensorboard_service_client_get_transport_class():
    transport = TensorboardServiceClient.get_transport_class()
    available_transports = [
        transports.TensorboardServiceGrpcTransport,
        transports.TensorboardServiceRestTransport,
    ]
    assert transport in available_transports

    transport = TensorboardServiceClient.get_transport_class("grpc")
    assert transport == transports.TensorboardServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (TensorboardServiceClient, transports.TensorboardServiceGrpcTransport, "grpc"),
        (
            TensorboardServiceAsyncClient,
            transports.TensorboardServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (TensorboardServiceClient, transports.TensorboardServiceRestTransport, "rest"),
    ],
)
@mock.patch.object(
    TensorboardServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(TensorboardServiceClient),
)
@mock.patch.object(
    TensorboardServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(TensorboardServiceAsyncClient),
)
def test_tensorboard_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(TensorboardServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(TensorboardServiceClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(transport=transport_name, client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                ),
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            client = client_class(transport=transport_name)
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            client = client_class(transport=transport_name)
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )
    # Check the case api_endpoint is provided
    options = client_options.ClientOptions(
        api_audience="https://language.googleapis.com"
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience="https://language.googleapis.com",
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (
            TensorboardServiceClient,
            transports.TensorboardServiceGrpcTransport,
            "grpc",
            "true",
        ),
        (
            TensorboardServiceAsyncClient,
            transports.TensorboardServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            TensorboardServiceClient,
            transports.TensorboardServiceGrpcTransport,
            "grpc",
            "false",
        ),
        (
            TensorboardServiceAsyncClient,
            transports.TensorboardServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (
            TensorboardServiceClient,
            transports.TensorboardServiceRestTransport,
            "rest",
            "true",
        ),
        (
            TensorboardServiceClient,
            transports.TensorboardServiceRestTransport,
            "rest",
            "false",
        ),
    ],
)
@mock.patch.object(
    TensorboardServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(TensorboardServiceClient),
)
@mock.patch.object(
    TensorboardServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(TensorboardServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_tensorboard_service_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options, transport=transport_name)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                )
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                with mock.patch(
                    "google.auth.transport.mtls.default_client_cert_source",
                    return_value=client_cert_source_callback,
                ):
                    if use_client_cert_env == "false":
                        expected_host = client._DEFAULT_ENDPOINT_TEMPLATE.format(
                            UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                        )
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class(transport=transport_name)
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                        always_use_jwt_access=True,
                        api_audience=None,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=False,
            ):
                patched.return_value = None
                client = client_class(transport=transport_name)
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                        UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                    ),
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                    api_audience=None,
                )


@pytest.mark.parametrize(
    "client_class", [TensorboardServiceClient, TensorboardServiceAsyncClient]
)
@mock.patch.object(
    TensorboardServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(TensorboardServiceClient),
)
@mock.patch.object(
    TensorboardServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(TensorboardServiceAsyncClient),
)
def test_tensorboard_service_client_get_mtls_endpoint_and_cert_source(client_class):
    mock_client_cert_source = mock.Mock()

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "true".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source == mock_client_cert_source

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "false".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        mock_client_cert_source = mock.Mock()
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert doesn't exist.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=False,
        ):
            api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
            assert api_endpoint == client_class.DEFAULT_ENDPOINT
            assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert exists.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=True,
        ):
            with mock.patch(
                "google.auth.transport.mtls.default_client_cert_source",
                return_value=mock_client_cert_source,
            ):
                (
                    api_endpoint,
                    cert_source,
                ) = client_class.get_mtls_endpoint_and_cert_source()
                assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
                assert cert_source == mock_client_cert_source

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            client_class.get_mtls_endpoint_and_cert_source()

        assert (
            str(excinfo.value)
            == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
        )

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            client_class.get_mtls_endpoint_and_cert_source()

        assert (
            str(excinfo.value)
            == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
        )


@pytest.mark.parametrize(
    "client_class", [TensorboardServiceClient, TensorboardServiceAsyncClient]
)
@mock.patch.object(
    TensorboardServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(TensorboardServiceClient),
)
@mock.patch.object(
    TensorboardServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(TensorboardServiceAsyncClient),
)
def test_tensorboard_service_client_client_api_endpoint(client_class):
    mock_client_cert_source = client_cert_source_callback
    api_override = "foo.com"
    default_universe = TensorboardServiceClient._DEFAULT_UNIVERSE
    default_endpoint = TensorboardServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = TensorboardServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    # If ClientOptions.api_endpoint is set and GOOGLE_API_USE_CLIENT_CERTIFICATE="true",
    # use ClientOptions.api_endpoint as the api endpoint regardless.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
        ):
            options = client_options.ClientOptions(
                client_cert_source=mock_client_cert_source, api_endpoint=api_override
            )
            client = client_class(
                client_options=options,
                credentials=ga_credentials.AnonymousCredentials(),
            )
            assert client.api_endpoint == api_override

    # If ClientOptions.api_endpoint is not set and GOOGLE_API_USE_MTLS_ENDPOINT="never",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with GDU as the api endpoint.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        client = client_class(credentials=ga_credentials.AnonymousCredentials())
        assert client.api_endpoint == default_endpoint

    # If ClientOptions.api_endpoint is not set and GOOGLE_API_USE_MTLS_ENDPOINT="always",
    # use the DEFAULT_MTLS_ENDPOINT as the api endpoint.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        client = client_class(credentials=ga_credentials.AnonymousCredentials())
        assert client.api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT

    # If ClientOptions.api_endpoint is not set, GOOGLE_API_USE_MTLS_ENDPOINT="auto" (default),
    # GOOGLE_API_USE_CLIENT_CERTIFICATE="false" (default), default cert source doesn't exist,
    # and ClientOptions.universe_domain="bar.com",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with universe domain as the api endpoint.
    options = client_options.ClientOptions()
    universe_exists = hasattr(options, "universe_domain")
    if universe_exists:
        options = client_options.ClientOptions(universe_domain=mock_universe)
        client = client_class(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )
    else:
        client = client_class(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )
    assert client.api_endpoint == (
        mock_endpoint if universe_exists else default_endpoint
    )
    assert client.universe_domain == (
        mock_universe if universe_exists else default_universe
    )

    # If ClientOptions does not have a universe domain attribute and GOOGLE_API_USE_MTLS_ENDPOINT="never",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with GDU as the api endpoint.
    options = client_options.ClientOptions()
    if hasattr(options, "universe_domain"):
        delattr(options, "universe_domain")
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        client = client_class(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )
        assert client.api_endpoint == default_endpoint


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (TensorboardServiceClient, transports.TensorboardServiceGrpcTransport, "grpc"),
        (
            TensorboardServiceAsyncClient,
            transports.TensorboardServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (TensorboardServiceClient, transports.TensorboardServiceRestTransport, "rest"),
    ],
)
def test_tensorboard_service_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(
        scopes=["1", "2"],
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (
            TensorboardServiceClient,
            transports.TensorboardServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            TensorboardServiceAsyncClient,
            transports.TensorboardServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (
            TensorboardServiceClient,
            transports.TensorboardServiceRestTransport,
            "rest",
            None,
        ),
    ],
)
def test_tensorboard_service_client_client_options_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


def test_tensorboard_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.aiplatform_v1.services.tensorboard_service.transports.TensorboardServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = TensorboardServiceClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (
            TensorboardServiceClient,
            transports.TensorboardServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            TensorboardServiceAsyncClient,
            transports.TensorboardServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_tensorboard_service_client_create_channel_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # test that the credentials from file are saved and used as the credentials.
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel"
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        file_creds = ga_credentials.AnonymousCredentials()
        load_creds.return_value = (file_creds, None)
        adc.return_value = (creds, None)
        client = client_class(client_options=options, transport=transport_name)
        create_channel.assert_called_with(
            "aiplatform.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
            ),
            scopes=None,
            default_host="aiplatform.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.CreateTensorboardRequest,
        dict,
    ],
)
def test_create_tensorboard(request_type, transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tensorboard), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_tensorboard(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.CreateTensorboardRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_tensorboard_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tensorboard), "__call__"
    ) as call:
        client.create_tensorboard()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.CreateTensorboardRequest()


@pytest.mark.asyncio
async def test_create_tensorboard_async(
    transport: str = "grpc_asyncio",
    request_type=tensorboard_service.CreateTensorboardRequest,
):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tensorboard), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_tensorboard(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.CreateTensorboardRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_tensorboard_async_from_dict():
    await test_create_tensorboard_async(request_type=dict)


def test_create_tensorboard_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.CreateTensorboardRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tensorboard), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_tensorboard(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_tensorboard_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.CreateTensorboardRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tensorboard), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_tensorboard(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_tensorboard_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tensorboard), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_tensorboard(
            parent="parent_value",
            tensorboard=gca_tensorboard.Tensorboard(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].tensorboard
        mock_val = gca_tensorboard.Tensorboard(name="name_value")
        assert arg == mock_val


def test_create_tensorboard_flattened_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_tensorboard(
            tensorboard_service.CreateTensorboardRequest(),
            parent="parent_value",
            tensorboard=gca_tensorboard.Tensorboard(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_tensorboard_flattened_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tensorboard), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_tensorboard(
            parent="parent_value",
            tensorboard=gca_tensorboard.Tensorboard(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].tensorboard
        mock_val = gca_tensorboard.Tensorboard(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_tensorboard_flattened_error_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_tensorboard(
            tensorboard_service.CreateTensorboardRequest(),
            parent="parent_value",
            tensorboard=gca_tensorboard.Tensorboard(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.GetTensorboardRequest,
        dict,
    ],
)
def test_get_tensorboard(request_type, transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tensorboard), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard.Tensorboard(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            blob_storage_path_prefix="blob_storage_path_prefix_value",
            run_count=989,
            etag="etag_value",
            is_default=True,
        )
        response = client.get_tensorboard(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.GetTensorboardRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tensorboard.Tensorboard)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.blob_storage_path_prefix == "blob_storage_path_prefix_value"
    assert response.run_count == 989
    assert response.etag == "etag_value"
    assert response.is_default is True


def test_get_tensorboard_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tensorboard), "__call__") as call:
        client.get_tensorboard()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.GetTensorboardRequest()


@pytest.mark.asyncio
async def test_get_tensorboard_async(
    transport: str = "grpc_asyncio",
    request_type=tensorboard_service.GetTensorboardRequest,
):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tensorboard), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard.Tensorboard(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                blob_storage_path_prefix="blob_storage_path_prefix_value",
                run_count=989,
                etag="etag_value",
                is_default=True,
            )
        )
        response = await client.get_tensorboard(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.GetTensorboardRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tensorboard.Tensorboard)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.blob_storage_path_prefix == "blob_storage_path_prefix_value"
    assert response.run_count == 989
    assert response.etag == "etag_value"
    assert response.is_default is True


@pytest.mark.asyncio
async def test_get_tensorboard_async_from_dict():
    await test_get_tensorboard_async(request_type=dict)


def test_get_tensorboard_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.GetTensorboardRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tensorboard), "__call__") as call:
        call.return_value = tensorboard.Tensorboard()
        client.get_tensorboard(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_tensorboard_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.GetTensorboardRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tensorboard), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard.Tensorboard()
        )
        await client.get_tensorboard(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_tensorboard_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tensorboard), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard.Tensorboard()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_tensorboard(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_tensorboard_flattened_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_tensorboard(
            tensorboard_service.GetTensorboardRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_tensorboard_flattened_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tensorboard), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard.Tensorboard()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard.Tensorboard()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_tensorboard(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_tensorboard_flattened_error_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_tensorboard(
            tensorboard_service.GetTensorboardRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.UpdateTensorboardRequest,
        dict,
    ],
)
def test_update_tensorboard(request_type, transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tensorboard), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_tensorboard(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.UpdateTensorboardRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_tensorboard_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tensorboard), "__call__"
    ) as call:
        client.update_tensorboard()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.UpdateTensorboardRequest()


@pytest.mark.asyncio
async def test_update_tensorboard_async(
    transport: str = "grpc_asyncio",
    request_type=tensorboard_service.UpdateTensorboardRequest,
):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tensorboard), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_tensorboard(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.UpdateTensorboardRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_tensorboard_async_from_dict():
    await test_update_tensorboard_async(request_type=dict)


def test_update_tensorboard_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.UpdateTensorboardRequest()

    request.tensorboard.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tensorboard), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_tensorboard(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "tensorboard.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_tensorboard_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.UpdateTensorboardRequest()

    request.tensorboard.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tensorboard), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_tensorboard(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "tensorboard.name=name_value",
    ) in kw["metadata"]


def test_update_tensorboard_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tensorboard), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_tensorboard(
            tensorboard=gca_tensorboard.Tensorboard(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].tensorboard
        mock_val = gca_tensorboard.Tensorboard(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_tensorboard_flattened_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_tensorboard(
            tensorboard_service.UpdateTensorboardRequest(),
            tensorboard=gca_tensorboard.Tensorboard(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_tensorboard_flattened_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tensorboard), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_tensorboard(
            tensorboard=gca_tensorboard.Tensorboard(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].tensorboard
        mock_val = gca_tensorboard.Tensorboard(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_tensorboard_flattened_error_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_tensorboard(
            tensorboard_service.UpdateTensorboardRequest(),
            tensorboard=gca_tensorboard.Tensorboard(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.ListTensorboardsRequest,
        dict,
    ],
)
def test_list_tensorboards(request_type, transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboards), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_service.ListTensorboardsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_tensorboards(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.ListTensorboardsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTensorboardsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_tensorboards_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboards), "__call__"
    ) as call:
        client.list_tensorboards()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.ListTensorboardsRequest()


@pytest.mark.asyncio
async def test_list_tensorboards_async(
    transport: str = "grpc_asyncio",
    request_type=tensorboard_service.ListTensorboardsRequest,
):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboards), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.ListTensorboardsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_tensorboards(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.ListTensorboardsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTensorboardsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_tensorboards_async_from_dict():
    await test_list_tensorboards_async(request_type=dict)


def test_list_tensorboards_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.ListTensorboardsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboards), "__call__"
    ) as call:
        call.return_value = tensorboard_service.ListTensorboardsResponse()
        client.list_tensorboards(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_tensorboards_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.ListTensorboardsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboards), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.ListTensorboardsResponse()
        )
        await client.list_tensorboards(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_tensorboards_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboards), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_service.ListTensorboardsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_tensorboards(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_tensorboards_flattened_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_tensorboards(
            tensorboard_service.ListTensorboardsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_tensorboards_flattened_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboards), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_service.ListTensorboardsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.ListTensorboardsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_tensorboards(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_tensorboards_flattened_error_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_tensorboards(
            tensorboard_service.ListTensorboardsRequest(),
            parent="parent_value",
        )


def test_list_tensorboards_pager(transport_name: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboards), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            tensorboard_service.ListTensorboardsResponse(
                tensorboards=[
                    tensorboard.Tensorboard(),
                    tensorboard.Tensorboard(),
                    tensorboard.Tensorboard(),
                ],
                next_page_token="abc",
            ),
            tensorboard_service.ListTensorboardsResponse(
                tensorboards=[],
                next_page_token="def",
            ),
            tensorboard_service.ListTensorboardsResponse(
                tensorboards=[
                    tensorboard.Tensorboard(),
                ],
                next_page_token="ghi",
            ),
            tensorboard_service.ListTensorboardsResponse(
                tensorboards=[
                    tensorboard.Tensorboard(),
                    tensorboard.Tensorboard(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_tensorboards(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, tensorboard.Tensorboard) for i in results)


def test_list_tensorboards_pages(transport_name: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboards), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            tensorboard_service.ListTensorboardsResponse(
                tensorboards=[
                    tensorboard.Tensorboard(),
                    tensorboard.Tensorboard(),
                    tensorboard.Tensorboard(),
                ],
                next_page_token="abc",
            ),
            tensorboard_service.ListTensorboardsResponse(
                tensorboards=[],
                next_page_token="def",
            ),
            tensorboard_service.ListTensorboardsResponse(
                tensorboards=[
                    tensorboard.Tensorboard(),
                ],
                next_page_token="ghi",
            ),
            tensorboard_service.ListTensorboardsResponse(
                tensorboards=[
                    tensorboard.Tensorboard(),
                    tensorboard.Tensorboard(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_tensorboards(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_tensorboards_async_pager():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboards),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            tensorboard_service.ListTensorboardsResponse(
                tensorboards=[
                    tensorboard.Tensorboard(),
                    tensorboard.Tensorboard(),
                    tensorboard.Tensorboard(),
                ],
                next_page_token="abc",
            ),
            tensorboard_service.ListTensorboardsResponse(
                tensorboards=[],
                next_page_token="def",
            ),
            tensorboard_service.ListTensorboardsResponse(
                tensorboards=[
                    tensorboard.Tensorboard(),
                ],
                next_page_token="ghi",
            ),
            tensorboard_service.ListTensorboardsResponse(
                tensorboards=[
                    tensorboard.Tensorboard(),
                    tensorboard.Tensorboard(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_tensorboards(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, tensorboard.Tensorboard) for i in responses)


@pytest.mark.asyncio
async def test_list_tensorboards_async_pages():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboards),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            tensorboard_service.ListTensorboardsResponse(
                tensorboards=[
                    tensorboard.Tensorboard(),
                    tensorboard.Tensorboard(),
                    tensorboard.Tensorboard(),
                ],
                next_page_token="abc",
            ),
            tensorboard_service.ListTensorboardsResponse(
                tensorboards=[],
                next_page_token="def",
            ),
            tensorboard_service.ListTensorboardsResponse(
                tensorboards=[
                    tensorboard.Tensorboard(),
                ],
                next_page_token="ghi",
            ),
            tensorboard_service.ListTensorboardsResponse(
                tensorboards=[
                    tensorboard.Tensorboard(),
                    tensorboard.Tensorboard(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_tensorboards(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.DeleteTensorboardRequest,
        dict,
    ],
)
def test_delete_tensorboard(request_type, transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tensorboard), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_tensorboard(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.DeleteTensorboardRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_tensorboard_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tensorboard), "__call__"
    ) as call:
        client.delete_tensorboard()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.DeleteTensorboardRequest()


@pytest.mark.asyncio
async def test_delete_tensorboard_async(
    transport: str = "grpc_asyncio",
    request_type=tensorboard_service.DeleteTensorboardRequest,
):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tensorboard), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_tensorboard(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.DeleteTensorboardRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_tensorboard_async_from_dict():
    await test_delete_tensorboard_async(request_type=dict)


def test_delete_tensorboard_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.DeleteTensorboardRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tensorboard), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_tensorboard(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_tensorboard_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.DeleteTensorboardRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tensorboard), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_tensorboard(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_delete_tensorboard_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tensorboard), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_tensorboard(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_tensorboard_flattened_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_tensorboard(
            tensorboard_service.DeleteTensorboardRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_tensorboard_flattened_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tensorboard), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_tensorboard(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_tensorboard_flattened_error_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_tensorboard(
            tensorboard_service.DeleteTensorboardRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.ReadTensorboardUsageRequest,
        dict,
    ],
)
def test_read_tensorboard_usage(request_type, transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.read_tensorboard_usage), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_service.ReadTensorboardUsageResponse()
        response = client.read_tensorboard_usage(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.ReadTensorboardUsageRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tensorboard_service.ReadTensorboardUsageResponse)


def test_read_tensorboard_usage_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.read_tensorboard_usage), "__call__"
    ) as call:
        client.read_tensorboard_usage()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.ReadTensorboardUsageRequest()


@pytest.mark.asyncio
async def test_read_tensorboard_usage_async(
    transport: str = "grpc_asyncio",
    request_type=tensorboard_service.ReadTensorboardUsageRequest,
):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.read_tensorboard_usage), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.ReadTensorboardUsageResponse()
        )
        response = await client.read_tensorboard_usage(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.ReadTensorboardUsageRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tensorboard_service.ReadTensorboardUsageResponse)


@pytest.mark.asyncio
async def test_read_tensorboard_usage_async_from_dict():
    await test_read_tensorboard_usage_async(request_type=dict)


def test_read_tensorboard_usage_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.ReadTensorboardUsageRequest()

    request.tensorboard = "tensorboard_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.read_tensorboard_usage), "__call__"
    ) as call:
        call.return_value = tensorboard_service.ReadTensorboardUsageResponse()
        client.read_tensorboard_usage(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "tensorboard=tensorboard_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_read_tensorboard_usage_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.ReadTensorboardUsageRequest()

    request.tensorboard = "tensorboard_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.read_tensorboard_usage), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.ReadTensorboardUsageResponse()
        )
        await client.read_tensorboard_usage(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "tensorboard=tensorboard_value",
    ) in kw["metadata"]


def test_read_tensorboard_usage_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.read_tensorboard_usage), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_service.ReadTensorboardUsageResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.read_tensorboard_usage(
            tensorboard="tensorboard_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].tensorboard
        mock_val = "tensorboard_value"
        assert arg == mock_val


def test_read_tensorboard_usage_flattened_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.read_tensorboard_usage(
            tensorboard_service.ReadTensorboardUsageRequest(),
            tensorboard="tensorboard_value",
        )


@pytest.mark.asyncio
async def test_read_tensorboard_usage_flattened_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.read_tensorboard_usage), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_service.ReadTensorboardUsageResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.ReadTensorboardUsageResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.read_tensorboard_usage(
            tensorboard="tensorboard_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].tensorboard
        mock_val = "tensorboard_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_read_tensorboard_usage_flattened_error_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.read_tensorboard_usage(
            tensorboard_service.ReadTensorboardUsageRequest(),
            tensorboard="tensorboard_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.ReadTensorboardSizeRequest,
        dict,
    ],
)
def test_read_tensorboard_size(request_type, transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.read_tensorboard_size), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_service.ReadTensorboardSizeResponse(
            storage_size_byte=1826,
        )
        response = client.read_tensorboard_size(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.ReadTensorboardSizeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tensorboard_service.ReadTensorboardSizeResponse)
    assert response.storage_size_byte == 1826


def test_read_tensorboard_size_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.read_tensorboard_size), "__call__"
    ) as call:
        client.read_tensorboard_size()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.ReadTensorboardSizeRequest()


@pytest.mark.asyncio
async def test_read_tensorboard_size_async(
    transport: str = "grpc_asyncio",
    request_type=tensorboard_service.ReadTensorboardSizeRequest,
):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.read_tensorboard_size), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.ReadTensorboardSizeResponse(
                storage_size_byte=1826,
            )
        )
        response = await client.read_tensorboard_size(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.ReadTensorboardSizeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tensorboard_service.ReadTensorboardSizeResponse)
    assert response.storage_size_byte == 1826


@pytest.mark.asyncio
async def test_read_tensorboard_size_async_from_dict():
    await test_read_tensorboard_size_async(request_type=dict)


def test_read_tensorboard_size_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.ReadTensorboardSizeRequest()

    request.tensorboard = "tensorboard_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.read_tensorboard_size), "__call__"
    ) as call:
        call.return_value = tensorboard_service.ReadTensorboardSizeResponse()
        client.read_tensorboard_size(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "tensorboard=tensorboard_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_read_tensorboard_size_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.ReadTensorboardSizeRequest()

    request.tensorboard = "tensorboard_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.read_tensorboard_size), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.ReadTensorboardSizeResponse()
        )
        await client.read_tensorboard_size(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "tensorboard=tensorboard_value",
    ) in kw["metadata"]


def test_read_tensorboard_size_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.read_tensorboard_size), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_service.ReadTensorboardSizeResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.read_tensorboard_size(
            tensorboard="tensorboard_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].tensorboard
        mock_val = "tensorboard_value"
        assert arg == mock_val


def test_read_tensorboard_size_flattened_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.read_tensorboard_size(
            tensorboard_service.ReadTensorboardSizeRequest(),
            tensorboard="tensorboard_value",
        )


@pytest.mark.asyncio
async def test_read_tensorboard_size_flattened_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.read_tensorboard_size), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_service.ReadTensorboardSizeResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.ReadTensorboardSizeResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.read_tensorboard_size(
            tensorboard="tensorboard_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].tensorboard
        mock_val = "tensorboard_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_read_tensorboard_size_flattened_error_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.read_tensorboard_size(
            tensorboard_service.ReadTensorboardSizeRequest(),
            tensorboard="tensorboard_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.CreateTensorboardExperimentRequest,
        dict,
    ],
)
def test_create_tensorboard_experiment(request_type, transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tensorboard_experiment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gca_tensorboard_experiment.TensorboardExperiment(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            etag="etag_value",
            source="source_value",
        )
        response = client.create_tensorboard_experiment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.CreateTensorboardExperimentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gca_tensorboard_experiment.TensorboardExperiment)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.etag == "etag_value"
    assert response.source == "source_value"


def test_create_tensorboard_experiment_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tensorboard_experiment), "__call__"
    ) as call:
        client.create_tensorboard_experiment()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.CreateTensorboardExperimentRequest()


@pytest.mark.asyncio
async def test_create_tensorboard_experiment_async(
    transport: str = "grpc_asyncio",
    request_type=tensorboard_service.CreateTensorboardExperimentRequest,
):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tensorboard_experiment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gca_tensorboard_experiment.TensorboardExperiment(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                etag="etag_value",
                source="source_value",
            )
        )
        response = await client.create_tensorboard_experiment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.CreateTensorboardExperimentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gca_tensorboard_experiment.TensorboardExperiment)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.etag == "etag_value"
    assert response.source == "source_value"


@pytest.mark.asyncio
async def test_create_tensorboard_experiment_async_from_dict():
    await test_create_tensorboard_experiment_async(request_type=dict)


def test_create_tensorboard_experiment_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.CreateTensorboardExperimentRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tensorboard_experiment), "__call__"
    ) as call:
        call.return_value = gca_tensorboard_experiment.TensorboardExperiment()
        client.create_tensorboard_experiment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_tensorboard_experiment_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.CreateTensorboardExperimentRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tensorboard_experiment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gca_tensorboard_experiment.TensorboardExperiment()
        )
        await client.create_tensorboard_experiment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_tensorboard_experiment_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tensorboard_experiment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gca_tensorboard_experiment.TensorboardExperiment()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_tensorboard_experiment(
            parent="parent_value",
            tensorboard_experiment=gca_tensorboard_experiment.TensorboardExperiment(
                name="name_value"
            ),
            tensorboard_experiment_id="tensorboard_experiment_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].tensorboard_experiment
        mock_val = gca_tensorboard_experiment.TensorboardExperiment(name="name_value")
        assert arg == mock_val
        arg = args[0].tensorboard_experiment_id
        mock_val = "tensorboard_experiment_id_value"
        assert arg == mock_val


def test_create_tensorboard_experiment_flattened_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_tensorboard_experiment(
            tensorboard_service.CreateTensorboardExperimentRequest(),
            parent="parent_value",
            tensorboard_experiment=gca_tensorboard_experiment.TensorboardExperiment(
                name="name_value"
            ),
            tensorboard_experiment_id="tensorboard_experiment_id_value",
        )


@pytest.mark.asyncio
async def test_create_tensorboard_experiment_flattened_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tensorboard_experiment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gca_tensorboard_experiment.TensorboardExperiment()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gca_tensorboard_experiment.TensorboardExperiment()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_tensorboard_experiment(
            parent="parent_value",
            tensorboard_experiment=gca_tensorboard_experiment.TensorboardExperiment(
                name="name_value"
            ),
            tensorboard_experiment_id="tensorboard_experiment_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].tensorboard_experiment
        mock_val = gca_tensorboard_experiment.TensorboardExperiment(name="name_value")
        assert arg == mock_val
        arg = args[0].tensorboard_experiment_id
        mock_val = "tensorboard_experiment_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_tensorboard_experiment_flattened_error_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_tensorboard_experiment(
            tensorboard_service.CreateTensorboardExperimentRequest(),
            parent="parent_value",
            tensorboard_experiment=gca_tensorboard_experiment.TensorboardExperiment(
                name="name_value"
            ),
            tensorboard_experiment_id="tensorboard_experiment_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.GetTensorboardExperimentRequest,
        dict,
    ],
)
def test_get_tensorboard_experiment(request_type, transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_tensorboard_experiment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_experiment.TensorboardExperiment(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            etag="etag_value",
            source="source_value",
        )
        response = client.get_tensorboard_experiment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.GetTensorboardExperimentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tensorboard_experiment.TensorboardExperiment)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.etag == "etag_value"
    assert response.source == "source_value"


def test_get_tensorboard_experiment_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_tensorboard_experiment), "__call__"
    ) as call:
        client.get_tensorboard_experiment()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.GetTensorboardExperimentRequest()


@pytest.mark.asyncio
async def test_get_tensorboard_experiment_async(
    transport: str = "grpc_asyncio",
    request_type=tensorboard_service.GetTensorboardExperimentRequest,
):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_tensorboard_experiment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_experiment.TensorboardExperiment(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                etag="etag_value",
                source="source_value",
            )
        )
        response = await client.get_tensorboard_experiment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.GetTensorboardExperimentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tensorboard_experiment.TensorboardExperiment)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.etag == "etag_value"
    assert response.source == "source_value"


@pytest.mark.asyncio
async def test_get_tensorboard_experiment_async_from_dict():
    await test_get_tensorboard_experiment_async(request_type=dict)


def test_get_tensorboard_experiment_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.GetTensorboardExperimentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_tensorboard_experiment), "__call__"
    ) as call:
        call.return_value = tensorboard_experiment.TensorboardExperiment()
        client.get_tensorboard_experiment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_tensorboard_experiment_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.GetTensorboardExperimentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_tensorboard_experiment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_experiment.TensorboardExperiment()
        )
        await client.get_tensorboard_experiment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_tensorboard_experiment_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_tensorboard_experiment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_experiment.TensorboardExperiment()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_tensorboard_experiment(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_tensorboard_experiment_flattened_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_tensorboard_experiment(
            tensorboard_service.GetTensorboardExperimentRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_tensorboard_experiment_flattened_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_tensorboard_experiment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_experiment.TensorboardExperiment()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_experiment.TensorboardExperiment()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_tensorboard_experiment(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_tensorboard_experiment_flattened_error_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_tensorboard_experiment(
            tensorboard_service.GetTensorboardExperimentRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.UpdateTensorboardExperimentRequest,
        dict,
    ],
)
def test_update_tensorboard_experiment(request_type, transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tensorboard_experiment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gca_tensorboard_experiment.TensorboardExperiment(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            etag="etag_value",
            source="source_value",
        )
        response = client.update_tensorboard_experiment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.UpdateTensorboardExperimentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gca_tensorboard_experiment.TensorboardExperiment)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.etag == "etag_value"
    assert response.source == "source_value"


def test_update_tensorboard_experiment_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tensorboard_experiment), "__call__"
    ) as call:
        client.update_tensorboard_experiment()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.UpdateTensorboardExperimentRequest()


@pytest.mark.asyncio
async def test_update_tensorboard_experiment_async(
    transport: str = "grpc_asyncio",
    request_type=tensorboard_service.UpdateTensorboardExperimentRequest,
):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tensorboard_experiment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gca_tensorboard_experiment.TensorboardExperiment(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                etag="etag_value",
                source="source_value",
            )
        )
        response = await client.update_tensorboard_experiment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.UpdateTensorboardExperimentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gca_tensorboard_experiment.TensorboardExperiment)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.etag == "etag_value"
    assert response.source == "source_value"


@pytest.mark.asyncio
async def test_update_tensorboard_experiment_async_from_dict():
    await test_update_tensorboard_experiment_async(request_type=dict)


def test_update_tensorboard_experiment_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.UpdateTensorboardExperimentRequest()

    request.tensorboard_experiment.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tensorboard_experiment), "__call__"
    ) as call:
        call.return_value = gca_tensorboard_experiment.TensorboardExperiment()
        client.update_tensorboard_experiment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "tensorboard_experiment.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_tensorboard_experiment_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.UpdateTensorboardExperimentRequest()

    request.tensorboard_experiment.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tensorboard_experiment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gca_tensorboard_experiment.TensorboardExperiment()
        )
        await client.update_tensorboard_experiment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "tensorboard_experiment.name=name_value",
    ) in kw["metadata"]


def test_update_tensorboard_experiment_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tensorboard_experiment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gca_tensorboard_experiment.TensorboardExperiment()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_tensorboard_experiment(
            tensorboard_experiment=gca_tensorboard_experiment.TensorboardExperiment(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].tensorboard_experiment
        mock_val = gca_tensorboard_experiment.TensorboardExperiment(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_tensorboard_experiment_flattened_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_tensorboard_experiment(
            tensorboard_service.UpdateTensorboardExperimentRequest(),
            tensorboard_experiment=gca_tensorboard_experiment.TensorboardExperiment(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_tensorboard_experiment_flattened_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tensorboard_experiment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gca_tensorboard_experiment.TensorboardExperiment()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gca_tensorboard_experiment.TensorboardExperiment()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_tensorboard_experiment(
            tensorboard_experiment=gca_tensorboard_experiment.TensorboardExperiment(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].tensorboard_experiment
        mock_val = gca_tensorboard_experiment.TensorboardExperiment(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_tensorboard_experiment_flattened_error_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_tensorboard_experiment(
            tensorboard_service.UpdateTensorboardExperimentRequest(),
            tensorboard_experiment=gca_tensorboard_experiment.TensorboardExperiment(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.ListTensorboardExperimentsRequest,
        dict,
    ],
)
def test_list_tensorboard_experiments(request_type, transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboard_experiments), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_service.ListTensorboardExperimentsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_tensorboard_experiments(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.ListTensorboardExperimentsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTensorboardExperimentsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_tensorboard_experiments_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboard_experiments), "__call__"
    ) as call:
        client.list_tensorboard_experiments()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.ListTensorboardExperimentsRequest()


@pytest.mark.asyncio
async def test_list_tensorboard_experiments_async(
    transport: str = "grpc_asyncio",
    request_type=tensorboard_service.ListTensorboardExperimentsRequest,
):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboard_experiments), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.ListTensorboardExperimentsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_tensorboard_experiments(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.ListTensorboardExperimentsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTensorboardExperimentsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_tensorboard_experiments_async_from_dict():
    await test_list_tensorboard_experiments_async(request_type=dict)


def test_list_tensorboard_experiments_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.ListTensorboardExperimentsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboard_experiments), "__call__"
    ) as call:
        call.return_value = tensorboard_service.ListTensorboardExperimentsResponse()
        client.list_tensorboard_experiments(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_tensorboard_experiments_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.ListTensorboardExperimentsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboard_experiments), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.ListTensorboardExperimentsResponse()
        )
        await client.list_tensorboard_experiments(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_tensorboard_experiments_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboard_experiments), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_service.ListTensorboardExperimentsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_tensorboard_experiments(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_tensorboard_experiments_flattened_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_tensorboard_experiments(
            tensorboard_service.ListTensorboardExperimentsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_tensorboard_experiments_flattened_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboard_experiments), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_service.ListTensorboardExperimentsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.ListTensorboardExperimentsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_tensorboard_experiments(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_tensorboard_experiments_flattened_error_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_tensorboard_experiments(
            tensorboard_service.ListTensorboardExperimentsRequest(),
            parent="parent_value",
        )


def test_list_tensorboard_experiments_pager(transport_name: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboard_experiments), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            tensorboard_service.ListTensorboardExperimentsResponse(
                tensorboard_experiments=[
                    tensorboard_experiment.TensorboardExperiment(),
                    tensorboard_experiment.TensorboardExperiment(),
                    tensorboard_experiment.TensorboardExperiment(),
                ],
                next_page_token="abc",
            ),
            tensorboard_service.ListTensorboardExperimentsResponse(
                tensorboard_experiments=[],
                next_page_token="def",
            ),
            tensorboard_service.ListTensorboardExperimentsResponse(
                tensorboard_experiments=[
                    tensorboard_experiment.TensorboardExperiment(),
                ],
                next_page_token="ghi",
            ),
            tensorboard_service.ListTensorboardExperimentsResponse(
                tensorboard_experiments=[
                    tensorboard_experiment.TensorboardExperiment(),
                    tensorboard_experiment.TensorboardExperiment(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_tensorboard_experiments(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, tensorboard_experiment.TensorboardExperiment) for i in results
        )


def test_list_tensorboard_experiments_pages(transport_name: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboard_experiments), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            tensorboard_service.ListTensorboardExperimentsResponse(
                tensorboard_experiments=[
                    tensorboard_experiment.TensorboardExperiment(),
                    tensorboard_experiment.TensorboardExperiment(),
                    tensorboard_experiment.TensorboardExperiment(),
                ],
                next_page_token="abc",
            ),
            tensorboard_service.ListTensorboardExperimentsResponse(
                tensorboard_experiments=[],
                next_page_token="def",
            ),
            tensorboard_service.ListTensorboardExperimentsResponse(
                tensorboard_experiments=[
                    tensorboard_experiment.TensorboardExperiment(),
                ],
                next_page_token="ghi",
            ),
            tensorboard_service.ListTensorboardExperimentsResponse(
                tensorboard_experiments=[
                    tensorboard_experiment.TensorboardExperiment(),
                    tensorboard_experiment.TensorboardExperiment(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_tensorboard_experiments(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_tensorboard_experiments_async_pager():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboard_experiments),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            tensorboard_service.ListTensorboardExperimentsResponse(
                tensorboard_experiments=[
                    tensorboard_experiment.TensorboardExperiment(),
                    tensorboard_experiment.TensorboardExperiment(),
                    tensorboard_experiment.TensorboardExperiment(),
                ],
                next_page_token="abc",
            ),
            tensorboard_service.ListTensorboardExperimentsResponse(
                tensorboard_experiments=[],
                next_page_token="def",
            ),
            tensorboard_service.ListTensorboardExperimentsResponse(
                tensorboard_experiments=[
                    tensorboard_experiment.TensorboardExperiment(),
                ],
                next_page_token="ghi",
            ),
            tensorboard_service.ListTensorboardExperimentsResponse(
                tensorboard_experiments=[
                    tensorboard_experiment.TensorboardExperiment(),
                    tensorboard_experiment.TensorboardExperiment(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_tensorboard_experiments(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, tensorboard_experiment.TensorboardExperiment)
            for i in responses
        )


@pytest.mark.asyncio
async def test_list_tensorboard_experiments_async_pages():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboard_experiments),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            tensorboard_service.ListTensorboardExperimentsResponse(
                tensorboard_experiments=[
                    tensorboard_experiment.TensorboardExperiment(),
                    tensorboard_experiment.TensorboardExperiment(),
                    tensorboard_experiment.TensorboardExperiment(),
                ],
                next_page_token="abc",
            ),
            tensorboard_service.ListTensorboardExperimentsResponse(
                tensorboard_experiments=[],
                next_page_token="def",
            ),
            tensorboard_service.ListTensorboardExperimentsResponse(
                tensorboard_experiments=[
                    tensorboard_experiment.TensorboardExperiment(),
                ],
                next_page_token="ghi",
            ),
            tensorboard_service.ListTensorboardExperimentsResponse(
                tensorboard_experiments=[
                    tensorboard_experiment.TensorboardExperiment(),
                    tensorboard_experiment.TensorboardExperiment(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_tensorboard_experiments(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.DeleteTensorboardExperimentRequest,
        dict,
    ],
)
def test_delete_tensorboard_experiment(request_type, transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tensorboard_experiment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_tensorboard_experiment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.DeleteTensorboardExperimentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_tensorboard_experiment_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tensorboard_experiment), "__call__"
    ) as call:
        client.delete_tensorboard_experiment()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.DeleteTensorboardExperimentRequest()


@pytest.mark.asyncio
async def test_delete_tensorboard_experiment_async(
    transport: str = "grpc_asyncio",
    request_type=tensorboard_service.DeleteTensorboardExperimentRequest,
):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tensorboard_experiment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_tensorboard_experiment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.DeleteTensorboardExperimentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_tensorboard_experiment_async_from_dict():
    await test_delete_tensorboard_experiment_async(request_type=dict)


def test_delete_tensorboard_experiment_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.DeleteTensorboardExperimentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tensorboard_experiment), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_tensorboard_experiment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_tensorboard_experiment_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.DeleteTensorboardExperimentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tensorboard_experiment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_tensorboard_experiment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_delete_tensorboard_experiment_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tensorboard_experiment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_tensorboard_experiment(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_tensorboard_experiment_flattened_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_tensorboard_experiment(
            tensorboard_service.DeleteTensorboardExperimentRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_tensorboard_experiment_flattened_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tensorboard_experiment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_tensorboard_experiment(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_tensorboard_experiment_flattened_error_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_tensorboard_experiment(
            tensorboard_service.DeleteTensorboardExperimentRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.CreateTensorboardRunRequest,
        dict,
    ],
)
def test_create_tensorboard_run(request_type, transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tensorboard_run), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gca_tensorboard_run.TensorboardRun(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            etag="etag_value",
        )
        response = client.create_tensorboard_run(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.CreateTensorboardRunRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gca_tensorboard_run.TensorboardRun)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.etag == "etag_value"


def test_create_tensorboard_run_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tensorboard_run), "__call__"
    ) as call:
        client.create_tensorboard_run()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.CreateTensorboardRunRequest()


@pytest.mark.asyncio
async def test_create_tensorboard_run_async(
    transport: str = "grpc_asyncio",
    request_type=tensorboard_service.CreateTensorboardRunRequest,
):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tensorboard_run), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gca_tensorboard_run.TensorboardRun(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                etag="etag_value",
            )
        )
        response = await client.create_tensorboard_run(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.CreateTensorboardRunRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gca_tensorboard_run.TensorboardRun)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.etag == "etag_value"


@pytest.mark.asyncio
async def test_create_tensorboard_run_async_from_dict():
    await test_create_tensorboard_run_async(request_type=dict)


def test_create_tensorboard_run_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.CreateTensorboardRunRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tensorboard_run), "__call__"
    ) as call:
        call.return_value = gca_tensorboard_run.TensorboardRun()
        client.create_tensorboard_run(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_tensorboard_run_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.CreateTensorboardRunRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tensorboard_run), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gca_tensorboard_run.TensorboardRun()
        )
        await client.create_tensorboard_run(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_tensorboard_run_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tensorboard_run), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gca_tensorboard_run.TensorboardRun()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_tensorboard_run(
            parent="parent_value",
            tensorboard_run=gca_tensorboard_run.TensorboardRun(name="name_value"),
            tensorboard_run_id="tensorboard_run_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].tensorboard_run
        mock_val = gca_tensorboard_run.TensorboardRun(name="name_value")
        assert arg == mock_val
        arg = args[0].tensorboard_run_id
        mock_val = "tensorboard_run_id_value"
        assert arg == mock_val


def test_create_tensorboard_run_flattened_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_tensorboard_run(
            tensorboard_service.CreateTensorboardRunRequest(),
            parent="parent_value",
            tensorboard_run=gca_tensorboard_run.TensorboardRun(name="name_value"),
            tensorboard_run_id="tensorboard_run_id_value",
        )


@pytest.mark.asyncio
async def test_create_tensorboard_run_flattened_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tensorboard_run), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gca_tensorboard_run.TensorboardRun()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gca_tensorboard_run.TensorboardRun()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_tensorboard_run(
            parent="parent_value",
            tensorboard_run=gca_tensorboard_run.TensorboardRun(name="name_value"),
            tensorboard_run_id="tensorboard_run_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].tensorboard_run
        mock_val = gca_tensorboard_run.TensorboardRun(name="name_value")
        assert arg == mock_val
        arg = args[0].tensorboard_run_id
        mock_val = "tensorboard_run_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_tensorboard_run_flattened_error_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_tensorboard_run(
            tensorboard_service.CreateTensorboardRunRequest(),
            parent="parent_value",
            tensorboard_run=gca_tensorboard_run.TensorboardRun(name="name_value"),
            tensorboard_run_id="tensorboard_run_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.BatchCreateTensorboardRunsRequest,
        dict,
    ],
)
def test_batch_create_tensorboard_runs(request_type, transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_tensorboard_runs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_service.BatchCreateTensorboardRunsResponse()
        response = client.batch_create_tensorboard_runs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.BatchCreateTensorboardRunsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tensorboard_service.BatchCreateTensorboardRunsResponse)


def test_batch_create_tensorboard_runs_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_tensorboard_runs), "__call__"
    ) as call:
        client.batch_create_tensorboard_runs()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.BatchCreateTensorboardRunsRequest()


@pytest.mark.asyncio
async def test_batch_create_tensorboard_runs_async(
    transport: str = "grpc_asyncio",
    request_type=tensorboard_service.BatchCreateTensorboardRunsRequest,
):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_tensorboard_runs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.BatchCreateTensorboardRunsResponse()
        )
        response = await client.batch_create_tensorboard_runs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.BatchCreateTensorboardRunsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tensorboard_service.BatchCreateTensorboardRunsResponse)


@pytest.mark.asyncio
async def test_batch_create_tensorboard_runs_async_from_dict():
    await test_batch_create_tensorboard_runs_async(request_type=dict)


def test_batch_create_tensorboard_runs_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.BatchCreateTensorboardRunsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_tensorboard_runs), "__call__"
    ) as call:
        call.return_value = tensorboard_service.BatchCreateTensorboardRunsResponse()
        client.batch_create_tensorboard_runs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_batch_create_tensorboard_runs_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.BatchCreateTensorboardRunsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_tensorboard_runs), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.BatchCreateTensorboardRunsResponse()
        )
        await client.batch_create_tensorboard_runs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_batch_create_tensorboard_runs_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_tensorboard_runs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_service.BatchCreateTensorboardRunsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.batch_create_tensorboard_runs(
            parent="parent_value",
            requests=[
                tensorboard_service.CreateTensorboardRunRequest(parent="parent_value")
            ],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].requests
        mock_val = [
            tensorboard_service.CreateTensorboardRunRequest(parent="parent_value")
        ]
        assert arg == mock_val


def test_batch_create_tensorboard_runs_flattened_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.batch_create_tensorboard_runs(
            tensorboard_service.BatchCreateTensorboardRunsRequest(),
            parent="parent_value",
            requests=[
                tensorboard_service.CreateTensorboardRunRequest(parent="parent_value")
            ],
        )


@pytest.mark.asyncio
async def test_batch_create_tensorboard_runs_flattened_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_tensorboard_runs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_service.BatchCreateTensorboardRunsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.BatchCreateTensorboardRunsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.batch_create_tensorboard_runs(
            parent="parent_value",
            requests=[
                tensorboard_service.CreateTensorboardRunRequest(parent="parent_value")
            ],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].requests
        mock_val = [
            tensorboard_service.CreateTensorboardRunRequest(parent="parent_value")
        ]
        assert arg == mock_val


@pytest.mark.asyncio
async def test_batch_create_tensorboard_runs_flattened_error_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.batch_create_tensorboard_runs(
            tensorboard_service.BatchCreateTensorboardRunsRequest(),
            parent="parent_value",
            requests=[
                tensorboard_service.CreateTensorboardRunRequest(parent="parent_value")
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.GetTensorboardRunRequest,
        dict,
    ],
)
def test_get_tensorboard_run(request_type, transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_tensorboard_run), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_run.TensorboardRun(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            etag="etag_value",
        )
        response = client.get_tensorboard_run(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.GetTensorboardRunRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tensorboard_run.TensorboardRun)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.etag == "etag_value"


def test_get_tensorboard_run_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_tensorboard_run), "__call__"
    ) as call:
        client.get_tensorboard_run()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.GetTensorboardRunRequest()


@pytest.mark.asyncio
async def test_get_tensorboard_run_async(
    transport: str = "grpc_asyncio",
    request_type=tensorboard_service.GetTensorboardRunRequest,
):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_tensorboard_run), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_run.TensorboardRun(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                etag="etag_value",
            )
        )
        response = await client.get_tensorboard_run(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.GetTensorboardRunRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tensorboard_run.TensorboardRun)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.etag == "etag_value"


@pytest.mark.asyncio
async def test_get_tensorboard_run_async_from_dict():
    await test_get_tensorboard_run_async(request_type=dict)


def test_get_tensorboard_run_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.GetTensorboardRunRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_tensorboard_run), "__call__"
    ) as call:
        call.return_value = tensorboard_run.TensorboardRun()
        client.get_tensorboard_run(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_tensorboard_run_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.GetTensorboardRunRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_tensorboard_run), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_run.TensorboardRun()
        )
        await client.get_tensorboard_run(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_tensorboard_run_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_tensorboard_run), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_run.TensorboardRun()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_tensorboard_run(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_tensorboard_run_flattened_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_tensorboard_run(
            tensorboard_service.GetTensorboardRunRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_tensorboard_run_flattened_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_tensorboard_run), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_run.TensorboardRun()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_run.TensorboardRun()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_tensorboard_run(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_tensorboard_run_flattened_error_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_tensorboard_run(
            tensorboard_service.GetTensorboardRunRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.UpdateTensorboardRunRequest,
        dict,
    ],
)
def test_update_tensorboard_run(request_type, transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tensorboard_run), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gca_tensorboard_run.TensorboardRun(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            etag="etag_value",
        )
        response = client.update_tensorboard_run(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.UpdateTensorboardRunRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gca_tensorboard_run.TensorboardRun)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.etag == "etag_value"


def test_update_tensorboard_run_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tensorboard_run), "__call__"
    ) as call:
        client.update_tensorboard_run()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.UpdateTensorboardRunRequest()


@pytest.mark.asyncio
async def test_update_tensorboard_run_async(
    transport: str = "grpc_asyncio",
    request_type=tensorboard_service.UpdateTensorboardRunRequest,
):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tensorboard_run), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gca_tensorboard_run.TensorboardRun(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                etag="etag_value",
            )
        )
        response = await client.update_tensorboard_run(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.UpdateTensorboardRunRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gca_tensorboard_run.TensorboardRun)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.etag == "etag_value"


@pytest.mark.asyncio
async def test_update_tensorboard_run_async_from_dict():
    await test_update_tensorboard_run_async(request_type=dict)


def test_update_tensorboard_run_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.UpdateTensorboardRunRequest()

    request.tensorboard_run.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tensorboard_run), "__call__"
    ) as call:
        call.return_value = gca_tensorboard_run.TensorboardRun()
        client.update_tensorboard_run(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "tensorboard_run.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_tensorboard_run_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.UpdateTensorboardRunRequest()

    request.tensorboard_run.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tensorboard_run), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gca_tensorboard_run.TensorboardRun()
        )
        await client.update_tensorboard_run(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "tensorboard_run.name=name_value",
    ) in kw["metadata"]


def test_update_tensorboard_run_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tensorboard_run), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gca_tensorboard_run.TensorboardRun()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_tensorboard_run(
            tensorboard_run=gca_tensorboard_run.TensorboardRun(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].tensorboard_run
        mock_val = gca_tensorboard_run.TensorboardRun(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_tensorboard_run_flattened_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_tensorboard_run(
            tensorboard_service.UpdateTensorboardRunRequest(),
            tensorboard_run=gca_tensorboard_run.TensorboardRun(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_tensorboard_run_flattened_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tensorboard_run), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gca_tensorboard_run.TensorboardRun()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gca_tensorboard_run.TensorboardRun()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_tensorboard_run(
            tensorboard_run=gca_tensorboard_run.TensorboardRun(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].tensorboard_run
        mock_val = gca_tensorboard_run.TensorboardRun(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_tensorboard_run_flattened_error_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_tensorboard_run(
            tensorboard_service.UpdateTensorboardRunRequest(),
            tensorboard_run=gca_tensorboard_run.TensorboardRun(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.ListTensorboardRunsRequest,
        dict,
    ],
)
def test_list_tensorboard_runs(request_type, transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboard_runs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_service.ListTensorboardRunsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_tensorboard_runs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.ListTensorboardRunsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTensorboardRunsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_tensorboard_runs_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboard_runs), "__call__"
    ) as call:
        client.list_tensorboard_runs()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.ListTensorboardRunsRequest()


@pytest.mark.asyncio
async def test_list_tensorboard_runs_async(
    transport: str = "grpc_asyncio",
    request_type=tensorboard_service.ListTensorboardRunsRequest,
):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboard_runs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.ListTensorboardRunsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_tensorboard_runs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.ListTensorboardRunsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTensorboardRunsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_tensorboard_runs_async_from_dict():
    await test_list_tensorboard_runs_async(request_type=dict)


def test_list_tensorboard_runs_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.ListTensorboardRunsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboard_runs), "__call__"
    ) as call:
        call.return_value = tensorboard_service.ListTensorboardRunsResponse()
        client.list_tensorboard_runs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_tensorboard_runs_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.ListTensorboardRunsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboard_runs), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.ListTensorboardRunsResponse()
        )
        await client.list_tensorboard_runs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_tensorboard_runs_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboard_runs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_service.ListTensorboardRunsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_tensorboard_runs(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_tensorboard_runs_flattened_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_tensorboard_runs(
            tensorboard_service.ListTensorboardRunsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_tensorboard_runs_flattened_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboard_runs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_service.ListTensorboardRunsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.ListTensorboardRunsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_tensorboard_runs(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_tensorboard_runs_flattened_error_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_tensorboard_runs(
            tensorboard_service.ListTensorboardRunsRequest(),
            parent="parent_value",
        )


def test_list_tensorboard_runs_pager(transport_name: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboard_runs), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            tensorboard_service.ListTensorboardRunsResponse(
                tensorboard_runs=[
                    tensorboard_run.TensorboardRun(),
                    tensorboard_run.TensorboardRun(),
                    tensorboard_run.TensorboardRun(),
                ],
                next_page_token="abc",
            ),
            tensorboard_service.ListTensorboardRunsResponse(
                tensorboard_runs=[],
                next_page_token="def",
            ),
            tensorboard_service.ListTensorboardRunsResponse(
                tensorboard_runs=[
                    tensorboard_run.TensorboardRun(),
                ],
                next_page_token="ghi",
            ),
            tensorboard_service.ListTensorboardRunsResponse(
                tensorboard_runs=[
                    tensorboard_run.TensorboardRun(),
                    tensorboard_run.TensorboardRun(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_tensorboard_runs(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, tensorboard_run.TensorboardRun) for i in results)


def test_list_tensorboard_runs_pages(transport_name: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboard_runs), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            tensorboard_service.ListTensorboardRunsResponse(
                tensorboard_runs=[
                    tensorboard_run.TensorboardRun(),
                    tensorboard_run.TensorboardRun(),
                    tensorboard_run.TensorboardRun(),
                ],
                next_page_token="abc",
            ),
            tensorboard_service.ListTensorboardRunsResponse(
                tensorboard_runs=[],
                next_page_token="def",
            ),
            tensorboard_service.ListTensorboardRunsResponse(
                tensorboard_runs=[
                    tensorboard_run.TensorboardRun(),
                ],
                next_page_token="ghi",
            ),
            tensorboard_service.ListTensorboardRunsResponse(
                tensorboard_runs=[
                    tensorboard_run.TensorboardRun(),
                    tensorboard_run.TensorboardRun(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_tensorboard_runs(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_tensorboard_runs_async_pager():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboard_runs),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            tensorboard_service.ListTensorboardRunsResponse(
                tensorboard_runs=[
                    tensorboard_run.TensorboardRun(),
                    tensorboard_run.TensorboardRun(),
                    tensorboard_run.TensorboardRun(),
                ],
                next_page_token="abc",
            ),
            tensorboard_service.ListTensorboardRunsResponse(
                tensorboard_runs=[],
                next_page_token="def",
            ),
            tensorboard_service.ListTensorboardRunsResponse(
                tensorboard_runs=[
                    tensorboard_run.TensorboardRun(),
                ],
                next_page_token="ghi",
            ),
            tensorboard_service.ListTensorboardRunsResponse(
                tensorboard_runs=[
                    tensorboard_run.TensorboardRun(),
                    tensorboard_run.TensorboardRun(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_tensorboard_runs(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, tensorboard_run.TensorboardRun) for i in responses)


@pytest.mark.asyncio
async def test_list_tensorboard_runs_async_pages():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboard_runs),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            tensorboard_service.ListTensorboardRunsResponse(
                tensorboard_runs=[
                    tensorboard_run.TensorboardRun(),
                    tensorboard_run.TensorboardRun(),
                    tensorboard_run.TensorboardRun(),
                ],
                next_page_token="abc",
            ),
            tensorboard_service.ListTensorboardRunsResponse(
                tensorboard_runs=[],
                next_page_token="def",
            ),
            tensorboard_service.ListTensorboardRunsResponse(
                tensorboard_runs=[
                    tensorboard_run.TensorboardRun(),
                ],
                next_page_token="ghi",
            ),
            tensorboard_service.ListTensorboardRunsResponse(
                tensorboard_runs=[
                    tensorboard_run.TensorboardRun(),
                    tensorboard_run.TensorboardRun(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_tensorboard_runs(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.DeleteTensorboardRunRequest,
        dict,
    ],
)
def test_delete_tensorboard_run(request_type, transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tensorboard_run), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_tensorboard_run(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.DeleteTensorboardRunRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_tensorboard_run_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tensorboard_run), "__call__"
    ) as call:
        client.delete_tensorboard_run()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.DeleteTensorboardRunRequest()


@pytest.mark.asyncio
async def test_delete_tensorboard_run_async(
    transport: str = "grpc_asyncio",
    request_type=tensorboard_service.DeleteTensorboardRunRequest,
):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tensorboard_run), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_tensorboard_run(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.DeleteTensorboardRunRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_tensorboard_run_async_from_dict():
    await test_delete_tensorboard_run_async(request_type=dict)


def test_delete_tensorboard_run_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.DeleteTensorboardRunRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tensorboard_run), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_tensorboard_run(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_tensorboard_run_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.DeleteTensorboardRunRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tensorboard_run), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_tensorboard_run(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_delete_tensorboard_run_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tensorboard_run), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_tensorboard_run(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_tensorboard_run_flattened_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_tensorboard_run(
            tensorboard_service.DeleteTensorboardRunRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_tensorboard_run_flattened_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tensorboard_run), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_tensorboard_run(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_tensorboard_run_flattened_error_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_tensorboard_run(
            tensorboard_service.DeleteTensorboardRunRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.BatchCreateTensorboardTimeSeriesRequest,
        dict,
    ],
)
def test_batch_create_tensorboard_time_series(request_type, transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_tensorboard_time_series), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            tensorboard_service.BatchCreateTensorboardTimeSeriesResponse()
        )
        response = client.batch_create_tensorboard_time_series(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.BatchCreateTensorboardTimeSeriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, tensorboard_service.BatchCreateTensorboardTimeSeriesResponse
    )


def test_batch_create_tensorboard_time_series_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_tensorboard_time_series), "__call__"
    ) as call:
        client.batch_create_tensorboard_time_series()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.BatchCreateTensorboardTimeSeriesRequest()


@pytest.mark.asyncio
async def test_batch_create_tensorboard_time_series_async(
    transport: str = "grpc_asyncio",
    request_type=tensorboard_service.BatchCreateTensorboardTimeSeriesRequest,
):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_tensorboard_time_series), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.BatchCreateTensorboardTimeSeriesResponse()
        )
        response = await client.batch_create_tensorboard_time_series(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.BatchCreateTensorboardTimeSeriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, tensorboard_service.BatchCreateTensorboardTimeSeriesResponse
    )


@pytest.mark.asyncio
async def test_batch_create_tensorboard_time_series_async_from_dict():
    await test_batch_create_tensorboard_time_series_async(request_type=dict)


def test_batch_create_tensorboard_time_series_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.BatchCreateTensorboardTimeSeriesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_tensorboard_time_series), "__call__"
    ) as call:
        call.return_value = (
            tensorboard_service.BatchCreateTensorboardTimeSeriesResponse()
        )
        client.batch_create_tensorboard_time_series(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_batch_create_tensorboard_time_series_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.BatchCreateTensorboardTimeSeriesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_tensorboard_time_series), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.BatchCreateTensorboardTimeSeriesResponse()
        )
        await client.batch_create_tensorboard_time_series(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_batch_create_tensorboard_time_series_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_tensorboard_time_series), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            tensorboard_service.BatchCreateTensorboardTimeSeriesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.batch_create_tensorboard_time_series(
            parent="parent_value",
            requests=[
                tensorboard_service.CreateTensorboardTimeSeriesRequest(
                    parent="parent_value"
                )
            ],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].requests
        mock_val = [
            tensorboard_service.CreateTensorboardTimeSeriesRequest(
                parent="parent_value"
            )
        ]
        assert arg == mock_val


def test_batch_create_tensorboard_time_series_flattened_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.batch_create_tensorboard_time_series(
            tensorboard_service.BatchCreateTensorboardTimeSeriesRequest(),
            parent="parent_value",
            requests=[
                tensorboard_service.CreateTensorboardTimeSeriesRequest(
                    parent="parent_value"
                )
            ],
        )


@pytest.mark.asyncio
async def test_batch_create_tensorboard_time_series_flattened_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_tensorboard_time_series), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            tensorboard_service.BatchCreateTensorboardTimeSeriesResponse()
        )

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.BatchCreateTensorboardTimeSeriesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.batch_create_tensorboard_time_series(
            parent="parent_value",
            requests=[
                tensorboard_service.CreateTensorboardTimeSeriesRequest(
                    parent="parent_value"
                )
            ],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].requests
        mock_val = [
            tensorboard_service.CreateTensorboardTimeSeriesRequest(
                parent="parent_value"
            )
        ]
        assert arg == mock_val


@pytest.mark.asyncio
async def test_batch_create_tensorboard_time_series_flattened_error_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.batch_create_tensorboard_time_series(
            tensorboard_service.BatchCreateTensorboardTimeSeriesRequest(),
            parent="parent_value",
            requests=[
                tensorboard_service.CreateTensorboardTimeSeriesRequest(
                    parent="parent_value"
                )
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.CreateTensorboardTimeSeriesRequest,
        dict,
    ],
)
def test_create_tensorboard_time_series(request_type, transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tensorboard_time_series), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gca_tensorboard_time_series.TensorboardTimeSeries(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            value_type=gca_tensorboard_time_series.TensorboardTimeSeries.ValueType.SCALAR,
            etag="etag_value",
            plugin_name="plugin_name_value",
            plugin_data=b"plugin_data_blob",
        )
        response = client.create_tensorboard_time_series(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.CreateTensorboardTimeSeriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gca_tensorboard_time_series.TensorboardTimeSeries)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert (
        response.value_type
        == gca_tensorboard_time_series.TensorboardTimeSeries.ValueType.SCALAR
    )
    assert response.etag == "etag_value"
    assert response.plugin_name == "plugin_name_value"
    assert response.plugin_data == b"plugin_data_blob"


def test_create_tensorboard_time_series_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tensorboard_time_series), "__call__"
    ) as call:
        client.create_tensorboard_time_series()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.CreateTensorboardTimeSeriesRequest()


@pytest.mark.asyncio
async def test_create_tensorboard_time_series_async(
    transport: str = "grpc_asyncio",
    request_type=tensorboard_service.CreateTensorboardTimeSeriesRequest,
):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tensorboard_time_series), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gca_tensorboard_time_series.TensorboardTimeSeries(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                value_type=gca_tensorboard_time_series.TensorboardTimeSeries.ValueType.SCALAR,
                etag="etag_value",
                plugin_name="plugin_name_value",
                plugin_data=b"plugin_data_blob",
            )
        )
        response = await client.create_tensorboard_time_series(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.CreateTensorboardTimeSeriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gca_tensorboard_time_series.TensorboardTimeSeries)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert (
        response.value_type
        == gca_tensorboard_time_series.TensorboardTimeSeries.ValueType.SCALAR
    )
    assert response.etag == "etag_value"
    assert response.plugin_name == "plugin_name_value"
    assert response.plugin_data == b"plugin_data_blob"


@pytest.mark.asyncio
async def test_create_tensorboard_time_series_async_from_dict():
    await test_create_tensorboard_time_series_async(request_type=dict)


def test_create_tensorboard_time_series_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.CreateTensorboardTimeSeriesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tensorboard_time_series), "__call__"
    ) as call:
        call.return_value = gca_tensorboard_time_series.TensorboardTimeSeries()
        client.create_tensorboard_time_series(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_tensorboard_time_series_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.CreateTensorboardTimeSeriesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tensorboard_time_series), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gca_tensorboard_time_series.TensorboardTimeSeries()
        )
        await client.create_tensorboard_time_series(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_tensorboard_time_series_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tensorboard_time_series), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gca_tensorboard_time_series.TensorboardTimeSeries()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_tensorboard_time_series(
            parent="parent_value",
            tensorboard_time_series=gca_tensorboard_time_series.TensorboardTimeSeries(
                name="name_value"
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].tensorboard_time_series
        mock_val = gca_tensorboard_time_series.TensorboardTimeSeries(name="name_value")
        assert arg == mock_val


def test_create_tensorboard_time_series_flattened_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_tensorboard_time_series(
            tensorboard_service.CreateTensorboardTimeSeriesRequest(),
            parent="parent_value",
            tensorboard_time_series=gca_tensorboard_time_series.TensorboardTimeSeries(
                name="name_value"
            ),
        )


@pytest.mark.asyncio
async def test_create_tensorboard_time_series_flattened_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tensorboard_time_series), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gca_tensorboard_time_series.TensorboardTimeSeries()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gca_tensorboard_time_series.TensorboardTimeSeries()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_tensorboard_time_series(
            parent="parent_value",
            tensorboard_time_series=gca_tensorboard_time_series.TensorboardTimeSeries(
                name="name_value"
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].tensorboard_time_series
        mock_val = gca_tensorboard_time_series.TensorboardTimeSeries(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_tensorboard_time_series_flattened_error_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_tensorboard_time_series(
            tensorboard_service.CreateTensorboardTimeSeriesRequest(),
            parent="parent_value",
            tensorboard_time_series=gca_tensorboard_time_series.TensorboardTimeSeries(
                name="name_value"
            ),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.GetTensorboardTimeSeriesRequest,
        dict,
    ],
)
def test_get_tensorboard_time_series(request_type, transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_tensorboard_time_series), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_time_series.TensorboardTimeSeries(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            value_type=tensorboard_time_series.TensorboardTimeSeries.ValueType.SCALAR,
            etag="etag_value",
            plugin_name="plugin_name_value",
            plugin_data=b"plugin_data_blob",
        )
        response = client.get_tensorboard_time_series(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.GetTensorboardTimeSeriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tensorboard_time_series.TensorboardTimeSeries)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert (
        response.value_type
        == tensorboard_time_series.TensorboardTimeSeries.ValueType.SCALAR
    )
    assert response.etag == "etag_value"
    assert response.plugin_name == "plugin_name_value"
    assert response.plugin_data == b"plugin_data_blob"


def test_get_tensorboard_time_series_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_tensorboard_time_series), "__call__"
    ) as call:
        client.get_tensorboard_time_series()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.GetTensorboardTimeSeriesRequest()


@pytest.mark.asyncio
async def test_get_tensorboard_time_series_async(
    transport: str = "grpc_asyncio",
    request_type=tensorboard_service.GetTensorboardTimeSeriesRequest,
):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_tensorboard_time_series), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_time_series.TensorboardTimeSeries(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                value_type=tensorboard_time_series.TensorboardTimeSeries.ValueType.SCALAR,
                etag="etag_value",
                plugin_name="plugin_name_value",
                plugin_data=b"plugin_data_blob",
            )
        )
        response = await client.get_tensorboard_time_series(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.GetTensorboardTimeSeriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tensorboard_time_series.TensorboardTimeSeries)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert (
        response.value_type
        == tensorboard_time_series.TensorboardTimeSeries.ValueType.SCALAR
    )
    assert response.etag == "etag_value"
    assert response.plugin_name == "plugin_name_value"
    assert response.plugin_data == b"plugin_data_blob"


@pytest.mark.asyncio
async def test_get_tensorboard_time_series_async_from_dict():
    await test_get_tensorboard_time_series_async(request_type=dict)


def test_get_tensorboard_time_series_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.GetTensorboardTimeSeriesRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_tensorboard_time_series), "__call__"
    ) as call:
        call.return_value = tensorboard_time_series.TensorboardTimeSeries()
        client.get_tensorboard_time_series(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_tensorboard_time_series_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.GetTensorboardTimeSeriesRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_tensorboard_time_series), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_time_series.TensorboardTimeSeries()
        )
        await client.get_tensorboard_time_series(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_tensorboard_time_series_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_tensorboard_time_series), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_time_series.TensorboardTimeSeries()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_tensorboard_time_series(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_tensorboard_time_series_flattened_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_tensorboard_time_series(
            tensorboard_service.GetTensorboardTimeSeriesRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_tensorboard_time_series_flattened_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_tensorboard_time_series), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_time_series.TensorboardTimeSeries()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_time_series.TensorboardTimeSeries()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_tensorboard_time_series(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_tensorboard_time_series_flattened_error_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_tensorboard_time_series(
            tensorboard_service.GetTensorboardTimeSeriesRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.UpdateTensorboardTimeSeriesRequest,
        dict,
    ],
)
def test_update_tensorboard_time_series(request_type, transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tensorboard_time_series), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gca_tensorboard_time_series.TensorboardTimeSeries(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            value_type=gca_tensorboard_time_series.TensorboardTimeSeries.ValueType.SCALAR,
            etag="etag_value",
            plugin_name="plugin_name_value",
            plugin_data=b"plugin_data_blob",
        )
        response = client.update_tensorboard_time_series(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.UpdateTensorboardTimeSeriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gca_tensorboard_time_series.TensorboardTimeSeries)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert (
        response.value_type
        == gca_tensorboard_time_series.TensorboardTimeSeries.ValueType.SCALAR
    )
    assert response.etag == "etag_value"
    assert response.plugin_name == "plugin_name_value"
    assert response.plugin_data == b"plugin_data_blob"


def test_update_tensorboard_time_series_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tensorboard_time_series), "__call__"
    ) as call:
        client.update_tensorboard_time_series()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.UpdateTensorboardTimeSeriesRequest()


@pytest.mark.asyncio
async def test_update_tensorboard_time_series_async(
    transport: str = "grpc_asyncio",
    request_type=tensorboard_service.UpdateTensorboardTimeSeriesRequest,
):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tensorboard_time_series), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gca_tensorboard_time_series.TensorboardTimeSeries(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                value_type=gca_tensorboard_time_series.TensorboardTimeSeries.ValueType.SCALAR,
                etag="etag_value",
                plugin_name="plugin_name_value",
                plugin_data=b"plugin_data_blob",
            )
        )
        response = await client.update_tensorboard_time_series(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.UpdateTensorboardTimeSeriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gca_tensorboard_time_series.TensorboardTimeSeries)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert (
        response.value_type
        == gca_tensorboard_time_series.TensorboardTimeSeries.ValueType.SCALAR
    )
    assert response.etag == "etag_value"
    assert response.plugin_name == "plugin_name_value"
    assert response.plugin_data == b"plugin_data_blob"


@pytest.mark.asyncio
async def test_update_tensorboard_time_series_async_from_dict():
    await test_update_tensorboard_time_series_async(request_type=dict)


def test_update_tensorboard_time_series_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.UpdateTensorboardTimeSeriesRequest()

    request.tensorboard_time_series.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tensorboard_time_series), "__call__"
    ) as call:
        call.return_value = gca_tensorboard_time_series.TensorboardTimeSeries()
        client.update_tensorboard_time_series(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "tensorboard_time_series.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_tensorboard_time_series_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.UpdateTensorboardTimeSeriesRequest()

    request.tensorboard_time_series.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tensorboard_time_series), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gca_tensorboard_time_series.TensorboardTimeSeries()
        )
        await client.update_tensorboard_time_series(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "tensorboard_time_series.name=name_value",
    ) in kw["metadata"]


def test_update_tensorboard_time_series_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tensorboard_time_series), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gca_tensorboard_time_series.TensorboardTimeSeries()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_tensorboard_time_series(
            tensorboard_time_series=gca_tensorboard_time_series.TensorboardTimeSeries(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].tensorboard_time_series
        mock_val = gca_tensorboard_time_series.TensorboardTimeSeries(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_tensorboard_time_series_flattened_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_tensorboard_time_series(
            tensorboard_service.UpdateTensorboardTimeSeriesRequest(),
            tensorboard_time_series=gca_tensorboard_time_series.TensorboardTimeSeries(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_tensorboard_time_series_flattened_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tensorboard_time_series), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gca_tensorboard_time_series.TensorboardTimeSeries()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gca_tensorboard_time_series.TensorboardTimeSeries()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_tensorboard_time_series(
            tensorboard_time_series=gca_tensorboard_time_series.TensorboardTimeSeries(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].tensorboard_time_series
        mock_val = gca_tensorboard_time_series.TensorboardTimeSeries(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_tensorboard_time_series_flattened_error_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_tensorboard_time_series(
            tensorboard_service.UpdateTensorboardTimeSeriesRequest(),
            tensorboard_time_series=gca_tensorboard_time_series.TensorboardTimeSeries(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.ListTensorboardTimeSeriesRequest,
        dict,
    ],
)
def test_list_tensorboard_time_series(request_type, transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboard_time_series), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_service.ListTensorboardTimeSeriesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_tensorboard_time_series(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.ListTensorboardTimeSeriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTensorboardTimeSeriesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_tensorboard_time_series_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboard_time_series), "__call__"
    ) as call:
        client.list_tensorboard_time_series()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.ListTensorboardTimeSeriesRequest()


@pytest.mark.asyncio
async def test_list_tensorboard_time_series_async(
    transport: str = "grpc_asyncio",
    request_type=tensorboard_service.ListTensorboardTimeSeriesRequest,
):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboard_time_series), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.ListTensorboardTimeSeriesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_tensorboard_time_series(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.ListTensorboardTimeSeriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTensorboardTimeSeriesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_tensorboard_time_series_async_from_dict():
    await test_list_tensorboard_time_series_async(request_type=dict)


def test_list_tensorboard_time_series_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.ListTensorboardTimeSeriesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboard_time_series), "__call__"
    ) as call:
        call.return_value = tensorboard_service.ListTensorboardTimeSeriesResponse()
        client.list_tensorboard_time_series(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_tensorboard_time_series_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.ListTensorboardTimeSeriesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboard_time_series), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.ListTensorboardTimeSeriesResponse()
        )
        await client.list_tensorboard_time_series(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_tensorboard_time_series_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboard_time_series), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_service.ListTensorboardTimeSeriesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_tensorboard_time_series(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_tensorboard_time_series_flattened_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_tensorboard_time_series(
            tensorboard_service.ListTensorboardTimeSeriesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_tensorboard_time_series_flattened_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboard_time_series), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_service.ListTensorboardTimeSeriesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.ListTensorboardTimeSeriesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_tensorboard_time_series(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_tensorboard_time_series_flattened_error_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_tensorboard_time_series(
            tensorboard_service.ListTensorboardTimeSeriesRequest(),
            parent="parent_value",
        )


def test_list_tensorboard_time_series_pager(transport_name: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboard_time_series), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            tensorboard_service.ListTensorboardTimeSeriesResponse(
                tensorboard_time_series=[
                    tensorboard_time_series.TensorboardTimeSeries(),
                    tensorboard_time_series.TensorboardTimeSeries(),
                    tensorboard_time_series.TensorboardTimeSeries(),
                ],
                next_page_token="abc",
            ),
            tensorboard_service.ListTensorboardTimeSeriesResponse(
                tensorboard_time_series=[],
                next_page_token="def",
            ),
            tensorboard_service.ListTensorboardTimeSeriesResponse(
                tensorboard_time_series=[
                    tensorboard_time_series.TensorboardTimeSeries(),
                ],
                next_page_token="ghi",
            ),
            tensorboard_service.ListTensorboardTimeSeriesResponse(
                tensorboard_time_series=[
                    tensorboard_time_series.TensorboardTimeSeries(),
                    tensorboard_time_series.TensorboardTimeSeries(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_tensorboard_time_series(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, tensorboard_time_series.TensorboardTimeSeries)
            for i in results
        )


def test_list_tensorboard_time_series_pages(transport_name: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboard_time_series), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            tensorboard_service.ListTensorboardTimeSeriesResponse(
                tensorboard_time_series=[
                    tensorboard_time_series.TensorboardTimeSeries(),
                    tensorboard_time_series.TensorboardTimeSeries(),
                    tensorboard_time_series.TensorboardTimeSeries(),
                ],
                next_page_token="abc",
            ),
            tensorboard_service.ListTensorboardTimeSeriesResponse(
                tensorboard_time_series=[],
                next_page_token="def",
            ),
            tensorboard_service.ListTensorboardTimeSeriesResponse(
                tensorboard_time_series=[
                    tensorboard_time_series.TensorboardTimeSeries(),
                ],
                next_page_token="ghi",
            ),
            tensorboard_service.ListTensorboardTimeSeriesResponse(
                tensorboard_time_series=[
                    tensorboard_time_series.TensorboardTimeSeries(),
                    tensorboard_time_series.TensorboardTimeSeries(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_tensorboard_time_series(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_tensorboard_time_series_async_pager():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboard_time_series),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            tensorboard_service.ListTensorboardTimeSeriesResponse(
                tensorboard_time_series=[
                    tensorboard_time_series.TensorboardTimeSeries(),
                    tensorboard_time_series.TensorboardTimeSeries(),
                    tensorboard_time_series.TensorboardTimeSeries(),
                ],
                next_page_token="abc",
            ),
            tensorboard_service.ListTensorboardTimeSeriesResponse(
                tensorboard_time_series=[],
                next_page_token="def",
            ),
            tensorboard_service.ListTensorboardTimeSeriesResponse(
                tensorboard_time_series=[
                    tensorboard_time_series.TensorboardTimeSeries(),
                ],
                next_page_token="ghi",
            ),
            tensorboard_service.ListTensorboardTimeSeriesResponse(
                tensorboard_time_series=[
                    tensorboard_time_series.TensorboardTimeSeries(),
                    tensorboard_time_series.TensorboardTimeSeries(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_tensorboard_time_series(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, tensorboard_time_series.TensorboardTimeSeries)
            for i in responses
        )


@pytest.mark.asyncio
async def test_list_tensorboard_time_series_async_pages():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensorboard_time_series),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            tensorboard_service.ListTensorboardTimeSeriesResponse(
                tensorboard_time_series=[
                    tensorboard_time_series.TensorboardTimeSeries(),
                    tensorboard_time_series.TensorboardTimeSeries(),
                    tensorboard_time_series.TensorboardTimeSeries(),
                ],
                next_page_token="abc",
            ),
            tensorboard_service.ListTensorboardTimeSeriesResponse(
                tensorboard_time_series=[],
                next_page_token="def",
            ),
            tensorboard_service.ListTensorboardTimeSeriesResponse(
                tensorboard_time_series=[
                    tensorboard_time_series.TensorboardTimeSeries(),
                ],
                next_page_token="ghi",
            ),
            tensorboard_service.ListTensorboardTimeSeriesResponse(
                tensorboard_time_series=[
                    tensorboard_time_series.TensorboardTimeSeries(),
                    tensorboard_time_series.TensorboardTimeSeries(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_tensorboard_time_series(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.DeleteTensorboardTimeSeriesRequest,
        dict,
    ],
)
def test_delete_tensorboard_time_series(request_type, transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tensorboard_time_series), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_tensorboard_time_series(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.DeleteTensorboardTimeSeriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_tensorboard_time_series_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tensorboard_time_series), "__call__"
    ) as call:
        client.delete_tensorboard_time_series()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.DeleteTensorboardTimeSeriesRequest()


@pytest.mark.asyncio
async def test_delete_tensorboard_time_series_async(
    transport: str = "grpc_asyncio",
    request_type=tensorboard_service.DeleteTensorboardTimeSeriesRequest,
):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tensorboard_time_series), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_tensorboard_time_series(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.DeleteTensorboardTimeSeriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_tensorboard_time_series_async_from_dict():
    await test_delete_tensorboard_time_series_async(request_type=dict)


def test_delete_tensorboard_time_series_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.DeleteTensorboardTimeSeriesRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tensorboard_time_series), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_tensorboard_time_series(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_tensorboard_time_series_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.DeleteTensorboardTimeSeriesRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tensorboard_time_series), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_tensorboard_time_series(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_delete_tensorboard_time_series_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tensorboard_time_series), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_tensorboard_time_series(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_tensorboard_time_series_flattened_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_tensorboard_time_series(
            tensorboard_service.DeleteTensorboardTimeSeriesRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_tensorboard_time_series_flattened_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tensorboard_time_series), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_tensorboard_time_series(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_tensorboard_time_series_flattened_error_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_tensorboard_time_series(
            tensorboard_service.DeleteTensorboardTimeSeriesRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.BatchReadTensorboardTimeSeriesDataRequest,
        dict,
    ],
)
def test_batch_read_tensorboard_time_series_data(request_type, transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_read_tensorboard_time_series_data), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            tensorboard_service.BatchReadTensorboardTimeSeriesDataResponse()
        )
        response = client.batch_read_tensorboard_time_series_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert (
            args[0] == tensorboard_service.BatchReadTensorboardTimeSeriesDataRequest()
        )

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, tensorboard_service.BatchReadTensorboardTimeSeriesDataResponse
    )


def test_batch_read_tensorboard_time_series_data_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_read_tensorboard_time_series_data), "__call__"
    ) as call:
        client.batch_read_tensorboard_time_series_data()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0] == tensorboard_service.BatchReadTensorboardTimeSeriesDataRequest()
        )


@pytest.mark.asyncio
async def test_batch_read_tensorboard_time_series_data_async(
    transport: str = "grpc_asyncio",
    request_type=tensorboard_service.BatchReadTensorboardTimeSeriesDataRequest,
):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_read_tensorboard_time_series_data), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.BatchReadTensorboardTimeSeriesDataResponse()
        )
        response = await client.batch_read_tensorboard_time_series_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert (
            args[0] == tensorboard_service.BatchReadTensorboardTimeSeriesDataRequest()
        )

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, tensorboard_service.BatchReadTensorboardTimeSeriesDataResponse
    )


@pytest.mark.asyncio
async def test_batch_read_tensorboard_time_series_data_async_from_dict():
    await test_batch_read_tensorboard_time_series_data_async(request_type=dict)


def test_batch_read_tensorboard_time_series_data_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.BatchReadTensorboardTimeSeriesDataRequest()

    request.tensorboard = "tensorboard_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_read_tensorboard_time_series_data), "__call__"
    ) as call:
        call.return_value = (
            tensorboard_service.BatchReadTensorboardTimeSeriesDataResponse()
        )
        client.batch_read_tensorboard_time_series_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "tensorboard=tensorboard_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_batch_read_tensorboard_time_series_data_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.BatchReadTensorboardTimeSeriesDataRequest()

    request.tensorboard = "tensorboard_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_read_tensorboard_time_series_data), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.BatchReadTensorboardTimeSeriesDataResponse()
        )
        await client.batch_read_tensorboard_time_series_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "tensorboard=tensorboard_value",
    ) in kw["metadata"]


def test_batch_read_tensorboard_time_series_data_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_read_tensorboard_time_series_data), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            tensorboard_service.BatchReadTensorboardTimeSeriesDataResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.batch_read_tensorboard_time_series_data(
            tensorboard="tensorboard_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].tensorboard
        mock_val = "tensorboard_value"
        assert arg == mock_val


def test_batch_read_tensorboard_time_series_data_flattened_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.batch_read_tensorboard_time_series_data(
            tensorboard_service.BatchReadTensorboardTimeSeriesDataRequest(),
            tensorboard="tensorboard_value",
        )


@pytest.mark.asyncio
async def test_batch_read_tensorboard_time_series_data_flattened_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_read_tensorboard_time_series_data), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            tensorboard_service.BatchReadTensorboardTimeSeriesDataResponse()
        )

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.BatchReadTensorboardTimeSeriesDataResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.batch_read_tensorboard_time_series_data(
            tensorboard="tensorboard_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].tensorboard
        mock_val = "tensorboard_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_batch_read_tensorboard_time_series_data_flattened_error_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.batch_read_tensorboard_time_series_data(
            tensorboard_service.BatchReadTensorboardTimeSeriesDataRequest(),
            tensorboard="tensorboard_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.ReadTensorboardTimeSeriesDataRequest,
        dict,
    ],
)
def test_read_tensorboard_time_series_data(request_type, transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.read_tensorboard_time_series_data), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_service.ReadTensorboardTimeSeriesDataResponse()
        response = client.read_tensorboard_time_series_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.ReadTensorboardTimeSeriesDataRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, tensorboard_service.ReadTensorboardTimeSeriesDataResponse
    )


def test_read_tensorboard_time_series_data_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.read_tensorboard_time_series_data), "__call__"
    ) as call:
        client.read_tensorboard_time_series_data()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.ReadTensorboardTimeSeriesDataRequest()


@pytest.mark.asyncio
async def test_read_tensorboard_time_series_data_async(
    transport: str = "grpc_asyncio",
    request_type=tensorboard_service.ReadTensorboardTimeSeriesDataRequest,
):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.read_tensorboard_time_series_data), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.ReadTensorboardTimeSeriesDataResponse()
        )
        response = await client.read_tensorboard_time_series_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.ReadTensorboardTimeSeriesDataRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, tensorboard_service.ReadTensorboardTimeSeriesDataResponse
    )


@pytest.mark.asyncio
async def test_read_tensorboard_time_series_data_async_from_dict():
    await test_read_tensorboard_time_series_data_async(request_type=dict)


def test_read_tensorboard_time_series_data_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.ReadTensorboardTimeSeriesDataRequest()

    request.tensorboard_time_series = "tensorboard_time_series_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.read_tensorboard_time_series_data), "__call__"
    ) as call:
        call.return_value = tensorboard_service.ReadTensorboardTimeSeriesDataResponse()
        client.read_tensorboard_time_series_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "tensorboard_time_series=tensorboard_time_series_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_read_tensorboard_time_series_data_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.ReadTensorboardTimeSeriesDataRequest()

    request.tensorboard_time_series = "tensorboard_time_series_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.read_tensorboard_time_series_data), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.ReadTensorboardTimeSeriesDataResponse()
        )
        await client.read_tensorboard_time_series_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "tensorboard_time_series=tensorboard_time_series_value",
    ) in kw["metadata"]


def test_read_tensorboard_time_series_data_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.read_tensorboard_time_series_data), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_service.ReadTensorboardTimeSeriesDataResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.read_tensorboard_time_series_data(
            tensorboard_time_series="tensorboard_time_series_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].tensorboard_time_series
        mock_val = "tensorboard_time_series_value"
        assert arg == mock_val


def test_read_tensorboard_time_series_data_flattened_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.read_tensorboard_time_series_data(
            tensorboard_service.ReadTensorboardTimeSeriesDataRequest(),
            tensorboard_time_series="tensorboard_time_series_value",
        )


@pytest.mark.asyncio
async def test_read_tensorboard_time_series_data_flattened_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.read_tensorboard_time_series_data), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_service.ReadTensorboardTimeSeriesDataResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.ReadTensorboardTimeSeriesDataResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.read_tensorboard_time_series_data(
            tensorboard_time_series="tensorboard_time_series_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].tensorboard_time_series
        mock_val = "tensorboard_time_series_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_read_tensorboard_time_series_data_flattened_error_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.read_tensorboard_time_series_data(
            tensorboard_service.ReadTensorboardTimeSeriesDataRequest(),
            tensorboard_time_series="tensorboard_time_series_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.ReadTensorboardBlobDataRequest,
        dict,
    ],
)
def test_read_tensorboard_blob_data(request_type, transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.read_tensorboard_blob_data), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter(
            [tensorboard_service.ReadTensorboardBlobDataResponse()]
        )
        response = client.read_tensorboard_blob_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.ReadTensorboardBlobDataRequest()

    # Establish that the response is the type that we expect.
    for message in response:
        assert isinstance(message, tensorboard_service.ReadTensorboardBlobDataResponse)


def test_read_tensorboard_blob_data_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.read_tensorboard_blob_data), "__call__"
    ) as call:
        client.read_tensorboard_blob_data()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.ReadTensorboardBlobDataRequest()


@pytest.mark.asyncio
async def test_read_tensorboard_blob_data_async(
    transport: str = "grpc_asyncio",
    request_type=tensorboard_service.ReadTensorboardBlobDataRequest,
):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.read_tensorboard_blob_data), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = mock.Mock(aio.UnaryStreamCall, autospec=True)
        call.return_value.read = mock.AsyncMock(
            side_effect=[tensorboard_service.ReadTensorboardBlobDataResponse()]
        )
        response = await client.read_tensorboard_blob_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.ReadTensorboardBlobDataRequest()

    # Establish that the response is the type that we expect.
    message = await response.read()
    assert isinstance(message, tensorboard_service.ReadTensorboardBlobDataResponse)


@pytest.mark.asyncio
async def test_read_tensorboard_blob_data_async_from_dict():
    await test_read_tensorboard_blob_data_async(request_type=dict)


def test_read_tensorboard_blob_data_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.ReadTensorboardBlobDataRequest()

    request.time_series = "time_series_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.read_tensorboard_blob_data), "__call__"
    ) as call:
        call.return_value = iter(
            [tensorboard_service.ReadTensorboardBlobDataResponse()]
        )
        client.read_tensorboard_blob_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "time_series=time_series_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_read_tensorboard_blob_data_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.ReadTensorboardBlobDataRequest()

    request.time_series = "time_series_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.read_tensorboard_blob_data), "__call__"
    ) as call:
        call.return_value = mock.Mock(aio.UnaryStreamCall, autospec=True)
        call.return_value.read = mock.AsyncMock(
            side_effect=[tensorboard_service.ReadTensorboardBlobDataResponse()]
        )
        await client.read_tensorboard_blob_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "time_series=time_series_value",
    ) in kw["metadata"]


def test_read_tensorboard_blob_data_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.read_tensorboard_blob_data), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter(
            [tensorboard_service.ReadTensorboardBlobDataResponse()]
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.read_tensorboard_blob_data(
            time_series="time_series_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].time_series
        mock_val = "time_series_value"
        assert arg == mock_val


def test_read_tensorboard_blob_data_flattened_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.read_tensorboard_blob_data(
            tensorboard_service.ReadTensorboardBlobDataRequest(),
            time_series="time_series_value",
        )


@pytest.mark.asyncio
async def test_read_tensorboard_blob_data_flattened_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.read_tensorboard_blob_data), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter(
            [tensorboard_service.ReadTensorboardBlobDataResponse()]
        )

        call.return_value = mock.Mock(aio.UnaryStreamCall, autospec=True)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.read_tensorboard_blob_data(
            time_series="time_series_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].time_series
        mock_val = "time_series_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_read_tensorboard_blob_data_flattened_error_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.read_tensorboard_blob_data(
            tensorboard_service.ReadTensorboardBlobDataRequest(),
            time_series="time_series_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.WriteTensorboardExperimentDataRequest,
        dict,
    ],
)
def test_write_tensorboard_experiment_data(request_type, transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.write_tensorboard_experiment_data), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_service.WriteTensorboardExperimentDataResponse()
        response = client.write_tensorboard_experiment_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.WriteTensorboardExperimentDataRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, tensorboard_service.WriteTensorboardExperimentDataResponse
    )


def test_write_tensorboard_experiment_data_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.write_tensorboard_experiment_data), "__call__"
    ) as call:
        client.write_tensorboard_experiment_data()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.WriteTensorboardExperimentDataRequest()


@pytest.mark.asyncio
async def test_write_tensorboard_experiment_data_async(
    transport: str = "grpc_asyncio",
    request_type=tensorboard_service.WriteTensorboardExperimentDataRequest,
):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.write_tensorboard_experiment_data), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.WriteTensorboardExperimentDataResponse()
        )
        response = await client.write_tensorboard_experiment_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.WriteTensorboardExperimentDataRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, tensorboard_service.WriteTensorboardExperimentDataResponse
    )


@pytest.mark.asyncio
async def test_write_tensorboard_experiment_data_async_from_dict():
    await test_write_tensorboard_experiment_data_async(request_type=dict)


def test_write_tensorboard_experiment_data_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.WriteTensorboardExperimentDataRequest()

    request.tensorboard_experiment = "tensorboard_experiment_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.write_tensorboard_experiment_data), "__call__"
    ) as call:
        call.return_value = tensorboard_service.WriteTensorboardExperimentDataResponse()
        client.write_tensorboard_experiment_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "tensorboard_experiment=tensorboard_experiment_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_write_tensorboard_experiment_data_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.WriteTensorboardExperimentDataRequest()

    request.tensorboard_experiment = "tensorboard_experiment_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.write_tensorboard_experiment_data), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.WriteTensorboardExperimentDataResponse()
        )
        await client.write_tensorboard_experiment_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "tensorboard_experiment=tensorboard_experiment_value",
    ) in kw["metadata"]


def test_write_tensorboard_experiment_data_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.write_tensorboard_experiment_data), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_service.WriteTensorboardExperimentDataResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.write_tensorboard_experiment_data(
            tensorboard_experiment="tensorboard_experiment_value",
            write_run_data_requests=[
                tensorboard_service.WriteTensorboardRunDataRequest(
                    tensorboard_run="tensorboard_run_value"
                )
            ],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].tensorboard_experiment
        mock_val = "tensorboard_experiment_value"
        assert arg == mock_val
        arg = args[0].write_run_data_requests
        mock_val = [
            tensorboard_service.WriteTensorboardRunDataRequest(
                tensorboard_run="tensorboard_run_value"
            )
        ]
        assert arg == mock_val


def test_write_tensorboard_experiment_data_flattened_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.write_tensorboard_experiment_data(
            tensorboard_service.WriteTensorboardExperimentDataRequest(),
            tensorboard_experiment="tensorboard_experiment_value",
            write_run_data_requests=[
                tensorboard_service.WriteTensorboardRunDataRequest(
                    tensorboard_run="tensorboard_run_value"
                )
            ],
        )


@pytest.mark.asyncio
async def test_write_tensorboard_experiment_data_flattened_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.write_tensorboard_experiment_data), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_service.WriteTensorboardExperimentDataResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.WriteTensorboardExperimentDataResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.write_tensorboard_experiment_data(
            tensorboard_experiment="tensorboard_experiment_value",
            write_run_data_requests=[
                tensorboard_service.WriteTensorboardRunDataRequest(
                    tensorboard_run="tensorboard_run_value"
                )
            ],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].tensorboard_experiment
        mock_val = "tensorboard_experiment_value"
        assert arg == mock_val
        arg = args[0].write_run_data_requests
        mock_val = [
            tensorboard_service.WriteTensorboardRunDataRequest(
                tensorboard_run="tensorboard_run_value"
            )
        ]
        assert arg == mock_val


@pytest.mark.asyncio
async def test_write_tensorboard_experiment_data_flattened_error_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.write_tensorboard_experiment_data(
            tensorboard_service.WriteTensorboardExperimentDataRequest(),
            tensorboard_experiment="tensorboard_experiment_value",
            write_run_data_requests=[
                tensorboard_service.WriteTensorboardRunDataRequest(
                    tensorboard_run="tensorboard_run_value"
                )
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.WriteTensorboardRunDataRequest,
        dict,
    ],
)
def test_write_tensorboard_run_data(request_type, transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.write_tensorboard_run_data), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_service.WriteTensorboardRunDataResponse()
        response = client.write_tensorboard_run_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.WriteTensorboardRunDataRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tensorboard_service.WriteTensorboardRunDataResponse)


def test_write_tensorboard_run_data_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.write_tensorboard_run_data), "__call__"
    ) as call:
        client.write_tensorboard_run_data()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.WriteTensorboardRunDataRequest()


@pytest.mark.asyncio
async def test_write_tensorboard_run_data_async(
    transport: str = "grpc_asyncio",
    request_type=tensorboard_service.WriteTensorboardRunDataRequest,
):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.write_tensorboard_run_data), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.WriteTensorboardRunDataResponse()
        )
        response = await client.write_tensorboard_run_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.WriteTensorboardRunDataRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tensorboard_service.WriteTensorboardRunDataResponse)


@pytest.mark.asyncio
async def test_write_tensorboard_run_data_async_from_dict():
    await test_write_tensorboard_run_data_async(request_type=dict)


def test_write_tensorboard_run_data_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.WriteTensorboardRunDataRequest()

    request.tensorboard_run = "tensorboard_run_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.write_tensorboard_run_data), "__call__"
    ) as call:
        call.return_value = tensorboard_service.WriteTensorboardRunDataResponse()
        client.write_tensorboard_run_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "tensorboard_run=tensorboard_run_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_write_tensorboard_run_data_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.WriteTensorboardRunDataRequest()

    request.tensorboard_run = "tensorboard_run_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.write_tensorboard_run_data), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.WriteTensorboardRunDataResponse()
        )
        await client.write_tensorboard_run_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "tensorboard_run=tensorboard_run_value",
    ) in kw["metadata"]


def test_write_tensorboard_run_data_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.write_tensorboard_run_data), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_service.WriteTensorboardRunDataResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.write_tensorboard_run_data(
            tensorboard_run="tensorboard_run_value",
            time_series_data=[
                tensorboard_data.TimeSeriesData(
                    tensorboard_time_series_id="tensorboard_time_series_id_value"
                )
            ],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].tensorboard_run
        mock_val = "tensorboard_run_value"
        assert arg == mock_val
        arg = args[0].time_series_data
        mock_val = [
            tensorboard_data.TimeSeriesData(
                tensorboard_time_series_id="tensorboard_time_series_id_value"
            )
        ]
        assert arg == mock_val


def test_write_tensorboard_run_data_flattened_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.write_tensorboard_run_data(
            tensorboard_service.WriteTensorboardRunDataRequest(),
            tensorboard_run="tensorboard_run_value",
            time_series_data=[
                tensorboard_data.TimeSeriesData(
                    tensorboard_time_series_id="tensorboard_time_series_id_value"
                )
            ],
        )


@pytest.mark.asyncio
async def test_write_tensorboard_run_data_flattened_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.write_tensorboard_run_data), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_service.WriteTensorboardRunDataResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.WriteTensorboardRunDataResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.write_tensorboard_run_data(
            tensorboard_run="tensorboard_run_value",
            time_series_data=[
                tensorboard_data.TimeSeriesData(
                    tensorboard_time_series_id="tensorboard_time_series_id_value"
                )
            ],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].tensorboard_run
        mock_val = "tensorboard_run_value"
        assert arg == mock_val
        arg = args[0].time_series_data
        mock_val = [
            tensorboard_data.TimeSeriesData(
                tensorboard_time_series_id="tensorboard_time_series_id_value"
            )
        ]
        assert arg == mock_val


@pytest.mark.asyncio
async def test_write_tensorboard_run_data_flattened_error_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.write_tensorboard_run_data(
            tensorboard_service.WriteTensorboardRunDataRequest(),
            tensorboard_run="tensorboard_run_value",
            time_series_data=[
                tensorboard_data.TimeSeriesData(
                    tensorboard_time_series_id="tensorboard_time_series_id_value"
                )
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.ExportTensorboardTimeSeriesDataRequest,
        dict,
    ],
)
def test_export_tensorboard_time_series_data(request_type, transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_tensorboard_time_series_data), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tensorboard_service.ExportTensorboardTimeSeriesDataResponse(
            next_page_token="next_page_token_value",
        )
        response = client.export_tensorboard_time_series_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.ExportTensorboardTimeSeriesDataRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ExportTensorboardTimeSeriesDataPager)
    assert response.next_page_token == "next_page_token_value"


def test_export_tensorboard_time_series_data_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_tensorboard_time_series_data), "__call__"
    ) as call:
        client.export_tensorboard_time_series_data()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.ExportTensorboardTimeSeriesDataRequest()


@pytest.mark.asyncio
async def test_export_tensorboard_time_series_data_async(
    transport: str = "grpc_asyncio",
    request_type=tensorboard_service.ExportTensorboardTimeSeriesDataRequest,
):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_tensorboard_time_series_data), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.ExportTensorboardTimeSeriesDataResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.export_tensorboard_time_series_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == tensorboard_service.ExportTensorboardTimeSeriesDataRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ExportTensorboardTimeSeriesDataAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_export_tensorboard_time_series_data_async_from_dict():
    await test_export_tensorboard_time_series_data_async(request_type=dict)


def test_export_tensorboard_time_series_data_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.ExportTensorboardTimeSeriesDataRequest()

    request.tensorboard_time_series = "tensorboard_time_series_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_tensorboard_time_series_data), "__call__"
    ) as call:
        call.return_value = (
            tensorboard_service.ExportTensorboardTimeSeriesDataResponse()
        )
        client.export_tensorboard_time_series_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "tensorboard_time_series=tensorboard_time_series_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_export_tensorboard_time_series_data_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tensorboard_service.ExportTensorboardTimeSeriesDataRequest()

    request.tensorboard_time_series = "tensorboard_time_series_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_tensorboard_time_series_data), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.ExportTensorboardTimeSeriesDataResponse()
        )
        await client.export_tensorboard_time_series_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "tensorboard_time_series=tensorboard_time_series_value",
    ) in kw["metadata"]


def test_export_tensorboard_time_series_data_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_tensorboard_time_series_data), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            tensorboard_service.ExportTensorboardTimeSeriesDataResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.export_tensorboard_time_series_data(
            tensorboard_time_series="tensorboard_time_series_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].tensorboard_time_series
        mock_val = "tensorboard_time_series_value"
        assert arg == mock_val


def test_export_tensorboard_time_series_data_flattened_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.export_tensorboard_time_series_data(
            tensorboard_service.ExportTensorboardTimeSeriesDataRequest(),
            tensorboard_time_series="tensorboard_time_series_value",
        )


@pytest.mark.asyncio
async def test_export_tensorboard_time_series_data_flattened_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_tensorboard_time_series_data), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            tensorboard_service.ExportTensorboardTimeSeriesDataResponse()
        )

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tensorboard_service.ExportTensorboardTimeSeriesDataResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.export_tensorboard_time_series_data(
            tensorboard_time_series="tensorboard_time_series_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].tensorboard_time_series
        mock_val = "tensorboard_time_series_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_export_tensorboard_time_series_data_flattened_error_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.export_tensorboard_time_series_data(
            tensorboard_service.ExportTensorboardTimeSeriesDataRequest(),
            tensorboard_time_series="tensorboard_time_series_value",
        )


def test_export_tensorboard_time_series_data_pager(transport_name: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_tensorboard_time_series_data), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            tensorboard_service.ExportTensorboardTimeSeriesDataResponse(
                time_series_data_points=[
                    tensorboard_data.TimeSeriesDataPoint(),
                    tensorboard_data.TimeSeriesDataPoint(),
                    tensorboard_data.TimeSeriesDataPoint(),
                ],
                next_page_token="abc",
            ),
            tensorboard_service.ExportTensorboardTimeSeriesDataResponse(
                time_series_data_points=[],
                next_page_token="def",
            ),
            tensorboard_service.ExportTensorboardTimeSeriesDataResponse(
                time_series_data_points=[
                    tensorboard_data.TimeSeriesDataPoint(),
                ],
                next_page_token="ghi",
            ),
            tensorboard_service.ExportTensorboardTimeSeriesDataResponse(
                time_series_data_points=[
                    tensorboard_data.TimeSeriesDataPoint(),
                    tensorboard_data.TimeSeriesDataPoint(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("tensorboard_time_series", ""),)
            ),
        )
        pager = client.export_tensorboard_time_series_data(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, tensorboard_data.TimeSeriesDataPoint) for i in results)


def test_export_tensorboard_time_series_data_pages(transport_name: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_tensorboard_time_series_data), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            tensorboard_service.ExportTensorboardTimeSeriesDataResponse(
                time_series_data_points=[
                    tensorboard_data.TimeSeriesDataPoint(),
                    tensorboard_data.TimeSeriesDataPoint(),
                    tensorboard_data.TimeSeriesDataPoint(),
                ],
                next_page_token="abc",
            ),
            tensorboard_service.ExportTensorboardTimeSeriesDataResponse(
                time_series_data_points=[],
                next_page_token="def",
            ),
            tensorboard_service.ExportTensorboardTimeSeriesDataResponse(
                time_series_data_points=[
                    tensorboard_data.TimeSeriesDataPoint(),
                ],
                next_page_token="ghi",
            ),
            tensorboard_service.ExportTensorboardTimeSeriesDataResponse(
                time_series_data_points=[
                    tensorboard_data.TimeSeriesDataPoint(),
                    tensorboard_data.TimeSeriesDataPoint(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.export_tensorboard_time_series_data(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_export_tensorboard_time_series_data_async_pager():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_tensorboard_time_series_data),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            tensorboard_service.ExportTensorboardTimeSeriesDataResponse(
                time_series_data_points=[
                    tensorboard_data.TimeSeriesDataPoint(),
                    tensorboard_data.TimeSeriesDataPoint(),
                    tensorboard_data.TimeSeriesDataPoint(),
                ],
                next_page_token="abc",
            ),
            tensorboard_service.ExportTensorboardTimeSeriesDataResponse(
                time_series_data_points=[],
                next_page_token="def",
            ),
            tensorboard_service.ExportTensorboardTimeSeriesDataResponse(
                time_series_data_points=[
                    tensorboard_data.TimeSeriesDataPoint(),
                ],
                next_page_token="ghi",
            ),
            tensorboard_service.ExportTensorboardTimeSeriesDataResponse(
                time_series_data_points=[
                    tensorboard_data.TimeSeriesDataPoint(),
                    tensorboard_data.TimeSeriesDataPoint(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.export_tensorboard_time_series_data(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, tensorboard_data.TimeSeriesDataPoint) for i in responses
        )


@pytest.mark.asyncio
async def test_export_tensorboard_time_series_data_async_pages():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_tensorboard_time_series_data),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            tensorboard_service.ExportTensorboardTimeSeriesDataResponse(
                time_series_data_points=[
                    tensorboard_data.TimeSeriesDataPoint(),
                    tensorboard_data.TimeSeriesDataPoint(),
                    tensorboard_data.TimeSeriesDataPoint(),
                ],
                next_page_token="abc",
            ),
            tensorboard_service.ExportTensorboardTimeSeriesDataResponse(
                time_series_data_points=[],
                next_page_token="def",
            ),
            tensorboard_service.ExportTensorboardTimeSeriesDataResponse(
                time_series_data_points=[
                    tensorboard_data.TimeSeriesDataPoint(),
                ],
                next_page_token="ghi",
            ),
            tensorboard_service.ExportTensorboardTimeSeriesDataResponse(
                time_series_data_points=[
                    tensorboard_data.TimeSeriesDataPoint(),
                    tensorboard_data.TimeSeriesDataPoint(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.export_tensorboard_time_series_data(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.CreateTensorboardRequest,
        dict,
    ],
)
def test_create_tensorboard_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["tensorboard"] = {
        "name": "name_value",
        "display_name": "display_name_value",
        "description": "description_value",
        "encryption_spec": {"kms_key_name": "kms_key_name_value"},
        "blob_storage_path_prefix": "blob_storage_path_prefix_value",
        "run_count": 989,
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "etag": "etag_value",
        "is_default": True,
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = tensorboard_service.CreateTensorboardRequest.meta.fields["tensorboard"]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["tensorboard"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["tensorboard"][field])):
                    del request_init["tensorboard"][field][i][subfield]
            else:
                del request_init["tensorboard"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_tensorboard(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_tensorboard_rest_required_fields(
    request_type=tensorboard_service.CreateTensorboardRequest,
):
    transport_class = transports.TensorboardServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_tensorboard._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_tensorboard._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_tensorboard(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_tensorboard_rest_unset_required_fields():
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_tensorboard._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "tensorboard",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_tensorboard_rest_interceptors(null_interceptor):
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TensorboardServiceRestInterceptor(),
    )
    client = TensorboardServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.TensorboardServiceRestInterceptor, "post_create_tensorboard"
    ) as post, mock.patch.object(
        transports.TensorboardServiceRestInterceptor, "pre_create_tensorboard"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tensorboard_service.CreateTensorboardRequest.pb(
            tensorboard_service.CreateTensorboardRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = tensorboard_service.CreateTensorboardRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_tensorboard(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_tensorboard_rest_bad_request(
    transport: str = "rest", request_type=tensorboard_service.CreateTensorboardRequest
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_tensorboard(request)


def test_create_tensorboard_rest_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            tensorboard=gca_tensorboard.Tensorboard(name="name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_tensorboard(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/tensorboards"
            % client.transport._host,
            args[1],
        )


def test_create_tensorboard_rest_flattened_error(transport: str = "rest"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_tensorboard(
            tensorboard_service.CreateTensorboardRequest(),
            parent="parent_value",
            tensorboard=gca_tensorboard.Tensorboard(name="name_value"),
        )


def test_create_tensorboard_rest_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.GetTensorboardRequest,
        dict,
    ],
)
def test_get_tensorboard_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/tensorboards/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tensorboard.Tensorboard(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            blob_storage_path_prefix="blob_storage_path_prefix_value",
            run_count=989,
            etag="etag_value",
            is_default=True,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = tensorboard.Tensorboard.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_tensorboard(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, tensorboard.Tensorboard)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.blob_storage_path_prefix == "blob_storage_path_prefix_value"
    assert response.run_count == 989
    assert response.etag == "etag_value"
    assert response.is_default is True


def test_get_tensorboard_rest_required_fields(
    request_type=tensorboard_service.GetTensorboardRequest,
):
    transport_class = transports.TensorboardServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_tensorboard._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_tensorboard._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = tensorboard.Tensorboard()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = tensorboard.Tensorboard.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_tensorboard(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_tensorboard_rest_unset_required_fields():
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_tensorboard._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_tensorboard_rest_interceptors(null_interceptor):
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TensorboardServiceRestInterceptor(),
    )
    client = TensorboardServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TensorboardServiceRestInterceptor, "post_get_tensorboard"
    ) as post, mock.patch.object(
        transports.TensorboardServiceRestInterceptor, "pre_get_tensorboard"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tensorboard_service.GetTensorboardRequest.pb(
            tensorboard_service.GetTensorboardRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = tensorboard.Tensorboard.to_json(
            tensorboard.Tensorboard()
        )

        request = tensorboard_service.GetTensorboardRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = tensorboard.Tensorboard()

        client.get_tensorboard(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_tensorboard_rest_bad_request(
    transport: str = "rest", request_type=tensorboard_service.GetTensorboardRequest
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/tensorboards/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_tensorboard(request)


def test_get_tensorboard_rest_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tensorboard.Tensorboard()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/tensorboards/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = tensorboard.Tensorboard.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_tensorboard(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/tensorboards/*}"
            % client.transport._host,
            args[1],
        )


def test_get_tensorboard_rest_flattened_error(transport: str = "rest"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_tensorboard(
            tensorboard_service.GetTensorboardRequest(),
            name="name_value",
        )


def test_get_tensorboard_rest_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.UpdateTensorboardRequest,
        dict,
    ],
)
def test_update_tensorboard_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "tensorboard": {
            "name": "projects/sample1/locations/sample2/tensorboards/sample3"
        }
    }
    request_init["tensorboard"] = {
        "name": "projects/sample1/locations/sample2/tensorboards/sample3",
        "display_name": "display_name_value",
        "description": "description_value",
        "encryption_spec": {"kms_key_name": "kms_key_name_value"},
        "blob_storage_path_prefix": "blob_storage_path_prefix_value",
        "run_count": 989,
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "etag": "etag_value",
        "is_default": True,
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = tensorboard_service.UpdateTensorboardRequest.meta.fields["tensorboard"]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["tensorboard"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["tensorboard"][field])):
                    del request_init["tensorboard"][field][i][subfield]
            else:
                del request_init["tensorboard"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_tensorboard(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_tensorboard_rest_required_fields(
    request_type=tensorboard_service.UpdateTensorboardRequest,
):
    transport_class = transports.TensorboardServiceRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_tensorboard._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_tensorboard._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "patch",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_tensorboard(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_tensorboard_rest_unset_required_fields():
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_tensorboard._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("updateMask",))
        & set(
            (
                "updateMask",
                "tensorboard",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_tensorboard_rest_interceptors(null_interceptor):
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TensorboardServiceRestInterceptor(),
    )
    client = TensorboardServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.TensorboardServiceRestInterceptor, "post_update_tensorboard"
    ) as post, mock.patch.object(
        transports.TensorboardServiceRestInterceptor, "pre_update_tensorboard"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tensorboard_service.UpdateTensorboardRequest.pb(
            tensorboard_service.UpdateTensorboardRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = tensorboard_service.UpdateTensorboardRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_tensorboard(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_tensorboard_rest_bad_request(
    transport: str = "rest", request_type=tensorboard_service.UpdateTensorboardRequest
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "tensorboard": {
            "name": "projects/sample1/locations/sample2/tensorboards/sample3"
        }
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_tensorboard(request)


def test_update_tensorboard_rest_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "tensorboard": {
                "name": "projects/sample1/locations/sample2/tensorboards/sample3"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            tensorboard=gca_tensorboard.Tensorboard(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_tensorboard(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{tensorboard.name=projects/*/locations/*/tensorboards/*}"
            % client.transport._host,
            args[1],
        )


def test_update_tensorboard_rest_flattened_error(transport: str = "rest"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_tensorboard(
            tensorboard_service.UpdateTensorboardRequest(),
            tensorboard=gca_tensorboard.Tensorboard(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_tensorboard_rest_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.ListTensorboardsRequest,
        dict,
    ],
)
def test_list_tensorboards_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tensorboard_service.ListTensorboardsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = tensorboard_service.ListTensorboardsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_tensorboards(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTensorboardsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_tensorboards_rest_required_fields(
    request_type=tensorboard_service.ListTensorboardsRequest,
):
    transport_class = transports.TensorboardServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_tensorboards._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_tensorboards._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "order_by",
            "page_size",
            "page_token",
            "read_mask",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = tensorboard_service.ListTensorboardsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = tensorboard_service.ListTensorboardsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_tensorboards(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_tensorboards_rest_unset_required_fields():
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_tensorboards._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "orderBy",
                "pageSize",
                "pageToken",
                "readMask",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_tensorboards_rest_interceptors(null_interceptor):
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TensorboardServiceRestInterceptor(),
    )
    client = TensorboardServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TensorboardServiceRestInterceptor, "post_list_tensorboards"
    ) as post, mock.patch.object(
        transports.TensorboardServiceRestInterceptor, "pre_list_tensorboards"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tensorboard_service.ListTensorboardsRequest.pb(
            tensorboard_service.ListTensorboardsRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = (
            tensorboard_service.ListTensorboardsResponse.to_json(
                tensorboard_service.ListTensorboardsResponse()
            )
        )

        request = tensorboard_service.ListTensorboardsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = tensorboard_service.ListTensorboardsResponse()

        client.list_tensorboards(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_tensorboards_rest_bad_request(
    transport: str = "rest", request_type=tensorboard_service.ListTensorboardsRequest
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_tensorboards(request)


def test_list_tensorboards_rest_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tensorboard_service.ListTensorboardsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = tensorboard_service.ListTensorboardsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_tensorboards(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/tensorboards"
            % client.transport._host,
            args[1],
        )


def test_list_tensorboards_rest_flattened_error(transport: str = "rest"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_tensorboards(
            tensorboard_service.ListTensorboardsRequest(),
            parent="parent_value",
        )


def test_list_tensorboards_rest_pager(transport: str = "rest"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            tensorboard_service.ListTensorboardsResponse(
                tensorboards=[
                    tensorboard.Tensorboard(),
                    tensorboard.Tensorboard(),
                    tensorboard.Tensorboard(),
                ],
                next_page_token="abc",
            ),
            tensorboard_service.ListTensorboardsResponse(
                tensorboards=[],
                next_page_token="def",
            ),
            tensorboard_service.ListTensorboardsResponse(
                tensorboards=[
                    tensorboard.Tensorboard(),
                ],
                next_page_token="ghi",
            ),
            tensorboard_service.ListTensorboardsResponse(
                tensorboards=[
                    tensorboard.Tensorboard(),
                    tensorboard.Tensorboard(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            tensorboard_service.ListTensorboardsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_tensorboards(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, tensorboard.Tensorboard) for i in results)

        pages = list(client.list_tensorboards(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.DeleteTensorboardRequest,
        dict,
    ],
)
def test_delete_tensorboard_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/tensorboards/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_tensorboard(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_tensorboard_rest_required_fields(
    request_type=tensorboard_service.DeleteTensorboardRequest,
):
    transport_class = transports.TensorboardServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_tensorboard._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_tensorboard._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "delete",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_tensorboard(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_tensorboard_rest_unset_required_fields():
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_tensorboard._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_tensorboard_rest_interceptors(null_interceptor):
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TensorboardServiceRestInterceptor(),
    )
    client = TensorboardServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.TensorboardServiceRestInterceptor, "post_delete_tensorboard"
    ) as post, mock.patch.object(
        transports.TensorboardServiceRestInterceptor, "pre_delete_tensorboard"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tensorboard_service.DeleteTensorboardRequest.pb(
            tensorboard_service.DeleteTensorboardRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = tensorboard_service.DeleteTensorboardRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_tensorboard(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_tensorboard_rest_bad_request(
    transport: str = "rest", request_type=tensorboard_service.DeleteTensorboardRequest
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/tensorboards/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_tensorboard(request)


def test_delete_tensorboard_rest_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/tensorboards/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_tensorboard(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/tensorboards/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_tensorboard_rest_flattened_error(transport: str = "rest"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_tensorboard(
            tensorboard_service.DeleteTensorboardRequest(),
            name="name_value",
        )


def test_delete_tensorboard_rest_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.ReadTensorboardUsageRequest,
        dict,
    ],
)
def test_read_tensorboard_usage_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "tensorboard": "projects/sample1/locations/sample2/tensorboards/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tensorboard_service.ReadTensorboardUsageResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = tensorboard_service.ReadTensorboardUsageResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.read_tensorboard_usage(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, tensorboard_service.ReadTensorboardUsageResponse)


def test_read_tensorboard_usage_rest_required_fields(
    request_type=tensorboard_service.ReadTensorboardUsageRequest,
):
    transport_class = transports.TensorboardServiceRestTransport

    request_init = {}
    request_init["tensorboard"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).read_tensorboard_usage._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["tensorboard"] = "tensorboard_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).read_tensorboard_usage._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "tensorboard" in jsonified_request
    assert jsonified_request["tensorboard"] == "tensorboard_value"

    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = tensorboard_service.ReadTensorboardUsageResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = tensorboard_service.ReadTensorboardUsageResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.read_tensorboard_usage(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_read_tensorboard_usage_rest_unset_required_fields():
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.read_tensorboard_usage._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("tensorboard",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_read_tensorboard_usage_rest_interceptors(null_interceptor):
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TensorboardServiceRestInterceptor(),
    )
    client = TensorboardServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TensorboardServiceRestInterceptor, "post_read_tensorboard_usage"
    ) as post, mock.patch.object(
        transports.TensorboardServiceRestInterceptor, "pre_read_tensorboard_usage"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tensorboard_service.ReadTensorboardUsageRequest.pb(
            tensorboard_service.ReadTensorboardUsageRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = (
            tensorboard_service.ReadTensorboardUsageResponse.to_json(
                tensorboard_service.ReadTensorboardUsageResponse()
            )
        )

        request = tensorboard_service.ReadTensorboardUsageRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = tensorboard_service.ReadTensorboardUsageResponse()

        client.read_tensorboard_usage(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_read_tensorboard_usage_rest_bad_request(
    transport: str = "rest",
    request_type=tensorboard_service.ReadTensorboardUsageRequest,
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "tensorboard": "projects/sample1/locations/sample2/tensorboards/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.read_tensorboard_usage(request)


def test_read_tensorboard_usage_rest_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tensorboard_service.ReadTensorboardUsageResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "tensorboard": "projects/sample1/locations/sample2/tensorboards/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            tensorboard="tensorboard_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = tensorboard_service.ReadTensorboardUsageResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.read_tensorboard_usage(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{tensorboard=projects/*/locations/*/tensorboards/*}:readUsage"
            % client.transport._host,
            args[1],
        )


def test_read_tensorboard_usage_rest_flattened_error(transport: str = "rest"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.read_tensorboard_usage(
            tensorboard_service.ReadTensorboardUsageRequest(),
            tensorboard="tensorboard_value",
        )


def test_read_tensorboard_usage_rest_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.ReadTensorboardSizeRequest,
        dict,
    ],
)
def test_read_tensorboard_size_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "tensorboard": "projects/sample1/locations/sample2/tensorboards/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tensorboard_service.ReadTensorboardSizeResponse(
            storage_size_byte=1826,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = tensorboard_service.ReadTensorboardSizeResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.read_tensorboard_size(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, tensorboard_service.ReadTensorboardSizeResponse)
    assert response.storage_size_byte == 1826


def test_read_tensorboard_size_rest_required_fields(
    request_type=tensorboard_service.ReadTensorboardSizeRequest,
):
    transport_class = transports.TensorboardServiceRestTransport

    request_init = {}
    request_init["tensorboard"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).read_tensorboard_size._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["tensorboard"] = "tensorboard_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).read_tensorboard_size._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "tensorboard" in jsonified_request
    assert jsonified_request["tensorboard"] == "tensorboard_value"

    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = tensorboard_service.ReadTensorboardSizeResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = tensorboard_service.ReadTensorboardSizeResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.read_tensorboard_size(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_read_tensorboard_size_rest_unset_required_fields():
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.read_tensorboard_size._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("tensorboard",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_read_tensorboard_size_rest_interceptors(null_interceptor):
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TensorboardServiceRestInterceptor(),
    )
    client = TensorboardServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TensorboardServiceRestInterceptor, "post_read_tensorboard_size"
    ) as post, mock.patch.object(
        transports.TensorboardServiceRestInterceptor, "pre_read_tensorboard_size"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tensorboard_service.ReadTensorboardSizeRequest.pb(
            tensorboard_service.ReadTensorboardSizeRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = (
            tensorboard_service.ReadTensorboardSizeResponse.to_json(
                tensorboard_service.ReadTensorboardSizeResponse()
            )
        )

        request = tensorboard_service.ReadTensorboardSizeRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = tensorboard_service.ReadTensorboardSizeResponse()

        client.read_tensorboard_size(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_read_tensorboard_size_rest_bad_request(
    transport: str = "rest", request_type=tensorboard_service.ReadTensorboardSizeRequest
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "tensorboard": "projects/sample1/locations/sample2/tensorboards/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.read_tensorboard_size(request)


def test_read_tensorboard_size_rest_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tensorboard_service.ReadTensorboardSizeResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "tensorboard": "projects/sample1/locations/sample2/tensorboards/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            tensorboard="tensorboard_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = tensorboard_service.ReadTensorboardSizeResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.read_tensorboard_size(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{tensorboard=projects/*/locations/*/tensorboards/*}:readSize"
            % client.transport._host,
            args[1],
        )


def test_read_tensorboard_size_rest_flattened_error(transport: str = "rest"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.read_tensorboard_size(
            tensorboard_service.ReadTensorboardSizeRequest(),
            tensorboard="tensorboard_value",
        )


def test_read_tensorboard_size_rest_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.CreateTensorboardExperimentRequest,
        dict,
    ],
)
def test_create_tensorboard_experiment_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/tensorboards/sample3"}
    request_init["tensorboard_experiment"] = {
        "name": "name_value",
        "display_name": "display_name_value",
        "description": "description_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "etag": "etag_value",
        "source": "source_value",
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = tensorboard_service.CreateTensorboardExperimentRequest.meta.fields[
        "tensorboard_experiment"
    ]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init[
        "tensorboard_experiment"
    ].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["tensorboard_experiment"][field])):
                    del request_init["tensorboard_experiment"][field][i][subfield]
            else:
                del request_init["tensorboard_experiment"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gca_tensorboard_experiment.TensorboardExperiment(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            etag="etag_value",
            source="source_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gca_tensorboard_experiment.TensorboardExperiment.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_tensorboard_experiment(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, gca_tensorboard_experiment.TensorboardExperiment)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.etag == "etag_value"
    assert response.source == "source_value"


def test_create_tensorboard_experiment_rest_required_fields(
    request_type=tensorboard_service.CreateTensorboardExperimentRequest,
):
    transport_class = transports.TensorboardServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["tensorboard_experiment_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped
    assert "tensorboardExperimentId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_tensorboard_experiment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "tensorboardExperimentId" in jsonified_request
    assert (
        jsonified_request["tensorboardExperimentId"]
        == request_init["tensorboard_experiment_id"]
    )

    jsonified_request["parent"] = "parent_value"
    jsonified_request["tensorboardExperimentId"] = "tensorboard_experiment_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_tensorboard_experiment._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("tensorboard_experiment_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "tensorboardExperimentId" in jsonified_request
    assert (
        jsonified_request["tensorboardExperimentId"]
        == "tensorboard_experiment_id_value"
    )

    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gca_tensorboard_experiment.TensorboardExperiment()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = gca_tensorboard_experiment.TensorboardExperiment.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_tensorboard_experiment(request)

            expected_params = [
                (
                    "tensorboardExperimentId",
                    "",
                ),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_tensorboard_experiment_rest_unset_required_fields():
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_tensorboard_experiment._get_unset_required_fields(
        {}
    )
    assert set(unset_fields) == (
        set(("tensorboardExperimentId",))
        & set(
            (
                "parent",
                "tensorboardExperimentId",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_tensorboard_experiment_rest_interceptors(null_interceptor):
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TensorboardServiceRestInterceptor(),
    )
    client = TensorboardServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TensorboardServiceRestInterceptor,
        "post_create_tensorboard_experiment",
    ) as post, mock.patch.object(
        transports.TensorboardServiceRestInterceptor,
        "pre_create_tensorboard_experiment",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tensorboard_service.CreateTensorboardExperimentRequest.pb(
            tensorboard_service.CreateTensorboardExperimentRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = (
            gca_tensorboard_experiment.TensorboardExperiment.to_json(
                gca_tensorboard_experiment.TensorboardExperiment()
            )
        )

        request = tensorboard_service.CreateTensorboardExperimentRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gca_tensorboard_experiment.TensorboardExperiment()

        client.create_tensorboard_experiment(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_tensorboard_experiment_rest_bad_request(
    transport: str = "rest",
    request_type=tensorboard_service.CreateTensorboardExperimentRequest,
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/tensorboards/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_tensorboard_experiment(request)


def test_create_tensorboard_experiment_rest_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gca_tensorboard_experiment.TensorboardExperiment()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/tensorboards/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            tensorboard_experiment=gca_tensorboard_experiment.TensorboardExperiment(
                name="name_value"
            ),
            tensorboard_experiment_id="tensorboard_experiment_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gca_tensorboard_experiment.TensorboardExperiment.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_tensorboard_experiment(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/tensorboards/*}/experiments"
            % client.transport._host,
            args[1],
        )


def test_create_tensorboard_experiment_rest_flattened_error(transport: str = "rest"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_tensorboard_experiment(
            tensorboard_service.CreateTensorboardExperimentRequest(),
            parent="parent_value",
            tensorboard_experiment=gca_tensorboard_experiment.TensorboardExperiment(
                name="name_value"
            ),
            tensorboard_experiment_id="tensorboard_experiment_id_value",
        )


def test_create_tensorboard_experiment_rest_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.GetTensorboardExperimentRequest,
        dict,
    ],
)
def test_get_tensorboard_experiment_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tensorboard_experiment.TensorboardExperiment(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            etag="etag_value",
            source="source_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = tensorboard_experiment.TensorboardExperiment.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_tensorboard_experiment(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, tensorboard_experiment.TensorboardExperiment)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.etag == "etag_value"
    assert response.source == "source_value"


def test_get_tensorboard_experiment_rest_required_fields(
    request_type=tensorboard_service.GetTensorboardExperimentRequest,
):
    transport_class = transports.TensorboardServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_tensorboard_experiment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_tensorboard_experiment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = tensorboard_experiment.TensorboardExperiment()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = tensorboard_experiment.TensorboardExperiment.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_tensorboard_experiment(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_tensorboard_experiment_rest_unset_required_fields():
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_tensorboard_experiment._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_tensorboard_experiment_rest_interceptors(null_interceptor):
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TensorboardServiceRestInterceptor(),
    )
    client = TensorboardServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TensorboardServiceRestInterceptor, "post_get_tensorboard_experiment"
    ) as post, mock.patch.object(
        transports.TensorboardServiceRestInterceptor, "pre_get_tensorboard_experiment"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tensorboard_service.GetTensorboardExperimentRequest.pb(
            tensorboard_service.GetTensorboardExperimentRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = (
            tensorboard_experiment.TensorboardExperiment.to_json(
                tensorboard_experiment.TensorboardExperiment()
            )
        )

        request = tensorboard_service.GetTensorboardExperimentRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = tensorboard_experiment.TensorboardExperiment()

        client.get_tensorboard_experiment(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_tensorboard_experiment_rest_bad_request(
    transport: str = "rest",
    request_type=tensorboard_service.GetTensorboardExperimentRequest,
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_tensorboard_experiment(request)


def test_get_tensorboard_experiment_rest_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tensorboard_experiment.TensorboardExperiment()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = tensorboard_experiment.TensorboardExperiment.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_tensorboard_experiment(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/tensorboards/*/experiments/*}"
            % client.transport._host,
            args[1],
        )


def test_get_tensorboard_experiment_rest_flattened_error(transport: str = "rest"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_tensorboard_experiment(
            tensorboard_service.GetTensorboardExperimentRequest(),
            name="name_value",
        )


def test_get_tensorboard_experiment_rest_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.UpdateTensorboardExperimentRequest,
        dict,
    ],
)
def test_update_tensorboard_experiment_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "tensorboard_experiment": {
            "name": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4"
        }
    }
    request_init["tensorboard_experiment"] = {
        "name": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4",
        "display_name": "display_name_value",
        "description": "description_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "etag": "etag_value",
        "source": "source_value",
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = tensorboard_service.UpdateTensorboardExperimentRequest.meta.fields[
        "tensorboard_experiment"
    ]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init[
        "tensorboard_experiment"
    ].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["tensorboard_experiment"][field])):
                    del request_init["tensorboard_experiment"][field][i][subfield]
            else:
                del request_init["tensorboard_experiment"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gca_tensorboard_experiment.TensorboardExperiment(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            etag="etag_value",
            source="source_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gca_tensorboard_experiment.TensorboardExperiment.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_tensorboard_experiment(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, gca_tensorboard_experiment.TensorboardExperiment)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.etag == "etag_value"
    assert response.source == "source_value"


def test_update_tensorboard_experiment_rest_required_fields(
    request_type=tensorboard_service.UpdateTensorboardExperimentRequest,
):
    transport_class = transports.TensorboardServiceRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_tensorboard_experiment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_tensorboard_experiment._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gca_tensorboard_experiment.TensorboardExperiment()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "patch",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = gca_tensorboard_experiment.TensorboardExperiment.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_tensorboard_experiment(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_tensorboard_experiment_rest_unset_required_fields():
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_tensorboard_experiment._get_unset_required_fields(
        {}
    )
    assert set(unset_fields) == (
        set(("updateMask",))
        & set(
            (
                "updateMask",
                "tensorboardExperiment",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_tensorboard_experiment_rest_interceptors(null_interceptor):
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TensorboardServiceRestInterceptor(),
    )
    client = TensorboardServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TensorboardServiceRestInterceptor,
        "post_update_tensorboard_experiment",
    ) as post, mock.patch.object(
        transports.TensorboardServiceRestInterceptor,
        "pre_update_tensorboard_experiment",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tensorboard_service.UpdateTensorboardExperimentRequest.pb(
            tensorboard_service.UpdateTensorboardExperimentRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = (
            gca_tensorboard_experiment.TensorboardExperiment.to_json(
                gca_tensorboard_experiment.TensorboardExperiment()
            )
        )

        request = tensorboard_service.UpdateTensorboardExperimentRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gca_tensorboard_experiment.TensorboardExperiment()

        client.update_tensorboard_experiment(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_tensorboard_experiment_rest_bad_request(
    transport: str = "rest",
    request_type=tensorboard_service.UpdateTensorboardExperimentRequest,
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "tensorboard_experiment": {
            "name": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4"
        }
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_tensorboard_experiment(request)


def test_update_tensorboard_experiment_rest_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gca_tensorboard_experiment.TensorboardExperiment()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "tensorboard_experiment": {
                "name": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            tensorboard_experiment=gca_tensorboard_experiment.TensorboardExperiment(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gca_tensorboard_experiment.TensorboardExperiment.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_tensorboard_experiment(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{tensorboard_experiment.name=projects/*/locations/*/tensorboards/*/experiments/*}"
            % client.transport._host,
            args[1],
        )


def test_update_tensorboard_experiment_rest_flattened_error(transport: str = "rest"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_tensorboard_experiment(
            tensorboard_service.UpdateTensorboardExperimentRequest(),
            tensorboard_experiment=gca_tensorboard_experiment.TensorboardExperiment(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_tensorboard_experiment_rest_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.ListTensorboardExperimentsRequest,
        dict,
    ],
)
def test_list_tensorboard_experiments_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/tensorboards/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tensorboard_service.ListTensorboardExperimentsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = tensorboard_service.ListTensorboardExperimentsResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_tensorboard_experiments(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTensorboardExperimentsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_tensorboard_experiments_rest_required_fields(
    request_type=tensorboard_service.ListTensorboardExperimentsRequest,
):
    transport_class = transports.TensorboardServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_tensorboard_experiments._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_tensorboard_experiments._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "order_by",
            "page_size",
            "page_token",
            "read_mask",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = tensorboard_service.ListTensorboardExperimentsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = tensorboard_service.ListTensorboardExperimentsResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_tensorboard_experiments(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_tensorboard_experiments_rest_unset_required_fields():
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_tensorboard_experiments._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "orderBy",
                "pageSize",
                "pageToken",
                "readMask",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_tensorboard_experiments_rest_interceptors(null_interceptor):
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TensorboardServiceRestInterceptor(),
    )
    client = TensorboardServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TensorboardServiceRestInterceptor,
        "post_list_tensorboard_experiments",
    ) as post, mock.patch.object(
        transports.TensorboardServiceRestInterceptor, "pre_list_tensorboard_experiments"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tensorboard_service.ListTensorboardExperimentsRequest.pb(
            tensorboard_service.ListTensorboardExperimentsRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = (
            tensorboard_service.ListTensorboardExperimentsResponse.to_json(
                tensorboard_service.ListTensorboardExperimentsResponse()
            )
        )

        request = tensorboard_service.ListTensorboardExperimentsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = tensorboard_service.ListTensorboardExperimentsResponse()

        client.list_tensorboard_experiments(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_tensorboard_experiments_rest_bad_request(
    transport: str = "rest",
    request_type=tensorboard_service.ListTensorboardExperimentsRequest,
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/tensorboards/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_tensorboard_experiments(request)


def test_list_tensorboard_experiments_rest_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tensorboard_service.ListTensorboardExperimentsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/tensorboards/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = tensorboard_service.ListTensorboardExperimentsResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_tensorboard_experiments(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/tensorboards/*}/experiments"
            % client.transport._host,
            args[1],
        )


def test_list_tensorboard_experiments_rest_flattened_error(transport: str = "rest"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_tensorboard_experiments(
            tensorboard_service.ListTensorboardExperimentsRequest(),
            parent="parent_value",
        )


def test_list_tensorboard_experiments_rest_pager(transport: str = "rest"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            tensorboard_service.ListTensorboardExperimentsResponse(
                tensorboard_experiments=[
                    tensorboard_experiment.TensorboardExperiment(),
                    tensorboard_experiment.TensorboardExperiment(),
                    tensorboard_experiment.TensorboardExperiment(),
                ],
                next_page_token="abc",
            ),
            tensorboard_service.ListTensorboardExperimentsResponse(
                tensorboard_experiments=[],
                next_page_token="def",
            ),
            tensorboard_service.ListTensorboardExperimentsResponse(
                tensorboard_experiments=[
                    tensorboard_experiment.TensorboardExperiment(),
                ],
                next_page_token="ghi",
            ),
            tensorboard_service.ListTensorboardExperimentsResponse(
                tensorboard_experiments=[
                    tensorboard_experiment.TensorboardExperiment(),
                    tensorboard_experiment.TensorboardExperiment(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            tensorboard_service.ListTensorboardExperimentsResponse.to_json(x)
            for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/tensorboards/sample3"
        }

        pager = client.list_tensorboard_experiments(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, tensorboard_experiment.TensorboardExperiment) for i in results
        )

        pages = list(client.list_tensorboard_experiments(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.DeleteTensorboardExperimentRequest,
        dict,
    ],
)
def test_delete_tensorboard_experiment_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_tensorboard_experiment(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_tensorboard_experiment_rest_required_fields(
    request_type=tensorboard_service.DeleteTensorboardExperimentRequest,
):
    transport_class = transports.TensorboardServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_tensorboard_experiment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_tensorboard_experiment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "delete",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_tensorboard_experiment(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_tensorboard_experiment_rest_unset_required_fields():
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_tensorboard_experiment._get_unset_required_fields(
        {}
    )
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_tensorboard_experiment_rest_interceptors(null_interceptor):
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TensorboardServiceRestInterceptor(),
    )
    client = TensorboardServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.TensorboardServiceRestInterceptor,
        "post_delete_tensorboard_experiment",
    ) as post, mock.patch.object(
        transports.TensorboardServiceRestInterceptor,
        "pre_delete_tensorboard_experiment",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tensorboard_service.DeleteTensorboardExperimentRequest.pb(
            tensorboard_service.DeleteTensorboardExperimentRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = tensorboard_service.DeleteTensorboardExperimentRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_tensorboard_experiment(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_tensorboard_experiment_rest_bad_request(
    transport: str = "rest",
    request_type=tensorboard_service.DeleteTensorboardExperimentRequest,
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_tensorboard_experiment(request)


def test_delete_tensorboard_experiment_rest_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_tensorboard_experiment(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/tensorboards/*/experiments/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_tensorboard_experiment_rest_flattened_error(transport: str = "rest"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_tensorboard_experiment(
            tensorboard_service.DeleteTensorboardExperimentRequest(),
            name="name_value",
        )


def test_delete_tensorboard_experiment_rest_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.CreateTensorboardRunRequest,
        dict,
    ],
)
def test_create_tensorboard_run_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4"
    }
    request_init["tensorboard_run"] = {
        "name": "name_value",
        "display_name": "display_name_value",
        "description": "description_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "etag": "etag_value",
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = tensorboard_service.CreateTensorboardRunRequest.meta.fields[
        "tensorboard_run"
    ]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["tensorboard_run"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["tensorboard_run"][field])):
                    del request_init["tensorboard_run"][field][i][subfield]
            else:
                del request_init["tensorboard_run"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gca_tensorboard_run.TensorboardRun(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            etag="etag_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gca_tensorboard_run.TensorboardRun.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_tensorboard_run(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, gca_tensorboard_run.TensorboardRun)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.etag == "etag_value"


def test_create_tensorboard_run_rest_required_fields(
    request_type=tensorboard_service.CreateTensorboardRunRequest,
):
    transport_class = transports.TensorboardServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["tensorboard_run_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped
    assert "tensorboardRunId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_tensorboard_run._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "tensorboardRunId" in jsonified_request
    assert jsonified_request["tensorboardRunId"] == request_init["tensorboard_run_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["tensorboardRunId"] = "tensorboard_run_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_tensorboard_run._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("tensorboard_run_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "tensorboardRunId" in jsonified_request
    assert jsonified_request["tensorboardRunId"] == "tensorboard_run_id_value"

    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gca_tensorboard_run.TensorboardRun()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = gca_tensorboard_run.TensorboardRun.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_tensorboard_run(request)

            expected_params = [
                (
                    "tensorboardRunId",
                    "",
                ),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_tensorboard_run_rest_unset_required_fields():
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_tensorboard_run._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("tensorboardRunId",))
        & set(
            (
                "parent",
                "tensorboardRun",
                "tensorboardRunId",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_tensorboard_run_rest_interceptors(null_interceptor):
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TensorboardServiceRestInterceptor(),
    )
    client = TensorboardServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TensorboardServiceRestInterceptor, "post_create_tensorboard_run"
    ) as post, mock.patch.object(
        transports.TensorboardServiceRestInterceptor, "pre_create_tensorboard_run"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tensorboard_service.CreateTensorboardRunRequest.pb(
            tensorboard_service.CreateTensorboardRunRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = gca_tensorboard_run.TensorboardRun.to_json(
            gca_tensorboard_run.TensorboardRun()
        )

        request = tensorboard_service.CreateTensorboardRunRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gca_tensorboard_run.TensorboardRun()

        client.create_tensorboard_run(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_tensorboard_run_rest_bad_request(
    transport: str = "rest",
    request_type=tensorboard_service.CreateTensorboardRunRequest,
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_tensorboard_run(request)


def test_create_tensorboard_run_rest_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gca_tensorboard_run.TensorboardRun()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            tensorboard_run=gca_tensorboard_run.TensorboardRun(name="name_value"),
            tensorboard_run_id="tensorboard_run_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gca_tensorboard_run.TensorboardRun.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_tensorboard_run(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/tensorboards/*/experiments/*}/runs"
            % client.transport._host,
            args[1],
        )


def test_create_tensorboard_run_rest_flattened_error(transport: str = "rest"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_tensorboard_run(
            tensorboard_service.CreateTensorboardRunRequest(),
            parent="parent_value",
            tensorboard_run=gca_tensorboard_run.TensorboardRun(name="name_value"),
            tensorboard_run_id="tensorboard_run_id_value",
        )


def test_create_tensorboard_run_rest_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.BatchCreateTensorboardRunsRequest,
        dict,
    ],
)
def test_batch_create_tensorboard_runs_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tensorboard_service.BatchCreateTensorboardRunsResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = tensorboard_service.BatchCreateTensorboardRunsResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.batch_create_tensorboard_runs(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, tensorboard_service.BatchCreateTensorboardRunsResponse)


def test_batch_create_tensorboard_runs_rest_required_fields(
    request_type=tensorboard_service.BatchCreateTensorboardRunsRequest,
):
    transport_class = transports.TensorboardServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).batch_create_tensorboard_runs._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).batch_create_tensorboard_runs._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = tensorboard_service.BatchCreateTensorboardRunsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = tensorboard_service.BatchCreateTensorboardRunsResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.batch_create_tensorboard_runs(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_batch_create_tensorboard_runs_rest_unset_required_fields():
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.batch_create_tensorboard_runs._get_unset_required_fields(
        {}
    )
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "requests",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_batch_create_tensorboard_runs_rest_interceptors(null_interceptor):
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TensorboardServiceRestInterceptor(),
    )
    client = TensorboardServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TensorboardServiceRestInterceptor,
        "post_batch_create_tensorboard_runs",
    ) as post, mock.patch.object(
        transports.TensorboardServiceRestInterceptor,
        "pre_batch_create_tensorboard_runs",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tensorboard_service.BatchCreateTensorboardRunsRequest.pb(
            tensorboard_service.BatchCreateTensorboardRunsRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = (
            tensorboard_service.BatchCreateTensorboardRunsResponse.to_json(
                tensorboard_service.BatchCreateTensorboardRunsResponse()
            )
        )

        request = tensorboard_service.BatchCreateTensorboardRunsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = tensorboard_service.BatchCreateTensorboardRunsResponse()

        client.batch_create_tensorboard_runs(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_batch_create_tensorboard_runs_rest_bad_request(
    transport: str = "rest",
    request_type=tensorboard_service.BatchCreateTensorboardRunsRequest,
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.batch_create_tensorboard_runs(request)


def test_batch_create_tensorboard_runs_rest_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tensorboard_service.BatchCreateTensorboardRunsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            requests=[
                tensorboard_service.CreateTensorboardRunRequest(parent="parent_value")
            ],
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = tensorboard_service.BatchCreateTensorboardRunsResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.batch_create_tensorboard_runs(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/tensorboards/*/experiments/*}/runs:batchCreate"
            % client.transport._host,
            args[1],
        )


def test_batch_create_tensorboard_runs_rest_flattened_error(transport: str = "rest"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.batch_create_tensorboard_runs(
            tensorboard_service.BatchCreateTensorboardRunsRequest(),
            parent="parent_value",
            requests=[
                tensorboard_service.CreateTensorboardRunRequest(parent="parent_value")
            ],
        )


def test_batch_create_tensorboard_runs_rest_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.GetTensorboardRunRequest,
        dict,
    ],
)
def test_get_tensorboard_run_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tensorboard_run.TensorboardRun(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            etag="etag_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = tensorboard_run.TensorboardRun.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_tensorboard_run(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, tensorboard_run.TensorboardRun)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.etag == "etag_value"


def test_get_tensorboard_run_rest_required_fields(
    request_type=tensorboard_service.GetTensorboardRunRequest,
):
    transport_class = transports.TensorboardServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_tensorboard_run._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_tensorboard_run._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = tensorboard_run.TensorboardRun()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = tensorboard_run.TensorboardRun.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_tensorboard_run(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_tensorboard_run_rest_unset_required_fields():
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_tensorboard_run._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_tensorboard_run_rest_interceptors(null_interceptor):
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TensorboardServiceRestInterceptor(),
    )
    client = TensorboardServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TensorboardServiceRestInterceptor, "post_get_tensorboard_run"
    ) as post, mock.patch.object(
        transports.TensorboardServiceRestInterceptor, "pre_get_tensorboard_run"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tensorboard_service.GetTensorboardRunRequest.pb(
            tensorboard_service.GetTensorboardRunRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = tensorboard_run.TensorboardRun.to_json(
            tensorboard_run.TensorboardRun()
        )

        request = tensorboard_service.GetTensorboardRunRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = tensorboard_run.TensorboardRun()

        client.get_tensorboard_run(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_tensorboard_run_rest_bad_request(
    transport: str = "rest", request_type=tensorboard_service.GetTensorboardRunRequest
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_tensorboard_run(request)


def test_get_tensorboard_run_rest_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tensorboard_run.TensorboardRun()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = tensorboard_run.TensorboardRun.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_tensorboard_run(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*}"
            % client.transport._host,
            args[1],
        )


def test_get_tensorboard_run_rest_flattened_error(transport: str = "rest"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_tensorboard_run(
            tensorboard_service.GetTensorboardRunRequest(),
            name="name_value",
        )


def test_get_tensorboard_run_rest_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.UpdateTensorboardRunRequest,
        dict,
    ],
)
def test_update_tensorboard_run_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "tensorboard_run": {
            "name": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5"
        }
    }
    request_init["tensorboard_run"] = {
        "name": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5",
        "display_name": "display_name_value",
        "description": "description_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "etag": "etag_value",
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = tensorboard_service.UpdateTensorboardRunRequest.meta.fields[
        "tensorboard_run"
    ]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["tensorboard_run"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["tensorboard_run"][field])):
                    del request_init["tensorboard_run"][field][i][subfield]
            else:
                del request_init["tensorboard_run"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gca_tensorboard_run.TensorboardRun(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            etag="etag_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gca_tensorboard_run.TensorboardRun.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_tensorboard_run(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, gca_tensorboard_run.TensorboardRun)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.etag == "etag_value"


def test_update_tensorboard_run_rest_required_fields(
    request_type=tensorboard_service.UpdateTensorboardRunRequest,
):
    transport_class = transports.TensorboardServiceRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_tensorboard_run._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_tensorboard_run._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gca_tensorboard_run.TensorboardRun()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "patch",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = gca_tensorboard_run.TensorboardRun.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_tensorboard_run(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_tensorboard_run_rest_unset_required_fields():
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_tensorboard_run._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("updateMask",))
        & set(
            (
                "updateMask",
                "tensorboardRun",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_tensorboard_run_rest_interceptors(null_interceptor):
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TensorboardServiceRestInterceptor(),
    )
    client = TensorboardServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TensorboardServiceRestInterceptor, "post_update_tensorboard_run"
    ) as post, mock.patch.object(
        transports.TensorboardServiceRestInterceptor, "pre_update_tensorboard_run"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tensorboard_service.UpdateTensorboardRunRequest.pb(
            tensorboard_service.UpdateTensorboardRunRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = gca_tensorboard_run.TensorboardRun.to_json(
            gca_tensorboard_run.TensorboardRun()
        )

        request = tensorboard_service.UpdateTensorboardRunRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gca_tensorboard_run.TensorboardRun()

        client.update_tensorboard_run(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_tensorboard_run_rest_bad_request(
    transport: str = "rest",
    request_type=tensorboard_service.UpdateTensorboardRunRequest,
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "tensorboard_run": {
            "name": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5"
        }
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_tensorboard_run(request)


def test_update_tensorboard_run_rest_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gca_tensorboard_run.TensorboardRun()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "tensorboard_run": {
                "name": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            tensorboard_run=gca_tensorboard_run.TensorboardRun(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gca_tensorboard_run.TensorboardRun.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_tensorboard_run(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{tensorboard_run.name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*}"
            % client.transport._host,
            args[1],
        )


def test_update_tensorboard_run_rest_flattened_error(transport: str = "rest"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_tensorboard_run(
            tensorboard_service.UpdateTensorboardRunRequest(),
            tensorboard_run=gca_tensorboard_run.TensorboardRun(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_tensorboard_run_rest_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.ListTensorboardRunsRequest,
        dict,
    ],
)
def test_list_tensorboard_runs_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tensorboard_service.ListTensorboardRunsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = tensorboard_service.ListTensorboardRunsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_tensorboard_runs(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTensorboardRunsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_tensorboard_runs_rest_required_fields(
    request_type=tensorboard_service.ListTensorboardRunsRequest,
):
    transport_class = transports.TensorboardServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_tensorboard_runs._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_tensorboard_runs._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "order_by",
            "page_size",
            "page_token",
            "read_mask",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = tensorboard_service.ListTensorboardRunsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = tensorboard_service.ListTensorboardRunsResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_tensorboard_runs(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_tensorboard_runs_rest_unset_required_fields():
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_tensorboard_runs._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "orderBy",
                "pageSize",
                "pageToken",
                "readMask",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_tensorboard_runs_rest_interceptors(null_interceptor):
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TensorboardServiceRestInterceptor(),
    )
    client = TensorboardServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TensorboardServiceRestInterceptor, "post_list_tensorboard_runs"
    ) as post, mock.patch.object(
        transports.TensorboardServiceRestInterceptor, "pre_list_tensorboard_runs"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tensorboard_service.ListTensorboardRunsRequest.pb(
            tensorboard_service.ListTensorboardRunsRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = (
            tensorboard_service.ListTensorboardRunsResponse.to_json(
                tensorboard_service.ListTensorboardRunsResponse()
            )
        )

        request = tensorboard_service.ListTensorboardRunsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = tensorboard_service.ListTensorboardRunsResponse()

        client.list_tensorboard_runs(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_tensorboard_runs_rest_bad_request(
    transport: str = "rest", request_type=tensorboard_service.ListTensorboardRunsRequest
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_tensorboard_runs(request)


def test_list_tensorboard_runs_rest_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tensorboard_service.ListTensorboardRunsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = tensorboard_service.ListTensorboardRunsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_tensorboard_runs(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/tensorboards/*/experiments/*}/runs"
            % client.transport._host,
            args[1],
        )


def test_list_tensorboard_runs_rest_flattened_error(transport: str = "rest"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_tensorboard_runs(
            tensorboard_service.ListTensorboardRunsRequest(),
            parent="parent_value",
        )


def test_list_tensorboard_runs_rest_pager(transport: str = "rest"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            tensorboard_service.ListTensorboardRunsResponse(
                tensorboard_runs=[
                    tensorboard_run.TensorboardRun(),
                    tensorboard_run.TensorboardRun(),
                    tensorboard_run.TensorboardRun(),
                ],
                next_page_token="abc",
            ),
            tensorboard_service.ListTensorboardRunsResponse(
                tensorboard_runs=[],
                next_page_token="def",
            ),
            tensorboard_service.ListTensorboardRunsResponse(
                tensorboard_runs=[
                    tensorboard_run.TensorboardRun(),
                ],
                next_page_token="ghi",
            ),
            tensorboard_service.ListTensorboardRunsResponse(
                tensorboard_runs=[
                    tensorboard_run.TensorboardRun(),
                    tensorboard_run.TensorboardRun(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            tensorboard_service.ListTensorboardRunsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4"
        }

        pager = client.list_tensorboard_runs(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, tensorboard_run.TensorboardRun) for i in results)

        pages = list(client.list_tensorboard_runs(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.DeleteTensorboardRunRequest,
        dict,
    ],
)
def test_delete_tensorboard_run_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_tensorboard_run(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_tensorboard_run_rest_required_fields(
    request_type=tensorboard_service.DeleteTensorboardRunRequest,
):
    transport_class = transports.TensorboardServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_tensorboard_run._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_tensorboard_run._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "delete",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_tensorboard_run(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_tensorboard_run_rest_unset_required_fields():
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_tensorboard_run._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_tensorboard_run_rest_interceptors(null_interceptor):
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TensorboardServiceRestInterceptor(),
    )
    client = TensorboardServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.TensorboardServiceRestInterceptor, "post_delete_tensorboard_run"
    ) as post, mock.patch.object(
        transports.TensorboardServiceRestInterceptor, "pre_delete_tensorboard_run"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tensorboard_service.DeleteTensorboardRunRequest.pb(
            tensorboard_service.DeleteTensorboardRunRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = tensorboard_service.DeleteTensorboardRunRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_tensorboard_run(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_tensorboard_run_rest_bad_request(
    transport: str = "rest",
    request_type=tensorboard_service.DeleteTensorboardRunRequest,
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_tensorboard_run(request)


def test_delete_tensorboard_run_rest_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_tensorboard_run(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_tensorboard_run_rest_flattened_error(transport: str = "rest"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_tensorboard_run(
            tensorboard_service.DeleteTensorboardRunRequest(),
            name="name_value",
        )


def test_delete_tensorboard_run_rest_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.BatchCreateTensorboardTimeSeriesRequest,
        dict,
    ],
)
def test_batch_create_tensorboard_time_series_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tensorboard_service.BatchCreateTensorboardTimeSeriesResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = tensorboard_service.BatchCreateTensorboardTimeSeriesResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.batch_create_tensorboard_time_series(request)

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, tensorboard_service.BatchCreateTensorboardTimeSeriesResponse
    )


def test_batch_create_tensorboard_time_series_rest_required_fields(
    request_type=tensorboard_service.BatchCreateTensorboardTimeSeriesRequest,
):
    transport_class = transports.TensorboardServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).batch_create_tensorboard_time_series._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).batch_create_tensorboard_time_series._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = tensorboard_service.BatchCreateTensorboardTimeSeriesResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = (
                tensorboard_service.BatchCreateTensorboardTimeSeriesResponse.pb(
                    return_value
                )
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.batch_create_tensorboard_time_series(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_batch_create_tensorboard_time_series_rest_unset_required_fields():
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = (
        transport.batch_create_tensorboard_time_series._get_unset_required_fields({})
    )
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "requests",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_batch_create_tensorboard_time_series_rest_interceptors(null_interceptor):
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TensorboardServiceRestInterceptor(),
    )
    client = TensorboardServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TensorboardServiceRestInterceptor,
        "post_batch_create_tensorboard_time_series",
    ) as post, mock.patch.object(
        transports.TensorboardServiceRestInterceptor,
        "pre_batch_create_tensorboard_time_series",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tensorboard_service.BatchCreateTensorboardTimeSeriesRequest.pb(
            tensorboard_service.BatchCreateTensorboardTimeSeriesRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = (
            tensorboard_service.BatchCreateTensorboardTimeSeriesResponse.to_json(
                tensorboard_service.BatchCreateTensorboardTimeSeriesResponse()
            )
        )

        request = tensorboard_service.BatchCreateTensorboardTimeSeriesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = (
            tensorboard_service.BatchCreateTensorboardTimeSeriesResponse()
        )

        client.batch_create_tensorboard_time_series(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_batch_create_tensorboard_time_series_rest_bad_request(
    transport: str = "rest",
    request_type=tensorboard_service.BatchCreateTensorboardTimeSeriesRequest,
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.batch_create_tensorboard_time_series(request)


def test_batch_create_tensorboard_time_series_rest_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tensorboard_service.BatchCreateTensorboardTimeSeriesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            requests=[
                tensorboard_service.CreateTensorboardTimeSeriesRequest(
                    parent="parent_value"
                )
            ],
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = tensorboard_service.BatchCreateTensorboardTimeSeriesResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.batch_create_tensorboard_time_series(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/tensorboards/*/experiments/*}:batchCreate"
            % client.transport._host,
            args[1],
        )


def test_batch_create_tensorboard_time_series_rest_flattened_error(
    transport: str = "rest",
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.batch_create_tensorboard_time_series(
            tensorboard_service.BatchCreateTensorboardTimeSeriesRequest(),
            parent="parent_value",
            requests=[
                tensorboard_service.CreateTensorboardTimeSeriesRequest(
                    parent="parent_value"
                )
            ],
        )


def test_batch_create_tensorboard_time_series_rest_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.CreateTensorboardTimeSeriesRequest,
        dict,
    ],
)
def test_create_tensorboard_time_series_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5"
    }
    request_init["tensorboard_time_series"] = {
        "name": "name_value",
        "display_name": "display_name_value",
        "description": "description_value",
        "value_type": 1,
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "etag": "etag_value",
        "plugin_name": "plugin_name_value",
        "plugin_data": b"plugin_data_blob",
        "metadata": {
            "max_step": 865,
            "max_wall_time": {},
            "max_blob_sequence_length": 2525,
        },
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = tensorboard_service.CreateTensorboardTimeSeriesRequest.meta.fields[
        "tensorboard_time_series"
    ]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init[
        "tensorboard_time_series"
    ].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["tensorboard_time_series"][field])):
                    del request_init["tensorboard_time_series"][field][i][subfield]
            else:
                del request_init["tensorboard_time_series"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gca_tensorboard_time_series.TensorboardTimeSeries(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            value_type=gca_tensorboard_time_series.TensorboardTimeSeries.ValueType.SCALAR,
            etag="etag_value",
            plugin_name="plugin_name_value",
            plugin_data=b"plugin_data_blob",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gca_tensorboard_time_series.TensorboardTimeSeries.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_tensorboard_time_series(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, gca_tensorboard_time_series.TensorboardTimeSeries)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert (
        response.value_type
        == gca_tensorboard_time_series.TensorboardTimeSeries.ValueType.SCALAR
    )
    assert response.etag == "etag_value"
    assert response.plugin_name == "plugin_name_value"
    assert response.plugin_data == b"plugin_data_blob"


def test_create_tensorboard_time_series_rest_required_fields(
    request_type=tensorboard_service.CreateTensorboardTimeSeriesRequest,
):
    transport_class = transports.TensorboardServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_tensorboard_time_series._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_tensorboard_time_series._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("tensorboard_time_series_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gca_tensorboard_time_series.TensorboardTimeSeries()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = gca_tensorboard_time_series.TensorboardTimeSeries.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_tensorboard_time_series(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_tensorboard_time_series_rest_unset_required_fields():
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_tensorboard_time_series._get_unset_required_fields(
        {}
    )
    assert set(unset_fields) == (
        set(("tensorboardTimeSeriesId",))
        & set(
            (
                "parent",
                "tensorboardTimeSeries",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_tensorboard_time_series_rest_interceptors(null_interceptor):
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TensorboardServiceRestInterceptor(),
    )
    client = TensorboardServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TensorboardServiceRestInterceptor,
        "post_create_tensorboard_time_series",
    ) as post, mock.patch.object(
        transports.TensorboardServiceRestInterceptor,
        "pre_create_tensorboard_time_series",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tensorboard_service.CreateTensorboardTimeSeriesRequest.pb(
            tensorboard_service.CreateTensorboardTimeSeriesRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = (
            gca_tensorboard_time_series.TensorboardTimeSeries.to_json(
                gca_tensorboard_time_series.TensorboardTimeSeries()
            )
        )

        request = tensorboard_service.CreateTensorboardTimeSeriesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gca_tensorboard_time_series.TensorboardTimeSeries()

        client.create_tensorboard_time_series(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_tensorboard_time_series_rest_bad_request(
    transport: str = "rest",
    request_type=tensorboard_service.CreateTensorboardTimeSeriesRequest,
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_tensorboard_time_series(request)


def test_create_tensorboard_time_series_rest_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gca_tensorboard_time_series.TensorboardTimeSeries()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            tensorboard_time_series=gca_tensorboard_time_series.TensorboardTimeSeries(
                name="name_value"
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gca_tensorboard_time_series.TensorboardTimeSeries.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_tensorboard_time_series(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/tensorboards/*/experiments/*/runs/*}/timeSeries"
            % client.transport._host,
            args[1],
        )


def test_create_tensorboard_time_series_rest_flattened_error(transport: str = "rest"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_tensorboard_time_series(
            tensorboard_service.CreateTensorboardTimeSeriesRequest(),
            parent="parent_value",
            tensorboard_time_series=gca_tensorboard_time_series.TensorboardTimeSeries(
                name="name_value"
            ),
        )


def test_create_tensorboard_time_series_rest_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.GetTensorboardTimeSeriesRequest,
        dict,
    ],
)
def test_get_tensorboard_time_series_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5/timeSeries/sample6"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tensorboard_time_series.TensorboardTimeSeries(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            value_type=tensorboard_time_series.TensorboardTimeSeries.ValueType.SCALAR,
            etag="etag_value",
            plugin_name="plugin_name_value",
            plugin_data=b"plugin_data_blob",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = tensorboard_time_series.TensorboardTimeSeries.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_tensorboard_time_series(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, tensorboard_time_series.TensorboardTimeSeries)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert (
        response.value_type
        == tensorboard_time_series.TensorboardTimeSeries.ValueType.SCALAR
    )
    assert response.etag == "etag_value"
    assert response.plugin_name == "plugin_name_value"
    assert response.plugin_data == b"plugin_data_blob"


def test_get_tensorboard_time_series_rest_required_fields(
    request_type=tensorboard_service.GetTensorboardTimeSeriesRequest,
):
    transport_class = transports.TensorboardServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_tensorboard_time_series._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_tensorboard_time_series._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = tensorboard_time_series.TensorboardTimeSeries()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = tensorboard_time_series.TensorboardTimeSeries.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_tensorboard_time_series(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_tensorboard_time_series_rest_unset_required_fields():
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_tensorboard_time_series._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_tensorboard_time_series_rest_interceptors(null_interceptor):
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TensorboardServiceRestInterceptor(),
    )
    client = TensorboardServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TensorboardServiceRestInterceptor, "post_get_tensorboard_time_series"
    ) as post, mock.patch.object(
        transports.TensorboardServiceRestInterceptor, "pre_get_tensorboard_time_series"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tensorboard_service.GetTensorboardTimeSeriesRequest.pb(
            tensorboard_service.GetTensorboardTimeSeriesRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = (
            tensorboard_time_series.TensorboardTimeSeries.to_json(
                tensorboard_time_series.TensorboardTimeSeries()
            )
        )

        request = tensorboard_service.GetTensorboardTimeSeriesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = tensorboard_time_series.TensorboardTimeSeries()

        client.get_tensorboard_time_series(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_tensorboard_time_series_rest_bad_request(
    transport: str = "rest",
    request_type=tensorboard_service.GetTensorboardTimeSeriesRequest,
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5/timeSeries/sample6"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_tensorboard_time_series(request)


def test_get_tensorboard_time_series_rest_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tensorboard_time_series.TensorboardTimeSeries()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5/timeSeries/sample6"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = tensorboard_time_series.TensorboardTimeSeries.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_tensorboard_time_series(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/timeSeries/*}"
            % client.transport._host,
            args[1],
        )


def test_get_tensorboard_time_series_rest_flattened_error(transport: str = "rest"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_tensorboard_time_series(
            tensorboard_service.GetTensorboardTimeSeriesRequest(),
            name="name_value",
        )


def test_get_tensorboard_time_series_rest_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.UpdateTensorboardTimeSeriesRequest,
        dict,
    ],
)
def test_update_tensorboard_time_series_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "tensorboard_time_series": {
            "name": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5/timeSeries/sample6"
        }
    }
    request_init["tensorboard_time_series"] = {
        "name": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5/timeSeries/sample6",
        "display_name": "display_name_value",
        "description": "description_value",
        "value_type": 1,
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "etag": "etag_value",
        "plugin_name": "plugin_name_value",
        "plugin_data": b"plugin_data_blob",
        "metadata": {
            "max_step": 865,
            "max_wall_time": {},
            "max_blob_sequence_length": 2525,
        },
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = tensorboard_service.UpdateTensorboardTimeSeriesRequest.meta.fields[
        "tensorboard_time_series"
    ]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init[
        "tensorboard_time_series"
    ].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["tensorboard_time_series"][field])):
                    del request_init["tensorboard_time_series"][field][i][subfield]
            else:
                del request_init["tensorboard_time_series"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gca_tensorboard_time_series.TensorboardTimeSeries(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            value_type=gca_tensorboard_time_series.TensorboardTimeSeries.ValueType.SCALAR,
            etag="etag_value",
            plugin_name="plugin_name_value",
            plugin_data=b"plugin_data_blob",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gca_tensorboard_time_series.TensorboardTimeSeries.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_tensorboard_time_series(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, gca_tensorboard_time_series.TensorboardTimeSeries)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert (
        response.value_type
        == gca_tensorboard_time_series.TensorboardTimeSeries.ValueType.SCALAR
    )
    assert response.etag == "etag_value"
    assert response.plugin_name == "plugin_name_value"
    assert response.plugin_data == b"plugin_data_blob"


def test_update_tensorboard_time_series_rest_required_fields(
    request_type=tensorboard_service.UpdateTensorboardTimeSeriesRequest,
):
    transport_class = transports.TensorboardServiceRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_tensorboard_time_series._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_tensorboard_time_series._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gca_tensorboard_time_series.TensorboardTimeSeries()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "patch",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = gca_tensorboard_time_series.TensorboardTimeSeries.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_tensorboard_time_series(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_tensorboard_time_series_rest_unset_required_fields():
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_tensorboard_time_series._get_unset_required_fields(
        {}
    )
    assert set(unset_fields) == (
        set(("updateMask",))
        & set(
            (
                "updateMask",
                "tensorboardTimeSeries",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_tensorboard_time_series_rest_interceptors(null_interceptor):
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TensorboardServiceRestInterceptor(),
    )
    client = TensorboardServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TensorboardServiceRestInterceptor,
        "post_update_tensorboard_time_series",
    ) as post, mock.patch.object(
        transports.TensorboardServiceRestInterceptor,
        "pre_update_tensorboard_time_series",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tensorboard_service.UpdateTensorboardTimeSeriesRequest.pb(
            tensorboard_service.UpdateTensorboardTimeSeriesRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = (
            gca_tensorboard_time_series.TensorboardTimeSeries.to_json(
                gca_tensorboard_time_series.TensorboardTimeSeries()
            )
        )

        request = tensorboard_service.UpdateTensorboardTimeSeriesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gca_tensorboard_time_series.TensorboardTimeSeries()

        client.update_tensorboard_time_series(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_tensorboard_time_series_rest_bad_request(
    transport: str = "rest",
    request_type=tensorboard_service.UpdateTensorboardTimeSeriesRequest,
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "tensorboard_time_series": {
            "name": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5/timeSeries/sample6"
        }
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_tensorboard_time_series(request)


def test_update_tensorboard_time_series_rest_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gca_tensorboard_time_series.TensorboardTimeSeries()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "tensorboard_time_series": {
                "name": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5/timeSeries/sample6"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            tensorboard_time_series=gca_tensorboard_time_series.TensorboardTimeSeries(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gca_tensorboard_time_series.TensorboardTimeSeries.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_tensorboard_time_series(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{tensorboard_time_series.name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/timeSeries/*}"
            % client.transport._host,
            args[1],
        )


def test_update_tensorboard_time_series_rest_flattened_error(transport: str = "rest"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_tensorboard_time_series(
            tensorboard_service.UpdateTensorboardTimeSeriesRequest(),
            tensorboard_time_series=gca_tensorboard_time_series.TensorboardTimeSeries(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_tensorboard_time_series_rest_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.ListTensorboardTimeSeriesRequest,
        dict,
    ],
)
def test_list_tensorboard_time_series_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tensorboard_service.ListTensorboardTimeSeriesResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = tensorboard_service.ListTensorboardTimeSeriesResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_tensorboard_time_series(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTensorboardTimeSeriesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_tensorboard_time_series_rest_required_fields(
    request_type=tensorboard_service.ListTensorboardTimeSeriesRequest,
):
    transport_class = transports.TensorboardServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_tensorboard_time_series._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_tensorboard_time_series._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "order_by",
            "page_size",
            "page_token",
            "read_mask",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = tensorboard_service.ListTensorboardTimeSeriesResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = tensorboard_service.ListTensorboardTimeSeriesResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_tensorboard_time_series(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_tensorboard_time_series_rest_unset_required_fields():
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_tensorboard_time_series._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "orderBy",
                "pageSize",
                "pageToken",
                "readMask",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_tensorboard_time_series_rest_interceptors(null_interceptor):
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TensorboardServiceRestInterceptor(),
    )
    client = TensorboardServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TensorboardServiceRestInterceptor,
        "post_list_tensorboard_time_series",
    ) as post, mock.patch.object(
        transports.TensorboardServiceRestInterceptor, "pre_list_tensorboard_time_series"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tensorboard_service.ListTensorboardTimeSeriesRequest.pb(
            tensorboard_service.ListTensorboardTimeSeriesRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = (
            tensorboard_service.ListTensorboardTimeSeriesResponse.to_json(
                tensorboard_service.ListTensorboardTimeSeriesResponse()
            )
        )

        request = tensorboard_service.ListTensorboardTimeSeriesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = tensorboard_service.ListTensorboardTimeSeriesResponse()

        client.list_tensorboard_time_series(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_tensorboard_time_series_rest_bad_request(
    transport: str = "rest",
    request_type=tensorboard_service.ListTensorboardTimeSeriesRequest,
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_tensorboard_time_series(request)


def test_list_tensorboard_time_series_rest_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tensorboard_service.ListTensorboardTimeSeriesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = tensorboard_service.ListTensorboardTimeSeriesResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_tensorboard_time_series(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/tensorboards/*/experiments/*/runs/*}/timeSeries"
            % client.transport._host,
            args[1],
        )


def test_list_tensorboard_time_series_rest_flattened_error(transport: str = "rest"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_tensorboard_time_series(
            tensorboard_service.ListTensorboardTimeSeriesRequest(),
            parent="parent_value",
        )


def test_list_tensorboard_time_series_rest_pager(transport: str = "rest"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            tensorboard_service.ListTensorboardTimeSeriesResponse(
                tensorboard_time_series=[
                    tensorboard_time_series.TensorboardTimeSeries(),
                    tensorboard_time_series.TensorboardTimeSeries(),
                    tensorboard_time_series.TensorboardTimeSeries(),
                ],
                next_page_token="abc",
            ),
            tensorboard_service.ListTensorboardTimeSeriesResponse(
                tensorboard_time_series=[],
                next_page_token="def",
            ),
            tensorboard_service.ListTensorboardTimeSeriesResponse(
                tensorboard_time_series=[
                    tensorboard_time_series.TensorboardTimeSeries(),
                ],
                next_page_token="ghi",
            ),
            tensorboard_service.ListTensorboardTimeSeriesResponse(
                tensorboard_time_series=[
                    tensorboard_time_series.TensorboardTimeSeries(),
                    tensorboard_time_series.TensorboardTimeSeries(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            tensorboard_service.ListTensorboardTimeSeriesResponse.to_json(x)
            for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5"
        }

        pager = client.list_tensorboard_time_series(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, tensorboard_time_series.TensorboardTimeSeries)
            for i in results
        )

        pages = list(client.list_tensorboard_time_series(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.DeleteTensorboardTimeSeriesRequest,
        dict,
    ],
)
def test_delete_tensorboard_time_series_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5/timeSeries/sample6"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_tensorboard_time_series(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_tensorboard_time_series_rest_required_fields(
    request_type=tensorboard_service.DeleteTensorboardTimeSeriesRequest,
):
    transport_class = transports.TensorboardServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_tensorboard_time_series._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_tensorboard_time_series._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "delete",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_tensorboard_time_series(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_tensorboard_time_series_rest_unset_required_fields():
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_tensorboard_time_series._get_unset_required_fields(
        {}
    )
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_tensorboard_time_series_rest_interceptors(null_interceptor):
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TensorboardServiceRestInterceptor(),
    )
    client = TensorboardServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.TensorboardServiceRestInterceptor,
        "post_delete_tensorboard_time_series",
    ) as post, mock.patch.object(
        transports.TensorboardServiceRestInterceptor,
        "pre_delete_tensorboard_time_series",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tensorboard_service.DeleteTensorboardTimeSeriesRequest.pb(
            tensorboard_service.DeleteTensorboardTimeSeriesRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = tensorboard_service.DeleteTensorboardTimeSeriesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_tensorboard_time_series(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_tensorboard_time_series_rest_bad_request(
    transport: str = "rest",
    request_type=tensorboard_service.DeleteTensorboardTimeSeriesRequest,
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5/timeSeries/sample6"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_tensorboard_time_series(request)


def test_delete_tensorboard_time_series_rest_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5/timeSeries/sample6"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_tensorboard_time_series(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/timeSeries/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_tensorboard_time_series_rest_flattened_error(transport: str = "rest"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_tensorboard_time_series(
            tensorboard_service.DeleteTensorboardTimeSeriesRequest(),
            name="name_value",
        )


def test_delete_tensorboard_time_series_rest_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.BatchReadTensorboardTimeSeriesDataRequest,
        dict,
    ],
)
def test_batch_read_tensorboard_time_series_data_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "tensorboard": "projects/sample1/locations/sample2/tensorboards/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tensorboard_service.BatchReadTensorboardTimeSeriesDataResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = (
            tensorboard_service.BatchReadTensorboardTimeSeriesDataResponse.pb(
                return_value
            )
        )
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.batch_read_tensorboard_time_series_data(request)

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, tensorboard_service.BatchReadTensorboardTimeSeriesDataResponse
    )


def test_batch_read_tensorboard_time_series_data_rest_required_fields(
    request_type=tensorboard_service.BatchReadTensorboardTimeSeriesDataRequest,
):
    transport_class = transports.TensorboardServiceRestTransport

    request_init = {}
    request_init["tensorboard"] = ""
    request_init["time_series"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped
    assert "timeSeries" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).batch_read_tensorboard_time_series_data._get_unset_required_fields(
        jsonified_request
    )
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "timeSeries" in jsonified_request
    assert jsonified_request["timeSeries"] == request_init["time_series"]

    jsonified_request["tensorboard"] = "tensorboard_value"
    jsonified_request["timeSeries"] = "time_series_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).batch_read_tensorboard_time_series_data._get_unset_required_fields(
        jsonified_request
    )
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("time_series",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "tensorboard" in jsonified_request
    assert jsonified_request["tensorboard"] == "tensorboard_value"
    assert "timeSeries" in jsonified_request
    assert jsonified_request["timeSeries"] == "time_series_value"

    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = tensorboard_service.BatchReadTensorboardTimeSeriesDataResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = (
                tensorboard_service.BatchReadTensorboardTimeSeriesDataResponse.pb(
                    return_value
                )
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.batch_read_tensorboard_time_series_data(request)

            expected_params = [
                (
                    "timeSeries",
                    "",
                ),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_batch_read_tensorboard_time_series_data_rest_unset_required_fields():
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = (
        transport.batch_read_tensorboard_time_series_data._get_unset_required_fields({})
    )
    assert set(unset_fields) == (
        set(("timeSeries",))
        & set(
            (
                "tensorboard",
                "timeSeries",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_batch_read_tensorboard_time_series_data_rest_interceptors(null_interceptor):
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TensorboardServiceRestInterceptor(),
    )
    client = TensorboardServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TensorboardServiceRestInterceptor,
        "post_batch_read_tensorboard_time_series_data",
    ) as post, mock.patch.object(
        transports.TensorboardServiceRestInterceptor,
        "pre_batch_read_tensorboard_time_series_data",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tensorboard_service.BatchReadTensorboardTimeSeriesDataRequest.pb(
            tensorboard_service.BatchReadTensorboardTimeSeriesDataRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = (
            tensorboard_service.BatchReadTensorboardTimeSeriesDataResponse.to_json(
                tensorboard_service.BatchReadTensorboardTimeSeriesDataResponse()
            )
        )

        request = tensorboard_service.BatchReadTensorboardTimeSeriesDataRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = (
            tensorboard_service.BatchReadTensorboardTimeSeriesDataResponse()
        )

        client.batch_read_tensorboard_time_series_data(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_batch_read_tensorboard_time_series_data_rest_bad_request(
    transport: str = "rest",
    request_type=tensorboard_service.BatchReadTensorboardTimeSeriesDataRequest,
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "tensorboard": "projects/sample1/locations/sample2/tensorboards/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.batch_read_tensorboard_time_series_data(request)


def test_batch_read_tensorboard_time_series_data_rest_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tensorboard_service.BatchReadTensorboardTimeSeriesDataResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "tensorboard": "projects/sample1/locations/sample2/tensorboards/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            tensorboard="tensorboard_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = (
            tensorboard_service.BatchReadTensorboardTimeSeriesDataResponse.pb(
                return_value
            )
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.batch_read_tensorboard_time_series_data(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{tensorboard=projects/*/locations/*/tensorboards/*}:batchRead"
            % client.transport._host,
            args[1],
        )


def test_batch_read_tensorboard_time_series_data_rest_flattened_error(
    transport: str = "rest",
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.batch_read_tensorboard_time_series_data(
            tensorboard_service.BatchReadTensorboardTimeSeriesDataRequest(),
            tensorboard="tensorboard_value",
        )


def test_batch_read_tensorboard_time_series_data_rest_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.ReadTensorboardTimeSeriesDataRequest,
        dict,
    ],
)
def test_read_tensorboard_time_series_data_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "tensorboard_time_series": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5/timeSeries/sample6"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tensorboard_service.ReadTensorboardTimeSeriesDataResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = tensorboard_service.ReadTensorboardTimeSeriesDataResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.read_tensorboard_time_series_data(request)

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, tensorboard_service.ReadTensorboardTimeSeriesDataResponse
    )


def test_read_tensorboard_time_series_data_rest_required_fields(
    request_type=tensorboard_service.ReadTensorboardTimeSeriesDataRequest,
):
    transport_class = transports.TensorboardServiceRestTransport

    request_init = {}
    request_init["tensorboard_time_series"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).read_tensorboard_time_series_data._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["tensorboardTimeSeries"] = "tensorboard_time_series_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).read_tensorboard_time_series_data._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "max_data_points",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "tensorboardTimeSeries" in jsonified_request
    assert jsonified_request["tensorboardTimeSeries"] == "tensorboard_time_series_value"

    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = tensorboard_service.ReadTensorboardTimeSeriesDataResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = tensorboard_service.ReadTensorboardTimeSeriesDataResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.read_tensorboard_time_series_data(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_read_tensorboard_time_series_data_rest_unset_required_fields():
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = (
        transport.read_tensorboard_time_series_data._get_unset_required_fields({})
    )
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "maxDataPoints",
            )
        )
        & set(("tensorboardTimeSeries",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_read_tensorboard_time_series_data_rest_interceptors(null_interceptor):
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TensorboardServiceRestInterceptor(),
    )
    client = TensorboardServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TensorboardServiceRestInterceptor,
        "post_read_tensorboard_time_series_data",
    ) as post, mock.patch.object(
        transports.TensorboardServiceRestInterceptor,
        "pre_read_tensorboard_time_series_data",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tensorboard_service.ReadTensorboardTimeSeriesDataRequest.pb(
            tensorboard_service.ReadTensorboardTimeSeriesDataRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = (
            tensorboard_service.ReadTensorboardTimeSeriesDataResponse.to_json(
                tensorboard_service.ReadTensorboardTimeSeriesDataResponse()
            )
        )

        request = tensorboard_service.ReadTensorboardTimeSeriesDataRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = tensorboard_service.ReadTensorboardTimeSeriesDataResponse()

        client.read_tensorboard_time_series_data(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_read_tensorboard_time_series_data_rest_bad_request(
    transport: str = "rest",
    request_type=tensorboard_service.ReadTensorboardTimeSeriesDataRequest,
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "tensorboard_time_series": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5/timeSeries/sample6"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.read_tensorboard_time_series_data(request)


def test_read_tensorboard_time_series_data_rest_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tensorboard_service.ReadTensorboardTimeSeriesDataResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "tensorboard_time_series": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5/timeSeries/sample6"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            tensorboard_time_series="tensorboard_time_series_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = tensorboard_service.ReadTensorboardTimeSeriesDataResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.read_tensorboard_time_series_data(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{tensorboard_time_series=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/timeSeries/*}:read"
            % client.transport._host,
            args[1],
        )


def test_read_tensorboard_time_series_data_rest_flattened_error(
    transport: str = "rest",
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.read_tensorboard_time_series_data(
            tensorboard_service.ReadTensorboardTimeSeriesDataRequest(),
            tensorboard_time_series="tensorboard_time_series_value",
        )


def test_read_tensorboard_time_series_data_rest_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.ReadTensorboardBlobDataRequest,
        dict,
    ],
)
def test_read_tensorboard_blob_data_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "time_series": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5/timeSeries/sample6"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tensorboard_service.ReadTensorboardBlobDataResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = tensorboard_service.ReadTensorboardBlobDataResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)

        json_return_value = "[{}]".format(json_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        with mock.patch.object(response_value, "iter_content") as iter_content:
            iter_content.return_value = iter(json_return_value)
            response = client.read_tensorboard_blob_data(request)

    assert isinstance(response, Iterable)
    response = next(response)

    # Establish that the response is the type that we expect.
    assert isinstance(response, tensorboard_service.ReadTensorboardBlobDataResponse)


def test_read_tensorboard_blob_data_rest_required_fields(
    request_type=tensorboard_service.ReadTensorboardBlobDataRequest,
):
    transport_class = transports.TensorboardServiceRestTransport

    request_init = {}
    request_init["time_series"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).read_tensorboard_blob_data._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["timeSeries"] = "time_series_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).read_tensorboard_blob_data._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("blob_ids",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "timeSeries" in jsonified_request
    assert jsonified_request["timeSeries"] == "time_series_value"

    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = tensorboard_service.ReadTensorboardBlobDataResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = tensorboard_service.ReadTensorboardBlobDataResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)
            json_return_value = "[{}]".format(json_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            with mock.patch.object(response_value, "iter_content") as iter_content:
                iter_content.return_value = iter(json_return_value)
                response = client.read_tensorboard_blob_data(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_read_tensorboard_blob_data_rest_unset_required_fields():
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.read_tensorboard_blob_data._get_unset_required_fields({})
    assert set(unset_fields) == (set(("blobIds",)) & set(("timeSeries",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_read_tensorboard_blob_data_rest_interceptors(null_interceptor):
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TensorboardServiceRestInterceptor(),
    )
    client = TensorboardServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TensorboardServiceRestInterceptor, "post_read_tensorboard_blob_data"
    ) as post, mock.patch.object(
        transports.TensorboardServiceRestInterceptor, "pre_read_tensorboard_blob_data"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tensorboard_service.ReadTensorboardBlobDataRequest.pb(
            tensorboard_service.ReadTensorboardBlobDataRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = (
            tensorboard_service.ReadTensorboardBlobDataResponse.to_json(
                tensorboard_service.ReadTensorboardBlobDataResponse()
            )
        )
        req.return_value._content = "[{}]".format(req.return_value._content)

        request = tensorboard_service.ReadTensorboardBlobDataRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = tensorboard_service.ReadTensorboardBlobDataResponse()

        client.read_tensorboard_blob_data(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_read_tensorboard_blob_data_rest_bad_request(
    transport: str = "rest",
    request_type=tensorboard_service.ReadTensorboardBlobDataRequest,
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "time_series": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5/timeSeries/sample6"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.read_tensorboard_blob_data(request)


def test_read_tensorboard_blob_data_rest_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tensorboard_service.ReadTensorboardBlobDataResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "time_series": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5/timeSeries/sample6"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            time_series="time_series_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = tensorboard_service.ReadTensorboardBlobDataResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        json_return_value = "[{}]".format(json_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        with mock.patch.object(response_value, "iter_content") as iter_content:
            iter_content.return_value = iter(json_return_value)
            client.read_tensorboard_blob_data(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{time_series=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/timeSeries/*}:readBlobData"
            % client.transport._host,
            args[1],
        )


def test_read_tensorboard_blob_data_rest_flattened_error(transport: str = "rest"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.read_tensorboard_blob_data(
            tensorboard_service.ReadTensorboardBlobDataRequest(),
            time_series="time_series_value",
        )


def test_read_tensorboard_blob_data_rest_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.WriteTensorboardExperimentDataRequest,
        dict,
    ],
)
def test_write_tensorboard_experiment_data_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "tensorboard_experiment": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tensorboard_service.WriteTensorboardExperimentDataResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = tensorboard_service.WriteTensorboardExperimentDataResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.write_tensorboard_experiment_data(request)

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, tensorboard_service.WriteTensorboardExperimentDataResponse
    )


def test_write_tensorboard_experiment_data_rest_required_fields(
    request_type=tensorboard_service.WriteTensorboardExperimentDataRequest,
):
    transport_class = transports.TensorboardServiceRestTransport

    request_init = {}
    request_init["tensorboard_experiment"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).write_tensorboard_experiment_data._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["tensorboardExperiment"] = "tensorboard_experiment_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).write_tensorboard_experiment_data._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "tensorboardExperiment" in jsonified_request
    assert jsonified_request["tensorboardExperiment"] == "tensorboard_experiment_value"

    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = tensorboard_service.WriteTensorboardExperimentDataResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = (
                tensorboard_service.WriteTensorboardExperimentDataResponse.pb(
                    return_value
                )
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.write_tensorboard_experiment_data(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_write_tensorboard_experiment_data_rest_unset_required_fields():
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = (
        transport.write_tensorboard_experiment_data._get_unset_required_fields({})
    )
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "tensorboardExperiment",
                "writeRunDataRequests",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_write_tensorboard_experiment_data_rest_interceptors(null_interceptor):
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TensorboardServiceRestInterceptor(),
    )
    client = TensorboardServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TensorboardServiceRestInterceptor,
        "post_write_tensorboard_experiment_data",
    ) as post, mock.patch.object(
        transports.TensorboardServiceRestInterceptor,
        "pre_write_tensorboard_experiment_data",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tensorboard_service.WriteTensorboardExperimentDataRequest.pb(
            tensorboard_service.WriteTensorboardExperimentDataRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = (
            tensorboard_service.WriteTensorboardExperimentDataResponse.to_json(
                tensorboard_service.WriteTensorboardExperimentDataResponse()
            )
        )

        request = tensorboard_service.WriteTensorboardExperimentDataRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = tensorboard_service.WriteTensorboardExperimentDataResponse()

        client.write_tensorboard_experiment_data(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_write_tensorboard_experiment_data_rest_bad_request(
    transport: str = "rest",
    request_type=tensorboard_service.WriteTensorboardExperimentDataRequest,
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "tensorboard_experiment": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.write_tensorboard_experiment_data(request)


def test_write_tensorboard_experiment_data_rest_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tensorboard_service.WriteTensorboardExperimentDataResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "tensorboard_experiment": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            tensorboard_experiment="tensorboard_experiment_value",
            write_run_data_requests=[
                tensorboard_service.WriteTensorboardRunDataRequest(
                    tensorboard_run="tensorboard_run_value"
                )
            ],
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = tensorboard_service.WriteTensorboardExperimentDataResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.write_tensorboard_experiment_data(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{tensorboard_experiment=projects/*/locations/*/tensorboards/*/experiments/*}:write"
            % client.transport._host,
            args[1],
        )


def test_write_tensorboard_experiment_data_rest_flattened_error(
    transport: str = "rest",
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.write_tensorboard_experiment_data(
            tensorboard_service.WriteTensorboardExperimentDataRequest(),
            tensorboard_experiment="tensorboard_experiment_value",
            write_run_data_requests=[
                tensorboard_service.WriteTensorboardRunDataRequest(
                    tensorboard_run="tensorboard_run_value"
                )
            ],
        )


def test_write_tensorboard_experiment_data_rest_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.WriteTensorboardRunDataRequest,
        dict,
    ],
)
def test_write_tensorboard_run_data_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "tensorboard_run": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tensorboard_service.WriteTensorboardRunDataResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = tensorboard_service.WriteTensorboardRunDataResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.write_tensorboard_run_data(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, tensorboard_service.WriteTensorboardRunDataResponse)


def test_write_tensorboard_run_data_rest_required_fields(
    request_type=tensorboard_service.WriteTensorboardRunDataRequest,
):
    transport_class = transports.TensorboardServiceRestTransport

    request_init = {}
    request_init["tensorboard_run"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).write_tensorboard_run_data._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["tensorboardRun"] = "tensorboard_run_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).write_tensorboard_run_data._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "tensorboardRun" in jsonified_request
    assert jsonified_request["tensorboardRun"] == "tensorboard_run_value"

    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = tensorboard_service.WriteTensorboardRunDataResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = tensorboard_service.WriteTensorboardRunDataResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.write_tensorboard_run_data(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_write_tensorboard_run_data_rest_unset_required_fields():
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.write_tensorboard_run_data._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "tensorboardRun",
                "timeSeriesData",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_write_tensorboard_run_data_rest_interceptors(null_interceptor):
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TensorboardServiceRestInterceptor(),
    )
    client = TensorboardServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TensorboardServiceRestInterceptor, "post_write_tensorboard_run_data"
    ) as post, mock.patch.object(
        transports.TensorboardServiceRestInterceptor, "pre_write_tensorboard_run_data"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tensorboard_service.WriteTensorboardRunDataRequest.pb(
            tensorboard_service.WriteTensorboardRunDataRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = (
            tensorboard_service.WriteTensorboardRunDataResponse.to_json(
                tensorboard_service.WriteTensorboardRunDataResponse()
            )
        )

        request = tensorboard_service.WriteTensorboardRunDataRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = tensorboard_service.WriteTensorboardRunDataResponse()

        client.write_tensorboard_run_data(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_write_tensorboard_run_data_rest_bad_request(
    transport: str = "rest",
    request_type=tensorboard_service.WriteTensorboardRunDataRequest,
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "tensorboard_run": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.write_tensorboard_run_data(request)


def test_write_tensorboard_run_data_rest_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tensorboard_service.WriteTensorboardRunDataResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "tensorboard_run": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            tensorboard_run="tensorboard_run_value",
            time_series_data=[
                tensorboard_data.TimeSeriesData(
                    tensorboard_time_series_id="tensorboard_time_series_id_value"
                )
            ],
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = tensorboard_service.WriteTensorboardRunDataResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.write_tensorboard_run_data(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{tensorboard_run=projects/*/locations/*/tensorboards/*/experiments/*/runs/*}:write"
            % client.transport._host,
            args[1],
        )


def test_write_tensorboard_run_data_rest_flattened_error(transport: str = "rest"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.write_tensorboard_run_data(
            tensorboard_service.WriteTensorboardRunDataRequest(),
            tensorboard_run="tensorboard_run_value",
            time_series_data=[
                tensorboard_data.TimeSeriesData(
                    tensorboard_time_series_id="tensorboard_time_series_id_value"
                )
            ],
        )


def test_write_tensorboard_run_data_rest_error():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        tensorboard_service.ExportTensorboardTimeSeriesDataRequest,
        dict,
    ],
)
def test_export_tensorboard_time_series_data_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "tensorboard_time_series": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5/timeSeries/sample6"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tensorboard_service.ExportTensorboardTimeSeriesDataResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = tensorboard_service.ExportTensorboardTimeSeriesDataResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.export_tensorboard_time_series_data(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ExportTensorboardTimeSeriesDataPager)
    assert response.next_page_token == "next_page_token_value"


def test_export_tensorboard_time_series_data_rest_required_fields(
    request_type=tensorboard_service.ExportTensorboardTimeSeriesDataRequest,
):
    transport_class = transports.TensorboardServiceRestTransport

    request_init = {}
    request_init["tensorboard_time_series"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).export_tensorboard_time_series_data._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["tensorboardTimeSeries"] = "tensorboard_time_series_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).export_tensorboard_time_series_data._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "tensorboardTimeSeries" in jsonified_request
    assert jsonified_request["tensorboardTimeSeries"] == "tensorboard_time_series_value"

    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = tensorboard_service.ExportTensorboardTimeSeriesDataResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = (
                tensorboard_service.ExportTensorboardTimeSeriesDataResponse.pb(
                    return_value
                )
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.export_tensorboard_time_series_data(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_export_tensorboard_time_series_data_rest_unset_required_fields():
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = (
        transport.export_tensorboard_time_series_data._get_unset_required_fields({})
    )
    assert set(unset_fields) == (set(()) & set(("tensorboardTimeSeries",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_export_tensorboard_time_series_data_rest_interceptors(null_interceptor):
    transport = transports.TensorboardServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TensorboardServiceRestInterceptor(),
    )
    client = TensorboardServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TensorboardServiceRestInterceptor,
        "post_export_tensorboard_time_series_data",
    ) as post, mock.patch.object(
        transports.TensorboardServiceRestInterceptor,
        "pre_export_tensorboard_time_series_data",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tensorboard_service.ExportTensorboardTimeSeriesDataRequest.pb(
            tensorboard_service.ExportTensorboardTimeSeriesDataRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = (
            tensorboard_service.ExportTensorboardTimeSeriesDataResponse.to_json(
                tensorboard_service.ExportTensorboardTimeSeriesDataResponse()
            )
        )

        request = tensorboard_service.ExportTensorboardTimeSeriesDataRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = (
            tensorboard_service.ExportTensorboardTimeSeriesDataResponse()
        )

        client.export_tensorboard_time_series_data(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_export_tensorboard_time_series_data_rest_bad_request(
    transport: str = "rest",
    request_type=tensorboard_service.ExportTensorboardTimeSeriesDataRequest,
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "tensorboard_time_series": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5/timeSeries/sample6"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.export_tensorboard_time_series_data(request)


def test_export_tensorboard_time_series_data_rest_flattened():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tensorboard_service.ExportTensorboardTimeSeriesDataResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "tensorboard_time_series": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5/timeSeries/sample6"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            tensorboard_time_series="tensorboard_time_series_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = tensorboard_service.ExportTensorboardTimeSeriesDataResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.export_tensorboard_time_series_data(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{tensorboard_time_series=projects/*/locations/*/tensorboards/*/experiments/*/runs/*/timeSeries/*}:exportTensorboardTimeSeries"
            % client.transport._host,
            args[1],
        )


def test_export_tensorboard_time_series_data_rest_flattened_error(
    transport: str = "rest",
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.export_tensorboard_time_series_data(
            tensorboard_service.ExportTensorboardTimeSeriesDataRequest(),
            tensorboard_time_series="tensorboard_time_series_value",
        )


def test_export_tensorboard_time_series_data_rest_pager(transport: str = "rest"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            tensorboard_service.ExportTensorboardTimeSeriesDataResponse(
                time_series_data_points=[
                    tensorboard_data.TimeSeriesDataPoint(),
                    tensorboard_data.TimeSeriesDataPoint(),
                    tensorboard_data.TimeSeriesDataPoint(),
                ],
                next_page_token="abc",
            ),
            tensorboard_service.ExportTensorboardTimeSeriesDataResponse(
                time_series_data_points=[],
                next_page_token="def",
            ),
            tensorboard_service.ExportTensorboardTimeSeriesDataResponse(
                time_series_data_points=[
                    tensorboard_data.TimeSeriesDataPoint(),
                ],
                next_page_token="ghi",
            ),
            tensorboard_service.ExportTensorboardTimeSeriesDataResponse(
                time_series_data_points=[
                    tensorboard_data.TimeSeriesDataPoint(),
                    tensorboard_data.TimeSeriesDataPoint(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            tensorboard_service.ExportTensorboardTimeSeriesDataResponse.to_json(x)
            for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "tensorboard_time_series": "projects/sample1/locations/sample2/tensorboards/sample3/experiments/sample4/runs/sample5/timeSeries/sample6"
        }

        pager = client.export_tensorboard_time_series_data(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, tensorboard_data.TimeSeriesDataPoint) for i in results)

        pages = list(
            client.export_tensorboard_time_series_data(request=sample_request).pages
        )
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.TensorboardServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = TensorboardServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.TensorboardServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = TensorboardServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.TensorboardServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = TensorboardServiceClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = TensorboardServiceClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.TensorboardServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = TensorboardServiceClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.TensorboardServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = TensorboardServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.TensorboardServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.TensorboardServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.TensorboardServiceGrpcTransport,
        transports.TensorboardServiceGrpcAsyncIOTransport,
        transports.TensorboardServiceRestTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "rest",
    ],
)
def test_transport_kind(transport_name):
    transport = TensorboardServiceClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.TensorboardServiceGrpcTransport,
    )


def test_tensorboard_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.TensorboardServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_tensorboard_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.aiplatform_v1.services.tensorboard_service.transports.TensorboardServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.TensorboardServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_tensorboard",
        "get_tensorboard",
        "update_tensorboard",
        "list_tensorboards",
        "delete_tensorboard",
        "read_tensorboard_usage",
        "read_tensorboard_size",
        "create_tensorboard_experiment",
        "get_tensorboard_experiment",
        "update_tensorboard_experiment",
        "list_tensorboard_experiments",
        "delete_tensorboard_experiment",
        "create_tensorboard_run",
        "batch_create_tensorboard_runs",
        "get_tensorboard_run",
        "update_tensorboard_run",
        "list_tensorboard_runs",
        "delete_tensorboard_run",
        "batch_create_tensorboard_time_series",
        "create_tensorboard_time_series",
        "get_tensorboard_time_series",
        "update_tensorboard_time_series",
        "list_tensorboard_time_series",
        "delete_tensorboard_time_series",
        "batch_read_tensorboard_time_series_data",
        "read_tensorboard_time_series_data",
        "read_tensorboard_blob_data",
        "write_tensorboard_experiment_data",
        "write_tensorboard_run_data",
        "export_tensorboard_time_series_data",
        "set_iam_policy",
        "get_iam_policy",
        "test_iam_permissions",
        "get_location",
        "list_locations",
        "get_operation",
        "wait_operation",
        "cancel_operation",
        "delete_operation",
        "list_operations",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client

    # Catch all for all remaining methods and properties
    remainder = [
        "kind",
    ]
    for r in remainder:
        with pytest.raises(NotImplementedError):
            getattr(transport, r)()


def test_tensorboard_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.aiplatform_v1.services.tensorboard_service.transports.TensorboardServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.TensorboardServiceTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
            ),
            quota_project_id="octopus",
        )


def test_tensorboard_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.aiplatform_v1.services.tensorboard_service.transports.TensorboardServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.TensorboardServiceTransport()
        adc.assert_called_once()


def test_tensorboard_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        TensorboardServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
            ),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.TensorboardServiceGrpcTransport,
        transports.TensorboardServiceGrpcAsyncIOTransport,
    ],
)
def test_tensorboard_service_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.TensorboardServiceGrpcTransport,
        transports.TensorboardServiceGrpcAsyncIOTransport,
        transports.TensorboardServiceRestTransport,
    ],
)
def test_tensorboard_service_transport_auth_gdch_credentials(transport_class):
    host = "https://language.com"
    api_audience_tests = [None, "https://language2.com"]
    api_audience_expect = [host, "https://language2.com"]
    for t, e in zip(api_audience_tests, api_audience_expect):
        with mock.patch.object(google.auth, "default", autospec=True) as adc:
            gdch_mock = mock.MagicMock()
            type(gdch_mock).with_gdch_audience = mock.PropertyMock(
                return_value=gdch_mock
            )
            adc.return_value = (gdch_mock, None)
            transport_class(host=host, api_audience=t)
            gdch_mock.with_gdch_audience.assert_called_once_with(e)


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.TensorboardServiceGrpcTransport, grpc_helpers),
        (transports.TensorboardServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_tensorboard_service_transport_create_channel(transport_class, grpc_helpers):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel", autospec=True
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        adc.return_value = (creds, None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])

        create_channel.assert_called_with(
            "aiplatform.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
            ),
            scopes=["1", "2"],
            default_host="aiplatform.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.TensorboardServiceGrpcTransport,
        transports.TensorboardServiceGrpcAsyncIOTransport,
    ],
)
def test_tensorboard_service_grpc_transport_client_cert_source_for_mtls(
    transport_class,
):
    cred = ga_credentials.AnonymousCredentials()

    # Check ssl_channel_credentials is used if provided.
    with mock.patch.object(transport_class, "create_channel") as mock_create_channel:
        mock_ssl_channel_creds = mock.Mock()
        transport_class(
            host="squid.clam.whelk",
            credentials=cred,
            ssl_channel_credentials=mock_ssl_channel_creds,
        )
        mock_create_channel.assert_called_once_with(
            "squid.clam.whelk:443",
            credentials=cred,
            credentials_file=None,
            scopes=None,
            ssl_credentials=mock_ssl_channel_creds,
            quota_project_id=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )

    # Check if ssl_channel_credentials is not provided, then client_cert_source_for_mtls
    # is used.
    with mock.patch.object(transport_class, "create_channel", return_value=mock.Mock()):
        with mock.patch("grpc.ssl_channel_credentials") as mock_ssl_cred:
            transport_class(
                credentials=cred,
                client_cert_source_for_mtls=client_cert_source_callback,
            )
            expected_cert, expected_key = client_cert_source_callback()
            mock_ssl_cred.assert_called_once_with(
                certificate_chain=expected_cert, private_key=expected_key
            )


def test_tensorboard_service_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.TensorboardServiceRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


def test_tensorboard_service_rest_lro_client():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.AbstractOperationsClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_tensorboard_service_host_no_port(transport_name):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="aiplatform.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "aiplatform.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://aiplatform.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_tensorboard_service_host_with_port(transport_name):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="aiplatform.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "aiplatform.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://aiplatform.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_tensorboard_service_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = TensorboardServiceClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = TensorboardServiceClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.create_tensorboard._session
    session2 = client2.transport.create_tensorboard._session
    assert session1 != session2
    session1 = client1.transport.get_tensorboard._session
    session2 = client2.transport.get_tensorboard._session
    assert session1 != session2
    session1 = client1.transport.update_tensorboard._session
    session2 = client2.transport.update_tensorboard._session
    assert session1 != session2
    session1 = client1.transport.list_tensorboards._session
    session2 = client2.transport.list_tensorboards._session
    assert session1 != session2
    session1 = client1.transport.delete_tensorboard._session
    session2 = client2.transport.delete_tensorboard._session
    assert session1 != session2
    session1 = client1.transport.read_tensorboard_usage._session
    session2 = client2.transport.read_tensorboard_usage._session
    assert session1 != session2
    session1 = client1.transport.read_tensorboard_size._session
    session2 = client2.transport.read_tensorboard_size._session
    assert session1 != session2
    session1 = client1.transport.create_tensorboard_experiment._session
    session2 = client2.transport.create_tensorboard_experiment._session
    assert session1 != session2
    session1 = client1.transport.get_tensorboard_experiment._session
    session2 = client2.transport.get_tensorboard_experiment._session
    assert session1 != session2
    session1 = client1.transport.update_tensorboard_experiment._session
    session2 = client2.transport.update_tensorboard_experiment._session
    assert session1 != session2
    session1 = client1.transport.list_tensorboard_experiments._session
    session2 = client2.transport.list_tensorboard_experiments._session
    assert session1 != session2
    session1 = client1.transport.delete_tensorboard_experiment._session
    session2 = client2.transport.delete_tensorboard_experiment._session
    assert session1 != session2
    session1 = client1.transport.create_tensorboard_run._session
    session2 = client2.transport.create_tensorboard_run._session
    assert session1 != session2
    session1 = client1.transport.batch_create_tensorboard_runs._session
    session2 = client2.transport.batch_create_tensorboard_runs._session
    assert session1 != session2
    session1 = client1.transport.get_tensorboard_run._session
    session2 = client2.transport.get_tensorboard_run._session
    assert session1 != session2
    session1 = client1.transport.update_tensorboard_run._session
    session2 = client2.transport.update_tensorboard_run._session
    assert session1 != session2
    session1 = client1.transport.list_tensorboard_runs._session
    session2 = client2.transport.list_tensorboard_runs._session
    assert session1 != session2
    session1 = client1.transport.delete_tensorboard_run._session
    session2 = client2.transport.delete_tensorboard_run._session
    assert session1 != session2
    session1 = client1.transport.batch_create_tensorboard_time_series._session
    session2 = client2.transport.batch_create_tensorboard_time_series._session
    assert session1 != session2
    session1 = client1.transport.create_tensorboard_time_series._session
    session2 = client2.transport.create_tensorboard_time_series._session
    assert session1 != session2
    session1 = client1.transport.get_tensorboard_time_series._session
    session2 = client2.transport.get_tensorboard_time_series._session
    assert session1 != session2
    session1 = client1.transport.update_tensorboard_time_series._session
    session2 = client2.transport.update_tensorboard_time_series._session
    assert session1 != session2
    session1 = client1.transport.list_tensorboard_time_series._session
    session2 = client2.transport.list_tensorboard_time_series._session
    assert session1 != session2
    session1 = client1.transport.delete_tensorboard_time_series._session
    session2 = client2.transport.delete_tensorboard_time_series._session
    assert session1 != session2
    session1 = client1.transport.batch_read_tensorboard_time_series_data._session
    session2 = client2.transport.batch_read_tensorboard_time_series_data._session
    assert session1 != session2
    session1 = client1.transport.read_tensorboard_time_series_data._session
    session2 = client2.transport.read_tensorboard_time_series_data._session
    assert session1 != session2
    session1 = client1.transport.read_tensorboard_blob_data._session
    session2 = client2.transport.read_tensorboard_blob_data._session
    assert session1 != session2
    session1 = client1.transport.write_tensorboard_experiment_data._session
    session2 = client2.transport.write_tensorboard_experiment_data._session
    assert session1 != session2
    session1 = client1.transport.write_tensorboard_run_data._session
    session2 = client2.transport.write_tensorboard_run_data._session
    assert session1 != session2
    session1 = client1.transport.export_tensorboard_time_series_data._session
    session2 = client2.transport.export_tensorboard_time_series_data._session
    assert session1 != session2


def test_tensorboard_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.TensorboardServiceGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_tensorboard_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.TensorboardServiceGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.TensorboardServiceGrpcTransport,
        transports.TensorboardServiceGrpcAsyncIOTransport,
    ],
)
def test_tensorboard_service_transport_channel_mtls_with_client_cert_source(
    transport_class,
):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = ga_credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(google.auth, "default") as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.TensorboardServiceGrpcTransport,
        transports.TensorboardServiceGrpcAsyncIOTransport,
    ],
)
def test_tensorboard_service_transport_channel_mtls_with_adc(transport_class):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_tensorboard_service_grpc_lro_client():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.OperationsClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_tensorboard_service_grpc_lro_async_client():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.OperationsAsyncClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_tensorboard_path():
    project = "squid"
    location = "clam"
    tensorboard = "whelk"
    expected = (
        "projects/{project}/locations/{location}/tensorboards/{tensorboard}".format(
            project=project,
            location=location,
            tensorboard=tensorboard,
        )
    )
    actual = TensorboardServiceClient.tensorboard_path(project, location, tensorboard)
    assert expected == actual


def test_parse_tensorboard_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "tensorboard": "nudibranch",
    }
    path = TensorboardServiceClient.tensorboard_path(**expected)

    # Check that the path construction is reversible.
    actual = TensorboardServiceClient.parse_tensorboard_path(path)
    assert expected == actual


def test_tensorboard_experiment_path():
    project = "cuttlefish"
    location = "mussel"
    tensorboard = "winkle"
    experiment = "nautilus"
    expected = "projects/{project}/locations/{location}/tensorboards/{tensorboard}/experiments/{experiment}".format(
        project=project,
        location=location,
        tensorboard=tensorboard,
        experiment=experiment,
    )
    actual = TensorboardServiceClient.tensorboard_experiment_path(
        project, location, tensorboard, experiment
    )
    assert expected == actual


def test_parse_tensorboard_experiment_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
        "tensorboard": "squid",
        "experiment": "clam",
    }
    path = TensorboardServiceClient.tensorboard_experiment_path(**expected)

    # Check that the path construction is reversible.
    actual = TensorboardServiceClient.parse_tensorboard_experiment_path(path)
    assert expected == actual


def test_tensorboard_run_path():
    project = "whelk"
    location = "octopus"
    tensorboard = "oyster"
    experiment = "nudibranch"
    run = "cuttlefish"
    expected = "projects/{project}/locations/{location}/tensorboards/{tensorboard}/experiments/{experiment}/runs/{run}".format(
        project=project,
        location=location,
        tensorboard=tensorboard,
        experiment=experiment,
        run=run,
    )
    actual = TensorboardServiceClient.tensorboard_run_path(
        project, location, tensorboard, experiment, run
    )
    assert expected == actual


def test_parse_tensorboard_run_path():
    expected = {
        "project": "mussel",
        "location": "winkle",
        "tensorboard": "nautilus",
        "experiment": "scallop",
        "run": "abalone",
    }
    path = TensorboardServiceClient.tensorboard_run_path(**expected)

    # Check that the path construction is reversible.
    actual = TensorboardServiceClient.parse_tensorboard_run_path(path)
    assert expected == actual


def test_tensorboard_time_series_path():
    project = "squid"
    location = "clam"
    tensorboard = "whelk"
    experiment = "octopus"
    run = "oyster"
    time_series = "nudibranch"
    expected = "projects/{project}/locations/{location}/tensorboards/{tensorboard}/experiments/{experiment}/runs/{run}/timeSeries/{time_series}".format(
        project=project,
        location=location,
        tensorboard=tensorboard,
        experiment=experiment,
        run=run,
        time_series=time_series,
    )
    actual = TensorboardServiceClient.tensorboard_time_series_path(
        project, location, tensorboard, experiment, run, time_series
    )
    assert expected == actual


def test_parse_tensorboard_time_series_path():
    expected = {
        "project": "cuttlefish",
        "location": "mussel",
        "tensorboard": "winkle",
        "experiment": "nautilus",
        "run": "scallop",
        "time_series": "abalone",
    }
    path = TensorboardServiceClient.tensorboard_time_series_path(**expected)

    # Check that the path construction is reversible.
    actual = TensorboardServiceClient.parse_tensorboard_time_series_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "squid"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = TensorboardServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "clam",
    }
    path = TensorboardServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = TensorboardServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "whelk"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = TensorboardServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "octopus",
    }
    path = TensorboardServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = TensorboardServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "oyster"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = TensorboardServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nudibranch",
    }
    path = TensorboardServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = TensorboardServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "cuttlefish"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = TensorboardServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "mussel",
    }
    path = TensorboardServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = TensorboardServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "winkle"
    location = "nautilus"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = TensorboardServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
    }
    path = TensorboardServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = TensorboardServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.TensorboardServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = TensorboardServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.TensorboardServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = TensorboardServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(
        type(getattr(client.transport, "grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_get_location_rest_bad_request(
    transport: str = "rest", request_type=locations_pb2.GetLocationRequest
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/locations/sample2"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_location(request)


@pytest.mark.parametrize(
    "request_type",
    [
        locations_pb2.GetLocationRequest,
        dict,
    ],
)
def test_get_location_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = locations_pb2.Location()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.get_location(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.Location)


def test_list_locations_rest_bad_request(
    transport: str = "rest", request_type=locations_pb2.ListLocationsRequest
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict({"name": "projects/sample1"}, request)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_locations(request)


@pytest.mark.parametrize(
    "request_type",
    [
        locations_pb2.ListLocationsRequest,
        dict,
    ],
)
def test_list_locations_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = locations_pb2.ListLocationsResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.list_locations(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.ListLocationsResponse)


def test_get_iam_policy_rest_bad_request(
    transport: str = "rest", request_type=iam_policy_pb2.GetIamPolicyRequest
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"resource": "projects/sample1/locations/sample2/featurestores/sample3"},
        request,
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_iam_policy(request)


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.GetIamPolicyRequest,
        dict,
    ],
)
def test_get_iam_policy_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {
        "resource": "projects/sample1/locations/sample2/featurestores/sample3"
    }
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = policy_pb2.Policy()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.get_iam_policy(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)


def test_set_iam_policy_rest_bad_request(
    transport: str = "rest", request_type=iam_policy_pb2.SetIamPolicyRequest
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"resource": "projects/sample1/locations/sample2/featurestores/sample3"},
        request,
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.set_iam_policy(request)


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.SetIamPolicyRequest,
        dict,
    ],
)
def test_set_iam_policy_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {
        "resource": "projects/sample1/locations/sample2/featurestores/sample3"
    }
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = policy_pb2.Policy()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.set_iam_policy(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)


def test_test_iam_permissions_rest_bad_request(
    transport: str = "rest", request_type=iam_policy_pb2.TestIamPermissionsRequest
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"resource": "projects/sample1/locations/sample2/featurestores/sample3"},
        request,
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.test_iam_permissions(request)


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.TestIamPermissionsRequest,
        dict,
    ],
)
def test_test_iam_permissions_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {
        "resource": "projects/sample1/locations/sample2/featurestores/sample3"
    }
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = iam_policy_pb2.TestIamPermissionsResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.test_iam_permissions(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy_pb2.TestIamPermissionsResponse)


def test_cancel_operation_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.CancelOperationRequest
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/locations/sample2/operations/sample3"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.cancel_operation(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.CancelOperationRequest,
        dict,
    ],
)
def test_cancel_operation_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2/operations/sample3"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = "{}"

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.cancel_operation(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_operation_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.DeleteOperationRequest
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/locations/sample2/operations/sample3"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_operation(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.DeleteOperationRequest,
        dict,
    ],
)
def test_delete_operation_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2/operations/sample3"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = "{}"

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.delete_operation(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_get_operation_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.GetOperationRequest
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/locations/sample2/operations/sample3"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_operation(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.GetOperationRequest,
        dict,
    ],
)
def test_get_operation_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2/operations/sample3"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.get_operation(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


def test_list_operations_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.ListOperationsRequest
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/locations/sample2"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_operations(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.ListOperationsRequest,
        dict,
    ],
)
def test_list_operations_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.ListOperationsResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.list_operations(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


def test_wait_operation_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.WaitOperationRequest
):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/locations/sample2/operations/sample3"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.wait_operation(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.WaitOperationRequest,
        dict,
    ],
)
def test_wait_operation_rest(request_type):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2/operations/sample3"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.wait_operation(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


def test_delete_operation(transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.DeleteOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_operation_async(transport: str = "grpc_asyncio"):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.DeleteOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_operation_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.DeleteOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        call.return_value = None

        client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_operation_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.DeleteOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_delete_operation_from_dict():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_delete_operation_from_dict_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_cancel_operation(transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.CancelOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_cancel_operation_async(transport: str = "grpc_asyncio"):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.CancelOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_cancel_operation_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.CancelOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        call.return_value = None

        client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_cancel_operation_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.CancelOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_cancel_operation_from_dict():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.cancel_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_cancel_operation_from_dict_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.cancel_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_wait_operation(transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.WaitOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.wait_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation()
        response = client.wait_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


@pytest.mark.asyncio
async def test_wait_operation(transport: str = "grpc_asyncio"):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.WaitOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.wait_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        response = await client.wait_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


def test_wait_operation_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.WaitOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.wait_operation), "__call__") as call:
        call.return_value = operations_pb2.Operation()

        client.wait_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_wait_operation_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.WaitOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.wait_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        await client.wait_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_wait_operation_from_dict():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.wait_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation()

        response = client.wait_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_wait_operation_from_dict_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.wait_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        response = await client.wait_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_get_operation(transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.GetOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation()
        response = client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


@pytest.mark.asyncio
async def test_get_operation_async(transport: str = "grpc_asyncio"):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.GetOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        response = await client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


def test_get_operation_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.GetOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value = operations_pb2.Operation()

        client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_operation_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.GetOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        await client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_get_operation_from_dict():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation()

        response = client.get_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_get_operation_from_dict_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        response = await client.get_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_list_operations(transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.ListOperationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.ListOperationsResponse()
        response = client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


@pytest.mark.asyncio
async def test_list_operations_async(transport: str = "grpc_asyncio"):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.ListOperationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        response = await client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


def test_list_operations_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.ListOperationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        call.return_value = operations_pb2.ListOperationsResponse()

        client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_operations_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.ListOperationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        await client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_list_operations_from_dict():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.ListOperationsResponse()

        response = client.list_operations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_list_operations_from_dict_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        response = await client.list_operations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_list_locations(transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = locations_pb2.ListLocationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = locations_pb2.ListLocationsResponse()
        response = client.list_locations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.ListLocationsResponse)


@pytest.mark.asyncio
async def test_list_locations_async(transport: str = "grpc_asyncio"):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = locations_pb2.ListLocationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.ListLocationsResponse()
        )
        response = await client.list_locations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.ListLocationsResponse)


def test_list_locations_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = locations_pb2.ListLocationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        call.return_value = locations_pb2.ListLocationsResponse()

        client.list_locations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_locations_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = locations_pb2.ListLocationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.ListLocationsResponse()
        )
        await client.list_locations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_list_locations_from_dict():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = locations_pb2.ListLocationsResponse()

        response = client.list_locations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_list_locations_from_dict_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.ListLocationsResponse()
        )
        response = await client.list_locations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_get_location(transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = locations_pb2.GetLocationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_location), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = locations_pb2.Location()
        response = client.get_location(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.Location)


@pytest.mark.asyncio
async def test_get_location_async(transport: str = "grpc_asyncio"):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = locations_pb2.GetLocationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_location), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.Location()
        )
        response = await client.get_location(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.Location)


def test_get_location_field_headers():
    client = TensorboardServiceClient(credentials=ga_credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = locations_pb2.GetLocationRequest()
    request.name = "locations/abc"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_location), "__call__") as call:
        call.return_value = locations_pb2.Location()

        client.get_location(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations/abc",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_location_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials()
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = locations_pb2.GetLocationRequest()
    request.name = "locations/abc"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_location), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.Location()
        )
        await client.get_location(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations/abc",
    ) in kw["metadata"]


def test_get_location_from_dict():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = locations_pb2.Location()

        response = client.get_location(
            request={
                "name": "locations/abc",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_get_location_from_dict_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.Location()
        )
        response = await client.get_location(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_set_iam_policy(transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.SetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy(
            version=774,
            etag=b"etag_blob",
        )
        response = client.set_iam_policy(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


@pytest.mark.asyncio
async def test_set_iam_policy_async(transport: str = "grpc_asyncio"):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.SetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policy_pb2.Policy(
                version=774,
                etag=b"etag_blob",
            )
        )
        response = await client.set_iam_policy(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


def test_set_iam_policy_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.SetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        call.return_value = policy_pb2.Policy()

        client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_set_iam_policy_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.SetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy_pb2.Policy())

        await client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource/value",
    ) in kw["metadata"]


def test_set_iam_policy_from_dict():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy()

        response = client.set_iam_policy(
            request={
                "resource": "resource_value",
                "policy": policy_pb2.Policy(version=774),
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_set_iam_policy_from_dict_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy_pb2.Policy())

        response = await client.set_iam_policy(
            request={
                "resource": "resource_value",
                "policy": policy_pb2.Policy(version=774),
            }
        )
        call.assert_called()


def test_get_iam_policy(transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.GetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy(
            version=774,
            etag=b"etag_blob",
        )

        response = client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


@pytest.mark.asyncio
async def test_get_iam_policy_async(transport: str = "grpc_asyncio"):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.GetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policy_pb2.Policy(
                version=774,
                etag=b"etag_blob",
            )
        )

        response = await client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


def test_get_iam_policy_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.GetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        call.return_value = policy_pb2.Policy()

        client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_iam_policy_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.GetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy_pb2.Policy())

        await client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource/value",
    ) in kw["metadata"]


def test_get_iam_policy_from_dict():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy()

        response = client.get_iam_policy(
            request={
                "resource": "resource_value",
                "options": options_pb2.GetPolicyOptions(requested_policy_version=2598),
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_get_iam_policy_from_dict_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy_pb2.Policy())

        response = await client.get_iam_policy(
            request={
                "resource": "resource_value",
                "options": options_pb2.GetPolicyOptions(requested_policy_version=2598),
            }
        )
        call.assert_called()


def test_test_iam_permissions(transport: str = "grpc"):
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.TestIamPermissionsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy_pb2.TestIamPermissionsResponse(
            permissions=["permissions_value"],
        )

        response = client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy_pb2.TestIamPermissionsResponse)

    assert response.permissions == ["permissions_value"]


@pytest.mark.asyncio
async def test_test_iam_permissions_async(transport: str = "grpc_asyncio"):
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.TestIamPermissionsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            iam_policy_pb2.TestIamPermissionsResponse(
                permissions=["permissions_value"],
            )
        )

        response = await client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy_pb2.TestIamPermissionsResponse)

    assert response.permissions == ["permissions_value"]


def test_test_iam_permissions_field_headers():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.TestIamPermissionsRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        call.return_value = iam_policy_pb2.TestIamPermissionsResponse()

        client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_test_iam_permissions_field_headers_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.TestIamPermissionsRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            iam_policy_pb2.TestIamPermissionsResponse()
        )

        await client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource/value",
    ) in kw["metadata"]


def test_test_iam_permissions_from_dict():
    client = TensorboardServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy_pb2.TestIamPermissionsResponse()

        response = client.test_iam_permissions(
            request={
                "resource": "resource_value",
                "permissions": ["permissions_value"],
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_test_iam_permissions_from_dict_async():
    client = TensorboardServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            iam_policy_pb2.TestIamPermissionsResponse()
        )

        response = await client.test_iam_permissions(
            request={
                "resource": "resource_value",
                "permissions": ["permissions_value"],
            }
        )
        call.assert_called()


def test_transport_close():
    transports = {
        "rest": "_session",
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = TensorboardServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        with mock.patch.object(
            type(getattr(client.transport, close_name)), "close"
        ) as close:
            with client:
                close.assert_not_called()
            close.assert_called_once()


def test_client_ctx():
    transports = [
        "rest",
        "grpc",
    ]
    for transport in transports:
        client = TensorboardServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()


@pytest.mark.parametrize(
    "client_class,transport_class",
    [
        (TensorboardServiceClient, transports.TensorboardServiceGrpcTransport),
        (
            TensorboardServiceAsyncClient,
            transports.TensorboardServiceGrpcAsyncIOTransport,
        ),
    ],
)
def test_api_key_credentials(client_class, transport_class):
    with mock.patch.object(
        google.auth._default, "get_api_key_credentials", create=True
    ) as get_api_key_credentials:
        mock_cred = mock.Mock()
        get_api_key_credentials.return_value = mock_cred
        options = client_options.ClientOptions()
        options.api_key = "api_key"
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=mock_cred,
                credentials_file=None,
                host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                ),
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )
