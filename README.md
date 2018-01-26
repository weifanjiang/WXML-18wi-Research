# WXML-18wi-Research

<ul id="top">
  <li><a href="#top">Overview</a></li>
  <li><a href="#Phase-1">Phase 1</a></li>
</ul>

This repository contains source code for <a href="http://wxml.math.washington.edu/">Washington Experimental Mathematics Lab</a>'s Winter 2018 Research Program: <u>Mathematics of Gerrymandering</u>, at the University of Washington.

<h2>Members</h2>
Faculty Mentor: Christopher Hoffman (Math)<br />
Graduate Mentor: Tejas Devanur<br />
Team Members: Leo Segovia, Alexander Robkin, Weifan Jiang, Namyoung Kim

<h2>Project Discription</h2>
Districting and Gerrymandering have been in the news a lot recently, and the mathematical modeling of how to draw districts is a very hot topic. This project will look at the space of all possible redistrictings of a state to see whether the current plan is an outlier. It will involve probability and computing skills.

<hr />

<h2 id="Phase-1">Phase 1: Metropolis Algorithm & Ising Model</h2>

This portion contains specifications of first phase of project - implementing <b>Metropolis Algortihm</b> and <b>Ising Model</b> in Python, which can be used to simulate a <i>random sample</i> on an input $n$ by $m$ grid-shaped graph.

<h2>Input of program</h2>

* <code>int</code> $n$: height of input 2D grid.
* <code>int</code> $m$: width of input 2D grid.
* <code>int</code> $\beta$: constant used for calculating
* <code>int</code> $N$: length of random walk chain

<h2>Constructs the larger graph</h2>

Let $G = \big\{V, E\big\}$ be the initial input graph.<br />
Suppose each vertex $v \in V$ has two possible states: $\big\{-1, 1\big\}$, we would like to construct a much larger graph $\tilde{G} = \big\{\tilde{V}, \tilde{E}\big\}$ such that:
* Each $\tilde{v} \in \tilde{V}$ represents a possible state of graph $G$. Since $G$ has $n \times m$ vertices and each vertex has 2 possibilities, <code>size(</code>$\tilde{V}$<code>) = </code>$2^{mn}$.
* Each $\tilde{e} \in \tilde{E}$ connects two vertices in $\tilde{V}$ if the two vertices only <b>differ by 1 state</b>.
* We would also like to compute a <b>probability vector</b> for $\tilde{G}$, which can be computed with methods of <b>Ising Model</b>:
    * First, we compute the unweighted value, $\hat{f_{\beta}}(\tilde{v})$ for each $\tilde{v} \in \tilde{V}$. Since each $\tilde{v}$ represents a unique state of $G$ (which just means a way to assign $1$ and $-1$ to each vertex in $G$).<br />
    Let $f(v)$ represent the value assigned to $v \in V$, within some $\tilde{v}$, we can compute the unweighted probability with:<br />
    $\ln(\hat{f_{\beta}}(\tilde{v})) = \beta\sum_{(v_1, v_2) \in E)}f(v_1) \cdot f(v_2)$.
    * Now, we compute the weighted value. Since we want the probability of every $\tilde{v} \in \tilde{V}$ to sum to $1$, we compute the sum of all probabilities of each $\tilde{v}$:<br />
    $C = \sum_{\tilde{v} \in \tilde{V}} \hat{f_{\beta}}(\tilde{v})$.<br />
    Then each $\tilde{v} \in \tilde{V}$'s normalized probability value is:<br />
    $f_{\beta}(\tilde{v}) = \frac{1}{C} \cdot \hat{f_{\beta}}(\tilde{v})$.

<h2>Simulate random walk</h2>

After constructing $\tilde{G}$, we would sample from $\tilde{G}$ by ultimately selecting a vertex from $\tilde{G}$ as our sample to present (this sample represents a state of original input graph $G$, so it can mean something like which party each presinct voted for).<br />
The basic idea is that we start from a random $\tilde{v}_0 \in \tilde{V}$ at timestamp $0$, noted as $X_0 = \tilde{v}_0$.<br />
Then, we can decide to either move or stay at each timestamp. Which can be implemented by the following algorithm:

Suppose $X_i = \tilde{v}_{a}$, then at timestamp $i + 1$:
* Randomly choose a direct neighbor of $\tilde{v}_a$, say $\tilde{v}_b$ as the <code>candidate</code> of next movement.
* Decide if we make the move by using the probability vector assiciated with $\tilde{G}$ by computing the probability ratio <code>r</code>$= \frac{f_{\beta}(\tilde{v}_b)}{f_{\beta}(\tilde{v}_a)}$:
    * if <code>r >= 1</code>, accept <code>candidate</code>. In other words, $X_{i + 1} = \tilde{v}_b$.
    * if <code>r < 1</code>, then we accept <code>candidate</code> with probability <code>r</code>, and reject <code>candidate</code> with probability <code>1 - r</code>. In other words:
        * for probability <code>r</code>, $X_{i + 1} = \tilde{v}_b$.
        * for probability <code>1 - r</code>, $X_{i + 1} = X_i = \tilde{v}_a$.

Repeat this process for $N$ times until we get $X_N = \tilde{v}_N$ which $\tilde{v}_N \in \tilde{V}$ is the sample.

<h2>Graphically represent sample</h2>

After obtaining $X_N = \tilde{v}_N$, since $\tilde{v}_N$ represents a state of original input graph $G$, we can color the vertices of $G$ based on each vertex's assigned value (either $1$ or $-1$) differently. Since $G$ has the shape of 2D grid, we will ultimately show a grid with different colors, as the result of <b>phase 1</b>.

Done with phase 1!