from FileBoi import FileBoi
from Sample import Sample
import tkinter as tk
# from Plotter import plot_sample_threshold_heatmap

# Cross validation parameters for finding an optimal tokenization inversion distance threshold -- NOT WORKING?
kfold_n: int = 5
current_vehicle_number = 0

class LogFile:
    def __init__(self, id_dict: dict, j1979_dict: dict, pid_dict: dict):
        self.id_dict:       dict = id_dict
        self.j1979_dict:    dict = j1979_dict
        self.pid_dict:      dict = pid_dict

log_dict = {}
good_boi = FileBoi()
samples = good_boi.go_fetch(kfold_n)
for key, sample_list in samples.items():  # type: tuple, list
    for sample in sample_list:  # type: Sample
        print(current_vehicle_number)
        print("\nData import and Pre-Processing for " + sample.output_vehicle_dir)
        id_dict, j1979_dict, pid_dict = sample.pre_process(False)
        if j1979_dict:
            sample.plot_j1979(j1979_dict, vehicle_number=str(current_vehicle_number))
        log_dict[str(current_vehicle_number)] = LogFile(id_dict, j1979_dict, pid_dict)
        current_vehicle_number += 1

def lexical(vehicle_number):
    id_dict = log_dict[str(vehicle_number)].id_dict
    j1979_dict = log_dict[str(vehicle_number)].j1979_dict
    pid_dict = log_dict[str(vehicle_number)].pid_dict
    #                 LEXICAL ANALYSIS                     #
    print("\n\t##### BEGINNING LEXICAL ANALYSIS OF " + sample.output_vehicle_dir + " #####")
    sample.tokenize_dictionary(id_dict)
    signal_dict = sample.generate_signals(id_dict, bool(j1979_dict))
    #signal_dict = sample.generate_integrals(signal_dict, bool(j1979_dict))
    signal_dict = sample.generate_reverse_endian(signal_dict, bool(j1979_dict))
    sample.plot_arb_ids(id_dict, signal_dict, vehicle_number=str(current_vehicle_number))

def semantic(vehicle_number):
    id_dict = log_dict[str(vehicle_number)].id_dict
    j1979_dict = log_dict[str(vehicle_number)].j1979_dict
    pid_dict = log_dict[str(vehicle_number)].pid_dict
    # Lexical Analysis disabled due to lack of protection against overly large clusters when integrating signals
    #                 LEXICAL ANALYSIS                     #
    print("\n\t##### BEGINNING SEMANTIC ANALYSIS OF " + sample.output_vehicle_dir + " #####")
    sample.tokenize_dictionary(id_dict)
    signal_dict = sample.generate_signals(id_dict, bool(j1979_dict))
    corr_matrix, combined_df = sample.generate_correlation_matrix(signal_dict)
    if j1979_dict:
        signal_dict, j1979_correlation = sample.j1979_labeling(j1979_dict, signal_dict, combined_df)
    cluster_dict, linkage_matrix = sample.cluster_signals(corr_matrix)
    sample.plot_clusters(cluster_dict, signal_dict, bool(j1979_dict), vehicle_number=str(current_vehicle_number))
    sample.plot_dendrogram(linkage_matrix, vehicle_number=str(current_vehicle_number))


root = tk.Tk()
root.title("CAN Reverse Engineering")
mainframe = tk.Frame(root, padding="3 3 12 12")
mainframe.tk.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
tk.Button(mainframe, text="lexical 0", command=lambda: lexical(0)).grid(column=3, row=3, sticky=W)
textbox = tk.Text(mainframe, width=40, height=10)

textbox.insert(tk.END, "Just a text Widget\nin two lines\n")
root.mainloop()

