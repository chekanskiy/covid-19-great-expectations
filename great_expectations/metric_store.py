import json
import numpy as np

from great_expectations.core import ensure_json_serializable
from great_expectations.core.metric import ValidationMetricIdentifier
from great_expectations.data_context.store.database_store_backend import (
    DatabaseStoreBackend,
)
from great_expectations.data_context.store.store import Store
from great_expectations.util import load_class, verify_dynamic_loading_support

class NumpyEncoder(json.JSONEncoder):
    """ Custom encoder for numpy data types """
    def default(self, obj):
        if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
                            np.int16, np.int32, np.int64, np.uint8,
                            np.uint16, np.uint32, np.uint64)):

            return int(obj)

        elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
            return float(obj)

        elif isinstance(obj, (np.complex_, np.complex64, np.complex128)):
            return {'real': obj.real, 'imag': obj.imag}

        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()

        elif isinstance(obj, (np.bool_)):
            return bool(obj)

        elif isinstance(obj, (np.void)):
            return None

        return json.JSONEncoder.default(self, obj)

class MetricStore(Store):
    """
    A MetricStore stores ValidationMetric information to be used between runs.
    """

    _key_class = ValidationMetricIdentifier

    def __init__(self, store_backend=None):
        if store_backend is not None:
            store_backend_module_name = store_backend.get(
                "module_name", "great_expectations.data_context.store"
            )
            store_backend_class_name = store_backend.get(
                "class_name", "InMemoryStoreBackend"
            )
            verify_dynamic_loading_support(module_name=store_backend_module_name)
            store_backend_class = load_class(
                store_backend_class_name, store_backend_module_name
            )

            if issubclass(store_backend_class, DatabaseStoreBackend):
                # Provide defaults for this common case
                if "table_name" not in store_backend:
                    store_backend["table_name"] = store_backend.get(
                        "table_name", "ge_metrics"
                    )
                if "key_columns" not in store_backend:
                    store_backend["key_columns"] = store_backend.get(
                        "key_columns",
                        [
                            "run_name",
                            "run_time",
                            "data_asset_name",
                            "expectation_suite_identifier",
                            "metric_name",
                            "metric_kwargs_id",
                        ],
                    )

        super().__init__(store_backend=store_backend)

    # noinspection PyMethodMayBeStatic
    def _validate_value(self, value):
        # Values must be json serializable since they must be inputs to expectation configurations
        ensure_json_serializable(value)

    def serialize(self, key, value):
        return json.dumps({"value": value}, cls=NumpyEncoder)

    def deserialize(self, key, value):
        if value:
            return json.loads(value)["value"]


class EvaluationParameterStore(MetricStore):
    def __init__(self, store_backend=None):
        if store_backend is not None:
            store_backend_module_name = store_backend.get(
                "module_name", "great_expectations.data_context.store"
            )
            store_backend_class_name = store_backend.get(
                "class_name", "InMemoryStoreBackend"
            )
            verify_dynamic_loading_support(module_name=store_backend_module_name)
            store_backend_class = load_class(
                store_backend_class_name, store_backend_module_name
            )

            # Store Backend Class was loaded successfully; verify that it is of a correct subclass.
            if issubclass(store_backend_class, DatabaseStoreBackend):
                # Provide defaults for this common case
                store_backend["table_name"] = store_backend.get(
                    "table_name", "ge_evaluation_parameters"
                )
        super().__init__(store_backend=store_backend)

    def get_bind_params(self, run_id):
        params = {}
        for k in self._store_backend.list_keys(run_id.to_tuple()):
            key = self.tuple_to_key(k)
            params[key.to_evaluation_parameter_urn()] = self.get(key)
        return params
