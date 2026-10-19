import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import matplotlib.pyplot as plt
import numpy as np

from functions import (
    ReadSignalFile,
    AddSignals,
    MultiplySignal,
    SubtractSignals,
    ShiftSignal,
    FoldSignal,
    QuantizeSignal
)


class DSP_GUI:

    def __init__(self, root):
        self.root = root
        self.root.title("DSP Framework - Task 1 & 2")
        self.root.geometry("750x700")

        # Store all loaded/generated signals
        self.signals = []

        # ==========================================
        # Menu Bar (Signal Generation)
        # ==========================================
        menubar = tk.Menu(root)
        
        signal_gen_menu = tk.Menu(menubar, tearoff=0)
        signal_gen_menu.add_command(label="Sine Wave", command=lambda: self.open_generation_dialog("sine"))
        signal_gen_menu.add_command(label="Cosine Wave", command=lambda: self.open_generation_dialog("cosine"))
        
        menubar.add_cascade(label="Signal Generation", menu=signal_gen_menu)
        root.config(menu=menubar)

        # ==========================================
        # Title
        # ==========================================
        title = tk.Label(
            root,
            text="Digital Signal Processing Framework",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=10)

        # ==========================================
        # Representation Mode (Continuous / Discrete)
        # ==========================================
        rep_frame = tk.LabelFrame(root, text="Display Representation", padx=10, pady=5)
        rep_frame.pack(pady=5)

        self.rep_var = tk.StringVar(value="continuous")
        tk.Radiobutton(rep_frame, text="Continuous", variable=self.rep_var, value="continuous").pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(rep_frame, text="Discrete", variable=self.rep_var, value="discrete").pack(side=tk.LEFT, padx=10)


        # ==========================================
        # Load Signal
        # ==========================================
        load_button = tk.Button(
            root,
            text="Load Signal from File",
            width=25,
            command=self.load_signal
        )
        load_button.pack(pady=5)

        # ==========================================
        # Loaded Signals Listbox
        # ==========================================
        tk.Label(root, text="Loaded Signals:").pack()

        self.signal_list = tk.Listbox(
            root,
            width=65,
            height=6,
            selectmode=tk.EXTENDED
        )
        self.signal_list.pack(pady=5)

        # ==========================================
        # Display Controls
        # ==========================================
        display_frame = tk.Frame(root)
        display_frame.pack(pady=5)

        display_button = tk.Button(
            display_frame,
            text="Display Selected Signal(s)",
            width=24,
            command=self.display_selected_signals
        )
        display_button.grid(row=0, column=0, padx=5)

        delete_button = tk.Button(
            display_frame,
            text="Delete Selected Signal(s)",
            width=24,
            bg="#ffebee",
            command=self.delete_selected_signals
        )
        delete_button.grid(row=0, column=1, padx=5)


        # ==========================================
        # Multiply
        # ==========================================
        multiply_frame = tk.Frame(root)
        multiply_frame.pack(pady=5)

        tk.Label(multiply_frame, text="Constant:").pack(side=tk.LEFT)
        self.constant_entry = tk.Entry(multiply_frame, width=10)
        self.constant_entry.pack(side=tk.LEFT, padx=5)

        multiply_button = tk.Button(
            multiply_frame,
            text="Multiply Signal",
            command=self.multiply_signal
        )
        multiply_button.pack(side=tk.LEFT, padx=5)

        # ==========================================
        # Shift
        # ==========================================
        shift_frame = tk.Frame(root)
        shift_frame.pack(pady=5)

        tk.Label(shift_frame, text="Shift k:").pack(side=tk.LEFT)
        self.shift_entry = tk.Entry(shift_frame, width=10)
        self.shift_entry.pack(side=tk.LEFT, padx=5)

        shift_button = tk.Button(
            shift_frame,
            text="Shift Signal",
            command=self.shift_signal
        )
        shift_button.pack(side=tk.LEFT, padx=5)

        # ==========================================
        # Operations
        # ==========================================
        operations_frame = tk.Frame(root)
        operations_frame.pack(pady=10)

        add_button = tk.Button(
            operations_frame,
            text="Add Signals",
            width=18,
            command=self.add_signals
        )
        add_button.grid(row=0, column=0, padx=5, pady=5)

        subtract_button = tk.Button(
            operations_frame,
            text="Subtract Two Signals",
            width=18,
            command=self.subtract_signals
        )
        subtract_button.grid(row=0, column=1, padx=5, pady=5)

        fold_button = tk.Button(
            operations_frame,
            text="Fold Signal",
            width=18,
            command=self.fold_signal
        )
        fold_button.grid(row=0, column=2, padx=5, pady=5)

        quantize_button = tk.Button(
            operations_frame,
            text="Quantize Signal",
            width=18,
            bg="#e1f5fe",
            command=self.quantize_signal
        )
        quantize_button.grid(row=1, column=1, padx=5, pady=5)


        # ==========================================
        # Clear
        # ==========================================
        clear_button = tk.Button(
            root,
            text="Clear All Signals",
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
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_name == "":
            return

        try:
            indices, samples = ReadSignalFile(file_name)
            signal = (indices, samples)
            self.signals.append(signal)

            name = file_name.split("/")[-1]
            self.signal_list.insert(tk.END, name)
        except Exception as e:
            messagebox.showerror("Error", "Could not read signal file.\n\n" + str(e))

    # ==============================================
    # Signal Generation Dialog & Logic
    # ==============================================
    def open_generation_dialog(self, sig_type):
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Generate {sig_type.capitalize()} Wave")
        dialog.geometry("320x280")
        dialog.grab_set()

        tk.Label(dialog, text="Amplitude (A):").pack(pady=2)
        entry_a = tk.Entry(dialog)
        entry_a.pack(pady=2)
        entry_a.insert(0, "1")

        tk.Label(dialog, text="Phase Shift (theta in rad):").pack(pady=2)
        entry_theta = tk.Entry(dialog)
        entry_theta.pack(pady=2)
        entry_theta.insert(0, "0")

        tk.Label(dialog, text="Analog Frequency (F in Hz):").pack(pady=2)
        entry_f = tk.Entry(dialog)
        entry_f.pack(pady=2)
        entry_f.insert(0, "5")

        tk.Label(dialog, text="Sampling Frequency (Fs in Hz):").pack(pady=2)
        entry_fs = tk.Entry(dialog)
        entry_fs.pack(pady=2)
        entry_fs.insert(0, "50")

        def generate():
            try:
                A = float(entry_a.get())
                theta = float(entry_theta.get())
                F = float(entry_f.get())
                Fs = float(entry_fs.get())

                # Sampling Theorem Validation: Fs > 2 * F
                if Fs <= 2 * F:
                    messagebox.showwarning(
                        "Sampling Theorem Warning",
                        f"Sampling frequency (Fs={Fs}) does not obey the sampling theorem (Fs > 2*F = {2*F}). Aliasing may occur!"
                    )

                # Generate signal over 1 second (or N samples based on Fs)
                duration = 1.0
                n = np.arange(0, int(Fs * duration))
                
                if sig_type == "sine":
                    samples = A * np.sin(2 * np.pi * (F / Fs) * n + theta)
                    sig_name = f"Sine (F={F}, Fs={Fs})"
                else:
                    samples = A * np.cos(2 * np.pi * (F / Fs) * n + theta)
                    sig_name = f"Cosine (F={F}, Fs={Fs})"

                indices = n.astype(int).tolist()
                samples = samples.tolist()

                self.signals.append((indices, samples))
                self.signal_list.insert(tk.END, sig_name)
                dialog.destroy()

            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values.")

        tk.Button(dialog, text="Generate", command=generate, width=15, bg="lightgreen").pack(pady=10)

    # ==============================================
    # Helper: Get Selected Signal
    # ==============================================
    def get_one_selected_signal(self):
        selected = self.signal_list.curselection()
        if len(selected) != 1:
            messagebox.showwarning("Warning", "Please select one signal.")
            return None
        return self.signals[selected[0]]

    # ==============================================
    # Display Single Signal
    # ==============================================
    def display_signal(self, signal, title):
        indices, samples = signal
        if len(indices) == 0:
            messagebox.showwarning("Warning", "The signal is empty.")
            return

        plt.figure(figsize=(8, 4))
        representation = self.rep_var.get()

        if representation == "discrete":
            plt.stem(indices, samples)
        else:
            plt.plot(indices, samples)


        plt.title(title)
        plt.xlabel("n (Sample Index)")
        plt.ylabel("Amplitude")
        plt.grid(True)
        plt.show()

    # ==============================================
    # Display Selected Signals (1 or multiple dynamically)
    # ==============================================
    def display_selected_signals(self):
        selected = self.signal_list.curselection()
        if len(selected) == 0:
            messagebox.showwarning("Warning", "Please select at least one signal to display.")
            return

        if len(selected) == 1:
            signal = self.signals[selected[0]]
            label = self.signal_list.get(selected[0])
            self.display_signal(signal, label)
            return

        # If multiple signals are selected, plot them together on a single plot
        representation = self.rep_var.get()
        plt.figure(figsize=(10, 6))

        # Color and line-style palettes for multiple signals
        colors = ['b', 'r', 'g', 'm', 'c', 'y', 'k', 'tab:orange', 'tab:purple', 'tab:brown']
        line_styles = ['-', '--', '-.', ':']

        labels = []
        for idx, sel_idx in enumerate(selected):
            sig = self.signals[sel_idx]
            label = self.signal_list.get(sel_idx)
            labels.append(label)
            color = colors[idx % len(colors)]
            style = line_styles[idx % len(line_styles)]

            if representation == "discrete":
                markerline, stemlines, baseline = plt.stem(sig[0], sig[1], label=label)
                plt.setp(stemlines, color=color, linestyle=style)
                plt.setp(markerline, color=color)
                plt.setp(baseline, color='k')
            else:
                plt.plot(sig[0], sig[1], color=color, linestyle=style, label=label)

        plt.title("Selected Signals Comparison: " + ", ".join(labels[:3]) + ("..." if len(labels) > 3 else ""))
        plt.xlabel("n (Sample Index)")
        plt.ylabel("Amplitude")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()


    # ==============================================
    # Delete Selected Signal(s)
    # ==============================================
    def delete_selected_signals(self):
        selected = list(self.signal_list.curselection())
        if len(selected) == 0:
            messagebox.showwarning("Warning", "Please select at least one signal to delete.")
            return

        # Delete in reverse order so indices do not shift while deleting
        for index in sorted(selected, reverse=True):
            del self.signals[index]
            self.signal_list.delete(index)



    # ==============================================
    # Operations (Add, Subtract, Multiply, Shift, Fold)
    # ==============================================
    def add_signals(self):
        selected = self.signal_list.curselection()
        if len(selected) < 2:
            messagebox.showwarning("Warning", "Please select at least two signals.")
            return
        selected_signals = [self.signals[i] for i in selected]
        result = AddSignals(selected_signals)
        self.display_signal(result, "Addition Result")

    def subtract_signals(self):
        selected = self.signal_list.curselection()
        if len(selected) != 2:
            messagebox.showwarning("Warning", "Please select exactly two signals.")
            return
        result = SubtractSignals(self.signals[selected[0]], self.signals[selected[1]])
        self.display_signal(result, "Subtraction Result")

    def multiply_signal(self):
        signal = self.get_one_selected_signal()
        if signal is None:
            return
        try:
            constant = float(self.constant_entry.get())
        except ValueError:
            messagebox.showwarning("Warning", "Please enter a valid constant number.")
            return
        result = MultiplySignal(signal, constant)
        self.display_signal(result, "Multiplication Result")

    def shift_signal(self):
        signal = self.get_one_selected_signal()
        if signal is None:
            return
        try:
            k = int(self.shift_entry.get())
        except ValueError:
            messagebox.showwarning("Warning", "Please enter an integer shift value.")
            return
        result = ShiftSignal(signal, k)
        self.display_signal(result, "Shift Result")

    def quantize_signal(self):
        signal = self.get_one_selected_signal()
        if signal is None:
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Quantize Signal")
        dialog.geometry("340x260")
        dialog.grab_set()

        choice_var = tk.StringVar(value="bits")

        tk.Label(dialog, text="Select Quantization Parameter:", font=("Arial", 10, "bold")).pack(pady=5)
        
        rb_frame = tk.Frame(dialog)
        rb_frame.pack(pady=5)
        tk.Radiobutton(rb_frame, text="Number of Bits", variable=choice_var, value="bits").pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(rb_frame, text="Number of Levels", variable=choice_var, value="levels").pack(side=tk.LEFT, padx=10)

        input_frame = tk.Frame(dialog)
        input_frame.pack(pady=10)
        label_val = tk.Label(input_frame, text="Enter Bits:")
        label_val.pack(side=tk.LEFT, padx=5)
        entry_val = tk.Entry(input_frame, width=12)
        entry_val.pack(side=tk.LEFT, padx=5)
        entry_val.insert(0, "3")

        def on_mode_change(*args):
            if choice_var.get() == "bits":
                label_val.config(text="Enter Bits:")
            else:
                label_val.config(text="Enter Levels:")

        choice_var.trace_add("write", on_mode_change)

        def execute_quantization():
            val_str = entry_val.get().strip()
            if not val_str:
                messagebox.showerror("Error", "Please enter a value.")
                return
            try:
                num = int(val_str)
                if num <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid positive integer.")
                return

            try:
                if choice_var.get() == "bits":
                    bits = num
                    levels = None
                else:
                    bits = None
                    levels = num

                indices, quantized_samples, errors, encoded, interval_indices, bits_count, total_levels = QuantizeSignal(
                    signal, bits=bits, levels=levels
                )
                dialog.destroy()

                # Add quantized signal to list
                self.signals.append((indices, quantized_samples))
                self.signal_list.insert(tk.END, f"Quantized (levels={total_levels}, bits={bits_count})")

                # Show table window with encoded signal and quantization details
                result_win = tk.Toplevel(self.root)
                result_win.title("Quantization Results & Encoded Signal")
                result_win.geometry("520x400")

                info_label = tk.Label(
                    result_win,
                    text=f"Total Levels: {total_levels} | Bits per sample: {bits_count}",
                    font=("Arial", 11, "bold"),
                    pady=5
                )
                info_label.pack()

                txt_frame = tk.Frame(result_win)
                txt_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

                scrollbar = tk.Scrollbar(txt_frame)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

                text_area = tk.Text(txt_frame, yscrollcommand=scrollbar.set, font=("Consolas", 10))
                text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                scrollbar.config(command=text_area.yview)

                header = f"{'Index':<7}{'Original':<12}{'Interval':<10}{'Encoded':<10}{'Quantized':<12}{'Error':<12}\n"
                text_area.insert(tk.END, header)
                text_area.insert(tk.END, "-" * 63 + "\n")

                orig_samples = signal[1]
                for i in range(len(indices)):
                    row = f"{indices[i]:<7}{orig_samples[i]:<12.3f}{interval_indices[i]:<10}{encoded[i]:<10}{quantized_samples[i]:<12.3f}{errors[i]:<12.3f}\n"
                    text_area.insert(tk.END, row)

                text_area.config(state=tk.DISABLED)

                # Plot Original, Quantized, and Quantization Error in a single plot
                plt.figure(figsize=(10, 6))
                representation = self.rep_var.get()

                if representation == "discrete":
                    plt.stem(indices, orig_samples, linefmt='b-', markerfmt='bo', basefmt='k-', label="Original Signal (x)")
                    plt.stem(indices, quantized_samples, linefmt='g--', markerfmt='gs', basefmt='k-', label="Quantized Signal (x_q)")
                    plt.stem(indices, errors, linefmt='r:', markerfmt='r^', basefmt='k-', label="Quantization Error (e = x_q - x)")
                else:
                    plt.plot(indices, orig_samples, 'b-', label="Original Signal (x)")
                    plt.plot(indices, quantized_samples, 'g--', label="Quantized Signal (x_q)")
                    plt.plot(indices, errors, 'r:', label="Quantization Error (e = x_q - x)")


                plt.title("Original Signal, Quantized Signal & Quantization Error")
                plt.xlabel("n (Sample Index)")
                plt.ylabel("Amplitude")
                plt.grid(True)
                plt.legend()
                plt.tight_layout()
                plt.show()


            except Exception as e:
                messagebox.showerror("Error", f"Quantization failed: {e}")

        tk.Button(dialog, text="Quantize", width=14, bg="#c8e6c9", command=execute_quantization).pack(pady=10)

    def fold_signal(self):
        signal = self.get_one_selected_signal()
        if signal is None:
            return
        result = FoldSignal(signal)
        self.display_signal(result, "Folding Result")

    def clear_signals(self):

        self.signals = []
        self.signal_list.delete(0, tk.END)


# ==============================================
# Start Program
# ==============================================
root = tk.Tk()
app = DSP_GUI(root)
root.mainloop()