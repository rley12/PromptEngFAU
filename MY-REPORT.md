![GenI-Banner](https://github.com/genilab-fau/genial-fau.github.io/blob/8f1a2d3523f879e1082918c7bba19553cb6e7212/images/geni-lab-banner.png?raw=true)

# The Effect of Varying Context and Token Numbers on Prompt Results

To observe the impact of model request parameters on the response to requirement analysis prompt.

* Authors: Rodrigo Ley
* Academic Supervisor: [Dr. Fernando Koch](http://www.fernandokoch.me)

  
# Research Question 

What is the impact of varying model request parameters on the results of prompts?

## Arguments

#### What is already known about this topic

* Context value determines the context window size. Higher context improves accuracy, coherence, and revelancy of the response. But also increases resource usage.
* Predict value controls the number of tokens generated. Higher values allow for more detailed or longer responses, especially important if the prompt is technical or complex. But it could lead to verbose or irrelevant information, along with increased resource usage.

#### What this research is exploring

* My aim, as a student, was:
* Explore how the value of the context and prediction parameters would impact the quality of the response to a prompt. This gave me more insight into LLMs as not just a black-box, or a monolithic entity.

* Explore the automation of automation. 16 different responses were generated (4 context parameter values x 4 prediction  parameter values). While these can be judged by a human, this is subjective, time-consuming and (if enough variations are explored) impractical to assess. So the assessment itself was done by a LLM.

* Explore multi-step chain prompting for requirement analysis

#### Implications for practice

* Iterative experimentation with various LLM parameters will help optimize results of the prompt. For example, the number of tokens could result in a lengthy and/or less relevant response. 
* In my case, I plan to continue to run and use these LLMs locally. But I have an older computer, which crashed several times as I tried doing the iterations. So I had to try lighter models until I settled on 0.5B Qwen2.5. So, performance and system stability is a consideration for me and testing various parameter values was part of that. As seen in the code, this experiment included tracking the run time, but I could have also recorded resource usage (I sporadically observed it on the terminal).


# Research Method

Using the Prompt Engineer Lab provided at FAU, I iteratively prompted the LLM. Details are: 
* Model: 0.5B Qwen2.5
* Context value: 1000, 10000, 50000 and 100000
* Predict value:  1000, 10000, 50000 and 100000
* Prompt: "Step 1: Generate a list of potential data sources for stock sentiment analysis (e.g., Twitter, news articles, Reddit, financial reports). Step 2: Identify the key financial metrics that influence stock overvaluation. Step 3: Based on steps 1 and 2, define the system requirements for an AI tool that integrates sentiment and fundamental analysis.".
* Other model parameters were untouched from the default settings set in the repo.

The run-time was logged and output was exported. The output was then fed to ChatGPT to score the results from a range of 1-10 (with 10 being the best), and the instructions being to score based on which response most adequately fufills the prompt. I manually skimmed the results too, to collaborate the score.


# Results
The output can be seen in Output.md file.
* Scores:
  
| num_ctx \ num_predict | 1000 | 10000 | 50000 | 100000 |
|----------------------|------|-------|-------|--------|
| **1000**   | 7  | 8  | 9  | 8  |
| **10000**  | 7  | 9  | 8  | 9  |
| **50000**  | 6  | 7  | 9  | 9  |
| **100000** | 8  | 9  | 8  | 10 |



* Ranking from 1 - 16 (several ties):
  
| num_ctx \ num_predict | 1000 | 10000 | 50000 | 100000 |
|----------------------|------|-------|-------|--------|
| **1000**   | 7  | 6  | 2  | 5  |
| **10000**  | 8  | 3  | 6  | 3  |
| **50000**  | 14 | 11 | 3  | 3  |
| **100000** | 9  | 3  | 7  | 1  |

* Run time (s):
  
| num_ctx \ num_predict | 1000 | 10000 | 50000 | 100000 |
|----------------------|------|-------|-------|--------|
| **1000**   | 20  | 13  | 12  | 13  |
| **10000**  | 18  | 11  | 13  | 14  |
| **50000**  | 43  | 40  | 30  | 30  |
| **100000** | 47  | 25  | 13  | 32  |

Interestingly, there is not a straightforward relationship between the parameters and run-time. Increasing context size does generally results in more time, but it is not clear what context's impact is.


# Further research

Other parameters could be modified, such as temperature. In this case, where the topic is a technical one but with some creativity possibly needed, all these parameters are worth trying in determining the best ones. Also, other system performance metrics could be added and automatically tracked (outside of run-time), if we are consider system stability as was my case with my older computer.
