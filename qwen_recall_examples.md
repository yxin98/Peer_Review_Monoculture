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

<!-- BEGIN GPT_MAIN_MINI_EXTENSION -->

## GPT main / GPT mini 对照扩展

数据源：`.homogeneous/closed_api_sample_eval_short/closed_api_sample_results.tsv`

口径：这一节使用另一组 10 条 hard cases，对同一条 review 同时比较 `Qwen`、`gpt-5.5 main` 和 `gpt-5.4-mini` 的 aspect mining 结果。人工判断仍然是快速审计，不是正式双人标注；这里的“准”主要表示 aspect + stance + evidence 是否被 review 原文明确支持。

### 总览

| 模型 | 抽取总数 | 人工判准 | 粗略 precision | 风格判断 |
|---|---:|---:|---:|---|
| Qwen | 132 | 83 / 132 | 62.9% | 高 recall，但 over-label 和误标明显 |
| GPT main (`gpt-5.5`) | 103 | 100 / 103 | 97.1% | 覆盖和准确率都最高，但成本高 |
| GPT mini (`gpt-5.4-mini`) | 68 | 63 / 68 | 92.6% | 很保守，precision 高，但漏掉不少细粒度点 |

### token / cost 统计

| 模型 | 平均 input tokens / review | 平均 output tokens / review | 平均 total tokens / review | 平均成本 / review | 估计成本 / 3-review paper |
|---|---:|---:|---:|---:|---:|
| GPT main (`gpt-5.5`) | 2568.4 | 3434.2 | 6002.6 | $0.03755 | $0.11266 |
| GPT mini (`gpt-5.4-mini`) | 2588.9 | 711.3 | 3300.2 | $0.00207 | $0.00621 |

### 逐条概览

| # | Year | Paper / Review | Qwen 判准 | GPT main 判准 | GPT mini 判准 | 明显问题 |
|---:|---:|---|---:|---:|---:|---|
| 1 | 2023 | `bNt7oajl2a` / `YE2hJRcjXS` | 5 / 17 | 7 / 7 | 6 / 6 | Qwen 明显 over-label；main 和 mini 都更干净，mini 少一个 Data/Dataset。 |
| 2 | 2025 | `5o0ZvYzh6B` / `NYEuDCNjso` | 9 / 14 | 11 / 11 | 4 / 6 | main 覆盖最完整；mini 漏掉数据、效率、ablation 等；Qwen 有 Ethics/Societal/Reproducibility 误标。 |
| 3 | 2023 | `fZZ4ubttru` / `UPEo4w5YPC` | 9 / 13 | 10 / 10 | 7 / 7 | main 覆盖完整；mini 高精度但漏掉 data/metrics/statistical；Qwen 有 Fit/Technical Correctness 牵强。 |
| 4 | 2023 | `RUgBoMu0ad` / `T96Tt4iKI6` | 9 / 13 | 11 / 11 | 6 / 8 | main 最稳；mini 把一些正面 baseline/ablation evidence 标成 negative；Qwen 覆盖好但有 Figures/Efficiency 错位。 |
| 5 | 2021 | `JHXjK94yH-y` / `u49Ua9bS1Hr` | 7 / 13 | 12 / 12 | 7 / 7 | main 覆盖完整；mini 主干准确但漏 statistical/figures/writing；Qwen 把 weak reject 当 Venue、把测试环境当 Technical。 |
| 6 | 2025 | `Nyjvjgh6jW` / `RQ413lRyIJ` | 9 / 13 | 10 / 11 | 7 / 7 | main 和 mini 都准；main 覆盖更多；Qwen 有一条 Related Work 幻觉证据。 |
| 7 | 2021 | `fGEoHDk0C` / `BrRMyeORxH3` | 7 / 13 | 9 / 9 | 6 / 6 | main 覆盖最完整；mini 精准但漏 efficiency/baseline/technical novelty；Qwen Venue/Related Work/Reproducibility 误标。 |
| 8 | 2024 | `KfkmwYQXWh` / `fE19txHpeO` | 8 / 12 | 10 / 11 | 7 / 7 | main 捕捉 societal/figures/OOD 等细节；mini 干净但漏 technical novelty/societal；Qwen 把正面贡献错标为负面 Fit/Technical。 |
| 9 | 2024 | `FK6T0U4Mg1` / `XhV3jyK4cq` | 11 / 12 | 8 / 9 | 7 / 7 | 三者都不错；main 的 Distribution Shift 略宽；mini 漏 positive motivation/technical correctness 等；Qwen 只有 Data/Dataset 明显错。 |
| 10 | 2025 | `44Pc9erEIV` / `8ry7XWmVdr` | 9 / 12 | 12 / 12 | 6 / 7 | main 覆盖非常完整；mini 漏 technical novelty/statistical/problem setup；Qwen Ethics/Fit 有误。 |

粗略结论：main 相比 mini 多抽出约 50% 的 aspect，而且大部分新增 aspect 是有效的；mini 的优势是便宜且干净，但容易漏掉 `Statistical Evidence`、`Hyperparameter / Seed Sensitivity`、`Problem Setup Validity`、`Data / Dataset Appropriateness` 等细粒度标签。

## 具体样例：GPT main / GPT mini

### 1. Inductive reasoning in LLMs

Paper / Review：`bNt7oajl2a` / `YE2hJRcjXS`，Year：2023

<details>
<summary>原始 review 全文</summary>

```text
The paper explores the inductive reasoning capabilities of large language models (LLMs) through iterative hypothesis refinement. The key ideas are:- Inductive reasoning involves proposing hypotheses to explain observations, selecting the best hypothesis, and refining it based on new examples. This process mirrorshuman inductive reasoning.- The authors test LLMs on this through:    1. Using the LLM to propose rule hypotheses based on examples    2. Testing the rules using symbolic interpreters or LLMs as rule appliers on new examples    3. Providing feedback to the LLM to further refine the rules- Experiments on 4 datasets show LLMs are phenomenal at proposing plausible hypotheses when combined with symbolic interpreters. Iterative refinement significantly improvesperformance.- However, LLMs display counter-intuitive inductive behaviors compared to humans:    - They struggle to apply their own proposed rules    - They are brittle to minor perturbations in examples    - Their induced rules differ in content and form from human-proposed rules- Well motivated, clear and flows well. I really enjoyed reading the paper.- The paper tackles an important problem in reasoning, reasoning inductively by proposing hypotheses.- The domains are well defined and the content is diverse.- The human experiments are insightful - comparing induced rules reveals qualitative gaps between LLMs and human reasoning.- The paper makes an important contribution in carefully evaluating both strengths and weaknesses of LLMs for inductive reasoning.- The analysis is thorough, spanning different models, datasets, and evaluations.- The limitations, scope and results are clearly defined and discussed.Overall, this is a clearly written, rigorous, and impactful study that advances our understanding of inductive reasoning in LLMs. The paradoxical findings are intriguing and point to promising future directions.- An analysis of the complexity of the rules used to generate the data would be interesting. Comparing the complexity of the hypothesis across tasks and domains might give some insight into the model performance.- Similarly, the complexity of the human induced and LLM induced rules might be interesting to analyze.- How were the number of examples seen by the model chosen across domains? What is the minimum number of examples needed to learn a rule?- An open source model would make the evaluations more comprehensive.- A separate evaluation for LLMs as symbolic interpreters of rules would help tease apart the rule-proposing / application componenets more. More on complexity: LMs might be bad appliers of complex rules.- Can LLMs apply rules induced by humans?- Is there a change in the types of rules induced if the prompt is changed to encourage communication (since this was what humans seemed to do)? Change prompt to emphasize communication?- MiniAC→MiniARC: 4.3 para1 line 3I have specified the questions/ suggestions in the weaknesses section.
```

</details>

Review 主要点：
- 动机和问题重要，写作清楚。
- LLM 能提出假设，但规则应用、扰动鲁棒性和人类规则差异仍需分析。
- 需要 complexity / component attribution / open-source model / prompt change 等补充实验。

Qwen 覆盖（原标注）：

- `Motivation / Problem Framing` (positive): The paper tackles an important problem in reasoning, reasoning inductively by proposing hypotheses.
- `Originality / Novelty` (positive): The paper makes an important contribution in carefully evaluating both strengths and weaknesses of LLMs for inductive reasoning.
- `Fit to Venue / Scope` (positive): Overall, this is a clearly written, rigorous, and impactful study that advances our understanding of inductive reasoning in LLMs.
- `Problem Setup Validity` (positive): The domains are well defined and the content is diverse.
- `Technical Correctness` (negative): An analysis of the complexity of the rules used to generate the data would be interesting.
- `Experimental Setup & Protocol` (negative): How were the number of examples seen by the model chosen across domains? What is the minimum number of examples needed to learn a rule?
- `Metrics & Evaluation Criteria` (positive): The analysis is thorough, spanning different models, datasets, and evaluations.
- `Statistical Evidence` (positive): The limitations, scope and results are clearly defined and discussed.
- `Ablation & Attribution` (negative): Comparing the complexity of the hypothesis across tasks and domains might give some insight into the model performance.
- `Hyperparameter / Seed Sensitivity` (negative): What is the minimum number of examples needed to learn a rule?
- `Interpretation of Results` (positive): The human experiments are insightful - comparing induced rules reveals qualitative gaps between LLMs and human reasoning.
- `Reproducibility & Implementation` (negative): An open source model would make the evaluations more comprehensive.
- `Writing Clarity & Organization` (positive): Well motivated, clear and flows well. I really enjoyed reading the paper.
- `Figures / Tables & Visual Presentation` (positive): The paper is well motivated, clear and flows well.
- `Related Work Positioning & Citations` (positive): The paper makes an important contribution in carefully evaluating both strengths and weaknesses of LLMs for inductive reasoning.
- `Ethics / Safety / Misuse` (positive): The paradoxical findings are intriguing and point to promising future directions.
- `Societal / Broader Impacts` (positive): The paradoxical findings are intriguing and point to promising future directions.

GPT main 覆盖：

- `Motivation / Problem Framing` (positive): Iterative refinement significantly improvesperformance.- However, LLMs display counter-intuitive inductive behaviors compared to humans:    - They struggle to apply their own proposed rules    - They are brittle to minor...
- `Originality / Novelty` (positive): I really enjoyed reading the paper.- The paper tackles an important problem in reasoning, reasoning inductively by proposing hypotheses.- The domains are well defined and the content is diverse.- The human experiments ar...
- `Data / Dataset Appropriateness` (positive): I really enjoyed reading the paper.- The paper tackles an important problem in reasoning, reasoning inductively by proposing hypotheses.- The domains are well defined and the content is diverse.- The human experiments ar...
- `Writing Clarity & Organization` (positive): Iterative refinement significantly improvesperformance.- However, LLMs display counter-intuitive inductive behaviors compared to humans:    - They struggle to apply their own proposed rules    - They are brittle to minor...
- `Experimental Setup & Protocol` (negative): Comparing the complexity of the hypothesis across tasks and domains might give some insight into the model performance.- Similarly, the complexity of the human induced and LLM induced rules might be interesting to analyz...
- `Ablation & Attribution` (negative): What is the minimum number of examples needed to learn a rule?- An open source model would make the evaluations more comprehensive.- A separate evaluation for LLMs as symbolic interpreters of rules would help tease apart...
- `Interpretation of Results` (negative): The paradoxical findings are intriguing and point to promising future directions.- An analysis of the complexity of the rules used to generate the data would be interesting.

GPT mini 覆盖：

- `Writing Clarity & Organization` (positive): Iterative refinement significantly improvesperformance.- However, LLMs display counter-intuitive inductive behaviors compared to humans:    - They struggle to apply their own proposed rules    - They are brittle to minor...
- `Motivation / Problem Framing` (positive): I really enjoyed reading the paper.- The paper tackles an important problem in reasoning, reasoning inductively by proposing hypotheses.- The domains are well defined and the content is diverse.- The human experiments ar...
- `Problem Setup Validity` (positive): I really enjoyed reading the paper.- The paper tackles an important problem in reasoning, reasoning inductively by proposing hypotheses.- The domains are well defined and the content is diverse.- The human experiments ar...
- `Originality / Novelty` (positive): The paradoxical findings are intriguing and point to promising future directions.- An analysis of the complexity of the rules used to generate the data would be interesting.
- `Experimental Setup & Protocol` (negative): Comparing the complexity of the hypothesis across tasks and domains might give some insight into the model performance.- Similarly, the complexity of the human induced and LLM induced rules might be interesting to analyz...
- `Interpretation of Results` (positive): I really enjoyed reading the paper.- The paper tackles an important problem in reasoning, reasoning inductively by proposing hypotheses.- The domains are well defined and the content is diverse.- The human experiments ar...

判断：Qwen `5 / 17`，GPT main `7 / 7`，GPT mini `6 / 6`。Qwen 明显 over-label；main 和 mini 都更干净，mini 少一个 Data/Dataset。

### 2. Expressive speech-to-speech translation

Paper / Review：`5o0ZvYzh6B` / `NYEuDCNjso`，Year：2025

