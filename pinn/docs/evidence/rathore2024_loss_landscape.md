Title: Challenges in Training PINNs: A Loss Landscape Perspective

URL Source: https://arxiv.org/pdf/2402.01868v2

Published Time: Wed, 05 Jun 2024 01:03:07 GMT

Number of Pages: 33

Markdown Content:
# Challenges in Training PINNs: A Loss Landscape Perspective 

Pratik Rathore 1 Weimu Lei 2 Zachary Frangella 3 Lu Lu 4 Madeleine Udell 2 3 

Abstract 

This paper explores challenges in training Physics-Informed Neural Networks (PINNs), emphasiz-ing the role of the loss landscape in the training process. We examine difficulties in minimizing the PINN loss function, particularly due to ill-conditioning caused by differential operators in the residual term. We compare gradient-based optimizers Adam, L-BFGS, and their combina-tion Adam+L-BFGS, showing the superiority of Adam+L-BFGS, and introduce a novel second-order optimizer, NysNewton-CG (NNCG), which significantly improves PINN performance. Theo-retically, our work elucidates the connection be-tween ill-conditioned differential operators and ill-conditioning in the PINN loss and shows the benefits of combining first- and second-order op-timization methods. Our work presents valuable insights and more powerful optimization strate-gies for training PINNs, which could improve the utility of PINNs for solving difficult partial differential equations. 

1. Introduction 

The study of Partial Differential Equations (PDEs) grounds a wide variety of scientific and engineering fields, yet these fundamental physical equations are often difficult to solve numerically. Recently, neural network-based approaches including physics-informed neural networks (PINNs) have shown promise to solve both forward and inverse prob-lems involving PDEs (Raissi et al., 2019; E & Yu, 2018; Lu et al., 2021a;b; Karniadakis et al., 2021; Cuomo et al., 2022). PINNs parameterize the solution to a PDE with a neural network, and are often fit by minimizing a least-squares 

> 1

Department of Electrical Engineering, Stanford University, Stanford, CA, USA 2ICME, Stanford University, Stanford, CA, USA 3Department of Management Science & Engineering, Stan-ford University, Stanford, CA, USA 4Department of Statistics and Data Science, Yale University, New Haven, CT, USA. Correspon-dence to: Pratik Rathore <pratikr@stanford.edu >.

Proceedings of the 41 st International Conference on Machine Learning , Vienna, Austria. PMLR 235, 2024. Copyright 2024 by the author(s). 0 10000 20000 30000 40000 Iterations 10 −4

> 10 −3
> 10 −2
> 10 −1
> 10 0
> Loss

Wave, β = 5   

> Adam L-BFGS NNCG

Figure 1. On the wave PDE, Adam converges slowly due to ill-conditioning and the combined Adam+L-BFGS optimizer stalls after about 40000 steps. Running NNCG (our method) after Adam+L-BFGS provides further improvement. 

loss involving the PDE residual, boundary condition(s), and initial condition(s). The promise of PINNs is the potential to obtain solutions to PDEs without discretizing or meshing the space, enabling scalable solutions to high-dimensional prob-lems that currently require weeks on advanced supercom-puters. This loss is typically minimized with gradient-based optimizers such as Adam (Kingma & Ba, 2014), L-BFGS (Liu & Nocedal, 1989), or a combination of both. However, the challenge of optimizing PINNs restricts the ap-plication and development of these methods. Previous work has shown that the PINN loss is difficult to minimize (Krish-napriyan et al., 2021; Wang et al., 2021a; 2022b; De Ryck et al., 2023) even in simple settings. As a result, the PINN often fails to learn the solution. Furthermore, optimiza-tion challenges can obscure the effectiveness of new neural network architectures for PINNs, as an apparently inferior performance may stem from insufficient loss function opti-mization rather than inherent limitations of an architecture. A simple, reliable training paradigm is critical to enable wider adoption of PINNs. This work explores the loss landscape of PINNs and the challenges this landscape poses for gradient-based optimiza-tion methods. We provide insights from optimization theory 1

> arXiv:2402.01868v2 [cs.LG] 3 Jun 2024 Challenges in Training PINNs

that explain slow convergence of first-order methods such as Adam and show how ill-conditioned differential operators make optimization difficult. We also use our theoretical in-sights to improve the PINN training pipeline by combining existing and new optimization methods. The most closely related works to ours are Krishnapriyan et al. (2021); De Ryck et al. (2023), which both identify ill-conditioning in the PINN loss. Unlike Krishnapriyan et al. (2021), we empirically confirm the ill-conditioning of the loss by visualizing the spectrum of the Hessian and demonstrating how quasi-Newton methods improve the con-ditioning. Our theoretical results directly show how an ill-conditioned linear operator induces an ill-conditioned ob-jective, in contrast to the approach in De Ryck et al. (2023) which relies on a linearization. 

Contributions. We highlight contributions of this paper: • We demonstrate that the loss landscape of PINNs is ill-conditioned due to differential operators in the residual term and show that quasi-Newton methods improve the conditioning by 1000 × or more (Section 5). • We compare three optimizers frequently used for train-ing PINNs: (i) Adam, (ii) L-BFGS, and (iii) Adam followed by L-BFGS (referred to as Adam+L-BFGS). We show that Adam+L-BFGS is superior across a vari-ety of network sizes (Section 6). • We show the PINN solution resembles the true PDE so-lution only for extremely small loss values (Section 4). However, we find that the loss returned by Adam+L-BFGS can be improved further, which also improves the PINN solution (Section 7). • Motivated by the ill-conditioned loss landscape, we introduce a novel second-order optimizer, NysNewton-CG (NNCG). We show NNCG can significantly im-prove the solution returned by Adam+L-BFGS (Fig-ure 1 and Section 7). • We prove that ill-conditioned differential operators lead to an ill-conditioned PINN loss (Section 8). We also prove that combining first- and second-order methods (e.g., Adam+L-BFGS) leads to fast convergence, pro-viding justification for the importance of the combined method (Section 8). 

Notation. We denote the Euclidean norm by ∥ · ∥ 2 and use 

∥M ∥ to denote the operator norm of M ∈ Rm×n. For a smooth function f : Rp → R, we denote its gradient at 

w ∈ Rp by ∇f (w) and its Hessian by Hf (w). We write 

∂wi f for ∂f /∂w i. For Ω ⊂ Rd, we denote its boundary by 

∂Ω. For any m ∈ N, we use Im to denote the m×m identity matrix. Finally, we use ⪯ to denote the Loewner ordering on the convex cone of positive semidefinite matrices. 

2. Problem Setup 

This section introduces physics-informed neural networks as optimization problems and our experimental methodology. 

2.1. Physics-informed Neural Networks 

The goal of physics-informed neural networks is to solve partial differential equations. Similar to prior work (Lu et al., 2021b; Hao et al., 2023), we consider the following system of partial differential equations: 

D[u(x), x ] = 0 , x ∈ Ω, (1a) 

B[u(x), x ] = 0 , x ∈ ∂Ω, (1b) where D is a differential operator defining the PDE, B is an operator associated with the boundary and/or initial condi-tions, and Ω ⊆ Rd. To solve (1), PINNs model u as a neural network u(x; w) (often a multi-layer perceptron (MLP)) and approximate the true solution by the network whose weights solve the following non-linear least-squares problem: minimize  

> w∈Rp

L(w) := 12nres 

> nres

X

> i=1

D[u(xir ; w), x ir ]2 (2) 

+ 12nbc 

> nbc

X

> i=1



B[u(xjb; w), x jb]

2

.

Here {xir }nres  

> i=1

are the residual points and {xjb}nbc  

> j=1

are the boundary/initial points. The first loss term measures how much u(x; w) fails to satisfy the PDE, while the second term measures how much u(x; w) fails to satisfy the bound-ary/initial conditions. For this loss, L(w) = 0 means that u(x; w) exactly satis-fies the PDE and boundary/initial conditions at the training points. In deep learning, this condition is called interpola-tion (Zhang et al., 2021; Belkin, 2021). There is no noise in (1), so the true solution of the PDE would make (2) equal to zero. Hence a PINN approach should choose an architec-ture and an optimizer to achieve interpolation. Moreover, smaller training error corresponds to better generalization for PINNs (Mishra & Molinaro, 2023). Common optimizers for (2) include Adam, L-BFGS, and Adam+L-BFGS (Raissi et al., 2019; Krishnapriyan et al., 2021; Hao et al., 2023). 

2.2. Experimental Methodology 

We conduct experiments on optimizing PINNs for convec-tion, wave PDEs, and a reaction ODE. These equations have been studied in previous works investigating difficulties in training PINNs; we use the formulations in Krishnapriyan et al. (2021); Wang et al. (2022b) for our experiments. The coefficient settings we use for these equations are consid-ered challenging in the literature (Krishnapriyan et al., 2021; Wang et al., 2022b). Appendix A contains additional details. 2Challenges in Training PINNs 

We compare the performance of Adam, L-BFGS, and Adam+L-BFGS on training PINNs for all three classes of PDEs. For Adam, we tune the learning rate by a grid search on {10 −5, 10 −4, 10 −3, 10 −2, 10 −1}. For L-BFGS, we use the default learning rate 1.0, memory size 100 , and strong Wolfe line search. For Adam+L-BFGS, we tune the learn-ing rate for Adam as before, and also vary the switch from Adam to L-BFGS (after 1000, 11000, 31000 iterations). These correspond to Adam+L-BFGS (1k), Adam+L-BFGS (11k), and Adam+L-BFGS (31k) in our figures. All three methods are run for a total of 41000 iterations. We use multilayer perceptrons (MLPs) with tanh activations and three hidden layers. These MLPs have widths 50, 100, 200, or 400. We initialize these networks with the Xavier normal initialization (Glorot & Bengio, 2010) and all biases equal to zero. Each combination of PDE, optimizer, and MLP architecture is run with 5 random seeds. We use 10000 residual points randomly sampled from a 

255 × 100 grid on the interior of the problem domain. We use 257 equally spaced points for the initial conditions and 101 equally spaced points for each boundary condition. We assess the discrepancy between the PINN solution and the ground truth using ℓ2 relative error (L2RE), a standard metric in the PINN literature. Let y = ( yi)ni=1 be the PINN prediction and y′ = ( y′

> i

)ni=1 the ground truth. Define 

L2RE = 

s Pni=1 (yi − y′

> i

)2

Pni=1 y′2

> i

=

s

∥y − y′∥22

∥y′∥22

.

We compute the L2RE using all points in the 255 × 100 grid on the interior of the problem domain, along with the 257 and 101 points used for the initial and boundary conditions. We develop our experiments in PyTorch 2.0.0 (Paszke et al., 2019) with Python 3.10.12. Each experiment is run on a single NVIDIA Titan V GPU using CUDA 11.8. The code for our experiments is available at https://github.com/pratikrathore8/opt for pinns. 

3. Related Work 

Here we review common approaches for solving PDEs with physics-informed machine learning and PINN training strategies proposed in the literature. 

3.1. Physics-informed ML for Solving PDEs 

A variety of ML-based methods for solving PDEs have been proposed, including PINNs (Raissi et al., 2019), the Fourier Neural Operator (FNO) (Li et al., 2021), and DeepONet (Lu et al., 2021a). The PINN approach solves the PDE by using the loss function to penalize deviations from the PDE residual, boundary, and initial conditions. Notably, PINNs do not require knowledge of the solution to solve the forward PDE problem. On the other hand, the FNO and DeepONet sample and learn from known solutions to a parameterized class of PDEs to solve PDEs with another fixed value of the parameter. However, these operator learning approaches may not produce predictions consistent with the underlying physical laws that produced the data, which has led to the development of hybrid approaches such as physics-informed DeepONet (Wang et al., 2021c). Our theory shows that the ill-conditioning issues we study in PINNs are unavoidable for any ML-based approach that penalizes deviations from the known physical laws. 

3.2. Challenges in Training PINNs 

The vanilla PINN (Raissi et al., 2019) can perform poorly when trying to solve high-dimensional, non-linear, and/or multi-scale PDEs. Researchers have proposed a variety of modifications to the vanilla PINN to address these is-sues, many of which attempt to make the optimization prob-lem easier to solve. Wang et al. (2021a; 2022a;b); Nabian et al. (2021); Wu et al. (2023a;b) propose loss reweight-ing/resampling to balance different components of the loss, Yao et al. (2023); M¨ uller & Zeinhofer (2023) propose scale-invariant and natural gradient-based optimizers for PINN training, Jagtap et al. (2020a;b); Wang et al. (2023) propose adaptive activation functions which can accelerate conver-gence of the optimizer, and Liu et al. (2024) propose an approach to precondition the PINN loss itself. Other ap-proaches include innovative loss functions and regulariza-tions (E & Yu, 2018; Lu et al., 2021c; Kharazmi et al., 2021; Khodayi-Mehr & Zavlanos, 2020; Yu et al., 2022) and new architectures (Jagtap et al., 2020c; Jagtap & Karniadakis, 2020; Li et al., 2020; Moseley et al., 2023). These strategies work with varying degrees of success, and no single strategy improves performance across all PDEs. Our work attempts to understand and tame the ill-conditioning in the (vanilla) PINN loss directly. We ex-pect our ideas to work well with many of the above training strategies for PINNs; none of these training strategies rid the objective of the differential operator that generates the ill-conditioning in the PINN loss (with the possible exception of Liu et al. (2024)). However, Liu et al. (2024) precon-ditions the PINN loss directly, which is equivalent to left preconditioning, while our work studies the effects of pre-conditioned optimization methods on the PINN loss, which is equivalent to right preconditioning (Appendix C.1). There is potential in combining the approach of Liu et al. (2024) and our approach to obtain a more reliable framework for training PINNs. Our work analyzes the spectrum (eigenvalues) of the Hes-sian HL of the loss. Previous work (Wang et al., 2022b) studies the conditioning of the loss using the neural tangent kernel (NTK), which requires an infinite-width assumption 3Challenges in Training PINNs 

on the neural network; our work studies the conditioning of the loss through the lens of the Hessian and yields useful results for finite-width PINN architectures. Several works have also studied the spectral bias of PINNs (Wang et al., 2021b; 2022b; Moseley et al., 2023), which refers to the in-ability of neural networks to learn high-frequency functions. Note that our paper uses the word spectrum to refer to the Hessian eigenvalues, not the spectrum of the PDE solution. 

4. Good Solutions Require Near-zero Loss 

First, we show that PINNs must be trained to near-zero loss to obtain a reasonably low L2RE. This phenomenon can be observed in Figure 2, demonstrating that a lower loss generally corresponds to a lower L2RE. For example, on the convection PDE, a loss of 10 −3 yields an L2RE around 

