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