<details>
<summary>原始 review 全文</summary>

```text
The paper introduces UniSS, a single-stage autoregressive framework for expressive speech-to-speech translation (S2ST) that preserves speaker voice, emotion, and duration while achieving high translation fidelity. Built on the pre-trained Qwen2.5-1.5B-Instruct LLM, it uses a triple-tokenizer strategy (speaker, linguistic, semantic tokens) and cross-modal CoT prompting to transfer text translation capabilities to speech. Two modes (Quality and Performance) balance fidelity and efficiency. The authors release UniST, a 44.8k-hour Chinese-English expressive S2ST dataset. Experiments on CVSS-T and FLEURS show superior performance over baselines like SeamlessM4T, GPT-4o, and cascaded systems in metrics such as Speech-BLEU, prosody consistency, duration compliance, and speech quality. Subjective MOS evaluations confirm high emotion/speaker similarity and naturalness.1. The paper addresses an important problem in speech-to-speech translation: preserving the speaker's voice, emotional style, and prosody across languages. This is crucial for applications like multilingual communication or media dubbing. The motivation is clear, and the cross-modal CoT approach effectively aligns text-based LLM capabilities with speech in a single model. This method is innovative and necessary, as ablations show that removing CoT leads to major drops in performance.2. The authors release UniST, a 44.8k-hour dataset for expressive S2ST, which tackles the key issue of limited paired data with style preservation. The creation pipeline is well-documented, making it valuable for the research community.3. The experiments cover a broad set of metrics, including semantic and acoustic part. Baselines are varied, spanning cascaded systems and end-to-end models, ensuring robust comparisons.4. UniSS outperforms baselines on most metrics, such as emotion similarity and duration matching. The demopage also illustrates the model's success in maintaining expressive qualities.5. The paper is well-structured and readable, with clear descriptions of the architecture, training strategy, and ablations that validate the approach.1. The novelty is limited. The model's strength in maintaining speaker voice, emotion, and prosody largely relies on pre-existing components, such as the BiCodec tokenizer for speaker representations and SparkTTS for synthesizing expressive data. UniSS itself mainly integrates these by organizing a multiple token sequence then inputing it into a LLM, reducing its core innovation and novelty.2. The Single-Stage claim is misleading.  While positioned as a streamlined single-stage model to avoid cascaded errors and latency, the Quality mode generates intermediate source text (T_src) and target text (T_tgt) before speech tokens, mirroring the sequential steps of a traditional 3-stage pipeline (ASR → MT → TTS). This undermines the claimed advantages and could lead to similar error accumulations and delays.3. Training and evaluations are centered on English-Chinese pairs. Besides, the use of GLM tokenizer and SparkTTS also constrains the method for applying on other languages. This raises questions about scalability to diverse languages, accents, or noisy real-world scenarios, where data scarcity for expressiveness could amplify issues.4. A significant issue is the unfair setting in evaluations, particularly for translation accuracy (BLEU). The UniST training data uses high-quality translations from the large Qwen2.5-72B model, while the 3-stage cascaded baseline relies on the much smaller pretrained NLLB-600M for machine translation. Why not use Qwen-2.5-1.5B-Instruct LLM in the cascaded system?5. The framework's heavy reliance on text-based elements. For example, CoT prompting with intermediate transcripts makes it unsuitable for unwritten or low-resource languages without scripts. This contradicts goals in textless S2ST research and should be highlighted as a key limitation, especially given the focus on expressive translation.1. To make a fair comparison, it will be better if you test another cascaded baseline that uses the same Qwen-2.5-1.5B-Instruct model for MT and the same SparkTTS model for TTS. Besides, consider training the baselines on the UniST dataset. This would show if the UniSS framework is truly better, or if it just benefited from better components and training data.2. How does the cross-modal CoT prompting specifically bridge text and speech modalities? Provide some studies of intermediate outputs (e.g., T_src, T_tgt) to explain whether UniSS addresses error propagation problems.3. The motivation emphasizes unifying expressiveness, but much relies on existing tools (BiCodec, SparkTTS). What novel insights does UniSS offer for LLM-based S2ST, and how does it differ from prior CoT adaptations in multimodal tasks?4. For training strategy, what is the individual contribution of each task to overall performance? Could you add ablations removing or weighting specific tasks to quantify their effects?5. Since UniST is fully a synthetic dataset generated by SparkTTS, is it unable to effectively capture word-level semantic prosody mapping or relevance in speech translation? For instance, the transfer of semantic nuances such as emphasized stress. It is recommended to provide corresponding analysis and discuss the potential limitations.
```

</details>

Review 主要点：
- S2ST preserving voice/emotion/prosody 问题重要，UniST 数据集有价值。
- novelty 受限，single-stage claim 有争议。
- 中英数据、合成数据、fair baseline、scalability/OOD 和 ablation 需要加强。

Qwen 覆盖（原标注）：

- `Motivation / Problem Framing` (positive): The paper addresses an important problem in speech-to-speech translation: preserving the speaker's voice, emotional style, and prosody across languages.
- `Originality / Novelty` (negative): The novelty is limited. The model's strength in maintaining speaker voice, emotion, and prosody largely relies on pre-existing components...
- `Fit to Venue / Scope` (negative): The 'Single-Stage' claim is misleading. While positioned as a streamlined single-stage model... mirroring the sequential steps of a traditional 3-stage pipeline
- `Technical Correctness` (negative): The 'Single-Stage' claim is misleading. While positioned as a streamlined single-stage model... mirroring the sequential steps of a traditional 3-stage pipeline
- `Data / Dataset Appropriateness` (negative): Training and evaluations are centered on English-Chinese pairs. Besides, the use of GLM tokenizer and SparkTTS also constrains the method for applying on other languages
- `Baselines & Fair Comparison` (negative): A significant issue is the unfair setting in evaluations, particularly for translation accuracy (BLEU). The UniST training data uses high-quality translations from the large Qwen2.5-72B model...
- `Ethics / Safety / Misuse` (negative): The framework's heavy reliance on text-based elements... contradicts goals in textless S2ST research and should be highlighted as a key limitation
- `Societal / Broader Impacts` (negative): The framework's heavy reliance on text-based elements... contradicts goals in textless S2ST research and should be highlighted as a key limitation
- `Technical Novelty` (positive): The cross-modal CoT approach effectively aligns text-based LLM capabilities with speech in a single model. This method is innovative and necessary
- `Writing Clarity & Organization` (positive): The paper is well-structured and readable, with clear descriptions of the architecture, training strategy, and ablations that validate the approach
- `Distribution Shift & Generalization (OOD)` (negative): This raises questions about scalability to diverse languages, accents, or noisy real-world scenarios, where data scarcity for expressiveness could amplify issues
- `Reproducibility & Implementation` (negative): The creation pipeline is well-documented, making it valuable for the research community
- `Efficiency & Scalability` (negative): The 'Single-Stage' claim is misleading. While positioned as a streamlined single-stage model to avoid cascaded errors and latency... could lead to similar error accumulations and delays
- `Figures / Tables & Visual Presentation` (positive): The demopage also illustrates the model's success in maintaining expressive qualities

GPT main 覆盖：

- `Motivation / Problem Framing` (positive): The paper addresses an important problem in speech-to-speech translation: preserving the speaker's voice, emotional style, and prosody across languages.
- `Originality / Novelty` (negative): The novelty is limited.
- `Metrics & Evaluation Criteria` (positive): The experiments cover a broad set of metrics, including semantic and acoustic part.
- `Baselines & Fair Comparison` (negative): A significant issue is the unfair setting in evaluations, particularly for translation accuracy (BLEU).
- `Interpretation of Results` (positive): UniSS outperforms baselines on most metrics, such as emotion similarity and duration matching.
- `Writing Clarity & Organization` (positive): The paper is well-structured and readable, with clear descriptions of the architecture, training strategy, and ablations that validate the approach.1.
- `Problem Setup Validity` (negative): The Single-Stage claim is misleading.
- `Distribution Shift & Generalization (OOD)` (negative): Training and evaluations are centered on English-Chinese pairs.
- `Efficiency & Scalability` (negative): While positioned as a streamlined single-stage model to avoid cascaded errors and latency, the Quality mode generates intermediate source text (T_src) and target text (T_tgt) before speech tokens, mirroring the sequentia...
- `Ablation & Attribution` (negative): For training strategy, what is the individual contribution of each task to overall performance?
- `Data / Dataset Appropriateness` (negative): Since UniST is fully a synthetic dataset generated by SparkTTS, is it unable to effectively capture word-level semantic prosody mapping or relevance in speech translation?

GPT mini 覆盖：

- `Motivation / Problem Framing` (positive): The paper addresses an important problem in speech-to-speech translation: preserving the speaker's voice, emotional style, and prosody across languages.
- `Originality / Novelty` (negative): The novelty is limited.
- `Experimental Setup & Protocol` (negative): The experiments cover a broad set of metrics, including semantic and acoustic part.
- `Baselines & Fair Comparison` (negative): The experiments cover a broad set of metrics, including semantic and acoustic part.
- `Distribution Shift & Generalization (OOD)` (negative): This raises questions about scalability to diverse languages, accents, or noisy real-world scenarios, where data scarcity for expressiveness could amplify issues.4.
- `Writing Clarity & Organization` (positive): The paper is well-structured and readable, with clear descriptions of the architecture, training strategy, and ablations that validate the approach.1.

判断：Qwen `9 / 14`，GPT main `11 / 11`，GPT mini `4 / 6`。main 覆盖最完整；mini 漏掉数据、效率、ablation 等；Qwen 有 Ethics/Societal/Reproducibility 误标。

### 3. GenBot robotic skill generation

Paper / Review：`fZZ4ubttru` / `UPEo4w5YPC`，Year：2023

<details>
<summary>原始 review 全文</summary>

```text
The paper introduces GenBot, a generative robotic agent designed to automatically learn a variety of robotic skills on a large scale via generative simulation.GenBot utilizes advancements in foundational and generative models. Instead of directly employing or adapting these models to formulate policies or specific actions, the authors suggest a generative approach. This approach employs the models to automatically generate diversified tasks, scenes, and training supervision. The goal is to enhance robotic skill learning with minimal human intervention.GenBot follows a propose-generate-learn cycle. Initially, the agent suggests intriguing tasks and skills. Following that, it generates simulation environments, populating them with relevant objects and assets in the appropriate spatial configurations. After obtaining all the required information for the proposed task, including scene components, GenBot proceeds with the actual skill learning.The contributions of this paper go as follows.- The paper introduces GenBot, a robotic agent that automates the process of task and environment generation and subsequently learns skills. This framework potentially reduces the need for human intervention in the process of creating simulation tasks.- A figure in the paper showcases 25 example tasks generated by GenBot and the corresponding skills it learned, highlighting the diversity and applicability of the system.Overall, this paper demonstrates that the entire pipeline—from creating tasks to learning skills—can potentially be automated by large models. While a lot of details are still missing, I commend the quality of this work, especially considering the engineering efforts involved.Specifically, the strengths of this paper include:- The paper introduces GenBot as an automated pipeline that can be endlessly queried to generate a continuous stream of skills for diverse tasks. This automation is a significant strength as it reduces human intervention and can potentially scale up robotic skill learning.- Task diversity is essential for generalizable robotic skill learning. If GenBot can produce a diverse set of tasks and learn corresponding skills, it signifies a robust and versatile system.## Major### **Task diversity**I am concerned regarding the diversity of the generated tasks. With tasks proposed by LLMs and only qualitative examples provided, it's challenging for readers to gauge the true diversity of these tasks. Specifically:- How many semantically distinct tasks are generated? By semantically distinct, I refer to tasks that are fundamentally different. For instance, opening a cabinet and lifting a bucket are semantically distinct, whereas walking forward and walking backward are not.- What is the range of diversity in scene configurations? Upon reviewing the prompts, it seems that certain elements, like a table, have fixed poses and heights. If this is a recurring theme, then scene configuration diversity appears limited.### **Task verification**The construction of tasks in simulation typically requires validation to ensure correct implementation. This involves examining success conditions, initial state distributions, physical parameters, and more. However, the paper lacks a systematic method for this crucial verification, especially given the automation of task creation. Mistakes at any stage could result in flawed tasks. Specifically:- What percentage of the tasks can be successfully solved? How does this compare to the total number of generated tasks?- Are trivial tasks, such as picking up a block when given the grasp action primitive, filtered out?### **Use of LLMs**While the paper demonstrates the potential for automating the entire pipeline, from task creation to skill learning, using large models, the necessity of LLMs is questionable. Could simple heuristics or random placements of objects yield similar results? Given the extensive prompting involved with GenBot, it's unclear if it genuinely produces more diverse tasks with reduced human efforts.### **Missing details**Numerous details are absent from the paper. Refer to the Questions section for more questions.### **Limited quantitative results**The majority of the results are qualitative, which lacks depth for readers. Additionally, the paper's comparison of task diversity to other benchmarks based solely on task descriptions is less than persuasive.## Minor- Object Assets: Currently, the paper relies heavily on PartNetMobility and RLBench for task-relevant objects, which may restrict task diversity. Although the paper suggests using Midjourney + Zero123 for additional 3D assets, this pipeline lacks detailed elaboration.- Lack of Open-Source Code: As of now, the paper hasn't released its code. Furthermore, the underlying simulation framework, Genesis, remains private.- Regarding Task Proposal:- How does the system handle incompatibilities between the robot and the object? For instance, if the robot is a dog and the object is a cabinet, what would the proposed task be?- In scenarios involving non-articulated objects, if the generated tasks aren't specifically tied to the sampled object, how does the sampled object influence the task?- Regarding Scene Generation:- Could you provide a more detailed explanation of the MidJourney + Zero123 pipeline?- What is the precise output format from the LLMs? How is this output imported into a simulator to construct a scene?- How does the system manage situations where the scene results in an unsolvable task? For example, if the task is to open a cabinet but the cabinet is positioned out of the robot arm's reach.- How are potential collisions in the initial scene configuration addressed?- Is the initial state of the scene fixed, or is it sampled from a distribution?- How does the system generate physical parameters other than size, such as friction?- Regarding Training Supervision Generation:- How reliable is the reward generated by the LLM? Are there instances where it may not align with the intended goal?- How does the system define the success conditions for a task?
```

