# 1 Prediction of Antibody Non-Specificity using Protein Language

# 2 Models and Biophysical Parameters

```
3 Laila I. Sakhnini^1 ,^3 ,*, Ludovica Beltrame^2 , Simone Fulle^2 , Pietro Sormanni^3 , Anette Henriksen^1 , Nikolai
4 Lorenzen^1 , Michele Vendruscolo^3 ,*, Daniele Granata^2 ,*
```
```
5 1 Therapeutics Discovery, Novo Nordisk A/S, Copenhagen, Denmark
6 2 Digital Chemistry and Design, Novo Nordisk A/S, Copenhagen, Denmark
7 3 Centre for Misfolding Diseases, Department of Chemistry, University of Cambridge, UK
8
9 *Corresponding authors:
```
10 L.I. Sakhnini (llsh@novonordisk.com), M. Vendruscolo (mv245@cam.ac.uk), D. Granata

11 (dngt@novonordisk.com)

12

13

```
made available under aCC-BY-NC 4.0 International license.
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is
```

# 14 Abstract

15 The development of therapeutic antibodies requires optimizing target binding affinity and
16 pharmacodynamics, while ensuring high developability potential, including minimizing non-specific
17 binding. In this study, we address this problem by predicting antibody non-specificity by two
18 complementary approaches: (i) antibody sequence embeddings by protein language models (PLMs),
19 and (ii) a comprehensive set of sequence-based biophysical descriptors. These models were trained
20 on human and mouse antibody data from Boughter et al. (2020) and tested on three public datasets:
21 Jain et al. ( 2017 ), Shehata et al. ( 2019 ) and Harvey et al. ( 2022 ). We show that non-specificity is best
22 predicted from the heavy variable domain and heavy-chain complementary variable regions (CDRs).
23 The top performing PLM, a heavy variable domain-based ESM 1v LogisticReg model, resulted in
24 10 - fold cross-validation accuracy of up to 71%. Our biophysical descriptor-based analysis identified
25 the isoelectric point as a key driver of non-specificity. Our findings underscore the importance of
26 biophysical properties in predicting antibody non-specificity and highlight the potential of protein
27 language models for the development of antibody-based therapeutics. To illustrate the use of our
28 approach in the development of lead candidates with high developability potential, we show that it
29 can be extended to therapeutic antibodies and nanobodies.

30 Keywords: Therapeutic antibodies, non-specificity, protein-language models, machine learning,
31 isoelectric point

```
made available under aCC-BY-NC 4.0 International license.
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is
```

# 32 1. Introduction

33 Monoclonal antibodies (mAbs) continue to be one of the leading drug modalities in the
34 pharmaceutical industry, with more than 100 unique mAbs approved by the FDA since 2021 [ 1 ] and
35 global sales forecasted to 300 billion US dollars by 2025 [ 2 , 3 ]. The success of mAbs for therapeutic
36 application is the result of advances in in vivo and in vitro discovery platforms, which have enabled
37 fast generation of high-affinity binders towards a highly diverse set of targets [ 4 , 5 ]. Recently, de novo
38 design has gained increasing interest in the field as a third-generation discovery approach with the
39 potential of significantly accelerating drug discovery and development timelines [ 6 , 7 ]. Moreover,
40 with the advances in mAb engineering, there has also been an increased interest in the development
41 of mAbs with ultra-high target affinity (pM to fM) [ 8 ], context-dependent target binding (e.g. pH-
42 dependent [ 9 , 10 ] or ligand induced target binding [ 11 ]), and various multi-specific functionalities
43 [ 12 ]. To reach optimal binding affinity and potency, mAb hits identified during discovery are often
44 subjected to comprehensive screening campaigns using display platforms (libraries of 103 to 1 010
45 variants) of and recombinant well-plate variant generation workflows (libraries of 102 to 1 04 variants)
46 [ 13 ].
47
48 When selecting an antibody lead candidate for development towards clinical testing, optimal target
49 binding affinity and/or pharmacodynamics are key selection parameters. In addition, in the last decade
50 there has been an increased focus on the importance of progressing antibodies to clinical stage which
51 also possess a good developability potential. Antibody developability requires the intersection of
52 multiple disciplines, in which diverse parameters such as expression levels, immunogenicity,
53 processability, and formulation feasibility are addressed, to ensure optimal potential for successful
54 clinical development of lead candidates. Non-specific binding, i.e. weak non-covalent interactions
55 with off-target molecules or interfaces, has emerged as one of the key developability parameters to
56 increase the chance for clinical success [ 14 , 15 ]. Specifically, several studies reported that high
57 tendency for non-specific binding can translate into faster in vivo clearance, thereby compromising
58 pharmacokinetics [ 16 , 17 , 18 , 19 , 20 , 21 , 22 ]. Furthermore, there is an inherent risk that non-specific
59 interactions can translate into undesirable side-effects [ 23 ]. Non-specific binding is not a rare
60 phenomenon, as recent reports suggest the presence of a trade-off between affinity and specificity
61 [ 24 , 25 , 26 , 27 ]. Thus, optimization of affinity and potency comes with an inherent risk of
62 compromising target specificity [ 28 , 29 , 30 , 31 ].
63
64 Given the high level of interest in measuring non-specific interactions, there are several in vitro
65 screening assays available for this purpose. A commonly used assay is the Enzyme-Linked
66 Immunosorbent Assay (ELISA) with a panel of common antigens, typically insulin, DNA, albumin,
67 cardiolipin and lipopolysaccharide (LPS) [ 31 , 15 ]. Initially, these biomolecules were studied as model
68 antigens for autoimmune responses and diseases. For example, insulin is a self-antigen for
69 autoantibodies associated with type 1 diabetes [ 32 , 33 ]. In addition, DNA, albumin and cardiolipin
70 are self-antigens for autoantibodies associated with several diseases such as systemic lupus
71 erythematosus [ 34 , 35 ] and anti-phospholipid syndrome [ 36 ], and LPS is an antigen for immune
72 responses to bacterial infections [ 37 ]. Moreover, ELISA is widely used in immunology, where non-

```
made available under aCC-BY-NC 4.0 International license.
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is
```

73 specific antibodies are often referred to as poly-reactive antibodies. Such antibodies are characterised
74 as having low-affinity binding to multiple distinct antigens, including self-antigens, and they have
75 been widely studied for targets such as HIV and Influenza viruses, as they can be broadly neutralizing
76 [ 38 , 39 ]. While this feature is beneficial for immunity to infectious diseases, to potentially confer
77 broad protection against viruses, it is a highly undesirable feature for therapeutic mAbs. Other
78 common non-specificity assays include baculovirus particle (BVP) ELISA [ 40 ], poly-specific reagent
79 (PSR) [ 41 ], and cross-interaction chromatography with ligands such as heparin [ 42 ] and human IgG
80 from serum [ 43 ].
81
82 In addition to these in vitro assays, in silico methods have been gaining interest, and several tools
83 have been reported recently for prediction of non-specific interactions [ 44 , 45 , 46 , 47 ]. The
84 development and implementation of predictive computational methods for the prediction and re-
85 design of monoclonal antibody non-specificity at an early stage is of great interest, as it facilitates the
86 generation of safe and efficacious lead candidates with high developability potential. Several studies
87 reported on the identification of non-specificity by in silico approaches. Short, linear sequence motifs
88 (e.g. GG, RR, VG, VV, YY, WW and WxW, where x can be any amino acid) enriched in non-specific
89 antibodies, as reported by Kelly et al. [ 48 ], have been utilized to create synthetic antibody libraries
90 free from such motifs in the CDRs [ 49 ]. Moreover, AI/ML models that classifies non-specific
91 antibodies, leveraging experimental data and sequence-based information, have been reported.
92 Boughter et al. [ 44 ] developed a classifier to identify non-specific antibodies based on experimental
93 data acquired from ELISA with a panel of common antigens. Harvey et al. [ 45 ] developed a one-hot
94 LogisticReg model based on a naïve Nb library assessed by the PSR assay.
95
96 In this study, we developed machine learning (ML) models to estimate the non-specificity of
97 antibodies (Figure 1 A). Commonly used biophysical properties were tested alongside protein
98 language models (PLMs) to embed antibody sequences. PLMs have emerged as powerful tools for
99 extracting informative features from raw protein sequences by leveraging patterns learned from
100 massive sequence databases [ 50 , 51 , 52 , 53 ]. Among these, Evolutionary Scale Modeling (ESM)
101 models have shown particular promise in capturing structural, functional, and physico-chemical
102 properties (including antibody specificity) without requiring explicit structural data [ 54 , 55 , 56 , 57 ].
103 ESM models, such as ESM-1v, encode sequences into high-dimensional embeddings that reflect
104 residue context, conservation, and evolutionary information, which are all factors known to influence
105 antibody behaviour. These features make ESM models well-suited for predicting complex properties
106 like non-specificity, which can arise from subtle sequence-dependent effects not easily captured by
107 traditional descriptors. By applying ESM models to antibody variable regions, we aim to harness its
108 representation power to identify sequence signatures of non-specific binding and improve early-stage
109 developability assessment.
110
111 Besides testing which encoding provided the best prediction performance, one aspect of the study
112 was to identify which part of the antibody contributes to non-specificity. Furthermore, to gain
113 biophysical insight, sequence-based biophysical descriptors were analysed to support the predictive
114 models. Our results indicate that the computational models that we considered enable the prediction

