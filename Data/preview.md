## Review Example (2020)

### review

This paper investigates the important problem of spatial-temporal forecasting, and proposes a multi-scale spatial-temporal joint graph convolution that jointly model the heterogeneous spatial-temporal correlations. Empirical results on multiple real-world datasets shows promising results.

The draft seems to be written in a rush, with mistake/typos in paragraphs, figures and tables. Besides, the some of the major claims are not well supported by the empirical results. Here are details about the main concerns:

D1: Some major claims are not well supported by the experimental results.
- <mark>The main novelty of this paper the is  the spatial temporal joint convolution. Yet, its design needs more theoretical and empirically justifications.</mark>  <mark>The idea of the concatenating K order of Laplacian matrix is a bit ad-hoc lacking of theoretical justification.</mark>  Besides, the spatial temporal joint graph convolution is not necessary "more joint" than baseline algorithm like DCRNN which incorporates the graph convolution operation into the each sub-step of the RNN operation.
- Besides, the claimed convolution in the spectral domain is actually operations in the spatial domain since the final form of the convolution is essentially a polynomial of the Laplacian matrix without involved the transformation into the spectral domain.
- <mark>Limited ablation studies are conducted to show its effectiveness.</mark> There are some ablation study in Table 2, but not enough to well support the claims.  For example, what is performance gain by simplify replacing the graph convolution with the proposed spatial-temporal joint graph convolution? Is inception style convolution is actually needed? What is the different with and without it?
- Besides, as shown in Table 2, even after the adding the spatiotemporal convolution and the inception attention mechanism, <mark>the performance is still worse than some baselines, including DCRNN and AGCRN.</mark> Potentially it is also possible that the mask (which can be applied to other baselines) actually contributes to the major improvement.

D2: Presentation. This paper seems to be written in a rush, and the presentation need more polish.

- <mark>The technical part is a bit hard to follow.</mark> For example, when explaining the spatial-temporal joint convolution, it might be easier to understand if the author provides an additional figure about it, e.g., a 2-D matrix with size T x K, with filters of size K_t and K_s applied on it, where graph convolution is used for the feature extraction.
- <mark>Inconsistent name of the proposed model.</mark> <mark>The name of the proposed model is not consistent, for example it is called ASTI-GCN in abstract, while in Figure 2a it is called ATI-GCN.</mark> Yet, in Section 4 is is call ASTIGCN, and in Table 2 it is also called ours.
- <mark>Errors/typos in table and paragraphs.</mark> For example, <mark>in Table 1 the RMAE should RMSE.</mark> <mark>The Laplqaacian in Section 3.2 should be Laplacian.</mark> - In Equation (8), we may rewrite \hat{Y}_i as \hat{Y}(\Theta)_i so the loss is a function of the parameter \Theta.  In Section 4.2, we may Capitalize the first letter of alternative to make it consistent with the other three. Also remove the duplicate periods at the end of the sentence.
- In Equation (2), the T_k(L) probably represents the order k instead of order k-1 otherwise T_0(L) will become order -1.
- The datasets use, i.e., PeMS04, PeMS08, seems to be PeMSD4 and PeMSD8, we may keep it consistent with previous methods to facilitate comparison of metrics in baseline papers.
-  In the Table 2, it is mentioned that each setting has been run for 10 time, and it is helpful to also include the standard deviation to show the statistical significance of the improvement

### (Aspect Classification)

| Aspect | Stance | Evidence |
|--------|--------|----------|
| Technical Correctness | negative | <mark>The main novelty of this paper the is  the spatial temporal joint convolution. Yet, its design needs more theoretical and empirically justifications. The idea of the concatenating K order of</mark> |
| Ablation & Attribution | negative | <mark>Limited ablation studies are conducted to show its effectiveness. There are some ablation study in Table 2, but not enough to well support the claims. For example, what is performance</mark> |
| Baselines & Fair Comparison | negative | <mark>the performance is still worse than some baselines, including DCRNN and AGCRN. Potentially it is also possible that the mask (which can be applied to other baselines) actually contributes to</mark> |
| Writing Clarity & Organization | negative | <mark>The technical part is a bit hard to follow. For example, when explaining the spatial-temporal joint convolution, it might be easier to understand if the author provides an additional figure</mark> |
| Related Work Positioning & Citations | negative | <mark>Inconsistent name of the proposed model. The name of the proposed model is not consistent, for example it is called ASTI-GCN in abstract, while in Figure 2a it is called</mark> |
| Reproducibility & Implementation | negative | <mark>Errors/typos in table and paragraphs. For example, in Table 1 the RMAE should RMSE. The Laplqaacian in Section 3.2 should be Laplacian</mark> |

---

## Review Example (2022)

### summary_of_the_paper

This paper proposes a test-time fine-tuning to boost the adversarial robustness of the classifier. Namely, the new method updates the parameter of the underlying deep network based on self-training (and potentially assuming the network is trained with a meta-learning algorithm). To evaluate the robustness, the paper places the model under a regular white-box adversary and a smarter one aware of the fine-tuning and shows that even with a smarter adversary the fine-tuned model is still more robust.

### strength_and_weaknesses

**Strength**: The paper has a solid motivating theorem that shows why a test-time fine-tuning can improve the robustness. Even though the theorem does not directly help the design of the final algorithm, the theoretical contribution is still important. In the empirical part, the paper uses a standard set of adversaries, e.g. AutoAttack and the improvement of robustness is significant compared to its baselines. Overall, the structure of the paper is easy to follow and I know what to expect when I finish reading one section.

**Weakness**: My major concern is the empirical evaluation. I also have some minor concerns on the motivating theorem and the writing. Please see the details below.