</details>

Review 主要点：
- GenBot 自动生成任务/场景/监督并学习技能，有新意。
- 任务多样性和成功率缺少量化验证。
- LLM 必要性、baseline、PartNet/RLBench 依赖、代码/Genesis 私有等是主要问题。

Qwen 覆盖（原标注）：

- `Originality / Novelty` (positive): The paper introduces GenBot as an automated pipeline that can be endlessly queried to generate a continuous stream of skills for diverse tasks.
- `Technical Novelty` (positive): The paper introduces GenBot, a robotic agent that automates the process of task and environment generation and subsequently learns skills.
- `Fit to Venue / Scope` (negative): While a lot of details are still missing, I commend the quality of this work, especially considering the engineering efforts involved.
- `Problem Setup Validity` (negative): I am concerned regarding the diversity of the generated tasks. With tasks proposed by LLMs and only qualitative examples provided, it's challenging for readers to gauge the true diversity of
- `Distribution Shift & Generalization (OOD)` (negative): Task diversity is essential for generalizable robotic skill learning. If GenBot can produce a diverse set of tasks and learn corresponding skills, it signifies a robust and versatile system.
- `Technical Correctness` (negative): The necessity of LLMs is questionable. Could simple heuristics or random placements of objects yield similar results?
- `Reproducibility & Implementation` (negative): The paper hasn't released its code. Furthermore, the underlying simulation framework, "Genesis," remains private.
- `Experimental Setup & Protocol` (negative): What percentage of the tasks can be successfully solved? How does this compare to the total number of generated tasks?
- `Baselines & Fair Comparison` (negative): The paper's comparison of task diversity to other benchmarks based solely on task descriptions is less than persuasive.
- `Data / Dataset Appropriateness` (negative): Currently, the paper relies heavily on PartNetMobility and RLBench for task-relevant objects, which may restrict task diversity.
- `Metrics & Evaluation Criteria` (negative): The majority of the results are qualitative, which lacks depth for readers.
- `Statistical Evidence` (negative): The paper's comparison of task diversity to other benchmarks based solely on task descriptions is less than persuasive.
- `Ablation & Attribution` (negative): What percentage of the tasks can be successfully solved? How does this compare to the total number of generated tasks?

GPT main 覆盖：

- `Originality / Novelty` (positive): While a lot of details are still missing, I commend the quality of this work, especially considering the engineering efforts involved.Specifically, the strengths of this paper include:- The paper introduces GenBot as an...
- `Efficiency & Scalability` (positive): While a lot of details are still missing, I commend the quality of this work, especially considering the engineering efforts involved.Specifically, the strengths of this paper include:- The paper introduces GenBot as an...
- `Figures / Tables & Visual Presentation` (positive): This framework potentially reduces the need for human intervention in the process of creating simulation tasks.- A figure in the paper showcases 25 example tasks generated by GenBot and the corresponding skills it learne...
- `Experimental Setup & Protocol` (negative): With tasks proposed by LLMs and only qualitative examples provided, it's challenging for readers to gauge the true diversity of these tasks.
- `Problem Setup Validity` (negative): However, the paper lacks a systematic method for this crucial verification, especially given the automation of task creation.
- `Ablation & Attribution` (negative): How does this compare to the total number of generated tasks?- Are trivial tasks, such as picking up a block when given the grasp action primitive, filtered out?### **Use of LLMs**While the paper demonstrates the potenti...
- `Metrics & Evaluation Criteria` (negative): Refer to the Questions section for more questions.### **Limited quantitative results**The majority of the results are qualitative, which lacks depth for readers.
- `Baselines & Fair Comparison` (negative): Could simple heuristics or random placements of objects yield similar results?
- `Data / Dataset Appropriateness` (negative): Additionally, the paper's comparison of task diversity to other benchmarks based solely on task descriptions is less than persuasive.## Minor- Object Assets: Currently, the paper relies heavily on PartNetMobility and RLB...
- `Reproducibility & Implementation` (negative): Given the extensive prompting involved with GenBot, it's unclear if it genuinely produces more diverse tasks with reduced human efforts.### **Missing details**Numerous details are absent from the paper.

GPT mini 覆盖：

- `Originality / Novelty` (positive): The paper introduces GenBot, a generative robotic agent designed to automatically learn a variety of robotic skills on a large scale via generative simulation.GenBot utilizes advancements in foundational and generative m...
- `Figures / Tables & Visual Presentation` (positive): This framework potentially reduces the need for human intervention in the process of creating simulation tasks.- A figure in the paper showcases 25 example tasks generated by GenBot and the corresponding skills it learne...
- `Motivation / Problem Framing` (positive): The goal is to enhance robotic skill learning with minimal human intervention.GenBot follows a propose-generate-learn cycle.
- `Experimental Setup & Protocol` (negative): Refer to the Questions section for more questions.### **Limited quantitative results**The majority of the results are qualitative, which lacks depth for readers.
- `Reproducibility & Implementation` (negative): While a lot of details are still missing, I commend the quality of this work, especially considering the engineering efforts involved.Specifically, the strengths of this paper include:- The paper introduces GenBot as an...
- `Interpretation of Results` (negative): Refer to the Questions section for more questions.### **Limited quantitative results**The majority of the results are qualitative, which lacks depth for readers.
- `Baselines & Fair Comparison` (negative): Could simple heuristics or random placements of objects yield similar results?

判断：Qwen `9 / 13`，GPT main `10 / 10`，GPT mini `7 / 7`。main 覆盖完整；mini 高精度但漏掉 data/metrics/statistical；Qwen 有 Fit/Technical Correctness 牵强。

### 4. Hierarchical image classification

Paper / Review：`RUgBoMu0ad` / `T96Tt4iKI6`，Year：2023

<details>
<summary>原始 review 全文</summary>

```text
This paper proposes two techniques for improving hierarchical image classification: a training method and an inference method. The training approach provides better utilization of pre-trained models by adopting an image-text model (CLIP) and applying a contrastive loss based on the (fixed) label embeddings from the text encoder. The hierarchical contrastive loss comprises an independent sum over per-level contrastive losses. The inference procedure applies diffusion to iteratively propagate scores in the (undirected) graph defined by the taxonomy. Using the iNaturalist datasets (2018, 2021-mini), the training method is shown to obtain greatly improved results over simply fine-tuning the CLIP image encoder using existing losses. The inference algorithm is also demonstrated to further improve the results. The authors also propose a differentiable diffusion approach, which replaces the adjacency matrix with a learned matrix.1. The baseline methods were evaluated using the same pre-trained initialization (CLIP image encoder) and a large improvement is achieved (+8 points Average Precision).1. The ablative study in Table 3 shows the improvement in accuracy obtained by using the text embedding and the contrastive loss.1. The inference procedure was compared to other approaches using the same model in Table 5, and with different models in Table 6.1. Good use of hierarchical metrics.1. The methods are demonstrated on both balanced and imbalanced datasets.1. Overall, the ablative studies were well-constructed, and answered most of my queries about the method.I will use [1] to denote Valmadre (2022).1. What is hierarchical training with CE loss in the ablative study? (L294; also CE loss + Lxxxx distinct from Contrastive Loss + Lxxxx in Table 3) This needs to be explicitly defined.1. The proposed level-wise loss does not seem to produce consistent probabilities as defined in [1]; i.e. where the probability of an internal node is greater than or equal to the sum of its children.1. The level-wise loss might not apply as well in hierarchies that contain leaf nodes of different depths (I believe the iNaturalist taxonomy has a uniform depth of 7).1. The results in Table 4 lack sufficient significance to conclude that for metrics like AP, AC, and Leaf F1, comprehensive training across all levels (denoted as L123467) outperforms other configurations and consequently that these findings diverge from theprevailing belief that top-1 accuracy benchmarks align with hierarchical metric rankings. Most of these numbers seem about the same, with the possible exception of Leaf F1. (However, I agree that L67 and L7 are significantly better for R@xxC and Leaf Top1.)1. While the ablative study shows some important results, I would have liked to see further investigation into the importance of the image encoder. In particular, while the authors used CLIP pretraining for the baselines, the numbers are quite close to those of [1], which used standard ImageNet pretraining. I think it would be useful to highlight this in the paper (it shows that the method better leverages the pretrained model). Furthermore, since the label embeddings seem crucially important, it would be interesting to investigate whether the CLIP image encoder is even necessary by using ImageNet pretraining with the same label embeddings.1. It would be useful to generate the operating curves as in [1], to highlight whether the method achieves a better trade-off or simply dominates the other methods.1. No confidence intervals (error-bars).1. The diffusion procedure was not evaluated on models that were trained using the parameter sharing softmax and soft-max-margin losses in Table 6.1. It's inaccurate to characterize the *inference* procedure of [1] as bottom-up (e.g. Table 5): it returns the most-informative ($\approx$ deepest) label that exceeds a confidence threshold. In fact, if the threshold is > 0.5 and the probabilities satisfy the tree constraint, then it is equivalent to greedy top-down (since there can only be one path with confidence > 0.5). A better example of bottom-up inference would be Davis et al. Hierarchical Semantic Labeling with Adaptive Confidence, where the inference algorithm starts at the argmax leaf node and proceeds upwards.1. Several details are unclear, see questions.Minor:1. It seems as though the Softmargin and Descendant softmax rows might be interchanged between Table 1 and Table 2? The results of [1] showed the softmargin to perform consistently better than descendant softmax, as in Table 2 but not in Table 1.1. In (1), it seems that one of the summations should be over all leaf nodes, rather than $L(y)$.1. The parameter-sharing softmax of Salakhutdinov et al. (2011), also considered in [1], is effectively a hybrid method: logits are obtained in a top-down fashion, normalization is performed at the leaf nodes, and then probabilities are obtained bottom-up.Suggestions:1. I would use terminology like graph diffusion at the start of the paper to make it clear that you're not considering generative diffusion (DDPMs, stable diffusion, etc.).1. down-top should be bottom-up, unless you mean something specific by this?1. Are the summations over $i$ and $j$ in (2) over all labels in level $l$ (in which case, it should be $N_l$ rather than $N$?), or all labels at all levels (in which case, are the ancestor labels excluded?)?1. How would the loss in (2) be extended to taxonomies where not all leaf nodes occur at the same depth?1. Is the diffusion process applied to raw image-text similarities, or are the probabilities normalized; if so, are they normalized globally or per-level (as appears to be the case in the loss)?1. Which model was used to produce Table 5?1. What explains the difference between the results for Flat softmax in Table 2 (61.18 AP) and Table 6 (69.18 AP)?
```

</details>

Review 主要点：
- 同初始化 baseline、hierarchical metrics、balanced/imbalanced datasets 和 ablation 有正面评价。
- level-wise loss consistency、Table 4 significance、confidence intervals、diffusion evaluation 缺口是关键问题。
- 术语、定义和相关工作表述有若干清晰度/正确性问题。

Qwen 覆盖（原标注）：