```
made available under aCC-BY-NC 4.0 International license.
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is
```

115 of non-specific interactions that can be used to guide the design and selection of antibodies with
116 improved specificity and efficacy.
117

# 118 2. Results & Discussion

119 2.1 Public antibody data

120 Four different datasets were retrieved from public sources; (i) a curated dataset of >1000 mouse IgA,
121 influenza-reactive and HIV-reactive antibodies with their respective non-specificity flag from ELISA
122 with a panel of common antigens [ 44 ], (ii) 137 clinical-stage IgG1-formatted antibodies with their
123 respective non-specificity flag from ELISA with a panel of common antigens [ 15 ], (iii) 398
124 antibodies, originating from naïve, IgG memory and long-lived plasma cells, with their respective
125 poly-specific reagent score [ 58 ], and (iv) 140 000 nanobody (Nb) clones assessed by the PSR assay
126 from a naïve Nb library [ 45 ]. These four datasets are referred to as the Boughter, the Jain, the Shehata
127 and the Harvey datasets, respectively.

128 As therapeutic antibodies are engineered to be closely related to human antibodies to avoid
129 immunogenic responses, it is important to exploit human antibody data for development of optimal
130 ML models. As the Boughter dataset partly consists of mouse IgA antibodies, the sequence similarity
131 of these mouse antibodies was compared to the human antibodies to ensure that there are not too large
132 sequence differences within the dataset. The mouse IgA antibodies appear to differ mostly in the H/L-
133 CDRs (Figure S 1 B). Another notable difference within the Boughter dataset is that the mouse IgA
134 antibodies have a slightly shorter H-CDR3 loop relative to the human antibodies (Figure S 1 C).

135 Ideally, training data sets for classification ML-Models should be balanced when it comes to positive
136 and negative data points. The distribution of non-specificity for the three datasets is visualised in
137 Figure 1 B. The Boughter and the Jain datasets are relatively balanced in terms of specific (zero flags),
138 mildly non-specific ( 1 - 3 flags) and non-specific (>4 flags) antibodies, while the Shehata dataset is
139 unbalanced, with 7 out of 398 antibodies characterised as non-specific only. In this study, the most
140 balanced dataset (i.e. Boughter one) was selected for training of ML models, while the remining three
141 (i.e. Jain, Shehata and Harvey, which consists exclusively of VHH sequences) were used for testing.

142 2.2 Protein language models enable the representation of antibody non-specificity

143 Following the study original study [ 44 ], the Boughter dataset was first parsed into two groups:
144 specific (0 flags) and non-specific group (>3 flags), leaving out the mildly non-specific antibodies (1-
145 3 flags) (Figure 1 A). The amino acid sequences of the parsed dataset were then annotated in the
146 CDRs, and various fragments of the antibody sequences were embedded into vectors representing
147 their physico-chemical and structural properties (i.e. ESM 1b, ESM 1v, ESM 2, Protbert bfd,
148 AntiBERTy, and AbLang2). This procedure resulted into the training of 12 different antibody
149 fragment-specific binary classification models were trained (see Table 4 ). Overall, all of the protein
150 language models (PLMs) performed well with 66 - 71% 10-fold CV accuracy, including the antibody-
151 specific ones AntiBERTy and AbLang2 (Figure 1 C). These deep learning models were trained on

```
made available under aCC-BY-NC 4.0 International license.
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is
```

152 large datasets of protein sequences in the million-to-billion range, encoding protein sequences into
153 vectors for representation of their physiological properties, remote homology, and secondary/tertiary
154 structure. PLMs were originally developed for the prediction of protein contacts and structure [ 81 ,
155 82 ]. Going forward, the Evolutionary Scale Modelling (ESM) 1v was selected as the embedder of
156 choice for this study.

157

```
made available under aCC-BY-NC 4.0 International license.
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is
```

## 158

159 Figure 1. Performance Evaluation of Machine Learning Models for Predicting Antibody Non-Specificity. (A) Schematic
160 workflow of the study. Publicly available datasets containing antibody sequences were used. These sequences were annotated and

```
made available under aCC-BY-NC 4.0 International license.
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is
```

161 embedded using sequence-based biophysical descriptors and protein language models (PLMs). Different ML models were trained and
162 evaluated using k-fold cross-validation, sensitivity-specificity analysis, and external datasets. (B) Histogram showing the distribution
163 of antibody sequences based on the number of flags in the Boughter dataset. Sequences are categorized as Influenza reactive (blue),
164 HIV non-reactive (red), and HIV reactive (light blue). (C) Bar plots showing the validation performance (k-Fold CV and Leave-One
165 Family-Out) for a top performing ML algorithm (LogisticReg) and PLMs across various validation schemes (k-fold CV and leave-one-
166 family-out). (D) Bar plot of 10-fold CV accuracy for different antibody sequences embedded by top performing language model (ESM
167 1v mean-mode). (E) Histogram of predicted probabilities of antibody non-specificity using the VH-based Logistic Regression (ESM
168 1v) model for the Jain dataset. Antibodies are classified into non-specific (dark blue), mildly non-specific (light blue), and specific
169 (red) categories. (F) Boxplot comparing the predicted non-specificity probabilities for antibodies across different datasets using VH-
170 based Logistic Regression (ESM 1v). The boxplot displays the median, interquartile range, and outliers, with significant differences
171 indicated by SCC and p-values (*** indicate p-value <0.001).

172 2.3 The highest PLM-based predictability is achieved by encoding the VH domain

173 An overview of the different antibody fragment-specific models based on the ESM 1v embedder is
174 shown in Figure 1 D. Highest predictability (71% 10-fold CV accuracy of non-specificity) was
175 obtained for the models trained on the VH and H-CDRs sequences. These results suggest that the
176 non-specificity primarily originates from the VH domain, with main contributions from the H-CDR
177 loops. When looking at the models based on the individual H-CDR loops, the order of low-to-high
178 predictability of non-specificity follows H-CDR2, H-CDR 1 and H-CDR3 (Figure 1 D). H-CDR3 has
179 the highest predictability of non-specificity among all the H-CDR loops. The importance of the H-
180 CDR3 loop for non-specificity is in agreement with Guthmiller et al. [ 59 ], who showed by using MD
181 simulation that the flexibility of the H-CDR3 loop plays an important role in the non-specific
182 behaviour of antibodies.

183 Accuracy of around 70% was consistently observed across 3, 5 and 10-Fold CV for the top performing
184 models (Figure 1 C), and similar performance obtained for sensitivity and specificity. Moreover,
185 when looking at the predictability of one antibody family to another, the overall accuracy was
186 consistently above >60% for the Leave-One Family-Out validations. However, when comparing
187 sensitivity and specificity, classifiers trained on human antibodies performed poorly when tested on
188 mouse antibodies. This is not surprising as mouse and human antibodies have notable sequence
189 differences, such as mouse IgA having a shorter H-CDR3 and larger sequence differences in the
190 CDRs relative to human antibodies (Figure S1B). Moreover, classifiers trained on mouse IgA and
191 HIV reactive antibodies perform well across all evaluation metrics (accuracy, sensitivity and
192 specificity) when tested on Influenza reactive antibodies, while classifiers trained on mouse IgA and
193 Influenza reactive antibodies seem to be better in predicting non-specific HIV reactive antibodies
194 than specific ones.

195 2.4 Classification probability of non-specificity against non-specificity ELISA flags mimics
196 regression behaviour

197 A prediction probability of non-specificity was computed in addition to the binary output from the
198 binary classification models. When comparing the prediction probability of non-specificity for all the
199 antibodies from the Boughter dataset (test antibodies sampled from the 10-Fold CV and the mildly
200 non-specific antibodies), three distinct distributions of prediction probabilities for the specific, mildly
201 non-specific and non-specific antibody groups appeared (Figure 1 E). The premise that non-
202 specificity is not a binary property is exemplified by the overlaps between the distributions. This

```
made available under aCC-BY-NC 4.0 International license.
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is
```

