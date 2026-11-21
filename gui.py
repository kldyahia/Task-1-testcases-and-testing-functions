"""
GUI for Signal Processing Functions
Provides interface for Moving Average, Derivatives, and Convolution
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from functions import (
    ReadSignalFile,
    MovingAverage,
    FirstDerivative,
    SecondDerivative,
    Convolve,
    AddSignals,
    MultiplySignal,
    SubtractSignals,
    ShiftSignal,
    FoldSignal,
)


class SignalProcessingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Signal Processing Toolkit")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)

        # State
        self.signal1 = None  # (indices, samples)
        self.signal2 = None  # For convolution
        self.result_signal = None
        self.current_plot = "signal1"

        self._build_ui()
        self._setup_plot()

    def _build_ui(self):
        # Main layout: left panel for controls, right for plot
        main_frame = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Left control panel
        control_frame = ttk.Frame(main_frame, width=350)
        main_frame.add(control_frame, weight=0)

        # Right plot panel
        plot_frame = ttk.Frame(main_frame)
        main_frame.add(plot_frame, weight=1)

        self._build_control_panel(control_frame)
        self._build_plot_panel(plot_frame)
        self._build_status_bar()

    def _build_control_panel(self, parent):
        # Notebook for different operation categories
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Tab 1: File Operations
        file_tab = ttk.Frame(notebook)
        notebook.add(file_tab, text="Files")
        self._build_file_tab(file_tab)

        # Tab 2: Moving Average
        ma_tab = ttk.Frame(notebook)
        notebook.add(ma_tab, text="Moving Average")
        self._build_ma_tab(ma_tab)

        # Tab 3: Derivatives
        deriv_tab = ttk.Frame(notebook)
        notebook.add(deriv_tab, text="Derivatives")
        self._build_deriv_tab(deriv_tab)

        # Tab 4: Convolution
        conv_tab = ttk.Frame(notebook)
        notebook.add(conv_tab, text="Convolution")
        self._build_conv_tab(conv_tab)

        # Tab 5: Other Operations
        other_tab = ttk.Frame(notebook)
        notebook.add(other_tab, text="Other Ops")
        self._build_other_tab(other_tab)

        # Results display
        results_frame = ttk.LabelFrame(parent, text="Signal Info / Results")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.results_text = scrolledtext.ScrolledText(results_frame, height=10, wrap=tk.WORD)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def _build_file_tab(self, parent):
        # Signal 1
        s1_frame = ttk.LabelFrame(parent, text="Signal 1 (Primary)")
        s1_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(s1_frame, text="Load Signal 1", command=self.load_signal1).pack(fill=tk.X, padx=5, pady=5)
        self.s1_info_label = ttk.Label(s1_frame, text="No signal loaded", foreground="gray")
        self.s1_info_label.pack(padx=5, pady=5)

        # Signal 2
        s2_frame = ttk.LabelFrame(parent, text="Signal 2 (For Convolution)")
        s2_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(s2_frame, text="Load Signal 2", command=self.load_signal2).pack(fill=tk.X, padx=5, pady=5)
        self.s2_info_label = ttk.Label(s2_frame, text="No signal loaded", foreground="gray")
        self.s2_info_label.pack(padx=5, pady=5)

        # Generate test signal
        gen_frame = ttk.LabelFrame(parent, text="Generate Test Signal")
        gen_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(gen_frame, text="Type:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.gen_type = ttk.Combobox(gen_frame, values=["Sine", "Step", "Ramp", "Impulse", "Noise"], state="readonly")
        self.gen_type.current(0)
        self.gen_type.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(gen_frame, text="Length:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.gen_length = ttk.Spinbox(gen_frame, from_=10, to=1000, value=50)
        self.gen_length.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(gen_frame, text="Freq/Param:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.gen_param = ttk.Spinbox(gen_frame, from_=0.1, to=10.0, increment=0.1, value=1.0)
        self.gen_param.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)

        ttk.Button(gen_frame, text="Generate as Signal 1", command=lambda: self.generate_signal(1)).grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky=tk.EW)
        ttk.Button(gen_frame, text="Generate as Signal 2", command=lambda: self.generate_signal(2)).grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky=tk.EW)

        gen_frame.columnconfigure(1, weight=1)

        # Save result
        save_frame = ttk.LabelFrame(parent, text="Save Result")
        save_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(save_frame, text="Save Result to File", command=self.save_result).pack(fill=tk.X, padx=5, pady=5)

    def _build_ma_tab(self, parent):
        frame = ttk.LabelFrame(parent, text="Moving Average")
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        ttk.Label(frame, text="Window Size:").grid(row=0, column=0, padx=5, pady=10, sticky=tk.W)
        self.ma_window = ttk.Spinbox(frame, from_=1, to=100, value=3)
        self.ma_window.grid(row=0, column=1, padx=5, pady=10, sticky=tk.EW)

        ttk.Label(frame, text="(Odd values give centered average)").grid(row=1, column=0, columnspan=2, padx=5, sticky=tk.W)

        ttk.Button(frame, text="Apply Moving Average", command=self.apply_moving_average).grid(row=2, column=0, columnspan=2, padx=5, pady=10, sticky=tk.EW)

        frame.columnconfigure(1, weight=1)

    def _build_deriv_tab(self, parent):
        frame = ttk.LabelFrame(parent, text="Derivatives (Sharpening)")
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        ttk.Button(frame, text="First Derivative\n(y[n] = x[n] - x[n-1])", command=self.apply_first_derivative).pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(frame, text="Second Derivative\n(y[n] = x[n+1] - 2x[n] + x[n-1])", command=self.apply_second_derivative).pack(fill=tk.X, padx=5, pady=5)

        info_label = ttk.Label(frame, text="Note: Output length reduces by 1 (1st deriv) or 2 (2nd deriv)", foreground="gray", wraplength=300)
        info_label.pack(padx=5, pady=10)

    def _build_conv_tab(self, parent):
        frame = ttk.LabelFrame(parent, text="Convolution")
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        ttk.Label(frame, text="Convolves Signal 1 with Signal 2").pack(padx=5, pady=5)
        ttk.Label(frame, text="y[n] = Σ x[k] * h[n-k]", font=("TkDefaultFont", 9, "italic")).pack(padx=5)

        ttk.Button(frame, text="Convolve Signals", command=self.apply_convolution).pack(fill=tk.X, padx=5, pady=10)

        # Quick kernels
        kernel_frame = ttk.LabelFrame(frame, text="Quick Kernels (apply to Signal 1)")
        kernel_frame.pack(fill=tk.X, padx=5, pady=5)

        kernels = [
            ("Moving Avg 3", [1/3, 1/3, 1/3]),
            ("Moving Avg 5", [0.2]*5),
            ("First Diff", [1, -1]),
            ("Second Diff", [1, -2, 1]),
            ("Sharpen", [0, -1, 0, -1, 5, -1, 0, -1, 0]),  # 3x3 sharpen
        ]

        for i, (name, kernel) in enumerate(kernels):
            btn = ttk.Button(kernel_frame, text=name, command=lambda k=kernel: self.apply_kernel(k))
            btn.grid(row=i//2, column=i%2, padx=3, pady=3, sticky=tk.EW)

        kernel_frame.columnconfigure(0, weight=1)
        kernel_frame.columnconfigure(1, weight=1)

    def _build_other_tab(self, parent):
        frame = ttk.LabelFrame(parent, text="Other Operations")
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        ops = [
            ("Add Signals", self.apply_add),
            ("Subtract (S1 - S2)", self.apply_subtract),
            ("Multiply by Constant", self.apply_multiply),
            ("Shift Signal", self.apply_shift),
            ("Fold Signal (Reverse)", self.apply_fold),
        ]

        for name, cmd in ops:
            ttk.Button(frame, text=name, command=cmd).pack(fill=tk.X, padx=5, pady=3)

        # Plot selection
        plot_frame = ttk.LabelFrame(parent, text="View")
        plot_frame.pack(fill=tk.X, padx=5, pady=10)

        self.view_var = tk.StringVar(value="signal1")
        views = [("Signal 1", "signal1"), ("Signal 2", "signal2"), ("Result", "result"), ("Overlay All", "overlay")]
        for text, val in views:
            ttk.Radiobutton(plot_frame, text=text, variable=self.view_var, value=val, command=self.update_plot).pack(anchor=tk.W, padx=5)

    def _build_plot_panel(self, parent):
        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlabel("Index (n)")
        self.ax.set_ylabel("Amplitude")
        self.ax.set_title("Signal Plot")
        self.ax.grid(True, alpha=0.3)

        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Toolbar
        from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
        toolbar_frame = ttk.Frame(parent)
        toolbar_frame.pack(fill=tk.X)
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.update()

    def _build_status_bar(self):
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=5)

    def _setup_plot(self):
        self.update_plot()

    def _update_status(self, msg):
        self.status_var.set(msg)
        self.root.update_idletasks()

    def _update_results_text(self, text):
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, text)

    def _format_signal_info(self, signal, name="Signal"):
        if signal is None:
            return f"{name}: None\n"
        indices, samples = signal
        return (f"{name}:\n"
                f"  Length: {len(samples)}\n"
                f"  Index range: [{indices[0]}, {indices[-1]}]\n"
                f"  Sample range: [{min(samples):.3f}, {max(samples):.3f}]\n"
                f"  Mean: {np.mean(samples):.3f}\n")

    def load_signal1(self):
        filepath = filedialog.askopenfilename(
            title="Load Signal 1",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filepath:
            try:
                self.signal1 = ReadSignalFile(filepath)
                self.s1_info_label.config(text=f"Loaded: {len(self.signal1[1])} samples", foreground="green")
                self._update_status(f"Loaded Signal 1 from {filepath}")
                self.update_plot()
                self._update_results_text(self._format_signal_info(self.signal1, "Signal 1"))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load signal: {e}")

    def load_signal2(self):
        filepath = filedialog.askopenfilename(
            title="Load Signal 2",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filepath:
            try:
                self.signal2 = ReadSignalFile(filepath)
                self.s2_info_label.config(text=f"Loaded: {len(self.signal2[1])} samples", foreground="green")
                self._update_status(f"Loaded Signal 2 from {filepath}")
                self.update_plot()
                info = self._format_signal_info(self.signal1, "Signal 1") + "\n" + self._format_signal_info(self.signal2, "Signal 2")
                self._update_results_text(info)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load signal: {e}")

    def generate_signal(self, which):
        try:
            length = int(self.gen_length.get())
            param = float(self.gen_param.get())
            signal_type = self.gen_type.get()

            indices = list(range(length))
            samples = []

            if signal_type == "Sine":
                samples = [np.sin(2 * np.pi * param * i / length) for i in range(length)]
            elif signal_type == "Step":
                samples = [1.0 if i >= length // 2 else 0.0 for i in range(length)]
            elif signal_type == "Ramp":
                samples = [i / length for i in range(length)]
            elif signal_type == "Impulse":
                samples = [1.0 if i == length // 2 else 0.0 for i in range(length)]
            elif signal_type == "Noise":
                np.random.seed(42)
                samples = list(np.random.normal(0, param, length))

            signal = (indices, samples)

            if which == 1:
                self.signal1 = signal
                self.s1_info_label.config(text=f"Generated: {length} samples", foreground="green")
            else:
                self.signal2 = signal
                self.s2_info_label.config(text=f"Generated: {length} samples", foreground="green")

            self._update_status(f"Generated {signal_type} signal ({length} samples)")
            self.update_plot()
            self._update_results_text(self._format_signal_info(signal, f"Signal {which}"))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate signal: {e}")

    def apply_moving_average(self):
        if self.signal1 is None:
            messagebox.showwarning("Warning", "Load Signal 1 first")
            return
        try:
            window = int(self.ma_window.get())
            self.result_signal = MovingAverage(self.signal1, window)
            self._update_status(f"Moving Average (window={window}) applied")
            self.view_var.set("result")
            self.update_plot()
            self._update_results_text(
                self._format_signal_info(self.signal1, "Input") + "\n" +
                self._format_signal_info(self.result_signal, f"Moving Average (window={window})")
            )
        except Exception as e:
            messagebox.showerror("Error", f"Moving average failed: {e}")

    def apply_first_derivative(self):
        if self.signal1 is None:
            messagebox.showwarning("Warning", "Load Signal 1 first")
            return
        try:
            self.result_signal = FirstDerivative(self.signal1)
            self._update_status("First Derivative applied")
            self.view_var.set("result")
            self.update_plot()
            self._update_results_text(
                self._format_signal_info(self.signal1, "Input") + "\n" +
                self._format_signal_info(self.result_signal, "First Derivative")
            )
        except Exception as e:
            messagebox.showerror("Error", f"First derivative failed: {e}")

    def apply_second_derivative(self):
        if self.signal1 is None:
            messagebox.showwarning("Warning", "Load Signal 1 first")
            return
        try:
            self.result_signal = SecondDerivative(self.signal1)
            self._update_status("Second Derivative applied")
            self.view_var.set("result")
            self.update_plot()
            self._update_results_text(
                self._format_signal_info(self.signal1, "Input") + "\n" +
                self._format_signal_info(self.result_signal, "Second Derivative")
            )
        except Exception as e:
            messagebox.showerror("Error", f"Second derivative failed: {e}")

    def apply_convolution(self):
        if self.signal1 is None or self.signal2 is None:
            messagebox.showwarning("Warning", "Load both Signal 1 and Signal 2")
            return
        try:
            self.result_signal = Convolve(self.signal1, self.signal2)
            self._update_status("Convolution applied")
            self.view_var.set("result")
            self.update_plot()
            self._update_results_text(
                self._format_signal_info(self.signal1, "Signal 1") + "\n" +
                self._format_signal_info(self.signal2, "Signal 2") + "\n" +
                self._format_signal_info(self.result_signal, "Convolution Result")
            )
        except Exception as e:
            messagebox.showerror("Error", f"Convolution failed: {e}")

    def apply_kernel(self, kernel):
        if self.signal1 is None:
            messagebox.showwarning("Warning", "Load Signal 1 first")
            return
        try:
            # Create kernel signal with indices starting at 0
            kernel_signal = (list(range(len(kernel))), kernel)
            self.result_signal = Convolve(self.signal1, kernel_signal)
            self._update_status(f"Kernel convolution applied ({len(kernel)} taps)")
            self.view_var.set("result")
            self.update_plot()
            self._update_results_text(
                self._format_signal_info(self.signal1, "Input") + "\n" +
                self._format_signal_info(self.result_signal, f"Kernel Result (len={len(kernel)})")
            )
        except Exception as e:
            messagebox.showerror("Error", f"Kernel convolution failed: {e}")

    def apply_add(self):
        if self.signal1 is None or self.signal2 is None:
            messagebox.showwarning("Warning", "Load both signals")
            return
        try:
            self.result_signal = AddSignals([self.signal1, self.signal2])
            self._update_status("Signals added")
            self.view_var.set("result")
            self.update_plot()
            self._update_results_text(self._format_signal_info(self.result_signal, "Sum"))
        except Exception as e:
            messagebox.showerror("Error", f"Add failed: {e}")

    def apply_subtract(self):
        if self.signal1 is None or self.signal2 is None:
            messagebox.showwarning("Warning", "Load both signals")
            return
        try:
            self.result_signal = SubtractSignals(self.signal1, self.signal2)
            self._update_status("Signal 2 subtracted from Signal 1")
            self.view_var.set("result")
            self.update_plot()
            self._update_results_text(self._format_signal_info(self.result_signal, "Difference (S1 - S2)"))
        except Exception as e:
            messagebox.showerror("Error", f"Subtract failed: {e}")

    def apply_multiply(self):
        if self.signal1 is None:
            messagebox.showwarning("Warning", "Load Signal 1 first")
            return
        try:
            const = tk.simpledialog.askfloat("Multiply", "Enter constant:", initialvalue=2.0)
            if const is not None:
                self.result_signal = MultiplySignal(self.signal1, const)
                self._update_status(f"Multiplied by {const}")
                self.view_var.set("result")
                self.update_plot()
                self._update_results_text(self._format_signal_info(self.result_signal, f"Multiplied by {const}"))
        except Exception as e:
            messagebox.showerror("Error", f"Multiply failed: {e}")

    def apply_shift(self):
        if self.signal1 is None:
            messagebox.showwarning("Warning", "Load Signal 1 first")
            return
        try:
            k = tk.simpledialog.askinteger("Shift", "Enter shift amount (k):", initialvalue=1)
            if k is not None:
                self.result_signal = ShiftSignal(self.signal1, k)
                self._update_status(f"Shifted by {k}")
                self.view_var.set("result")
                self.update_plot()
                self._update_results_text(self._format_signal_info(self.result_signal, f"Shifted by {k}"))
        except Exception as e:
            messagebox.showerror("Error", f"Shift failed: {e}")

    def apply_fold(self):
        if self.signal1 is None:
            messagebox.showwarning("Warning", "Load Signal 1 first")
            return
        try:
            self.result_signal = FoldSignal(self.signal1)
            self._update_status("Signal folded (reversed)")
            self.view_var.set("result")
            self.update_plot()
            self._update_results_text(self._format_signal_info(self.result_signal, "Folded"))
        except Exception as e:
            messagebox.showerror("Error", f"Fold failed: {e}")

    def save_result(self):
        if self.result_signal is None:
            messagebox.showwarning("Warning", "No result to save")
            return
        filepath = filedialog.asksaveasfilename(
            title="Save Result",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filepath:
            try:
                indices, samples = self.result_signal
                with open(filepath, "w") as f:
                    f.write(f"{len(samples)}\n")
                    for idx, samp in zip(indices, samples):
                        f.write(f"{idx} {samp}\n")
                self._update_status(f"Result saved to {filepath}")
                messagebox.showinfo("Success", "Result saved successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Save failed: {e}")

    def update_plot(self):
        self.ax.clear()
        self.ax.set_xlabel("Index (n)")
        self.ax.set_ylabel("Amplitude")
        self.ax.grid(True, alpha=0.3)

        view = self.view_var.get()

        if view == "signal1" and self.signal1 is not None:
            self._plot_signal(self.signal1, "Signal 1", 'b-', 'bo')
        elif view == "signal2" and self.signal2 is not None:
            self._plot_signal(self.signal2, "Signal 2", 'g-', 'go')
        elif view == "result" and self.result_signal is not None:
            self._plot_signal(self.result_signal, "Result", 'r-', 'ro')
        elif view == "overlay":
            if self.signal1 is not None:
                self._plot_signal(self.signal1, "Signal 1", 'b-', 'bo', alpha=0.7)
            if self.signal2 is not None:
                self._plot_signal(self.signal2, "Signal 2", 'g-', 'go', alpha=0.7)
            if self.result_signal is not None:
                self._plot_signal(self.result_signal, "Result", 'r-', 'ro', alpha=0.7)
            self.ax.legend()

        self.ax.set_title(f"Signal Plot - {view.replace('_', ' ').title()}")
        self.fig.tight_layout()
        self.canvas.draw()

    def _plot_signal(self, signal, label, line_style, marker_style, alpha=1.0):
        indices, samples = signal
        self.ax.plot(indices, samples, line_style, label=label, alpha=alpha, markersize=4)
        self.ax.plot(indices, samples, marker_style, alpha=alpha, markersize=4)


def main():
    root = tk.Tk()
    app = SignalProcessingGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()