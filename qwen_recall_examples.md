# Qwen 原分类结果的 Recall 样例审计

数据源：`C:\Users\YX\Desktop\read_aspect_results\ICLR_review_aspect_2021_2025_all_fields.tsv`

口径：下面挑了 10 条 review，Qwen 一共抽出 132 个 aspect，正好对应你图里提到的 “132 aspects / 10 reviews”。我按 review 原文快速人工列出主要信息点，再看 Qwen 的 `aspect_bundle` 是否覆盖。这里的 recall 是内容层面的粗审计，不是正式双人标注。

## 总览

| # | Year | Paper / Review | Qwen aspects | 人工重要点覆盖 | 明显问题 |
|---:|---:|---|---:|---:|---|
| 1 | 2021 | `HRL6el2SBQ` / `pHbdQ7sY93F` | 13 | 10 / 10 | 有一个较边缘的 `Data / Dataset` |
| 2 | 2022 | `JJuP86nBl4q` / `hx3gHPbI2xG` | 13 | 11 / 11 | 个别 evidence 截断，aspect 偏细 |
| 3 | 2022 | `YaPPldR6te` / `-XUXEzfsED` | 13 | 10 / 10 | `Reproducibility` 和外部有效性有重复 |
| 4 | 2022 | `WE_vluYUL-X` / `RAT_SeKlfZL` | 12 | 10 / 10 | 噪音少，是较干净样例 |
| 5 | 2022 | `0_TxFpAsEI` / `g6YHe54SnPT` | 14 | 8 / 9 | `Ethics`、`Societal`、`Reproducibility` 明显误标 |
| 6 | 2023 | `6FAH0SgQzO` / `3UoO8ZnqmI` | 13 | 10 / 10 | `Metrics` 标签有些牵强 |
| 7 | 2024 | `4y6Q98hJzr` / `uwNc55Ylqm` | 13 | 10 / 10 | `Originality` 和 `Experimental` 用了同一段泛 evidence |
| 8 | 2024 | `ctzGqxE3O0` / `9ysHAQODuK` | 14 | 12 / 12 | `Ethics` / `Societal` 有重复 |
| 9 | 2024 | `py34636XvR` / `ofeya4m0rs` | 13 | 8 / 10 | `Ethics`、`Societal` 是空 evidence；`Fit` 误标 |
| 10 | 2025 | `avnKEvJk3O` / `fdXzMEetmC` | 14 | 11 / 11 | 个别 aspect 互相重叠 |

粗略合计：人工列出的 103 个重要点里，Qwen 内容上覆盖约 100 个，重要点 recall 很高；但 132 个抽取项里有不少重复、误标、空 evidence 或过细拆分，所以 precision 会显著下降。

## 具体样例

### 1. Intra-class mixup / OOD detection

<details>
<summary>原始 review 全文</summary>

```text
Inspired from inter-class mixup (Zhang et al, ICLR 2018), where data augmentation is used to train models more robust to adversarial samples, this work proposes intra-class mixup to reduce the variance of in-distribution samples, i.e. the training set, and improve the capacity of a trained model to detect out-of-distribution samples at inference time. The key difference between the two works is that the here proposed does the mixup within samples belonging to the same class. 

In addition to this, the work propose to use the angular margin, i.e. the angle between the normal of the decision boundary of a neural net (obtained from the weights of the last layer) and an unmixed sample, to detect OOD samples. The cosine of such angle shall be coupled with an OOD method to perform OOD detection. 

Strengths
- Overall the paper is clearly written, although the experiments and results could be improved. 
- Good coverage of the related work
- Very relevant topic

Weaknesses
- This work is presented as an alternative to standard empirical risk minimization (ERM) or the setup of mixup (Zhang et al, ICLR 2018), where ERM is replaced by vicinal risk minimization (VRM, Chappelle et al, NIPS 2000). What learning strategy is used here, in opposition to these two works, is never stated. 
- The experimental setup is not clear, which limits reproducibility and makes difficult to interpret the obtained results. What exactly is considered as in-distribution and what samples are OoD and how are they generated? (see detailed comments)
- The proposed comparisons against ERM and mixup are not necessarily relevant. ERM is the standard approach to train a model and mixup proposes a data augmentation strategy to make a model more robust to adversarial samples. This work, instead focuses on the detection of OOD samples. As such, it should compare itself with methods addressing the same problem and not directly against ERM and mixup (table 1).

Detailed comments
- Please acknowledge previous work on angle-based outlier detection [1], as it closely relates to this work.
- The angular margin is estimated w.r.t the decision boundary (see eqs. 3 and 4). Therefore, there is an error in the illustration in Fig. 1a.
- Differently from mixup, in this work \lambda does not follow a Beta distribution. Moreover, no details are provided on how it is chosen. Please comment.
- If the label should not change, second line of Eq. 2 could be omitted. Otherwise, there is no guarantee that \hat{y} will have the same value. This would only hold when \lambda=1 or 0 and y_i=y_j=1 or 0.
- Eq 5 implies that new data is being generated, i.e. data augmentation. Is this the case? What happends with the original samples? I suppose they are undesired since they have high variance.
- Could the authors motivate why the angular margin needs to be used coupled with another metric (eq. 7) and not on its own?
- The experimental setup is not clear. The paper misses to clearly establish what is an OoD sample/set on each of the experiments. In which way Gaussian and uniform noise are used for this purpose?
- At inference time, when is a sample considered OOD?
- The AUROC is not a good measure in OOD detection problems, since usually the majority class dominates. AUPRC should be favored. Interestingly, it is mixup that fairs best in that scenario, despite not being a method designed for OOD detection. Please comment 

Minor
- There are typos in the plots in figure 1b,c,d
- Table 2 is unnecessary and may be omitted

References
[1] H.-P. Kriegel, M. S hubert, and A. Zimek. Angle-based outlier detection in high-dimensional data. In Proceedings of the 14th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, KDD ’08, pages 444–452. ACM, 2008.


This work proposes intra-class mixup coupled with an angular mesaure for OOD detection. The idea of an angle-based measure has been explored in the past (not mentioned in the work) and it is interesting to propose it in the context of deep nets.

The work, however, misses some key elements in the presentation of the method and has a weak experimental setup.
```

</details>


Review 主要点：
- 文章清楚、related work 覆盖好、主题 relevant。
- 学习策略没有说清楚。
- 实验设置不清楚，影响结果解释。
- ERM / mixup baseline 对比不够相关。
- Figure 有 typo。
- intra-class mixup 的超参数选择没说明。
- AUROC 不适合，需要 AUPRC。
- OOD / in-distribution 样本定义和生成方式不清。
- angular margin 为什么要和另一个 metric 结合使用，需要解释。

