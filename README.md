# HYPOTHESIS-DRIVEN EXPERIMENT DESIGN WITH AN EXTENSION TO SED-ML 

Welcome to the Hypothesis-driven experiment design with an extension to SEDML development page! The repository includes the latest version of the Kepler Workflow that is calling the necessary model transformation, experiment execution and analysis code realized in Python. The main goal of this page is to create an entry point for the experimenters who want to design, execute and analyze their experiments starting from hypotheses.

## Introduction
Our ultimate vision is to attempt to provide a design process to guide the experimental scientists by creating an MDE-based ecosystem. Toward this vision, the Global Model Management (GMM) concept leads us to the management of such a complex system. Accordingly, we launched a megamodel that embodies the modelling artefacts of the scientific experimentation methods, and the required groundwork necessitates building a metamodel for simulation experiment megamodels. The convenience of using the megamodel is that the conforming megamodels can be defined and expanded in time by the experimental scientists for their particular experiments. We call the megamodel GMM4SE, short for Global Model Management for Simulation Experiments. GMM4SE identifies the supported types of modelling artefacts as metamodels, transformations, and the relationships between metamodels and model transformations. The user works with them as a cohesive unit, where the artefacts represent data, transformation, or model relationship (e.g., the dependency between the source and target models of model transformation) for a particular megamodel. 

Since our goal is to corroborate a Hypothesis-driven Experiment Design process, we integrated frameworks, DSLs, and a workflow engine that are serving for the experimentation domain into the megamodel. Our proof of concept megamodel specification contains a model-based solution comprised of three kinds of modelling artefacts:
1.	A metamodel for the megamodel, capturing the modelling artefact’s details and their dependencies,
2.	Metamodels and models of the languages for experiment specification (e.g., STL, Xperimenter for Simulation Experiments, SED-ML),
3.	Metamodels and models of the workflow management engines for experiment design, capturing the steps for creating, executing, and analysing the experiments (e.g., Kepler Workflow Management System).

We will give an example to illustrate how to carry out our Hypothesis-driven Experiment Design process with the megamodel and artefacts. The user operations for the model and hypothesis creation are given below:
1.	The user creates a system model for the system under study and collects/generates data sets for the defined system. This system model consists of input and output variables, limits and intervals for these variables, and a tracing formula to mark the time traces of the model for the given hypothesis. The data sets should contain values for the input variables.
2.	The user specifies a hypothesis for a system under study (e.g., hospital bed availability prediction), in a formally defined hypothesis language (e.g., STL specification).

When the user completes the system and hypothesis specification, our workflow for Hypothesis-driven Experiment Design takes action. The workflow handles the model transformation to create an experiment from the specified hypothesis, also manages the execution, validation, and analyses of the generated experiment. The followings explain the main modules that carry out the workflow:
1. Hypothesis 2 Experiment Transformator: is responsible for translating a formal language to an experiment specification (specifically, from ptSTL to Xperimenter model transformation, and SED-ML).
2. Experiment Executor: translates experiment specification into an executable, runs the executable and returns the throughputs (specifically, from Xperimenter to Kepler Workflow Management System).
3. STL Trace Checker: validates if the result of the experiment fits to the user-defined hypothesis, and finds the non-fitting time traces.
4. Analysis Tool Executor: enables analysis options for the user. 


# AN EXAMPLE: A PREDICTIVE ANALYSIS OF HOSPITAL BED AVAILABILITY DURING COVID-19 PANDEMIC

In order to gain a deeper understanding of a megamodel and the process for the hypothesis-driven experiment design (Cam, 2018), we opted for a current and simple study domain to degrade the complexity of the proposed system. We consider that a hospital bed availability prediction system serves excellent for this purpose based on its importance, especially during COVID-19 pandemic. A rise in the number of COVID-19 patients burdens hospitals and it is also a valid indicator of the necessity of taking further measures against the pandemic.

