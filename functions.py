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

        # Normal format
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

    # Get all indices
    for indices, samples in signals:

        for index in indices:

            if index not in all_indices:
                all_indices.append(index)

    all_indices.sort()

    result_samples = []

    # Add samples having the same index
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

    #signal1 - signal2
    # = signal1 + (-1 * signal2)

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

    # Keep each index with its sample
    folded_signal = list(zip(new_indices, samples))

    # Sort using the new indices
    folded_signal.sort()

    result_indices = []
    result_samples = []

    for index, sample in folded_signal:

        result_indices.append(index)
        result_samples.append(sample)

    return result_indices, result_samples