Qwen 覆盖：
- `Writing Clarity & Organization`: "Overall the paper is clearly written"
- `Related Work Positioning & Citations`: "Please acknowledge previous work..."
- `Fit to Venue / Scope`: "Very relevant topic"
- `Problem Setup Validity`: "What learning strategy is used here... is never stated"
- `Experimental Setup & Protocol`: "The experimental setup is not clear..."
- `Baselines & Fair Comparison`: "comparisons against ERM and mixup are not necessarily relevant"
- `Figures / Tables`: "There are typos in the plots"
- `Hyperparameter / Seed Sensitivity`: "no details are provided on how it is chosen"
- `Metrics & Evaluation Criteria`: "AUROC is not a good measure..."
- `Distribution Shift & Generalization`: "What exactly is considered as in-distribution..."
- `Interpretation of Results`: angular margin question

判断：重要点基本全覆盖，噪音主要是拆得很细。

### 2. LAVA datapoint valuation

<details>
<summary>原始 review 全文</summary>

```text
This paper proposes a datapoint valuation method, LAVA, that does not require a pre-defined learning algorithm, which is a common assumption in the existing literature. It utilizes the Wasserstein distance between the training set and the validation set with respect to a hybrid cost that considers both feature and label distances. The authors prove that the distance has theoretical connections with the validation performance (i.e., the utility) and show that the distance can be efficiently calculated using existing solvers. With that, the authors propose to use calibrated gradient to account for a datapoint’s contribution to the distance and thus its value. The paper has done extensive empirical experiments on 5 important application scenarios and demonstrated superior performances. Ablation studies are also done to better understand the behaviors of the proposed method. 

Advantages: 
1. The paper is well-written and easy to follow. The authors additionally give lots of interpretations after results or formulations to help with the understanding. 
2. Label information is incorporated into the dataset distance design.
3. The theoretical part of the paper is sound. Also, the connection from OT distance sensitivity to individual datapoint value is neat and natural.
4. The author provides rather extensive empirical validations of the method and showed state-of-the-art performance. An interesting new application on “irrelevant data detection” is also included, which was originally often discussed as mislabeled data detection.
5. Discussions on the limitations of LAVA in the conclusion are valid and indeed insightful.

Disadvantages:
1. The motivation for developing a learning-agnostic valuation method, especially in the context of the existing works with similar dataset distance approaches could be improved.
2. Some small parts of the experiment details require clarification.
For more details, see below.

1. In the introduction, one motivation for a learning-agnostic method is that the retrainings of the models are too expensive in LOO and CGT. However, I do not think LAVA directly addresses this problem, at least about CGT, because LAVA is more like a perturbation-based contribution measure essentially similar to influence function (INF). LAVA performs a LOO-like computation and does not consider combinations (like in CGT). Also, please give formal justifications with references that the LOO and CGT methods “remain expensive” given the approximations.

2. This is related to the novelty of the work, and how insight it has contributed to the community. There have been attempts to use distribution divergence or dataset differences for data valuation. One reason for choosing OT is that OT is computationally tractable from finite samples: As far as I know, MMD used in [1] has similar properties. It is also essential to draw connections between distribution divergence to learning performance: Another work [2] also partially uses MMD to bound generalization performance. Discussions might be needed to examine the significance of LAVA in the context of the existing works mentioned above.

3. The paper has extensive applications and great performance in detecting “bad” data. However, we care about “good” data as well. Can LAVA perform data summarization tasks (another common application of data valuation) as well? I know that Appendix B.4 is relevant to this question, but I am looking at a much smaller subset size for summarization. For example, can you select 1K points to train a network? This is essentially about the effectiveness of LAVA in picking representative and highly valued datapoints. I would expect a faster increase in model performance when including the highest value points first. 

4. In Section 3.1, it is unclear to me how to calculate the actual change in the OT distance when we perturb the datapoint probability mass by a given amount, if we calculate OT distance based on finite samples?

5. Can you also clarify why is the difference in groundtruth values of the calibrated gradients in Section 3.2 enough to rank all data points? Do you calculate this difference with respect to a common datapoint selected and then rank them accordingly?

6. Why is the feature extractor trained with the validation dataset? Will this introduce any form of bias since the validation dataset will be used for the data valuation step? Will an extractor trained on the overall training dataset work?

7. In Figure 3, it really confuses me that most of the baseline methods perform even worse than random guessing in terms of the detection rate. Are the baselines implemented correctly? Or do you have an explanation for this abnormal behavior? Also, it is weird that some attack/model accuracies do not start from the same point when you start to throw away data (bottom plots).

8. Regarding the Poisoning Attack Detection experiments, you mentioned that this task is “especially hard to detect”. However, the baseline methods actually work better than those in Backdoor Detection. In contrast, LAVA does not perform here as well as that in Backdoor Detection. Any explanation?

Minor: 

9. Referring to the discussion on Figure 1, it would be helpful to briefly explain how do you select (or manipulate) the datasets to create different Wasserstein distances to the validation set when drawing the curves? Or alternatively, do you change the validation set?

10. For Appendix B.2.4, I am interested to know how does the model directly trained on the validation dataset detect bad data?

References: 

[1] Incentivizing Collaboration in Machine Learning via Synthetic Data Rewards. AAAI 2022.

[2] DAVINZ: Data Valuation using Deep Neural Networks at Initialization. ICML 2022.

Overall, I like the idea of a label-aware dataset distance measure as a data valuation metric despite borrowed from the OT literature. The method is backed by theoretical connections to validation performance, which is of interest in the topic of data valuation. The datapoint’s sensitivity to OT distance also naturally fits the marginal contribution concepts often used in data valuation. If my concerns above can be addressed, I think this work could contribute value to the community.
```

</details>


Review 主要点：
- 方法是 learning-agnostic data valuation，设计有新意。
- 写得清楚，理论 sound。
- 5 个应用场景、ablation 比较完整。
- motivation 需要加强，尤其是和已有 dataset-distance 方法的关系。
- 需要补 MMD / distribution divergence 到 learning performance 的相关工作。
- OT perturbation 如何计算不清楚。
- Figure 3 中 baseline 比 random 还差，令人困惑。
- poisoning/backdoor detection baseline 对比解释不清。
- feature extractor 用 validation data 可能引入 bias。

Qwen 覆盖：
- 正面覆盖 writing、technical correctness、experimental protocol、novelty、limitations。
- 负面覆盖 motivation、technical novelty/related work、implementation、figure、baseline fairness、dataset bias。

判断：主要正反评价都抓到，recall 很好；precision 问题在于把 related work / technical novelty 拆得稍碎。

### 3. BCI longitudinal stability

<details>
<summary>原始 review 全文</summary>

