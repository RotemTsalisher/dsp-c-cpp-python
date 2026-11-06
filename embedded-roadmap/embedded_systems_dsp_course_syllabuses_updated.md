# Embedded Systems & DSP Learning Roadmap

## Course Syllabuses for Cursor

**Target learners:** The courses have different entry points. The
MSP430, Arduino, and ESP32 courses assume basic programming knowledge as
specified in each syllabus. The dedicated algorithm-development course
starts from the level of a second-year Electrical Engineering student
who has coding experience but no prior algorithm or data-structure
experience.

**Purpose:** Use these syllabuses as the source of truth when generating
five separate, structured, hands-on courses. Keep each course
independent, with its own lessons, labs, exercises, assignments,
solutions, and final project.

## Global course-generation requirements

For every course:

-   Follow the module count and order specified in that course. The four
    embedded-platform/DSP courses have 13 modules each; the dedicated
    algorithm-development course has 24 modules.
-   Explain concepts concisely but accurately, progressing from
    fundamentals to advanced implementation.
-   Include hardware-specific explanations and cite the relevant
    datasheet, reference manual, and official documentation.
-   Include practical, step-by-step labs using the specified hardware.
-   Include at least 3 progressive exercises and 1 independent
    assignment per module.
-   Provide expected results, test procedures, common mistakes, and
    debugging guidance.
-   Include complete, buildable code examples, with comments explaining
    important decisions.
-   Keep exercise solutions separate from the learner-facing exercises.
-   Use Python or MATLAB as a reference environment for DSP algorithms
    where useful.
-   Do not invent hardware capabilities. Clearly identify any external
    components, adapters, or circuitry required.
-   Respect the stated learner level for each course. In particular, the
    algorithm-development course must start from first principles and
    must not assume prior knowledge of algorithms, data structures, Big
    O notation, or formal complexity analysis.
-   Use Git-friendly project structure and explain how to build, flash,
    test, and version each project.
-   Teach algorithm terminology explicitly and progressively wherever
    relevant. Include intuitive explanations, precise definitions,
    worked examples, and exercises that require correct use of terms.
-   Treat time complexity, space complexity, data-structure selection,
    and resource constraints as recurring engineering concerns, not
    isolated advanced topics.
-   For algorithm-focused work, distinguish theoretical complexity from
    measured execution time. Analyze best, average, and worst cases
    where applicable; auxiliary and total space; memory overhead;
    determinism; and scalability.
-   Require learners to justify data-structure and algorithm choices
    against realistic requirements and alternatives.
-   For embedded implementations, estimate resource use before coding
    and measure or otherwise verify RAM, stack, Flash, and execution
    time after implementation whenever technically possible.

------------------------------------------------------------------------

# Course 1 --- TI MSP430: Embedded C and Microcontroller Programming

**Target hardware:** TI MSP-EXP430G2 LaunchPad using the MSP430G2553.

**Purpose:** Learn microcontroller programming from GPIO and timers
through interrupts, analog acquisition, serial communication, low-power
operation, and complete firmware design. Emphasize direct register-level
work and understanding the hardware rather than relying only on
abstractions.

**Hardware constraints to respect:** MSP430G2553 is a 16-bit MCU with up
to 16 MHz operation, 16 KB Flash, 512 bytes RAM, a 10-bit ADC, and
Timer_A/USCI peripherals. Do not attribute features from newer MSP430
families to this device. It has no hardware FPU or onboard DAC.

### Modules

1.  **Embedded systems and MSP430 architecture** --- MCU fundamentals,
    CPU, memory, buses, peripherals, LaunchPad layout, execution model,
    and first firmware.
2.  **Toolchain and debugging workflow** --- Code Composer Studio,
    compiler/linker, project structure, flashing, debugger basics, build
    output, and breakpoints.
3.  **GPIO and digital electronics** --- Pin configuration,
    input/output, pull-ups, active-high/low logic, bit masks, button
    debouncing, and LED control.
4.  **Clock system and low-power modes** --- DCO, clock sources and
    dividers, timing accuracy, low-power modes, wake-up sources, and
    energy-aware firmware.
5.  **Interrupts and event handling** --- Port interrupts, ISRs, shared
    variables, `volatile`, race conditions, interrupt latency, and
    event-driven design.
6.  **Timer_A and timing systems** --- Timer modes, capture/compare,
    periodic interrupts, time measurement, and timer-driven
    applications.
7.  **ADC10 and analog interfacing** --- ADC configuration, reference
    voltage, sampling/conversion, resolution, quantization, analog input
    limits, and measurement.
8.  **PWM and actuator control** --- Timer-based PWM, frequency and duty
    cycle, LED dimming, and motor control through an appropriate
    external driver.
9.  **UART communication** --- USCI UART, baud rate, framing, serial
    terminal, command parsing, and robust communication.
10. **SPI and I2C communication** --- USCI serial modes, bus
    transactions, external devices, protocol debugging, and
    logic-analyzer use.
11. **Memory, watchdog, and reliability** --- Flash, tiny SRAM, stack
    use, persistent data, watchdog operation, fault handling, and
    resource constraints.