- `Experimental Setup & Protocol` (positive): The ablative studies were well-constructed, and answered most of my queries about the method.
- `Technical Correctness` (negative): The proposed level-wise loss does not seem to produce consistent probabilities as defined in [1]; i.e. where the probability of an internal node is greater than or equal to the
- `Statistical Evidence` (negative): The results in Table 4 lack sufficient significance to conclude that "for metrics like AP, AC, and Leaf F1, comprehensive training across all levels (denoted as L123467) outperforms other configurations"...
- `Reproducibility & Implementation` (negative): The diffusion procedure was not evaluated on models that were trained using the "parameter sharing softmax" and "soft-max-margin" losses in Table 6.
- `Related Work Positioning & Citations` (negative): It's inaccurate to characterize the *inference* procedure of [1] as "bottom-up"...
- `Writing Clarity & Organization` (negative): Several details are unclear, see questions.
- `Figures / Tables & Visual Presentation` (positive): Good use of hierarchical metrics.
- `Baselines & Fair Comparison` (positive): The baseline methods were evaluated using the same pre-trained initialization (CLIP image encoder) and a large improvement is achieved (+8 points Average Precision).
- `Data / Dataset Appropriateness` (positive): The methods are demonstrated on both balanced and imbalanced datasets.
- `Efficiency & Scalability` (negative): The diffusion procedure was not evaluated on models that were trained using the "parameter sharing softmax" and "soft-max-margin" losses in Table 6.
- `Distribution Shift & Generalization (OOD)` (negative): The level-wise loss might not apply as well in hierarchies that contain leaf nodes of different depths...
- `Interpretation of Results` (negative): The results in Table 4 lack sufficient significance to conclude that "for metrics like AP, AC, and Leaf F1, comprehensive training across all levels (denoted as L123467) outperforms other configurations"...
- `Ablation & Attribution` (positive): The ablative study in Table 3 shows the improvement in accuracy obtained by using the text embedding and the contrastive loss.

GPT main 覆盖：

- `Baselines & Fair Comparison` (positive): The baseline methods were evaluated using the same pre-trained initialization (CLIP image encoder) and a large improvement is achieved (+8 points Average Precision).1.
- `Metrics & Evaluation Criteria` (positive): Good use of hierarchical metrics.1.
- `Data / Dataset Appropriateness` (positive): The methods are demonstrated on both balanced and imbalanced datasets.1.
- `Ablation & Attribution` (negative): Overall, the ablative studies were well-constructed, and answered most of my queries about the method.I will use [1] to denote Valmadre (2022).1.
- `Reproducibility & Implementation` (negative): (L294; also CE loss + Lxxxx distinct from Contrastive Loss + Lxxxx in Table 3) This needs to be explicitly defined.1.
- `Statistical Evidence` (negative): The results in Table 4 lack sufficient significance to conclude that for metrics like AP, AC, and Leaf F1, comprehensive training across all levels (denoted as L123467) outperforms other configurations and consequently t...
- `Distribution Shift & Generalization (OOD)` (negative): The level-wise loss might not apply as well in hierarchies that contain leaf nodes of different depths (I believe the iNaturalist taxonomy has a uniform depth of 7).1.
- `Experimental Setup & Protocol` (negative): The diffusion procedure was not evaluated on models that were trained using the parameter sharing softmax and soft-max-margin losses in Table 6.1.
- `Technical Correctness` (negative): It's inaccurate to characterize the *inference* procedure of [1] as bottom-up (e.g.
- `Problem Setup Validity` (negative): The proposed level-wise loss does not seem to produce consistent probabilities as defined in [1]; i.e.
- `Writing Clarity & Organization` (negative): I would use terminology like graph diffusion at the start of the paper to make it clear that you're not considering generative diffusion (DDPMs, stable diffusion, etc.).1.

GPT mini 覆盖：

- `Experimental Setup & Protocol` (negative): The methods are demonstrated on both balanced and imbalanced datasets.1.
- `Ablation & Attribution` (negative): The ablative study in Table 3 shows the improvement in accuracy obtained by using the text embedding and the contrastive loss.1.
- `Baselines & Fair Comparison` (negative): The baseline methods were evaluated using the same pre-trained initialization (CLIP image encoder) and a large improvement is achieved (+8 points Average Precision).1.
- `Metrics & Evaluation Criteria` (positive): Good use of hierarchical metrics.1.
- `Reproducibility & Implementation` (negative): Several details are unclear, see questions.Minor:1.
- `Technical Correctness` (negative): The proposed level-wise loss does not seem to produce consistent probabilities as defined in [1]; i.e.
- `Writing Clarity & Organization` (negative): Several details are unclear, see questions.Minor:1.
- `Related Work Positioning & Citations` (negative): It's inaccurate to characterize the *inference* procedure of [1] as bottom-up (e.g.

判断：Qwen `9 / 13`，GPT main `11 / 11`，GPT mini `6 / 8`。main 最稳；mini 把一些正面 baseline/ablation evidence 标成 negative；Qwen 覆盖好但有 Figures/Efficiency 错位。

### 5. Adversarial Surprise for unsupervised RL

Paper / Review：`JHXjK94yH-y` / `u49Ua9bS1Hr`，Year：2021

<details>
<summary>原始 review 全文</summary>

```text
This paper introduces Adversarial Surprise, a new approach for unsupervised reinforcement learning in stochastic BMDPs, where the goal is to explore an environment without rewards. The algorithm uses a single agent with two policies, an Explorer and a Controller, which switch during an episode with opposite rewards: to maximize and minimize surprise. The method is supported by a theoretical argument under the assumptions of the stochastic BMDP. When these are present in an environment, the empirical results are strong. The method is also tested in Atari and Doom. Overall this is a neat idea, related to but distinct from previous works. The problem setting of a stochastic block MDP (BMDP) is well motivated although not frequently encountered in RL. The strongest results come from a new custom environment in MiniGrid, which clearly motivates the switching mechanism to discover interesting behaviors and fully explore the environment. In other environments the results are less compelling: in Doom the AGAC baseline is not included, while the Atari experiments are hard to interpret due to the choice of the four games, which is not clear. While I like the paper, I am voting for weak reject primarily because of the reporting protocol, only showing the top 3 seeds. This is known to be bad practice and does not seem justified, at least without presenting full results in the Appendix. As with any review it is possible I missed something, in which case I can change my score to reflect this during the discussion.More Detailed Comments:1. One of the greatest strengths of this work is that is it well motivated, and thorough. The related work section for instance positions the paper effectively within the literature, which is surprisingly rare. The flip side of this, is that the specific setting considered, stochastic BMDPs, seems very specific. It would be great to have more examples of real world settings where this setting would be present.2. The MiniGrid experiment is a nice example of a setting where existing methods fail in stochastic environments, with a switch that allows AS to remove the stochasticity. Is it the case that the Explore agent can turn the stochasticity back on? How often does it do this?3. Why are the methods in Fig. 2b) and 2c) different? E.g. AGAC is in one but not the other. More of an aesthetic issue but it is confusing switching the colors for methods in plots that are side by side.4. The authors say ViZDoom environment (Kempka et al., 2016b), which was used by AGAC and SMiRL, *but then do not include AGAC in the Doom experiments.* Why?5. How were the four Atari games chosen? As far as I am aware, the common games used for exploration are Montezuma's Revenge and Pitfall, but these were not included. This makes the reader question the choice, for example if the method works best for these but would do equally poorly on a different set of games. While it isn't the perfect environment by any means, Montezuma's Revenge is a good benchmark because it has been predefined, so if a method does/doesn't work there it can serve as a litmus test.6. How does AS combine with rewards? All of the other methods (aside from ASP) are designed for settings where an extrinsic reward is available, and they use this to get their best results. I know unsupervised or self-supervised RL is currently a popular topic, but in many cases we may have a reward function. Indeed - the baselines compared against were not designed to work in the regime they were tested in.7. How do you choose k? I may have missed it but couldn't find it anywhere. The paper does mention that the ability to tune this per environment is a strength, but as a reviewer it is a concern that this may have led to the performance gains and actually the method could be very sensitive to this hyperparameter. I am thinking if k is less than the size of the room with the switch, Alice and Bob could take turns to turn it on/off and then stay in the same room forever.8. The authors should cite RIDE, AMIGo and BeBold, three recent works studying exploration in procedurally generated environments. Comparison against them would be a nice to have but not expected, since AGAC is included and it compares against them.  Minor Comments/Typos:* p6, reference Equation 5 but I think you mean Equation 4.* p6, after the AS formula (min max) it says BMPD rather than BMDP. Later in that sentence, induce→ induces.* Fig 2.c) has the methods twice on the legend.* P7 Minigrid should have a capital G.The method is elegant and well motivated, hence a desire to see it accepted despite question marks about the experimental results. In particular, the broader applicability may be limited given the gains are clearest in the setting specifically designed to satisfy the properties which motivated the method. To increase my score I would need clarification around the evaluation protocol, which is already known to be challenging in RL without selecting the top 3 seeds (while saying 5 seeds elsewhere). I would also be happy to increase my score if there are additional baselines (e.g. AGAC for Doom) or benchmark environments (e.g. additional Atari games/MiniGrid environments), clarification around hyperparameter choices or an effective demonstration of combining AS with an extrinsic reward. Overall I could increase multiple times if this is improved. 
```

</details>

Review 主要点：
- Adversarial Surprise idea neat，problem framing well motivated。
- top 3 seeds reporting protocol 是核心问题。
- Doom/Atari baselines、game choice、k sensitivity、broader applicability、figure/typo 都被提出。

Qwen 覆盖（原标注）：

- `Motivation / Problem Framing` (positive): One of the greatest strengths of this work is that it is well motivated, and thorough. The related work section for instance positions the paper effectively within the literature, which
- `Originality / Novelty` (positive): Overall this is a neat idea, related to but distinct from previous works.
- `Fit to Venue / Scope` (negative): I am voting for weak reject primarily because of the reporting protocol, only showing the top 3 seeds. This is known to be bad practice and does not seem justified,
- `Technical Correctness` (negative): The method is tested in Atari and Doom. Overall this is a neat idea, related to but distinct from previous works.
- `Experimental Setup & Protocol` (negative): The Atari experiments are hard to interpret due to the choice of the four games, which is not clear.
- `Baselines & Fair Comparison` (negative): Doom the AGAC baseline is not included, while the Atari experiments are hard to interpret due to the choice of the four games, which is not clear.
- `Data / Dataset Appropriateness` (negative): Why are the methods in Fig. 2b) and 2c) different? E.g. AGAC is in one but not the other.
- `Metrics & Evaluation Criteria` (negative): I am voting for weak reject primarily because of the reporting protocol, only showing the top 3 seeds. This is known to be bad practice and does not seem justified,
- `Statistical Evidence` (negative): I am voting for weak reject primarily because of the reporting protocol, only showing the top 3 seeds. This is known to be bad practice and does not seem justified,
- `Hyperparameter / Seed Sensitivity` (negative): How do you choose k? I may have missed it but couldn't find it anywhere. The paper does mention that the ability to tune this per environment is a strength,
- `Distribution Shift & Generalization (OOD)` (positive): The strongest results come from a new custom environment in MiniGrid, which clearly motivates the switching mechanism to discover interesting behaviors and fully explore the environment.
- `Interpretation of Results` (negative): The Atari experiments are hard to interpret due to the choice of the four games, which is not clear.
- `Reproducibility & Implementation` (negative): I am voting for weak reject primarily because of the reporting protocol, only showing the top 3 seeds. This is known to be bad practice and does not seem justified,

GPT main 覆盖：

- `Motivation / Problem Framing` (positive): One of the greatest strengths of this work is that is it well motivated, and thorough.
- `Originality / Novelty` (positive): Overall this is a neat idea, related to but distinct from previous works.
- `Experimental Setup & Protocol` (negative): While I like the paper, I am voting for weak reject primarily because of the reporting protocol, only showing the top 3 seeds.
- `Statistical Evidence` (negative): While I like the paper, I am voting for weak reject primarily because of the reporting protocol, only showing the top 3 seeds.
- `Baselines & Fair Comparison` (negative): In other environments the results are less compelling: in Doom the AGAC baseline is not included, while the Atari experiments are hard to interpret due to the choice of the four games, which is not clear.
- `Data / Dataset Appropriateness` (negative): In other environments the results are less compelling: in Doom the AGAC baseline is not included, while the Atari experiments are hard to interpret due to the choice of the four games, which is not clear.
- `Hyperparameter / Seed Sensitivity` (negative): How do you choose k?
- `Related Work Positioning & Citations` (negative): The related work section for instance positions the paper effectively within the literature, which is surprisingly rare.
- `Figures / Tables & Visual Presentation` (negative): More of an aesthetic issue but it is confusing switching the colors for methods in plots that are side by side.4.
- `Writing Clarity & Organization` (negative): Minor Comments/Typos:* p6, reference Equation 5 but I think you mean Equation 4.* p6, after the AS formula (min max) it says BMPD rather than BMDP.
- `Distribution Shift & Generalization (OOD)` (negative): It would be great to have more examples of real world settings where this setting would be present.2.
- `Interpretation of Results` (negative): In other environments the results are less compelling: in Doom the AGAC baseline is not included, while the Atari experiments are hard to interpret due to the choice of the four games, which is not clear.

GPT mini 覆盖：

- `Experimental Setup & Protocol` (negative): While I like the paper, I am voting for weak reject primarily because of the reporting protocol, only showing the top 3 seeds.
- `Baselines & Fair Comparison` (negative): In other environments the results are less compelling: in Doom the AGAC baseline is not included, while the Atari experiments are hard to interpret due to the choice of the four games, which is not clear.
- `Distribution Shift & Generalization (OOD)` (negative): In other environments the results are less compelling: in Doom the AGAC baseline is not included, while the Atari experiments are hard to interpret due to the choice of the four games, which is not clear.
- `Hyperparameter / Seed Sensitivity` (negative): I am thinking if k is less than the size of the room with the switch, Alice and Bob could take turns to turn it on/off and then stay in the same room forever.8.
- `Related Work Positioning & Citations` (negative): The related work section for instance positions the paper effectively within the literature, which is surprisingly rare.
- `Originality / Novelty` (positive): Overall this is a neat idea, related to but distinct from previous works.
- `Motivation / Problem Framing` (positive): The problem setting of a stochastic block MDP (BMDP) is well motivated although not frequently encountered in RL.