```text
The problem tackled is that of the decay in performance of BCI systems over time. The article presents an analysis of an electrocorticography data set (n=6) used for brain-computer interface, and in particular discusses the importance of the different features used by a predictive model built with machine learning techniques.
Four different models are put to the test and the one exhibiting highest prediction rates is further analyses to decode the importance of the different features.
Although ML is popular for BCI applications, I agree with the statement that for the specific case of boosting longitudinal stability of the BCI its application is novel.


Strengths

+ The problem studied is clear and remains open and the study proposed in this draft is a clear contribution to the field.
+ The introduction is entertaining and of adequate depth, the literature review is extensive and its use throughout the article is excellent, the methodology is solid, the results are clear, the discussion (embedded within the results) is interesting, and the article has high nomological validity.

Weaknesses

Not many…
+ Absence of inferential statistics, and even the descriptive statistics is incomplete. For example, the standard deviations of the different statistics are not described, the statistical power analysis is not described, etc.


This is certainly one of the strengths of the paper. Except for a couple of aspects that I would like to ask for more detail, but certainly this paper scores high on all; clarity, quality, novelty, and reproducibility. Regarding that couple of aspects:
+ Why is the 6th rat considered useful for “external validity” yet there Is no evidence or explanation that this rat would be statistically different from the first 5, and certainly the surgery date is not a factor affecting the neural responses of the rodent, is it? If the rat is then statistically similar to the others (besides the natural inter-subject variability for which the other rats may be as different for all that I understand) then there is no reason to accept the 6th subject as useful for claiming external validity and it might be better to use it to increase the internal validity.
+ 1000 replication for 95% statistical power seems pretty large even for small effect sizes. No further details of the power analysis is given. Can the authors indicate how was this calculated? Is perhaps the study overpowered?


+ Without an analysis of error propagation it is difficult to anticipate how far in the long term would the predictive power of the model hold within useful boundaries.
+ There appears to be no measure of the degradation of the performance of the xML pipelines as the prediction horizon is further away.
+ Cross-correlated variables were removed. Were corrections considered (as opposed to simply dropping) e.g. statistical whitening, Bayesian multivariate decoupling, ARIMA models with a cross-variate feed, etc?
+ The explanatory approach methods taken here (SHAP and decision paths) is actually very insightful and in principle is generic, hence it could be translated to other BCI modalities; e.g. EEG based, fNIRS based, etc. What adaptations would be suggested to do so?
+ Although the translation to humans is identified as one of the limitations of the study, I can see how rather than a limitation of this study that makes up for a different study altogether. In this sense, my question is a bit more humble, regardless of the length of the BCI intervention, and focusing strictly on the predictive horizon of the model (currently shown at 15 weeks for the rats), is it likely to be at least equally long in humans? Even if it is only for 15 weeks, that remains a quite reasonable horizon in humans, but unfortunately, with a much more complex nervous system, I reckon the decay of the performance of the predictive models might suffer more heavily?.


Minor details
+ Figures looks grainy on my end (although readable). Not sure whether this is only on my side, but just in case it does not cost much to double check.
+ AI and ML are closely related but not the same. The authors seem to use explainable machine learning and explainable artificial intelligence interchangeably. If this is intentional, I’m fine with it. If not, why not stick to only one of them? Subjectively I would say this paper in particular is closer to xML rather than xAI but I wouldn’t argue with other perceptions.
+ Some of the things explaining the figures are in the main text. Of course, every author has its style and I do not want to interfere. But if there is no strong preference, may I suggest to move such parts to the figure caption to make the images self-contained?


```

</details>


Review 主要点：
- 问题清楚、开放、有贡献。
- 方法、结果、讨论整体扎实。
- ML 用于 BCI 不新，但用于 longitudinal stability 有新意。
- 缺少 inferential statistics，descriptive stats 也不完整。
- `n=6` 的 external validity 解释不足。
- 95% power / 1000 replication 依据不足。
- 长期预测的 error propagation 没分析。
- prediction horizon 越远性能是否退化没测。
- human translation 是限制。
- 图有点糊；AI/ML 术语混用。

Qwen 覆盖：
- `Problem Setup Validity`, `Technical Correctness`, `Technical Novelty`, `Statistical Evidence`, `Fit to Venue`, `Metrics`, `Distribution Shift`, `Efficiency`, `Societal`, `Figures`, `Related Work`, `Writing` 都有对应。

判断：重要点覆盖很高，但有重复，例如 external validity 同时进了 `Fit` 和 `Reproducibility`。

### 4. ReAct prompting

<details>
<summary>原始 review 全文</summary>

```text
This paper proposes ReAct; a novel framework for prompting large language models (LLMs) on tasks that require explicit reasoning and/or acting in an environment. Driven by recent work in plugging in LLMs into the main loop of a reasoning problem (e.g., fact verification or multi-hop question answering), or embodied plan generation (requiring actions/partial observability over time), this work makes a notable observation that the existing ways we have of interacting with LLMs capable of in-context learning are insufficient.

Namely, approaches that follow standard in-context prompting (example/answer) are not enough for any high-resolution reasoning tasks; similarly, chain-of-thought prompting is great for reasoning tasks, but when actions/observations are streaming in, there’s not a good way to incorporate that information in a structured fashion, allowing for downstream exploitation.

Where ReAct is different is in it’s fusion of chain-of-thought style reasoning with records of actions and observations from an external source; for example, one of the evaluations in this work is on HotPotQA — a multi-hop question answering dataset. The LLM in question (PaLM-540B) is enriched with an API that allows it to query targeted passages from Wikipedia. ReAct allows for a system to use the language model as a “notepad”, first noting down any “thoughts” or reasoning traces, and then using the LLM to predict concrete actions (e.g., Wikipedia queries), that are then paired with the corresponding environment observation (e.g., the retrieved Wikipedia passage). The LLM continues this (given only one-two ReAct few-shot formatted examples), until it comes up with the correct answer.

On evaluations spanning Fact Verification, Question Answering, and Plan Generation, this paper clearly demonstrates the superiority of the ReAct style prompting over alternative approaches like standard (prompt/example) approaches, and the competitive “chain-of-thought” prompting, especially by noting that chain-of-thought prompting has a high false positive rate, because it’s reasoning traces are more likely to propagate “hallucinated/false” information.

This is a strong paper with a clear motivation, thorough evaluation, and strong results. I think ReAct-style prompting is a clear win for tasks involving reasoning and embodied actions, and would love to see it adopted.

This is a clearly written paper with thorough explanations, ablations, and design choices. The novelty (given that prompting LLMs is still very much an open question) is clear, and I really trust the evaluation. Reproducibility is the only question here — PaLM-540B is still a gated LM, and no other language models are evaluated here (e.g., GPT-3, which while expensive, is still publicly accessible) — so not sure how these results _really_ generalize.


Strong paper, thorough and insightful evaluation, with clear wins over all alternative methods for prompting language models. Evaluating on multiple tasks, and especially showing the weaknesses of prior approaches like chain-of-thought prompting (e.g., high false positive rate due to “hallucinating” facts) is an added bonus.

I really like this work!

```

</details>