12. **Firmware architecture and real-time programming** --- Modular
    drivers, finite-state machines, cooperative scheduling, timing
    budgets, and testable application structure.
13. **Integration and final project** --- Combine multiple peripherals
    into a complete application, debug it, measure its behavior, and
    document the design.

**Final project options:** sensor monitor/data logger, PWM motor
controller, serial command controller, or timer-driven measurement
system.

------------------------------------------------------------------------

# Course 2 --- TI MSP430: Embedded Digital Signal Processing

**Target hardware:** Same MSP-EXP430G2 LaunchPad and MSP430G2553.

**Purpose:** Learn how DSP algorithms behave on a very
resource-constrained 16-bit MCU. Prioritize fixed-point arithmetic,
careful memory use, simple algorithms, and measurement of execution time
and numerical error. This is a DSP fundamentals and optimization course,
not a claim that the G2553 is a full audio-processing platform.

**Hardware constraints to respect:** 512 bytes of RAM, 10-bit ADC, no
FPU, and no onboard DAC. Use an external output circuit/DAC only when a
lab specifically requires analog output. Keep sample buffers and FFT
sizes realistic.

### Modules

1.  **Embedded DSP foundations** --- Discrete-time signals, real-time
    constraints, processing architectures, sample-by-sample operation,
    and MCU resource limits.
2.  **Discrete-time signals and systems** --- Sequences, impulse/step
    response, LTI systems, convolution, and difference equations.
3.  **ADC-based signal acquisition** --- ADC10 configuration,
    timer-triggered sampling, sample rate, quantization, aliasing, and
    input conditioning.
4.  **Fixed-point arithmetic** --- Q formats, scaling, signed
    arithmetic, multiplication, rounding, saturation, overflow, and
    precision.
5.  **Time-domain signal analysis** --- Mean, RMS, peak, energy, moving
    average, and lightweight signal statistics.
6.  **DFT and spectral analysis** --- DFT definition, complex
    arithmetic, frequency bins, magnitude, resolution, and computational
    cost.
7.  **Small FFT implementations** --- Radix-2 FFT, butterfly operations,
    twiddle factors, small block sizes, and memory-aware implementation.
8.  **FIR filters** --- Difference equations, coefficients, windowing,
    low/high-pass design, frequency response, and fixed-point
    implementation.
9.  **IIR filters** --- Recursive structures, poles and zeros,
    stability, first/second-order filters, and numerical behavior.
10. **Practical embedded DSP algorithms** --- Tone detection,
    threshold/event detection, simple spectral analysis, and signal
    conditioning.
11. **Real-time acquisition and processing** --- Timer-driven sampling,
    interrupt-based acquisition, circular buffers, processing deadlines,
    and data loss.
12. **DSP optimization and validation** --- Cycle counting, memory
    profiling, fixed-point optimization, error analysis, and comparison
    with Python/MATLAB references.
13. **Final embedded DSP project** --- Design and validate a realistic
    signal-processing application within the G2553's resource limits.

**Final project options:** fixed-point FIR filter, tone detector,
small-window FFT analyzer, or low-frequency signal monitor/classifier.

------------------------------------------------------------------------

# Course 3 --- Arduino UNO R4 Minima: Embedded Systems and DSP

**Target hardware:** Arduino UNO R4 Minima, based on the Renesas RA4M1.

**Purpose:** Move from Arduino-level programming to understanding the
underlying ARM Cortex-M4 microcontroller. Cover C/C++, GPIO, timers,
interrupts, ADC/DAC, communication, DMA, memory, real-time firmware,
DSP, and practical analog audio interfacing.

**Hardware facts to respect:** RA4M1, 32-bit ARM Cortex-M4 with FPU, 48
MHz, 256 KB Flash, 32 KB SRAM, 8 KB data flash, 5 V board logic, ADC,
12-bit DAC, PWM, UART, SPI, I2C, and CAN. Verify pin routing and
peripheral availability against the actual board schematic and RA4M1
documentation.

### Modules

1.  **Arduino and RA4M1 architecture** --- Board setup, Arduino core,
    build/flash workflow, MCU architecture, memory, peripherals, and the
    relationship between framework and hardware.
2.  **Embedded C/C++** --- Pointers, structures, bit operations,
    `volatile`, memory, modular drivers, C++ abstractions, and generated
    code.
3.  **GPIO and digital logic** --- Pin configuration, pull-ups,
    debouncing, external loads, electrical limits, and state machines.
4.  **Timers, counters, and PWM** --- Timer hardware, clocking,
    frequency, duty cycle, timer interrupts, PWM generation, and
    motor-driver interfacing.
5.  **Interrupts and event handling** --- Cortex-M interrupt model,
    NVIC, ISRs, shared data, race conditions, latency, and event-driven
    design.
6.  **ADC, DAC, and analog interfacing** --- ADC configuration,
    resolution, references, sampling, DAC waveform output, analog
    limits, and measurement.
7.  **UART, SPI, and I2C** --- Protocol fundamentals, peripheral setup,
    external sensors/devices, and logic-analyzer debugging.