203 illustrates that the prediction probability can be used beyond the binary output to assess antibodies of
204 varying degree of non-specificity.

205 When comparing those to non-specificity ELISA flags, a significant regression-like behaviour (SCC
206 0.43) was observed for one of the top performing classifiers, ESM 1v mean-mode VH-based
207 LogisticReg model (Figure 1 F). The prediction probability for non-specificity followed an uptrend
208 when compared to the non-specificity ELISA flags. An exception to this trend was the antibodies
209 with seven non-specificity ELISA flags, as those were exclusively mouse IgA antibodies (differences
210 discussed in previous section).

211 2.5 The isoelectric point: a key biophysical driver of non-specificity

212 To gain insight into the biophysical origins of antibody non-specificity, a set of 68 sequence
213 descriptors (Table S1) was computed for the parsed Boughter dataset. These descriptors encompass
214 a wide range of biophysical properties derived from the antibodies sequence, including theoretical
215 isoelectric point (pI), secondary structure propensity, and hydrophobicity. To assess the presence of
216 redundancy among the descriptors, we constructed a Spearman’s correlation matrix, which revealed
217 that several descriptors, such as hydrophobicity descriptors, exhibited strong correlation among each
218 other (SCC > 0.5, Figure S 9 ), thus indicating redundancy. All the descriptors were ranked according
219 to the absolute logistic regression coefficients (Table S2), whereafter top 25 descriptors were
220 selected, and used for training of a VH-based LogisticReg model. The in-depth analysis of the
221 importance of the 25 descriptors is shown in four different plots in Figure 2 A:

222 • The first plot shows the LogisticReg coefficients, indicating the relative importance of each
223 descriptor. Notably, Disorder_Propensity_DisProt, Aggrescan_a4v, and theoretical pI show
224 significant positive coefficients, suggesting that they are strong drivers of non-specificity.
225 • The second plot displays the permutation importance, highlighting the change in accuracy
226 when each descriptor is permuted. Descriptors like theoretical pI, bulkiness,
227 Hplc_Hfba_retention and Polarity_Zimmerman demonstrate substantial decrease in accuracy
228 upon permutation.
229 • The third plot illustrates the accuracy of models based on single descriptors to underscore
230 their individual predictive power. Theoretical pI resulted in the highest accuracy compared to
231 the other descriptors, confirming its critical role in the prediction of non-specificity.
232 • The fourth plot shows the leave-one-feature-out accuracy, revealing how the exclusion of each
233 descriptor affects the overall model performance. Most of the descriptors result in a minimal
234 drop in accuracy, indicating that the model performance remains unaffected when a certain
235 descriptor is left out. This can be explained by that there remains a certain level of redundancy
236 among the 25 descriptors, e.g. theoretical pI appears to be negatively correlated with
237 Polarity_Zimmerman, according to the Spearman’s correlation matrix in Figure 2 B.

238

239 Table 1. Top 2, 3, 4 and 5 combined VH-based sequence descriptors.

```
Top Descriptors
```
```
made available under aCC-BY-NC 4.0 International license.
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is
```

2 Theoretical pI, Bulkiness
3 Theoretical pI, Bulkiness, Aggrescan_Nr_hotspots
4 Theoretical pI, Average_Flexibility_BP, Beta_Turn_Chou_Fasman, Hplc_Hfba_Retention
5 Theoretical pI, Bulkiness, Disorder_Propensity_DisProt, Percentage_Acessible_Res, Aggrescan_av
240

241 To further narrow down the redundancy, the 25 descriptors were tested in all possible combinations
242 of 2, 3, 4 and 5 descriptors for training of new LogisticReg models. The results of the top descriptors
243 from this analysis are shown in

244 Table 1. The results indicate that, among the top 5 descriptors, the theoretical pI appear to be the most
245 important driver for non-specificity. This conclusion is also supported by the frequency of this
246 particular descriptor among the top models (Figure S10). Additionally, as a parallel check, we
247 performed Principal Component Analysis (PCA) for dimensionality reduction and feature selection.
248 The primary objective of this study was again to address multicollinearity among the descriptors and
249 to identify the most significant features contributing to the variance in the dataset. We thus evaluated
250 the performance of the LogisticReg models trained on the top 3, 5, and 10 principal components
251 identified by PCA. In agreement with our previous findings regarding the theoretical pI, the presence
252 of this descriptor among the selected features significantly influenced the model performance,
253 particularly when it was included in the top 5 and 10 components, but it was absent in the top 3
254 components (Figure S19). The isoelectric point is known to influence PKPD behaviour/clearance of
255 antibodies [ 60 , 61 ].

```
made available under aCC-BY-NC 4.0 International license.
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is
```

## 256

257 Figure 2. Analysis of Descriptor Importance and Model Performance for VH-Based Logistic Regression. (A) Analysis of
258 descriptor importance using various metrics for the VH-based Logistic Regression model; (first panel) Logistic regression coefficients
259 indicating the relative importance of different features, (second panel) permutation importance showing the change in 10 - fold CV
260 accuracy when each descriptor is permuted, (third panel) 10 - fold CV accuracy of models based on single descriptors, and (fourth panel)
261 10 - fold CV accuracy of leave-one-feature-out models compared to the mean accuracy of model using the top 25 descriptors. (B)
262 Heatmap displaying the Spearman's correlation coefficient (SCC) between the top 25 descriptors selected based on highest Logistic
263 Regression coefficient in model with all descriptors. The dendrogram shows hierarchical clustering of descriptors based on their SCC.
264 (C) Bar plot comparing the 10 - fold CV accuracy of different models in predicting antibody non-specificity across various validation
265 schemes: k-fold CV and leave-one-family-out validation. Models compared include VH-based sequences embedded by ESM 1v, all
266 descriptors, PCA with 3, 5 and 10 components, and top 2, 3, 4, and 5 descriptors. Sensitivity and specificity bar plots can be found in
267 Figure S12.

268 Altogether, a comparison between the PLM-based and descriptor-based ML models in terms of
269 accuracy of across different validation schemes is shown in Figure 2 C. The results indicate that the
270 ESM 1v model consistently achieves high accuracy across all validation schemes. The VH-based
271 Logistic Regression model using all descriptors also performs well, though slightly lower than the
272 ESM 1v model. Notably, the PCA-based models show comparable performance, demonstrating the
273 effectiveness of dimensionality reduction in maintaining model accuracy. Interestingly, the VH-based
274 Logistic Regression models using the top descriptors, 2, 3, 4, and 5 combinations (

```
made available under aCC-BY-NC 4.0 International license.
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is
```

275 Table 1 ), exhibit robust performance. This finding suggests that a smaller subset of key descriptors
276 can achieve similar predictive power as using the full set of descriptors, highlighting the potential for
277 model simplification without compromising accuracy.

278 2.6 VH-based LogisticReg classification model is applicable to clinical-stage therapeutic
279 antibodies

280 To show applicability of the non-specificity classification model on therapeutic antibodies, the ESM
281 1v mean-mode VH-based LogisticReg model was tested on the Jain dataset. As in the Boughter
282 dataset, the Jain dataset was parsed into two groups, specific (0 flags) and non-specific (>3 flags),
283 leaving out the mildly non-specific antibodies (1-3 flags). An accuracy of 69% was obtained for the
284 parsed Jain dataset (see confusion matrix in Figure S 14 A). This value is comparable to the mean
285 accuracy of 71% obtained for the same classifier across 3, 5 and 10-Fold CV for the parsed Boughter
286 dataset. Moreover, as in the case of the Boughter dataset, a similar distribution of prediction
287 probability of non-specificity was obtained for the full Jain dataset, and it appears to mimic
288 regression-like behaviour when compared to the non-specificity ELISA flags, although to a slightly
289 weaker extent (Figure 3 A and S 13 ). The same trend can be observed for the top 5 descriptors model
290 (Figure 3 C). The overall performance of the classifier on the Jain dataset illustrates that it can be
291 applied to therapeutic antibodies.

292 2.7 Antibodies characterised by the PSR assay appear to be on a different non-specificity
293 spectrum than that from the non-specificity ELISA assay