Review 主要点：
- ReAct 融合 reasoning + action/observation，动机清楚。
- novelty 明确。
- 多任务 evaluation 有说服力。
- Chain-of-thought 的 hallucination / false positive 缺点被清楚展示。
- 文章写得清楚。
- 主要问题是 PaLM-540B gated，复现性不足，没有测其他 LM。

Qwen 覆盖：
- `Motivation`, `Originality`, `Technical Novelty`, `Experimental Setup`, `Baselines`, `Reproducibility`, `Technical Correctness`, `Writing`, `Data`, `Metrics`, `Interpretation` 都有明确 evidence。

判断：这是 Qwen 高 recall 且 precision 也相对高的样例。

### 5. Label noise and adversarial robustness

<details>
<summary>原始 review 全文</summary>

```text
The paper studies the adversarial robustness of interpolants (that fit the training data perfectly) in the presence of label noise. They provide bounds on the risk of any interpolant under some mild assumptions on the data generating process. They also prove that adversarial robustness under uniform label noise is close to the worst-case label noise for fixed budget of incorrect labels. They also study the effect of different forms of label noise on real-world datasets and find that "naturally occuring" label noise leads to less adversarial susceptibility than uniform label noise. 

Strengths: The paper studies a generally important problem of understanding the robustness of interpolants (like modern deep networks) in the presence of label noise. The result on how uniform label noise is as hard as worst-case noise is surprising and interesting (but might be of limited practical use as discussed below). The paper also performs experiments on real-world label noise (dataset from prior work) and observes that the adversarial risk in the presence of real world human annotator noise is much better than under uniform label noise. 

Weaknesses: The first result that generalizes Sanyal's result to more general input distributions does not seem that significant/useful to me. As noted below, the authors should clarify why their assumptions are more reflective of real-world datasets than their current assumptions. I also do not believe this paper offers any actionable insights, apart from possibly the insight that "real world" noise is easier to handle than uniform label noise. But of course, there is the difficulty of actually modeling real-world noise correctly. The paper does not compare different training methods (or different interpolants) which seems like an obvious missing piece to me. 

Clarity: At a local level, the paper is quite clear and easy to follow. However, I was unfortunately struggling to get a big picture and unified view on the results. Section 3 was particularly confusing and did not add to the flow of the rest of the paper, which already felt like a combination of disjoint pieces. 

(Major) 
i. Could the authors please clarify why the assumption of Sanyal et al. about input distribution consisting of balls with a single class is unrealistic? It seems like an assumption on the separation between classes which seems natural.  

(Minor)
(a) In the introduction, it is not clear how this work relates to Sanyal et al. What is natural vs adversarial vs uniform random label noise? It needs to be motivated 
(b) the presentation didn't make it very clear that $f$ is any interpolant. The definition was buried in the setup 

Quality: The theoretical results are generally precise and look accurate (I didn't verify all proofs), and the experimental conclusions are well substantiated. The paper makes a series of conjectures that seem a little unnecessary, and it was hard to get clear takeaways from those parts. The paper mentions inductive biases, but offers no real-world "obvious" experiments like comparing interpolants obtained via adversarial training to interpolants obtained via ERM. 

Originality: The paper builds heavily off of the work of Sanyal et al., and extends their results to more general settings. Experiments on different kinds of label noise seem novel and interesting. 

The paper offers some interesting insights, but is missing a clear overall story or actionable takeaways. I believe the paper is currently borderline and I hope the authors can clarify some concerns raised above that can help tilt away from borderline. 
```

</details>


Review 主要点：
- 问题重要：理解 interpolants 在 label noise 下的 robustness。
- 理论结果看起来准确。
- uniform label noise 接近 worst-case label noise 的结果有趣。
- 但第一个理论结果实际意义有限。
- assumptions 是否更贴近真实数据需要解释。
- 没比较不同 training methods / interpolants。
- Section 3 confusing。
- related work 中 Sanyal assumption 需要澄清。
- conjectures 太多，takeaway 不清楚。

Qwen 覆盖：
- 前 9 个主要内容大多抓到。
- 噪音：`Reproducibility` 里放了 interpretation evidence；`Ethics / Safety`、`Societal` 基本是误标。

判断：内容 recall 仍高，但 precision 下降明显。

### 6. FedRC federated learning under shifts

<details>
<summary>原始 review 全文</summary>

```text
This paper studied the federated learning problem with heterogeneous data induced by multiple types of distribution shifts, e.g., feature shift, label shift, and concept shift. To solve this problem, this paper introduced a principle of robust clustering where clients with concept shifts should be clustered together. Then, it proposed a novel FedRC approach (as well as its centralized version RobustCluster) to find the clusters based on the types of distribution shifts. The convergence of RobustCluster was also theoretically analyzed.

**Originality:** This paper studied a more challenging clustered FL setting where multiple types of distribution shifts existed in local clients. It pointed out that the clusters with concept shifts might not learn a common decision boundary, and existing clustered FL approaches failed in handling the concept shifts. This paper then proposed a novel FedRC with concept shift aware objective function. Experiments demonstrated that FedRC achieved better performance than clustered FL baselines in various data sets.

**Quality:** The motivating example in Figures 3&4 clearly illustrated the principles of robust clustering in handling concept shifts. Then the principles of robust clustering also guided the design of the objective function in Eq. (1). The clients with concept shifts were expected to clustered in different groups. The experiments verified the effectiveness of FedRC with respect to local and global generalization performance.

**Clarity:** The motivation of this paper is clear. Different from feature or label shift, concept shift essentially affects the clustering structure. The objective function in Eq. (1) aims to avoid generating clusters with concept shifts. Experiments show that the proposed FedRC significantly outperforms existing clustered FL methods.

**Significance:** The problem studied in this paper is practical but challenging. In real scenarios, different types of distribution shifts occur simultaneously among clients. As a result, adaptively generating clusters based on the types of distribution shifts can be applied to solve real-world federated learning problems.

**W1:** The impact of feature and label shifts on clustering can be further explained. The goal of the proposed clustered method is to separate clients with concept shifts into different clusters. It might consider clients with feature and label shifts into a single cluster. Thus, the clustering quality can also be affected by the feature and label shifts. For example, a single model might fail to hand clients with large label shifts.

**W2:** The optimization of Eq. (2) is unclear. 
- Firstly, the definition of $\tilde{\mathcal{I}}(\mathbf{x}, y; \theta_k)$ is confusing. It is defined over the weights $\gamma_{i,j; k}$, but $\gamma_{i,j; k}$ is also defined over $\tilde{\mathcal{I}}(\mathbf{x}, y; \theta_k)$ in Eq. (4). 
- Secondly, the updating in Eqs. (4)(5) are not associated with $\lambda_i$ in Eq. (2). Then how would the second term of Eq. (2) affect the optimization?

**W3:** The convergence of FedRC is not provided. Theorem 4.3 shows the convergence of the centralized version of FedRC. Can it also hold for federated learning scenarios?

**W4:** Step 2 in Algorithm 1 is not explained. It is unclear why checking and removing models are necessary for FedRC during training.

**Q1:** Figure 1 is hard to follow. It is confusing how label shift and concept shift are involved in Figure 1.

**Q2:** Section 3 compares different clustered FL algorithms in Figure 3. It shows that existing approaches, e.g., FeSEM, IFCA, are not robust to feature and label shifts. But it is confusing how these observations are indicated in Figure 3.

**Q3:** Does FedRC in Algorithm 1 update $\gamma_{i,j; k}, w_{i; k}$ once and $\theta_{i; k}$ for $\Gamma$ local steps?

**Q4:** How are the models of nonparticipating clients generated during testing in the experiments?

**Q5:** Figure 6(d) shows that FedRC outperforms FedAvg and retains robustness when there is only one concept. When there is only one concept, would FedRC exactly recover FedAvg?

**Q6:** Figure 6(c) shows that FedRC with hard clustering consistently outperforms that with soft clustering. Besides, hard clustering can better satisfy the principles of robust clustering by separating clients with concept shifts into different clusters. In this case, It is confusing why not simply apply hard clustering when optimizing FedRC.
```

