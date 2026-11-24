# MAT235 Week 10 Answers, Worked Exercises, Self-Test, and Coverage Appendix

> Companion to [Study-Notes.md](Study-Notes.md) covering **§14.7 Second-Order Partial Derivatives** and **§14.8 Differentiability**.

## Contents

1. [Teaching-Example Solutions (PT-10.1 – PT-10.7)](#1-teaching-example-solutions)
2. [Slide Questions and Solutions (`Week10-sol.pdf`)](#2-slide-questions-and-solutions)
3. [Textbook Exercises and Solutions (§14.7 & §14.8)](#3-textbook-exercises-and-solutions)
   - [§14.7 Requested Exercises (21 exercise numbers)](#31-147-requested-exercises)
   - [§14.8 Requested Exercises (7 exercise numbers)](#32-148-requested-exercises)
4. [Original Self-Test](#4-original-self-test)
   - [Self-Test Questions](#41-self-test-questions)
   - [Self-Test Answers](#42-self-test-answers)
5. [Coverage Appendix](#5-coverage-appendix)

---

## 1. Teaching-Example Solutions

### PT-10.1: Computing Second-Order (and Higher-Order) Partial Derivatives

- **Question:** [Study-Notes.md — PT-10.1](Study-Notes.md#pt-101-computing-second-order-and-higher-order-partial-derivatives) ($f(x,y) = x^3 y^2 - 4y e^{2x}$).
- **Solution:**
  1. First-order partials:
     $$f_x(x,y) = 3x^2 y^2 - 8y e^{2x}, \qquad f_y(x,y) = 2x^3 y - 4e^{2x}.$$
  2. Second-order partials:
     $$f_{xx}(x,y) = (f_x)_x = 6xy^2 - 16y e^{2x},$$
     $$f_{xy}(x,y) = (f_x)_y = 6x^2 y - 8e^{2x},$$
     $$f_{yx}(x,y) = (f_y)_x = 6x^2 y - 8e^{2x},$$
     $$f_{yy}(x,y) = (f_y)_y = 2x^3.$$
- **Final Answer:** $f_{xx} = 6xy^2 - 16y e^{2x}$, $f_{xy} = f_{yx} = 6x^2 y - 8e^{2x}$, $f_{yy} = 2x^3$.
- **Check:** $f_{xy}$ and $f_{yx}$ match identically, as guaranteed by Clairaut's Theorem since both are continuous everywhere on $\mathbb{R}^2$.

---

### PT-10.2: Estimating Second-Order Partial Derivatives from a Table or Gradient Data

- **Question:** [Study-Notes.md — PT-10.2](Study-Notes.md#pt-102-estimating-second-order-partial-derivatives-from-a-table-or-gradient-data) (estimate $f_{xy}(3,4)$ from the $3\times 3$ table).
- **Solution:**
  1. Use the centered difference in $y$ around $y = 4$ (with $y = 2$ and $y = 6$, $\Delta y = 6 - 2 = 4$):
     $$f_{xy}(3,4) \approx \frac{f_x(3,6) - f_x(3,2)}{6 - 2}.$$
  2. Estimate $f_x(3,6)$ and $f_x(3,2)$ using centered differences in $x$ (using $x = 1$ and $x = 5$, $\Delta x = 5 - 1 = 4$):
     $$f_x(3,6) \approx \frac{f(5,6) - f(1,6)}{5 - 1} = \frac{31 - 13}{4} = \frac{18}{4} = 4.5,$$
     $$f_x(3,2) \approx \frac{f(5,2) - f(1,2)}{5 - 1} = \frac{11 - 5}{4} = \frac{6}{4} = 1.5.$$
  3. Substitute into the outer quotient:
     $$f_{xy}(3,4) \approx \frac{4.5 - 1.5}{4} = \frac{3}{4} = 0.75.$$
- **Final Answer:** $f_{xy}(3,4) \approx 0.75$ (using $f(1,2)=5$, $f(5,2)=11$, $f(1,6)=13$, $f(5,6)=31$).
- **Check:** Computing $f_{yx}(3,4) \approx \frac{f_y(5,4) - f_y(1,4)}{5-1}$ with $f_y(5,4)\approx\frac{31-11}{4}=5$ and $f_y(1,4)\approx\frac{13-5}{4}=2$ gives $\frac{5-2}{4} = 0.75$, agreeing exactly.

---

### PT-10.3: Testing Whether Proposed Partial Derivatives Can Come from a Function

- **Question:** [Study-Notes.md — PT-10.3](Study-Notes.md#pt-103-testing-whether-proposed-partial-derivatives-can-come-from-a-function) ($f_x = 2xy + y^3$, $f_y = x^2 + 3xy^2 + 4x$).
- **Solution:**
  1. Suppose for contradiction that such a function $f(x,y)$ exists.
  2. Compute the mixed partial derivatives:
     $$f_{xy} = \frac{\partial}{\partial y}(2xy + y^3) = 2x + 3y^2,$$
     $$f_{yx} = \frac{\partial}{\partial x}(x^2 + 3xy^2 + 4x) = 2x + 3y^2 + 4.$$
  3. Both $f_{xy}$ and $f_{yx}$ are polynomials, hence continuous everywhere on $\mathbb{R}^2$. By Clairaut's Theorem, we would have $f_{xy}(x,y) = f_{yx}(x,y)$ everywhere.
  4. However, $2x + 3y^2 \neq 2x + 3y^2 + 4$ (their difference is $4 \neq 0$). Contradiction.
- **Final Answer:** **No**, no such function $f(x,y)$ exists.
- **Check:** Even without the $+4x$ term, $f(x,y) = x^2 y + xy^3$ would give $f_x = 2xy+y^3$ and $f_y = x^2+3xy^2$, confirming that the extra $+4x$ in $f_y$ breaks equality of mixed partials.

---

### PT-10.4: Verifying a Solution (or Parameter Relation) for a PDE

- **Question:** [Study-Notes.md — PT-10.4](Study-Notes.md#pt-104-verifying-a-solution-or-parameter-relation-for-a-pde) ($u(x,t) = e^{-kt}\cos(cx)$, heat equation $u_t = u_{xx}$, $c \neq 0$).
- **Solution:**
  1. Compute $u_t$ and $u_{xx}$:
     $$u_t = -k e^{-kt}\cos(cx),$$
     $$u_x = -c e^{-kt}\sin(cx), \qquad u_{xx} = -c^2 e^{-kt}\cos(cx).$$
  2. Substitute into $u_t = u_{xx}$:
     $$-k e^{-kt}\cos(cx) = -c^2 e^{-kt}\cos(cx) \iff (c^2 - k)e^{-kt}\cos(cx) = 0.$$
  3. Since $e^{-kt} > 0$ everywhere and $\cos(cx)$ is not identically zero (e.g., $\cos(0) = 1$), this holds for all $(x,t) \in \mathbb{R}^2$ if and only if $c^2 - k = 0$, i.e., $k = c^2$.
- **Final Answer:** $k = c^2$.
- **Check:** Plugging $k = c^2$ back in gives $u_t = -c^2 e^{-c^2 t}\cos(cx) = u_{xx}$ identically.

---

### PT-10.5: Constructing Degree-1 and Degree-2 Taylor Polynomials and Comparing Approximations

- **Question:** [Study-Notes.md — PT-10.5](Study-Notes.md#pt-105-constructing-degree-1-and-degree-2-taylor-polynomials-and-comparing-approximations) ($f(x,y) = x e^{2y}$ near $(1,0)$, evaluated at $(1.1, -0.05)$).
- **Solution:**
  **(a)** Compute the value and partial derivatives at $(a,b) = (1,0)$:

  | Derivative | Formula | Value at $(1,0)$ |
  |---|---|---|
  | $f(x,y)$ | $x e^{2y}$ | $1$ |
  | $f_x(x,y)$ | $e^{2y}$ | $1$ |
  | $f_y(x,y)$ | $2x e^{2y}$ | $2$ |
  | $f_{xx}(x,y)$ | $0$ | $0$ |
  | $f_{xy}(x,y)$ | $2e^{2y}$ | $2$ |
  | $f_{yy}(x,y)$ | $4x e^{2y}$ | $4$ |

  - Linear Taylor polynomial:
    $$L(x,y) = 1 + 1(x-1) + 2(y-0) = x + 2y.$$
  - Quadratic Taylor polynomial:
    $$Q(x,y) = 1 + (x-1) + 2y + \frac{0}{2}(x-1)^2 + 2(x-1)y + \frac{4}{2}y^2 = 1 + (x-1) + 2y + 2(x-1)y + 2y^2.$$

  **(b)** Evaluate at $(1.1, -0.05)$ (where $x-1 = 0.1$ and $y = -0.05$):
  - Exact: $f(1.1, -0.05) = 1.1\,e^{-0.1} \approx 0.995321$.
  - Linear: $L(1.1, -0.05) = 1.1 + 2(-0.05) = 1.000000$, error $|f - L| \approx 0.004679$.
  - Quadratic: $Q(1.1, -0.05) = 1 + 0.1 - 0.1 + 2(0.1)(-0.05) + 2(-0.05)^2 = 1 - 0.01 + 0.005 = 0.995000$, error $|f - Q| \approx 0.000321$.
- **Final Answer:** $L(x,y) = 1 + (x-1) + 2y$; $Q(x,y) = 1 + (x-1) + 2y + 2(x-1)y + 2y^2$; at $(1.1, -0.05)$, $Q = 0.995$ (error $\approx 0.000321$) is over $14\times$ more accurate than $L = 1.000$ (error $\approx 0.004679$).
- **Check:** $Q(1,0)=1$, $Q_x(1,0)=1$, $Q_y(1,0)=2$, $Q_{xx}(1,0)=0$, $Q_{xy}(1,0)=2$, $Q_{yy}(1,0)=4$ — all six derivatives match $f$ at $(1,0)$.

---

### PT-10.6: Showing a Function Is Not Differentiable at a Point (Without the Formal Definition)

- **Question:** [Study-Notes.md — PT-10.6](Study-Notes.md#pt-106-showing-a-function-is-not-differentiable-at-a-point-without-the-formal-definition) (test $f(x,y)=\sqrt{4x^2+y^2}$ and $g(x,y)=\frac{2x^2 y}{x^4+y^2}$ at $(0,0)$).
- **Solution:**
  - **(a)** Test $f_x(0,0)$ via the limit definition:
    $$f_x(0,0) = \lim_{h\to 0}\frac{f(h,0) - f(0,0)}{h} = \lim_{h\to 0}\frac{\sqrt{4h^2} - 0}{h} = \lim_{h\to 0}\frac{2|h|}{h}.$$
    As $h \to 0^+$, $\frac{2|h|}{h} = 2$; as $h \to 0^-$, $\frac{2|h|}{h} = -2$. The two one-sided limits disagree, so $f_x(0,0)$ does not exist. Because differentiability requires both partial derivatives to exist, **$f$ is not differentiable at $(0,0)$**.
  - **(b)** Test continuity of $g$ at $(0,0)$ using two paths:
    - Along the $x$-axis ($y = 0$, $x \neq 0$): $g(x,0) = \frac{0}{x^4} = 0 \to 0$.
    - Along the parabola $y = x^2$ ($x \neq 0$): $g(x, x^2) = \frac{2x^4}{x^4 + x^4} = 1 \to 1 \neq 0$.
    Since the path limits disagree, $\lim_{(x,y)\to(0,0)} g(x,y)$ does not exist, so $g$ is **not continuous** at $(0,0)$. Because differentiability implies continuity, **$g$ is not differentiable at $(0,0)$**.
- **Final Answer:** Neither $f$ nor $g$ is differentiable at $(0,0)$.
- **Check:** Geometrically, $f$ is an elliptic cone with a sharp vertex at $(0,0)$, and $g$ has a jump/ridge along $y=x^2$ — neither can be approximated by a plane at $(0,0)$.

---

### PT-10.7: Proving Differentiability via Continuity of Partial Derivatives

- **Question:** [Study-Notes.md — PT-10.7](Study-Notes.md#pt-107-proving-differentiability-via-continuity-of-partial-derivatives) ($f(x,y) = \ln(1 + x^2 + 2y^2)$).
- **Solution:**
  1. **Domain:** Since $1 + x^2 + 2y^2 \ge 1 > 0$ for all $(x,y) \in \mathbb{R}^2$, the domain of $f$ is all of $\mathbb{R}^2$.
  2. **Partial derivatives:**
     $$f_x(x,y) = \frac{2x}{1 + x^2 + 2y^2}, \qquad f_y(x,y) = \frac{4y}{1 + x^2 + 2y^2}.$$
  3. **Continuity of partials:** Both $f_x$ and $f_y$ are rational functions whose denominator $1 + x^2 + 2y^2$ is strictly positive everywhere on $\mathbb{R}^2$. Thus $f_x$ and $f_y$ exist and are continuous on all of $\mathbb{R}^2$ (in particular, on a small open disk around every point $(a,b) \in \mathbb{R}^2$).
  4. **Conclusion:** By the sufficient condition for differentiability, $f$ is differentiable everywhere on $\mathbb{R}^2$.
- **Final Answer:** Domain is $\mathbb{R}^2$, and $f$ is differentiable everywhere on $\mathbb{R}^2$.
- **Check:** At $(0,0)$, $f_x(0,0)=0$ and $f_y(0,0)=0$, with no $0/0$ denominator anywhere.

---

## 2. Slide Questions and Solutions

All in-scope original questions from `W10/lec/Week10-sol.pdf` (12 PDF pages; printed Slides 1–7 of 7) are accounted for below.

### Slide Q1 — Compute Second-Order Partial Derivatives (`Week10-sol.pdf`, PDF p. 2 / Slide p. 1, §14.7)
- **Statement:** Let $f(x,y) = x^2 y + 3y^2 e^x$. Compute all four second-order partial derivatives of $f$. *(Also asked in lecture: "What can be observed?")*
- **PT:** [PT-10.1](Study-Notes.md#pt-101-computing-second-order-and-higher-order-partial-derivatives)
- **Solution:**
  - $f_x = 2xy + 3y^2 e^x$, $\quad f_y = x^2 + 6y e^x$.
  - $f_{xx} = 2y + 3y^2 e^x$, $\quad f_{xy} = 2x + 6y e^x$, $\quad f_{yx} = 2x + 6y e^x$, $\quad f_{yy} = 6e^x$.
  - Observation: $f_{xy} = f_{yx}$ everywhere.

### Slide Q2 — Can These Be the Partial Derivatives of a Function? (`Week10-sol.pdf`, PDF p. 3 / Slide p. 2, §14.7)
- **Statement:** Does there exist a continuous function $f(x,y)$ such that $f_x = 3y^2 + x$ and $f_y = 6xy + 3x$?
- **PT:** [PT-10.3](Study-Notes.md#pt-103-testing-whether-proposed-partial-derivatives-can-come-from-a-function)
- **Solution:**
  Suppose such an $f$ exists. Then $f_{xy} = (f_x)_y = 6y$ and $f_{yx} = (f_y)_x = 6y + 3$. Both $6y$ and $6y+3$ are continuous everywhere on $\mathbb{R}^2$, so by equality of mixed partial derivatives we must have $f_{xy} = f_{yx}$. Since $6y \neq 6y + 3$, this is impossible. **Answer: No, there is no such function $f$.**

### Slide Q3 — Estimate Derivatives from a Table (`Week10-sol.pdf`, PDF p. 3 / Slide p. 2, §14.7)
- **Statement:** The table gives values of $f(x,y)$:

  | $x \backslash y$ | $2$ | $4$ | $6$ | $8$ |
  |---|---|---|---|---|
  | **$2$** | $2$ | $4$ | $6$ | $8$ |
  | **$4$** | $3$ | $6$ | $9$ | $12$ |
  | **$6$** | $4$ | $8$ | $12$ | $16$ |
  | **$8$** | $5$ | $10$ | $15$ | $20$ |

  Estimate the following, making clear which table values you use:
  (a) The directional derivative at $(4,4)$ in the direction of $\vec{v} = 2\vec{i} + 4\vec{j}$ (directly from the table without using the gradient).
  (b) $f_{xy}(4,4)$ (Hint: $f_{xy}(4,4) \approx \frac{\Delta f_x}{\Delta y}$).
- **PT:** [PT-10.2](Study-Notes.md#pt-102-estimating-second-order-partial-derivatives-from-a-table-or-gradient-data) (part (b); part (a) reviews §14.5 directional derivative directly from a table).
- **Solution:**
  - **(a)** Moving from $(4,4)$ by $\vec{v} = \langle 2, 4 \rangle$ lands at $(4+2, 4+4) = (6,8)$, a distance of $\|\vec{v}\| = \sqrt{(6-4)^2 + (8-4)^2} = \sqrt{20} = 2\sqrt{5}$. Using $f(4,4) = 6$ and $f(6,8) = 16$:
    $$f_{\vec{u}}(4,4) \approx \frac{f(6,8) - f(4,4)}{\sqrt{(6-4)^2 + (8-4)^2}} = \frac{16 - 6}{\sqrt{20}} = \frac{10}{2\sqrt{5}} = \sqrt{5} \approx 2.24.$$
  - **(b)** Using centered differences around $(4,4)$:
    $$f_{xy}(4,4) \approx \frac{f_x(4,6) - f_x(4,2)}{6 - 2},$$
    with $f_x(4,6) \approx \frac{f(6,6) - f(2,6)}{6 - 2} = \frac{12 - 6}{4} = \frac{3}{2}$ and $f_x(4,2) \approx \frac{f(6,2) - f(2,2)}{6 - 2} = \frac{4 - 2}{4} = \frac{1}{2}$. Therefore:
    $$f_{xy}(4,4) \approx \frac{\frac{3}{2} - \frac{1}{2}}{4} = \frac{1}{4} = 0.25.$$

### Slide Q4 — Find a Quadratic Taylor Polynomial (`Week10-sol.pdf`, PDF p. 4 / Slide p. 3, §14.7)
- **Statement:** Find the Taylor polynomial of degree 2 at $(1,2)$ for $f(x,y) = \frac{1}{xy}$.
- **PT:** [PT-10.5](Study-Notes.md#pt-105-constructing-degree-1-and-degree-2-taylor-polynomials-and-comparing-approximations)
- **Solution:**
  - $f(x,y) = x^{-1}y^{-1} \implies f(1,2) = \frac{1}{2}$.
  - $f_x = -\frac{1}{x^2 y} \implies f_x(1,2) = -\frac{1}{2}$; $\quad f_y = -\frac{1}{x y^2} \implies f_y(1,2) = -\frac{1}{4}$.
  - $f_{xx} = \frac{2}{x^3 y} \implies f_{xx}(1,2) = 1$; $\quad f_{xy} = \frac{1}{x^2 y^2} \implies f_{xy}(1,2) = \frac{1}{4}$; $\quad f_{yy} = \frac{2}{x y^3} \implies f_{yy}(1,2) = \frac{1}{4}$.
  - Assembling $Q(x,y)$:
    $$Q(x,y) = \frac{1}{2} - \frac{1}{2}(x-1) - \frac{1}{4}(y-2) + \frac{1}{2}(1)(x-1)^2 + \frac{1}{4}(x-1)(y-2) + \frac{1}{2}\!\left(\frac{1}{4}\right)(y-2)^2$$
    $$= \frac{1}{2} - \frac{x-1}{2} - \frac{y-2}{4} + \frac{(x-1)^2}{2} + \frac{(x-1)(y-2)}{4} + \frac{(y-2)^2}{8}.$$

### Slide Q5 — Compare Linear and Quadratic Approximations (`Week10-sol.pdf`, PDF p. 5 / Slide p. 4, §14.7)
- **Statement:** Let $f(x,y) = x^2 y$.
  (a) Find the linear Taylor polynomial $L(x,y)$ and the quadratic Taylor polynomial $Q(x,y)$ near $(1,0)$.
  (b) Compare $L(0.9, 0.2)$ and $Q(0.9, 0.2)$ with the exact value $f(0.9, 0.2)$.
- **PT:** [PT-10.5](Study-Notes.md#pt-105-constructing-degree-1-and-degree-2-taylor-polynomials-and-comparing-approximations) *(also identical to §14.7 Problem 43)*.
- **Solution:**
  - **(a)** At $(1,0)$: $f(1,0) = 0$, $f_x = 2xy \to 0$, $f_y = x^2 \to 1$, $f_{xx} = 2y \to 0$, $f_{xy} = 2x \to 2$, $f_{yy} = 0 \to 0$.
    $$L(x,y) = y, \qquad Q(x,y) = y + 2(x-1)y = 2xy - y.$$
  - **(b)** At $(0.9, 0.2)$: $f(0.9, 0.2) = (0.9)^2(0.2) = 0.162$; $L(0.9, 0.2) = 0.2$ (error $|f-L| = 0.038$); $Q(0.9, 0.2) = 0.2 + 2(-0.1)(0.2) = 0.16$ (error $|f-Q| = 0.002 \ll 0.038$).

### Slide Q6 — Check a Solution of the Heat Equation (`Week10-sol.pdf`, PDF p. 5 / Slide p. 4, §14.7)
- **Statement:** Find the relationship between the constants $a$ and $b \neq 0$ for which $u(x,t) = e^{at}\sin(bx)$ satisfies the heat equation $u_t = u_{xx}$.
- **PT:** [PT-10.4](Study-Notes.md#pt-104-verifying-a-solution-or-parameter-relation-for-a-pde)
- **Solution:**
  - $u_t = a e^{at}\sin(bx)$, $\quad u_x = b e^{at}\cos(bx)$, $\quad u_{xx} = -b^2 e^{at}\sin(bx)$.
  - $u_t = u_{xx} \iff a e^{at}\sin(bx) = -b^2 e^{at}\sin(bx)$ for all $(x,t)$. Since $b \neq 0$, $e^{at}\sin(bx)$ is not identically zero, so this holds if and only if **$a = -b^2$**.

### Slide Q7 — Is a Cone Differentiable at Its Vertex? (`Week10-sol.pdf`, PDF p. 9 / Slide p. 5, §14.8)
- **Statement:** Consider $f(x,y) = \sqrt{x^2 + y^2}$.
  (a) Is $f$ continuous at $(0,0)$?
  (b) Use the definition of a partial derivative to determine whether $f_x(0,0)$ and $f_y(0,0)$ exist. Is $f$ differentiable at $(0,0)$?
  *(Part (c), using the formal definition of differentiability, was shaded out as outside TT2 scope on PDF p. 9.)*
- **PT:** [PT-10.6](Study-Notes.md#pt-106-showing-a-function-is-not-differentiable-at-a-point-without-the-formal-definition)
- **Solution:**
  - **(a)** **Yes.** $x^2 + y^2$ is continuous everywhere and $\sqrt{\cdot}$ is continuous on $[0, \infty)$, so their composition $f(x,y) = \sqrt{x^2 + y^2}$ is continuous at $(0,0)$.
  - **(b)** By definition,
    $$f_x(0,0) = \lim_{h\to 0}\frac{f(h,0)-f(0,0)}{h} = \lim_{h\to 0}\frac{\sqrt{h^2} - 0}{h} = \lim_{h\to 0}\frac{|h|}{h},$$
    which equals $+1$ for $h > 0$ and $-1$ for $h < 0$, so $f_x(0,0)$ **does not exist** (similarly, $f_y(0,0)$ does not exist). Since differentiability requires $f_x(0,0)$ and $f_y(0,0)$ to exist, **$f$ is not differentiable at $(0,0)$**.

### Slide Q8 — Are Partial Derivatives Enough? (`Week10-sol.pdf`, PDF p. 10 / Slide p. 6, §14.8)
- **Statement:** Let $f(x,y) = x^{1/3} y^{1/3}$.
  (a) Find $f_x(0,0)$ and $f_y(0,0)$ using the definition of a partial derivative.
  (b) Show that $f$ is not differentiable at $(0,0)$ via:
  (i) Observing the graph near the origin: is it well approximated by a plane?
  (iii) Assuming $f$ is differentiable at $(0,0)$, using the Chain Rule to find $g'(0)$ for $g(t) = f(t,t)$, and comparing with the direct derivative of $g(t)$.
  *(Part (b)(ii), formal definition in Example 3 of §14.8, was crossed out on PDF p. 10 as outside TT2 scope.)*
- **PT:** [PT-10.6](Study-Notes.md#pt-106-showing-a-function-is-not-differentiable-at-a-point-without-the-formal-definition)
- **Solution:**
  - **(a)** $f_x(0,0) = \lim_{h\to 0}\frac{f(h,0)-f(0,0)}{h} = \lim_{h\to 0}\frac{0 - 0}{h} = 0$. Similarly, $f_y(0,0) = 0$.
  - **(b)(i)** No — the graph rises steeply along $y = x$ and drops steeply along $y = -x$ with a pinched cusp at $(0,0)$, so zooming in never makes it look like a plane.
  - **(b)(iii)** If $f$ were differentiable at $(0,0)$, then with $x(t) = t, y(t) = t$, the Chain Rule would give
    $$g'(0) = f_x(0,0)x'(0) + f_y(0,0)y'(0) = 0(1) + 0(1) = 0.$$
    Directly, $g(t) = f(t,t) = t^{2/3}$, so
    $$g'(0) = \lim_{h\to 0}\frac{h^{2/3} - 0}{h} = \lim_{h\to 0}\frac{1}{h^{1/3}},$$
    which does not exist. Contradiction! Therefore **$f$ is not differentiable at $(0,0)$**.

### Slide Q9 — Continuity and Partial Derivatives at a Point (`Week10-sol.pdf`, PDF p. 10 / Slide p. 6, §14.8)
- **Statement:** Let $f(x,y) = \begin{cases} \dfrac{xy}{x^2+y^2}, & (x,y)\neq(0,0), \\ 0, & (x,y)=(0,0). \end{cases}$
  (a) Find $f_x(0,0)$ and $f_y(0,0)$ using the definition of a partial derivative.
  (b) Is $f$ continuous at $(0,0)$? Compare its values along the $x$-axis and along $y = x$.
  (c) Is $f$ differentiable at $(0,0)$?
- **PT:** [PT-10.6](Study-Notes.md#pt-106-showing-a-function-is-not-differentiable-at-a-point-without-the-formal-definition)
- **Solution:**
  - **(a)** $f_x(0,0) = \lim_{h\to 0}\frac{f(h,0) - f(0,0)}{h} = \lim_{h\to 0}\frac{0}{h} = 0$. Similarly, $f_y(0,0) = 0$.
  - **(b)** Along the $x$-axis ($y=0, x\neq 0$): $\lim_{x\to 0} f(x,0) = 0$. Along $y=x$ ($x\neq 0$): $\lim_{x\to 0} f(x,x) = \lim_{x\to 0}\frac{x^2}{2x^2} = \frac{1}{2} \neq 0$. Thus $\lim_{(x,y)\to(0,0)} f(x,y)$ does not exist, so **$f$ is not continuous at $(0,0)$**.
  - **(c)** **No**, because $f$ is not continuous at $(0,0)$ (and differentiability implies continuity).

### Slide Q10 — Use Continuity of the Partial Derivatives (`Week10-sol.pdf`, PDF p. 11 / Slide p. 7, §14.8)
- **Statement:** Determine the domain of each function and show that it is differentiable everywhere in its domain:
  (a) $f(x,y) = \ln(x^2 + y^2)$.
  (b) $f(x,y) = e^{-x^2 - y^2}$.
- **PT:** [PT-10.7](Study-Notes.md#pt-107-proving-differentiability-via-continuity-of-partial-derivatives)
- **Solution:**
  - **(a)** Domain: all $(x,y) \neq (0,0)$ (since $x^2 + y^2 > 0 \iff (x,y) \neq (0,0)$). For $(x,y) \neq (0,0)$, $f_x(x,y) = \frac{2x}{x^2+y^2}$ and $f_y(x,y) = \frac{2y}{x^2+y^2}$. Both are rational functions with nonzero denominator on $\mathbb{R}^2 \setminus \{(0,0)\}$, hence continuous on a small open disk around every point in the domain. By the sufficient condition, $f$ is differentiable everywhere in its domain.
  - **(b)** Domain: all of $\mathbb{R}^2$. Partial derivatives $f_x(x,y) = -2x e^{-x^2-y^2}$ and $f_y(x,y) = -2y e^{-x^2-y^2}$ exist and are continuous everywhere on $\mathbb{R}^2$. By the sufficient condition, $f$ is differentiable everywhere on $\mathbb{R}^2$.

---

## 3. Textbook Exercises and Solutions

All exercise numbers and statements are verified against Hughes-Hallett et al., *Calculus*, 8th Edition (`MAT235_textbook.pdf`). Printed textbook pages and PDF pages (+20 offset) are distinguished below.

### 3.1 §14.7 Requested Exercises

*(21 exercise numbers: 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 25, 29, 35, 37, 41, 43, 45, 47, 57, 61, 69 — Printed pp. 844–847 / PDF pp. 864–867.)*

#### Shared Instruction (Exercises 1–11, p. 844 / PDF p. 864)
*Calculate all four second-order partial derivatives and check that $f_{xy} = f_{yx}$. Assume the variables are restricted to a domain on which the function is defined.* — **[PT-10.1](Study-Notes.md#pt-101-computing-second-order-and-higher-order-partial-derivatives)**

- **§14.7 #1:** $f(x,y) = (x+y)^2$.
  - $f_x = 2(x+y)$, $\; f_y = 2(x+y)$.
  - **Answer:** $f_{xx} = 2$, $\; f_{xy} = 2$, $\; f_{yx} = 2$, $\; f_{yy} = 2$ (and $f_{xy} = f_{yx}$).

- **§14.7 #3:** $f(x,y) = 3x^2 y + 5xy^3$.
  - $f_x = 6xy + 5y^3$, $\; f_y = 3x^2 + 15xy^2$.
  - **Answer:** $f_{xx} = 6y$, $\; f_{xy} = 6x + 15y^2$, $\; f_{yx} = 6x + 15y^2$, $\; f_{yy} = 30xy$ (and $f_{xy} = f_{yx}$).

- **§14.7 #5:** $f(x,y) = (x+y)e^y$.
  - $f_x = e^y$, $\; f_y = e^y + (x+y)e^y = (x + y + 1)e^y$.
  - **Answer:** $f_{xx} = 0$, $\; f_{xy} = e^y$, $\; f_{yx} = e^y$, $\; f_{yy} = (x + y + 2)e^y$ (and $f_{xy} = f_{yx}$).

- **§14.7 #7:** $f(x,y) = \sin(x/y)$ ($y \neq 0$).
  - $f_x = \dfrac{\cos(x/y)}{y}$, $\; f_y = -\dfrac{x\cos(x/y)}{y^2}$.
  - $f_{xx} = -\dfrac{\sin(x/y)}{y^2}$.
  - $f_{xy} = \dfrac{\partial}{\partial y}\!\left(y^{-1}\cos(x/y)\right) = -y^{-2}\cos(x/y) + y^{-1}\!\left(-\sin(x/y)\right)\!\left(-\frac{x}{y^2}\right) = \dfrac{x\sin(x/y) - y\cos(x/y)}{y^3}$.
  - $f_{yx} = \dfrac{\partial}{\partial x}\!\left(-\dfrac{x\cos(x/y)}{y^2}\right) = -\dfrac{\cos(x/y) - (x/y)\sin(x/y)}{y^2} = \dfrac{x\sin(x/y) - y\cos(x/y)}{y^3}$.
  - $f_{yy} = \dfrac{\partial}{\partial y}\!\left(-x y^{-2}\cos(x/y)\right) = 2x y^{-3}\cos(x/y) - x y^{-2}\!\left(-\sin(x/y)\right)\!\left(-\frac{x}{y^2}\right) = \dfrac{2xy\cos(x/y) - x^2\sin(x/y)}{y^4}$.
  - **Answer:** $f_{xx} = -\dfrac{\sin(x/y)}{y^2}$, $\; f_{xy} = f_{yx} = \dfrac{x\sin(x/y) - y\cos(x/y)}{y^3}$, $\; f_{yy} = \dfrac{2xy\cos(x/y) - x^2\sin(x/y)}{y^4}$.

- **§14.7 #9:** $f(x,y) = 5x^3 y^2 - 7xy^3 + 9x^2 + 11$.
  - $f_x = 15x^2 y^2 - 7y^3 + 18x$, $\; f_y = 10x^3 y - 21xy^2$.
  - **Answer:** $f_{xx} = 30xy^2 + 18$, $\; f_{xy} = f_{yx} = 30x^2 y - 21y^2$, $\; f_{yy} = 10x^3 - 42xy$.

- **§14.7 #11:** $f(x,y) = 3\sin(2x)\cos(5y)$.
  - $f_x = 6\cos(2x)\cos(5y)$, $\; f_y = -15\sin(2x)\sin(5y)$.
  - **Answer:** $f_{xx} = -12\sin(2x)\cos(5y)$, $\; f_{xy} = f_{yx} = -30\cos(2x)\sin(5y)$, $\; f_{yy} = -75\sin(2x)\cos(5y)$.

---

#### Shared Instruction (Exercises 12–19, p. 844 / PDF p. 864)
*Find the quadratic Taylor polynomials about $(0,0)$ for the function.* — **[PT-10.5](Study-Notes.md#pt-105-constructing-degree-1-and-degree-2-taylor-polynomials-and-comparing-approximations)**

- **§14.7 #13:** $f(x,y) = (x - y + 1)^2$.
  - At $(0,0)$: $f = 1$, $f_x = 2(x-y+1) \to 2$, $f_y = -2(x-y+1) \to -2$, $f_{xx} = 2$, $f_{xy} = -2$, $f_{yy} = 2$.
  - **Answer:** $Q(x,y) = 1 + 2x - 2y + x^2 - 2xy + y^2$ *(exact, since $f$ is already a quadratic polynomial)*.

- **§14.7 #15:** $f(x,y) = e^x \cos y$.
  - At $(0,0)$: $f = 1$, $f_x = e^x\cos y \to 1$, $f_y = -e^x\sin y \to 0$, $f_{xx} = e^x\cos y \to 1$, $f_{xy} = -e^x\sin y \to 0$, $f_{yy} = -e^x\cos y \to -1$.
  - **Answer:** $Q(x,y) = 1 + x + \dfrac{1}{2}x^2 - \dfrac{1}{2}y^2$.

- **§14.7 #17:** $f(x,y) = \cos(x + 3y)$.
  - At $(0,0)$: $f = 1$, $f_x = -\sin(x+3y) \to 0$, $f_y = -3\sin(x+3y) \to 0$, $f_{xx} = -\cos(x+3y) \to -1$, $f_{xy} = -3\cos(x+3y) \to -3$, $f_{yy} = -9\cos(x+3y) \to -9$.
  - **Answer:** $Q(x,y) = 1 - \dfrac{1}{2}x^2 - 3xy - \dfrac{9}{2}y^2$.

- **§14.7 #19:** $f(x,y) = \ln(1 + x^2 - y)$.
  - $f(0,0) = 0$.
  - $f_x = \dfrac{2x}{1 + x^2 - y} \to 0$; $\quad f_y = \dfrac{-1}{1 + x^2 - y} \to -1$.
  - $f_{xx} = \dfrac{2(1+x^2-y) - 4x^2}{(1+x^2-y)^2} \to 2$; $\quad f_{xy} = \dfrac{2x}{(1+x^2-y)^2} \to 0$; $\quad f_{yy} = \dfrac{-1}{(1+x^2-y)^2} \to -1$.
  - **Answer:** $Q(x,y) = -y + x^2 - \dfrac{1}{2}y^2$.

---

#### Shared Instruction (Exercises 22–33, p. 844 / PDF p. 864)
*Use the level curves of the function $z = f(x,y)$ to decide the sign (positive, negative, or zero) of each of the following partial derivatives at the point $P$: (a) $f_x(P)$, (b) $f_y(P)$, (c) $f_{xx}(P)$, (d) $f_{yy}(P)$, (e) $f_{xy}(P)$. Assume the $x$- and $y$-axes are in the usual positions.* — **[Concept 14.7-A (Supplementary geometric note)](Study-Notes.md#concept-147-a-second-order-and-higher-order-partial-derivatives)**

![Reconstructed contour diagrams for Section 14.7 Exercises 25 and 29 (reconstructed from Hughes-Hallett 8th ed., p. 844 / PDF p. 864): Exercise 25 has vertical contours 1 to 5 getting closer rightward with P on contour 3; Exercise 29 has equally spaced diagonal slope -1 contours 1 to 5 with P on contour 3.](figures/fig4_ex14_7_25_29_contours.png)

- **§14.7 #25:** *(Vertical parallel contours labeled $1, 2, 3, 4, 5$ from left to right, becoming closer together as $x$ increases; $P$ lies on the contour labeled $3$.)*
  - **(a) $f_x(P) > 0$:** Values increase from $2$ to $3$ to $4$ as $x$ increases.
  - **(b) $f_y(P) = 0$:** Contours are vertical, so $f$ is constant along vertical lines.
  - **(c) $f_{xx}(P) > 0$:** Contours get closer together as $x$ increases, so the positive rate of change $f_x$ increases with $x$.
  - **(d) $f_{yy}(P) = 0$:** $f_y = 0$ everywhere.
  - **(e) $f_{xy}(P) = 0$:** $f_x$ does not vary with $y$ (contours are identical vertical lines at every height $y$).

- **§14.7 #29:** *(Equally spaced diagonal parallel contours of slope $-1$, labeled $1, 2, 3, 4, 5$ from bottom-left to top-right; $P$ lies on the contour labeled $3$.)*
  - **(a) $f_x(P) > 0$:** Moving right ($+x$) crosses contours from lower to higher values ($2 \to 3 \to 4$).
  - **(b) $f_y(P) > 0$:** Moving up ($+y$) crosses contours from lower to higher values ($2 \to 3 \to 4$).
  - **(c) $f_{xx}(P) = 0$:** The parallel contours are **equally spaced**, so $f$ is linear and the horizontal rate of change $f_x$ is constant; hence $f_{xx}(P) = 0$.
  - **(d) $f_{yy}(P) = 0$:** Because the contours are equally spaced, the vertical rate of change $f_y$ is constant; hence $f_{yy}(P) = 0$.
  - **(e) $f_{xy}(P) = 0$:** Because the contours are parallel and equally spaced, $f_x$ does not change as $y$ changes; hence $f_{xy}(P) = 0$.

---

#### Shared Instruction (Problems 34–37, p. 845 / PDF p. 865)
*Estimate the quantity, if possible. If it is not possible, explain why. Assume that $g$ is smooth and $\nabla g(2,3) = -7\vec{i} + 3\vec{j}$, $\nabla g(2.4, 3) = -10.2\vec{i} + 4.2\vec{j}$.* — **[PT-10.2](Study-Notes.md#pt-102-estimating-second-order-partial-derivatives-from-a-table-or-gradient-data)**

- **§14.7 #35:** Estimate $g_{xx}(2,3)$.
  - Here $y = 3$ is fixed and $\Delta x = 2.4 - 2 = 0.4$, with $g_x(2,3) = -7$ and $g_x(2.4, 3) = -10.2$.
  - $$g_{xx}(2,3) \approx \frac{g_x(2.4, 3) - g_x(2,3)}{2.4 - 2} = \frac{-10.2 - (-7)}{0.4} = \frac{-3.2}{0.4} = -8.$$
  - **Answer:** $g_{xx}(2,3) \approx -8$.

- **§14.7 #37:** Estimate $g_{xy}(2,3)$.
  - Because $g$ is smooth, $g_{xy}(2,3) = g_{yx}(2,3)$ by Clairaut's Theorem. Using $g_y(2,3) = 3$ and $g_y(2.4, 3) = 4.2$:
  - $$g_{xy}(2,3) = g_{yx}(2,3) \approx \frac{g_y(2.4, 3) - g_y(2,3)}{2.4 - 2} = \frac{4.2 - 3}{0.4} = \frac{1.2}{0.4} = 3.$$
  - **Answer:** $g_{xy}(2,3) \approx 3$.

#### Shared Instruction (Problems 38–41, p. 845 / PDF p. 865)
*Estimate the quantity, if possible. Assume that $h$ is smooth and $\nabla h(2.4, 3) = -20.4\vec{i} + 8.4\vec{j}$, $\nabla h(2.4, 2.7) = -22.2\vec{i} + 9\vec{j}$.* — **[PT-10.2](Study-Notes.md#pt-102-estimating-second-order-partial-derivatives-from-a-table-or-gradient-data)**

- **§14.7 #41:** Estimate $h_{yx}(2.4, 2.7)$.
  - Here $x = 2.4$ is fixed and $y$ varies from $2.7$ to $3$ ($\Delta y = 0.3$). Since $h$ is smooth, $h_{yx}(2.4, 2.7) = h_{xy}(2.4, 2.7)$:
  - $$h_{yx}(2.4, 2.7) = h_{xy}(2.4, 2.7) \approx \frac{h_x(2.4, 3) - h_x(2.4, 2.7)}{3 - 2.7} = \frac{-20.4 - (-22.2)}{0.3} = \frac{1.8}{0.3} = 6.$$
  - **Answer:** $h_{yx}(2.4, 2.7) \approx 6$.

---

#### Shared Instruction (Problems 42–46, p. 845 / PDF p. 865)
*Find the linear, $L(x,y)$, and quadratic, $Q(x,y)$, Taylor polynomials valid near $(1,0)$. Compare the values of the approximations $L(0.9, 0.2)$ and $Q(0.9, 0.2)$ with the exact value of the function $f(0.9, 0.2)$.* — **[PT-10.5](Study-Notes.md#pt-105-constructing-degree-1-and-degree-2-taylor-polynomials-and-comparing-approximations)**

- **§14.7 #43:** $f(x,y) = x^2 y$.
  - *(Identical to Slide Q5 above.)*
  - At $(1,0)$: $f=0, f_x=0, f_y=1, f_{xx}=0, f_{xy}=2, f_{yy}=0$.
  - **Answer:** $L(x,y) = y$, $\; Q(x,y) = y + 2(x-1)y$. At $(0.9, 0.2)$: exact $f = 0.162$, $L = 0.2$ (error $0.038$), $Q = 0.16$ (error $0.002$). $Q$ is much closer to $f$.

- **§14.7 #45:** $F(x,y) = e^x \sin y + e^y \sin x$.
  - Derivatives and values at $(1,0)$:
    - $F(1,0) = \sin 1$
    - $F_x = e^x\sin y + e^y\cos x \implies F_x(1,0) = \cos 1$
    - $F_y = e^x\cos y + e^y\sin x \implies F_y(1,0) = e + \sin 1$
    - $F_{xx} = e^x\sin y - e^y\sin x \implies F_{xx}(1,0) = -\sin 1$
    - $F_{xy} = e^x\cos y + e^y\cos x \implies F_{xy}(1,0) = e + \cos 1$
    - $F_{yy} = -e^x\sin y + e^y\sin x \implies F_{yy}(1,0) = \sin 1$
  - Polynomials:
    $$L(x,y) = \sin 1 + (\cos 1)(x-1) + (e + \sin 1)y,$$
    $$Q(x,y) = \sin 1 + (\cos 1)(x-1) + (e + \sin 1)y - \frac{\sin 1}{2}(x-1)^2 + (e + \cos 1)(x-1)y + \frac{\sin 1}{2}y^2.$$
  - Comparison at $(0.9, 0.2)$ (where $x-1 = -0.1$, $y = 0.2$):
    - Exact: $F(0.9, 0.2) = e^{0.9}\sin(0.2) + e^{0.2}\sin(0.9) \approx 1.4454$.
    - Linear: $L(0.9, 0.2) \approx 1.4994$ (error $\approx 0.0540$).
    - Quadratic: $Q(0.9, 0.2) \approx 1.4468$ (error $\approx 0.0014$).
  - **Answer:** $L$ and $Q$ as above; $Q(0.9, 0.2) \approx 1.4468$ is dramatically closer to $F(0.9, 0.2) \approx 1.4454$ than $L(0.9, 0.2) \approx 1.4994$.

---

#### Problem 47 (p. 845 / PDF p. 865) — **[PT-10.4](Study-Notes.md#pt-104-verifying-a-solution-or-parameter-relation-for-a-pde)**

- **§14.7 #47:** *Show that $F(x,y) = e^{-x}\sin y$ satisfies Laplace's equation, $F_{xx} + F_{yy} = 0$.*
  - $F_x = -e^{-x}\sin y \implies F_{xx} = e^{-x}\sin y$.
  - $F_y = e^{-x}\cos y \implies F_{yy} = -e^{-x}\sin y$.
  - Therefore $F_{xx} + F_{yy} = e^{-x}\sin y - e^{-x}\sin y = 0$ for all $(x,y) \in \mathbb{R}^2$.

---

#### Problem 57 (p. 846 / PDF p. 866) — **[PT-10.2](Study-Notes.md#pt-102-estimating-second-order-partial-derivatives-from-a-table-or-gradient-data)**

- **§14.7 #57:** *The table gives values of a quadratic polynomial $P(x,y) = a + bx + cy + dx^2 + exy + fy^2$. Determine whether each of the coefficients $d, e$, and $f$ is positive, negative, or zero.*

  | $y \backslash x$ | $10$ | $12$ | $14$ |
  |---|---|---|---|
  | **$10$** | $90$ | $82$ | $74$ |
  | **$15$** | $75$ | $87$ | $99$ |
  | **$20$** | $10$ | $42$ | $74$ |

  - Recall $P_{xx} = 2d$, $P_{xy} = e$, $P_{yy} = 2f$ (constants for any quadratic polynomial!).
  - **Sign of $d$:** Along each fixed-$y$ row ($\Delta x = 2$), the first differences are constant:
    - $y=10$: $82-90 = -8$, $74-82 = -8$ (second difference $= 0$).
    - $y=15$: $87-75 = +12$, $99-87 = +12$ (second difference $= 0$).
    - $y=20$: $42-10 = +32$, $74-42 = +32$ (second difference $= 0$).
    Thus $P_{xx} = 2d = 0 \implies \mathbf{d = 0}$.
  - **Sign of $e$:** As $y$ increases by $\Delta y = 5$, the $x$-step difference $\Delta_x P$ increases from $-8$ to $+12$ to $+32$ (change of $+20$ per $\Delta y = 5$), so $P_{xy} = e = \frac{20}{2 \cdot 5} = 2 \implies \mathbf{e > 0}$.
  - **Sign of $f$:** Along the fixed column $x = 10$ ($\Delta y = 5$), the values are $90, 75, 10$. First differences: $75 - 90 = -15$ and $10 - 75 = -65$. Second difference: $-65 - (-15) = -50 < 0$, so $P_{yy} = 2f = \frac{-50}{5^2} = -2 \implies f = -1$, hence $\mathbf{f < 0}$.
  - **Answer:** $d = 0$, $e > 0$, $f < 0$.

---

#### Problem 61 (p. 846 / PDF p. 866) — **[Concept 14.7-A (Supplementary contextual note)](Study-Notes.md#concept-147-a-second-order-and-higher-order-partial-derivatives)**

- **§14.7 #61:** *Human surface area $S(h,w)$ satisfies $\partial^2 S/\partial w^2 < 0$ and $\partial^2 S/(\partial h\,\partial w) > 0$. Two people $A$ and $B$ each gain $1$ pound. Which experiences the greater increase in surface area if (a) they have the same weight but $A$ is taller; (b) they have the same height, but $A$ is heavier?*
  - For a $1$-pound weight gain ($\Delta w = 1$), the increase in surface area is approximately $\Delta S \approx \frac{\partial S}{\partial w}$.
  - **(a)** Since $\frac{\partial}{\partial h}\!\left(\frac{\partial S}{\partial w}\right) = \frac{\partial^2 S}{\partial h\,\partial w} > 0$, the rate $\frac{\partial S}{\partial w}$ increases with height $h$. Because $A$ is taller (at the same weight), **person $A$** experiences the greater increase in surface area.
  - **(b)** Since $\frac{\partial}{\partial w}\!\left(\frac{\partial S}{\partial w}\right) = \frac{\partial^2 S}{\partial w^2} < 0$, the rate $\frac{\partial S}{\partial w}$ decreases as weight $w$ increases. Because $A$ is heavier (at the same height), **person $B$** (the lighter person) experiences the greater increase in surface area.

---

#### Problem 69 (Strengthen Your Understanding, p. 847 / PDF p. 867) — **[PT-10.3](Study-Notes.md#pt-103-testing-whether-proposed-partial-derivatives-can-come-from-a-function)**

- **§14.7 #69:** *Explain what is wrong with the statement: "There is a function $f(x,y)$ with partial derivatives $f_x = xy$ and $f_y = y^2$."*
  - If such an $f$ existed, then $f_{xy} = (xy)_y = x$ and $f_{yx} = (y^2)_x = 0$. Both $f_{xy} = x$ and $f_{yx} = 0$ are continuous everywhere on $\mathbb{R}^2$, so by Clairaut's Theorem we must have $f_{xy} = f_{yx}$ everywhere. Since $x \neq 0$ for $x \neq 0$, this is a contradiction; no such function exists.

---

### 3.2 §14.8 Requested Exercises

*(7 exercise numbers: 1, 5, 13(b, c, e), 17(b, c), 21, 23, 25 — Printed pp. 852–854 / PDF pp. 872–874. Only the listed subparts are included for #13 and #17.)*

#### Shared Instruction (Exercises 1–10, p. 852 / PDF p. 872)
*List the points in the $xy$-plane, if any, at which the function $z = f(x,y)$ is not differentiable.*

- **§14.8 #1:** $z = -\sqrt{x^2 + y^2}$. — **[PT-10.6](Study-Notes.md#pt-106-showing-a-function-is-not-differentiable-at-a-point-without-the-formal-definition) & [PT-10.7](Study-Notes.md#pt-107-proving-differentiability-via-continuity-of-partial-derivatives)**
  - For $(x,y) \neq (0,0)$, $f_x = \frac{-x}{\sqrt{x^2+y^2}}$ and $f_y = \frac{-y}{\sqrt{x^2+y^2}}$ exist and are continuous, so $f$ is differentiable everywhere away from $(0,0)$.
  - At $(0,0)$, $f_x(0,0) = \lim_{h\to 0}\frac{-\sqrt{h^2} - 0}{h} = \lim_{h\to 0}\frac{-|h|}{h}$ does not exist (right limit $-1$, left limit $+1$).
  - **Answer:** Not differentiable at **$(0,0)$** only.

- **§14.8 #5:** $z = e^{-(x^2+y^2)}$. — **[PT-10.7](Study-Notes.md#pt-107-proving-differentiability-via-continuity-of-partial-derivatives)**
  - $f_x = -2x e^{-(x^2+y^2)}$ and $f_y = -2y e^{-(x^2+y^2)}$ exist and are continuous everywhere on $\mathbb{R}^2$. By the sufficient condition, $f$ is differentiable everywhere.
  - **Answer:** **None** (differentiable at every point in the $xy$-plane).

---

#### Problem 13(b, c, e) (p. 852 / PDF p. 872) — **[PT-10.7](Study-Notes.md#pt-107-proving-differentiability-via-continuity-of-partial-derivatives) & [PT-10.6](Study-Notes.md#pt-106-showing-a-function-is-not-differentiable-at-a-point-without-the-formal-definition)**

- **§14.8 #13:** Given $f(x,y) = \begin{cases} \dfrac{x^2 y}{x^4 + y^2}, & (x,y)\neq(0,0), \\ 0, & (x,y)=(0,0). \end{cases}$
  - **(b) Is $f$ differentiable at all points $(x,y) \neq (0,0)$?**
    **Yes.** As shown in part (c), $f_x$ and $f_y$ exist and are continuous on the open set $\mathbb{R}^2 \setminus \{(0,0)\}$, so by the sufficient condition, $f$ is differentiable at every $(x,y) \neq (0,0)$.
  - **(c) Do $f_x$ and $f_y$ exist and are they continuous at all points $(x,y) \neq (0,0)$?**
    **Yes.** For $(x,y) \neq (0,0)$, $x^4 + y^2 > 0$, so by the quotient rule:
    $$f_x(x,y) = \frac{2xy(x^4+y^2) - x^2 y(4x^3)}{(x^4+y^2)^2} = \frac{2xy(y^2 - x^4)}{(x^4+y^2)^2},$$
    $$f_y(x,y) = \frac{x^2(x^4+y^2) - x^2 y(2y)}{(x^4+y^2)^2} = \frac{x^2(x^4 - y^2)}{(x^4+y^2)^2}.$$
    Both are rational functions with nonzero denominator for $(x,y) \neq (0,0)$, so both exist and are continuous at all $(x,y) \neq (0,0)$.
  - **(e) Do $f_x$ and $f_y$ exist and are they continuous at $(0,0)$?**
    - **Existence:** By the limit definition,
      $$f_x(0,0) = \lim_{h\to 0}\frac{f(h,0) - f(0,0)}{h} = \lim_{h\to 0}\frac{0}{h} = 0, \qquad f_y(0,0) = \lim_{k\to 0}\frac{f(0,k) - f(0,0)}{k} = \lim_{k\to 0}\frac{0}{k} = 0.$$
      So both $f_x(0,0)$ and $f_y(0,0)$ **exist** (and equal $0$).
    - **Continuity at $(0,0)$:**
      - For $f_x$: along $y = 2x^2$ ($x \neq 0$), $f_x(x, 2x^2) = \dfrac{2x(2x^2)(4x^4 - x^4)}{(x^4 + 4x^4)^2} = \dfrac{12x^7}{25x^8} = \dfrac{12}{25x}$, which diverges as $x \to 0$. Thus $f_x$ is **not continuous** at $(0,0)$.
      - For $f_y$: along $y = 0$ ($x \neq 0$), $f_y(x, 0) = \dfrac{x^6}{x^8} = \dfrac{1}{x^2} \to +\infty$ as $x \to 0$. Thus $f_y$ is **not continuous** at $(0,0)$.
    - **Answer to (e):** Both $f_x(0,0)$ and $f_y(0,0)$ **exist** (both equal $0$), but **neither** $f_x$ nor $f_y$ is continuous at $(0,0)$.

---

#### Problem 17(b, c) (p. 853 / PDF p. 873) — **[PT-10.6](Study-Notes.md#pt-106-showing-a-function-is-not-differentiable-at-a-point-without-the-formal-definition)**

- **§14.8 #17:** Given $f(x,y) = \begin{cases} \dfrac{xy^2}{x^2 + y^4}, & (x,y)\neq(0,0), \\ 0, & (x,y)=(0,0). \end{cases}$
  - **(b) Show that the directional derivative $f_{\vec{u}}(0,0)$ exists for each unit vector $\vec{u} = a\vec{i} + b\vec{j}$ ($a^2 + b^2 = 1$).**
    By definition, $f_{\vec{u}}(0,0) = \lim_{h\to 0}\frac{f(ha, hb) - f(0,0)}{h}$.
    - Case 1 ($a = 0$): $f(0, hb) = 0$ for all $h$, so $f_{\vec{u}}(0,0) = \lim_{h\to 0}\frac{0}{h} = 0$.
    - Case 2 ($a \neq 0$): for $h \neq 0$,
      $$\frac{f(ha, hb)}{h} = \frac{h^3 a b^2}{h(h^2 a^2 + h^4 b^4)} = \frac{ab^2}{a^2 + h^2 b^4} \xrightarrow{h\to 0} \frac{ab^2}{a^2} = \frac{b^2}{a}.$$
    In both cases the limit exists, so $f_{\vec{u}}(0,0)$ exists for **every** unit vector $\vec{u}$.
  - **(c) Is $f$ continuous at $(0,0)$? Is $f$ differentiable at $(0,0)$? Explain.**
    - Along the $x$-axis ($y = 0, x \neq 0$): $f(x,0) = 0 \to 0$.
    - Along the parabola $x = y^2$ ($y \neq 0$): $f(y^2, y) = \dfrac{y^4}{y^4 + y^4} = \dfrac{1}{2} \to \dfrac{1}{2} \neq 0$.
    - Thus $\lim_{(x,y)\to(0,0)} f(x,y)$ does not exist, so **$f$ is not continuous at $(0,0)$**.
    - Because differentiability implies continuity, **$f$ is not differentiable at $(0,0)$** (even though every directional derivative exists there!).

---

#### Problems 21, 23, 25 (Strengthen Your Understanding, p. 854 / PDF p. 874)

- **§14.8 #21** *(PT-10.6 / Concept 14.8-A)*: *Explain what is wrong with the statement: "If $f(x,y)$ is continuous at the origin, then it is differentiable at the origin."*
  - **Answer:** The implication goes the other way: differentiability implies continuity, but continuity does **not** imply differentiability. Counterexample: $f(x,y) = \sqrt{x^2 + y^2}$ is continuous at $(0,0)$, yet has a sharp vertex there ($f_x(0,0)$ and $f_y(0,0)$ do not exist), so it is not differentiable at $(0,0)$.

- **§14.8 #23** *(PT-10.6 / Concept 14.8-A)*: *Give an example of a continuous function $f(x,y)$ that is not differentiable at the origin.*
  - **Answer:** $f(x,y) = \sqrt{x^2 + y^2}$ (continuous at $(0,0)$ as a composition of continuous functions, but not differentiable at $(0,0)$ because $f_x(0,0) = \lim_{h\to 0}\frac{|h|}{h}$ does not exist). *(Other valid examples: $f(x,y) = |x| + |y|$ or $f(x,y) = x^{1/3}y^{1/3}$.)*

- **§14.8 #25** *(PT-10.6 & PT-10.7)*: *Which of the following functions $f(x,y)$ is differentiable at the given point?*
  - **(a) $\sqrt{1 - x^2 - y^2}$ at $(0,0)$:** **Differentiable.** Near $(0,0)$, $1 - x^2 - y^2 > 0$, so $f_x = \frac{-x}{\sqrt{1-x^2-y^2}}$ and $f_y = \frac{-y}{\sqrt{1-x^2-y^2}}$ exist and are continuous on a small open disk around $(0,0)$.
  - **(b) $\sqrt{4 - x^2 - y^2}$ at $(2,0)$:** **Not differentiable.** The domain is the closed disk $x^2 + y^2 \le 4$, so $(2,0)$ is a boundary point (undefined for $x > 2$), and $f_x(2,0)$ does not exist (even the one-sided slope tends to $-\infty$).
  - **(c) $-\sqrt{x^2 + 2y^2}$ at $(0,0)$:** **Not differentiable.** $f_x(0,0) = \lim_{h\to 0}\frac{-|h|}{h}$ does not exist (sharp cone vertex).
  - **(d) $-\sqrt{x^2 + 2y^2}$ at $(2,0)$:** **Differentiable.** At $(2,0)$, $x^2 + 2y^2 = 4 > 0$, so $f_x = \frac{-x}{\sqrt{x^2+2y^2}}$ and $f_y = \frac{-2y}{\sqrt{x^2+2y^2}}$ exist and are continuous on a small open disk around $(2,0)$.
  - **Answer:** **(a)** and **(d)** are differentiable at their given points; **(b)** and **(c)** are not.

---

## 4. Original Self-Test

### 4.1 Self-Test Questions

Attempt all seven questions before checking the answers below.

1. **(PT-10.1)** Let $f(x,y) = y\sin(3x) + x^2 y^3$. Compute $f_{xx}$, $f_{xy}$, $f_{yx}$, and $f_{yy}$, and verify that $f_{xy} = f_{yx}$.
2. **(PT-10.2 — Supplementary: gradient-data branch, matching §14.7 #35, #37, #41)** Suppose $g(x,y)$ is smooth, with $\nabla g(1,2) = 4\vec{i} - 5\vec{j}$ and $\nabla g(1.2, 2) = 4.6\vec{i} - 4.4\vec{j}$. Estimate $g_{xx}(1,2)$ and $g_{xy}(1,2)$.
3. **(PT-10.3)** Does there exist a function $f(x,y)$ such that $f_x(x,y) = e^y + 2x$ and $f_y(x,y) = x e^y + 5x$? Justify your answer.
4. **(PT-10.4 — Supplementary: Laplace's equation, matching §14.7 #47)** Show that $F(x,y) = e^{2x}\cos(2y)$ satisfies Laplace's equation $F_{xx} + F_{yy} = 0$ on $\mathbb{R}^2$.
5. **(PT-10.5)** Let $f(x,y) = \ln(1 + 2x - y)$.
   (a) Find the degree-1 Taylor polynomial $L(x,y)$ and degree-2 Taylor polynomial $Q(x,y)$ near $(0,0)$.
   (b) Compare $L(0.1, 0.1)$ and $Q(0.1, 0.1)$ with the exact value $f(0.1, 0.1) = \ln(1.1) \approx 0.09531$.
6. **(PT-10.6)** Show without using the formal limit definition that $f(x,y) = \begin{cases} \dfrac{3xy}{2x^2 + y^2}, & (x,y)\neq(0,0), \\ 0, & (x,y)=(0,0) \end{cases}$ is **not** differentiable at $(0,0)$, even though $f_x(0,0)$ and $f_y(0,0)$ both exist.
7. **(PT-10.7)** Determine the domain of $f(x,y) = \sqrt{9 - x^2 - y^2}$ and show that $f$ is differentiable at every interior point of its domain ($x^2 + y^2 < 9$).

---

### 4.2 Self-Test Answers

1. **ST-1 (PT-10.1):**
   $f_x = 3y\cos(3x) + 2xy^3$, $\; f_y = \sin(3x) + 3x^2 y^2$.
   - $f_{xx} = -9y\sin(3x) + 2y^3$,
   - $f_{xy} = f_{yx} = 3\cos(3x) + 6xy^2$,
   - $f_{yy} = 6x^2 y$.
2. **ST-2 (PT-10.2):**
   With $y=2$ fixed and $\Delta x = 0.2$:
   - $g_{xx}(1,2) \approx \dfrac{g_x(1.2, 2) - g_x(1,2)}{0.2} = \dfrac{4.6 - 4}{0.2} = 3$.
   - By smoothness, $g_{xy}(1,2) = g_{yx}(1,2) \approx \dfrac{g_y(1.2, 2) - g_y(1,2)}{0.2} = \dfrac{-4.4 - (-5)}{0.2} = 3$.
3. **ST-3 (PT-10.3):**
   **No.** If such an $f$ existed, $f_{xy} = (e^y + 2x)_y = e^y$ and $f_{yx} = (xe^y + 5x)_x = e^y + 5$. Both are continuous everywhere on $\mathbb{R}^2$, so Clairaut's Theorem requires $f_{xy} = f_{yx}$, contradicting $e^y \neq e^y + 5$.
4. **ST-4 (PT-10.4):**
   $F_x = 2e^{2x}\cos(2y) \implies F_{xx} = 4e^{2x}\cos(2y)$; $\; F_y = -2e^{2x}\sin(2y) \implies F_{yy} = -4e^{2x}\cos(2y)$. Thus $F_{xx} + F_{yy} = 0$ for all $(x,y) \in \mathbb{R}^2$.
5. **ST-5 (PT-10.5):**
   - **(a)** At $(0,0)$: $f=0$, $f_x = \frac{2}{1+2x-y} \to 2$, $f_y = \frac{-1}{1+2x-y} \to -1$, $f_{xx} = \frac{-4}{(1+2x-y)^2} \to -4$, $f_{xy} = \frac{2}{(1+2x-y)^2} \to 2$, $f_{yy} = \frac{-1}{(1+2x-y)^2} \to -1$.
     $$L(x,y) = 2x - y, \qquad Q(x,y) = 2x - y - 2x^2 + 2xy - \frac{1}{2}y^2.$$
   - **(b)** At $(0.1, 0.1)$: $L(0.1, 0.1) = 0.10000$ (error $\approx 0.00469$), $Q(0.1, 0.1) = 0.1 - 0.02 + 0.02 - 0.005 = 0.09500$ (error $\approx 0.00031 \ll 0.00469$).
6. **ST-6 (PT-10.6):**
   - Partials exist: $f_x(0,0) = \lim_{h\to 0}\frac{f(h,0)-0}{h} = 0$ and $f_y(0,0) = \lim_{k\to 0}\frac{f(0,k)-0}{k} = 0$.
   - Discontinuous at $(0,0)$: along $y=0$ ($x\neq 0$), $f(x,0) = 0 \to 0$; along $y=x$ ($x\neq 0$), $f(x,x) = \frac{3x^2}{3x^2} = 1 \to 1 \neq 0$.
   - Since $f$ is not continuous at $(0,0)$, $f$ is **not differentiable** at $(0,0)$.
7. **ST-7 (PT-10.7):**
   Domain: closed disk $x^2 + y^2 \le 9$. On the open disk $x^2 + y^2 < 9$, $9 - x^2 - y^2 > 0$, so
   $$f_x(x,y) = \frac{-x}{\sqrt{9-x^2-y^2}}, \qquad f_y(x,y) = \frac{-y}{\sqrt{9-x^2-y^2}}$$
   exist and are continuous on a small open disk around every interior point $(a,b)$ with $a^2 + b^2 < 9$. By the sufficient condition, $f$ is differentiable at every point with $x^2 + y^2 < 9$.

---

## 5. Coverage Appendix

### 5.1 Learning-Objectives Mapping

| # | Quercus Learning Objective | Concept | Slide Locator (`Week10-sol.pdf`) | PT(s) | Practice Coverage |
|---|---|---|---|---|---|
| 1 | **§14.7:** Compute higher-order partial derivatives of a multivariable function | Concept 14.7-A | PDF p. 2 (Slide p. 1) | PT-10.1, PT-10.2 | Slide Q1, Q3(b); §14.7 #1, 3, 5, 7, 9, 11, 25, 29, 35, 37, 41, 47, 57, 61; ST-1, ST-2, ST-4 |
| 2 | **§14.7:** Explain when the mixed partial derivatives of a two-variable function are equal | Concept 14.7-B | PDF pp. 2–3 (Slides pp. 1–2) | PT-10.3 | Slide Q2; §14.7 #1–11 (check), #37, #41, #69; ST-3 |
| 3 | **§14.7:** Construct and use degree-1 and degree-2 Taylor polynomials to approximate a two-variable function | Concept 14.7-C | PDF pp. 4–5 (Slides pp. 3–4) | PT-10.5 | Slide Q4, Q5; §14.7 #13, 15, 17, 19, 43, 45; ST-5 |
| 4 | **§14.7:** Explain the algebraic and graphical relationships between the function and its Taylor polynomials | Concept 14.7-C | PDF pp. 1, 4–6 (Slides pp. 3–4 + board notes) | PT-10.5 | `fig1_taylor_linear_vs_quadratic.png`; Slide Q5; §14.7 #43, 45, 57; ST-5 |
| 5 | **§14.8:** Explain intuitively what it means for a two-variable function to be differentiable | Concept 14.8-A | PDF pp. 9–10, 12 (Slides pp. 5–6 + summary) | PT-10.6 | `fig2_differentiability_comparison.png`; Slide Q7, Q8(b)(i); §14.8 #1, 21, 23 |
| 6 | **§14.8:** Use partial derivatives to determine when a function is differentiable | Concept 14.8-A, 14.8-B | PDF pp. 9–12 (Slides pp. 5–7 + summary) | PT-10.6, PT-10.7 | Slide Q7, Q8, Q10; §14.8 #1, 5, 13(b,c,e), 25; ST-6, ST-7 |
| 7 | **§14.8:** Explain the relationship between continuity and differentiability | Concept 14.8-A, 14.8-B | PDF pp. 9–12 (Slides pp. 5–7 + summary) | PT-10.6, PT-10.7 | `fig3_differentiability_logic_map.png`; Slide Q7, Q9; §14.8 #17(b,c), 21, 23; ST-6 |

### 5.2 Requested Textbook Exercise Accounting

- **§14.7 (21 / 21 exercise numbers solved):** 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 25, 29, 35, 37, 41, 43, 45, 47, 57, 61, 69.
- **§14.8 (7 / 7 exercise numbers solved, exact restricted subparts):** 1, 5, 13(b, c, e), 17(b, c), 21, 23, 25.

### 5.3 Verified Assigned Reading vs. Supporting Reading

- **Verified Assigned Pre-Class Reading (Canvas Week 10 Pre-Class Reading — `MAT235_textbook.pdf`, Hughes-Hallett 8th ed.):**
  - §14.7, printed p. 838 (PDF p. 858): definition of second-order partial derivatives and Example 1.
  - §14.7, printed p. 839 (PDF p. 859): Theorem 14.1 (Equality of Mixed Partial Derivatives).
  - §14.7, printed p. 840 (PDF p. 860): definitions of degree-1 and degree-2 Taylor approximations near the origin.
- **Supporting Reading:**
  - Remaining textbook sections covered in Week 10 lectures and exercises: §14.7 printed pp. 841–847 (PDF pp. 861–867) and §14.8 printed pp. 847–854 (PDF pp. 867–874), excluding the formal limit definition proofs for TT2.
  - Professor's Week 10 slides: `W10/lec/Week10-sol.pdf` (PDF pp. 1–12 / Slides 1–7 of 7).
  - Handwritten lecture notes in `W10/`: `Nov 18.pdf` (numerical mixed partials & graphical concavity of $f_{xx}, f_{yy}, f_{xt}$) and `Nov 20.pdf` (differentiability, continuity, directional derivatives).
  - Prerequisite review: §14.1 (partial derivatives), §14.3 (local linearity), §14.5 (directional derivatives & gradient), §14.6 (Chain Rule).

### 5.4 Source Gaps and Scope Notes (Recorded Once)

1. **Quercus screenshot file:** No separate Quercus PNG screenshot file was present in `W10/`; the official Quercus learning objectives and suggested exercise list were taken verbatim from the user prompt.
2. **Textbook difficulty grouping ("Basic"):** Hughes-Hallett 8th edition (`MAT235_textbook.pdf`) groups end-of-section items under **EXERCISES**, **PROBLEMS**, and **Strengthen Your Understanding** rather than a "Basic" label. No "Basic" labels were inferred from exercise numbers; all 7 Problem Types (**PT-10.1** through **PT-10.7**) were established strictly from actual questions in `W10/lec/Week10-sol.pdf`.
3. **Out-of-scope files & subparts:** `W10/nov 23-2.pdf` covers §15.1 (critical points) and is kept outside Week 10 notes. On `Week10-sol.pdf`, PDF p. 9 part (c) and PDF p. 10 part (b)(ii) (formal limit definition of differentiability) were explicitly marked out of TT2 scope by the professor and excluded from TT2 core methods; none of the requested textbook exercises required implicit differentiation or the formal limit definition.