**<mark>The setup of an empirical adversary may not be strong enough.</mark>** Firstly let me restate the setup of the problem. If my read on the paper is correct, given a batch of input $X$, this work proposes to fine-tune the parameter of the model $\theta_0 \rightarrow \theta$ and the update $\Delta \theta = \theta - \theta_0$ is a function of the batch $X$ (and some training batch).

To evaluate the robustness, the paper uses two adversaries: a standard and an adaptive one. I am not able to find the definition of a standard adversary but by reading the description of an adaptive one I think the paper assumes that a standard one targets on a model parameterized with $\theta_0$ while an adaptive one targets $\theta$ (please correct me if I am wrong).

The paper assumes the adaptive one is a strong adversary by fully leveraging the knowledge of the fine-tuning process. My comment for this setup is that:

(1) <mark>the adaptive one may be just as strong as a standard adversary who is faced with a model without fine-tuning.</mark> This is because the white-box adversary has access to the parameters (i.e. $\theta$) of the model that makes the inference instead of some parameters (i.e.$ \theta_0$) that have nothing to do with the inference;

and (2) an adversary who is smarter should be targeting the fine-tuning process. One example I can think of is that the adversary carefully constructs the test batch sent to your system such that these inputs sit evenly on two sides of the decision boundary and are both less than $\epsilon$ away from the boundary. How would the fine-tuning behave? Will it almost make no update to $\theta_0$ (so the adversary can attack the original model again) or it gives up one half the points so after fine-tuning $\theta$ can be robust on the rest? In practice, the adversary can jointly optimize the noise added to each input. For example, if the adversary only cares about the inference result on $x_i$, it can accompany another input $x_j$, together with $x_i, that targets only on making the fine-tuning doing nothing or worse. I drew a picture [here](https://ibb.co/yXPS71D) for a linear classifier to illustrate the case. Also, the training set used in fine-tuning is also exposed to the attacker and a realistic attacker should take advantage of it. In general, I don't think the current adaptive attacker is adaptive enough to the potentially vulnerable parts in the proposed defense.

Two additional questions regarding the experiment:

1. <mark>a strictly stronger attacker should always have lower accuracy than a standard one but in Table 1, some adaptive attacker is even worse than a standard one.</mark> For example, on the intersection of the row Probation-OnlineFT and the column Square Attack. Can the authors give some explanation to these results?

2. <mark>It seems that there are a lot of hyper-parameters to be tuned. Can the author provide some recommendations of ways to find these parameters in the main body of the paper.</mark>

**Soft labels used in Theorem 3.1.**  <mark>Will the theorem fail to hold if considering hard labels like [0, 1] instead of soft labels generated from Gaussian noise?</mark> I think in a classification setup using a soft label might be okay if well-explained motivation is given.

**Typos.** I found many typos in the paper. I list some examples here:

4. <mark>In Figure 1, it should be $\theta_AB$ not $\theta_BA$ from the caption (or I mis-understand the picture).</mark>

### clarity,_quality,_novelty_and_reproducibility

**Clarity**: Overall the idea of the paper is clearly stated. The clarity can be further improved if (1) <mark>The notation becomes simpler and less dense;</mark> (2) Some definitions are pretty ad-hoc. For example, the definition of $L_{SS}$ is not presented until the experiment section that discusses what are the self-learning tasks; and (3) Taking several passes to fix the typo.

**Quality**: The theoretical part of the work is sound. <mark>The empirical evaluation does not convince me that the proposed method is actually more robust (see the Weakness part in the previous review box).</mark>

**Novelty**: <mark>The proposed method is somewhat novel by adapting test-time fine-tuning to improve adversarial robustness.</mark>

**Responsibility**: <mark>The reproducibility can be improved if the author provides a summary paragraph about where to find descriptions that produce the experiments.</mark>

### summary_of_the_review

In summary, I am inclined to reject it at this moment because I am not sure if the proposed method actually produces a new network $\theta$ that is more robust with more obviously vulnerable parts exposed to the adversary. The writing of the paper can be improved as well.

### (Aspect Classification)

| Aspect | Stance | Evidence |
|--------|--------|----------|
| Experimental Setup & Protocol | negative | <mark>The setup of an empirical adversary may not be strong enough.</mark> |
| Distribution Shift & Generalization (OOD) | negative | <mark>the adaptive one may be just as strong as a standard adversary who is faced with a model without fine-tuning.</mark> |
| Hyperparameter / Seed Sensitivity | negative | <mark>It seems that there are a lot of hyper-parameters to be tuned.</mark> |
| Writing Clarity & Organization | negative | <mark>The notation becomes simpler and less dense;</mark> |
| Technical Correctness | negative | <mark>Will the theorem fail to hold if considering hard labels like [0, 1] instead of soft labels generated from Gaussian noise?</mark> |
| Reproducibility & Implementation | negative | <mark>The reproducibility can be improved if the author provides a summary paragraph about where to find descriptions that produce the experiments.</mark> |
| Originality / Novelty | positive | <mark>The proposed method is somewhat novel by adapting test-time fine-tuning to improve adversarial robustness.</mark> |
| Figures / Tables & Visual Presentation | negative | <mark>In Figure 1, it should be $\theta_AB$ not $\theta_BA$ from the caption (or I mis-understand the picture).</mark> |
| Baselines & Fair Comparison | negative | <mark>a strictly stronger attacker should always have lower accuracy than a standard one but in Table 1, some adaptive attacker is even worse than a standard one.</mark> |
| Statistical Evidence | negative | <mark>The empirical evaluation does not convince me that the proposed method is actually more robust (see the Weakness part in the previous review box).</mark> |

---