</details>


Review 主要点：
- 研究多种 distribution shift 下的 clustered FL。
- concept shift clustering 的 problem setup 合理。
- FedRC objective 有新意。
- Eq. (2) optimization 不清楚。
- feature / label shifts 对 clustering 的影响需要解释。
- 现有 baselines 如 FeSEM/IFCA 不 robust。
- 实验支持 local/global generalization。
- hard clustering 为什么不直接用，需要解释。
- Figure 1 难理解。

Qwen 覆盖：
- 对应抽到 `Originality`, `Problem Setup Validity`, `Technical Correctness`, `Technical Novelty`, `Experimental Setup`, `Baselines`, `Statistical Evidence`, `Distribution Shift`, `Interpretation`, `Reproducibility`, `Figures`。

判断：覆盖很全，少量 label 选择偏奇怪，比如把算法步骤问题归到 `Metrics`。

### 7. LLM continual pretraining stability gap

<details>
<summary>原始 review 全文</summary>

```text
This paper uses the concept of stability gap to explain the initial drop in LLM performance during continual pretraining in a new domain. The authors propose three training strategies to address the initial instability: 1) continually pretrain the LLM on a properly sized corpus subset for multiple epochs; 2) Continually pretrain LLM on a high-quality corpus subset; 3) Using data mixture rate that is similar to the pretraining data. The proposed strategies improve the accuracy of the LLM in the new domain when compared to the existing continual pretraining techniques.

- The proposed strategies are easy to implement.
- The LLM fine-tuned with the proposed strategies achieved the highest averaged accuracy score on a suite of medical question answering tasks.

## Major
- It is important to justify the methods of Muennighoff et al. (2024) and Lin et al. (2024) used in this paper. (I assume the four subsequent sentences explain the method (L158-161)). Here are some missing details:
  - Why was KenLM chosen?
  - What is a "high-quality medical reference corpus"? how do you define it? This is a fairly critical point because the "highest-quality" medical corpus can also be defined as those that resemble the downstream tasks the most, which makes the findings more expected (the closer the continual pretraining data is to the downstream tasks, the better the model will perform in the downstream tasks).
- The authors claim that the average accuracy of the LLM on the medical tasks initially drops and rises during the continual pretraining.
	- However, the drop itself does not look significant (less than 1% averaged accuracy). This makes the observation less strong. (See Question 2)
- This paper contains a flawed assumption due to the lack of access to the pretraining corpus. If a stability gap was proposed to explain the ability of the model to maintain performance on previous tasks, such an analysis cannot be achieved if we do not have access to the pretraining corpus.
	- The authors claimed (L233-235) that language modelling loss also preserves general knowledge and text modelling capabilities, which is a big assumption that is not backed by any evidence.
	- Note that text modelling capabilities may still be preserved via language modelling loss during the domain adaptation (continual) pretraining, however, we cannot guarantee that the general knowledge is still being preserved.
	- Additionally, there is no guarantee that the continual pretraining corpus was not included in the pretraining corpus. To examine this, the authors may have to conduct a pretraining from scratch.
- There exists a logical gap between the concepts of relative weight update, stability gradient, and instruction-following ability.
	- The authors concluded that the relative weight update indicates the stability gradient and, in turn, instruction-following ability (L241-253). However, there is no guarantee that relative weight update relates to stability gradient, let alone instruction-following capability.
        - Additional experiments using pretraining from scratch may help understand this phenomenon better.
- There are several mentions of a "properly sized" subset. However, they are not properly defined.
- The performance improvement (Figure 4) when compared to the baseline seems to be <1%. This does not look very significant.

## Minor
- Note that the submission and paper titles are different
- Abstract is generally filled with jargon which makes it harder to follow.
- L50-51: The last sentence of paragraph 1 in the Introduction can benefit from some citations.
- L56: Missing citation for "Previous research"
The introduction section still contains a lot of undefined jargon (i.e., "proper size", "highest-quality tokens", "data mixture")
- L194: Concluding that the "LLM has acquired medical domain knowledge" based on the perplexity score is a bit of an overclaim. Consider rephrasing it.
- Table 2: This misses the performance of the Llama-3-8B models without fine-tuning.
- The authors claim that the proposed strategies are computationally more efficient. By how much exactly? What metrics should you evaluate this on?

## Very minor (e.g., typos, etc)
- Use consistent verb tense (many inconsistent uses of present and past tenses)
- Typo L15: "phrase" -> "phase"
- L68: Instead of "harness" perhaps "mitigate" it? since you would like to mitigate the stability gap as opposed to harnessing it.
- Typo L125: lowercase "Language models"
- Typo L125: "RoBERTa"
- Page 4: Perhaps observations 1 and 2 can be swapped because in practice we may not know the downstream tasks during the (continual) pretraining phase.
- Figure 6b: The caption does not seem to be correct. The figure seems to show accuracy during law continual pretraining, while the caption is about relative parameter updates during the medical continual pretraining process.

1) The stability gap concept proposed by previous studies is about the inability to maintain performance on **prior** tasks and the one mentioned in this paper is about the performance in the **new** target task. How are they two related in your experiments?
2) The initial drop in the averaged accuracy of the LLM on the medical tasks looks very insignificant.
	- Have you done a statistical test to verify this? 
	- Is the small drop (<1%) in line with the findings of previous stability gap studies?
3) Data Mixture Results (Figure 4b and 4c):
	- The authors may need to compare the proposed strategies with the baseline (full data with multiple epochs).
	- The average medical and commonsense performance seems to drop in the 5th epoch. Why is that the case? What would happen if you continue the pretraining to 6th, 7th, ... epoch?
4) How similar is the "high-quality" medical reference corpus to the downstream tasks?
	- If you run the KenLM model on the downstream datasets, what is the perplexity? Would the perplexity be very low too?
```

</details>