## 1.1. Hospital Bed Availability
The Hospital Bed Availability study is modeled based on the hospitals in the capital city of Turkey, Ankara dedicated to serving the COVID-19 patients in Figure 1. There exist 6 hospitals and these hospitals are intentionally selected as they serve the most of the patients in Ankara. Authorities state that depending on the daily situation and their capacity, the hospitals transfer patients to the closest hospitals. For example, if the Bilkent Sehir Hastanesi gets filled up, the closest hospitals Ankara Gazi Universitesi Hastanesi and Sehit Sait Erturk Devlet Hastanesi will start to admit more patients than average, depending on the increase of daily COVID-19 patients. Thus, keeping the accurate number of occupancy and predicting the possible increase in the number of patients becomes quite important for the healthcare professionals.

<p align="center">
  <img width="600" height="400" src="https://github.com/semacammetu/Hypothesis-driven-experiment-design-with-SEDML-extension/blob/master/stl_fs_sm-master/stl_fs_sm-master/fig15.png" />
</p>
<p align="center">Figure 1. Selected hospitals with Covid-19 services in Ankara</p>

As we propose to study predictive analysis on hospital bed availability, we stipulated two main required data: First is the bed capacity of each hospital, second is the daily number of hospitalized COVID-19 patients in Turkey. However, as of being the capital city of Turkey and its location, hospitals in Ankara also admit patients from other cities due to its hospital capacity. Therefore, a third parameter for the number of COVID-19 patients from neighbor cities are added to the study. Additionally, a state vector retains the number of daily bed occupancy of each hospital i, the number of daily COVID-19 patients j, and the daily number of admitted COVID-19 patients from the neighbor cities k at a certain state. We denote the daily number of bed occupancy hi on each hospital i.

The capacity of the hospitals is given in Table 1. The capacity of the hospitals are 117, 3810, 300, 1150, 115, and 480, respectively. Considering the capacity of the Bilkent Sehir Hastanesi, the hospital becomes the major center where it should raise an alert in case of fullness. Finally, a hospital is considered to be over capacity by having many patients over 80% of the capacity.


| Number 	|                      Hospital Name                     	| Bed Capacity 	|
|:------:	|:------------------------------------------------------:	|:------------:	|
| h0     	| Ankara Gazi Universitesi Hastanesi                     	| 117          	|
| h1     	| Bilkent Sehir Hastanesi                                	| 3810         	|
| h2     	| Diskapi Yildirim Beyazit Egitim ve Arastirma Hastanesi 	| 300          	|
| h3     	| Gulhane education and research hospital                	| 1150         	|
| h4     	| Sehit Sait Erturk Devlet Hastanesi                     	| 115          	|
| h5     	| Yeni Sincan Devlet Hastanesi                           	| 480          	|

Table 1. Selected hospitals with COVID-19 services in Ankara and their capacities (TTB, 2019)</p>

### 1.1.1. System Specification and Data Collection 