294 During recent years, alternative assays to ELISA have been developed to meet the demand of high-
295 throughput screening during drug discovery, and such one is the poly-specific reagent (PSR) assay
296 [ 62 ], where antibodies displayed on the surface of yeast cells are counter-selected when non-
297 specifically bound to soluble membrane protein in a flow cytometry-setup. Several studies have been
298 reported using this assay for assessing antibody non-specificity [ 15 , 58 , 63 ]. Recently, Harvey and co-
299 authors [ 45 ] developed a one-hot LogisticReg model based on > 140 000 clones assessed by the PSR
300 assay from a naïve Nb library. They found a significant correlation of the PSR with the gold-standard
301 ELISA based on six Nbs. To find out whether our ESM 1v mean-mode VH-based LogisticReg model
302 can extend its applicability further to the non-specificity scored by the PSR assay, the Shehata dataset
303 and the VH-based Nb dataset by Harvey and co-authors [ 45 ], here referred to as the Harvey dataset,
304 were tested. The classifier did not appear to separate the PSR-scored specific and non-specific
305 antibodies well. All the specific PSR-scored antibodies of the Shehata dataset were distributed along
306 the entire prediction probability scale, while the few non-specific ones were on the probability end
307 towards higher non-specificity (Figure 3 C,D). A similar forecast was observed for the Harvey
308 dataset; all the specific PSR-scored Nbs resulted in a broad probability distribution, while the non-
309 specific PSR-scored ones resulted in a narrower probability distribution towards higher non-
310 specificity (Figure 3 E,F). Thus, the classifier appears to be better at predicting non-specific PSR-
311 scored antibodies, than specific PSR-scored antibodies. This result suggests that the spectrum of non-
312 specificity from the PSR assay is different than the one from the non-specificity ELISA assay, of
313 which the classifier is trained on. Thus, a specific antibody classified by the PSR assay may
314 necessarily not translate into a specific antibody classified by the non-specificity ELISA assay. The

```
made available under aCC-BY-NC 4.0 International license.
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is
```

315 specific PSR-scored Nbs could partly consist of mildly non-specific clones in addition to specific
316 ones, thus resulting in this broad probability distribution.

317 An interesting remark can be made about the distributions of predicted probabilities obtained from
318 the two different LogisticReg models tested on the Harvey dataset in Figure 3 E,F. The ESM 1v VH-
319 based LogisticReg model produces a more uniform distribution of predicted probabilities across the
320 dataset, while the top 5 descriptors VH-based LogisticReg model exhibits a clear biphasic
321 distribution. It is no surprise that this bimodal pattern closely resembles the distribution of pI (Figures
322 S15-S 18 ), as this descriptor is the main driver of non-specificity in the top 2, 3, 4 and 5 descriptors
323 LogisticReg models (

324 Table 1 and Figure S10). Nonetheless, the distribution of non-specific antibodies in the Harvey
325 dataset appears to exclusively be of high pI (>8) according to Figure S18A. The distributions of the
326 other descriptors do not appear to differ significantly between specific and non-specific antibodies
327 see (Figures S15-S 18 ). The distinct separation suggests that the pI plays a crucial role in
328 differentiating between specific and non-specific antibodies.

```
made available under aCC-BY-NC 4.0 International license.
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is
```

## 329

330 Figure 3. Logistic Regression Models Predicting Antibody Non-Specificity Across Different Datasets. (A-F) Distributions of
331 predicted probabilities of antibody non-specificity for three different datasets using two logistic regression models: predictions for the
332 Jain dataset (A,B), for the Shehata dataset (C,D), and for the Harvey dataset (E,F). (A, C, and E) depict results from the ESM 1v VH-
333 based logistic regression model, while (B, D, and F) depict results from the top 5 descriptors VH-based logistic regression model. For
334 each dataset, antibodies are classified into specific, mildly non-specific (only in the Jain dataset), and non-specific categories,
335 represented by different colours.

336

```
made available under aCC-BY-NC 4.0 International license.
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is
```

337 2.8 VH-based LogisticReg models performs on par or better than existing predictors

338 The ESM 1v VH-based LogisticReg model can be compared to two existing predictors in the
339 literature - the predictors reported in the Boughter et al. study [ 44 ], and the Harvey et al. study [ 45 ].
340 Boughter and colleagues stated that while no notable difference could be observed between specific
341 and non-specific antibodies in both gene usage level and amino acid-usage level in CDRs, the
342 positional context of biophysical properties can show the differences. They showed to be successful
343 in developing a binary classifier based on a position-sensitive biophysical matrix with accuracy up to
344 75%. Their reported performance is on par with the achieved performance of the PLM-based classifier
345 (ESM 1v VH-based LogisticReg), which was trained on the same data (parsed Boughter dataset).

346 Furthermore, Harvey and colleagues developed a one-hot LogisticReg model based on >140 000
347 clones assessed by the PSR assay from a naïve Nb library with an accuracy >80%. Using their
348 published web-based predictor [ 64 ], we tested its performance on the Boughter, Jain, and Shehata
349 datasets. The results show that the Harvey predictor does not separate well the different antibody
350 groups in the Boughter dataset (Figure S19A,B), with overlapping distributions of prediction scores.
351 Similarly, the Jain and the Shehata datasets demonstrate significant overlap between specific and non-
352 specific antibodies (Figure S19C-F), indicating some limitations for the Harvey method in predicting
353 non-specificity of antibodies as compared to Nbs.

354 2.9 Prediction of non-specificity in antibody drug development programs

355 Consequences of non-specificity in the clinic: Non-specific binding of therapeutic antibodies can lead
356 to significant adverse effects in the clinic. Such antibodies can bind to structurally unrelated off-
357 targets and thereby potentially result in unwanted toxicity [ 65 ] or reduced efficacy [ 66 ]. They can
358 also interact with tissues like subcutis and thereby result in faster clearance via pinocytosis
359 independently of FcRn [ 60 , 61 , 67 ]. Ultimately, non-specificity can compromise the safety and
360 efficacy of therapeutic antibodies, potentially resulting in clinical trial failures and increased
361 development costs. Thus, early-stage prediction of non-specificity, such as during selection and
362 optimisation stage, is essential to reduce the risk of failing at late-stage during clinical trials.
363 Otherwise, the further into the development program, the harder it becomes to allow additional
364 protein engineering to mitigate biophysical liabilities, as new in vitro and in vivo data must be
365 reproduced.

366 A powerful strategy to address this problem is to combine in silico prediction with in vitro
367 developability assessment. To identify and flag non-specific antibodies, we propose a combined
368 strategy that integrates in silico prediction models with traditional in vitro developability assessments
369 during the lead optimization stage in the drug development process. This hybrid approach leverages
370 the strengths of computational predictions and experimental validations, ensuring the selection of
371 lead candidates with high developability potential.

# 372 3. Conclusions

373 In this study, we developed ML models to predict the non-specificity of antibodies, utilizing both
374 PLMs and biophysical properties to embed antibody sequences. In agreement with previous reports

```
made available under aCC-BY-NC 4.0 International license.
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is
```

375 on different datasets [ 68 ], our results indicate that the VH domain, particularly the H-CDR loops, as
376 the main contributor to non-specificity, and that the biophysical parameter pI is a key biophysical
377 driver of non-specificity. The resulting computational models enable the prediction of non-specific
378 interactions of antibodies with accuracy of 71% in 10 - fold CV, thus providing a valuable tool to guide
379 the design and selection of monoclonal antibodies with improved specificity and efficacy. These
380 findings have important implications for the development of safe and efficacious lead candidates with
381 high developability potential.
382

# 383

```
made available under aCC-BY-NC 4.0 International license.
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is
```

# 384 4. Methods

385 4.1 Data sources

386 All antibody datasets used in this study were retrieved from public sources only. A list of the datasets
387 and their corresponding sources are reported Table 2.

388 Table 2. List of public antibody datasets with their corresponding size, non-specificity assay and reference.

```
Dataset Size Poly-reactive assay Reference
Boughter
dataset
```
```
>1000 antibodies (HIV-1 broadly
neutralizing, Influenza reactive, IgA
mouse) of varying degree of non-
specificity
```
```
ELISA with a panel of 7
ligands (DNA, insulin,
LPS, albumin, cardiolipin,
flagellin, KLH)
```
```
[ 44 ]
```
```
Jain dataset 137 clinical stage IgG1-formatted
antibodies
```
```
ELISA with a panel of 6
ligands (ssDNA, dsDNA,
insulin, LPS, cardiolipin,
KLH)
```
```
[ 15 ]
```
```
Shehata dataset 398 antibodies from naïve, IgG memory,
IgM memory and long-lived plasma cells
```
```
Poly-specific reagent
(PSR) assay
```
```
[ 58 ]
```
```
Harvey dataset >140 000 naïve nanobodies Poly-specific reagent
(PSR) assay
```
```
[ 45 ]
```
389

390 4.2 Python programming

391 All coding was performed in Python using Spyder IDE and Jupyter Notebook (Anaconda software
392 distribution) [ 69 ], and a list of used Python modules is reported in Table 3.

393 Table 3. List of software and Python modules.