10 −1, but decreasing the loss by a factor of 100 to 10 −5

yields an L2RE around 10 −2, a 10 × improvement. This relationship between loss and L2RE in Figure 2 is typical of many PDEs (Lu et al., 2022). The relationship in Figure 2 underscores that high-accuracy optimization is required for a useful PINN. There are in-stances (especially on the reaction ODE), where the PINN solution has a L2RE around 1, despite a near-zero loss; we provide insight into why this is occurring in Appendix B. In Sections 5 and 7, we show that ill-conditioning and under-optimization make reaching a solution with sufficient accu-racy difficult. 

5. The Loss Landscape is Ill-conditioned 

We show empirically that the ill-conditioning of the PINN loss is mainly due to the residual loss, which contains the dif-ferential operator. We also show that quasi-Newton methods like L-BFGS improve the conditioning of the problem. 

5.1. The PINN Loss is Ill-conditioned 

The conditioning of the loss L plays a key role in the perfor-mance of first-order optimization methods (Nesterov, 2018). We can understand the conditioning of an optimization prob-lem through the eigenvalues of the Hessian of the loss, HL.Intuitively, the eigenvalues of HL provide information about the local curvature of the loss function at a given point along different directions. The condition number is defined as the ratio of the largest magnitude’s eigenvalue to the smallest magnitude’s eigenvalue. A large condition number implies the loss is very steep in some directions and flat in others, making it difficult for first-order methods to make suffi-cient progress toward the minimum. When HL(w) has a large condition number (particularly, for w near the opti-mum), the loss L is called ill-conditioned . For example, the convergence rate of gradient descent (GD) depends on the condition number (Nesterov, 2018), which results in GD converging slowly on ill-conditioned problems. To investigate the conditioning of the PINN loss L, we would like to examine the eigenvalues of the Hessian. For large matrices, it is convenient to visualize the set of eigen-values via spectral density , which approximates the distribu-tion of the eigenvalues. Fast approximation methods for the spectral density of the Hessian are available for deep neural networks (Ghorbani et al., 2019; Yao et al., 2020). Figure 3 shows the estimated Hessian spectral density (solid lines) of the PINN loss for the convection, reaction, and wave problems after training with Adam+L-BFGS. For all three problems, we observe large outlier eigenvalues ( > 10 4 for convection, > 10 3 for reaction, and > 10 5 for wave) in the spectrum, and a significant spectral density near 0, implying that the loss L is ill-conditioned. The plots also show how the spectrum is improved by preconditioning (Section 5.3). 

5.2. The Ill-conditioning is Due to the Residual Loss 

We use the same method to study the conditioning of each component of the PINN loss. Figures 3 and 7 show the esti-mated spectral density of the Hessian of the residual, initial condition, and boundary condition components of the PINN loss for each problem after training with Adam+L-BFGS. We see residual loss, which contains the differential operator 

D, is the most ill-conditioned among all components. Our theory (Section 8) shows this ill-conditioning is likely due to the ill-conditioning of D.

5.3. L-BFGS Improves Problem Conditioning 

Preconditioning is a popular technique for improving con-ditioning in optimization. A classic example is Newton’s method, which uses second-order information (i.e., the Hes-sian) to (locally) transform an ill-conditioned loss landscape into a well-conditioned one. L-BFGS is a quasi-Newton method that improves conditioning without explicit access to the problem Hessian. To examine the effectiveness of quasi-Newton methods for optimizing L, we compute the spectral density of the Hessian after L-BFGS precondition-ing. (For details of this computation and how L-BFGS preconditions, see Appendix C.) Figure 3 shows this pre-conditioned Hessian spectral density (dashed lines). For all three problems, the magnitude of eigenvalues and the condition number has been reduced by at least 10 3. In addi-tion, the preconditioner improves the conditioning of each individual loss component of L (Figures 3 and 7). These ob-servations offer clear evidence that quasi-Newton methods improve the conditioning of the loss, and show the impor-tance of quasi-Newton methods in training PINNs, which we demonstrate in Section 6. 4Challenges in Training PINNs 10 −5 10 −4 10 −3 10 −2 10 −1 10 0              

> Loss 10 −2
> 10 −1
> 10 0
> L2RE
> Convection, β= 40
> 10 −410 −210 0
> Loss 10 −1
> 10 0
> L2RE
> Reaction, ρ= 5
> 10 −310 −210 −1
> Loss 10 −1
> 10 0
> L2RE
> Wave, β= 5
> Adam L-BFGS Adam + L-BFGS (1k) Adam + L-BFGS (11k) Adam + L-BFGS (31k)

Figure 2. We plot the final L2RE against the final loss for each combination of network width, optimization strategy, and random seed. Across all three PDEs, a lower loss generally corresponds to a lower L2RE. 0 10 0 10 1 10 2 10 3 10 4                                      

> Eigenvalue 10 −10
> 10 −7
> 10 −4
> 10 −1
> 10 2
> Density
> Convection, β= 40
> −10 1−10 0010 010 110 210 3
> Eigenvalue 10 −10
> 10 −7
> 10 −4
> 10 −1
> 10 2
> Density
> Reaction, ρ= 5
> 010 010 110 210 310 410 5
> Eigenvalue 10 −10
> 10 −7
> 10 −4
> 10 −1
> 10 2
> Density
> Wave, β= 5
> −10 1−10 0010 010 110 210 310 4
> Eigenvalue 10 −10
> 10 −7
> 10 −4
> 10 −1
> 10 2
> Density
> Residual
> −10 1−10 0010 010 110 210 3
> Eigenvalue 10 −10
> 10 −7
> 10 −4
> 10 −1
> 10 2
> Density
> Initial Condition
> 010 010 110 210 3
> Eigenvalue 10 −10
> 10 −7
> 10 −4
> 10 −1
> 10 2
> Density
> Boundary Condition
> Total Loss Loss Components for Convection, β= 40
> Hessian Preconditioned Hessian

Figure 3. (Top) Spectral density of the Hessian and the preconditioned Hessian after 41000 iterations of Adam+L-BFGS. The plots show that the PINN loss is ill-conditioned and that L-BFGS improves the conditioning, reducing the top eigenvalue by 10 3 or more. (Bottom) Spectral density of the Hessian and the preconditioned Hessian of each loss component after 41000 iterations of Adam+L-BFGS for convection. The plots show that each component loss is ill-conditioned and that the conditioning is improved by L-BFGS. 

6. Adam+L-BFGS Optimizes the Loss Better Than Other Methods 

We demonstrate that the combined optimization method Adam+L-BFGS consistently provides a smaller loss and L2RE than using Adam or L-BFGS alone. We justify this finding using intuition from optimization theory. 

6.1. Adam+L-BFGS vs Adam or L-BFGS 

Figure 8 in Appendix D compares Adam+L-BFGS, Adam, and L-BFGS on the convection, reaction, and wave prob-lems at difficult coefficient settings noted in the literature (Krishnapriyan et al., 2021; Wang et al., 2022b). Across each network width, the lowest loss and L2RE is always delivered by Adam+L-BFGS. Similarly, the lowest median loss and L2RE are almost always delivered by Adam+L-BFGS (Figure 8). The only exception is the reaction prob-lem, where Adam outperforms Adam+L-BFGS on loss at width = 100 and L2RE at width = 200 (Figure 8). 

Table 1. Lowest loss for Adam, L-BFGS, and Adam+L-BFGS across all network widths after hyperparameter tuning. Adam+L-BFGS attains both smaller loss and L2RE vs. Adam or L-BFGS.                           

> Optimizer Convection Reaction Wave Loss L2RE Loss L2RE Loss L2RE Adam 1.40e-4 5.96e-2 4.73e-6 2.12e-2 2.03e-2 3.49e-1 L-BFGS 1.51e-5 8.26e-3 8.93e-6 3.83e-2 1.84e-2 3.35e-1 Adam+L-BFGS 5.95e-6 4.19e-3 3.26e-6 1.92e-2 1.12e-3 5.52e-2

Table 1 summarizes the best performance of each optimizer. Again, Adam+L-BFGS is better than running either Adam or L-BFGS alone. Notably, Adam+L-BFGS attains 14.2 ×

smaller L2RE than Adam on the convection problem and 6.07 × smaller L2RE than L-BFGS on the wave problem. 

6.2. Intuition From Optimization Theory 

The success of Adam+L-BFGS over Adam and L-BFGS can be explained by existing results in optimization theory. In neural networks, saddle points typically outnumber local 5Challenges in Training PINNs 

minima (Dauphin et al., 2014; Lee et al., 2019). A saddle point can never be a global minimum. We want to reach a global minimum when training PINNs. Newton’s method (which L-BFGS attempts to approximate) is attracted to saddle points (Dauphin et al., 2014), and quasi-Newton methods such as L-BFGS also converge to saddle points since they ignore negative curvature (Dauphin et al., 2014). On the other hand, first-order methods such as gradient descent and AdaGrad (Duchi et al., 2011) avoid saddle points (Lee et al., 2019; Antonakopoulos et al., 2022). We expect that (full-gradient) Adam also avoids saddles for similar reasons, although we are not aware of such a result. Alas, first-order methods converge slowly when the prob-lem is ill-conditioned. This result generalizes the well-known slow convergence of conjugate gradient (CG) for ill-conditioned linear systems: O(√κ log( 1 

> ϵ

)) iterations to converge to an ϵ-approximate solution of a system with con-dition number κ. In optimization, an analogous notion of a condition number in a set S near a global minimum is given by κf (S) := sup w∈S ∥Hf (w)∥/μ , where μ is the PŁ ⋆-constant (see Section 8). Then gradient descent requires 

O(κf (S) log( 1 

> ϵ

)) iterations to converge to an ϵ-suboptimal point. For PINNs, the condition number near a solution is often > 10 4 (Figure 3), which leads to slow convergence of first-order methods. However, Newton’s method and L-BFGS can significantly reduce the condition number (Fig-ure 3), which yields faster convergence. Adam+L-BFGS combines the best of both first- and second-order/quasi-Newton methods. By running Adam first, we avoid saddle points that would attract L-BFGS. By running L-BFGS after Adam, we can reduce the condition number of the problem, which leads to faster local convergence. Figure 1 exemplifies this, showing faster convergence of Adam+L-BFGS over Adam on the wave equation. This intuition also explains why Adam sometimes performs as well as Adam+L-BFGS on the reaction problem. Figure 3 shows the largest eigenvalue of the reaction problem is around 10 3, while the largest eigenvalues of the convection and wave problems are around 10 4 and 10 5, suggesting the reaction problem is less ill-conditioned. 

7. The Loss is Often Under-optimized 

In Section 6, we show that Adam+L-BFGS improves on running Adam or L-BFGS alone. However, even Adam+L-BFGS does not reach a critical point of the loss: the loss is still under-optimized. We show that the loss and L2RE can be further improved by running a damped version of Newton’s method. 

7.1. Why is the Loss Under-optimized? 

Figure 4 shows the run of Adam+L-BFGS with smallest L2RE for each PDE. For each run, L-BFGS stops making progress before reaching the maximum number of iterations. L-BFGS uses strong Wolfe line search , as it is needed to maintain the stability of L-BFGS (Nocedal & Wright, 2006). L-BFGS often terminates because it cannot find a positive step size satisfying these conditions—we have observed several instances where L-BFGS picks a step size of zero (Figure 9 in Appendix E), leading to early stopping. Per-versely, L-BFGS stops in these cases without reaching a critical point: the gradient norm is around 10 −2 or 10 −3

(see the bottom row of Figure 4). The gradient still contains useful information for improving the loss. 

7.2. NysNewton-CG (NNCG) 

We can avoid premature termination by using a damped version of Newton’s method with Armijo line search . The Armijo conditions use only a subset of the strong Wolfe con-ditions. Under only Armijo conditions, L-BFGS is unstable; we require a different approximation to the Hessian ( p × p

for a neural net with p parameters) that does not require storing ( O(p2)) or inverting ( O(p3)) the Hessian. Instead, we run a Newton-CG algorithm that solves for the Newton step using preconditioned conjugate gradient (PCG). This al-gorithm can be implemented efficiently with Hessian-vector products. These can be computed O (( nres + nbc )p) time (Pearlmutter, 1994). Section 5 shows that the Hessian is ill-conditioned with fast spectral decay, so CG without precon-ditioning will converge slowly. Hence we use Nystr¨ omPCG, a PCG method that is designed to solve linear systems with fast spectral decay (Frangella et al., 2023). The resulting algorithm is called NysNewton-CG (abbreviated NNCG); a full description of the algorithm appears in Appendix E. 

7.3. Performance of NNCG 

Figure 4 shows that NNCG significantly improves both the loss and gradient norm of the solution when applied after Adam+L-BFGS, while Figure 5 visualizes how NNCG im-proves the absolute error (pointwise) of the PINN solution when applied after Adam+L-BFGS. Furthermore, Table 2 shows that NNCG also improves the L2RE of the PINN solution. In contrast, applying gradient descent (GD) af-ter Adam+L-BFGS improves neither the loss nor the L2RE. This result is unsurprising, as our theory predicts that NNCG will work better than GD for an ill-conditioned loss (Sec-tion 8). 

7.4. Why Not Use NNCG Directly After Adam? 

Since NNCG improves the PINN solution and uses sim-pler line search conditions than L-BFGS, it is tempting to 6Challenges in Training PINNs 0 10000 20000 30000 40000 Iterations 10 −5

10 −3

10 −1

10 1

> Loss

Convection, β = 40 

0 10000 20000 30000 40000 Iterations 10 −5

10 −3

10 −1

> Loss

Reaction, ρ = 5 

0 10000 20000 30000 40000 Iterations 10 −4

10 −3

10 −2

10 −1

10 0

> Loss

Wave, β = 5 

0 10000 20000 30000 40000 Iterations 10 −3

10 −1

10 1

> Gradient Norm

Convection, β = 40 

0 10000 20000 30000 40000 Iterations 10 −4

10 −2

10 0

10 2

> Gradient Norm

Reaction, ρ = 5 

0 10000 20000 30000 40000 Iterations 10 −2

10 −1

10 0

> Gradient Norm

Wave, β = 5 

Adam L-BFGS NNCG GD 

Figure 4. Performance of NNCG and GD after Adam+L-BFGS. (Top) NNCG reduces the loss by a factor greater than 10 in all instances, while GD fails to make progress. (Bottom) Furthermore, NNCG significantly reduces the gradient norm on the convection and wave problems, while GD fails to do so. 0.0 0.2 0.4 0.6 0.8 1.0

t

0123456

> x

Adam 

