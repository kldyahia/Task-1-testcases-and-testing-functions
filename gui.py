import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import matplotlib.pyplot as plt

from functions import (
    ReadSignalFile,
    AddSignals,
    MultiplySignal,
    SubtractSignals,
    ShiftSignal,
    FoldSignal
)


class DSP_GUI:

    def __init__(self, root):

        self.root = root

        self.root.title("DSP Task 1")

        self.root.geometry("750x600")

        # Store all loaded signals
        self.signals = []

        # ==========================================
        # Title
        # ==========================================

        title = tk.Label(
            root,
            text="Digital Signal Processing - Task 1",
            font=("Arial", 20, "bold")
        )

        title.pack(pady=15)

        # ==========================================
        # Load Signal
        # ==========================================

        load_button = tk.Button(
            root,
            text="Load Signal",
            width=20,
            command=self.load_signal
        )

        load_button.pack(pady=5)

        # ==========================================
        # Loaded Signals
        # ==========================================

        tk.Label(
            root,
            text="Loaded Signals:"
        ).pack()

        self.signal_list = tk.Listbox(
            root,
            width=60,
            height=7,
            selectmode=tk.EXTENDED
        )

        self.signal_list.pack(pady=5)

        # ==========================================
        # Display
        # ==========================================

        display_button = tk.Button(
            root,
            text="Display Selected Signal",
            width=25,
            command=self.display_selected
        )

        display_button.pack(pady=5)

        # ==========================================
        # Multiply
        # ==========================================

        multiply_frame = tk.Frame(root)

        multiply_frame.pack(pady=5)

        tk.Label(
            multiply_frame,
            text="Constant:"
        ).pack(side=tk.LEFT)

        self.constant_entry = tk.Entry(
            multiply_frame,
            width=10
        )

        self.constant_entry.pack(
            side=tk.LEFT,
            padx=5
        )

        multiply_button = tk.Button(
            multiply_frame,
            text="Multiply Signal",
            command=self.multiply_signal
        )

        multiply_button.pack(
            side=tk.LEFT,
            padx=5
        )

        # ==========================================
        # Shift
        # ==========================================

        shift_frame = tk.Frame(root)

        shift_frame.pack(pady=5)

        tk.Label(
            shift_frame,
            text="Shift k:"
        ).pack(side=tk.LEFT)

        self.shift_entry = tk.Entry(
            shift_frame,
            width=10
        )

        self.shift_entry.pack(
            side=tk.LEFT,
            padx=5
        )

        shift_button = tk.Button(
            shift_frame,
            text="Shift Signal",
            command=self.shift_signal
        )

        shift_button.pack(
            side=tk.LEFT,
            padx=5
        )

        # ==========================================
        # Operations
        # ==========================================

        operations_frame = tk.Frame(root)

        operations_frame.pack(pady=15)

        # Addition

        add_button = tk.Button(
            operations_frame,
            text="Add Selected Signals",
            width=20,
            command=self.add_signals
        )

        add_button.grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

        # Subtraction

        subtract_button = tk.Button(
            operations_frame,
            text="Subtract Two Signals",
            width=20,
            command=self.subtract_signals
        )

        subtract_button.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        # Folding

        fold_button = tk.Button(
            operations_frame,
            text="Fold Selected Signal",
            width=20,
            command=self.fold_signal
        )

        fold_button.grid(
            row=0,
            column=2,
            padx=5,
            pady=5
        )

        # ==========================================
        # Clear
        # ==========================================

        clear_button = tk.Button(
            root,
            text="Clear Signals",
            width=20,
            command=self.clear_signals
        )

        clear_button.pack(pady=5)

    # ==============================================
    # Load Signal
    # ==============================================

    def load_signal(self):

        file_name = filedialog.askopenfilename(
            title="Choose Signal File",
            filetypes=[
                ("Text Files", "*.txt"),
                ("All Files", "*.*")
            ]
        )

        if file_name == "":
            return

        try:

            indices, samples = ReadSignalFile(
                file_name
            )

            signal = (
                indices,
                samples
            )

            self.signals.append(signal)

            # Get file name
            name = file_name.split("/")[-1]

            self.signal_list.insert(
                tk.END,
                name
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                "Could not read signal file.\n\n" + str(e)
            )

    # ==============================================
    # Get One Selected Signal
    # ==============================================

    def get_one_selected_signal(self):

        selected = self.signal_list.curselection()

        if len(selected) != 1:

            messagebox.showwarning(
                "Warning",
                "Please select one signal."
            )

            return None

        index = selected[0]

        return self.signals[index]

    # ==============================================
    # Display Signal
    # ==============================================

    def display_signal(self, signal, title):

        indices, samples = signal

        if len(indices) == 0:

            messagebox.showwarning(
                "Warning",
                "The signal is empty."
            )

            return

        plt.figure()

        plt.stem(
            indices,
            samples
        )

        plt.title(title)

        plt.xlabel("n")

        plt.ylabel("Amplitude")

        plt.grid(True)

        plt.show()

    # ==============================================
    # Display Selected Signal
    # ==============================================

    def display_selected(self):

        signal = self.get_one_selected_signal()

        if signal is None:
            return

        self.display_signal(
            signal,
            "Signal"
        )

    # ==============================================
    # Addition
    # ==============================================

    def add_signals(self):

        selected = self.signal_list.curselection()

        if len(selected) < 2:

            messagebox.showwarning(
                "Warning",
                "Please select at least two signals."
            )

            return

        selected_signals = []

        for index in selected:

            selected_signals.append(
                self.signals[index]
            )

        result = AddSignals(
            selected_signals
        )

        self.display_signal(
            result,
            "Addition Result"
        )

    # ==============================================
    # Subtraction
    # ==============================================

    def subtract_signals(self):

        selected = self.signal_list.curselection()

        if len(selected) != 2:

            messagebox.showwarning(
                "Warning",
                "Please select exactly two signals."
            )

            return

        signal1 = self.signals[selected[0]]

        signal2 = self.signals[selected[1]]

        result = SubtractSignals(
            signal1,
            signal2
        )

        self.display_signal(
            result,
            "Subtraction Result"
        )

    # ==============================================
    # Multiplication
    # ==============================================

    def multiply_signal(self):

        signal = self.get_one_selected_signal()

        if signal is None:
            return

        try:

            constant = float(
                self.constant_entry.get()
            )

        except:

            messagebox.showwarning(
                "Warning",
                "Please enter a valid number."
            )

            return

        result = MultiplySignal(
            signal,
            constant
        )

        self.display_signal(
            result,
            "Multiplication Result"
        )

    # ==============================================
    # Shift
    # ==============================================

    def shift_signal(self):

        signal = self.get_one_selected_signal()

        if signal is None:
            return

        try:

            k = int(
                self.shift_entry.get()
            )

        except:

            messagebox.showwarning(
                "Warning",
                "Please enter an integer."
            )

            return

        result = ShiftSignal(
            signal,
            k
        )

        self.display_signal(
            result,
            "Shift Result"
        )

    # ==============================================
    # Folding
    # ==============================================

    def fold_signal(self):

        signal = self.get_one_selected_signal()

        if signal is None:
            return

        result = FoldSignal(
            signal
        )

        self.display_signal(
            result,
            "Folding Result"
        )

    # ==============================================
    # Clear
    # ==============================================

    def clear_signals(self):

        self.signals = []

        self.signal_list.delete(
            0,
            tk.END
        )


# ==============================================
# Start Program
# ==============================================

root = tk.Tk()

app = DSP_GUI(root)

root.mainloop()