8.  **Memory and data structures** --- Flash, SRAM, data flash,
    stack/heap, circular buffers, persistent settings, and memory
    analysis.
9.  **ARM Cortex-M4 and low-level programming** --- Registers,
    exceptions, stack, assembly inspection, CMSIS, memory-mapped I/O,
    and direct peripheral-register access.
10. **DMA and data movement** --- DMA concepts, peripheral requests,
    buffers, double buffering, transfer constraints, and performance
    measurement.
11. **Real-time firmware architecture** --- State machines, cooperative
    scheduling, timing budgets, watchdogs, fault recovery, and
    deterministic behavior.
12. **Debugging, testing, and optimization** --- Unit/integration
    testing, profiling, compiler optimization, memory/timing analysis,
    and hardware-in-the-loop methods.
13. **Final embedded systems project** --- Integrate peripherals and
    firmware architecture into a documented, tested embedded
    application.

### Embedded DSP and audio progression

The course should include DSP concepts and practical DSP labs as a
dedicated sequence within the same 13-module curriculum:

-   Discrete-time signals, sampling, quantization, aliasing, and ADC
    acquisition.
-   Signal generation using lookup tables and numerical oscillators.
-   Time-domain analysis, convolution, correlation, RMS, and peak
    detection.
-   FIR and IIR filters, biquads, and frequency response.
-   DFT/FFT, windowing, spectral analysis, and audio features.
-   Fixed-point versus floating-point processing and performance
    profiling.
-   Real-time sample acquisition, buffering, DMA concepts, and latency
    measurement.
-   Audio gain, clipping, equalization, envelope detection, and basic
    effects.

### Required external analog audio labs

The UNO R4 Minima is not an audio-codec board. The course must teach the
learner to build and measure the external circuitry needed to interface
analog audio safely.

1.  **Microphone preamplifier:** bias an electret microphone, design an
    op-amp preamplifier, calculate gain, and measure noise/clipping.
2.  **ADC input conditioning:** AC coupling, mid-supply bias, anti-alias
    low-pass filter, input protection, and verification that the signal
    stays within the board's permitted analog input range.
3.  **DAC reconstruction:** generate a waveform, design a reconstruction
    low-pass filter, buffer the output, and measure ripple/frequency
    response.
4.  **Audio output stage:** connect a suitable amplifier to the
    conditioned DAC output and drive a small speaker; measure output
    level and distortion.

Include schematics, component calculations, wiring instructions, safe
voltage limits, expected oscilloscope traces, and troubleshooting. Never
connect headphones or a speaker directly to a DAC pin.

### I2S treatment on UNO R4 Minima

Teach I2S concepts: BCLK, LRCLK/WS, SDATA, MCLK, framing, sample widths,
stereo slots, and codec architecture. Investigate the RA4M1 SSIE
peripheral using the MCU documentation. Do not promise a hands-on I2S
lab until the complete signal set is verified as routed to accessible
UNO R4 Minima pins and supported by the chosen software/toolchain. Use
the board's ADC/DAC and external analog circuits for the core practical
audio labs.

**Final project options:** analog audio input/output interface with DSP,
programmable waveform generator, FIR/IIR processor, sensor acquisition
system, or real-time spectrum analyzer.

------------------------------------------------------------------------

# Course 4 --- ESP32-S3: Embedded Systems, DSP, and Digital Audio

**Target hardware:** ESP32-S3 development board, preferably Espressif
ESP32-S3-DevKitC-1 or a clearly documented equivalent.

**Purpose:** Build a complete embedded audio system, from MCU
architecture and FreeRTOS through I2S, DMA, real-time DSP, microphone
capture, and digital audio playback.

**Development approach:** Use ESP-IDF as the primary framework and
Arduino-ESP32 as a secondary comparison. Teach the learner to use the
official ESP-IDF drivers and APIs rather than depending exclusively on
high-level Arduino libraries.

**Hardware facts to respect:** ESP32-S3 uses dual-core Xtensa LX7
processors, supports Wi-Fi and Bluetooth LE, and provides I2S
peripherals with DMA support. It does not have a general-purpose
built-in analog DAC like the original ESP32. For audio output, use an
external I2S DAC/amplifier or codec. Verify the exact development board,
pin availability, PSRAM presence, and module variant before designing
labs.

### Modules

1.  **ESP32-S3 architecture and development environment** --- SoC
    architecture, dual-core MCU, memory, peripherals, ESP-IDF setup,
    build/flash workflow, and project structure.
2.  **Embedded C/C++ and memory architecture** --- Static/dynamic
    allocation, stack/heap, internal RAM, optional PSRAM, Flash, NVS,
    buffers, and memory debugging.
3.  **GPIO, interrupts, and peripheral routing** --- GPIO matrix, pin
    configuration, interrupts, electrical limits, event handling, and
    peripheral signal routing.
4.  **Timers and PWM** --- Hardware timers, LEDC PWM, clocking, timing
    accuracy, and actuator control.
5.  **FreeRTOS and multitasking** --- Tasks, priorities, queues,
    semaphores, mutexes, event groups, synchronization, core affinity,
    and real-time scheduling.