```
Module Additional information Reference
NumPy https://numpy.org [ 70 ]
SciPy https://www.scipy.org [ 71 ]
Statsmodels https://www.statsmodels.org [ 72 ]
Pandas https://pandas.pydata.org [ 73 ]
Matplotlib https://matplotlib.org [ 74 ]
Seaborn https://seaborn.pydata.org [ 75 ]
Scikit-Learn https://scikit-learn.org [ 76 ]
Json https://docs.python.org/3/library/json [ 77 ]
Collections https://docs.python.org/3/library/collections [ 78 ]
Itertools https://docs.python.org/3/library/itertools [ 79 ]
ANARCI https://github.com/oxpig/ANARCI [ 80 ]
```
394 4.3 Training and validation of binary classification models

395 First, the Boughter dataset was parsed into three groups as previously done in [ 44 ]: specific group (
396 flags), mildly poly-reactive group (1-3 flags) and poly-reactive group (>3 flags). The primary

```
made available under aCC-BY-NC 4.0 International license.
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is
```

397 sequences were annotated in the CDRs using ANARCI following the IMGT numbering scheme.
398 Following this, 1 6 different antibody fragment sequences were assembled and embedded by three
399 state-of-the-art protein language models (PLMs), ESM 1v [ 81 ], Protbert bfd [ 82 ], and AbLang2 [ 83 ],
400 for representation of the physico-chemical properties and secondary/tertiary structure, and a physico-
401 chemical descriptor of amino acids, the Z-scale [ 84 ] Table 4 ). For the embeddings from the PLMs,
402 mean (average of all token vectors) was used. The vectorised embeddings were served as features for
403 training of binary classification models (e.g. LogisticReg, RandomForest, GaussianProcess,
404 GradeintBoosting and SVM algorithms) for non-specificity (class 0: specific group, and class 1: poly-
405 reactive group). The mildly poly-reactive group was left out from the training of the models.

406 Table 4. Type and description of sequence input for the binary classification models.

```
Type of input Description
VL, VH,
L-CDR 1- 3 ,
H-CDR 1- 3 ,
```
```
A vectorised embedding of VL, VH or an individual CDR sequence
```
```
VH/VL joined,
L-CDRs joined,
H-CDRs joined,
H/L-CDRs joined
```
```
A vectorised embedding of a joined sequence
```
407 The trained classification models were validated by (i) 3, 5 and 10-Fold cross-validation (CV), (ii)
408 Leave-One Family-Out validation, e.g. training on HIV and Influenza reactive antibodies, while
409 testing on mouse IgA antibodies, (iii) comparing probability of predicted poly-reactive class to true
410 class, and (iv) testing on the Jain dataset. The evaluation metrics included accuracy, sensitivity and
411 specificity (Eqs. 1-3).

```
𝐴𝑐𝑐𝑢𝑟𝑎𝑐𝑦=
𝑇𝑃+𝑇𝑁
𝑇𝑃+𝑇𝑁+𝐹𝑃+𝐹𝑁^
(1)^
```
```
𝑆𝑒𝑛𝑠𝑖𝑡𝑖𝑣𝑖𝑡𝑦=
𝑇𝑃
𝑃^
```
```
(2)
```
```
𝑆𝑝𝑒𝑐𝑖𝑓𝑖𝑐𝑖𝑡𝑦=
𝑇𝑁
𝑁^
```
```
(3)
```
412 Where TP is true positive (true poly-reactive), TN is true negative (true specific), FP is false positive
413 (false poly-reactive), FN is false negative (false specific), P is all positives (all poly-reactive), and N
414 is all negatives (all specific).

# 415 Acknowledgements

416 We would like to thank Mauricio Augilar Rangel, Dillon Rinauro and Ross Taylor from the
417 University of Cambridge for their valuable discussions to this work.

```
made available under aCC-BY-NC 4.0 International license.
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is
```

# 418 Funding

419 Financial support from Novo Nordisk A/S is acknowledged.

420 P.S. is a Royal Society University Research Fellow (grant no. URF\R1\201461) and acknowledges
421 funding from UK Research and Innovation (UKRI), and Engineering and Physical Sciences Research
422 Council (grant no. EP/X024733/1).

423 The authors declare no competing financial interest.

# 424

```
made available under aCC-BY-NC 4.0 International license.
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is
```

# 425 References

```
[ 1 ] A. Mullard, FDA approves 100th monoclonal antibody product. Nat Rev (2021) 491 - 495.
```
```
[ 2 ] H. Kaplon, A. Chenoweth, S. Crescioli, J.M. Reichert, Antibodies to watch in 2022. mAbs
(2022) e2014296.
```
```
[ 3 ] R.M. Lu, Y.C. Hwang, I.J. Liu, C.C. Lee, H.Z. Tsai, H.J. Li, H.C. Wu. Development of therapeutic
antibodies for the treatment of diseases. J Biomed Sci (2020) 1-30.
```
```
[ 4 ] A. Pedrioli, A. Oxenius, Single B cell technologies for monoclonal antibody discovery. Trends
Immunol (2021) 1143 - 1158.
```
```
[ 5 ] M. Tabasinezhad, Y. Talebkhan, W. Wenzel, H. Rahimi, E. Omidinia, F. Mahboudi, Trends in
therapeutic antibody affinity maturation: From in-vitro towards next-generation sequencing
approaches. Immunol Lett (2019) 106-113.
```
```
[ 6 ] T.M. Chidyausiku, S.R. Mendes, J.C. Klima, M. Nadal , U. Eckhard , J. Roel-Touris, S. Houliston,
T. Guevara, H.K. Haddox, A. Moyer, C.H. Arrowsmith, F.X. Gomis-Rüth, D. Baker, E. Marcos, De
novo design of immunoglobulin-like domains. Nat Commun ( 2022 ) 5661.
```
```
[ 7 ] J.L. Watson, D. Juergens, N.R. Bennett, B.L. Trippe, J. Yim, H.E. Eisenach, W. Ahern, A.J. Borst,
R.J. Ragotte, L.F. Milles, B.I.M. Wicky, N. Hanikel, S.J. Pellock, A. Courbet, W. Sheffler, J. Wang,
P. Venkatesh, I. Sappington, S.V. Torres, A. Lauko, V. De Bortoli, E. Mathieu, S. Ovchinnikov, R.
Barzilay, T.S. Jaakkola, F. DiMaio, M. Baek, D. Baker, De novo design of protein structure and
function with RFdiffusion. Nature ( 2023 ) 10.1038/s41586- 023 - 06415 - 8.
```
```
[ 8 ] E.T. Boder, K.S. Midelfort, K.D. Wittrup, Directed evolution of antibody fragments with
monovalent femtomolar antigen-binding affinity. Proceedings of the National Academy of Sciences
USA (2000) 10701 - 10705.
```
```
[ 9 ] T. Igawa, S. Ishii, T. Tachibana, A. Maeda, Y. Higuchi, S. Shimaoka, C. Moriyama, T. Watanabe,
R. Takubo, Y. Doi, T. Wakabayashi, A. Hayasaka, S. Kadono, T. Miyazaki, K. Haraya, Y. Sekimori,
T. Kojima, Y. Nabuchi, Y. Aso, Y. Kawabe, K. Hattori, Antibody recycling by engineered pH-
dependent antigen binding improves the duration of antigen neutralization. Nat Biotechnol ( 2010 )
1203 - 1207.
```
```
[ 10 ] T. Klaus, S. Deshmukh, pH-responsive antibodies for therapeutic applications. J. Biomed. Sci.
(2021) 10.1186/s12929- 021 - 00709 - 7.
```
```
[ 11 ] M. Kamata-Sakurai, Y. Narita, Y. Hori, T. Nemoto, R. Uchikawa, M. Honda, N. Hironiwa, K.
Taniguchi, M. Shida-Kawazoe, S. Metsugi, T. Miyazaki, N.A. Wada, Y. Ohte, S. Shimizu, H.
Mikami, T. Tachibana, N. Ono, K. Adachi, T. Sakiyama, T. Matsushita, S. Kadono, S.I. Komatsu,
Akihisa Sakamoto, S. Horikawa, A. Hirako, K. Hamada, S. Naoi, N. Savory, Y. Satoh, M. Sato, Y.
```
```
made available under aCC-BY-NC 4.0 International license.
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is
```

