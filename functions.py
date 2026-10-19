def ReadSignalFile(file_name):
    indices = []
    samples = []

    with open(file_name, "r") as file:

        lines = []

        for line in file:
            line = line.strip()

            if line != "":
                lines.append(line)



    if len(lines[0].split()) == 1:

        n = int(lines[0])

        if len(lines) >= n + 1 and len(lines[1].split()) == 2:

            for i in range(1, n + 1):

                parts = lines[i].split()

                indices.append(int(parts[0]))
                samples.append(float(parts[1]))

            return indices, samples


    n = int(lines[2])

    for i in range(3, 3 + n):

        parts = lines[i].split()

        indices.append(int(parts[0]))
        samples.append(float(parts[1]))

    return indices, samples


def AddSignals(signals):

    if len(signals) == 0:
        return [], []

    all_indices = []

    for indices, samples in signals:

        for index in indices:

            if index not in all_indices:
                all_indices.append(index)

    all_indices.sort()

    result_samples = []

    for index in all_indices:

        total = 0

        for indices, samples in signals:

            if index in indices:

                position = indices.index(index)

                total = total + samples[position]

        result_samples.append(total)

    return all_indices, result_samples


def MultiplySignal(signal, constant):

    indices, samples = signal

    result_samples = []

    for sample in samples:

        result_samples.append(sample * constant)

    return indices.copy(), result_samples


def SubtractSignals(signal1, signal2):

    negative_signal2 = MultiplySignal(
        signal2,
        -1
    )

    result = AddSignals([
        signal1,
        negative_signal2
    ])

    return result


def ShiftSignal(signal, k):

    indices, samples = signal

    new_indices = []

    for index in indices:

        new_indices.append(index + k)

    return new_indices, samples.copy()


def FoldSignal(signal):

    indices, samples = signal

    new_indices = []

    for index in indices:

        new_indices.append(-index)


    folded_signal = list(zip(new_indices, samples))

    folded_signal.sort()

    result_indices = []
    result_samples = []

    for index, sample in folded_signal:

        result_indices.append(index)
        result_samples.append(sample)

    return result_indices, result_samples


def QuantizeSignal(signal, bits=None, levels=None):
    indices, samples = signal

    if bits is not None and levels is None:
        levels = 2 ** bits
        bits_count = bits
    elif levels is not None:
        import math
        bits_count = math.ceil(math.log2(levels))
        if bits is None:
            bits = bits_count
    else:
        raise ValueError("Either bits or levels must be provided.")

    min_val = min(samples)
    max_val = max(samples)
    delta = (max_val - min_val) / levels

    intervals = []
    for i in range(levels):
        start = min_val + i * delta
        end = min_val + (i + 1) * delta
        mid = (start + end) / 2.0
        intervals.append((start, end, mid))

    interval_indices = []
    encoded_signals = []
    quantized_samples = []
    quantization_errors = []

    for x in samples:
        idx = int((x - min_val) / delta)
        if idx >= levels:
            idx = levels - 1
        if idx < 0:
            idx = 0

        mid = intervals[idx][2]
        interval_index = idx + 1
        encoded = format(idx, f"0{bits_count}b")
        q_val = round(mid, 3)
        error = round(q_val - x, 3)

        interval_indices.append(interval_index)
        encoded_signals.append(encoded)
        quantized_samples.append(q_val)
        quantization_errors.append(error)

    return indices, quantized_samples, quantization_errors, encoded_signals, interval_indices, bits_count, levels