6.  **ADC and analog interfacing** --- ADC configuration, calibration,
    attenuation, noise, input limits, external DAC options, and safe
    analog acquisition.
7.  **UART, SPI, and I2C** --- Serial drivers, bus protocols, external
    sensors, peripheral integration, and logic-analyzer debugging.
8.  **DSP foundations on ESP32-S3** --- Sampling, quantization,
    discrete-time signals, convolution, signal statistics, and
    Python/MATLAB reference implementations.
9.  **I2S digital audio interface** --- I2S framing, BCLK, LRCLK/WS,
    SDATA, MCLK, master/slave modes, mono/stereo, sample widths, clock
    configuration, and codec/microphone integration.
10. **DMA-based audio streaming** --- I2S DMA, descriptors,
    circular/double buffers, continuous capture/playback, task
    synchronization, underruns/overruns, latency, and throughput.
11. **FIR, IIR, and FFT on ESP32-S3** --- Filter design, biquads, FFT,
    windows, spectral analysis, DSP libraries, numerical accuracy, and
    execution-time optimization.
12. **Advanced embedded audio processing** --- Parametric EQ, gain,
    mixing, envelope tracking, compression fundamentals, audio effects,
    noise-reduction concepts, and parameter updates.
13. **Final ESP32-S3 audio DSP project** --- Build a complete digital
    audio system with I2S input/output, DMA, DSP, testing, and
    performance analysis.

### Required ESP32-S3 hardware labs

Use suitable modules, with exact pin assignments checked for the
selected board:

-   **INMP441 or equivalent I2S microphone:** digital audio input.
-   **MAX98357A or equivalent I2S amplifier:** digital audio output to a
    small speaker.
-   **External I2S codec/DAC:** optional more advanced audio
    input/output.
-   Breadboard, jumper wires, speaker, and appropriate power supply.

### Practical I2S exercises

1.  Configure I2S master mode and generate/transmit a digital sine wave.
2.  Connect an I2S amplifier and play the generated tone.
3.  Connect an I2S microphone and capture audio samples.
4.  Stream captured samples to a PC for inspection.
5.  Implement continuous I2S receive and transmit using DMA.
6.  Add digital gain and FIR/IIR filtering.
7.  Implement double-buffered audio processing in a FreeRTOS task.
8.  Measure latency, CPU utilization, dropped samples, and buffer
    errors.

**Final project options:**

-   Real-time I2S digital audio effects processor.
-   Multi-band parametric equalizer.
-   FFT spectrum analyzer.
-   I2S audio acquisition and Wi-Fi streaming system.

------------------------------------------------------------------------

# Course 5 --- Algorithm Development for Embedded Systems (C/C++)

**Target learner:** A second-year Electrical Engineering student who
already has general coding experience but has never formally studied
algorithms or data structures. Start from absolute beginner level in
algorithmic thinking. Do not assume familiarity with pseudocode, Big O,
complexity analysis, common data structures, or algorithm design
paradigms.

**Target outcome:** Build the skills expected of a strong junior
algorithm developer / embedded software engineer: translate problem
statements into algorithms, select suitable data structures, reason
about correctness, analyze time and space complexity, prototype in
Python, implement in embedded C, test systematically, and optimize
against real hardware constraints.

**Primary embedded target:** TI MSP-EXP430G2 LaunchPad with MSP430G2553.

**Languages and workflow:**

-   Python is used for proof-of-concept implementations, test-data
    generation, reference behavior, and experimentation.
-   Embedded C is the primary implementation language on the MSP430.
-   C++ is taught progressively, primarily through host-based exercises
    and projects. Cover relevant modern C++ features and standard
    library concepts, while clearly distinguishing what is practical on
    a tiny MCU and what depends on compiler/toolchain support.
-   Do not translate Python line by line into C. Teach the learner to
    preserve algorithmic behavior while redesigning the implementation
    for fixed-width types, bounded memory, and target constraints.

**Hardware constraints:** MSP430G2553 is a 16-bit MCU operating at up to
16 MHz, with 16 KB Flash and 512 bytes RAM. It has no hardware FPU. Use
these constraints throughout the course as real engineering constraints.
Verify exact board, compiler, linker, and toolchain details against
official documentation.

## Mandatory learning and exercise methodology

Every major algorithm exercise must follow this sequence:

1.  **Problem understanding:** State the problem, inputs, outputs,
    constraints, assumptions, and edge cases.
2.  **Algorithm design:** Explain the approach in plain language, work
    through examples, and write pseudocode before implementation.
3.  **Python proof of concept:** Implement the algorithm in Python and
    validate it with representative, boundary, and adversarial tests.
4.  **Correctness reasoning:** Explain why the algorithm works. Use
    invariants, preconditions, postconditions, induction, or other
    appropriate reasoning as the learner progresses.
5.  **Complexity analysis:** Analyze time and space complexity. Include
    best, average, and worst cases where meaningful.
6.  **Data-structure justification:** Explain why the chosen data
    structure fits the problem and compare it with at least one
    reasonable alternative.
7.  **Embedded C implementation:** Implement the algorithm for the
    MSP430 using fixed-width types, explicit capacity limits, safe
    interfaces, and appropriate memory strategies.