```
Noguchi, J. Shinozuka, H. Kuroi, A. Ito, T. Wakabayashi, M. Kamimura, F. Isomura, Y. Tomii, N.
Sawada, A. Kato, O. Ueda, Y. Nakanishi, M. Endo, K.I. Jishage, Y. Kawabe, T. Kitazawa, T. Igawa,
Antibody to CD137 Activated by Extracellular Adenosine Triphosphate Is Tumor Selective and
Broadly Effective In Vivo without Systemic Immune Activation. Cancer Discov. ( 2021 ) 158 - 175.
```
```
[ 12 ] M. Elshiaty, H. Schindler, P. Christopoulos, Principles and Current Clinical Landscape of
Multispecific Antibodies against Cancer. Int J Mol Sci ( 2021 ) 5632.
```
```
[ 13 ] H. Østergaard, J. Lund, P.J. Greisen, S. Kjellev, A. Henriksen, N. Lorenzen, E. Johansson, G.
Røder, M.G. Rasch, L.B. Johnsen, T. Egebjerg, S. Lund, H. Rahbek-Nielsen, P.S. Gandhi, K.
Lamberth, M. Loftager, L.M. Andersen, A.C. Bonde, F. Stavenuiter, D.E. Madsen, X. Li, T.L. Holm,
C.D. Ley, P. Thygesen, H. Zhu, R. Zhou, K. Thorn, Z. Yang, M.B. Hermit, J.R. Bjelke, B.G. Hansen,
I. Hilden, A factor VIIIa-mimetic bispecific antibody, Mim8, ameliorates bleeding upon severe
vascular challenge in hemophilia A mice. Blood ( 2021 ) 1258 - 1268.
```
```
[ 14 ] C.G. Starr, P.M. Tessier, Selecting and engineering monoclonal antibodies with drug-like
specificity. Curr Opin Biotechnol ( 2019 ) 119 - 127.
```
```
[ 15 ] T. Jain, T. Sun, S. Durand, A. Hall, N.R. Houston, J.H. Nett, B. Sharkey, B. Bobrowicz, I. Caffry,
Y. Yu, Y. Cao, H. Lynaugh, M. Brown, H. Baruah, L.T. Gray, E.M. Krauland, Y. Xu, M. Vásquez,
K.D. Wittrup, Biophysical properties of the clinical-stage antibody landscape. Proceedings of the
National Academy of Sciences USA (2017) 944-949.
```
```
[ 16 ] L.B. Avery, J. Wade, M. Wang, A. Tam, A. King, N. Piche-Nicholas, M.S. Kavosi, S. Penn, D.
Cirelli, J.C. Kurz, M. Zhang, O. Cunningham, R. Jones, B.J. Fennell, B. McDonnell, P. Sakorafas, J.
Apgar, W.J. Finlay, L. Lin, L. Bloom, D.M. O'Hara. Establishing in vitro in vivo correlations to
screen monoclonal antibodies for physicochemical properties related to favorable human
pharmacokinetics. MAbs ( 2018 ) 244 - 255.
```
```
[ 17 ] R.L. Kelly, T. Sun, T. Jain, I. Caffry, Y. Yu, Y. Cao, H. Lynaugh, M. Brown, M. Vásquez, K.D.
Wittrup, Y. Xu, High throughput cross-interaction measures for human IgG1 antibodies correlate
with clearance rates in mice. MAbs ( 2015 ) 770 - 77 7.
```
```
[ 18 ] T.E. Kraft, W.F. Richter, T. Emrich, A. Knaupp, M. Schuster, A. Wolfert, H. Kettenberger,
Heparin chromatography as an in vitro predictor for antibody clearance rate through pinocytosis.
MAbs ( 2020 ) 1683432.
```
```
[ 19 ] C.L. Dobson, P.W. Devine, J.J. Phillips, D.R. Higazi, C. Lloyd, B. Popovic, J. Arnold, A.
Buchanan, A. Lewis, J. Goodman, C.F. van der Walle, P. Thornton, L. Vinall, D. Lowne, A. Aagaard,
L.L. Olsson, A. Ridderstad Wollberg, F. Welsh, T.K. Karamanos, C.L. Pashley, M.G. Iadanza, N.A.
Ranson, A.E. Ashcroft, A.D. Kippen, T.J. Vaughan, S.E. Radford, D.C. Lowe, Engineering the
```
made available under aCC-BY-NC 4.0 International license.
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is


```
surface properties of a human monoclonal antibody prevents self-association and rapid clearance in
vivo. Sci Rep ( 2016 ) 38644.
```
```
[ 20 ] A. Datta-Mannan, J. Lu, D.R. Witcher, D. Leung, Y. Tang, V.J. Wroblewski, The interplay of
non-specific binding, target-mediated clearance and FcRn interactions on the pharmacokinetics of
humanized antibodies. MAbs ( 2015 ) 1084 - 10 93.
```
```
[ 21 ] A. Datta-Mannan, A. Thangaraju, D. Leung, Y. Tang, D.R. Witcher, J. Lu, V.J. Wroblewski,
Balancing charge in the complementarity-determining regions of humanized mAbs without affecting
pI reduces non-specific binding and improves the pharmacokinetics. MAbs ( 2015 ) 483 - 493.
```
```
[ 22 ] T. Igawa, H. Tsunoda, T. Tachibana, A. Maeda, F. Mimoto, C. Moriyama, M. Nanami, Y.
Sekimori, Y. Nabuchi, Y. Aso, K. Hattori, Reduced elimination of IgG antibodies by engineering the
variable region. Protein Eng Des Sel ( 2010 ) 385 - 3 92.
```
```
[ 23 ] D. Bumbaca, A. Wong, E. Drake, A.E. Reyes II, B.C. Lin, J.P. Stephan, L. Desnoyers, B.Q.
Shen, M.S. Dennis, Highly specific off-target binding identified and eliminated during the
humanization of an antibody against FGF receptor 4. mAbs (2011) 376-386.
```
```
[ 24 ] K.E. Tiller, L. Li, S. Kumar, M.S. Julian, S. Garde, P.M. Tessier, Arginine mutations in antibody
complementarity-determining regions display context-dependent affinity/specificity trade-offs. J Biol
Chem, ( 2017 ) 16638 - 16652.
```
```
[ 25 ] R.L. Kelly, D. Le, J. Zhao, K.D. Wittrup, Reduction of Nonspecificity Motifs in Synthetic
Antibody Libraries. J Mol Biol ( 2018 ) 119 - 130.
```
```
[ 26 ] H. Ausserwöger, M.M. Schneider, T.W. Herling, P. Arosio, G. Invernizzi, T.P.J. Knowles, N.
Lorenzen, Non-specificity as the sticky problem in therapeutic antibody development. Nat Rev Chem
( 2022 ) 844 - 861.
```
```
[ 27 ] O. Cunningham, M. Scott, Z.S. Zhou, W.J.J. Finlay, Polyreactivity and polyspecificity in
therapeutic antibody development: risk factors for failure in preclinical and clinical development
campaigns. MAbs ( 2021 ) 1999195.
```
```
[ 28 ] K.E. Tiller, L. Li, S. Kumar, M.S. Julian, S. Garde, P.M. Tessier, Arginine mutations in antibody
complementarity-determining regions display context-dependent affinity/specificity trade-offs. J Biol
Chem, ( 2017 ) 16638 - 16652.
```
```
[ 29 ] R.L. Kelly, D. Le, J. Zhao, K.D. Wittrup, Reduction of Nonspecificity Motifs in Synthetic
Antibody Libraries. J Mol Biol ( 2018 ) 119 - 130.
```
made available under aCC-BY-NC 4.0 International license.
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is