(Note that relevant file and code can be found in [Cases in Turkey](stl_fs_sm-master/stl_fs_sm-master/ltl_transformation/cases_turkey.xlsx), [Generated data](https://github.com/semacammetu/Hypothesis-driven-experiment-design-with-SEDML-extension/blob/master/stl_fs_sm-master/stl_fs_sm-master/ltl_transformation/hospital%20data), [GenerateHospitalData.py](https://github.com/semacammetu/Hypothesis-driven-experiment-design-with-SEDML-extension/blob/master/stl_fs_sm-master/stl_fs_sm-master/ltl_transformation/GenerateHospitalData.py))

The identified hospital bed capacity system owns several specific features and constraints (e.g., the number of daily bed occupancy of each hospital and the overall capacity of the hospitals) defining the self and creating the recognized problem. Accordingly, those sets of specifications can be beneficial to introduce the system under investigation to the hypothesis-based experiment design workflow. The followings describe the fundamental specifications for the system under study. The capacity of the variables *j* and *k* were determined based on the total number of selected hospital capacities in Ankara multiplied by 10. The multiplication coefficient 10 represents the percentage of the daily number of hospitalized COVID-19 patients in Turkey, i.e., a maximum of 10% (T.C. Saglik Bakanligi, 2021).

1. An integer array for the number of daily bed occupancy of each hospital, number of hospitalized COVID-19 patients in Turkey and number of admitted COVID-19 patients from neighbor cities counts: *[0, 1, 2, 3, 4, 5, 6, 7]*,
2. An integer array for the non-capacity factors that are numbers representing the number of hospitalized COVID-19 patients in Turkey and number of admitted COVID-19 patients from neighbor cities counts: *[6, 7]*,
3. A map for all the hospitals with their capacity: 
	*'h0': [60, 117], 'h1': [1905,3810], 'h2': [150, 300], 'h3': [575, 1150], 'h4': [57, 115], 'h5': [240, 480], 'j':['0', '59720'], 'k': ['0', '59720']*,
5. A formula to trace the non-fitting time traces of the hospitals calculated with the multiplication of its capacity and the capacity fullness ratio, i.e., 80% (e.g., *h1 < 3048*)

Unfortunately, we found the acquisition of authentic test data difficult as they are not shared per city by the Turkish authorities. This impediment motivated us toward data generation alternatives for the prevalent problem domain, i.e., hospital bed availability during COVID-19. Therefore, for the purpose of this study, a data generation algorithm that simulates a system under study from random initial states was employed to create data sets for the hospital bed availability in Ankara during COVID-19. The algorithm generates data for the daily number of the occupied beds of each hospital and the transferred number of patients from the neighboring cities. The generated data were randomized upon the COVID-19 numbers shared by the Republic of Turkey Ministry of Health (Republic of Turkey Ministry of Health, 2021), i.e., number of patients for today. We assumed that the hospitals had half of their capacity was already occupied by non-COVID-19 patients, when the pandemic has started. The algorithm essentially builds data sets from random initial conditions for a provided number of time traces. The data contains the temporal operator P(previously) and the time interval *[0, 101]*. Although valuable for generating lots of data, this algorithm has the disadvantage of generating relatively small non-fitting data.

The decisions about data generation made upon a requirement that the overall time traces for a single hospital avoiding the fullness should be as approximate as possible to the hospital's fullness measure, i.e., 80%. As a result, we obtained 4 different data sets, and each data set contains 101 sequential time traces for every hospital and noncapacity variables that are number of hospitalized COVID-19 patients in Turkey and number of admitted COVID-19 patients from neighbor cities. We eventually achieved 404 time traces representing the last 14 months of COVID-19, where 62 of the time traces have hospital h1 with over 80% capacity, i.e., *h1 > 3048*.


### 1.1.2. Hypotheses about Hospital Bed Availability in Ankara during COVID-19
Hospital bed availability became one of the major concerns in many countries during the COVID-19 pandemic. Discovering the conditions causing this fatal problem, at least in Ankara, before it aggravates is the concern of this case study. Thus, we formulated our concern based on the previously established steps of the scientific process in the Introduction section, with an appropriate question addressing the problem and hypotheses targeting to solve the problem. Specifically, the formalized questions as ptSTL formulas describe the hypotheses.
1. **Question**: What are the conditions that originate fulness on hospital h1 on the next day? 
2. **Conditions**: The following conditions, defined according to the formal specification originate fullness on hospital h1 on the next day:

<p align="center">
  <img src="https://github.com/semacammetu/Hypothesis-driven-experiment-design-with-SEDML-extension/blob/master/stl_fs_sm-master/stl_fs_sm-master/eq1.png" />
</p>												
	
	
	Each sub-formula &theta;<sub>1, &theta;<sub>2 and &theta;<sub>3 states a condition that leads to fullness on hospital h1 on the next day.

	* &theta;<sub>1 : on the occasion of more than 1500 patients at hospital h1, the number of hospitalized COVID-19 patients is more than 3000, and more than 50 patients get transfered to Ankara,
	* &theta;<sub>2 : on the occasion of more than 2500 patients at hospital h1 and the number of hospitalized COVID-19 patients is more than 3000, 
	* &theta;<sub>3 : on the occasion of more than 900 patients at hospital h3, the number of hospitalized COVID-19 patients is more than 3000, and more than 50 patients get transfered to Ankara.

3. **Null hypothesis (H0)**: If one of the condition occurs, then the hospital h1 observes fullness by growing 80% over its capacity where the condition is *h1 > 3048*.
4. **Alternative hypothesis (H1)**: If one of the condition occurs, then the hospital h1 does not observe fullness by growing 80% over its capacity where the condition is *h1 <= 3048*.

We assign our individual hypothesis-based experiment design workflow in Figure 2 (**[Go to Kepler workflow](https://github.com/semacammetu/Hypothesis-driven-experiment-design-with-SEDML-extension/blob/master/Kepler/HypothesisBasedExperimentGeneratorForHospital.kar)**) for the remainder of the steps (4, 5, 6, and 7) of the scientific process. In the following sections, we explain how the work ow supervises the complete list of experiment procedures sequentially; specifically, design, execution, validation, and analysis.

<p align="center">
  <img src="https://github.com/semacammetu/Hypothesis-driven-experiment-design-with-SEDML-extension/blob/master/stl_fs_sm-master/stl_fs_sm-master/fig10.png" />
</p>
<p align="center">Figure 2. The Kepler workflow for hypothesis-based experiment design</p>


## 1.2. Hypothesis to Experiment Model Transformations ([Go to code](https://github.com/semacammetu/Hypothesis-driven-experiment-design-with-SEDML-extension/blob/master/stl_fs_sm-master/stl_fs_sm-master/ltl_transformation/Hypothesis2Experiment.py))

Following the fulfillment of the user operations for the system under study, Hypothesis 2 Experiment Transformator module, i.e., the primary step in Figure 2, initiates the simulation experiment workflow. Having the system specifications and the hypotheses is the compulsory provision to employ the tasks for SED-ML model generation from system specification and from SED-ML to Xperimenter model transformation. It is pertinent to remark that generated datasets are only necessary for the later phases of the workflow, e.g., experiment execution. 

The module, an individualized Python script, is solely liable for the experiment model obtaining in two ways: model generation and model transformation. For this study, we underline how we interpret these two similar tasks: while we describe the model transformations as a practice over two or more conventional models serving the same domain, e.g., DSLs, we contemplate the data generation as another practice between any custom specification. In light of this, Hypothesis 2 Experiment Transformator practices the following functions:
1. From user-defined system specification to SED-ML model generation,
2. From SED-ML to Xperimenter model transformation.

The following sections explain the proposed hypothesis extension to SED-ML alongside the model generation, and SED-ML to Xperimenter model transformations, sequentially.

### 1.2.1. Hypothesis Extension to SED-ML 
(Note that relevant SED-ML file & code can be found in [SEDML with hypothesis](https://github.com/semacammetu/Hypothesis-driven-experiment-design-with-SEDML-extension/blob/master/stl_fs_sm-master/stl_fs_sm-master/ltl_transformation/SEDML_with_hypothesis.xml), [GenerateSedML.py](https://github.com/semacammetu/Hypothesis-driven-experiment-design-with-SEDML-extension/blob/master/stl_fs_sm-master/stl_fs_sm-master/ltl_transformation/GenerateSedML.py))

We propose a hypothesis extension to SED-ML to attain a solution for the lacking association issue between an experiment and its hypothesis. The proposed SED-ML
model gracefully interprets the STL semantics into a markup language, i.e., XML. The followings clarifies how the user-defined system specification and the hypotheses describe the SED-ML model accordingly with Table 2. We set the default initial values for the SED-ML model generation with the fact that one experiment associated with a single task and an experiment model can suffciently prove or refute a list of hypotheses enclosed to a question.
1. An integer array for the number of daily bed occupancy of each hospital, the number of hospitalized COVID-19 patients, and admitted COVID-19 patients from the neighbor cities: transformed into variables in the data generator of a task,
2. A map for hospital capacities: transformed into variable limits,
3. Hypotheses: transformed into list of hypotheses.

| System specifications 	|                          SED-ML                          	|
|:---------------------:	|:--------------------------------------------------------:	|
| hypotheses            	| listOfHypotheses                                         	|
| default               	| initial values for a single simulation listOfSimulations 	|
| default               	| initial values for a single model listOfModels           	|
| default               	| initial values for a single task listOfTasks             	|
| system specification  	| listOfDataGenerators                                     	|

Table 2. User-defined specifications to SED-ML Mapping

For the sake of simplicity and readability of the SED-ML model, we only presented the extended listOfHypotheses for a single variable part of the generated SED-ML model in the Listing below. A hypothesis in SED-ML consists of an expression that defines the hypothesis, itself, and three conditions with multiple expressions, and the expression relations are defined with and for this specific example. The temporalOperators are *P[1, 1]* for each condition and expression. And, the relation entity is used to explain the hypothesis H0 with its conditions for refuting or proving, as there is a single hypothesis. It is important to note that H1 uses the same conditions with H0, as the relation between the hypotheses is *CONTRADICT*.
Finally, H0 has a referenceModel that relates the expressions to an actual model.
```xml
	1 <listOfHypotheses>
	2 	<hypothesis metaid="H0">
	3		<listOfExpressions>
	4			<expression expr="h1 > 3048">
	5				<temporalOperator opr="P[1, 1]" />
	6			</expression>
	7		</listOfExpressions>
	8		<listOfConditions>
	9 			<condition metaid="C1">
	10 				<temporalOperator opr="P[1, 1]" />
	11				<expression expr="h1 > 1500"/>
	12 				<operator opr="and"/>
	13 				<expression expr="j > 3000"/>
	14 				<operator opr="and"/>
	15 				<expression expr="k > 50"/>
	16 			</condition>
	17 			<condition metaid="C2">
	18 				<temporalOperator opr="P[1, 1]" />
	19 				<expression expr="h1 > 2500"/>
	20 				<operator opr="and"/>
	21 				<expression expr="j > 3000"/>
	22		 	</condition>
	23			<condition metaid="C3">
	24				<temporalOperator opr="P[1, 1]" />
	25				<expression expr="h3 < 900"/>
	26 				<operator opr="and"/>
	27				<expression expr="j > 3000"/>
	28				<operator opr="and"/>
	29		        	<expression expr="k > 50"/>
	30 			</condition>
	31 		</listOfConditions>
	32 		<referenceModel model="model"/>
	33 	</hypothesis>
	34	<hypothesis metaid="H1">
	35 		<listOfExpressions>
	36 			<expression expr="h1 <= 3048">
	37				  <temporalOperator opr="P[1, 1]" />
	38 			</expression>
	39 		</listOfExpressions>
	40 	</hypothesis>
	41	<listOfRelations>
	42		<relation relation="CONTRADICT">
	43 			<hypothesis hyp="H0"/>
	44			<hypothesis hyp="H1"/>
	45  	     	</relation>
	46 	</listOfRelations>
	47 </listOfHypotheses>
	48 <listOfModels>
	49 	<model metaid="model" source="/sourceModel" />
	50 </listOfModels>
```

### 1.2.2. SED-ML to Xperimenter Model Transformation 
(Note that relevant Xperimenter file & code can be found in [xperimenter.xpr](https://github.com/semacammetu/Hypothesis-driven-experiment-design-with-SEDML-extension/blob/master/stl_fs_sm-master/stl_fs_sm-master/ltl_transformation/xperimenter.xpr), [GenerateXperimenter.py](https://github.com/semacammetu/Hypothesis-driven-experiment-design-with-SEDML-extension/blob/master/stl_fs_sm-master/stl_fs_sm-master/ltl_transformation/GenerateXperimenter.py))

The generation of another experiment model alongside the SED-ML is an essential effort to enrich the megamodel for the experimenters. The intention supporting this effort is to encourage the experimenters to develop their DSLs serving their particular needs, introduce them to the megamodel, and find common ground to bestow the knowledge. With this in mind, we undertook the Xperimenter model transformation from SED-ML, and achieved the Xperimenter model in the Listing below. We opted to apply model transformation from SED-ML to Xperimenter rather than the STL to Xperimenter. Because the SED-ML specification represents a formal model for capturing the essentials of simulation experiments including hypotheses and this method improves the ability to create traceability to the lower models, i.e., Xperimenter. It is crucial to note that the STL formula defining the hypotheses was given as user input. In order to keep the originality of the Xperimenter model and as it was not a primary goal in this research, those inputs were not translated into Xperimenter and processed by the Python script in the following Experiment Execution section. 
```java
	1  experiment experiment{
	2 	desc "predictive analysis on hospital bed availability";
	3 	objective COMPARATIVE;
	4 	design design;
	5 	simulation simulation;
	6 	visual DEFAULT;
	7 	target KEPLER;
	8  }
	9  variable h0: INTEGER group FACTOR [0, 117];
	10 variable h1: INTEGER group FACTOR [0, 3810];
	11 variable h2: INTEGER group FACTOR [0, 300];
	12 variable h3: INTEGER group FACTOR [0, 1150];
	13 variable h4: INTEGER group FACTOR [0, 115];
	14 variable h5: INTEGER group FACTOR [0, 480];
	15 variable j: INTEGER group FACTOR [0, 59720];
	16 variable k: INTEGER group FACTOR [0, 59720];
	17 design design{
	18 	method FULLFACTORIAL;
	19 	varlist h0 h1 h2 h3 h4 h5 j k ;
	20 }
	21 simulation simulation{
	22 	modelFile /hospital_data/;
	23 	modelType DISCRETEEVENT;
	24 	inport h0: h0;
	25 	inport h1: h1;
	26 	inport h2: h2;
	27 	inport h3: h3;
	28 	inport h4: h4;
	29 	inport h5: h5;
	30 	inport j: j;
	31 	inport k: k;
	32 }
```

The model transformation from SED-ML to Xperimenter is a relatively straightforward duty as both of the SED-ML and Xperimenter models possess many mutual variables. Table 3 summarizes the variable mapping effort from SED-ML to Xperimenter. An Xperimenter model starts with an experiment specification containing a description, an objective, a design, a simulation, an analysis, a visual and a target information. The model and simulation variables from SED-ML is equivalent to the same variables in Xperimenter. Having said that, while the task is representing the experiment, the dataGenerator and output collectively represents variable in Xperimenter. And, variable of the task are transformed into varList of design for Xperimenter.

|     SED-ML    	|   Xperimenter  	|
|:-------------:	|:--------------:	|
| model         	| model          	|
| simulation    	| simulation     	|
| task          	| experiment     	|
| dataGenerator 	| variable       	|
| output        	| variable       	|
| task.variable 	| design.varList 	|

Table 3. SED-ML to Xperimenter Variable Mapping

## 1.3. Experiment Execution ([Go to code](https://github.com/semacammetu/Hypothesis-driven-experiment-design-with-SEDML-extension/blob/master/stl_fs_sm-master/stl_fs_sm-master/ltl_transformation/ExperimentRunnerForHospital.py))

Once achieving the experiment models, the execution phase of the experimentation process inaugurates the workflow for the execution. The experiment execution module, i.e., the second step in Figure 2, exclusively consists of a Python script that takes the generated data sets, the user-defined system specification, and the previously generated SED-ML model as inputs and determines the time traces that prove and refute the hypotheses. The script is fundamentally responsible for the following tasks:
1. Interpreting experiment model, i.e., SED-ML specification, to collect the hypotheses,
2. Interpreting the data set on the basis of the system specifications,
3. Executing the conditions against the data set to find the hypothesis proving and refuting time traces. 

The experiment run accumulates throughputs for the number of successful and failing conditions, the overall number of time traces, the number of skipped data, and finally prints out the results in Figure 3. The screenshot precisely contains the following information:
1. The number of time traces that successfully prove the conditions,
2. The number of the filled h1 traces where previous traces refute the conditions,
3. The number of non-fitting time traces that refute the conditions where the next trace is not over the capacity (*h1 < 3048*),
4. The overall number of skipped time traces due to the non-fitting conditions for the hypotheses,
5. The overall number of traces that the experiment used, excluding the first ten time traces in each dataset to enhance the quality of the input by eliminating the initial  randomized time traces.

<p align="center">
  <img src="https://github.com/semacammetu/Hypothesis-driven-experiment-design-with-SEDML-extension/blob/master/stl_fs_sm-master/stl_fs_sm-master/fig12.png" />
</p>
<p align="center">Figure 3. Hospital bed availability experiment result including the time steps with the hospital capacities that proving the hypothesis</p>
		
## 1.4. Experiment Validation ([Go to code](https://github.com/semacammetu/Hypothesis-driven-experiment-design-with-SEDML-extension/blob/master/stl_fs_sm-master/stl_fs_sm-master/ltl_transformation/HypothesisChecker.py))

Trace analysis is a useful technique for verifying formal proofs. A trace checker analyses the traces and outlines any violations of the profiered formula. Due to its frugality and practicality of the method, employing a trace checker for STL specifications appears to be reasonable in terms of experiment result validation in this study. Taking that into consideration, we employed the STL Trace Checker (Ergurtuna and Gol, 2019) to validate the experiment output that we formerly conducted. The trace checker takes the previously stated conditions for the hospital bed availability analysis for the hospital h1 alongside the generated datasets and returns the proving and disproving data traces. The output of the STL Trace Checker appears to tally with our expectations for the number of the traces providing the conditions, i.e., 62, and the number of the traces the disproving the conditions, i.e., 4. 

Based on the quantitative comparison of the throughputs from the STL Trace Checker and the experiment run we conducted, we also observed that the throughputs are consistent with the analysis reported by us. The compatibility of the analysis results demonstrates the adequacy of using a trace checker for the validation of formally specified hypotheses.

## 1.5. Experiment Analysis ([Go to code](https://github.com/semacammetu/Hypothesis-driven-experiment-design-with-SEDML-extension/blob/master/stl_fs_sm-master/stl_fs_sm-master/ltl_transformation/AnalysisTool.py))

The final phase of the scientific experimentation process is to evaluate the acquired throughputs with the help of prevalent analytical methods. These analytical techniques assist in collecting and modeling data in the process of decision making. We, hence, offer an STL based experiment statistical analysis software, embedded in the workflow as the final step in the Figure 2, that helps the experiment designers in their endeavour of data analysis. The proposed statistical analysis tool utilizes the statistical capabilities of the Python programming language.
The tool is capable of applying the following statistical methods on a given dataset:
1. Proving or refuting an STL formula on a dataset,
2. Applying the following statistical analysis:
	1. Histogram of data sets
	2. Linear regression
	3. Statistical summary
We opted for a humble statistical search to scrutinize the utilized datasets in terms of the quality aspect, and for the illustration purposes of the offered analytical tool. To attain this objective, we revisit and expand the formerly exploited hypotheses specification with a condition where the hospital h1 has a number of patients less than 80% of its capacity in the next trace.

<p align="center">
  <img src="https://github.com/semacammetu/Hypothesis-driven-experiment-design-with-SEDML-extension/blob/master/stl_fs_sm-master/stl_fs_sm-master/eq2.png" />
</p>
	
The execution of the analysis produces graphical throughput in Figure 4. The throughput highlights that in every five trace intervals for the aggregated dataset, there exist two or more traces that refute the hypothesis. Bear in mind that the graphic depicts the aggregation of the 4 different datasets where each dataset contains *101* traces. Explained differently, approximately *1 traces in 101* traces disprove the hypothesis, and the analysis outcome is considerably close to our experiment result for the refuting cases. The significance of this analysis for the data quality can be assumed marginal regarding the aim of the study, i.e., having a complete work ow for the simulation experiment.

<p align="center">
  <img width="400" height="300" src="https://github.com/semacammetu/Hypothesis-driven-experiment-design-with-SEDML-extension/blob/master/stl_fs_sm-master/stl_fs_sm-master/fig13.png" />
</p>
<p align="center">Figure 4. Time traces of the hospital capacities that refute the hypothesis</p>


# REFERENCES
1. Cam, S., Dayibas, O., Gorur, B.K., Oguztuzun, H., Yilmaz, L., Chakladar, S., Doud, K., Smith, A.E., and Teran-Somohano, A., Supporting simulation experiments with megamodeling. In Proceedings of the 6th International Conference on Model-Driven Engineering and Software Development - Volume 1: MODELSWARD,, pages 372{378. INSTICC, Sciteress, 2018.
2. TTB ANKARA TABiP ODASI, 2019. Verilerle Ankara'nin Sagligi. Retrieved May 5, 2021, from https://ato.org.tr/_les/documents/ATO 
3. T.C. Saglik Bakanligi. COVID-19 Durum Raporu. Retrieved May 5, 2021, from https://covid19.saglik.gov.tr/TR-68443/covid-19-durum-raporu.html
4. Republic of Turkey Ministry of Health (2021). COVID-19 Information Page, General Coronavirus Table. Retrieved May 6, 2021, from https://covid19.saglik.gov.tr/EN-69532/general-coronavirus-table.html.
5. Ergurtuna, M., and Aydin Gol, E., An effcient formula synthesis method with past signal temporal logic, 2019.
