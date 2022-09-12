This project aimed at building an interpretable framework to integrate toxic language annotations. Most data sets address only one aspect of the complex relationship in toxic communication and are inconsistent with each other. Enriching annotations with more details and information is, however, of great importance in order to develop high-performing and comprehensive explainable language models. Such systems should recognize and interpret both expressions that are toxic as well as expressions that make reference to specific targets to combat toxic language. We, therefore, create a crowd-annotation task to mark the spans of words that refer to target communities as an extension of the HateXplain data set. We presented a quantitative and qualitative analysis of the annotations. We also fine-tuned RoBERTa-base on our data and experimented with different data thresholds to measure their effect on the classification. The F1-score of our best model on the test set is 79%. The annotations are freely available and can be combined with the existing HateXplain annotations to build richer and more complete models. For more information, you can refer to our paper via the link below:<br>
example_link<br><br>
Colab notebooks contain the codes for fine-tuning RoBERTa-base langauge models with different threholds on the training set and obtaining the predictions on the test set that have been created with a fixed UQS threshold (50)<br>
-UQS threshold = 50: https://colab.research.google.com/drive/143tvkcNAPd7bbr4vVAIznHc1lBHy6G-q?usp=sharing<br>
-UQS threshold = 60: https://colab.research.google.com/drive/1J4av7UrmIIUUA5-WG4jEYH6UMy4xPJS0?usp=sharing<br>
-UQS threshold = 70: https://colab.research.google.com/drive/1b7hVVTxA67cGiTKaae9VrrUrq5vR4NEG?usp=sharing<br><br>
Fine-tuned models on Hugging Face:<br>
-UQS threshold = 50: BBarbarestani/RoBERTa_HateXplain_Target_Span_Detection_UQS_Threshold_50_2_Previous_Hyperparameters<br>
-UQS threshold = 60: BBarbarestani/RoBERTa_HateXplain_Target_Span_Detection_UQS_Threshold_60_2<br>
-UQS threshold = 70: BBarbarestani/RoBERTa_HateXplain_Target_Span_Detection_UQS_Threshold_70_2<br><br>

##Folder Descriptions:<br>
1- HateXplain data modified + creation of batches: It contains codes on how the HateXplained data set was organized based on sorted target groups and then the target groups were evenly distributed across the data set. The way samples were selected and preprocessed has been explained in the paper.<br>
2- annotation batches: The raw batches created based on the proposed selection of the HateXplain data set.<br>
3- annotation platform: It contains all the files that have been created or modified for designing the annotation task uisng LingoTURK. For more information on LingoTURK and how it works, please visit "https://github.com/FlorianPusse/Lingoturk".<br>
4- annotation results: It contains the annotated 120 batches and all the information collected from the crowd. The "batches 1- 120" folder includes some general post-analysis on the whole collected data, especially based on the UQS scores achieved.<br>
4- annotations analysis + reports: It contains codes on how some of the analyses were carried out on the achieved annotations from the crowd and experts and reports on the results.<br>
classification: It contains codes on how the data were prepared to be fed into the langauge models for the classification task.<br><br>
##Remarks:<br>
1- Most but not all of the available codes are examples codes, which means that they have been written for a certain input file, UQS threshold, number of batches, etc. If you want to, for example, run them with a different score, data set, etc, you should modify them and give your own input file and parameters.<br>
2- The annotation platfrom used for recruiting the crowd was prolific (https://www.prolific.co)<br><br>
##Requirements:<br>
1- LingoTURK for designing the task (more information on https://github.com/FlorianPusse/Lingoturk)<br>
2- CrowdTruth for calculating the inter-annotator agreement scores and analyzing the annotations (https://github.com/CrowdTruth/CrowdTruth.git)<br>
3- 