8.  **Differential validation:** Run equivalent test vectors against
    Python and embedded C implementations and investigate discrepancies.
9.  **Measurement:** Measure or estimate execution cycles/time, RAM,
    stack, and Flash use where technically possible.
10. **Engineering report:** Document complexity, correctness, measured
    resource use, limitations, and trade-offs.

For every exercise, provide a beginner-friendly explanation, a worked
example, pseudocode, Python starter code, a separate Python solution,
embedded C starter code, a separate embedded C solution, expected
results, test cases, complexity analysis, embedded resource analysis,
common mistakes, and debugging guidance. Do not reveal solutions in
learner-facing exercise files.

## Mandatory algorithm-engineering requirements

These requirements apply from the first modules onward, at a level
appropriate to the learner's current knowledge:

-   Analyze time complexity and space complexity, not just whether code
    produces the correct output.
-   Explain Big O, Big Theta, and Big Omega progressively and
    accurately.
-   Analyze best-case, average-case, and worst-case behavior where
    applicable.
-   Distinguish auxiliary space from total memory requirements.
-   Consider stack use, static storage, dynamic allocation, memory
    overhead, fragmentation, alignment, and allocation failure.
-   Consider execution-time determinism, worst-case execution time,
    latency, throughput, deadlines, and jitter when relevant.
-   Explain the difference between asymptotic complexity and measured
    execution time. An O(n) algorithm is not automatically fast enough
    for a real-time deadline.
-   Teach learners to estimate resource requirements before coding and
    compare estimates with actual measurements afterward.
-   Do not automatically choose the algorithm with the best theoretical
    asymptotic complexity. Choose the implementation that best satisfies
    the actual constraints.
-   Explicitly identify when dynamic memory allocation is inappropriate
    for a particular embedded use case and explain alternatives.
-   Never invent precise hardware measurements. Provide a measurement
    procedure and let the learner record results from their own target.

### Required data-structure analysis

Teach not only how to implement data structures, but when to use them
and when not to use them. For each substantial data-structure exercise,
cover:

-   Memory layout and per-element overhead.
-   Time complexity of lookup, insertion, deletion, traversal, and other
    relevant operations.
-   Fixed-capacity versus dynamically sized behavior.
-   Pointer and metadata overhead.
-   Allocation requirements and fragmentation risks.
-   Predictability and worst-case behavior.
-   Suitability for the MSP430's limited RAM.
-   At least one alternative and a reasoned selection.

Examples of recurring embedded trade-offs:

-   Static arrays: predictable memory and O(1) indexing, but fixed
    capacity and potentially expensive insertion/deletion.
-   Linked lists: flexible linking, but pointer overhead, O(n) lookup,
    and allocation/fragmentation concerns.
-   Circular buffers: bounded memory and efficient streaming, with
    explicit full/empty handling.
-   Hash tables: fast average lookup, but collision behavior, capacity,
    and memory overhead must be considered.
-   Binary heaps: efficient priority queues, with O(log n) insertion and
    removal and compact array-based storage.
-   Stacks and queues: simple access policies, but capacity and overflow
    behavior must be defined.

### Required terminology and communication skills

Introduce terminology progressively. For each important term, provide a
plain-language explanation, a precise definition, a worked example, and
an exercise that requires the learner to use it correctly.

Terminology must include, as appropriate:

-   Algorithm, data structure, abstraction, interface, invariant,
    precondition, postcondition, correctness.
-   Asymptotic analysis, Big O, Big Theta, Big Omega, best/average/worst
    case, auxiliary space, amortized complexity.
-   Stable sorting, in-place algorithm, recursion, iteration, call
    stack.
-   Divide and conquer, greedy algorithm, dynamic programming,
    overlapping subproblems, optimal substructure.
-   Deterministic algorithm, worst-case execution time, latency,
    throughput, deadline, jitter.
-   Memory fragmentation, allocation overhead, memory alignment, static
    storage, stack, heap.
-   Fixed-point arithmetic, quantization, saturation, overflow,
    precision, numerical error.
-   Time-space trade-off, scalability, bounded execution, resource
    budget.

The learner should be able to explain these concepts in technical
discussions, code reviews, and engineering documentation.

## Modules

### Stage I --- Learning to think algorithmically

1.  **Introduction to algorithm development**
    -   What an algorithm is; algorithm versus implementation.
    -   Inputs, outputs, constraints, assumptions, and expected
        behavior.
    -   Breaking problems into smaller steps.
    -   Sequential execution, branches, loops, and state.
    -   Tracing algorithms manually.
    -   Pseudocode and flowcharts.
    -   Edge cases and simple correctness reasoning.
    -   Python POC: maximum, minimum, average, counting occurrences.
    -   MSP430 C: implement the same functions with arrays and debugger
        inspection or UART output.
2.  **Mathematical foundations for algorithms**
    -   Binary, decimal, and hexadecimal representation.
    -   Integer arithmetic, signed/unsigned values, and overflow.
    -   Modulo arithmetic, divisibility, powers, and logarithms.
    -   Summations and introductory recurrence relations.
    -   Prime numbers, GCD, LCM, and integer factorization.
    -   Introductory mathematical induction.
    -   Python POC: implement number-theory utilities and test
        boundaries.
    -   MSP430 C: fixed-width implementations; investigate overflow,
        intermediate types, and safe arithmetic.
