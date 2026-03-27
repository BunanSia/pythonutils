# My personal Python util collection

## Introduction
Including several basic python utils like crawler, small language training model

# 🧠 Small Language Model (SLM) Implementation Guide

This document explains the architecture and logic of the `pytorch_try.py` script. The model is a character-level **Generative Pre-trained Transformer (GPT)** designed to learn patterns in text and generate similar content.

---

## ⚙️ 1. Configuration & Hyperparameters
The script begins by setting the "DNA" of the model. These values determine its size and intelligence:

* **`block_size` (8):** The context window. The model looks at 8 characters to predict the 9th.
* **`n_embd` (32):** The dimensionality of the character vectors.
* **`n_head` (4):** Number of parallel "attention" streams.
* **`n_layer` (4):** How many Transformer blocks are stacked vertically.

---

## 🔡 2. Tokenization: Turning Text into Math
Machines don't read letters; they process tensors.
1.  **Vocabulary:** We identify every unique character in the text (e.g., `a, b, c, \n, !`).
2.  **Mapping:** * `stoi`: String-to-Integer (e.g., 'S' -> 24)
    * `itos`: Integer-to-String (e.g., 24 -> 'S')
3.  **Self-Supervision:** The model is "self-supervised" because the labels are the text itself, shifted by one character. If the input is `SHAKES`, the model learns that `S` is followed by `H`, `SH` is followed by `A`, and so on.

---

## 🏗️ 3. The Architecture

### A. The Attention Head (`Head` class)
This is where the model "focuses." It uses three vectors for every character:
1.  **Query ($Q$):** What am I looking for?
2.  **Key ($K$):** What information do I have?
3.  **Value ($V$):** If I'm relevant, what do I contribute?

The "affinity" or importance of a character relative to others is calculated as:
$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$



### B. Multi-Head Attention
Instead of one big head, we use 4 smaller heads. This allows the model to look for 4 different types of patterns at the same time (e.g., one head for grammar, one for punctuation).

### C. The Feed-Forward Network (`FeedForward` class)
After characters communicate via attention, they need time to "process" that info. This is a simple neural network with a **ReLU** activation that operates on each character position independently.

### D. The Block (`Block` class)
This is the fundamental unit of the Transformer. It combines:
1.  **LayerNorm:** Keeps the mathematical values stable.
2.  **Communication:** Multi-Head Attention.
3.  **Computation:** Feed-Forward network.
4.  **Residual Connections:** `x = x + self.sa(x)`. These allow gradients to flow easily through the network during training.

---

## 🚀 4. The Training Process
The model improves through an iterative loop:
1.  **Batching:** We take 32 random snippets of text.
2.  **Forward Pass:** The model guesses the next character for every position in those snippets.
3.  **Loss Calculation:** We compare the guess to the actual next character using **Cross Entropy**.
4.  **Backpropagation:** The **AdamW** optimizer adjusts the weights to make the guess slightly more accurate next time.

---

## ✍️ 5. Generation
To generate text, we provide a "seed" (like a newline character). The model:
1.  Predicts the probabilities for the next character.
2.  **Samples** from that probability (choosing the most likely ones).
3.  Appends the result to the input and repeats.

---

## 🛠️ How to Run Locally
1. Save the Python script as `main.py`.
2. Ensure you have PyTorch installed: `pip install torch`.
3. Run the script: `python main.py`.

> **Note:** On a standard CPU, 5000 iterations may take 5–10 minutes. On a GPU, it will finish in seconds!