0.0 0.2 0.4 0.6 0.8 1.0

t

0123456

> x

Adam + L-BFGS 

0.0 0.2 0.4 0.6 0.8 1.0

t

0123456

> x

Adam + L-BFGS + NNCG 

0.0 0.2 0.4 0.6 0.8 1.0

t

0123456

> x

Adam 

0.0 0.2 0.4 0.6 0.8 1.0

t

0123456

> x

Adam + L-BFGS 

0.0 0.2 0.4 0.6 0.8 1.0

t

0123456

> x

Adam + L-BFGS + NNCG 

0.0 0.2 0.4 0.6 0.8 1.0

t

0.00.20.40.60.81.0

> x

Adam 

0.0 0.2 0.4 0.6 0.8 1.0

t

0.00.20.40.60.81.0

> x

Adam + L-BFGS 

0.0 0.2 0.4 0.6 0.8 1.0

t

0.00.20.40.60.81.0

> x

Adam + L-BFGS + NNCG 

0.00.20.40.60.81.0

0.000 0.002 0.004 0.006 

0.000 0.002 0.004 0.006 

0.00.20.40.60.8

0.00 0.02 0.04 0.06 0.08 

0.00 0.02 0.04 0.06 0.08 

0.00 0.25 0.50 0.75 1.00 1.25 

0.000 0.025 0.050 0.075 0.100 0.125 0.150 

0.000 0.025 0.050 0.075 0.100 0.125 0.150 

Convection, β = 40 Reaction, ρ = 5 Wave, β = 5 

Figure 5. Absolute errors of the PINN solution at optimizer switch points. The first column shows errors after Adam, the second column shows errors after running L-BFGS following Adam, and the third column shows the errors after running NNCG folllowing Adam+L-BFGS. L-BFGS improves the solution obtained from first running Adam, and NNCG further improves the solution even after Adam+L-BFGS stops making progress. Note that Adam solution errors (left-most column) are presented at separate scales as these solutions are far off from the exact solutions. 

7Challenges in Training PINNs 

Table 2. Loss and L2RE after fine-tuning by NNCG and GD. NNCG outperforms both GD and the original Adam+L-BFGS results.                           

> Optimizer Convection Reaction Wave Loss L2RE Loss L2RE Loss L2RE Adam+L-BFGS 5.95e-6 4.19e-3 5.26e-6 1.92e-2 1.12e-3 5.52e-2 Adam+L-BFGS+NNCG 3.63e-7 1.94e-3 2.89e-7 9.92e-3 6.13e-5 1.27e-2
> Adam+L-BFGS+GD 5.95e-6 4.19e-3 5.26e-6 1.92e-2 1.12e-3 5.52e-2

replace L-BFGS with NNCG entirely. However, NNCG is slower than L-BFGS: the L-BFGS update can be com-puted in O(mp ) time, where m is the memory parameter, while just a single Hessian-vector product for computing the NNCG update requires O (( nres + nbc )p) time. Table 3 shows NNCG takes 5, 20, and 322 more times per-iteration as L-BFGS on convection, reaction, and wave respectively. Consequently, we should run Adam+L-BFGS to make as much progress as possible before switching to NNCG. 

8. Theory 

We relate the conditioning of the differential operator to the conditioning of the PINN loss function (2) in Theorem 8.4. When the differential operator is ill-conditioned, gradient descent takes many iterations to reach a high-precision solu-tion. As a result, first-order methods alone may not deliver sufficient accuracy. 

Algorithm 1 Gradient-Damped Newton Descent (GDND) 

input # of gradient descent iterations KGD , gradient descent learning rate ηGD , # of damped Newton iterations KDN , damped Newton learning rate ηDN , damping parameter γ

Phase I : Gradient descent for k = 0 , . . . , K GD − 1 do 

wk+1 = wk − ηGD ∇L(wk )

end for Phase II : Damped Newton 

Set ˜w0 = wKGD 

for k = 0 , . . . , K DN − 1 do 

˜wk+1 = ˜ wk − ηDN (HL( ˜ wk ) + γI )−1 ∇L( ˜ wk )

end for output approximate solution ˜wKDN 

To address this issue, we develop and analyze a hybrid algorithm, Gradient Damped Newton Descent (GDND, Al-gorithm 1), that switches from gradient descent to damped Newton’s method after a fixed number of iterations. We show that GDND gives fast linear convergence independent of the condition number. This theory supports our empirical results, which show that the best performance is obtained by running Adam and switching to L-BFGS. Moreover, it pro-vides a theoretical basis for using Adam+L-BFGS+NNCG to achieve the best performance. GDND differs from Adam+L-BFGS+NNCG, the algorithm we recommend in practice. We analyze GD instead of Adam because existing analyses of Adam (D´ efossez et al., 2022; Zhang et al., 2022) do not mirror its empirical performance. The reason we run both L-BFGS and damped Newton is to maximize computational efficiency (Section 7.4). 

8.1. Preliminaries 

We begin with the main assumption for our analysis. 

Assumption 8.1 (Interpolation) . Let W⋆ denote the set of minimizers of (2). We assume that 

L(w⋆) = 0 , for all w⋆ ∈ W ⋆,

i.e., the model perfectly fits the training data. From a theoretical standpoint, Assumption 8.1 is natural in light of various universal approximation theorems (Cy-benko, 1989; Hornik et al., 1990; De Ryck et al., 2021), which show neural networks are capable of approximating any continuous function to arbitrary accuracy. Moreover, in-terpolation in neural networks is common in practice (Zhang et al., 2021; Belkin, 2021). 

PŁ ⋆-condition. In modern neural network optimization, the PŁ ⋆-condition (Liu et al., 2022; 2023) is key to showing convergence of gradient-based optimizers. It is a local ver-sion of the celebrated Polyak-Łojasiewicz condition (Polyak, 1963; Karimi et al., 2016), specialized to interpolation. 

Definition 8.2 (PŁ ⋆-condition) . Suppose L satisfies As-sumption 8.1. Let S ⊂ Rp. Then L is μ-PŁ ⋆in S if 

∥∇ L(w)∥2

2μ ≥ L(w), ∀w ∈ S .

The PŁ ⋆-condition relates the gradient norm to the loss and implies that any minimizer in S is a global minimizer. Im-portantly, the PŁ ⋆-condition can hold for non-convex losses and is known to hold, with high probability, for sufficiently wide neural nets with the least-squares loss (Liu et al., 2022). 

Definition 8.3 (Condition number for PŁ ⋆ loss functions) .

Let S be a set for which L is μ-PŁ ⋆. Then the condition number of L over S is given by 

κL(S) = sup w∈S ∥HL(w)∥

μ ,

where HL(w) is the Hessian matrix of the loss function. Gradient descent over S converges to ϵ-suboptimality in 

O κL(S) log  1

> ϵ

 iterations (Liu et al., 2022). 8Challenges in Training PINNs 

8.2. Ill-conditioned Differential Operators Lead to Challenging Optimization 

Here, we show that when the differential operator defining the PDE is linear and ill-conditioned, the condition number of the PINN objective (in the sense of Definition 8.3) is large. Our analysis in this regard is inspired by the recent work of De Ryck et al. (2023), who prove a similar result for the population PINN residual loss. However, De Ryck et al. (2023)’s analysis is based on the lazy training regime ,which assumes the NTK is approximately constant. This regime does not accurately capture the behavior of practical neural networks (Allen-Zhu & Li, 2019; Chizat et al., 2019; Ghorbani et al., 2020; 2021). Moreover, gradient descent can converge even with a non-constant NTK (Liu et al., 2020). Our theoretical result is more closely aligned with deep learning practice as it does not assume lazy training and pertains to the empirical loss rather than the population loss. Theorem 8.4 provides an informal version of our result in Appendix F that shows that ill-conditioned differential op-erators induce ill-conditioning in the loss (2). The theorem statement involves a kernel integral operator, K∞ (defined in (6) in Appendix F), evaluated at the optimum w⋆.

Theorem 8.4 (Informal) . Suppose Assumption 8.1 holds and p ≥ nres + nbc . Fix w⋆ ∈ W ⋆ and set A = D∗D. For some α > 1/2, suppose the eigenvalues of A ◦ K ∞(w⋆) sat-isfy λj (A◦K ∞(w⋆)) = O j−2α. If √nres = Ω log  1

> δ

 ,then for any set S that contains w⋆ and for which L is μ-PŁ ⋆,

κL(S) = Ω ( nα

> res

) , with probability ≥ 1 − δ. 

Theorem 8.4 relates the conditioning of the PINN optimiza-tion problem to the conditioning of the operator A◦K ∞(w⋆),where A is the Hermitian square of D. If the spectrum of 

A ◦ K ∞(w⋆) decays polynomially, then, with high probabil-ity, the condition number grows with nres . As nres typically ranges from 10 3 to 10 4, Theorem 8.4 shows the condition number of the PINN problem is generally large, and so first-order methods will be slow to converge to the optimum. Figure 10 in Appendix F.5 empirically verifies the claim of Theorem 8.4 for the convection equation. 

8.3. Efficient High-precision Solutions via GDND 

We now analyze the convergence behavior of Algorithm 1. Theorem 8.5 provides an informal version of our result in Appendix G. 

Theorem 8.5 (Informal) . Suppose L(w) satisfies the μ-PŁ ⋆-condition in a certain ball about w0. Then there exists 

ηGD > 0 and KGD < ∞ such that Phase I of Algorithm 1 outputs a point wKGD , for which Phase II of Algorithm 1 with ηDN = 5 /6 and appropriate damping γ > 0, satisfies 

L( ˜ wk) ≤

 23

k

L(wKGD ).

Hence after KDN ≥ 3 log 

 L(wKGD )

> ϵ



iterations, Phase II of Algorithm 1 outputs a point satisfying L( ˜ wKDN ) ≤ ϵ. 

Theorem 8.5 shows only a fixed number of gradient de-scent iterations are needed before Algorithm 1 can switch to damped Newton’s method and enjoy linear convergence independent of the condition number. As the convergence rate of Phase II with damped Newton is independent of the condition number, Algorithm 1 produces a highly accurate solution to (2). Note that Theorem 8.5 is local; Algorithm 1 must find a point sufficiently close to a minimizer with gradient descent before switching to damped Newton’s method and achieving rapid convergence. It is not possible to develop a second-order method with a fast rate that does not require a good initialization, as in the worst-case, global convergence of second-order methods may fail to improve over first-order methods (Cartis et al., 2010; Arjevani et al., 2019). More-over, Theorem 8.5 is consistent with our experiments, which show L-BFGS is inferior to Adam+L-BFGS. 

9. Conclusion 

In this work, we explore the challenges posed by the loss landscape of PINNs for gradient-based optimizers. We demonstrate ill-conditioning in the PINN loss and show it hinders effective training of PINNs. By comparing Adam, L-BFGS, and Adam+L-BFGS, and introducing NNCG, we have demonstrated several approaches to improve the train-ing process. Our theory supports our experimental find-ings: we connect ill-conditioned differential operators to ill-conditioning in the PINN loss and prove the benefits of second-order methods over first-order methods for PINNs. 

Acknowledgements 

We would like to acknowledge helpful comments from the anonymous reviewers and area chairs, which have improved this submission. MU, PR, WL, and ZF gratefully acknowl-edge support from the National Science Foundation (NSF) Award IIS-2233762, the Office of Naval Research (ONR) Award N000142212825 and N000142312203, and the Al-fred P. Sloan Foundation. LL gratefully acknowledges sup-port from the U.S. Department of Energy [DE-SC0022953]. 

Impact Statement 

This paper presents work whose goal is to advance the field of scientific machine learning. There are many potential 9Challenges in Training PINNs 

societal consequences of our work, none which we feel must be specifically highlighted here. 

References 

Allen-Zhu, Z. and Li, Y. What Can ResNet Learn Effi-ciently, Going Beyond Kernels? In Advances in Neural Information Processing Systems , 2019. Antonakopoulos, K., Mertikopoulos, P., Piliouras, G., and Wang, X. AdaGrad Avoids Saddle Points. In Proceed-ings of the 39th International Conference on Machine Learning , 2022. Arjevani, Y., Shamir, O., and Shiff, R. Oracle complexity of second-order methods for smooth convex optimization. 

Mathematical Programming , 178:327–360, 2019. Bach, F. Sharp analysis of low-rank kernel matrix approxi-mations. In Conference on learning theory , 2013. Belkin, M. Fit without fear: remarkable mathematical phe-nomena of deep learning through the prism of interpola-tion. Acta Numerica , 30:203–248, 2021. Cartis, C., Gould, I. N., and Toint, P. L. On the complexity of steepest descent, Newton’s and regularized Newton’s methods for nonconvex unconstrained optimization prob-lems. SIAM Journal on Optimization , 20(6):2833–2852, 2010. Chizat, L., Oyallon, E., and Bach, F. On Lazy Training in Differentiable Programming. In Advances in Neural Information Processing Systems , 2019. Cohen, M. B., Musco, C., and Musco, C. Input sparsity time low-rank approximation via ridge leverage score sampling. In Proceedings of the Twenty-Eighth Annual ACM-SIAM Symposium on Discrete Algorithms , 2017. Cuomo, S., Di Cola, V. S., Giampaolo, F., Rozza, G., Raissi, M., and Piccialli, F. Scientific Machine Learning Through Physics–Informed Neural Networks: Where We Are and What’s Next. J. Sci. Comput. , 92(3), 2022. Cybenko, G. Approximation by superpositions of a sig-moidal function. Mathematics of control, signals and systems , 2(4):303–314, 1989. Dauphin, Y. N., Pascanu, R., Gulcehre, C., Cho, K., Gan-guli, S., and Bengio, Y. Identifying and attacking the saddle point problem in high-dimensional non-convex op-timization. In Advances in Neural Information Processing Systems , 2014. De Ryck, T., Lanthaler, S., and Mishra, S. On the approx-imation of functions by tanh neural networks. Neural Networks , 143:732–750, 2021. De Ryck, T., Bonnet, F., Mishra, S., and de B´ ezenac, E. An operator preconditioning perspective on training in physics-informed machine learning. arXiv preprint arXiv:2310.05801 , 2023. D´ efossez, A., Bottou, L., Bach, F., and Usunier, N. A simple convergence proof of Adam and Adagrad. Transactions on Machine Learning Research , 2022. Duchi, J., Hazan, E., and Singer, Y. Adaptive Subgradient Methods for Online Learning and Stochastic Optimiza-tion. Journal of Machine Learning Research , 12(61): 2121–2159, 2011. E, W. and Yu, B. The Deep Ritz Method: A Deep Learning-Based Numerical Algorithm for Solving Variational Prob-lems. Communications in Mathematics and Statistics , 6 (1):1–12, 2018. Frangella, Z., Tropp, J. A., and Udell, M. Randomized Nystr¨ om Preconditioning. SIAM Journal on Matrix Anal-ysis and Applications , 44(2):718–752, 2023. Ghorbani, B., Krishnan, S., and Xiao, Y. An Investigation into Neural Net Optimization via Hessian Eigenvalue Density. In Proceedings of the 36th International Confer-ence on Machine Learning , 2019. Ghorbani, B., Mei, S., Misiakiewicz, T., and Montanari, A. When Do Neural Networks Outperform Kernel Methods? In Advances in Neural Information Processing Systems ,2020. Ghorbani, B., Mei, S., Misiakiewicz, T., and Montanari, A. Linearized two-layers neural networks in high dimension. 