3.  **Understanding algorithm complexity**
    -   Why efficiency matters.
    -   Counting operations and identifying dominant growth.
    -   Big O, Big Theta, and Big Omega from first principles.
    -   O(1), O(log n), O(n), O(n log n), O(n\^2), and exponential
        growth.
    -   Best, average, and worst cases.
    -   Nested loops, recursion, and introductory recurrence analysis.
    -   Time complexity versus space complexity.
    -   Python POC: compare multiple solutions and benchmark increasing
        input sizes.
    -   MSP430 C: measure execution using a hardware timer or GPIO
        timing; compare measured results with theoretical predictions.
4.  **Problem-solving methods and correctness**
    -   Translating a statement into inputs, outputs, and constraints.
    -   Brute force, decomposition, and incremental improvement.
    -   Pseudocode and structured algorithm descriptions.
    -   Preconditions, postconditions, loop invariants, and assertions.
    -   Boundary-value and adversarial test design.
    -   Informal correctness arguments, then introductory proof
        techniques.
    -   Python POC: solve small problems using multiple approaches.
    -   MSP430 C: create reusable functions and validate with known
        vectors.

### Stage II --- Core data structures

5.  **Arrays and memory representation**
    -   Contiguous memory, indexing, pointer arithmetic, and layout.
    -   Static versus dynamic arrays.
    -   One- and multidimensional arrays.
    -   Traversal, insertion, deletion, search, and update.
    -   Bounds checking, alignment, and memory safety.
    -   Complexity of common array operations.
    -   Python POC: implement array operations and compare behavior.
    -   MSP430 C: static-array utilities; calculate memory use before
        coding.
6.  **Strings and character processing**
    -   ASCII and character encoding.
    -   Null-terminated strings and C string representation.
    -   Traversal, comparison, copying, and concatenation.
    -   Substrings, pattern matching, and tokenization.
    -   Parsing structured input.
    -   Buffer boundaries, termination, and safe string handling.
    -   Python POC: string utilities and a basic parser.
    -   MSP430 C: fixed-size buffers, explicit lengths, and strict
        bounds.
7.  **Pointers, linked lists, stacks, and queues**
    -   Pointers, structures, nodes, and memory ownership.
    -   Singly, doubly, and circular linked lists.
    -   Stack (LIFO) and queue (FIFO) abstractions.
    -   Circular queues and ring buffers.
    -   Static storage versus dynamic allocation.
    -   Operation complexity and pointer/memory overhead.
    -   Python POC: implement and test each abstraction.
    -   MSP430 C: fixed-capacity stack/queue and a linked list backed by
        a fixed memory pool; compare memory cost and predictability.
8.  **Hash tables, heaps, and priority queues**
    -   Hash functions, collisions, chaining, and open addressing.
    -   Linear probing, lookup, insertion, and deletion.
    -   Sets and maps as abstractions.
    -   Binary heaps and priority queues.
    -   Average versus worst-case behavior.
    -   Capacity, load factor, metadata, and memory overhead.
    -   Python POC: implement a hash table and binary heap.
    -   MSP430 C: fixed-capacity hash table and heap; justify memory
        layout and collision strategy.

### Stage III --- Essential algorithms

9.  **Searching algorithms**
    -   Linear search and binary search.
    -   Preconditions for searching sorted data.
    -   Lower bound, upper bound, first/last occurrence.
    -   Search in rotated arrays.
    -   Interpolation search and its assumptions.
    -   Correctness invariants and complexity.
    -   Python POC: implement and test all covered searches.
    -   MSP430 C: implement with fixed-width indices and measure
        runtime.
10. **Sorting algorithms: foundations**
    -   Sorting problem, stability, in-place behavior, and auxiliary
        storage.
    -   Bubble sort, selection sort, insertion sort, and Shell sort.
    -   Best, average, and worst-case complexity.
    -   Nearly sorted, reversed, random, and duplicate-heavy inputs.
    -   Python POC: implement and benchmark the algorithms.
    -   MSP430 C: measure cycles and memory; choose based on dataset
        size and constraints, not only asymptotic complexity.
11. **Advanced sorting algorithms**
    -   Merge sort, quick sort, and heap sort.
    -   Counting sort and radix sort.
    -   Partitioning and pivot selection.
    -   Recursive and iterative implementations.
    -   Stability, auxiliary memory, stack depth, and worst-case
        behavior.
    -   Python POC: implement, test, and benchmark.
    -   MSP430 C: use static buffers where appropriate; assess stack,
        RAM, Flash, and worst-case runtime.
12. **Recursion and backtracking**
    -   Recursive functions, base cases, and recursive call stacks.
    -   Recursion trees and recurrence relations.
    -   Stack overflow and bounded stack use.
    -   Iterative alternatives.
    -   Backtracking, permutations, combinations, and constraint search.
    -   Maze-solving and small search problems.
    -   Python POC: recursive and iterative implementations.
    -   MSP430 C: bounded-depth implementations and iterative
        alternatives; measure stack impact.