Review 主要点：
- 文章提出三种 continual pretraining 策略，容易实现。
- 医学 QA 平均准确率提升。
- efficiency claim 需要具体指标。
- LM loss preserve general knowledge 是未经支持的大假设。
- Muennighoff / Lin 方法引用和使用需要 justification。
- KenLM 与 high-quality corpus 定义不清。
- 初始 drop 很小，需要统计检验。
- 需要 full-data multiple epochs baseline。
- abstract jargon 太多。
- Figure 6b caption 错。

Qwen 覆盖：
- 上述点基本都进了 `Efficiency`, `Technical Correctness`, `Related Work`, `Data`, `Distribution Shift`, `Statistical Evidence`, `Ablation`, `Writing`, `Figures`, `Originality/Experimental`。

判断：recall 高；问题是 positive evidence 被重复塞进两个 aspect。

### 8. Android malware BID

<details>
<summary>原始 review 全文</summary>

```text
The paper presents a Broad Incremental Detection (BID) framework to address Android malware detection.
It proposes an incremental learning mechanism using the Broad Learning System (BLS) for
real-time malware detection without retraining, alongside Sparse Relational Autoencoders (SRAE)
for better feature selection. Experimental results are reported across three datasets,
suggesting that BID achieves superior performance and computational efficiency over existing models.

While this paper is timely and attempts to address a practical challenge in cybersecurity domain, there are several critical issues that need
to be addressed. In particular, the system is not clearly explained, the datasets are non-standard and limited,
and the results are not compared with state-of-the-art malware detection methods.
Important aspects, such as catastrophic forgetting and real-world applicability, are not addressed.
The experimental setup lacks depth with missing implementation details, no statistical analysis, and
an unclear discussion of results. See the detailed breakdown below.

1. Incremental Learning Integration: The application of incremental learning to Android malware detection is interesting and
        offers a practical way to reduce retraining costs.

2. Computational Efficiency: The paper shows that BID requires relatively less runtime compared to prior work, making it appear suitable for real-time scenarios.

3. Use of Public Datasets: The experiments use public datasets.

1. Clarity of the system

The reviewer had a hard time understanding how the proposed system works.
Furthermore, the use of BLS in an incremental learning framework is not particularly new,
especially in the malware domain (see related references 1-3, 12, 13).
The reviewer is unable to identify the unique contribution of the paper.

The reviewer suggests a step-by-step breakdown of the BID framework’s architecture and functioning.
Detailed explanation of how incremental learning is applied in the model,
beyond the BLS component would strengthen the paper.
In addition, references to similar works in malware
detection (e.g., specific papers on BLS in malware)
would enhance the comparison and clarify unique contributions of the paper.

2. Incremental learning (IL)

a. How is the proposed system better than other IL approaches?
b. How does IL compare with continual learning (CL) approaches for malware detection?
c. Why is IL needed instead of CL?

3. Catastrophic Forgetting for IL

The paper did not evaluate its system against catastrophic forgetting, a major drawback of incremental learning.

To ensure robustness, the reviewer recommends adding experiments to evaluate the
system against catastrophic forgetting phenomena,
a fundamental challenge in IL. The reviewer suggests the paper to follow this paper [14].


4. Lack of Comparison with State-of-the-Art Methods

The paper fails to compare its approach with widely adopted state-of-the-art
Android malware detection techniques (see related references 4-9).
This omission limits the relevance and impact of the reported findings.
Without such comparisons, it is difficult to determine whether the BID framework truly outperforms best practices.

The reviewer strongly suggests the paper to evaluate the system against these benchmarks to
evaluate the strengths of the proposed system. 



5. Dataset

The most widely used Android malware dataset is Drebin [7], but the paper does not evaluate its approach with this dataset.
The datasets used (i.e., TUANDROMD, CIC-2019, and CIC-2020) are not widely adopted in the malware research space and are not considered benchmark datasets.

The paper uses only 1/40 of the CIC-2020 dataset, which is an insufficient sample size. It is unclear why the dataset was reduced for evaluation.

The explanation of the CIC-2020 dataset is inaccurate; the original paper mentions that the dataset contains 200K benign and 200K malware samples [10], but this paper reports different numbers.

The CIC-2019 dataset is unavailable at the given URL.

The datasets used are too small compared to standard practices in malware research.
Moreover, the ratio of benign to malware apps is typically 90:10 to reflect practical Android malware distributions [6],
but this ratio is not followed in the paper.

The reviewer suggests the paper to evaluate their system with i. Drebin dataset [7], and ii. use AndrooZoo [11] repository to collect a larger dataset following the best practices and evaluate their system against the larger dataset. 

6. Experimental setting

Although the BID model shows some performance improvements, the experimental setup lacks depth. There are no details about the implementation or configuration of the proposed system. The reviewer suggests including hyperparameter choices, training configuration, and feature selection specifics.
These should be included to improve reproducibility.

The paper does not provide statistical significance analysis, error ranges, or detailed hyperparameter optimization procedures, making it difficult to trust the reported results. The reviewer suggests including standard deviation or confidence intervals on performance metrics.

The incremental dataset split is not well justified and does not seem to reflect the real-world dynamic evolution of malware.

7. Results

The reviewer finds the interpretation of the results unclear. There is no analysis or discussion of the results to provide insights into their significance.

The reviewer suggests the paper to include insights into
what the results imply about the system’s performance,
efficiency, and limitations.

8. No Discussion of Limitations and Real-world Impact:

The paper does not discuss the limitations of the proposed framework, such as challenges in real-world deployment. It is unclear how relevant this work is to practical Android malware detection systems.


Related references:

[1] Yuan, Wei, et al. "A lightweight on-device detection method for android malware." IEEE transactions on systems, man, and cybernetics: systems, 2019.

[2] Vasan, Danish, Mohammad Hammoudeh, and Mamoun Alazab. "Broad learning: A GPU-free image-based malware classification." Applied Soft Computing, 2024.

[3] Liu, Licheng, et al. "Self-paced broad learning system." IEEE Transactions on Cybernetics, 2022.

[4] McLaughlin, Niall, et al. "Deep android malware detection." CODASPY. 2017.

[5] Yuan, Zhenlong, et al. "Droid-sec: deep learning in android malware detection." SIGCOMM. 2014.

[6] Xu, Ke, et al. "Droidevolver: Self-evolving android malware detection system." EuroS&P 2019.

[7] Arp, Daniel, et al. "Drebin: Effective and explainable detection of android malware in your pocket." NDSS 2014.

[8] Mariconti, Enrico, et al. "Mamadroid: Detecting android malware by building markov chains of behavioral models." NDSS 2017.

[9] Renjith, G., and S. Aji. "On-device resilient Android malware detection using incremental learning." Procedia Computer Science 215 (2022): 929-936.

[10] Rahali, Abir, et al. "Didroid: Android malware classification and characterization using deep image learning." Proceedings of the 2020 
10th International Conference on Communication and Network Security. 2020.

[11] Allix, Kevin, et al. "Androzoo: Collecting millions of android apps for the research community." Proceedings of the 13th international conference on mining software repositories. 2016.

[12] Vasan, Danish, Mohammad Hammoudeh, and Mamoun Alazab. "Broad learning: A GPU-free image-based malware classification." Applied Soft Computing 154 (2024): 111401.

[13] Zhang, Yibin, Guan Gui, and Shiwen Mao. "A lightweight malware traffic classification method based on a broad learning architecture." IEEE Internet of Things Journal (2023).

[14] Díaz-Rodríguez, Natalia, et al. "Don't Forget, There is More than Forgetting: new Metrics for Continual Learning." Continual Learning Workshop at NeurIPS 2018.

1. How is the proposed system better than other Incremental Learning (IL) approaches?
2. How does IL compare with Continual Learning (CL) approaches for malware detection?
3. Why is IL preferred over CL in this context?
4. Why did the paper not include comparisons with widely adopted state-of-the-art Android malware detection techniques?
5. Why was the Drebin dataset not used for evaluation, given its widespread use in Android malware research?
6. Why was only 1/40 of the CIC-2020 dataset used, and how does this reduced size impact the evaluation?
7. Why does the paper report different numbers for the CIC-2020 dataset than the original source?
8. How does the incremental dataset split align with real-world malware evolution?
9. What strategies can be adapted to prevent catastrophic forgetting in the incremental learning framework for android malware detection?
10. What real-world deployment challenges do the authors foresee, and how does the system address them?
```