```
[ 30 ] H. Ausserwöger, M.M. Schneider, T.W. Herling, P. Arosio, G. Invernizzi, T.P.J. Knowles, N.
Lorenzen, Non-specificity as the sticky problem in therapeutic antibody development. Nat Rev Chem
( 2022 ) 844 - 861.
```
```
[ 31 ] O. Cunningham, M. Scott, Z.S. Zhou, W.J.J. Finlay, Polyreactivity and polyspecificity in
therapeutic antibody development: risk factors for failure in preclinical and clinical development
campaigns. MAbs ( 2021 ) 1999195.
```
```
[ 32 ] J.P. Palmer, C.M. Asplin, P. Clemons, K. Lyen, O. Tatpati, P.K. Raghu, T.L. Paquette, Insulin
antibodies in insulin-dependent diabetics before insulin treatment. Science ( 1983 ) 1337 - 1339.
```
```
[ 33 ] C.E. Taplin, J.M. Barker, Autoantibodies in type 1 diabetes. Autoimmunity ( 2008 ) 11 - 18.
```
```
[ 34 ] P.W. Noble, S. Bernatsky, A.E. Clarke, D.A. Isenberg, R. Ramsey-Goldman, J.E. Hansen, DNA-
damaging autoantibodies and cancer: the lupus butterfly theory. Nat Rev Rheumatol ( 2016 ) 429 - 434.
```
```
[ 35 ] J. Nehring, L.A. Schirmbeck, J. Friebus-Kardash, D. Dubler, U. Huynh-Do, C. Chizzolini, C.
Ribi, M. Trendelenburg, Autoantibodies Against Albumin in Patients With Systemic Lupus
Erythematosus. Front Immunol ( 2018 ) 10.1128/cdli.6.6.775-782.1999.
```
```
[ 36 ] S. Miyakis, M.D. Lockshin, T. Atsumi, D.W. Branch, R.L. Brey, R. Cervera, R.H. Derksen, P.G.
DE Groot, T. Koike, P.L. Meroni, G. Reber, Y. Shoenfeld, A. Tincani, P.G. Vlachoyiannopoulos,
S.A. Krilis, International consensus statement on an update of the classification criteria for definite
antiphospholipid syndrome (APS). J Thromb Haemost ( 2006 ) 295 - 306.
```
```
[ 37 ] I.R. Poxton, Antibodies to lipopolysaccharide. J Immunol Methods (1995) 1-15.
```
```
[ 38 ] H. Mouquet, J.F. Scheid, M.J. Zoller, M. Krogsgaard, R.G. Ott, S. Shukair, M.N. Artyomov, J.
Pietzsch, M. Connors, F. Pereyra, B.D. Walker, D.D. Ho, P.C. Wilson, M.S. Seaman, H.N. Eisen,
A.K. Chakraborty, T.J. Hope, J.V. Ravetch, H. Wardemann, M.C. Nussenzweig, Polyreactivity
increases the apparent affinity of anti-HIV antibodies by heteroligation. Nature (2010) 591-595.
```
```
[ 39 ] J.J. Guthmiller, L.Y. Lan, M.L. Fernández-Quintero, J. Han, H.A. Utset, D.J. Bitar, N.J. Hamel,
O. Stovicek, L. Li, M. Tepora, C. Henry, K.E. Neu, H.L. Dugan, M.T. Borowska, Y.Q. Chen, S.T.H.
Liu, C.T. Stamper, N.Y. Zheng, M. Huang, A.E. Palm, A. García-Sastre, R. Nachbagauer, P. Palese,
L. Coughlan, F. Krammer, A.B. Ward, K.R. Liedl, P.C. Wilson, Polyreactive Broadly Neutralizing
B cells Are Selected to Provide Defense against Pandemic Threat Influenza Viruses. Immunity ( 2020 )
1230 - 1244.
```
```
[ 40 ] I. Hötzel, F.P. Theil, L.J. Bernstein, S. Prabhu, R. Deng, L. Quintana, J. Lutman, R. Sibia, P.
Chan, D. Bumbaca, P. Fielder, P.J. Carter, R.F. Kelley, A strategy for risk mitigation of antibodies
with fast clearance. MAbs ( 2012 ) 753 - 7 60.
```
made available under aCC-BY-NC 4.0 International license.
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is


```
[ 41 ] Y. Xu, W. Roach, T. Sun, T. Jain, B. Prinz, T.Y. Yu, J. Torrey, J. Thomas, P. Bobrowicz, M.
Vásquez, K.D. Wittrup, E. Krauland, Addressing polyspecificity of antibodies selected from an in
vitro yeast presentation system: a FACS-based, high-throughput selection and analytical tool. Protein
Eng Des Sel ( 2013 ) 663 - 670.
```
```
[ 42 ] T.E. Kraft, W.F. Richter, T. Emrich, A. Knaupp, M. Schuster, A. Wolfert, H. Kettenberger,
Heparin chromatography as an in vitro predictor for antibody clearance rate through pinocytosis.
MAbs ( 2020 ) 1683432.
```
```
[ 43 ] R.L. Kelly, T. Sun, T. Jain, I. Caffry, Y. Yu, Y. Cao, H. Lynaugh, M. Brown, M. Vásquez, K.D.
Wittrup, Y. Xu, High throughput cross-interaction measures for human IgG1 antibodies correlate
with clearance rates in mice. MAbs ( 2015 ) 770 - 777.
```
```
[ 44 ] C.T. Boughter, M.T. Borowska, J.J. Guthmiller, A. Bendelac, P.C. Wilson, B. Roux, E.J. Adams,
Biochemical patterna of antibody polyreactivity revealed through a bioinformatics-based analysis of
CDR loops. eLife (20 20 ) 9:e61393.
```
```
[ 45 ] E.P. Harvey, J.E. Shin, M.A. Skiba, G.R. Nemeth, J.D. Hurley, A. Wellner, A.Y. Shaw, V.G.
Miranda, J.K. Min, C.C. Liu, D.S. Marks, A.C. Kruse, An in silico method to assess antibody
fragment polyreactivity. Nat Commun (2022) 13, 7554.
```
```
[ 46 ] P.A. Robert, R. Akbar, R. Frank, M. Pavlović, M. Widrich, I. Snapkov, A. Slabodkin, M.
Chernigovskaya, L. Scheffer, E. Smorodina, P. Rawat, B. Bhushan Mehta, M. Ha Vu, I. Frøberg
Mathisen, A. Prósz, K. Abram, A. Olar, E. Miho, D. Trygve Tryslew Haug, F. Lund-Johansen, S.
Hochreiter, I. Hobæk Haff, G. Klambauer, G. Kjetil Sandve, V. Greiff, Unconstrained generation of
synthetic antibody–antigen structures to guide machine learning methodology for antibody specificity
prediction. Nat Comput Sci (2022) 10.1038/s43588- 022 - 00372 - 4.
```
```
[ 47 ] E.K. Makowski, P.C. Kinnunen, J. Huang, L. Wu, M.D. Smith, T. Wang, A.A. Desai, C.N.
Streu, Y. Zhang, J.M. Zupancic, J.S. Schardt, J.J. Linderman, P.M. Tessier, Co-optimization of
therapeutic antibody affinity and specificity using machine learning models that generalize to novel
mutational space. Nat Commun ( 2022 ) 3788.
```
```
[ 48 ] R.L. Kelly, D. Le, J. Zhao, K.D. Wittrup, Reduction of nonspecificity motifs in synthetic
antibody libraries. J Mol Biol (2018) 13, 119-130.
```
```
[ 49 ] A.A.R. Teixeira, S. D'Angelo, M.F. Erasmus, C. Leal-Lopes, F. Ferrara, L.P. Spector, L.
Naranjo, E. Molina, T. Max, A. DeAguero, K. Perea, S. Stewart, R.A. Buonpane, H.G. Nastri, A.R.M.
Bradbury, Simultaneous affinity maturation and developability enhancement using natural liability-
free CDRs. MAbs (2022) 14, 2115200.
```
made available under aCC-BY-NC 4.0 International license.
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is


```
[ 50 ] Hie, Brian L., et al. "Efficient evolution of human antibodies from general protein language
models." Nature biotechnology 42.2 (2024): 275-283.
```
```
B.L. Hie, V.R. Shanker, D. Xu, T.U.J. Bruun, P.A. Weidenbacher, S. Tang, W. Wu, J.E. Pak, P.S.
Kim, Efficient evolution of human antibodies from general protein language models. Nat Biotechnol
( 2024 ) 42 , 275 - 283.
```
```
[ 51 ] T.H. Olsen, I.H. Moal, C.M. Deane, AbLang: an antibody language model for completing
antibody sequences. Bioinform Adv ( 2022 ) 10.1093/bioadv/vbac046.
```
```
[ 52 ] V.R. Shanker, T.U.J. Bruun, B.L. Hie, P.S. Kim, Unsupervised evolution of protein and antibody
complexes with a structure-informed language model. Science (2024) 385, 46-53.
```
```
[ 53 ] R. Singh, C. Im, Y. Qiu, B. Mackness, A. Gupta, T. Joren, S. Sledzieski, L. Erlach, M. Wendt,
Y.F. Nanfack, B. Bryson, B. Berger, Learning the language of antibody hypervariability. Proceedings
of the National Academy of Sciences USA (2025) 122, e2418918121.
```
```
[ 54 ] D.M. Mason, S. Friedensohn, C.R. Weber, C. Jordi, B. Wagner, S.M. Meng, R.A. Ehling, L.
Bonati, J. Dahinden, P. Gainza, B.E. Correia, S.T. Reddy, Optimization of therapeutic antibodies by
predicting antigen specificity from antibody sequence via deep learning. Nat Biomed Eng ( 2021 ) 5 ,
600 - 612.
```
```
[ 55 ] Y. Wang, H. Lv, Q.W. Teo, R. Lei, A.B. Gopal, W.O. Ouyang, Y.H. Yeung, T.J.C. Tan, D. Choi,
I.R. Shen, X. Chen, C.S. Graham, N.C. Wu, An explainable language model for antibody specificity
prediction using curated influenza hemagglutinin antibodies. Immunity ( 2024 ) 8 , 2453 - 2465.
```
```
[ 56 ] M. Wang, J. Patsenker, H. Li, Y. Kluger, S.H. Kleinstein, Supervised fine-tuning of pre-trained
antibody language models improves antigen specificity prediction. PLOS Comput Biol 21.3 (2025)
e1012153.
```
```
[ 57 ] X. Yu, K. Vangjeli, A. Prakash, M. Chhaya, S.J. Stanley, N. Cohen, L. Huang, Protein language
models enable prediction of polyreactivity of monospecific, bispecific, and heavy-chain-only
antibodies. Antib Ther ( 2024 ) 30 , 199 - 208.
```
```
[ 58 ] L. Shehata, D.P. Maurer, A.Z. Wec, A. Lilov, E. Champney, T. Sun, K. Archambault, I. Burnina,
H. Lynaugh, X. Zhi, Y. Xu, L.M. Walker, Affinity maturation enhances antibody specificity but
compromises conformational stability. Cell Reports (2019) 3300-3308.
```
```
[ 59 ] J.J. Guthmiller, L. Yu-Ling Lan, M.L. Fernández-Quintero, J. Han, H.A. Utset, D.J. Bitar, N. J.
Hamel, O. Stovicek, L. Li, M. Tepora, C. Henry, K.E. Neu, H.L. Dugan, M.T. Borowska, Y.Q. Chen,
S.T.H. Liu, C.T. Stamper, N.Y. Zheng, M. Huang, A.K.E. Palm, P.C. Wilson, Polyreactive Broadly
```
made available under aCC-BY-NC 4.0 International license.
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is