13. **Bit manipulation and bitwise algorithms**
    -   Binary representation and bitwise operators.
    -   Masks, setting, clearing, toggling, and testing bits.
    -   Shifts, packed data, and bit fields.
    -   Population count and finding set bits.
    -   Circular shifts and bitwise algorithm patterns.
    -   Integer width, signed shifts, and
        undefined/implementation-defined behavior to avoid in C.
    -   Python POC: bit utilities checked against simple reference
        logic.
    -   MSP430 C: register-oriented operations and compact data
        structures.

### Stage IV --- Algorithm design techniques

14. **Divide and conquer**
    -   Divide, solve, and combine.
    -   Recurrence relations and recursion trees.
    -   Master theorem introduction.
    -   Binary search, merge sort, and quick sort revisited.
    -   Choosing recursive versus iterative implementations.
    -   Python POC: solve problems with divide and conquer.
    -   MSP430 C: implement selected algorithms with explicit stack and
        memory budgets.
15. **Greedy algorithms**
    -   Greedy choice, local versus global optimum.
    -   Greedy-choice property and optimal substructure.
    -   Activity selection and interval scheduling.
    -   Coin-change counterexamples.
    -   Introductory minimum spanning tree applications.
    -   Proving when a greedy choice is valid.
    -   Python POC: compare greedy solutions with brute force on small
        datasets.
    -   MSP430 C: bounded-array implementations and runtime analysis.
16. **Dynamic programming**
    -   Overlapping subproblems and optimal substructure.
    -   State definition and transition relations.
    -   Memoization and tabulation.
    -   Fibonacci, knapsack, coin change, and longest common
        subsequence.
    -   Time/space trade-offs and memory optimization.
    -   Python POC: recursive, memoized, and tabulated solutions.
    -   MSP430 C: static memory, compact state, bounded inputs, and
        measured resource use.
17. **Graph representations and algorithms**
    -   Graph terminology; directed, undirected, weighted, and
        unweighted.
    -   Adjacency matrices and adjacency lists.
    -   BFS, DFS, connected components, and cycle detection.
    -   Dijkstra shortest paths.
    -   Prim and Kruskal minimum spanning trees.
    -   Complexity depends on representation; compare memory costs.
    -   Python POC: graph toolkit and selected graph algorithms.
    -   MSP430 C: fixed-capacity graph representation; choose a compact
        representation and document limits.
18. **Common algorithmic problem-solving patterns**
    -   Sliding window and two pointers.
    -   Prefix sums and difference arrays.
    -   Fast/slow pointers and cycle detection.
    -   Monotonic stacks.
    -   Binary search on an answer.
    -   Interval merging and top-K problems.
    -   Recognizing and combining patterns.
    -   Python POC: progressively harder pattern-based problems.
    -   MSP430 C: selected bounded implementations with complexity and
        resource analysis.

### Stage V --- Embedded algorithm engineering

19. **Embedded C for algorithm developers**
    -   Fixed-width integer types and exact-width assumptions.
    -   Integer promotions, conversions, signedness, and overflow.
    -   Pointers, arrays, structs, unions, enums, and function pointers.
    -   Const correctness and safe interfaces.
    -   Static storage, stack, heap, and memory ownership.
    -   Header/source separation and reusable libraries.
    -   Defensive programming and compiler warnings.
    -   Python POC: reference behavior and test generators.
    -   MSP430 C: reusable algorithm library with static allocation and
        documented interfaces.
20. **Fixed-point arithmetic and numerical algorithms**
    -   Floating-point versus integer arithmetic.
    -   Fixed-point representation and Q formats.
    -   Scaling, quantization, rounding, and truncation.
    -   Saturation, overflow, precision, and error accumulation.
    -   Lookup tables and integer square root.
    -   Efficient arithmetic and numerical stability.
    -   Python POC: fixed-point emulation compared with floating-point
        references.
    -   MSP430 C: fixed-point utilities and numerical algorithms;
        measure error, cycles, and memory.
21. **Real-time and streaming algorithms**
    -   Batch versus streaming processing.
    -   Incremental processing and bounded work per input.
    -   Circular buffers and sliding windows.
    -   Running average, minimum, maximum, and statistics.
    -   Peak/event detection and state machines.
    -   Latency, throughput, deadlines, jitter, and worst-case
        execution.
    -   Timer-driven acquisition, interrupts, and ISR/task boundaries.
    -   Python POC: simulate streams and verify incremental results.
    -   MSP430 C: ADC/timer-driven algorithms and ring buffers; measure
        latency and missed samples.
22. **Optimization for embedded targets**
    -   Profile before optimizing.
    -   CPU cycles, RAM, stack, Flash, and compiler map files.
    -   Compiler optimization levels and generated assembly inspection.
    -   Loop, branch, memory-access, and function-call costs.
    -   Lookup tables versus computation.
    -   Code-size versus speed trade-offs.
    -   Worst-case execution time and bounded algorithms.
    -   Python POC: compare algorithmic alternatives and establish
        reference behavior.
    -   MSP430 C: optimize selected algorithms and document measured
        changes without sacrificing correctness.