The Annals of Statistics , 49(2):1029–1054, 2021. Glorot, X. and Bengio, Y. Understanding the difficulty of training deep feedforward neural networks. In Pro-ceedings of the Thirteenth International Conference on Artificial Intelligence and Statistics , 2010. Golub, G. H. and Meurant, G. Matrices, moments and quadrature with applications , volume 30. Princeton Uni-versity Press, 2009. Hao, Z., Yao, J., Su, C., Su, H., Wang, Z., Lu, F., Xia, Z., Zhang, Y., Liu, S., Lu, L., and Zhu, J. PINNa-cle: A Comprehensive Benchmark of Physics-Informed Neural Networks for Solving PDEs. arXiv preprint arXiv:2306.08827 , 2023. Horn, R. A. and Johnson, C. R. Matrix Analysis . Cambridge University Press, 2nd edition, 2012. Hornik, K., Stinchcombe, M., and White, H. Universal approximation of an unknown mapping and its derivatives using multilayer feedforward networks. Neural networks ,3(5):551–560, 1990. 10 Challenges in Training PINNs 

Jagtap, A. D. and Karniadakis, G. E. Extended physics-informed neural networks (xpinns): A generalized space-time domain decomposition based deep learning frame-work for nonlinear partial differential equations. Commu-nications in Computational Physics , 28(5):2002–2041, 2020. Jagtap, A. D., Kawaguchi, K., and Karniadakis, G. E. Adap-tive activation functions accelerate convergence in deep and physics-informed neural networks. Journal of Com-putational Physics , 404:109136, 2020a. Jagtap, A. D., Kawaguchi, K., and Karniadakis, G. E. Lo-cally adaptive activation functions with slope recovery for deep and physics-informed neural networks. Proceed-ings of the Royal Society A: Mathematical, Physical and Engineering Sciences , 2020b. Jagtap, A. D., Kharazmi, E., and Karniadakis, G. E. Con-servative physics-informed neural networks on discrete domains for conservation laws: Applications to forward and inverse problems. Computer Methods in Applied Mechanics and Engineering , 365:113028, 2020c. Karimi, H., Nutini, J., and Schmidt, M. Linear Convergence of Gradient and Proximal-Gradient Methods under the Polyak-Łojasiewicz Condition. In Machine Learning and Knowledge Discovery in Databases , 2016. Karniadakis, G. E., Kevrekidis, I. G., Lu, L., Perdikaris, P., Wang, S., and Yang, L. Physics-informed machine learning. Nature Reviews Physics , 3(6):422–440, 2021. Kharazmi, E., Zhang, Z., and Karniadakis, G. E. hp-VPINNs: Variational physics-informed neural networks with domain decomposition. Computer Methods in Ap-plied Mechanics and Engineering , 374:113547, 2021. Khodayi-Mehr, R. and Zavlanos, M. VarNet: Variational Neural Networks for the Solution of Partial Differential Equations. In Proceedings of the 2nd Conference on Learning for Dynamics and Control , pp. 298–307, 2020. Kingma, D. P. and Ba, J. Adam: A method for stochastic optimization. arXiv preprint arXiv:1412.6980 , 2014. Krishnapriyan, A., Gholami, A., Zhe, S., Kirby, R., and Mahoney, M. W. Characterizing possible failure modes in physics-informed neural networks. In Advances in Neural Information Processing Systems , 2021. Lee, J. D., Panageas, I., Piliouras, G., Simchowitz, M., Jor-dan, M. I., and Recht, B. First-order methods almost always avoid strict saddle points. Mathematical Program-ming , 176(1):311–337, 2019. Li, K., Tang, K., Wu, T., and Liao, Q. D3M: A Deep Domain Decomposition Method for Partial Differential Equations. 

IEEE Access , 8:5283–5294, 2020. Li, Z., Kovachki, N. B., Azizzadenesheli, K., liu, B., Bhat-tacharya, K., Stuart, A., and Anandkumar, A. Fourier Neural Operator for Parametric Partial Differential Equa-tions. In International Conference on Learning Represen-tations , 2021. Lin, L., Saad, Y., and Yang, C. Approximating spectral densities of large matrices. SIAM review , 58(1):34–65, 2016. Liu, C., Zhu, L., and Belkin, M. On the linearity of large non-linear models: when and why the tangent kernel is constant. Advances in Neural Information Processing Systems , 2020. Liu, C., Zhu, L., and Belkin, M. Loss landscapes and opti-mization in over-parameterized non-linear systems and neural networks. Applied and Computational Harmonic Analysis , 59:85–116, 2022. Liu, C., Drusvyatskiy, D., Belkin, M., Davis, D., and Ma, Y.-A. Aiming towards the minimizers: fast convergence of SGD for overparametrized problems. arXiv preprint arXiv:2306.02601 , 2023. Liu, D. C. and Nocedal, J. On the limited memory BFGS method for large scale optimization. Mathematical Pro-gramming , 45(1):503–528, 1989. Liu, S., Su, C., Yao, J., Hao, Z., Su, H., Wu, Y., and Zhu, J. Preconditioning for physics-informed neural networks, 2024. Lu, L., Jin, P., Pang, G., Zhang, Z., and Karniadakis, G. E. Learning nonlinear operators via DeepONet based on the universal approximation theorem of operators. Nature Machine Intelligence , 3(3):218–229, 2021a. Lu, L., Meng, X., Mao, Z., and Karniadakis, G. E. Deep-XDE: A Deep Learning Library for Solving Differential Equations. SIAM Review , 63(1):208–228, 2021b. Lu, L., Pestourie, R., Yao, W., Wang, Z., Verdugo, F., and Johnson, S. G. Physics-informed neural networks with hard constraints for inverse design. SIAM Journal on Scientific Computing , 43(6):B1105–B1132, 2021c. Lu, L., Pestourie, R., Johnson, S. G., and Romano, G. Mul-tifidelity deep neural operators for efficient learning of partial differential equations with application to fast in-verse design of nanoscale heat transport. Physical Review Research , 4(2):023210, 2022. Mishra, S. and Molinaro, R. Estimates on the generalization error of physics-informed neural networks for approxi-mating pdes. IMA Journal of Numerical Analysis , 43(1): 1–43, 2023. 11 Challenges in Training PINNs 

Moseley, B., Markham, A., and Nissen-Meyer, T. Finite basis physics-informed neural networks (FBPINNs): a scalable domain decomposition approach for solving dif-ferential equations. Advances in Computational Mathe-matics , 49(4):62, 2023. M¨ uller, J. and Zeinhofer, M. Achieving High Accuracy with PINNs via Energy Natural Gradient Descent. In Proceed-ings of the 40th International Conference on Machine Learning , 2023. Nabian, M. A., Gladstone, R. J., and Meidani, H. Efficient training of physics-informed neural networks via impor-tance sampling. Comput.-Aided Civ. Infrastruct. Eng. , 36 (8):962–977, 2021. Nesterov, Y. Lectures on Convex Optimization . Springer Publishing Company, Incorporated, 2nd edition, 2018. Nocedal, J. and Wright, S. J. Numerical Optimization .Springer, 2nd edition, 2006. Paszke, A., Gross, S., Massa, F., Lerer, A., Bradbury, J., Chanan, G., Killeen, T., Lin, Z., Gimelshein, N., Antiga, L., Desmaison, A., K¨ opf, A., Yang, E. Z., DeVito, Z., Raison, M., Tejani, A., Chilamkurthy, S., Steiner, B., Fang, L., Bai, J., and Chintala, S. PyTorch: An Imperative Style, High-Performance Deep Learning Library. arXiv preprint arXiv:1912.01703 , 2019. Pearlmutter, B. A. Fast exact multiplication by the hessian. 

Neural computation , 6(1):147–160, 1994. Polyak, B. T. Gradient methods for minimizing function-als. Zhurnal vychislitel’noi matematiki i matematicheskoi fiziki , 3(4):643–653, 1963. Raissi, M., Perdikaris, P., and Karniadakis, G. Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations. Journal of Computational Physics , 378:686–707, 2019. Rohrhofer, F. M., Posch, S., G¨ oßnitzer, C., and Geiger, B. C. On the Role of Fixed Points of Dynamical Systems in Training Physics-Informed Neural Networks. Transac-tions on Machine Learning Research , 2023. Rudi, A., Carratino, L., and Rosasco, L. FALKON: An Optimal Large Scale Kernel Method. In Advances in Neural Information Processing Systems , 2017. Tropp, J. A. An introduction to matrix concentration inequal-ities. Foundations and Trends® in Machine Learning , 8 (1-2):1–230, 2015. Wang, H., Lu, L., Song, S., and Huang, G. Learning Special-ized Activation Functions for Physics-Informed Neural Networks. Communications in Computational Physics ,34(4):869–906, 2023. Wang, S., Teng, Y., and Perdikaris, P. Understanding and Mitigating Gradient Flow Pathologies in Physics-Informed Neural Networks. SIAM Journal on Scientific Computing , 43(5):A3055–A3081, 2021a. Wang, S., Wang, H., and Perdikaris, P. On the eigenvector bias of Fourier feature networks: From regression to solving multi-scale PDEs with physics-informed neural networks. Computer Methods in Applied Mechanics and Engineering , 384:113938, 2021b. Wang, S., Wang, H., and Perdikaris, P. Learning the solution operator of parametric partial differential equations with physics-informed DeepONets. Science Advances , 7(40): eabi8605, 2021c. Wang, S., Sankaran, S., and Perdikaris, P. Respecting causal-ity is all you need for training physics-informed neural networks. arXiv preprint arXiv:2203.07404 , 2022a. Wang, S., Yu, X., and Perdikaris, P. When and why PINNs fail to train: A neural tangent kernel perspective. Journal of Computational Physics , 449:110768, 2022b. Wu, C., Zhu, M., Tan, Q., Kartha, Y., and Lu, L. A compre-hensive study of non-adaptive and residual-based adaptive sampling for physics-informed neural networks. Com-puter Methods in Applied Mechanics and Engineering ,403:115671, 2023a. Wu, W., Daneker, M., Jolley, M. A., Turner, K. T., and Lu, L. Effective data sampling strategies and boundary condition constraints of physics-informed neural networks for iden-tifying material properties in solid mechanics. Applied mathematics and mechanics , 44(7):1039–1068, 2023b. Yao, J., Su, C., Hao, Z., Liu, S., Su, H., and Zhu, J. Mul-tiAdam: Parameter-wise Scale-invariant Optimizer for Multiscale Training of Physics-informed Neural Net-works. In Proceedings of the 40th International Con-ference on Machine Learning , 2023. Yao, Z., Gholami, A., Keutzer, K., and Mahoney, M. W. PyHessian: Neural Networks Through the Lens of the Hessian. In 2020 IEEE International Conference on Big Data (Big Data) , 2020. Yu, J., Lu, L., Meng, X., and Karniadakis, G. E. Gradient-enhanced physics-informed neural networks for forward and inverse PDE problems. Computer Methods in Applied Mechanics and Engineering , 393:114823, 2022. Zhang, C., Bengio, S., Hardt, M., Recht, B., and Vinyals, O. Understanding deep learning (still) requires rethinking generalization. Communications of the ACM , 64(3):107– 115, 2021. 12 Challenges in Training PINNs 

Zhang, Y., Chen, C., Shi, N., Sun, R., and Luo, Z.-Q. Adam Can Converge Without Any Modification On Update Rules. In Advances in Neural Information Processing Systems , 2022. 13 Challenges in Training PINNs 

A. Additional Details on Problem Setup 

Here we present the differential equations that we study in our experiments. 

A.1. Convection 

The one-dimensional convection problem is a hyperbolic PDE that can be used to model fluid flow, heat transfer, and biological processes. The convection PDE we study is 

∂u ∂t + β ∂u ∂x = 0 , x ∈ (0 , 2π), t ∈ (0 , 1) ,u(x, 0) = sin( x), x ∈ [0 , 2π],u(0 , t ) = u(2 π, t ), t ∈ [0 , 1] .

The analytical solution to this PDE is u(x, t ) = sin( x − βt ). We set β = 40 in our experiments. 

A.2. Reaction 

The one-dimensional reaction problem is a non-linear ODE which can be used to model chemical reactions. The reaction ODE we study is 

∂u ∂t − ρu (1 − u) = 0 , x ∈ (0 , 2π), t ∈ (0 , 1) 

u(x, 0) = exp 



− (x − π)2

2( π/ 4) 2



, x ∈ [0 , 2π],u(0 , t ) = u(2 π, t ), t ∈ [0 , 1] .

The analytical solution to this ODE is u(x, t ) = h(x)eρt  

> h(x)eρt +1 −h(x)

, where h(x) = exp 



− (x−π)2

> 2( π/ 4) 2



. We set ρ = 5 in our experiments. 

A.3. Wave 

The one-dimensional wave problem is a hyperbolic PDE that often arises in acoustics, electromagnetism, and fluid dynamics. The wave PDE we study is 

∂2u∂t 2 − 4 ∂2u∂x 2 = 0 , x ∈ (0 , 1) , t ∈ (0 , 1) ,u(x, 0) = sin( πx ) + 12 sin( βπx ), x ∈ [0 , 1] ,∂u (x, 0) 

∂t = 0 , x ∈ [0 , 1] ,u(0 , t ) = u(1 , t ) = 0 , t ∈ [0 , 1] .

The analytical solution to this PDE is u(x, t ) = sin( πx ) cos(2 πt ) + 12 sin( βπx ) cos(2 βπt ). We set β = 5 in our experi-ments. 

B. Why can Low Losses Correspond to Large L2RE? 

In Figure 2, there are several instances on the convection PDE and reaction ODE where the PINN loss is close to 0, but the L2RE of the PINN solution is close to 1. Rohrhofer et al. (2023) demonstrate that PINNs can be attracted to points in the loss landscape that minimize the residual portion of the PINN loss, 12nres 

