Source: https://papers.nips.cc/paper_files/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf
Title: "Hidden Technical Debt in Machine Learning Systems" — D. Sculley, Gary Holt, Daniel Golovin, Eugene Davydov, Todd Phillips, Dietmar Ebner, Vinay Chaudhary, Michael Young, Jean-François Crespo, Dan Dennison (Google, Inc.), NIPS 2015
Fetched-via: PDF downloaded from papers.nips.cc, pages 1-2 transcribed by hand from the rendered pages
Fetch-status: verbatim excerpts (abstract + Entanglement section); subscripts rendered as plain text (x1, xn+1)

# Hidden Technical Debt in Machine Learning Systems (excerpts)

Abstract (p. 1):

> Machine learning offers a fantastically powerful toolkit for building useful complex prediction systems quickly. This paper argues it is dangerous to think of these quick wins as coming for free. Using the software engineering framework of *technical debt*, we find it is common to incur massive ongoing maintenance costs in real-world ML systems. We explore several ML-specific risk factors to account for in system design. These include boundary erosion, entanglement, hidden feedback loops, undeclared consumers, data dependencies, configuration issues, changes in the external world, and a variety of system-level anti-patterns.

Section 2, "Complex Models Erode Boundaries" — Entanglement (p. 2), the CACE principle:

> **Entanglement.** Machine learning systems mix signals together, entangling them and making isolation of improvements impossible. For instance, consider a system that uses features x1, ...xn in a model. If we change the input distribution of values in x1, the importance, weights, or use of the remaining n − 1 features may all change. This is true whether the model is retrained fully in a batch style or allowed to adapt in an online fashion. Adding a new feature xn+1 can cause similar changes, as can removing any feature xj. No inputs are ever really independent. We refer to this here as the CACE principle: Changing Anything Changes Everything. CACE applies not only to input signals, but also to hyper-parameters, learning settings, sampling methods, convergence thresholds, data selection, and essentially every other possible tweak.

Same section, the ensemble caveat (p. 2):

> One possible mitigation strategy is to isolate models and serve ensembles. [...] However, in many cases ensembles work well because the errors in the component models are uncorrelated. Relying on the combination creates a strong entanglement: improving an individual component model may actually make the system accuracy worse if the remaining errors are more strongly correlated with the other components.
