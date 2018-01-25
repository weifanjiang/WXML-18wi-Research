# Metropolis Algorithm & Ising Model

This file contains specifications of first phase of project - implementing <b>Metropolis Algortihm</b> and <b>Ising Model</b> in Python, which can be used to simulate a <i>random sample</i> on an input $n$ by $m$ grid-shaped graph.

<h2>Input of program</h2>

* <code>int</code> $n$: width of input 2D grid.
* <code>int</code> $m$: height of input 2D grid.
* <code>int</code> $\beta$: constant used for calculating
* <code>int</code> $X$: length of random walk chain

<h2>Constructs the larger graph</h2>

Let $G = \big\{V, E\big\}$ be the initial input graph.<br />
Suppose each vertex $v \in V$ has two possible states: $\big\{-1, 1\big\}$, we would like to construct a much larger graph $\tilde{G} = \big\{\tilde{V}, \tilde{E}\big\}$ such that:
* Each $\tilde{v} \in \tilde{V}$ represents a possible state of graph $G$. Since $G$ has $n \times m$ vertices and each vertex has 2 possibilities, <code>size(</code>$\tilde{V}$<code>) = </code>$2^{mn}$.
* Each $\tilde{e} \in \tilde{E}$ connects two vertices in $\tilde{V}$ if the two vertices only <b>differ by 1 state</b>.


<h2>Simulate random walk</h2>

<h2>Graphically represent sample</h2>