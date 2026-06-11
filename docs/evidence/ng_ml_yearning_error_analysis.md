Source: https://github.com/ajaymache/machine-learning-yearning/blob/master/full%20book/machine-learning-yearning.pdf (mirror of the draft Andrew Ng distributed via deeplearning.ai mailing list, 2018; never formally published)
Title: "Machine Learning Yearning" (draft) — Andrew Ng, chapters 13-19 (basic error analysis)
Fetched-via: PDF downloaded from the github mirror, text extracted with pdfplumber, 2026-06-11
Fetch-status: verbatim excerpts; line breaks rejoined

# Machine Learning Yearning — basic error analysis (excerpts)

Chapter 13, "Build your first system quickly, then iterate" (p. 29):

> So don't start off trying to design and build the perfect system. Instead, build and train a basic system quickly—perhaps in just a few days. Even if the basic system is far from the "best" system you can build, it is valuable to examine how the basic system functions: you will quickly find clues that show you the most promising directions in which to invest your time.

Chapter 14, "Error analysis: Look at dev set examples to evaluate ideas" (pp. 30-31):

> Before investing a month on this task, I recommend that you first estimate how much it will actually improve the system's accuracy. [...] In detail, here's what you can do:
> 1. Gather a sample of 100 dev set examples that your system misclassified. I.e., examples that your system made an error on.
> 2. Look at these examples manually, and count what fraction of them are dog images.

> Error analysis can often help you figure out how promising different directions are. I've seen many engineers reluctant to carry out error analysis. It often feels more exciting to just jump in and implement some idea, rather than question if the idea is worth the time investment. This is a common mistake: It might result in your team spending a month only to realize afterward that it resulted in little benefit.

> Manually examining 100 examples does not take long. Even if you take one minute per image, you'd be done in under two hours. These two hours could save you a month of wasted effort.

Chapter 15, "Evaluating multiple ideas in parallel during error analysis" (p. 32):

> You can efficiently evaluate all of these ideas in parallel. I usually create a spreadsheet and fill it out while looking through ~100 misclassified dev set images. I also jot down comments that might help me remember specific examples. [...] once you start looking through examples, you will probably be inspired to propose new error categories.

Chapter 19, "Takeaways: Basic error analysis" (p. 40):

> When you start a new project, especially if it is in an area in which you are not an expert, it is hard to correctly guess the most promising directions.

> Carry out error analysis by manually examining ~100 dev set examples the algorithm misclassifies and counting the major categories of errors. Use this information to prioritize what types of errors to work on fixing.

> Consider splitting the dev set into an Eyeball dev set, which you will manually examine, and a Blackbox dev set, which you will not manually examine. If performance on the Eyeball dev set is much better than the Blackbox dev set, you have overfit the Eyeball dev set and should consider acquiring more data for it.