```
Neutralizing B cells Are Selected to Provide Defense against Pandemic Threat Influenza Viruses.
Immunity (2020) 53, 1230-1244.
```
```
[ 60 ] R.L. Kelly, Y. Yu, T. Sun, I. Caffry, H. Lynaugh, M. Brown, T. Jain, Y. Xu, K.D. Wittrup,
Target-independent variable region mediated effects on antibody clearance can be FcRn independent.
Mabs ( 2016 ) 8 , 1269 - 1275.
```
```
[ 61 ] B. Li, D. Tesar, C.A. Boswell. H.S. Cahaya, A. Wong, J. Zhang, Y.G. Meng, C. Eigenbrot, H.
Pantua, J. Diao, S.B Kapadia, R. Deng, R.F. Kelley. Framework selection can influence
pharmacokinetics of a humanized therapeutic antibody through differences in molecule charge. MAbs
( 2014 ) 6 , 1255 - 1264.
```
```
[ 62 ] Y. Xu, W. Roach, T. Sun, T. Jain, B. Prinz, T.Y. Yu, J. Torrey, J. Thomas, P. Bobrowicz, M.
Vásquez, K.D. Wittrup, E. Krauland, Addressing polyspecificity of antibodies selected from an in
vitro yeast presentation system: a FACS-based, high-throughput selection and analytical tool. Protein
Engineering, Design and Selection (2013) 26, 663- 670.
```
```
[ 63 ] R.L. Kelly, T. Sun, T. Jain, I. Caffry, Y. Yu, Y. Cao, H. Lynaugh, M. Brown, M. Vásquez, K.D.
Wittrup, Y. Xu, High throughput cross-interaction measures for human IgG1 antibodies correlate
with clearance rates in mice. mAbs (2015) 7, 770 - 777.
```
```
[ 64 ] Web-based predictor of nanobody non-specificity available at Nanobody Polyreactivity
Prediction Server.
```
```
[ 65 ] W.J.J. Finlay, J.E. Coleman, J.S. Edwards, K.S. Johnson, Anti-PD1 'SHR-1210' aberrantly
targets pro-angiogenic receptors and this polyspecificity can be ablated by paratope refinement. MAbs
( 2019 ) 11 , 26 - 44.
```
```
[ 66 ] D. Bumbaca, A. Wong, E. Drake, A.E. Reyes 2nd, B.C. Lin, J.P. Stephan, L. Desnoyers, B.Q.
Shen, M.S. Dennis, Highly specific off-target binding identified and eliminated during the
humanization of an antibody against FGF receptor 4. MAbs ( 2011 ) 3 , 376 - 386.
```
```
[ 67 ] C.A. Boswell, D.B. Tesar, K. Mukhyala, F.P. Theil, P.J. Fielder, L.A. Khawli, Effects of charge
on antibody tissue distribution and pharmacokinetics. Bioconjug Chem ( 2010 ) 21 , 2153 - 2163.
```
```
[ 68 ] H.T. Chen, Y. Zhang, J. Huang, M. Sawant, M.D. Smith, N. Rajagopal, A.A. Desai, E.
Makowski, G. Licari, Y. Xie, M.S. Marlow, S. Kumar, P.M. Tessier, Human antibody polyreactivity
is governed primarily by the heavy-chain complementarity-determining regions. Cell Rep ( 2024 ) 22 ,
10.1016/j.celrep.2024.114801.
```
```
[ 69 ] Anaconda Software Distribution, Anaconda Documentation. Anaconda Inc (2020) Retrieved
from https://docs.anaconda.com/.
```
made available under aCC-BY-NC 4.0 International license.
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is


```
[ 70 ] C.R. Harris, K.J. Millman, S.J. van der Walt et al., Array programming with NumPy.
Nature 585 (2020) 357 – 362.
```
```
[ 71 ] P. Virtanen, R. Gommers, T.E. Oliphant et al., SciPy 1.0: fundamental algorithms for scientific
computing in Python. Nat Methods 17 (2020) 261 – 272.
```
```
[ 72 ] Seabold, Skipper, Josef Perktold, statsmodels: Econometric and statistical modeling with
python. Proceedings of the 9th Python in Science Conference ( 2010 ).
```
```
[ 73 ] W. McKinney, Data Structures for Statistical Computing in Python, Proceedings of the 9th
Python in Science Conference (2010).
```
```
[ 74 ] J.D. Hunter, Matplotlib: A 2D Graphics Environment. Computing in Science & Engineering 9
(2007) 90- 95.
```
```
[ 75 ] M. Waskom, O. Botvinnik, D. O’Kane et al., mwaskom/seaborn: v0.8.1 (September 2017).
Zenodo (2017) Retrieved from https://doi.org/10.5281/zenodo.883859.
```
```
[ 76 ] F. Pedregosa, G. Varoquaux, A. Gramfort et al., Scikit-learn: Machine Learning in Python.
Journal of Machine Learning Research 12 (2011) 2825- 2830.
```
```
[ 77 ] Json, The Python Standard Standard, release 3.9.2. Python Software Foundation. Retrieved
from https://docs.python.org/3/library/json.html#rfc-errata.
```
```
[ 78 ] Collections, The Python Standard Reference, release 3.9.2. Python Software Foundation.
Retrieved from https://docs.python.org/3/library/collections.html.
```
```
[ 79 ] Itertools, The Python Standard Reference, release 3.9.2. Python Software Foundation.
Retrieved from https://docs.python.org/3/library/itertools.html?highlight=itertools.
```
```
[ 80 ] J. Dunbar, C.M. Deane, ANARCI: antigen receptor numbering and receptor classification.
Bioinformatics 32 (2016) 298-300.
```
```
[ 81 ] A. Rives, J., Meier, T., Sercu, S., Goyal, Z., Lin, J., Liu, D., Guo, M., Ott, C.L., Zitnick, J., Ma,
R., Fergus, Biological structure and function emerge from scaling unsupervised learning to 250
million protein sequences, Proceedings of the National Academy of Sciences USA (2021) 118,
e2016239118.
```
```
[ 82 ] A. Elnaggar, M. Heinzinger, C. Dallago, G. Rehawi, Y. Wang, L. Jones, T. Gibbs, T. Feher, C.
Angerer, M. Steinegger, D. Bhowmik, B. Rost, ProtTrans: Toward Understanding the Language of
Life Through Self-Supervised Learning. IEEE Transactions on Pattern Analysis and Machine
Intelligence (2022) 44, 7112-7127.
```
```
[ 83 ] T.H. Olsen, I.H. Moal, C.M. Deane, Addressing the antibody germline bias and its effect on
language models for improved antibody design. bioRXiv ( 2024 ) 10.1101/2024.02.02.578678v1.
```
made available under aCC-BY-NC 4.0 International license.
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is


```
[ 84 ] M. Sandberg, L. Eriksson, J. Jonsson, M. Sjöström, S. Wold, New Chemical Descriptors
Relevant for the Design of Biologically Active Peptides. A Multivariate Characterization of 87
Amino Acids. J Med Chem (1998) 41, 2481- 2491.
```
made available under aCC-BY-NC 4.0 International license.
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is