</details>


Review 主要点：
- 问题 timely，有实践价值。
- incremental learning 用于 malware detection 有趣。
- runtime 看起来更适合 real-time。
- 系统解释不清。
- 数据集 non-standard / limited。
- 没和 SOTA Android malware detection 比。
- implementation details 缺失。
- catastrophic forgetting 未评估。
- real-world deployment limitation 未讨论。
- 没 statistical analysis / error ranges / hyperparameter details。
- incremental split 不像真实 malware evolution。
- result interpretation 不清楚。

Qwen 覆盖：
- 12 个主要点基本逐项命中，并分到 motivation、technical novelty、efficiency、writing、data、baseline、implementation、OOD、statistical evidence、experimental protocol、interpretation 等。

判断：这是高 recall 的很强样例；噪音主要是 `Ethics` 和 `Societal` 对同一句 real-world limitation 重复编码。

### 9. Entropic unbalanced optimal transport

<details>
<summary>原始 review 全文</summary>

```text
This work introduces a method to solve the (semi-relaxed) entropic unbalanced optimal transport problem. First, different equivalent formulation of the problem (namely a dynamic formulation and a dynamic dual) are derived. Then, it is shown that the problem can be stated as a stochastic optimal control problem with a HJB constraint on the value function and a Fokker-Planck constraint for the distribution. The authors then propose to solve this problem by parameterizing the value function with neural networks. Finally, they experiment on generative modeling tasks, and compare on synthetic datasets how well the method allows to recover the optimal coupling and value.

The paper is overall well written. It introduces a well motivated method by deriving a suitable dual dynamic formulation of the EUOT problem, and rewriting it as a stochastic optimal control problem.

The experiments on generative modeling seem good.

On the presentation of the paper, I believe some things could be improved. For instance, in Section 4.1, a lot of equations are presented, which are obtained by performing only some rewriting (e.g. equation (21) to (22) and then (22) to (24)). While this is very clear, I would suggest to just report the last equation (24) with some description of what has been done, and report the detailed derivations in Appendix. Also, the legend of Figure 3 are too small. A lot of abreviations are not given or are given after their introduction (NFE, IPF, IMF, HJB...). The notations often change between $u_t(x)$ and $u(t,x)$.

The full procedure is not very clear. It would be better to add an Algorithm.

I believe some relevant baselines are missing from the Generative modeling experiment. I am thinking e.g. of [1] who solve the UOT problem and reported a FID of 2.97 on CIFAR10.

While this method computes an unbalanced OT problem, the robustness to outliers is not discussed nor tested.

[1] Choi, Jaemoo, Jaewoong Choi, and Myungjoo Kang. "Generative modeling through the semi-dual formulation of unbalanced optimal transport." Advances in Neural Information Processing Systems 36 (2024).

Line 31, the paper (Jordan et al, 1998) is cited for generative modeling. I don't think they do generative modeling at all.

Something more subjective, Line 107, I don't like the terminology of "stochastic map". It is not really a map. I would be more accurate to describe it as a (conditional) probability or probability kernel.

Since the first marginal of the problem is fixed, it would be clearer to state the problem as semi-unbalanced. Is it more difficult to derive Theorem 3.2 and Proposition 3.4 with both marginals relaxed?

The method relaxes a lot of constraints into the loss. I wonder how hard it is to make sure every term go to 0. Also, is this method costly compared e.g. to the semi-dual approach of [1]? And is it stable to train?

Line 512, it is stated that "there is no closed-form for the EUOT problem". But I believe there are in [2], and [2] is also the right reference for closed forms of the EOT problem between Gaussian. Therefore, I would suggest to also perform the experiments in Section 5.2 with unbalanced Gaussian.

Some references on generative modeling with unbalanced OT problem could be added, e.g. [3, 4].

Typos:
- Line 175: "Dynamcial"
- Line 513: "Conducted same benchmark"

[1] Choi, Jaemoo, Jaewoong Choi, and Myungjoo Kang. "Generative modeling through the semi-dual formulation of unbalanced optimal transport." Advances in Neural Information Processing Systems 36 (2024).

[2] Janati, H., Muzellec, B., Peyré, G., & Cuturi, M. (2020). Entropic optimal transport between unbalanced gaussian measures has a closed form. Advances in neural information processing systems, 33, 10468-10479.

[3] Dao, Q., Ta, B., Pham, T., & Tran, A. (2023). Robust Diffusion GAN using Semi-Unbalanced Optimal Transport. arXiv preprint arXiv:2311.17101.

[4] Lübeck, F., Bunne, C., Gut, G., del Castillo, J. S., Pelkmans, L., & Alvarez-Melis, D. (2022). Neural unbalanced optimal transport via cycle-consistent semi-couplings. arXiv preprint arXiv:2209.15621.
```

</details>


Review 主要点：
- 方法动机好，dual dynamic formulation / stochastic control 重写清楚。
- generative modeling 实验看起来不错。
- Section 4.1 方程太多，presentation 可改。
- loss 中 relaxed constraints 是否能归零不清楚。
- closed-form claim 可能错误，引用 [2]。
- generative modeling 缺相关 UOT baseline。
- outlier robustness 没测。
- Figure 3 legend 太小。
- Jordan et al. citation 不合适。