Pnres 

> i=1

D[u(xir ; w), x ir ]2, to 0. However, these can correspond to trivial solutions: for the convection PDE, the residual portion is equal to 0 for any constant function u; for the reaction ODE, the residual portion is equal to 0 for constant u = 0 or u = 1 .14 Challenges in Training PINNs 0.0 0.2 0.4 0.6 0.8 1.0                                          

> t
> 0123456
> x
> Exact solution
> 0.00.20.40.60.81.0
> t
> 0123456
> x
> PINN solution
> 0246
> x
> −1.0
> −0.50.00.51.0
> u(x,  0)
> Initial condition
> 0.00.20.40.60.81.0
> t
> −1.0
> −0.50.00.51.0
> u(0 , t ) or  u(2 π, t )
> Boundary condition
> 0.00.20.40.60.81.0
> t
> 0123456
> x
> Exact solution
> 0.00.20.40.60.81.0
> t
> 0123456
> x
> PINN solution
> 0246
> x
> 0.00.20.40.60.81.0
> u(x,  0)
> Initial condition
> 0.00.20.40.60.81.0
> t
> 0.00 0.01 0.02 0.03 0.04
> u(0 , t ) or  u(2 π, t )
> Boundary condition
> −1.0
> −0.50.00.51.0
> −1.0
> −0.50.00.51.0
> 0.00.20.40.60.81.0
> 0.00.20.40.60.81.0
> Convection, β= 40 Reaction, ρ= 5
> Exact solution PINN solution PINN solution at x= 0 PINN solution at x= 2 π

Figure 6. The first two columns from the left display the exact solutions and PINN solutions. The PINN fails to learn the exact solution, which leads to large L2RE. Moreover, the PINN solutions are effectively constant over the domain. The third and fourth columns from the left display the PINN solutions at the initial time ( t = 0 ) and the boundaries ( x = 0 and x = 2 π). The PINN solutions learn the initial conditions, but they do not learn the boundary conditions. 

To show that the PINN is indeed learning a trivial solution, we visualize two solutions with small residual loss but large L2RE in Figure 6. The second column of Figure 6 shows the PINN solutions are close to 0 almost everywhere in the domain. Interestingly, the PINN solutions correctly learn the initial condition. However, the PINN solutions for the convection PDE and reaction ODE do not match the exact solution at the boundaries. One approach for alleviating this training issue would be to (adaptively) reweight the residual, initial condition, and boundary condition terms in the PINN loss (Wang et al., 2021a; 2022b). 

C. Computing the Spectral Density of the L-BFGS-preconditioned Hessian 

C.1. How L-BFGS Preconditions 

To minimize (2), L-BFGS uses the update 

wk+1 = wk − ηH k∇L(wk), (3) where Hk is a matrix approximating the inverse Hessian. We now show how (3) is equivalent to preconditioning the objective (2). Define the coordinate transformation w = H1/2

k z. By the chain rule, ∇L(z) = H1/2

k ∇L(w) and HL(z) = 

H1/2

k HL(w)H1/2

k . Thus, (3) is equivalent to 

zk+1 = zk − η∇L(zk), (4) 

wk+1 = H1/2

k zk+1 .

Equation (4) reveals how L-BFGS preconditions (2). L-BFGS first takes a step in the preconditioned z-space, where the conditioning is determined by HL(z), the preconditioned Hessian. Since Hk approximates H−1

L (w), H1/2

k HL(w)H1/2

k ≈

Ip, so the condition number of HL(z) is much smaller than that of HL(w). Consequently, L-BFGS can take a step that makes more progress than a method like gradient descent, which performs no preconditioning at all. In the second phase, L-BFGS maps the progress in the preconditioned space back to the original space. Thus, L-BFGS is able to make superior progress by transforming (2) to another space where the conditioning is more favorable, which enables it to compute an update that better reduces the loss in (2). 15 Challenges in Training PINNs 

C.2. Preconditioned Spectral Density Computation 

Here we discuss how to compute the spectral density of the Hessian after preconditioning by L-BFGS. This is the procedure we use to generate the figures in Section 5.3. L-BFGS stores a set of vector pairs given by the difference in consecutive iterates and gradients from most recent m

iterations (we use m = 100 in our experiments). To compute the update direction Hk∇fk, L-BFGS combines the stored vector pairs with a recursive scheme (Nocedal & Wright, 2006). Defining 

sk = xk+1 − xk, yk = ∇fk+1 − ∇ fk, ρk = 1

yTk sk

, γk = sTk−1yk−1

yTk−1yk−1

, Vk = I − ρkyksTk , H0 

> k

= γkI, 

the formula for Hk can be written as 

Hk = ( V Tk−1V Tk−m)H0 

> k

(Vk−mVk−1) + 

> m

X

> l=2

ρk−l(V Tk−1 · · · V Tk−l+1 )sk−lsTk−l(Vk−l+1 · · · Vk−1) + ρk−1sk−1sTk−1.

Expanding the terms, we have for j ∈ { 1, 2, . . . , i },

Vk−i · · · Vk−1 = I −

> i

X

> j=1

ρk−j yk−j ˜vTk−j where ˜vk−j = sk−j −

> j−1

X

> l=1

(ρk−lyTk−lsk−j )˜ vk−l.

It follows that 

Hk = ( I − ˜Y ˜V T )T γkI(I − ˜Y ˜V T ) + ˜S ˜ST = √γk(I − ˜Y ˜V T )T ˜S √γk(I − ˜Y ˜V T )˜ST .



= ˜Hk ˜HTk ,

where 

˜Y =



| |

ρk−1yk−1 · · · ρk−myk−m

| |

 ,

˜V =



| |

˜vk−1 · · · ˜vk−m

| |

 ,

˜S =



| |

˜sk−1 · · · ˜sk−m

| |

 , ˜sk−1 = √ρk−1sk−1, ˜sk−l = √ρk−l(V Tk−1 · · · V Tk−l+1 )sk−l for 2 ≤ l ≤ m. 

We now apply Algorithm 2 to unroll the above recurrence relations to compute columns of ˜Y , ˜S and ˜V .

Algorithm 2 Unrolling the L-BFGS Update 

input saved directions {yi}k−mi=k−1, saved steps {si}k−mi=k−1, saved inverse of inner products {ρi}k−mi=k−1

˜yk−1 = ρk−1yk−1

˜vk−1 = sk−1

˜sk−1 = √ρk−1sk−1

for i = k − 2, . . . , k − m do 

˜yi = ρiyi

Set α = 0 

for j = k − 1, . . . , i + 1 do 

α = α + (˜ yTj si)˜ vj

end for 

˜vi = si − α

˜si = √ρi(si − α)

end for output vectors {˜yi, ˜vi, ˜si}k−mi=k−1

16 Challenges in Training PINNs 0 10 0 10 1 10 2 10 3

> Eigenvalue 10 −10
> 10 −7
> 10 −4
> 10 −1
> 10 2
> Density

Residual    

> 010 010 110 2
> Eigenvalue 10 −10
> 10 −7
> 10 −4
> 10 −1
> 10 2
> Density

Initial Condition    

> 010 010 110 2
> Eigenvalue 10 −10
> 10 −7
> 10 −4
> 10 −1
> 10 2
> Density

Boundary Condition Reaction, ρ = 5        

> Hessian Preconditioned Hessian 010 010 110 210 310 410 5
> Eigenvalue 10 −10
> 10 −6
> 10 −2
> 10 2
> Density

Residual        

> −10 2−10 1−10 00 10 010 110 210 310 410 5
> Eigenvalue 10 −10
> 10 −7
> 10 −4
> 10 −1
> 10 2
> Density

Initial Condition     

> 010 010 110 210 3
> Eigenvalue 10 −10
> 10 −7
> 10 −4
> 10 −1
> 10 2
> Density

Boundary Condition Wave, β = 5  

> Hessian Preconditioned Hessian

Figure 7. Spectral density of the Hessian and the preconditioned Hessian of each loss component after 41000 iterations of Adam+L-BFGS for the reaction and wave problems. The plots show the loss landscape of each component is ill-conditioned, and the conditioning of each loss component is improved by L-BFGS. 

Since (non-zero) eigenvalues of ˜HTk HL(w) ˜Hk equal the eigenvalues of the preconditioned Hessian HkHL(w) =˜Hk ˜HTk HL(w) (Theorem 1.3.22 of Horn & Johnson (2012)), we can analyze the spectrum of ˜HTk HL(w) ˜Hk instead. This is advantageous since methods for calculating the spectral density of neural network Hessians are only compatible with symmetric matrices. Since ˜HTk HL(w) ˜Hk is symmetric, we can use stochastic Lanczos quadrature (SLQ) (Golub & Meurant, 2009; Lin et al., 2016) to compute spectral density of this matrix. SLQ only requires matrix-vector products with ˜Hk and Hessian-vector products, the latter of which may be efficiently computed via automatic differentiation; this is precisely what PyHessian does to compute spectral densities (Yao et al., 2020). 

Algorithm 3 Performing matrix-vector product 

input matrices ˜Y , ˜V , ˜S formed from resulting vectors from unrolling, vector v, and saved scaling factor for initializing diagonal matrix γk

Split vector v of length size( w) + m into v1 of size size( w) and v2 of size mv′ = √γk(v1 − ˜V ˜Y T v1) + ˜Sv 2

Perform Hessian-vector-product on v′, and obtain v′′ 

Stack √γk(v′′ − ˜Y ˜V T v′′ ) and ˜ST v′′ , and obtain v′′′ 

output resulting vector v′′′ 

By combining the matrix-vector product procedure described in Algorithm 3 with the Hessian-vector product operation, we are able to obtain spectral information of the preconditioned Hessian. 

D. Adam+L-BFGS Generally Gives the Best Performance 

Figure 8 shows that Adam+L-BFGS typically yields the best performance on both loss and L2RE across network widths. 17 Challenges in Training PINNs 50 100 200 400 Network Width 10 −5                               

> 10 −4
> 10 −3
> 10 −2
> Loss
> Convection, β= 40
> 50 100 200 400 Network Width 10 −5
> 10 −4
> 10 −3
> 10 −2
> 10 −1
> Loss
> Reaction, ρ= 5
> 50 100 200 400 Network Width 10 −3
> 10 −2
> 10 −1
> Loss
> Wave, β= 5
> 50 100 200 400 Network Width 10 −2
> 10 −1
> 10 0
> L2RE
> Convection, β= 40
> 50 100 200 400 Network Width 10 −1
> 10 0
> L2RE
> Reaction, ρ= 5
> 50 100 200 400 Network Width 10 −1
> L2RE
> Wave, β= 5
> Adam Adam + L-BFGS (1k) Adam + L-BFGS (11k) Adam + L-BFGS (31k) L-BFGS

Figure 8. Performance of Adam, L-BFGS, and Adam+L-BFGS after tuning. We find the learning rate η⋆ for each network width and optimization strategy that attains the lowest loss (L2RE) across all random seeds. The min, median, and max loss (L2RE) are calculated by taking the min, median, and max of the losses (L2REs) for learning rate η∗ across all random seeds. Each bar on the plot corresponds to the median, while the top and bottom error bars correspond to the max and min, respectively. The smallest min loss and L2RE are always attained by one of the Adam+L-BFGS strategies; the smallest median loss and L2RE are nearly always attained by one of the Adam+L-BFGS strategies. 

E. Additional details on Under-optimization 

E.1. Early Termination of L-BFGS 

Figure 9 explains why L-BFGS terminates early for the convection, reaction, and wave problems. We evaluate the loss at 

10 4 uniformly spaced points in the interval [0 , 1] . The orange stars in Figure 9 are step sizes that satisfy the strong Wolfe conditions and the red dots are step sizes that L-BFGS examines during the line search. 

E.2. NysNewton-CG (NNCG) 

Here we present the NNCG algorithm (Algorithm 4) introduced in Section 7.2 and its associated subroutines Randomized-Nystr¨ omApproximation (Algorithm 5), Nystr¨ omPCG (Algorithm 6), and Armijo (Algorithm 7). At each iteration, NNCG first checks whether the Nystr¨ om preconditioner (stored in U and ˆΛ) for the Nystr¨ omPCG method needs to be updated. If so, the preconditioner is recomputed using the RandomizedNystr¨ omApproximation subroutine. From here, the Newton step dk is computed using Nystr¨ omPCG; we warm start the PCG algorithm using the Newton step dk−1 from the previous iteration. After computing the Newton step, we compute the step size ηk using Armijo line search — this guarantees that the loss will decrease when we update the parameters. Finally, we update the parameters using ηk and dk.In our experiments, we set η = 1 , K = 2000 , s = 60 , F = 20 , ϵ = 10 −16 , M = 1000 , α = 0 .1, and β = 0 .5. We tune 

μ ∈ [10 −5, 10 −4, 10 −3, 10 −2, 10 −1]; we find that μ = 10 −2, 10 −1 work best in practice. Figures 1 and 4 show the NNCG run that attains the lowest loss after tuning μ.18 Challenges in Training PINNs 0.00 0.25 0.50 0.75 1.00 Stepsize 5.949 × 10 −6                                             

> 5.95 ×10 −6
> 5.951 ×10 −6
> 5.952 ×10 −6
> 5.953 ×10 −6
> 5.954 ×10 −6
> 5.955 ×10 −6
> Loss
> Convection, β= 40
> 0.00 0.25 0.50 0.75 1.00 Stepsize 6.5188 ×10 −6
> 6.519 ×10 −6
> 6.5192 ×10 −6
> 6.5194 ×10 −6
> Loss
> Reaction, ρ= 5
> 0.00 0.25 0.50 0.75 1.00 Stepsize 1.55784 ×10 −3
> 1.55786 ×10 −3
> 1.55788 ×10 −3
> 1.5579 ×10 −3
> 1.55792 ×10 −3
> Loss
> Wave, β= 5
> Satisfactory stepsize Assessed stepsize

Figure 9. Loss evaluated along the L-BFGS search direction at different stepsizes after 41000 iterations of Adam+L-BFGS. For convection and wave, the line search does not find a stepsize that satisfies the strong Wolfe conditions, even though there are plenty of such points. For reaction, the slope of the objective used in the line search procedure at the current iterate is less than a pre-defined threshold 10 −9, so L-BFGS terminates without performing any line-search. 

Algorithm 4 NysNewton-CG (NNCG) 

input Initialization w0, max. learning rate η, number of iterations K, preconditioner sketch size s, preconditioner update frequency F , damping parameter μ, CG tolerance ϵ, CG max. iterations M , backtracking parameters α, β d−1 = 0 