### Stage VI --- Professional algorithm development

23. **Testing, verification, and engineering quality**
    -   Unit and integration testing.
    -   Test-driven development and regression tests.
    -   Reference implementations and test vectors.
    -   Boundary, randomized, and property-based testing.
    -   Differential testing between Python and C.
    -   Invariants, assertions, and correctness arguments.
    -   Debugging memory errors and undefined behavior.
    -   Reproducible benchmarks and Git workflows.
    -   Technical documentation and code review.
    -   Python POC: automated test suite and test-data generator.
    -   MSP430 C: run equivalent vectors, compare results, and document
        discrepancies and resource measurements.
24. **Final engineering project: embedded algorithm library**
    -   Build a reusable, modular algorithm library for MSP430G2553.
    -   Include array/data-processing utilities, search and sorting,
        bitwise utilities, numerical/fixed-point functions, at least one
        streaming algorithm, and at least one state-machine algorithm.
    -   Provide Python reference implementations and automated tests.
    -   Provide embedded C implementations with documented APIs.
    -   Define input and resource limits before implementation.
    -   Measure execution time, RAM, stack, and Flash.
    -   Compare algorithmic alternatives and justify design decisions.
    -   Deliver a benchmark report, test report, memory report,
        technical documentation, and a working hardware demonstration.

## C and C++ language progression

Teach C as the primary embedded implementation language. Teach C++
alongside it, primarily on the host computer, and introduce embedded C++
only where the compiler, toolchain, and resource constraints make it
appropriate.

**C topics:** pointers, arrays, structs/unions, memory management,
static allocation, function pointers, bitwise operations, fixed-width
types, const correctness, modular libraries, and safe interfaces.

**C++ topics:** classes and objects, constructors/destructors,
references, templates, STL containers and algorithms, iterators, RAII,
`constexpr`, move semantics, and generic programming. Explain the
runtime/memory implications of abstractions and which features are
appropriate for small embedded targets.

## Required engineering report for every major assignment

Each major assignment must produce a concise report containing:

1.  Problem statement, inputs, outputs, constraints, and assumptions.
2.  Algorithm description and pseudocode.
3.  Data-structure choice and justification.
4.  Correctness reasoning and edge cases.
5.  Best/average/worst-case time complexity where applicable.
6.  Auxiliary space and total memory analysis.
7.  Python POC results and test coverage.
8.  Embedded C implementation decisions.
9.  Measured or verified execution time/cycles.
10. RAM, stack, and Flash usage.
11. Comparison with at least one alternative.
12. Limitations, trade-offs, and possible improvements.

## Course 5 project structure

Use the following structure for this course:

-   `README.md` --- learner level, goals, prerequisites, setup,
    hardware, and module map.
-   `syllabus.md` --- this complete 24-module syllabus.
-   `modules/` --- one directory per module, with theory and worked
    examples.
-   `exercises/` --- learner-facing exercises and independent
    assignments.
-   `python_poc/` --- starter implementations, reference solutions,
    tests, and test-data generators.
-   `embedded_c/` --- MSP430 starter projects, implementations, tests,
    and build instructions.
-   `solutions/` --- separate, fully explained solutions.
-   `projects/` --- final project specifications and starter code.
-   `benchmarks/` --- timing, memory, and comparison reports.
-   `references/` --- textbooks, official documentation, and technical
    references.
-   `tools/` --- scripts for testing, generating vectors, and analyzing
    results.

------------------------------------------------------------------------

------------------------------------------------------------------------

# Recommended learning order

1.  **TI MSP430 Course 1:** Learn the fundamentals of microcontroller
    programming and low-level peripherals.
2.  **TI MSP430 Course 2:** Learn DSP implementation under strict memory
    and compute constraints.
3.  **Arduino UNO R4 Minima:** Expand into ARM Cortex-M4, DMA, analog
    circuitry, and more capable embedded DSP.
4.  **ESP32-S3:** Learn FreeRTOS, I2S, DMA audio streaming, and complete
    embedded digital-audio applications.
5.  **Algorithm Development for Embedded Systems:** Start this course
    from its first module and progress alongside or after the platform
    courses. It develops the general algorithmic thinking, data
    structures, complexity analysis, and embedded implementation skills
    that complement the DSP courses.

# Important instructions to Cursor

Generate each course as a separate directory. Do not merge the four
syllabuses into one course.

For each course, create: - `README.md` --- course overview,
prerequisites, hardware, setup, and module map. - `syllabus.md` --- the
complete 13-module syllabus. - `modules/` --- one descriptive lesson
folder per module. - `exercises/` --- learner-facing exercises and
assignments. - `solutions/` --- separate explained solutions. -
`projects/` --- final project specifications and starter code. -
`references/` --- datasheets, official manuals, and technical
references. - `tools/` --- helper scripts and test/reference utilities
where appropriate.

Start by creating the complete course structure and detailed module
plans. Then develop the material module by module. Do not generate
shallow placeholder lessons: every module must contain enough
explanation and practical work to be genuinely useful for independent
study.
