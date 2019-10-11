from numpy import float64
from pandas import Series
from os import path, remove
from pickle import load
from scipy import integrate
from PipelineTimer import PipelineTimer


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

                transformed_signal.time_series = Series(integrate.cumtrapz(signal.time_series.values),
                                                        index=signal.time_series.axes[0][:-1],
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

                a_timer.set_signal_to_integral()

    a_timer.set_integral_generation()
    return integral_dict

def generate_reverse_endian(a_timer: PipelineTimer,
                       signal_dict: dict,
                       integral_pickle_filename: str,
                       normalize_strategy,
                       force=False):
    if force and path.isfile(integral_pickle_filename):
        remove(integral_pickle_filename)
    if path.isfile(integral_pickle_filename):
        print("\nIntegral generation already completed and forcing is turned off. Using pickled data...")
        return load(open(integral_pickle_filename, "rb"))

    def reverseBits(num):
        # convert number into binary representation
        # output will be like bin(10) = '0b10101'
        print("converted " + str(num) + " to")
        binary = bin(num)

        # skip first two characters of binary
        # representation string and reverse
        # remaining string and then append zeros
        # after it. binary[-1:1:-1]  --> start
        # from last character and reverse it until
        # second last character from left
        reverse = binary[-1:1:-1]
        reverse = reverse + (8 - len(reverse)) * '0'

        # converts reversed binary string into integer
        print(str(int(reverse, 2)) + ".")
        return int(reverse, 2)

    a_timer.start_function_time()

    reverse_endian_dict = {}

    for k_arb_id, arb_id_signals in signal_dict.items():
        for k_signal_id, signal in arb_id_signals.items():
            if not signal.static:
                a_timer.start_iteration_time()

                transformed_signal = signal
                original_time_series = signal.time_series


                # I know there's a better way to do this, rewrite after POC works
                b0 = signal.original_data['b0']
                b1 = signal.original_data['b1']
                b2 = signal.original_data['b2']
                b3 = signal.original_data['b3']
                b4 = signal.original_data['b4']
                b5 = signal.original_data['b5']
                b6 = signal.original_data['b6']
                b7 = signal.original_data['b7']

                for i in range(0,7):
                    transformed_signal.original_data['b' + str(i)] = transformed_signal.original_data['b' + str(i)].map(reverseBits)

                # Normalize the signal and update its meta-data
                transformed_signal.normalize_and_set_metadata(normalize_strategy)
                # add this signal to the integral dictionary which is keyed by Signal ID
                if k_arb_id in reverse_endian_dict:
                    reverse_endian_dict[k_arb_id][(transformed_signal.arb_id,
                                             transformed_signal.start_index,
                                             transformed_signal.stop_index)] = transformed_signal
                else:
                    reverse_endian_dict[k_arb_id] = {(transformed_signal.arb_id,
                                                transformed_signal.start_index,
                                                transformed_signal.stop_index): transformed_signal}

                a_timer.set_signal_to_integral()

    a_timer.set_integral_generation()
    return reverse_endian_dict