for k = 0 , . . . , K − 1 do if k is a multiple of F then 

[U, ˆΛ] = RandomizedNystr¨ omApproximation (HL(wk), s ) ▷ Update Nystr¨ om preconditioner every F iterations 

end if 

dk = Nystr¨ omPCG (HL(wk), ∇L(wk), d k−1, U, ˆΛ, s, μ, ϵ, M ) ▷ Damped Newton step (HL(wk) + μI )−1∇L(wk)

ηk = Armijo (L, w k, ∇L(wk), −dk, η ) ▷ Compute step size via line search 

wk+1 = wk − ηkdk ▷ Update parameters 

end for 

The RandomizedNystr¨ omApproximation subroutine (Algorithm 5) is used in NNCG to compute the preconditioner for Nystr¨ omPCG. The algorithm returns the top-s approximate eigenvectors and eigenvalues of the input matrix M . Within NNCG, the sketch computation Y = M Q is implemented using Hessian-vector products. The portion in red is a fail-safe that allows for the preconditioner to be computed when H is an indefinite matrix. For further details, please see Frangella et al. (2023). 19 Challenges in Training PINNs 

Algorithm 5 RandomizedNystr¨ omApproximation 

input Symmetric matrix M , sketch size sS = randn (p, s ) ▷ Generate test matrix 

Q = qr econ (S)

Y = M Q ▷ Compute sketch 

ν = √peps (norm (Y, 2)) ▷ Compute shift 

Yν = Y + νQ ▷ Add shift for stability 

λ = 0 ▷ Additional shift may be required for positive definiteness 

C = chol (QT Yν ) ▷ Cholesky decomposition: CT C = QT Yν

if chol fails then 

Compute [W, Γ] = eig( QT Yν ) ▷ Q T Yν is small and square Set λ = λmin (QT Yν )

R = W (Γ + |λ|I)−1/2W T

B = Y R ▷ R is psd 

else 

B = Y C −1 ▷ Triangular solve 

end if 

[ ˆV , Σ, ∼] = svd (B, 0) ▷ Thin SVD 

ˆΛ = max {0, Σ2 − (ν + |λ|I)} ▷ Compute eigs, and remove shift with element-wise max 

Return: ˆV , ˆΛ

The Nystr¨ omPCG subroutine (Algorithm 6) is used in NNCG to compute the damped Newton step. The preconditioner P

and its inverse P −1 are given by 

P = 1ˆλs + μ U (ˆΛ + μI )U T + ( I − U U T )

P −1 = ( ˆλs + μ)U (ˆΛ + μI )−1U T + ( I − U U T ).

Within NNCG, the matrix-vector product involving the Hessian (i.e., A = HL(wk)) is implemented using Hessian-vector products. For further details, please see Frangella et al. (2023). 

Algorithm 6 Nystr¨ omPCG 

input Psd matrix A, right-hand side b, initial guess x0, approx. eigenvectors U , approx. eigenvalues ˆΛ, sketch size s,damping parameter μ, CG tolerance ϵ, CG max. iterations Mr0 = b − (A + μI )x0

z0 = P −1r0

p0 = z0

k = 0 ▷ Iteration counter 

while ∥r0∥2 ≥ ε and k < M do 

v = ( A + μI )p0

α = ( rT 

> 0

z0)/(pT 

> 0

v0) ▷ Compute step size 

x = x0 + αp 0 ▷ Update solution 

r = r0 − αv ▷ Update residual 

z = P −1rβ = ( rT z)/(rT 

> 0

z0)

x0 ← x, r 0 ← r, p 0 ← z + βp 0, z 0 ← z, k ← k + 1 

end while Return: x

The Armijo subroutine (Algorithm 7) is used in NNCG to guarantee that the loss decreases at every iteration. The function oracle is implemented in PyTorch using a closure . At each iteration, the subroutine checks whether the sufficient decrease condition has been met; if not, it shrinks the step size by a factor of β. For further details, please see Nocedal & Wright (2006). 20 Challenges in Training PINNs  

> Table 3. Per-iteration times (in seconds) of L-BFGS and NNCG on each PDE.

Optimizer Convection Reaction Wave L-BFGS 4.6e-2 3.6e-2 9.0e-2 NNCG 2.5e-1 7.2e-1 2.9e1 Time Ratio 5.43 20 322.22 

Algorithm 7 Armijo 

input Function oracle f , current iterate x, current gradient ∇f (x), search direction d, initial step size t, backtracking parameters α, β 

while f (x + td ) > f (x) + αt (∇f (x)T d) do 

t ← βt ▷ Shrink step size 

end while Return: t

E.3. Wall-clock Times for L-BFGS and NNCG 

Table 3 summarizes the per-iteration wall-clock times of L-BFGS and NNCG on each PDE. The large gap on wave (compared to reaction and convection) is because NNCG has to compute hessian-vector products involving second derivatives, while this is not the case for the two other PDEs. 

F. Ill-conditioned Differential Operators Lead to Difficult Optimization Problems 

In this section, we state and prove the formal version of Theorem 8.4. The overall structure of the proof is based on showing the conditioning of the Gauss-Newton matrix of the population PINN loss is controlled by the conditioning of the differential operator. We then show the empirical Gauss-Newton matrix is close to its population counterpart by using matrix concentration techniques. Finally, as the conditioning of HL at a minimizer is controlled by the empirical Gauss-Newton matrix, we obtain the desired result. 

F.1. Preliminaries 

Similar to De Ryck et al. (2023), we consider a general linear PDE with Dirichlet boundary conditions: 

D[u]( x) = f (x), x ∈ Ω,u(x) = g(x), x ∈ ∂Ω,

where u : Rd 7 → R, f : Rd 7 → R and Ω is a bounded subset of Rd. The “population” PINN objective for this PDE is 

L∞(w) = 12

Z

> Ω

(D[u(x; w)] − f (x)) 2 dμ (x) + λ

2

Z

> ∂Ω

(u(x; w) − g(x)) 2 dσ (x).λ can be any positive real number; we set λ = 1 in our experiments. Here μ and σ are probability measures on Ω and ∂Ω

respectively, from which the data is sampled. The empirical PINN objective is given by 

L(w) = 12nres 

> nres

X

> i=1

D[u(xir ; w)] − f (xi)2 + λ

2nbc 

> nbc

X

> j=1



u(xjb; w) − g(xj )

2

.

Moreover, throughout this section we use the notation ⟨f, g ⟩L2(Ω) to denote the standard L2-inner product on Ω:

⟨f, g ⟩L2(Ω) =

Z

> Ω

f gdμ (x).

21 Challenges in Training PINNs 

Lemma F.1. The Hessian of the L∞(w) is given by 

HL∞ (w) = 

Z

> Ω

D[∇wu(x; w)] D[∇wu(x; w)] T dμ (x) + 

Z

> Ω

D[∇2

> w

u(x; w)] ( D[∇wu(x; w)] − f (x)) dμ (x)+ λ

Z

> ∂Ω

∇wu(x; w)∇wu(x; w)T dσ (x) + λ

Z

> ∂Ω

∇2

> w

u(x; w) ( u(x; w) − g(x)) dσ (x).

The Hessian of L(w) is given by 

HL(w) = 1

nres 

> nres

X

> i=1

D[∇wu(xir ; w)] D[∇wu(xir ; w)] T + 1

nres 

> nres

X

> i=1

D[∇2

> w

u(xri ; w)] D[∇wu(xir ; w)] − f (xir ) (5) 

+ λnbc 

> nbc

X

> j=1

∇wu(xjb; w)∇wu(xjb; w)T + λnbc 

> nbc

X

> j=1

∇2

> w

u(xjb; w)



u(xjb; w) − g(xj )



.

In particular, for w⋆ ∈ W ⋆

HL(w⋆) = Gr (w) + Gb(w).

Here 

Gr (w) := 1

nres 

> nres

X

> i=1

D[∇wu(xi; w⋆)] D[∇wu(xi; w⋆)] T , Gb(w) = λnbc 

> nbc

X

> j=1

∇wu(xjb; w⋆)∇wu(xjb; w⋆)T .

Define the maps Fres (w) = 



D[u(x1 

> r

; w)] 

...

D[u(xnres  

> r

; w)] 

, and Fbc (w) = 



u(x1 

> b

; w)

...

u(xnbc  

> b

; w)] 

. We have the following important lemma, which follows via routine calculation. 

Lemma F.2. Let n = nres + nbc . Define the map F : Rp → Rn, by stacking Fres (w), Fbc (w). Then, the Jacobian of F is given by 

JF (w) = 

JFres (w)

JFbc (w).



Moreover, the tangent kernel KF (w) = JF (w)JF (w)T is given by 

KF (w) = 

JFres (w)JFres (w)T JFres (w)JFbc (w)T

JFbc (w)JFres (w)T JFbc (w)JFbc (w)T



=

 KFres (w) JFres (w)JFbc (w)T

JFbc (w)JFres (w)T KFbc (w)



.

F.2. Relating G∞(w) to D

Isolate the population Gauss-Newton matrix for the residual: 

G∞(w) = 

Z

> Ω

D[∇wu(x; w)] D[∇wu(x; w)] T dμ (x).

Analogous to De Ryck et al. (2023) we define the functions ϕi(x; w) = ∂wi u(x; w) for i ∈ { 1 . . . , p }. From this and the definition of G∞(w), it follows that (G∞(w)) ij = ⟨D [ϕi], D[ϕj ]⟩L2(Ω) .Similar to De Ryck et al. (2023) we can associate each w ∈ Rp with a space of functions H(w) =

span (ϕ1(x; w), . . . , ϕ p(x; w)) ⊂ L2(Ω) . We also define two linear maps associated with H(w):

T (w)v =

> p

X

> i=1

viϕi(x; w),T ∗(w)f = ⟨f, ϕ 1⟩L2(Ω) , . . . , ⟨f, ϕ p⟩L2(Ω) 

 .

From these definitions, we establish the following lemma. 22 Challenges in Training PINNs 

Lemma F.3 (Characterizing G∞(w)). Define A = D∗D. Then the matrix G∞(w) satisfies 

G∞(w) = T ∗(w)AT (w).

Proof. Let ei and ej denote the ith and jth standard basis vectors in Rp. Then, 

(G∞(w)) ij = ⟨D [ϕi]( w), D[ϕj ]( w)⟩L2(Ω) = ⟨ϕi(w), D∗D[ϕj (w)] ⟩L2(Ω) = ⟨T e i, D∗D[T e j ]⟩L2(Ω) 

= ⟨ei, (T ∗D∗DT )[ ej ]⟩L2(Ω) ,

where the second equality follows from the definition of the adjoint. Hence, using A = D∗D, we conclude G∞(w) = 

T ∗(w)AT (w).Define the kernel integral operator K∞(w) : L2(Ω) → H by 

K∞(w)[ f ]( x) = T (w)T ∗(w)f =

> p

X

> i=1

⟨f, ϕ i(x; w)⟩ϕi(x; w), (6) and the kernel matrix A(w) with entries Aij (w) = ⟨ϕi(x; w), ϕ j (x; w)⟩L2(Ω) .Using Lemma F.3 and applying the same logic as in the proof of Theorem 2.4 in De Ryck et al. (2023), we obtain the following theorem. 

Theorem F.4. Suppose that the matrix A(w) is invertible. Then the eigenvalues of G∞(w) satisfy 

λj (G∞(w)) = λj (A ◦ K ∞(w)) , for all j ∈ [p].

F.3. Gr (w) Concentrates Around G∞(w)

In order to relate the conditioning of the population objective to the empirical objective, we must relate the population Gauss-Newton residual matrix to its empirical counterpart. We accomplish this by showing Gr (w) concentrates around 

G∞(w). To this end, we recall the following variant of the intrinsic dimension matrix Bernstein inequality from Tropp (2015). 

Theorem F.5 (Intrinsic Dimension Matrix Bernstein) . Let {Xi}i∈[n] be a sequence of independent mean zero random matrices of the same size. Suppose that the following conditions hold: 

∥Xi∥ ≤ B, 

> n

X

> i=1

E[XiXTi ] ⪯ V1,

> n

X

> i=1

E[XTi Xi] ⪯ V2.

Define 

V =

V1 00 V2



, ς 2 = max {∥ V1∥, ∥V2∥} ,

and the intrinsic dimension dint = trace (V) 

> ∥V∥

.Then for all t ≥ ς + B 

> 3

,

P

> n

X

> i=1

Xi ≥ t

!

≤ 4dint exp 



− 38 min 

 t2

ς2 , tB

 

.

Next, we recall two key concepts from the kernel ridge regression literature and approximation via sampling literature: 

γ-effective dimension and γ-ridge leverage coherence (Bach, 2013; Cohen et al., 2017; Rudi et al., 2017). 

Definition F.6 (γ-Effective dimension and γ-ridge leverage coherence) . Let γ > 0. Then the γ-effective dimension of 

G∞(w) is given by 

dγ

> eff

(G∞(w)) = trace G∞(w)( G∞(w) + γI )−1 .

The γ-ridge leverage coherence is given by 

χγ (G∞(w)) = sup 

> x∈Ω

(G∞(w) + γI )−1/2D[∇wu(x; w)] 2

Ex∼μ (G∞(w) + γI )−1/2D[∇wu(x; w)] 2 = sup x∈Ω (G∞(w) + γI )−1/2D[∇wu(x; w)] 2

dγ

> eff

(G∞(w)) .

23 Challenges in Training PINNs 

Observe that dγ

> eff

(G∞(w)) only depends upon γ and w, while χγ (G∞(w)) only depends upon γ, w, and Ω. Moreover, 

χγ (G∞(w)) < ∞ as Ω is bounded. We prove the following lemma using the γ-effective dimension and γ-ridge leverage coherence in conjunction with Theorem F.5. 

Lemma F.7 (Finite-sample approximation) . Let 0 < γ < λ1(G∞(w)) . If nres ≥

40 χγ (G∞(w)) dγ

> eff

(G∞(w)) log 

 8dγ

> eff (G∞(w))
> δ



, then with probability at least 1 − δ

12 [G∞(w) − γI ] ⪯ Gr (w) ⪯ 12 [3 G∞(w) + γI. ]

Proof. Let xi = ( G∞(w)+ γI )−1/2D[∇wu(xi; w)] , and Xi = 1

> nres

xixTi − Dγ

, where Dγ = G∞(w) ( G∞(w) + γI )−1.Clearly, E[Xi] = 0 . Moreover, the Xi’s are bounded as 

∥Xi∥ = max 

 λmax (Xi)

nres 

, − λmin (Xi)

nres 



≤ max 

 ∥xi∥2