判断：Qwen `7 / 13`，GPT main `12 / 12`，GPT mini `7 / 7`。main 覆盖完整；mini 主干准确但漏 statistical/figures/writing；Qwen 把 weak reject 当 Venue、把测试环境当 Technical。

### 6. Goal-conditioned test-time training

Paper / Review：`Nyjvjgh6jW` / `RQ413lRyIJ`，Year：2025

<details>
<summary>原始 review 全文</summary>

```text
The paper proposes goal-conditioned test-time training (GC-TTT) for offline reinforcement learning. Instead of freezing a pre-trained goal-conditioned policy at inference, the method repeatedly fine-tunes it during evaluation on a small batch of goal-relevant, high-quality sub-trajectories drawn from the original offline dataset. Relevance is defined by proximity to the current state and optimality by an H-step return estimate using a learned critic; a critic-free variant uses reward returns on expert data. The updates are applied in a receding-horizon loop that resets weights every K steps, yielding consistent gains across OGBench loco-navigation and a manipulation task on top of GC-BC, GC-IQL, and SAW backbones. The paper further studies compute allocation at inference and shows that spending compute on GC-TTT outperforms simply scaling model size at matched inference FLOPs.* The core idea is simple, broadly applicable, and well-motivated by analogies to test-time adaptation in foundation models. The algorithmic design is clear: a principled data filter that combines state relevance with estimated return, plus a lightweight fine-tuning loop with periodic resets; the paper explains these choices and provides an ablation showing that both relevance and optimality are needed for the observed gains.* Empirically, the method consistently improves success rates across pointmaze, antmaze, humanoidmaze, and cubesingle when layered on GC-BC, GC-IQL, and SAW, sometimes converting weak pre-trained policies into strong ones with only a few gradient steps. The critic-free variant is a practical bonus for pure imitation settings with expert data. The compute analysis is thoughtful, reporting control frequency, profiling overheads, and showing that increasing TTT frequency often buys more than enlarging the backbone under matched FLOPs.* The approach assumes convenient access to the entire pre-training dataset at test time, plus fast retrieval by state proximity; the paper does not quantify memory and I/O costs or the latency of building and querying this index online.   * Several comparisons could be tighter. The compute comparison with model scaling relies on simplifying assumptions about FLOPs and may understate benefits of width scaling with better regularization; sensitivity analyses are limited. Some backbones are already near-saturated on certain tasks, and the absolute gains there are modest. Results use three seeds and fixed goals; it would help to include broader goal sets and confidence intervals or statistical tests. Finally, performance depends on critic quality and hyperparameters like K, N, and the percentile threshold; while there are ablations, guidance for robust default settings under distribution shift is limited.* How is state proximity computed in practice for high-dimensional observations and what indexing structure is used for fast retrieval at test time? Please report memory footprint, average query latency, and end-to-end wall-clock overhead per episode on your hardware.  * How sensitive is performance to the percentile threshold q and distance threshold, especially when relevant data are scarce or when the current state lies outside the support of D? Do you have a fallback for the no-data case beyond widening the threshold?  * Can you clarify the stability of the critic during test-time adaptation? Since the actor is updated but the critic guides data selection, is there drift that degrades the H-step estimate over repeated loops, and would periodic critic refresh help?  * In the compute study, could you include alternative baselines that also spend test-time compute, such as nearest-neighbor action retrieval, dynamic evaluation on behavior-cloned policies, or short-horizon planning with learned dynamics, matched for wall-clock and FLOPs?  * What happens if you also incorporate freshly collected transitions into the fine-tuning buffer, possibly with conservative weighting, so GC-TTT becomes a hybrid test-time online learner? Any early results or pitfalls you observed?
```

</details>

Review 主要点：
- GC-TTT 思路清楚，ablation 和 compute analysis 有正面评价。
- 需要全预训练数据 test-time 访问和快速检索，memory/I/O/latency 未量化。
- baselines、statistical tests、hyperparameter/OOD guidance 和 implementation details 需要补。

Qwen 覆盖（原标注）：

- `Fit to Venue / Scope` (positive): The core idea is simple, broadly applicable, and well-motivated by analogies to test-time adaptation in foundation models.
- `Technical Correctness` (positive): The algorithmic design is clear: a principled data filter that combines state relevance with estimated return, plus a lightweight fine-tuning loop with periodic resets; the paper explains these choices and
- `Reproducibility & Implementation` (negative): The approach assumes convenient access to the entire pre-training dataset at test time, plus fast retrieval by state proximity; the paper does not quantify memory and I/O costs or the
- `Experimental Setup & Protocol` (negative): Results use three seeds and fixed goals; it would help to include broader goal sets and confidence intervals or statistical tests.
- `Baselines & Fair Comparison` (negative): Several comparisons could be tighter. The compute comparison with model scaling relies on simplifying assumptions about FLOPs and may understate benefits of width scaling with better regularization; sensitivity analyses...
- `Data / Dataset Appropriateness` (negative): The approach assumes convenient access to the entire pre-training dataset at test time, plus fast retrieval by state proximity; the paper does not quantify memory and I/O costs or the
- `Metrics & Evaluation Criteria` (negative): Results use three seeds and fixed goals; it would help to include broader goal sets and confidence intervals or statistical tests.
- `Statistical Evidence` (negative): Results use three seeds and fixed goals; it would help to include broader goal sets and confidence intervals or statistical tests.
- `Hyperparameter / Seed Sensitivity` (negative): Performance depends on critic quality and hyperparameters like K, N, and the percentile threshold; while there are ablations, guidance for robust default settings under distribution shift is limited.
- `Distribution Shift & Generalization (OOD)` (negative): Performance depends on critic quality and hyperparameters like K, N, and the percentile threshold; while there are ablations, guidance for robust default settings under distribution shift is limited.
- `Related Work Positioning & Citations` (negative): The paper does not clearly position itself relative to prior work on test-time adaptation or offline reinforcement learning.
- `Efficiency & Scalability` (positive): The compute analysis is thoughtful, reporting control frequency, profiling overheads, and showing that increasing TTT frequency often buys more than enlarging the backbone under matched FLOPs.
- `Writing Clarity & Organization` (positive): The paper explains these choices and provides an ablation showing that both relevance and optimality are needed for the observed gains.

GPT main 覆盖：

- `Motivation / Problem Framing` (positive): The paper further studies compute allocation at inference and shows that spending compute on GC-TTT outperforms simply scaling model size at matched inference FLOPs.* The core idea is simple, broadly applicable, and well...
- `Writing Clarity & Organization` (positive): The algorithmic design is clear: a principled data filter that combines state relevance with estimated return, plus a lightweight fine-tuning loop with periodic resets; the paper explains these choices and provides an ab...
- `Ablation & Attribution` (positive): The algorithmic design is clear: a principled data filter that combines state relevance with estimated return, plus a lightweight fine-tuning loop with periodic resets; the paper explains these choices and provides an ab...
- `Interpretation of Results` (negative): The algorithmic design is clear: a principled data filter that combines state relevance with estimated return, plus a lightweight fine-tuning loop with periodic resets; the paper explains these choices and provides an ab...
- `Problem Setup Validity` (negative): The compute analysis is thoughtful, reporting control frequency, profiling overheads, and showing that increasing TTT frequency often buys more than enlarging the backbone under matched FLOPs.* The approach assumes conve...
- `Efficiency & Scalability` (negative): The compute analysis is thoughtful, reporting control frequency, profiling overheads, and showing that increasing TTT frequency often buys more than enlarging the backbone under matched FLOPs.* The approach assumes conve...
- `Baselines & Fair Comparison` (negative): * Several comparisons could be tighter.
- `Statistical Evidence` (negative): Results use three seeds and fixed goals; it would help to include broader goal sets and confidence intervals or statistical tests.
- `Hyperparameter / Seed Sensitivity` (negative): The compute comparison with model scaling relies on simplifying assumptions about FLOPs and may understate benefits of width scaling with better regularization; sensitivity analyses are limited.
- `Distribution Shift & Generalization (OOD)` (negative): Finally, performance depends on critic quality and hyperparameters like K, N, and the percentile threshold; while there are ablations, guidance for robust default settings under distribution shift is limited.* How is sta...
- `Reproducibility & Implementation` (negative): Finally, performance depends on critic quality and hyperparameters like K, N, and the percentile threshold; while there are ablations, guidance for robust default settings under distribution shift is limited.* How is sta...

GPT mini 覆盖：

- `Originality / Novelty` (positive): The paper further studies compute allocation at inference and shows that spending compute on GC-TTT outperforms simply scaling model size at matched inference FLOPs.* The core idea is simple, broadly applicable, and well...
- `Interpretation of Results` (positive): The algorithmic design is clear: a principled data filter that combines state relevance with estimated return, plus a lightweight fine-tuning loop with periodic resets; the paper explains these choices and provides an ab...
- `Efficiency & Scalability` (negative): The compute analysis is thoughtful, reporting control frequency, profiling overheads, and showing that increasing TTT frequency often buys more than enlarging the backbone under matched FLOPs.* The approach assumes conve...
- `Reproducibility & Implementation` (negative): Finally, performance depends on critic quality and hyperparameters like K, N, and the percentile threshold; while there are ablations, guidance for robust default settings under distribution shift is limited.* How is sta...
- `Experimental Setup & Protocol` (negative): * Several comparisons could be tighter.
- `Ablation & Attribution` (positive): The algorithmic design is clear: a principled data filter that combines state relevance with estimated return, plus a lightweight fine-tuning loop with periodic resets; the paper explains these choices and provides an ab...
- `Metrics & Evaluation Criteria` (negative): Results use three seeds and fixed goals; it would help to include broader goal sets and confidence intervals or statistical tests.

判断：Qwen `9 / 13`，GPT main `10 / 11`，GPT mini `7 / 7`。main 和 mini 都准；main 覆盖更多；Qwen 有一条 Related Work 幻觉证据。

### 7. DNN/PDE robustness framework

Paper / Review：`fGEoHDk0C` / `BrRMyeORxH3`，Year：2021

<details>
<summary>原始 review 全文</summary>

```text
The authors cast DNN classifiers as the push-forward of a base classifier under aflow map at some fixed final time. Under some reasonable assumptions on the flow,they show that, given any base classifier, the flow map can be obtained as the solutionto a convection-diffusion equation. They show that ResNets and Gaussian noise injectioncan be viewed as special cases of their model and give a robustness guarantee for any classifier defined as a solution to their PDE. Experiments on the 2-d half moon data setas well CIFAR 10 and 100 show better robustness  of their model to adversarial attacks when compared to standard ResNet(s).Apart from a few typos, the paper is well-written and generally easy to follow and understand.The proofs, while not containing any novel techniques, are rigorous and correct. Viewing a DNN model as the flow of a regular Markovian operator seems quite natural and generalizes the neural ODE idea. I also appreciate that the authors derive an explicit PDE based on very reasonable assumptions on the desired properties of a generic classifier. I also reallylike the illustrative example for ResNet and the Gaussian model injection, essentially viewing neural ODE(s) as the characteristic curves of a transport equation which is a special case of their more general convection-diffusion equation (for ResNet). I also liked therobustness guarantee which serves as an inspiration for using this framework to build modelsthat are better adept at handling adversarial examples. Generally, I think stability is the right motivation for considering such frameworks.The algorithms and numerics are the weaker parts of this work. It is unclear why the authors choose to reduce their PDE (1) to a re-scaled heat equation after showing that ResNet(s), models that are known to work well, come from a transport equation. Perhaps this simply makes the PDE easier to solve with less parameters to be learned. Nevertheless,I think exploring the more general form should certainly be done given the first part of the paper places a lot of emphasis on this result. My guess as to why the methods ends up working is that the diffusion form the heat equation is able to smooth out the loss functionwhich results in finding more stable regions of parameter space (perhaps there is a connection to https://arxiv.org/pdf/1704.04932.pdf which takes a similar point of view but with a viscous Hamilton-Jacobi equation on SGD instead)? The method of solving this heat equation just with another neural network seems a bit uninspired and is simply a special case of PINNS (https://www.sciencedirect.com/science/article/pii/S0021999118307125).While the PDE is very high dimensional, it is also very simple so applying some Using classical techniques to solve it will, I think, make for a very interesting comparison. Furthermore the numerics are not nearly extensive enough (I do appreciatethe half moon example showing the smoothed decision boundary). The authors need to consider more network architectures, not just ResNet, as well as harder datasets,like ImageNet, and more types of adversarial attacks to really make a case that this method is practically useful. Furthermore, there seems to be a significant decreasein accuracy for clean images. If this is to be practical, this issue must be resolvedas sacrificing 10% in accuracy for some robustness is usually not acceptable.Very interesting connection between DNN(s) and PDE(s), generalizing neural ODE(s) but the practical algorithms presented don't make a strong case for the method.
```

