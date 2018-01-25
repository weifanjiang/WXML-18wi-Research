# WXML-18wi-Research

<ul id="top">
  <li><a href="#top">Overview</a></li>
  <li><a href="#Phase-1">Phase 1</a></li>
</ul>

This repository contains source code for <a href="http://wxml.math.washington.edu/">Washington Experimental Mathematics Lab</a>'s Winter 2018 Research Program: Mathematics of Gerrymandering.

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