nres 

, λmax (−Xi)

nres 



≤ max 

 χγ (G∞(w)) dγ

> eff

(G∞(w)) 

nres 

, 1

nres 



= χγ (G∞(w)) dγ

> eff

(G∞(w)) 

nres 

.

Thus, it remains to verify the variance condition. We have 

> nres

X

> i=1

E[XiXTi ] = nres E[X21 ] = nres × 1

n2

> res

E[( x1xT 

> 1

− Dγ )2] ⪯ 1

nres 

E[∥x1∥2x1xT 

> 1

]

⪯ χγ (G∞(w)) dγ

> eff

(G∞(w)) 

nres 

Dγ .

Hence, the conditions of Theorem F.5 hold with B = χγ (G∞(w)) dγ 

> eff (G∞(w))
> nres

and V1 = V2 = χγ (G∞(w)) dγ 

> eff (G∞(w))
> nres

Dγ .Now 1/2 ≤ ∥V∥ ≤ 1 as nres ≥ χγ (G∞(w)) dγ

> eff

(G∞(w)) and γ ≤ λ1 (G∞(w)) . Moreover, as V1 = V2 we have 

dint ≤ 4dγ

> eff

(G∞(w)) . So, setting 

t =

vuut 8χγ (G∞(w)) dγ

> eff

(G∞(w)) log 

 8dγ

> eff (G∞(w))
> δ



3nres 

+8χγ (G∞(w)) dγ

> eff

(G∞(w)) log 

 8dγ

> eff (G∞(w))
> δ



3nres 

and using nres ≥ 40 χγ (G∞(w)) dγ

> eff

(G∞(w)) log 

 8dγ

> eff (G∞(w))
> δ



, we conclude 

P

> nres

X

> i=1

Xi ≥ 12

!

≤ δ. 

Now, ∥Pnres  

> i=1

Xi∥ ≤ 12 implies 

− 12 [G∞(w) + γI ] ⪯ Gr (w) − G∞(w) ⪯ 12 [G∞(w) + γI ] .

The claim now follows by rearrangement. By combining Theorem F.4 and Lemma F.7, we show that if the spectrum of A ◦ K ∞(w) decays, then the spectrum of the empirical Gauss-Newton matrix also decays with high probability. 

Proposition F.8 (Spectrum of empirical Gauss-Newton matrix decays fast) . Suppose the eigenvalues of A ◦ K ∞(w)

satisfy λj (A ◦ K ∞(w)) ≤ Cj −2α, where α > 1/2 and C > 0 is some absolute constant. Then if √nres ≥

40 C1χγ (G∞(w)) log  1

> δ

, for some absolute constant C1, it holds that 

λnres (Gr (w)) ≤ n−α

> res

with probability at least 1 − δ.

24 Challenges in Training PINNs 

Proof. The hypotheses on the decay of the eigenvalues implies dγ

> eff

(G∞(w)) ≤ C1γ− 12α (see Appendix C of Bach (2013)). Consequently, given γ = n−α 

> res

, we have dγ

> eff

(G∞(w)) ≤ C1n 12

> res

. Combining this with our hypotheses on nres , it follows 

nres ≥ 40 C1χγ (G∞(w)) dγ

> eff

(G∞(w)) log 

 8dγ

> eff (G∞(w))
> δ



. Hence Lemma F.7 implies with probability at least 1 − δ that 

Gr (w) ⪯ 12 (3 G∞(w) + γI ) ,

which yields for any 1 ≤ r ≤ nλnres (Gr (w)) ≤ 12 (3 λr (G∞(w)) + γ) .

Combining the last display with nres ≥ 3dγ

> eff

(G∞(w)) , Lemma 5.4 of Frangella et al. (2023) guarantees λr (G∞(w)) ≤ γ/ 3,and so 

λnres (Gr (w)) ≤ 12 (3 λr (G∞(w)) + γ) ≤ γ ≤ n−α 

> res

.

F.4. Formal Statement of Theorem 8.4 and Proof Theorem F.9 (An ill-conditioned differential operator leads to hard optimization) . Fix w⋆ ∈ W ⋆, and let S be a set containing w⋆ for which S is μ-PŁ ⋆. Let α > 1/2. If the eigenvalues of A ◦ K ∞(w⋆) satisfy λj (A ◦ K ∞(w⋆)) ≤ Cj −2α

and √nres ≥ 40 C1χγ (G∞(w⋆)) log  1

> δ

, then 

κL(S) ≥ C2nα

> res

,

with probability at least 1 − δ. Here C, C 1, and C2 are absolute constants. Proof. By the assumption on nres , the conditions of Proposition F.8 are met, so, 

λnres (Gr (w⋆)) ≤ n−α 

> res

.

with probability at least 1 − δ. By definition Gr (w⋆) = JFres (w⋆)T JFres (w⋆), consequently, 

λnres (KFres (w⋆)) = λnres (Gr (w⋆)) ≤ n−α 

> res

.

Now, the PŁ ⋆-constant for S, satisfies μ = inf w∈S λn(KF (w)) (Liu et al., 2022). Combining this with the expression for 

KF (w⋆) in Lemma F.2, we reach 

μ ≤ λn(KF (w⋆)) ≤ λnres (KFres (w⋆)) ≤ n−α 

> res

,

where the second inequality follows from Cauchy’s Interlacing theorem. Recalling that κL(S) = sup w∈S ∥HL(w)∥ 

> μ

, and 

HL(w⋆) is symmetric psd, we reach 

κL(S) ≥ λ1(HL(w⋆)) 

μ

> (1)

≥ λ1(Gr (w⋆)) + λp(Gb(w⋆)) 

μ

> (2)

= λ1(Gr (w⋆)) 

μ

> (3)

≥ C3λ1(G∞(w⋆)) nα

> res

.

Here (1) uses HL(w⋆) = Gr (w⋆) + Gb(w⋆) and Weyl’s inequalities, (2) uses p ≥ nres + nbc , so that λp(Gb(w⋆)) = 0 .Inequality (3) uses the upper bound on μ and the lower bound on Gr (w) given in Lemma F.7. Hence, the claim follows with C2 = C3λ1(G∞(w⋆)) .

F.5. κ Grows with the Number of Residual Points 

Figure 10 plots the ratio λ1(HL)/λ 129 (HL) near a minimizer w⋆. This ratio is a lower bound for the condition number of 

HL, and is computationally tractable to compute. We see that the estimate of the κ grows polynomially with nres , which provides empirical verification for Theorem 8.4. 

G. Convergence of GDND (Algorithm 1) 

In this section, we provide the formal version of Theorem 8.5 and its proof. However, this is delayed till Appendix G.4, as the theorem is a consequence of a series of results. Before jumping to the theorem, we recommend reading the statements in the preceding subsections to understand the statement and corresponding proof. 25 Challenges in Training PINNs 8 9 10 11 12 13 log 2 nres   

> 10 4
> λ1/λ 129
> Convection, β= 1

Figure 10. Estimated condition number after 41000 iterations of Adam+L-BFGS with different number of residual points from 255 × 100 

grid on the interior. Here λi denotes the ith largest eigenvalue of the Hessian. The model has 2 layers and the hidden layer has width 32 .The plot shows κL grows polynomially in the number of residual points. 

G.1. Overview and Notation 

Recall, we are interested in minimizing the objective in (2): 

L(w) = 12nres 

> nres

X

> i=1

D[u(xir ; w)] 2 + 12nbc 

> nbc

X

> j=1



B[u(xjb; w)] 

2

,

where D is the differential operator defining the PDE and B is the operator defining the boundary conditions. Define 

F(w) = 

 

> 1√nres

D[u(x1 

> r

; w)] 

... 

> 1√nres

D[u(xnres  

> r

; w)]  

> 1√nbc

B[u(x1 

> b

; w)] 

... 

> 1√nbc

B[u(xnbc  

> b

; w)] 



, y = 0 

Using the preceding definitions, our objective may be rewritten as: 

L(w) = 12 ∥F (w) − y∥2.

Throughout the appendix, we work with the condensed expression for the loss given above. We denote the (nres + nbc ) × p

Jacobian matrix of F by JF (w). The tangent kernel at w is given by the n × n matrix KF (w) = JF (w)JF (w)T . The closely related Gauss-Newton matrix is given by G(w) = JF (w)T JF (w).

G.2. Global Behavior: Reaching a Small Ball About a Minimizer 

We begin by showing that under appropriate conditions, gradient descent outputs a point close to a minimizer after a fixed number of iterations. We first start with the following assumption which is common in the neural network literature (Liu et al., 2022; 2023). 

Assumption G.1. The mapping F(w) is LF -Lipschitz, and the loss L(w) is βL-smooth. Under Assumption G.1 and a PŁ ⋆-condition, we have the following theorem of Liu et al. (2022), which shows gradient descent converges linearly. 

Theorem G.2. Let w0 denote the network weights at initialization. Suppose Assumption G.1 holds, and that L(w) is μ-PŁ ⋆

in B(w0, 2R) with R = 2√2βLL(w0) 

> μ

. Then the following statements hold: 1. The intersection B(w0, R ) ∩ W ⋆ is non-empty. 

26 Challenges in Training PINNs 

2. Gradient descent with step size η = 1 /β L satisfies: 

wk+1 = wk − η∇L(wk) ∈ B(w0, R ) for all k ≥ 0,L(wk) ≤



1 − μβL

k

L(w0).

For wide neural neural networks, it is known that the μ-PŁ ⋆condition in Theorem G.2 hold with high probability, see Liu et al. (2022) for details. We also recall the following lemma from Liu et al. (2023). 

Lemma G.3 (Descent Principle) . Let L : Rp 7 → [0 , ∞) be differentiable and μ-PŁ ⋆in the ball B(w, r ). Suppose 

L(w) < 12 μr 2. Then the intersection B(w, r ) ∩ W ⋆ is non-empty, and 

μ

2 dist 2(w, W⋆) ≤ L(w).

Let LHL be the Hessian Lipschitz constant in B(w0, 2R), and LJF = sup w∈B(w0,2R) ∥HF (w)∥, where ∥HF (w)∥ =max i∈[n] ∥HFi (w)∥. Define M = max {L HL , LJF , LF LJF , 1}, εloc = εμ 3/2 

> 4M

, where ε ∈ (0 , 1) . By combining Theo-rem G.2 and Lemma G.3, we are able to establish the following important corollary, which shows gradient descent outputs a point close to a minimizer. 

Corollary G.4 (Getting close to a minimizer) . Set ρ = min 

( 

> εloc
> 19
> qβLμ

, √μR, R 

)

. Run gradient descent for k = 

> βL
> μ

log 

 4 max {2βL,1}L(w0)

> μρ 2



iterations, gradient descent outputs a point wloc satisfying 

L(wloc ) ≤ μρ 2

4 min 



1, 12βL



,

∥wloc − w⋆∥HL(w⋆)+ μI ≤ ρ, for some w⋆ ∈ W ⋆.

Proof. The first claim about L(wloc ) is an immediate consequence of Theorem G.2. For the second claim, consider the ball B(wloc , ρ ). Observe that B(wloc , ρ ) ⊂ B(w0, 2R), so L is μ-PŁ ⋆ in B(wloc , ρ ). Combining this with L(wloc ) ≤ μρ 2 

> 4

,Lemma G.3 guarantees the existence of w⋆ ∈ B(wloc , ρ ) ∩ W ⋆, with ∥wloc − w⋆∥ ≤ 

q 2 

> μ

L(wloc ). Hence Cauchy-Schwarz yields 

∥wloc − w⋆∥HL(w⋆)+ μI ≤ pβL + μ∥wloc − w⋆∥ ≤ p2βL∥wloc − w⋆∥≤ 2

s

βL

μ L(wloc ) ≤ 2 ×

s

βL

μμρ 2

8βL

≤ ρ, 

which proves the claim. 

G.3. Fast Local Convergence of Damped Newton’s Method 

In this section, we show damped Newton’s method with fixed stepsize exhibits fast linear convergence in an appropriate region about the minimizer w⋆ from Corollary G.4. Fix ε ∈ (0 , 1) , then the region of local convergence is given by: 

Nεloc (w⋆) = w ∈ Rp : ∥w − w⋆∥HL(w⋆)+ μI ≤ εloc ,

where εloc = εμ 3/2 

> 4M

as above. Note that wloc ∈ N εloc (w⋆).We now prove several lemmas, that are essential to the argument. We begin with the following elementary technical result, which shall be used repeatedly below. 27 Challenges in Training PINNs 

Lemma G.5 (Sandwich lemma) . Let A be a symmetric matrix and B be a symmetric positive-definite matrix. Suppose that 

A and B satisfy ∥A − B∥ ≤ ελ min (B) where ε ∈ (0 , 1) . Then 

(1 − ε)B ⪯ A ⪯ (1 + ε)B. 

Proof. By hypothesis, it holds that 

−ελ min (B)I ⪯ A − B ⪯ ελ min (B)I. 

So using B ⪰ λmin (B)I, and adding B to both sides, we reach 

(1 − ε)B ⪯ A ⪯ (1 + ε)B. 

The next result describes the behavior of the damped Hessian in Nεloc (w⋆).

Lemma G.6 (Damped Hessian in Nεloc (w⋆)). Suppose that γ ≥ μ and ε ∈ (0 , 1) .1. (Positive-definiteness of damped Hessian in Nεloc (w⋆)) For any w ∈ N εloc (w⋆),

HL(w) + γI ⪰



1 − ε

4



γI. 

2. (Damped Hessians stay close in Nεloc (w⋆)) For any w, w ′ ∈ N εloc (w⋆),

(1 − ε) [ HL(w) + γI ] ⪯ HL(w′) + γI ⪯ (1 + ε) [ HL(w) + γI ] .

Proof. We begin by observing that the damped Hessian at w⋆ satisfies 

HL(w⋆) + γI = G(w⋆) + γI + 1

n

> n

X

> i=1

[F(w⋆) − y]i HFi (w⋆)= G(w⋆) + γI ⪰ γI. 

Thus, HL(w⋆) + γI is positive definite. Now, for any w ∈ N εloc (w⋆), it follows from Lipschitzness of HL that 

∥(HL(w) + γI ) − (HL(w⋆) + γI )∥ ≤ L HL ∥w − w⋆∥ ≤ LHL

√γ ∥w − w⋆∥HL(w⋆)+ γI ≤ εμ 

4 .

As λmin (HL(w⋆) + γI ) ≥ γ > μ , we may invoke Lemma G.5 to reach 



1 − ε

4



[HL(w⋆) + γI ] ⪯ HL(w) + γI ⪯



1 + ε

4