</details>

Review 主要点：
- DNN-PDE connection 有趣，proof correct，writing clear。
- 算法和 numerics 较弱，heat equation reduction 和 PINNs-like solver 被质疑。
- 需要更多架构、ImageNet、更广泛 attack、clean accuracy tradeoff 和 classical solver baseline。

Qwen 覆盖（原标注）：

- `Technical Correctness` (positive): The proofs, while not containing any novel techniques, are rigorous and correct.
- `Technical Novelty` (negative): The method of solving this heat equation just with another neural network seems a bit uninspired and is simply a special case of PINNS
- `Related Work Positioning & Citations` (positive): I also appreciate that the authors derive an explicit PDE based on very reasonable assumptions on the desired properties of a generic classifier
- `Experimental Setup & Protocol` (negative): The authors need to consider more network architectures, not just ResNet, as well as harder datasets, like ImageNet, and more types of adversarial attacks
- `Reproducibility & Implementation` (negative): The method of solving this heat equation just with another neural network seems a bit uninspired and is simply a special case of PINNS
- `Efficiency & Scalability` (negative): If this is to be practical, this issue must be resolved as sacrificing 10% in accuracy for some robustness is usually not acceptable
- `Writing Clarity & Organization` (positive): Apart from a few typos, the paper is well-written and generally easy to follow and understand
- `Originality / Novelty` (positive): Viewing a DNN model as the flow of a regular Markovian operator seems quite natural and generalizes the neural ODE idea
- `Fit to Venue / Scope` (positive): The paper is well-written and generally easy to follow and understand
- `Metrics & Evaluation Criteria` (negative): The authors need to consider more network architectures, not just ResNet, as well as harder datasets, like ImageNet, and more types of adversarial attacks
- `Hyperparameter / Seed Sensitivity` (negative): It is unclear why the authors choose to reduce their PDE (1) to a re-scaled heat equation...
- `Distribution Shift & Generalization (OOD)` (negative): The authors need to consider more network architectures, not just ResNet, as well as harder datasets, like ImageNet, and more types of adversarial attacks
- `Interpretation of Results` (negative): The authors need to consider more network architectures, not just ResNet, as well as harder datasets, like ImageNet, and more types of adversarial attacks

GPT main 覆盖：

