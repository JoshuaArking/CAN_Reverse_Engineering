from numpy import float64
from pandas import Series
from os import path, remove
from pickle import load
from scipy import integrate
from PipelineTimer import PipelineTimer


# noinspection PyProtectedMember
def generate_integrals(a_timer: PipelineTimer,
                       signal_dict: dict,
                       integral_pickle_filename: str,
                       normalize_strategy,
                       force=False):
    if force and path.isfile(integral_pickle_filename):
        remove(integral_pickle_filename)
    if path.isfile(integral_pickle_filename):
        print("\nIntegral generation already completed and forcing is turned off. Using pickled data...")
        return load(open(integral_pickle_filename, "rb"))

    a_timer.start_function_time()

    integral_dict = {}

    for k_arb_id, arb_id_signals in signal_dict.items():
        for k_signal_id, signal in arb_id_signals.items():
            if not signal.static:
                a_timer.start_iteration_time()

                transformed_signal = signal

                transformed_signal.time_series = Series(integrate.cumtrapz(signal.time_series._ndarray_values),
                                                        index=signal.time_series._index[:-1],
                                                        dtype=float64)

                # Normalize the signal and update its meta-data
                transformed_signal.normalize_and_set_metadata(normalize_strategy)
                # add this signal to the integral dictionary which is keyed by Signal ID
                if k_arb_id in integral_dict:
                    integral_dict[k_arb_id][(transformed_signal.arb_id,
                                             transformed_signal.start_index,
                                             transformed_signal.stop_index)] = transformed_signal
                else:
                    integral_dict[k_arb_id] = {(transformed_signal.arb_id,
                                                transformed_signal.start_index,
                                                transformed_signal.stop_index): transformed_signal}

                a_timer.set_token_to_signal()

    a_timer.set_signal_generation()
    return integral_dict