[HL(w⋆) + γI ] .

This immediately yields 

λmin (HL(w) + γI ) ≥



1 − ε

4



γ ≥ 34 γ, 

which proves item 1. To see the second claim, observe for any w, w ′ ∈ N εloc (w⋆) the triangle inequality implies 

∥(HL(w′) + γI ) − (HL(w) + γI )∥ ≤ εμ 

2 ≤ 23 ε

 34 γ



.

As λmin (HL(w) + γI ) ≥ 34 γ, it follows from Lemma G.5 that 



1 − 23 ε



[HL(w) + γI ] ⪯ HL(w′) + γI ⪯



1 + 23 ε



[HL(w) + γI ] ,

which establishes item 2. 28 Challenges in Training PINNs 

The next result characterizes the behavior of the tangent kernel and Gauss-Newton matrix in Nεloc (w⋆).

Lemma G.7 (Tangent kernel and Gauss-Newton matrix in Nεloc (w⋆)). Let γ ≥ μ. Then for any w, w ′ ∈ N εloc (w⋆), the following statements hold: 1. (Tangent kernels stay close) 

1 − ε

2



KF (w⋆) ⪯ KF (w) ⪯



1 + ε

2



KF (w⋆)

2. (Gauss-Newton matrices stay close) 



1 − ε

2



[G(w) + γI ] ⪯ G(w⋆) + γI ⪯



1 + ε

2



[G(w) + γI ]

3. (Damped Hessian is close to damped Gauss-Newton matrix) 

(1 − ε) [ G(w) + γI ] ⪯ HL(w) + γI ⪯ (1 + ε) [ G(w) + γI ] .

4. (Jacobian has full row-rank) The Jacobian satisfies rank (JF (w)) = n.Proof. 1. Observe that 

∥KF (w) − KF (w⋆)∥ = ∥JF (w)JF (w)T − JF (w⋆)JF (w⋆)T ∥

= [JF (w) − JF (w⋆)] JF (w)T + JF (w⋆) [ JF (w) − JF (w⋆)] T

≤ 2LF LJF ∥w − w⋆∥ ≤ 2LF LJF

√γ ∥w − w⋆∥HL(w⋆)+ γI ≤ εμ 3/2

√γ ≤ ε

2 μ, 

where in the first inequality we applied the fundamental theorem of calculus to reach 

∥JF (w) − JF (w⋆)∥ ≤ L JF ∥w − w⋆∥.

Hence the claim follows from Lemma G.5. 2. By an analogous argument to item 1, we find 

∥(G(w) + γI ) − (G(w⋆) + γI )∥ ≤ ε

2 μ, 

so the result again follows from Lemma G.5. 3. First observe HL(w⋆) + γI = G(w⋆) + γI . Hence the proof of Lemma G.6 implies, 



1 − ε

4



[G(w⋆) + γI ] ⪯ HL(w) + γI ⪯



1 + ε

4



[G(w⋆) + γI ] .

Hence the claim now follows from combining the last display with item 2. 4. This last claim follows immediately from item 1, as for any w ∈ N εloc (w⋆),

σn (JF (w)) = pλmin (KF (w)) ≥

r

1 − ε

2



μ > 0.

Here the last inequality uses λmin (KF (w⋆)) ≥ μ, which follows as w⋆ ∈ B(w0, 2R).The next lemma is essential to proving convergence. It shows in Nεloc (w⋆) that L(w) is uniformly smooth with respect to the damped Hessian, with nice smoothness constant (1 + ε). Moreover, it establishes that the loss is uniformly PŁ ⋆with respect to the damped Hessian in Nεloc (w⋆).29 Challenges in Training PINNs 

Lemma G.8 (Preconditioned smoothness and PŁ ⋆). Suppose γ ≥ μ. Then for any w, w ′, w ′′ ∈ N εloc (w⋆), the following statements hold: 1. L(w′′ ) ≤ L(w′) + ⟨∇ L(w′), w ′′ − w′⟩ + 1+ ε 

> 2

∥w′′ − w′∥2 

> HL(w)+ γI

.2. ∥∇ L(w)∥2(HL(w)+ γI )−1 

> 2

≥ 11+ ε 

> 1(1+ γ/μ )

L(w).Proof. 1. By Taylor’s theorem 

L(w′′ ) = L(w′) + ⟨∇ L(w′), w ′′ − w′⟩ +

Z 10

(1 − t)∥w′′ − w′∥2

> HL(w′+t(w′′ −w′))

dt 

Note w′ + t(w′′ − w′) ∈ N εloc (w⋆) as Nεloc (w⋆) is convex. Thus we have, 

L(w′′ ) ≤ L(w′) + ⟨∇ L(w′), w ′′ − w′⟩ +

Z 10

(1 − t)∥w′′ − w′∥2 

> HL(w′+t(w′′ −w′))+ γI

dt 

≤ L(w′) + ⟨∇ L(w′), w ′′ − w′⟩ +

Z 10

(1 − t)(1 + ε)∥w′′ − w′∥2 

> HL(w)+ γI

dt 

= L(w′) + ⟨∇ L(w′), w ′′ − w′⟩ + (1 + ε)2 ∥w′′ − w′∥2 

> HL(w)+ γI

.

2. Observe that 

∥∇ L(w)∥2(HL(w)+ γI )−1

2 = 12 (F(w) − y)T h

JF (w) ( HL(w) + γI )−1 JF (w)T i

(F(w) − y).

Now, 

JF (w) ( HL(w) + γI )−1 JF (w)T ⪰ 1(1 + ε) JF (w) ( G(w) + γI )−1 JF (w)T

= 1(1 + ε) JF (w) JF (w)T JF (w) + γI −1 JF (w)T

Lemma G.7 guarantees JF (w) has full row-rank, so the SVD yields 

JF (w) JF (w)T JF (w) + γI −1 JF (w)T = U Σ2(Σ 2 + γI )−1U T ⪰ μμ + γ I. 

Hence ∥∇ L(w)∥2(HL(w)+ γI )−1

2 ≥ μ

(1 + ε)( μ + γ)12 ∥F (w) − y∥2 = μ

(1 + ε)( μ + γ) L(w).

Lemma G.9 (Local preconditioned-descent) . Run Phase II of Algorithm 1 with ηDN = (1 + ε)−1 and γ = μ. Suppose that 

˜wk, ˜wk+1 ∈ N εloc (w⋆), then 

L( ˜ wk+1 ) ≤



1 − 12(1 + ε)2



L( ˜ wk).

Proof. As ˜wk, ˜wk+1 ∈ N εloc (w⋆), item 1 of Lemma G.8 yields 

L( ˜ wk+1 ) ≤ L( ˜ wk) − ∥∇ L( ˜ wk)∥2(HL( ˜ wk )+ μI )−1

2(1 + ε) .

Combining the last display with the preconditioned PŁ ⋆condition, we conclude 

L( ˜ wk+1 ) ≤



1 − 12(1 + ε)2



L( ˜ wk).

30 Challenges in Training PINNs 

The following lemma describes how far an iterate moves after one-step of Phase II of Algorithm 1. 

Lemma G.10 (1-step evolution) . Run Phase II of Algorithm 1 with ηDN = (1 + ε)−1 and γ ≥ μ. Suppose ˜wk ∈ N ε 

> 3

(w⋆),then ˜wk+1 ∈ N εloc (w⋆).Proof. Let P = HL( ˜ wk) + γI . We begin by observing that 

∥ ˜wk+1 − w⋆∥HL(w⋆)+ μI ≤ √1 + ε∥ ˜wk+1 − w⋆∥P .

Now, 

∥ ˜wk+1 − w⋆∥P = 11 + ε ∥∇ L( ˜ wk) − ∇ L(w⋆) − (1 + ε)P (w⋆ − ˜wk)∥P −1

= 11 + ε

Z 10

∇2L(w⋆ + t(wk − w⋆)) − (1 + ε)P  dt (w⋆ − ˜wk) P −1

= 11 + ε

Z 10

h

P −1/2∇2L(w⋆ + t(wk − w⋆)) P −1/2 − (1 + ε)I

i

dtP 1/2(w⋆ − ˜wk)

≤ 11 + ε

Z 10

P −1/2∇2L(w⋆ + t(wk − w⋆)) P −1/2 − (1 + ε)I dt ∥ ˜wk − w⋆∥P

We now analyze the matrix P −1/2∇2L(w⋆ + t(wk − w⋆)) P −1/2. Observe that 

P −1/2∇2L(w⋆ + t(wk − w⋆)) P −1/2 = P −1/2(∇2L(w⋆ + t(wk − w⋆)) + γI − γI )P −1/2

= P −1/2(∇2L(w⋆ + t(wk − w⋆)) + γI )P −1/2 − γP −1 ⪰ (1 − ε)I − γP −1 ⪰ − εI. 

Moreover, 

P −1/2∇2L(w⋆ + t(wk − w⋆)) P −1/2 ⪯ P −1/2(∇2L(w⋆ + t(wk − w⋆)) + γI )P −1/2 ⪯ (1 + ε)I. 

Hence, 

0 ⪯ (1 + ε)I − P −1/2∇2L(w⋆ + t(wk − w⋆)) P −1/2 ⪯ (1 + 2 ε)I, 

and so 

∥ ˜wk+1 − w⋆∥P ≤ 1 + 2 ε

1 + ε ∥ ˜wk − w⋆∥P .

Thus, 

∥ ˜wk+1 − w⋆∥HL(w⋆)+ μI ≤ 1 + 2 ε

√1 + ε ∥ ˜wk − w⋆∥P ≤ (1 + 2 ε)∥ ˜wk − w⋆∥HL(w⋆)+ μI ≤ εloc .

The following lemma is key to establishing fast local convergence; it shows that the iterates produced by damped Newton’s method remain in Nεloc (w⋆), the region of local convergence. 

Lemma G.11 (Staying in Nεloc (w⋆)). Suppose that wloc ∈ N ρ(w⋆), where ρ = εloc 

> 19

√βL/μ . Run Phase II of Algorithm 1 with 

γ = μ and η = (1 + ε)−1, then ˜wk+1 ∈ N εloc (w⋆) for all k ≥ 1.Proof. In the argument that follows κP = 2(1 + ε)2. The proof is via induction. Observe that if wloc ∈ N ϱ(w⋆) then by Lemma G.10, ˜w1 ∈ N εloc (w⋆). Now assume ˜wj ∈ N εloc (w⋆) for j = 2 , . . . , k . We shall show ˜wk+1 ∈ N εloc (w⋆). To this end, observe that 

∥ ˜wk+1 − w⋆∥HL(w⋆)+ μI ≤ ∥ wloc − w⋆∥HL(w⋆)+ μI + 11 + ε

> k

X

> j=1

∥∇ L(wj )∥(HL(w⋆)+ μI )−1

31 Challenges in Training PINNs 

Now, 

∥∇ L(wj )∥(HL(w⋆)+ μI )−1 ≤ 1

√μ ∥∇ L(wj )∥2 ≤

s

2βL

μ L(wj )

≤

s

2βL

μ



1 − 1

κP

j/ 2 pL(wloc ),

Here the second inequality follows from ∥∇ L(w)∥ ≤ p2βLL(w), and the last inequality follows from Lemma G.9, which is applicable as ˜w0, . . . , ˜wk ∈ N εloc (w⋆). Thus, 

∥ ˜wk+1 − w⋆∥HL(w⋆)+ μI ≤ ρ +

s

2βL

μ

> k

X

> j=1



1 − 1

κP

j/ 2 pL( ˜ w0)

≤ ρ +

s

(1 + ε)βL

2μ ∥wloc − w⋆∥HL(w⋆)+ μI kX

> j=1



1 − 1

κP

j/ 2

≤

1 + 

s

βL

μ

> ∞

X

> j=0



1 − 1

κP

j/ 2

 ρ

=

1 + 

pβL/μ 

1 −

q

1 − 1

> κP

 ρ ≤ εloc .

Here, in the second inequality we have used L( ˜ w0) ≤ 2(1 + ε)∥wloc − w⋆∥2 

> HL(w⋆)+ μI

, which is an immediate consequence of Lemma G.8. Hence, ˜wk+1 ∈ N εloc (w⋆), and the desired claim follows by induction. 

Theorem G.12 (Fast-local convergence of Damped Newton) . Let wloc be as in Corollary G.4. Consider the iteration 

˜wk+1 = ˜ wk − 11 + ε (HL( ˜ wk) + μI )−1∇L( ˜ wk), where ˜w0 = wloc .

Then, after k iterations, the loss satisfies 

L( ˜ wk) ≤



1 − 12(1 + ε)2

k

L(wloc ).

Thus after k = O log  1

> ϵ

 iterations 

L( ˜ wk) ≤ ϵ. 

Proof. Lemma G.11 ensure that ˜wk ∈ N εloc (w⋆) for all k. Thus, we can apply item 1 of Lemma G.8 and the definition of 

˜wk+1 , to reach 

L( ˜ wk+1 ) ≤ L( ˜ wk) − 12(1 + ε) ∥∇ L( ˜ wk)∥2  

> P−1

.

Now, using item 2 of Lemma G.8 and recursing yields 

L( ˜ wk+1 ) ≤



1 − 12(1 + ε)2



L( ˜ wk) ≤



1 − 12(1 + ε)2

k+1 

L(wloc ).

The remaining portion of the theorem now follows via a routine calculation. 

G.4. Formal Convergence of Algorithm 1 

Here, we state and prove the formal convergence result for Algorithm 1. 32 Challenges in Training PINNs 

Theorem G.13. Suppose that Assumption 8.1 and Assumption G.1 hold, and that the loss is μ-PŁ ⋆in B(w0, 2R), where 

R = 2√2βLL(w0) 

> μ

. Let εloc and ρ be as in Corollary G.4, and set ε = 1 /6 in the definition of εloc . Run Algorithm 1 with parameters: ηGD = 1 /β L, K GD = βL 

> μ

log 

 4 max {2βL,1}L(w0)

> μρ 2



, η DN = 5 /6, γ = μ and KDN ≥ 1. Then Phase II of Algorithm 1 satisfies 

L( ˜ wk) ≤

 23

k

L(wKGD ).

Hence after KDN ≥ 3 log 

 L(wKGD )

> ϵ



iterations, Phase II of Algorithm 1 outputs a point satisfying 

L( ˜ wKDN ) ≤ ϵ. 

Proof. By assumption the conditions of Corollary G.4 are met, therefore wKGD satisfies ∥wKGD − w⋆∥HL(w⋆)+ μI ≤ ρ, for some w⋆ ∈ W ⋆. Hence, we may invoke Theorem G.12 to conclude the desired result. 33