- `Writing Clarity & Organization` (positive): Experiments on the 2-d half moon data setas well CIFAR 10 and 100 show better robustness  of their model to adversarial attacks when compared to standard ResNet(s).Apart from a few typos, the paper is well-written and ge...
- `Technical Correctness` (positive): Experiments on the 2-d half moon data setas well CIFAR 10 and 100 show better robustness  of their model to adversarial attacks when compared to standard ResNet(s).Apart from a few typos, the paper is well-written and ge...
- `Originality / Novelty` (positive): If this is to be practical, this issue must be resolvedas sacrificing 10% in accuracy for some robustness is usually not acceptable.Very interesting connection between DNN(s) and PDE(s), generalizing neural ODE(s) but th...
- `Motivation / Problem Framing` (positive): Generally, I think stability is the right motivation for considering such frameworks.The algorithms and numerics are the weaker parts of this work.
- `Problem Setup Validity` (negative): It is unclear why the authors choose to reduce their PDE (1) to a re-scaled heat equation after showing that ResNet(s), models that are known to work well, come from a transport equation.
- `Technical Novelty` (negative): Experiments on the 2-d half moon data setas well CIFAR 10 and 100 show better robustness  of their model to adversarial attacks when compared to standard ResNet(s).Apart from a few typos, the paper is well-written and ge...
- `Experimental Setup & Protocol` (negative): Furthermore the numerics are not nearly extensive enough (I do appreciatethe half moon example showing the smoothed decision boundary).
- `Baselines & Fair Comparison` (negative): The method of solving this heat equation just with another neural network seems a bit uninspired and is simply a special case of PINNS (https://www.sciencedirect.com/science/article/pii/S0021999118307125).While the PDE i...
- `Interpretation of Results` (negative): Furthermore, there seems to be a significant decreasein accuracy for clean images.

GPT mini 覆盖：

- `Writing Clarity & Organization` (positive): Experiments on the 2-d half moon data setas well CIFAR 10 and 100 show better robustness  of their model to adversarial attacks when compared to standard ResNet(s).Apart from a few typos, the paper is well-written and ge...
- `Technical Correctness` (positive): Experiments on the 2-d half moon data setas well CIFAR 10 and 100 show better robustness  of their model to adversarial attacks when compared to standard ResNet(s).Apart from a few typos, the paper is well-written and ge...
- `Originality / Novelty` (positive): Viewing a DNN model as the flow of a regular Markovian operator seems quite natural and generalizes the neural ODE idea.
- `Motivation / Problem Framing` (positive): Generally, I think stability is the right motivation for considering such frameworks.The algorithms and numerics are the weaker parts of this work.
- `Experimental Setup & Protocol` (negative): The authors need to consider more network architectures, not just ResNet, as well as harder datasets,like ImageNet, and more types of adversarial attacks to really make a case that this method is practically useful.
- `Distribution Shift & Generalization (OOD)` (negative): The authors need to consider more network architectures, not just ResNet, as well as harder datasets,like ImageNet, and more types of adversarial attacks to really make a case that this method is practically useful.

判断：Qwen `7 / 13`，GPT main `9 / 9`，GPT mini `6 / 6`。main 覆盖最完整；mini 精准但漏 efficiency/baseline/technical novelty；Qwen Venue/Related Work/Reproducibility 误标。

### 8. Couple-dance mocap and generation

Paper / Review：`KfkmwYQXWh` / `fE19txHpeO`，Year：2024

<details>
<summary>原始 review 全文</summary>

```text
This paper presents a mocap dataset for couple dances, a novel motion representation that takes contact into account, and a diffusion-based model for predicting conditional motion during couple dance.* The proposed mocap dataset is a good contribution to the community especially as it contains enough fine-grained information to capture contact points between people.* The proposed motion representation prioritizes correctly predicting contact, something that is often missing from similar works.* The proposed diffusion-based method seems to achieve competitive results (though see weaknesses and questions for issues with the evaluation methodology).* Evaluation:    * Simple strong baselines missing from the quantitative and qualitative experiments:        * Return a NN motion clip of a follower from the training set where the distance is calculated based on motion-based distance        * Return a NN motion clip of a follower from the training set where the distance is calculated based on a SOTA music embedding distance        * Mirror the motion of the leader.    * Metrics:        * Missing a measure of correlation between the dancers in comparison to ground truth (see questions below)    * Baselines:        * Missing an apples-to-Apples comparison with existing baselines on the datasets on which they were trained:            * Result tables in main and appendix only seem to test Duolando on the InterDance dataset or train the proposed method on DD100 (Table 3 in the appendix E) but I couldn’t find an apples-to-apples comparison of the proposed method trained and tested on the existing DD100 to Duolando trained and tested on DD100 (allowing Duolando to be tested on the dataset on which it was trained.            * This apples-to-apples comparison is crucial in the case of Duolando which learns a motion codebook from training data and therefore is not suited to be tested on out-of-distribution dance genres. * Exposition:    * Missing some implementation details for the experimental setup (see details below in the questions section)    * Missing details of the user study: where were participants recruited from, how were they compensated, in what format were videos presented, in what resolution, was music included and did the experimenters verify it was in use, etc.* Smaller notes:    * The caption of Table 1 is not entirely factual as stated since InterHuman has Strong interaction and a longer total duration: “Among duet dance datasets with strong interaction, InterDance features the widest range of 15 dance genres, the longest average duration per sample at 142.7 seconds, and the longest total duration of 3.93 hours.”* Limitations:    * Limitations are not properly discussed. As in all studies, there are limitations in both dataset and method. These are to be expected, but should also be mentioned.         * The dataset is indeed larger than existing mocap ones, but is still a small dataset when compared to methods that can rely on image-based 3D lifting. There is a balance here between data quality and quantity, but that should be mentioned.        * There are limitations to using diffusion-based generative models for motion prediction in comparison with autoregressive methods, namely the full trajectory is predicted at once, without training to predict longer sequences in a sliding-window fashion.        * This is the only limitation mentioned: “The potential societal impact is that, as dance generation and human interaction technology become more advanced, highly realistic virtual humans might lead users to become so immersed in the virtual world that they detach from real-world participation.” (L 531). However, if this technology becomes more advanced, more imminent limitations may present themselves. Namely, music-to-dance and person-to-person prediction of dance may be used by AI systems to replace human dancers and choreographers, leading to a less creative human kind and numerous copyright issues.* Dataset: why not combine with DD100 to create a larger total dataset?* Motion representation: if the root translation and angle is modeled jointly with the body pose (joints and vertices) it seems to me that translation, orientation, and pose would be coupled together. i.e. a person lifting their leg at point A in space would need a different representation then a person lifting their leg in the same way at point B in space. This seems to lead to needing more data in order to learn motion priors from the data as opposed to representations that would decouple pose from location and orientation. I am not listing this as a limitation yet as I would like to hear your thoughts about this issue. Would you be so kind as to explain this to me?* Evaluation:    * Metrics:        * How is FID calculated?        * While cross distance captures the distance between the two dancers, I am missing some measure of the correlation between the motion dynamics of the two dancers (see, for example paired FD here: https://arxiv.org/pdf/2204.08451). Do you think that cross distance captures this already somehow? If so, please explain. If not, I would suggest adding a measure of correlation in comparison to the ground truth correlation.    * Baselines:        * how are Edge and InterGen modified for benchmarking on this task (as they were designed a trained for different tasks)? Details are not given in the manuscript.        * Was Duolando trained on the proposed InterDance dataset for the experiments presented? Or was it trained on its original DD100 dataset and tested on InterDance?        * The following explanation regarding the performance of Duolando is cryptic to me. Please explain what you meant by it (line 421) “Compared with Duolando, which is carefully designed for reactive dance generation, our method performs better in most metrics. This is because Duolando employs a two-stage training framework that stores motions in a codebook, making it difficult to optimize fine-grained interactions.”* Result videos:    * Are the result videos on unseen test examples or from the train/val set?    * Are the other methods in the result videos tested on the newly proposed dataset or on their original datasets on which they were trained? Was testing conducted on the test sets of the other methods in comparison?    * Why is EDGE not in the results videos?    * Please provide results also on randomly-chosen (rather than cherry-picked) examples.
```

</details>

Review 主要点：
- couple-dance mocap dataset 和 contact-aware representation 有贡献。
- 缺少 strong baselines、correlation metric、apples-to-apples comparison。
- user study details、dataset size、table caption、limitations 和 societal impacts 需补。

Qwen 覆盖（原标注）：

- `Fit to Venue / Scope` (negative): The proposed mocap dataset is a good contribution to the community especially as it contains enough fine-grained information to capture contact points between people.
- `Technical Correctness` (negative): The proposed motion representation prioritizes correctly predicting contact, something that is often missing from similar works.
- `Reproducibility & Implementation` (negative): Missing details of the user study: where were participants recruited from, how were they compensated, in what format were videos presented, in what resolution, was music included and did the
- `Experimental Setup & Protocol` (negative): Missing some implementation details for the experimental setup (see details below in the questions section)
- `Baselines & Fair Comparison` (negative): Simple strong baselines missing from the quantitative and qualitative experiments
- `Metrics & Evaluation Criteria` (negative): Missing a measure of correlation between the dancers in comparison to ground truth (see questions below)
- `Data / Dataset Appropriateness` (negative): The caption of Table 1 is not entirely factual as stated since InterHuman has Strong interaction and a longer total duration
- `Societal / Broader Impacts` (negative): The potential societal impact is that, as dance generation and human interaction technology become more advanced, highly realistic virtual humans might lead users to become so immersed in the virtual
- `Technical Novelty` (positive): The proposed motion representation prioritizes correctly predicting contact, something that is often missing from similar works
- `Originality / Novelty` (positive): The proposed mocap dataset is a good contribution to the community especially as it contains enough fine-grained information to capture contact points between people
- `Related Work Positioning & Citations` (negative): Missing an apples-to-apples comparison with existing baselines on the datasets on which they were trained
- `Ethics / Safety / Misuse` (negative): The potential societal impact is that, as dance generation and human interaction technology become more advanced, highly realistic virtual humans might lead users to become so immersed in the virtual

GPT main 覆盖：

- `Technical Novelty` (positive): This paper presents a mocap dataset for couple dances, a novel motion representation that takes contact into account, and a diffusion-based model for predicting conditional motion during couple dance.* The proposed mocap...
- `Data / Dataset Appropriateness` (negative): This paper presents a mocap dataset for couple dances, a novel motion representation that takes contact into account, and a diffusion-based model for predicting conditional motion during couple dance.* The proposed mocap...
- `Baselines & Fair Comparison` (negative): This paper presents a mocap dataset for couple dances, a novel motion representation that takes contact into account, and a diffusion-based model for predicting conditional motion during couple dance.* The proposed mocap...
- `Metrics & Evaluation Criteria` (negative): * Metrics:        * Missing a measure of correlation between the dancers in comparison to ground truth (see questions below)    * Baselines:        * Missing an apples-to-Apples comparison with existing baselines on the...
- `Experimental Setup & Protocol` (negative): * Exposition:    * Missing some implementation details for the experimental setup (see details below in the questions section)    * Missing details of the user study: where were participants recruited from, how were they...
- `Reproducibility & Implementation` (negative): * Exposition:    * Missing some implementation details for the experimental setup (see details below in the questions section)    * Missing details of the user study: where were participants recruited from, how were they...
- `Distribution Shift & Generalization (OOD)` (negative): * This apples-to-apples comparison is crucial in the case of Duolando which learns a motion codebook from training data and therefore is not suited to be tested on out-of-distribution dance genres.
- `Figures / Tables & Visual Presentation` (negative): * Exposition:    * Missing some implementation details for the experimental setup (see details below in the questions section)    * Missing details of the user study: where were participants recruited from, how were they...
- `Writing Clarity & Organization` (negative): * The following explanation regarding the performance of Duolando is cryptic to me.
- `Interpretation of Results` (negative): * Exposition:    * Missing some implementation details for the experimental setup (see details below in the questions section)    * Missing details of the user study: where were participants recruited from, how were they...
- `Societal / Broader Impacts` (negative): However, if this technology becomes more advanced, more imminent limitations may present themselves.

GPT mini 覆盖：

- `Experimental Setup & Protocol` (negative): This paper presents a mocap dataset for couple dances, a novel motion representation that takes contact into account, and a diffusion-based model for predicting conditional motion during couple dance.* The proposed mocap...
- `Baselines & Fair Comparison` (negative): This paper presents a mocap dataset for couple dances, a novel motion representation that takes contact into account, and a diffusion-based model for predicting conditional motion during couple dance.* The proposed mocap...
- `Metrics & Evaluation Criteria` (negative): * Metrics:        * Missing a measure of correlation between the dancers in comparison to ground truth (see questions below)    * Baselines:        * Missing an apples-to-Apples comparison with existing baselines on the...
- `Reproducibility & Implementation` (negative): * Exposition:    * Missing some implementation details for the experimental setup (see details below in the questions section)    * Missing details of the user study: where were participants recruited from, how were they...
- `Data / Dataset Appropriateness` (negative): * The dataset is indeed larger than existing mocap ones, but is still a small dataset when compared to methods that can rely on image-based 3D lifting.
- `Interpretation of Results` (negative): * The following explanation regarding the performance of Duolando is cryptic to me.
- `Originality / Novelty` (positive): This paper presents a mocap dataset for couple dances, a novel motion representation that takes contact into account, and a diffusion-based model for predicting conditional motion during couple dance.* The proposed mocap...

判断：Qwen `8 / 12`，GPT main `10 / 11`，GPT mini `7 / 7`。main 捕捉 societal/figures/OOD 等细节；mini 干净但漏 technical novelty/societal；Qwen 把正面贡献错标为负面 Fit/Technical。

### 9. SubZero zeroth-order LLM fine-tuning

Paper / Review：`FK6T0U4Mg1` / `XhV3jyK4cq`，Year：2024

<details>
<summary>原始 review 全文</summary>

```text
The paper introduces SubZero, a random subspace zeroth-order optimization method designed for memory-efficient fine-tuning of large language models (LLMs). Traditional backpropagation becomes impractical for such massive models due to high memory demands, and while zeroth-order (ZO) methods offer a memory-efficient alternative by estimating gradients using only forward passes, they suffer from high variance in high-dimensional settings typical of LLMs. SubZero addresses this issue by applying layer-specific low-rank perturbations, significantly reducing memory consumption and improving training performance. The authors theoretically prove that their gradient estimates closely approximate those from backpropagation and have lower variance than traditional ZO methods. They also introduce a simple yet effective pretraining strategy to implement SubZero effectively. Furthermore, they integrate SubZero into traditional and parameter-efficient fine-tuning techniques like LoRA, proposing specific adjustments to enhance this integration.1. Clear and Well-Written: The paper is well-written, making complex concepts—including theoretical proofs—accessible and easy to understand.2. Addresses a Critical Problem in Traditional LLM Fine-Tuning: It tackles the significant issue of high memory consumption during fine-tuning of large language models (LLMs). By maintaining only six matrices—a subset of the original full model—it substantially reduces memory requirements.3. Effective Use of Zeroth-Order Optimization: The authors leverage existing zeroth-order (ZO) methods to approximate gradients efficiently. Their approach yields gradient estimates that are closer to true gradients and exhibit lower variance than traditional ZO methods.4. Reproducibility Through Detailed Pseudocode: The inclusion of straightforward pseudocode and comprehensive methodological details ensures that the work is reproducible and easy to follow.5. Comprehensive Ablation Studies: The paper provides thorough ablation studies on the components of the method. These experiments validate the effectiveness of each component and demonstrate their contributions to the overall performance.6. Modularity and Integration with Existing Fine-Tuning techniques: It's commendable that the method is designed as a module that can be incorporated into both traditional fine-tuning and parameter-efficient fine-tuning methods like LoRA. The authors address issues arising from this integration by proposing practical techniques, investigating their validity and effectiveness, and ultimately delivering a robust and versatile method.7. Strong Theoretical and Empirical Support: All claims are substantiated with theoretical proofs and empirical investigations.8. Performance Improvements Over SoTA: The method shows performance boosts compared to existing state-of-the-art ZO methods, achieving faster convergence and better fine-tuning results across various language modeling tasks.9. Evaluation on Diverse Downstream Tasks and Models: The authors use a variety of benchmarks and models to demonstrate the performance and ease of application of their method.1. Lack of Comparison with Vanilla LoRA: The paper does not compare the proposed ZO-LoRA method directly with the standard LoRA approach, making it difficult to quantify the benefits of using ZO-LoRA over existing parameter-efficient fine-tuning methods. Including such a baseline would clarify the practical advantages of SubZero.2. Missing Advanced LoRA Baselines: The evaluation does not consider advanced LoRA variants like AutoLoRA (Zhang et al., 2024). Including comparisons with such methods could strengthen the practical relevance of the paper.3. Inconsistency in Reporting Results: In Table 2, for the SST-2 column under ZO-FT methods, the best-performing metric is not correctly highlighted; SubZero's metric is highlighted instead of the incumbent method's performance.4. Influence of ReCoRD Task on Overall Performance: The ReCoRD task appears to disproportionately influence the average performance in the fine-tuning case. Excluding ReCoRD, the average scores for the methods become very similar (69.4, 70, and 70.4), making the differences negligible.5. Unclear Computational Overheads and Budgets: In Figure 1c (training loss vs. wall-clock time), it is unclear whether the overhead associated with ZO methods is included. Additionally, the methods seem to have different computational budgets, complicating the comparison of convergence speeds and efficiency.6. Need for Clarification on Variance Reduction: The paper emphasizes that SubZero reduces variance in gradient estimates and accelerates convergence. While it's generally understood that lower variance can lead to faster convergence, it's unclear why these are presented as two separate points. Clarifying this relationship would enhance understanding.1. Have you compared ZO-LoRA directly with vanilla LoRA, and can you provide the results?2. Could you include comparisons with advanced LoRA variants like AutoLoRA to strengthen the practical side of your evaluation?3. In Table 2, could you verify and correct the highlighting for the best metric in the SST-2 column under ZO-FT methods?4. Could you explain the low performance of the ReCoRD task for S-MeZO?5. In Figure 1c, does the wall-clock time include ZO methods' overhead, and why do the methods have different computational budgets?6. Why are variance reduction and accelerated convergence presented as separate points when faster convergence is generally a result of lower variance in gradients?
```

</details>

Review 主要点：
- SubZero 针对 LLM fine-tuning memory 问题，写作、pseudocode、ablation 都受到表扬。
- 缺少 vanilla LoRA / advanced LoRA fair comparison。
- compute overhead、budget、Table 2 highlight、ReCoRD dominance 等需要澄清。

Qwen 覆盖（原标注）：

- `Writing Clarity & Organization` (positive): The paper is well-written, making complex concepts—including theoretical proofs—accessible and easy to understand.
- `Problem Setup Validity` (positive): It tackles the significant issue of high memory consumption during fine-tuning of large language models (LLMs).
- `Technical Correctness` (positive): The authors theoretically prove that their gradient estimates closely approximate those from backpropagation and have lower variance than traditional ZO methods.
- `Reproducibility & Implementation` (positive): The inclusion of straightforward pseudocode and comprehensive methodological details ensures that the work is reproducible and easy to follow.
- `Ablation & Attribution` (positive): The paper provides thorough ablation studies on the components of the method. These experiments validate the effectiveness of each component and demonstrate their contributions to the overall performance.
- `Technical Novelty` (positive): The authors leverage existing zeroth-order (ZO) methods to approximate gradients efficiently. Their approach yields gradient estimates that are closer to true gradients and exhibit lower variance than traditional ZO meth...
- `Experimental Setup & Protocol` (positive): The authors use a variety of benchmarks and models to demonstrate the performance and ease of application of their method.
- `Metrics & Evaluation Criteria` (positive): The method shows performance boosts compared to existing state-of-the-art Z, achieving faster convergence and better fine-tuning results across various language modeling tasks.
- `Statistical Evidence` (positive): All claims are substantiated with theoretical proofs and empirical investigations.
- `Efficiency & Scalability` (negative): In Figure 1c (training loss vs. wall-clock time), it is unclear whether the overhead associated with ZO methods is included.
- `Baselines & Fair Comparison` (negative): The paper does not compare the proposed ZO-LoRA method directly with the standard LoRA approach, making it difficult to quantify the benefits of using ZO-LoRA over existing parameter-efficient fine-tuning methods.
- `Data / Dataset Appropriateness` (negative): In Table 2, for the SST-2 column under ZO-FT methods, the best-performing metric is not correctly highlighted; SubZero's metric is highlighted instead of the incumbent method's performance.

GPT main 覆盖：

- `Writing Clarity & Organization` (positive): Clear and Well-Written: The paper is well-written, making complex concepts—including theoretical proofs—accessible and easy to understand.2.
- `Motivation / Problem Framing` (positive): Addresses a Critical Problem in Traditional LLM Fine-Tuning: It tackles the significant issue of high memory consumption during fine-tuning of large language models (LLMs).
- `Reproducibility & Implementation` (positive): Reproducibility Through Detailed Pseudocode: The inclusion of straightforward pseudocode and comprehensive methodological details ensures that the work is reproducible and easy to follow.5.
- `Ablation & Attribution` (positive): Comprehensive Ablation Studies: The paper provides thorough ablation studies on the components of the method.
- `Baselines & Fair Comparison` (negative): Performance Improvements Over SoTA: The method shows performance boosts compared to existing state-of-the-art ZO methods, achieving faster convergence and better fine-tuning results across various language modeling tasks...
- `Figures / Tables & Visual Presentation` (negative): Inconsistency in Reporting Results: In Table 2, for the SST-2 column under ZO-FT methods, the best-performing metric is not correctly highlighted; SubZero's metric is highlighted instead of the incumbent method's perform...
- `Efficiency & Scalability` (negative): By maintaining only six matrices—a subset of the original full model—it substantially reduces memory requirements.3.
- `Distribution Shift & Generalization (OOD)` (positive): Evaluation on Diverse Downstream Tasks and Models: The authors use a variety of benchmarks and models to demonstrate the performance and ease of application of their method.1.
- `Interpretation of Results` (negative): Influence of ReCoRD Task on Overall Performance: The ReCoRD task appears to disproportionately influence the average performance in the fine-tuning case.

GPT mini 覆盖：

- `Writing Clarity & Organization` (positive): Clear and Well-Written: The paper is well-written, making complex concepts—including theoretical proofs—accessible and easy to understand.2.
- `Reproducibility & Implementation` (positive): Reproducibility Through Detailed Pseudocode: The inclusion of straightforward pseudocode and comprehensive methodological details ensures that the work is reproducible and easy to follow.5.
- `Ablation & Attribution` (positive): Comprehensive Ablation Studies: The paper provides thorough ablation studies on the components of the method.
- `Baselines & Fair Comparison` (negative): Lack of Comparison with Vanilla LoRA: The paper does not compare the proposed ZO-LoRA method directly with the standard LoRA approach, making it difficult to quantify the benefits of using ZO-LoRA over existing parameter...
- `Figures / Tables & Visual Presentation` (negative): Unclear Computational Overheads and Budgets: In Figure 1c (training loss vs.
- `Experimental Setup & Protocol` (negative): Additionally, the methods seem to have different computational budgets, complicating the comparison of convergence speeds and efficiency.6.
- `Interpretation of Results` (negative): Influence of ReCoRD Task on Overall Performance: The ReCoRD task appears to disproportionately influence the average performance in the fine-tuning case.

判断：Qwen `11 / 12`，GPT main `8 / 9`，GPT mini `7 / 7`。三者都不错；main 的 Distribution Shift 略宽；mini 漏 positive motivation/technical correctness 等；Qwen 只有 Data/Dataset 明显错。

### 10. Missing-at-random DiD

Paper / Review：`44Pc9erEIV` / `8ry7XWmVdr`，Year：2025

<details>
<summary>原始 review 全文</summary>

```text
The paper studies two-group, two-period Difference-in-Differences when pretreatment outcomes are Missing-At-Random (MAR). It targets the Average Treatment Effect on the Treated. The authors give two identification strategies: (i) MAR given $(X,A)$ and (ii) MAR given $(X,A,Y)$. For each, they derive the observed-data efficient influence function and the semiparametric efficiency bound. They then construct cross-fitted estimators that achieve the bounds and show “multiple robustness”: consistency holds if certain sets of nuisance models are correct. A simulation study illustrates bias/RMSE patterns across correctly specified vs misspecified nuisances.Originality- Treats missing pre- or post- outcomes in the canonical $2 \times 2$ DiD with covariates, and does so in a semiparametric framework with explicit EIFs. Prior DiD papers often assume full outcomes or focus on staggered timing without MAR-aware efficiency analysis. Framing MAR both as post-treatment outcome-independent (given $X, A$ ) and post-treatment outcome-dependent (given $X, Y_1, A$ ) is a clear conceptual step.- The nested regression component $\eta_0(x, 0)=\mathbb{E}\left[\mu_0\left(x, Y_1, 0\right) \mid X=x, A=0\right]$ and its stability analysis give a concrete recipe to learn the extra layer needed under outcome-dependent MAR. This is a neat link to modern DR-Learner style ideas.Quality- Identification statements are precise, and the EIFs are derived with clear bookkeeping of nuisance components $(\mu, \pi, \gamma, \eta)$. The efficiency-loss decompositions versus the fully-observed benchmark are informative.- The cross-fitting scheme and high-level conditions for asymptotic normality align with current best practice and are stated cleanly.Clarity- The paper lays out the two MAR regimes, writes explicit plug-in equations for estimators, and provides a concise multiple-robustness table. This helps readers see exactly which nuisance pieces must be correct for consistency.- The simulations mirror the theory with clear toggles between correctly specified and misspecified nuisances. Significance- DiD with missing outcomes is common in applied work. A semi-parametrically efficient, multiply robust procedure is valuable for practice, especially when complete-case strategies are biased. The results can plug into modern ML pipelines through cross-fitting.1. Positioning vs related work (novelty claims).The paper cites DiD with staggered adoption and some recent missing-data DiD work, but the empirical reader will ask: how do your estimators compare to (a) complete-case DiD (DiD with missing items dropped), (b) simple inverse-probability weighting for $R_0$, (c) regression imputation baselines, and (d) standard DR DiD with fully observed outcomes?So, could the authors add a benchmark section with these baselines, including plots of bias, RMSE, and coverage? It would be better include a brief analytic comparison to DR DiD under full data to highlight where efficiency is lost and recovered.2. Inference and coverage.The simulations emphasize bias and RMSE but not confidence interval coverage or interval length. Since the paper claims efficiency and gives EIFs, empirical coverage is central.Could the authors report empirical coverage and average CI width across scenarios, including small-sample behavior and the impact of fold choice $J$? The authors can show whether the sandwich variance based on the estimated EIF is reliable.3. Plausibility of MAR assumptions.Outcome-dependent MAR given $Y_1$ is subtle: it conditions on a post-treatment variable. I was wondering which examples in the Introduction (job training programs in labor economics, prior test scores in education policy, and EHR in health research) would arguably satisfy this assumption.4. Nested regression learning details.The stability definition and oracle rates are high-level. Readers will want concrete guidance: what models to fit for $\mu_0\left(x, y_1, a\right)$, how to construct pseudo-outcomes with augmentation, and how to tune them.Can the authors add an algorithm box for learning $\eta_0$ under both the regression and conditional-density approaches? They can also give default choices (e.g., gradient-boosted trees for $\mu$, logistic for $\gamma$, random-forest regression for $\eta$ ), with practical notes on hyperparameter tuning, cross-fitting folds, and clipping for $\hat{\gamma}$. 5. External validity and real data.The paper would benefit from at least one real application to show end-to-end feasibility and the size of efficiency gains in practice.Can the authors add a compact empirical example (even in the appendix)? They can report the estimated ATT with the proposed method and the baselines, Cl widths, and a short discussion of assumption plausibility in that setting.1. On outcome-dependent MAR:In practice, when would you recommend modeling $\operatorname{Pr}\left(R_0=1 \mid X, Y_1, A\right)$ rather than $\operatorname{Pr}\left(R_0=\right. 1 \mid X, A)$ ? Can you provide guidance or a rule-of-thumb diagnostic for deciding whether including $Y_1$ is likely to help or to add variance? Any empirical check that conditioning on $Y_1$ does not induce harmful instability?2. Efficiency gains in practice:Can you report the magnitude of efficiency gains (variance reduction) relative to simple IPW or regression imputation in your simulations and, ideally, one real dataset? A table with bound estimates, plug-in variances, and empirical variances would help.3. Coverage under misspecification:When multiple robustness conditions fail, how badly do Cls mis-cover? Please provide coverage heatmaps across nuisance-misspecification cells to show the method's breaking points.4. Learning $\eta_0$ :For the augmented pseudo-outcome strategy, do you recommend trimming on $\hat{\gamma}$? If so, what thresholds and what is the implied target estimand after trimming? How sensitive are results to this choice?
```

</details>

Review 主要点：
- MAR-DiD 的 EIF / efficiency / multiple robustness 有清晰贡献。
- 需要更多 baseline comparison、coverage/CI width、real application。
- MAR plausibility、nested regression implementation、tuning/folds/clipping 需要更具体。

Qwen 覆盖（原标注）：

- `Originality / Novelty` (positive): Originality - Treats missing pre- or post- outcomes in the canonical 2 × 2 DiD with covariates, and does so in a semiparametric framework with explicit EIFs.
- `Fit to Venue / Scope` (negative): The paper cites DiD with staggered adoption and some recent missing-data DiD work, but the empirical reader will ask: how do your estimators compare to (a) complete-case DiD...
- `Technical Correctness` (positive): Identification statements are precise, and the EIFs are derived with clear bookkeeping of nuisance components (μ, π, γ, η).
- `Experimental Setup & Protocol` (positive): The cross-fitting scheme and high-level conditions for asymptotic normality align with current best practice and are stated cleanly.
- `Baselines & Fair Comparison` (negative): could the authors add a benchmark section with these baselines, including plots of bias, RMSE, and coverage?
- `Metrics & Evaluation Criteria` (negative): The simulations emphasize bias and RMSE but not confidence interval coverage or interval length.
- `Reproducibility & Implementation` (negative): Readers will want concrete guidance: what models to fit for μ₀(x, y₁, a), how to construct pseudo-outcomes with augmentation, and how to tune them.
- `Efficiency & Scalability` (positive): A semi-parametrically efficient, multiply robust procedure is valuable for practice, especially when complete-case strategies are biased.
- `Writing Clarity & Organization` (positive): The paper lays out the two MAR regimes, writes explicit plug-in equations for estimators, and provides a concise "multiple-robustness" table.
- `Related Work Positioning & Citations` (negative): The paper cites DiD with staggered adoption and some recent missing-data DiD work, but the empirical reader will ask: how do your estimators compare to (a) complete-case DiD...
- `Ethics / Safety / Misuse` (negative): The paper would benefit from at least one real application to show end-to-end feasibility and the size of efficiency gains in practice.
- `Societal / Broader Impacts` (positive): DiD with missing outcomes is common in applied work. A semi-parametrically efficient, multiply robust procedure is valuable for practice...

GPT main 覆盖：

- `Originality / Novelty` (positive): Framing MAR both as post-treatment outcome-independent (given $X, A$ ) and post-treatment outcome-dependent (given $X, Y_1, A$ ) is a clear conceptual step.- The nested regression component $\eta_0(x, 0)=\mathbb{E}\left[...
- `Technical Novelty` (positive): Framing MAR both as post-treatment outcome-independent (given $X, A$ ) and post-treatment outcome-dependent (given $X, Y_1, A$ ) is a clear conceptual step.- The nested regression component $\eta_0(x, 0)=\mathbb{E}\left[...
- `Motivation / Problem Framing` (positive): Significance- DiD with missing outcomes is common in applied work.
- `Writing Clarity & Organization` (positive): The efficiency-loss decompositions versus the fully-observed benchmark are informative.- The cross-fitting scheme and high-level conditions for asymptotic normality align with current best practice and are stated cleanly...
- `Related Work Positioning & Citations` (negative): Positioning vs related work (novelty claims).The paper cites DiD with staggered adoption and some recent missing-data DiD work, but the empirical reader will ask: how do your estimators compare to (a) complete-case DiD (...
- `Baselines & Fair Comparison` (negative): Positioning vs related work (novelty claims).The paper cites DiD with staggered adoption and some recent missing-data DiD work, but the empirical reader will ask: how do your estimators compare to (a) complete-case DiD (...
- `Metrics & Evaluation Criteria` (negative): Inference and coverage.The simulations emphasize bias and RMSE but not confidence interval coverage or interval length.
- `Statistical Evidence` (negative): Since the paper claims efficiency and gives EIFs, empirical coverage is central.Could the authors report empirical coverage and average CI width across scenarios, including small-sample behavior and the impact of fold ch...
- `Problem Setup Validity` (negative): Plausibility of MAR assumptions.Outcome-dependent MAR given $Y_1$ is subtle: it conditions on a post-treatment variable.
- `Reproducibility & Implementation` (negative): Nested regression learning details.The stability definition and oracle rates are high-level.
- `Hyperparameter / Seed Sensitivity` (negative): They can also give default choices (e.g., gradient-boosted trees for $\mu$, logistic for $\gamma$, random-forest regression for $\eta$ ), with practical notes on hyperparameter tuning, cross-fitting folds, and clipping f...
- `Distribution Shift & Generalization (OOD)` (negative): External validity and real data.The paper would benefit from at least one real application to show end-to-end feasibility and the size of efficiency gains in practice.Can the authors add a compact empirical example (even...

GPT mini 覆盖：

- `Originality / Novelty` (positive): Framing MAR both as post-treatment outcome-independent (given $X, A$ ) and post-treatment outcome-dependent (given $X, Y_1, A$ ) is a clear conceptual step.- The nested regression component $\eta_0(x, 0)=\mathbb{E}\left[...
- `Experimental Setup & Protocol` (negative): This helps readers see exactly which nuisance pieces must be correct for consistency.- The simulations mirror the theory with clear toggles between correctly specified and misspecified nuisances.
- `Reproducibility & Implementation` (negative): Readers will want concrete guidance: what models to fit for $\mu_0\left(x, y_1, a\right)$, how to construct pseudo-outcomes with augmentation, and how to tune them.Can the authors add an algorithm box for learning $\eta_...
- `Efficiency & Scalability` (positive): The results can plug into modern ML pipelines through cross-fitting.1.
- `Writing Clarity & Organization` (positive): The efficiency-loss decompositions versus the fully-observed benchmark are informative.- The cross-fitting scheme and high-level conditions for asymptotic normality align with current best practice and are stated cleanly...
- `Interpretation of Results` (negative): Inference and coverage.The simulations emphasize bias and RMSE but not confidence interval coverage or interval length.
- `Baselines & Fair Comparison` (negative): Positioning vs related work (novelty claims).The paper cites DiD with staggered adoption and some recent missing-data DiD work, but the empirical reader will ask: how do your estimators compare to (a) complete-case DiD (...

判断：Qwen `9 / 12`，GPT main `12 / 12`，GPT mini `6 / 7`。main 覆盖非常完整；mini 漏 technical novelty/statistical/problem setup；Qwen Ethics/Fit 有误。

## GPT 对照结论

这 10 条样本里，Qwen 的优势仍然是 recall：它几乎把 review 里所有可能相关的批评点都捞出来了；但噪音主要来自高风险标签误触发，例如 `Fit to Venue / Scope`、`Ethics / Safety / Misuse`、`Societal / Broader Impacts`、`Technical Correctness` 和 `Reproducibility & Implementation`。

GPT mini 明显更像一个高 precision extractor：它通常只保留最明确的 6-8 个 aspect，错得少，但漏掉不少细分问题。对于大规模低成本跑数，它是一个比 Qwen 干净得多的 baseline。

GPT main 是当前最稳的选择：相比 mini，它多出来的 aspect 多数是有效补充，尤其擅长区分统计证据、实验协议、问题设定、数据适配、超参数敏感性和相关工作定位。缺点是成本约为 mini 的 18 倍，且 evidence span 偶尔偏长。

实用建议：如果预算允许，最终主结果用 GPT main；如果要控制成本，可以先用 GPT mini 全量跑，再对长 review、mini 抽取 aspect 过少、或 mixed stance 明显的样本用 GPT main 复核。

<!-- END GPT_MAIN_MINI_EXTENSION -->
