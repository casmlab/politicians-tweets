# Dataset of Indian and US politicians as on July 22, 2020

This repository contains the dataset of politicians' Twitter handles we have compiled for India and the United States. These handles were collected as a part of the [NivaDuck](https://dl.acm.org/doi/abs/10.1145/3400806.3400830) project (NivaDuck is the Marathi word for selector). Please cite the paper from the link above if you plan to use the data in publications. 
Detailed credits for collaborators are provied in the Team Section.

## Team
- [Anmol Panda](https://anmolpanda.github.io/) - Building NivaDuck, annotating and verifying politician data
- [A'ndre Gonawela](https://scholar.google.com/citations?user=twTvND0AAAAJ&hl=en) - Bulding the seed set for the US version, verifying sample of politicians to estimate precision
- [Sreangsu Acharyya](https://dblp.org/pers/a/Acharyya:Sreangsu.html) - Design of NivaDuck's classifiers
- [Dibyendu Mishra](https://www.linkedin.com/in/dibyendu-mishra/?originalSubdomain=in) - Verifying politicians, annotating politicians with metadata, and complementing final output by adding missing politicians of the India version
- [Mugdha Mohapatra](https://www.linkedin.com/in/mugdha-mohapatra-372548143/?originalSubdomain=in) - Annotating politicians with metadata, writing code to match Twitter handles to ECI database for the India version
- [Ramgopal Chandrasekaran](https://scholar.google.com/citations?user=uiReuCAAAAAJ&hl=en) - Verifying politicians, annotating politicians with metadata, and complementing final output by adding missing politicians for the India version
- [Venkatesh Thapan]( https://www.linkedin.com/in/venkatesh-thapan-b07187119/) - Adding missing politicians for the India dataset
- [Sachita Nishal](https://nishalsach.github.io/) - Adding missing politicians for the India dataset
- [Divyanshu Kukreti](https://github.com/Divyanshu718) - Adding missing politicians for the India dataset
- [Lia Bozarth](https://lbozarth.github.io/) - Seed set for Indian politicians
- [Ramaravind Kommiya Mothilal](https://raam93.github.io/) - Verifying and annotating politicians with metadata for the India dataset
- [Azhagu Meena](https://scholar.google.com/citations?user=A4drjU4AAAAJ&hl=en) - Verifying and annotating politicians with metadata for the India dataset
- [Zainab Akbar](https://scholar.google.com/citations?user=NXFwzv0AAAAJ&hl=en) - Preparing updated set of Indian MPs, verifying and annotating politicians  with metadata for the India dataset
- [Faisal Lalani](https://www.linkedin.com/in/faisalmlalani/) - Verifying and annotating politicians  with metadata for the India dataset
- [Ashwin Rajadesingan](https://ashwinrajadesingan.com/) -  Verifying politicians
- Udit Thawani -  Verifying politicians
- Reeshma Kumar -  Verifying politicians
- Tanvi Madhani -  Verifying politicians
- [Joyojeet Pal](https://www.microsoft.com/en-us/research/people/jopal/) -  Project Architect
<!--, research advisor and manager of the NivaDuck project and the dataset of politicians at Microsoft Research India -->

## Data
We are publishing the list of Twitter handles compiled as of July 22, 2020. This list is subject to updation (addition, removal and change in metadata) as politicians change parties, more false positives are identified, and new politicians arrive. The metadata consists of state and party annotations for about half the Indian handles and state annotations almost all of the USA handles. For the remaining accounts, we are adding and verifying metadata and will update this repository at regular intervals.

## Methods
For the India set, roughly 17K handles were found by NivaDuck. These were complemented, verified and annotated (with metadata) by human coders. Additionally roughly 18K handles were manually added from amongst friends of these politicians by [Sachita Nishal](https://nishalsach.github.io/), [Venkatesh Thapan](https://www.linkedin.com/in/venkatesh-thapan-b07187119/), and [Divyanshu Kukreti](https://github.com/Divyanshu718). The latter do not have state and party annotations yet and will be added in due course.
Barring the seed set for the US data, the remaining accounts were gathered using NivaDuck and were verified and annotated by [Anmol Panda](https://anmolpanda.github.io/) and [A'ndre Gonawela](https://scholar.google.com/citations?user=twTvND0AAAAJ&hl=en). We are working to complement this set using the same procedure as the India dataset to get a more comprehensive dataset of political figures in the US.

## Future work
Currently NivaDuck, trained for high precision, suffers from low recall and misses out on many politicians, necessiating significant human effort (see [paper](https://dl.acm.org/doi/abs/10.1145/3400806.3400830) for details). We aim to work towards improving the current classification pipeline and adding new functionality to alleviate the precision-recall trade-off. 