Qwen 覆盖：
- 大部分内容被抓到：motivation、novelty、problem setup、technical correctness、baseline、data、writing、figures、citation。
- 噪音：`Fit to Venue` 用了正面 motivation evidence，明显错；`Ethics` 和 `Societal` 是空 evidence。

判断：recall 中高，但 precision 明显被空项和误标拉低。

### 10. Retinal-wave transformer visual self-organization

<details>
<summary>原始 review 全文</summary>

```text
This paper examines whether transformers can self-organize like newborn visual systems when trained on biologically inspired “prenatal” data. Specifically, the authors train Vision Transformers (ViT-CoT) on simulated retinal wave inputs using a temporally contrastive learning objective. They report that the trained models spontaneously develop three hallmarks of early visual organization: (1) edge sensitivity in early layers (2) shape sensitivity in later layers and (3) progressively larger receptive fields across depth. Control experiments using temporally scrambled inputs fail to produce these properties, leading the authors to conclude that temporal continuity in prenatal sensory experience is sufficient for the emergence of newborn-like visual structure.

While the framing is interesting, the main claims of the study seem overstated. It remains unclear what unique scientific or methodological insights arise specifically from using transformers instead of CNNs, beyond substituting architectures and adopting an existing temporal contrastive objective. The lack of downstream or out-of-domain evaluations makes it difficult to assess whether pretraining on retinal waves produces useful or generalizable representations. Training for 100 epochs (!) on a small, repetitive dataset diverges sharply from real prenatal conditions, and the model’s spatial resolution and foveal focus limit biological plausibility. The study seems to be an illustrative demonstration than quantitative progress toward understanding how brains self-organize.

1. he paper is well structured, and easy to follow from motivation through methods and results. The narrative is coherent, and the figures are well integrated with the text.
2. The plots and visualizations are clean, intuitive, and easy to interpret, which makes the main findings immediately accessible even to readers outside the specific subfield.
3. The idea itself is conceptually compelling and has the potential to inspire new directions at the intersection of neuroscience and machine learning.

1. The work closely mirrors the approach of [Ligeralde et al. (2024)], differing mainly in the substitution of CNNs with ViTs and the adoption of the ViT-CoT contrastive temporal loss from [Pandey et al.]. Several prior studies have already trained models on simulated retinal wave data, demonstrating the emergence of V1-like receptive fields. As a result, the scientific contribution here feels incremental (architecture substitution than fundamentally new idea or learning principle, or even a strong test)

2. The paper does not meaningfully compare the current results against other (prior) models trained on retinal activity (like Ligeralde et al., or ReWaRD). Is the claim that those models don't learn V1-like receptive fields? Not including the existing body of work within the evaluations of the current paper makes it unclear what conceptual advance is being claimed. 

3. The authors claim that “if transformers really do learn like brains, they should develop the same structure as newborn brains when trained on the same prenatal data.” But they end up training , training for *100 epochs* (!) seems biologically implausible. This seems contradictory to the core premise of the paper. A model of development should consider the developmental training trajectories as well!

5. The experiments use very low-resolution inputs, which raises concerns about whether the reported findings would hold at more realistic scales (e.g., 224×224 images). Alternative architectures such as [LightViT](https://arxiv.org/pdf/2207.05557) could be used because a) they don’t have convolutional layers and b) they support large image resolutions.

6. The receptive field experiments are restricted to the foveal region. However, receptive field size is known to vary with eccentricity (see [Freeman & Simoncelli, 2011](https://www.nature.com/articles/nn.2889), Fig. 1). Extending this analysis across eccentricities would provide a more comprehensive and biologically grounded evaluation.

7. By default, the ViT-CoT architecture (as implemented in the [  vit_pytorch  ](https://github.com/buildingamind/ViT-CoT/blob/097f83ed70814793f7b32a1beddeb3a4cbbc4625/requirements.txt#L19C1-L19C12) library used by [used by Pandey et al.](https://github.com/buildingamind/ViT-CoT/blob/097f83ed70814793f7b32a1beddeb3a4cbbc4625/models/vit_contrastive.py#L82), which the authors follow) takes the   [CLS]   token as the model’s output embedding by default (as seen [here](https://github.com/lucidrains/vit-pytorch/blob/cbf6723063df2aa89526f9482b1c9a64feef9cb0/vit_pytorch/vit.py#L83)). If this token is excluded when computing receptive fields, the analysis may no longer reflect the representations actually used for downstream processing. This discrepancy (using one token for functional output and another set for representational analysis) raises concerns about the validity and interpretability of the receptive field results.

1. What does using ViTs and the ViT-CoT loss reveal beyond Ligeralde et al. (2024)? Is there any new scientific insight here, or just an architectural substitution? Do the authors think Transformers are more biologically realistic than CNNs? Please clarify the core claims better. 

2. Why are prior models trained on retinal activity (Ligeralde et al., ReWaRD) not compared during evaluation? Do those models fail to show the same effects claimed in the study?

3. How is training for 100 epochs on a small, repeating dataset biologically plausible? Would a single-pass or variable-input setup yield the same outcomes?

4. Do the reported trends (edge → shape → hierarchy) hold at higher image resolutions (e.g., 224×224)? Why not test this with transformer variants like LightViT that can handle larger inputs?

5. Since receptive field size varies with eccentricity, have the authors tested whether similar scaling trends emerge beyond the foveal region?

6. Why does the receptive field analysis use patch tokens instead of the [CLS] token that defines the model’s output? Does this mismatch affect the validity of the results?
```

</details>


Review 主要点：
- framing 有趣。
- 贡献偏 incremental，更像 architecture substitution。
- transformer 是否提供独特 insight 不清楚。
- claim 过强：不能说 transformer really learn like brains。
- 100 epochs 小重复数据与真实 prenatal condition 不符。
- 没和 prior retinal activity models 比。
- 缺 downstream / OOD evaluation。
- 224x224 / LightViT 等更高分辨率泛化没测。
- receptive field analysis 用 patch tokens 而不是 CLS。
- 写作结构好，图清楚。

Qwen 覆盖：
- 上述点基本全部被覆盖到 `Originality`, `Fit`, `Problem Setup`, `Technical Correctness`, `Experimental Setup`, `Baselines`, `Data`, `Metrics`, `Ablation`, `OOD`, `Reproducibility`, `Writing`, `Figures`, `Related Work`。

判断：重要点 recall 很高；噪音主要来自多个 aspect 其实对应同一批 baseline / data / protocol criticism。

## 结论

这 10 条足以说明：Qwen 的优势不是 precision，而是把 review 里的主干批评和表扬几乎都“捞上来”了。它的问题是：

- 同一个证据会被分到多个 aspect；
- 有些 aspect 标签不准确；
- 少量 aspect 为空 evidence；
- 会把边缘信息也抽出来，所以数量膨胀。

所以图里的判断可以更精确地写成：Qwen 是 high-recall / noisy extractor，适合做候选池；后面需要用更强模型或规则做去重、过滤和 label 校正。
